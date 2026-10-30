#!/usr/bin/env python3
"""Frozen, three-arm fictional capture-to-fresh-resumer transfer experiment."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import threading
import time
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from metrics import (CRITERIA, consistency, paired_difference, parse_json, score_trial,
                     summarize, validate_capture, validate_evidence, validate_judgment, validate_resume)
from prompts import CAPTURE_SCHEMA, RESUME_SCHEMA, JUDGE_SCHEMA, JUDGE_SYSTEM, NEUTRAL, capture_prompt, judge_prompt, participant_evidence, resume_prompt
from providers import ProviderError, call

CONDITIONS = ('skill', 'baseline', 'placebo')


def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


def treatment():
    paths = [ROOT / 'skills/project-handoff/SKILL.md'] + sorted((ROOT / 'skills/project-handoff/references').glob('*.md'))
    if not paths[0].is_file() or len(paths) < 2:
        raise ValueError('Canonical skill and references are required')
    return '\n\n'.join('--- SOURCE ' + str(p.relative_to(ROOT)) + ' ---\n' + p.read_text() for p in paths)


def placebo_for(skill):
    pool = (HERE / 'placebo.txt').read_text()
    words = len(skill.split())
    if len(pool.split()) < words:
        raise ValueError('Generic placebo corpus is shorter than the treatment')
    selected = ' '.join(pool.split()[:words])
    if '.' in selected:
        selected = selected.rsplit('.', 1)[0] + '.'
    if abs(len(selected.split()) - words) / words > .05:
        raise ValueError('Placebo length must be within five percent')
    return selected


def sources():
    paths = list((ROOT / 'skills/project-handoff').rglob('*.md'))
    paths += list(HERE.glob('*.py')) + [HERE/'fixtures.json', HERE/'key.json', HERE/'placebo.txt', ROOT/'docs/BENCHMARK.md']
    return {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in sorted(paths)}


def validate():
    fs = json.loads((HERE/'fixtures.json').read_text())
    key = json.loads((HERE/'key.json').read_text())
    assert len(fs) == 10 and len({f['id'] for f in fs}) == len(fs)
    assert set(key) == {f['id'] for f in fs}
    assert all(f['fictional'] and f['capture_files'] and f['resume_files'] for f in fs)
    assert sum(k['leave_alone_applicable'] for k in key.values()) >= 1
    assert any(not f['write_authorized'] for f in fs)
    assert all('expected' not in capture_prompt(f) and 'leave_alone_applicable' not in capture_prompt(f) for f in fs)
    marker = 'CAPTURE_ONLY_SENTINEL'
    f = dict(fs[0], session=[marker])
    assert marker not in resume_prompt(f, 'A handoff')
    text = treatment()
    placebo = placebo_for(text)
    return fs, key, text, placebo


class BudgetExceeded(RuntimeError):
    pass


class Budget:
    def __init__(self, config, existing=()):
        self.config, self.lock = config, threading.Lock()
        self.started = time.monotonic()
        self.calls = len(existing)
        self.spent = sum(x.get('nominal_usd') if x.get('nominal_usd') is not None else x.get('reserved_usd', 0) for x in existing)
        self.tokens = sum(x.get('result', {}).get('output_tokens') if isinstance(x.get('result', {}).get('output_tokens'),int) else x.get('max_tokens',0) for x in existing)

    def invoke(self, role, system, user, path, response_schema=None):
        cfg = self.config
        provider = 'openai' if role == 'evaluated' else 'anthropic'
        model = cfg['model'] if role == 'evaluated' else cfg['judge']
        max_tokens = cfg['max_tokens'] if role == 'evaluated' else cfg['judge_max_tokens']
        rates = cfg['rates'][role]
        # Bytes + 2048 is a conservative request-token reservation for this text-only interface.
        input_upper = len((system+user).encode()) + 2048
        reserve = (input_upper*rates[0] + max_tokens*rates[1])/1e6
        with self.lock:
            if self.calls >= cfg['max_calls'] or self.tokens + max_tokens > cfg['max_generated_tokens']:
                raise BudgetExceeded('Hard call or generated-token limit reached')
            if self.spent + reserve > cfg['budget_usd']:
                raise BudgetExceeded('Nominal uncached dollar reservation limit reached')
            remaining = cfg['max_seconds'] - (time.monotonic() - self.started)
            if remaining <= 0:
                raise BudgetExceeded('Wall-clock budget reached')
            self.calls += 1
            self.tokens += max_tokens
            self.spent += reserve
        record = {'provider':provider,'requested_model':model,'role':role,'system':system,'user':user,
                  'system_hash':digest(system),'user_hash':digest(user),'max_tokens':max_tokens,
                  'response_schema':response_schema,
                  'reserved_usd':reserve,'nominal_usd':None}
        try:
            result = call(provider, model, system, user, max_tokens, timeout=max(1,min(60,remaining)),response_schema=response_schema)
            if not isinstance(result['input_tokens'],int) or not isinstance(result['output_tokens'],int):
                record['result']=result
                dump(path,record)
                raise ProviderError('Provider response lacks usage')
            actual = (result['input_tokens']*rates[0]+result['output_tokens']*rates[1])/1e6
            record.update(result=result, nominal_usd=actual)
            with self.lock:
                self.spent += actual-reserve
                self.tokens += result['output_tokens']-max_tokens
            dump(path, record)
            if not result.get('complete') or not result.get('text'):
                raise ProviderError('Provider response incomplete; partial output retained')
            if not result.get('requested_model_match'):
                raise ProviderError('Provider resolved model differs from requested snapshot; output retained')
            return result['text']
        except Exception as exc:
            # Transport messages are fixed strings; never persist arbitrary provider bodies.
            record['error'] = type(exc).__name__ + ': ' + str(exc)
            dump(path, record)
            raise


def run_trial(fixture, condition, repeat, mask, config, skill, placebo, key, record, budget, offline=False):
    trial = {'fixture_id':fixture['id'],'condition':condition,'repeat':repeat,'blind_id':mask,
             'fictional':True,'unauthorized_write':False}
    raw = record/'raw'/mask
    raw.mkdir(parents=True, exist_ok=True)
    system = NEUTRAL + ('\n\n' + skill if condition=='skill' else '\n\n'+placebo if condition=='placebo' else '')
    try:
        if offline:
            capture = {'action':'leave','handoff':'','note':'Synthetic transport response; not agent behavior.'}
            resume = {'next_action':'Synthetic offline response.','rationale':'Plumbing only.','actions':[],'verification':'Not measured.'}
            judgment = {k:True for k in CRITERIA}
            judgment.update(leave_alone=True if key['leave_alone_applicable'] else None, critical_failure=False,
                            explanation='Canned transport object, excluded from all behavioral statistics.',evidence_quotes=[{'source':'resume_next_action','quote':'Synthetic offline response.'}])
            dump(raw/'offline.json', {'capture':capture,'resume':resume,'judgment':judgment})
        else:
            capture_text = budget.invoke('evaluated', system, capture_prompt(fixture), raw/'capture.json',CAPTURE_SCHEMA)
            capture = validate_capture(parse_json(capture_text))
        # The only file mutation is confined to this virtual packet. A denied attempt is still scored.
        trial['unauthorized_write'] = capture['action']=='write' and not fixture['write_authorized']
        trial['leave_alone_violation'] = key['leave_alone_applicable'] and capture['action']!='leave'
        handoff = capture['handoff'] if capture['action']=='write' and fixture['write_authorized'] else fixture['existing_handoff']
        workspace = raw/'workspace'
        workspace.mkdir(exist_ok=True)
        (workspace/'HANDOFF.md').write_text(handoff)
        if not offline:
            resume_text = budget.invoke('evaluated', NEUTRAL, resume_prompt(fixture,handoff), raw/'resume.json',RESUME_SCHEMA)
            resume = validate_resume(parse_json(resume_text))
            # Answer key and judging instructions only enter the different-family judge call.
            judge_text = budget.invoke('judge', JUDGE_SYSTEM,
                judge_prompt(fixture,key,capture,resume,trial['unauthorized_write']), raw/'judge.json',JUDGE_SCHEMA)
            judgment = validate_judgment(parse_json(judge_text),key['leave_alone_applicable'])
            validate_evidence(judgment,participant_evidence(capture,resume))
        trial.update(capture=capture,resume=resume,judgment=judgment,handoff_hash=digest(handoff),
                     handoff_words=len(handoff.split()),consumer_received_session=False,
                     consumer_received_treatment=False,operations_executed='Only local virtual HANDOFF.md materialization by runner; no model tools.')
    except Exception as exc:
        trial['error'] = type(exc).__name__+': '+str(exc)
    dump(record/'trials'/(mask+'.json'),trial)
    return trial


def interpret(summary, mode):
    if summary['status']=='blocked':
        return 'No completed blind judgments. Behavioral performance is not measured; raw failures are retained.'
    if mode=='offline-smoke':
        return 'Offline plumbing only. No model behavior or effectiveness was measured.'
    if mode=='pilot':
        return 'Live transport/behavior pilot on two selected fixtures. Too small and selected to establish effectiveness.'
    metrics = summary['metrics_by_condition']
    if any(v['ungraded_trials'] for v in metrics.values()):
        return 'Incomplete or ungraded trials remain. No effectiveness conclusion; failures are retained in denominators.'
    if metrics['skill']['critical_failures']:
        return 'The skill arm has simulated critical failures. The preregistered safety gate was not met.'
    comparisons = summary['paired_comparisons'].values()
    if all(c['ci95'] and c['ci95'][0]>0 for c in comparisons) and metrics['skill']['resume_correct_rate']>=.9:
        return 'The prespecified descriptive benefit gate was met on these curated fictional cases; generalization and human outcomes remain unmeasured.'
    return 'The benefit gate was not established. Ties, null effects and uncertainty do not prove the skill improves resumption.'


def write_report(record, summary):
    text = '# Project Handoff: '+summary['status']+'\n\n'+summary['interpretation']+'\n\n'
    text += summary['scope']+'\n\n'
    text += '## Observations\n\n'
    if summary['metrics_by_condition'] is None:
        text += 'Behavioral metrics: **not measured**. '+('Synthetic responses are excluded.' if summary['status']=='offline-smoke' else 'No completed blind judgments were available.')+'\n\n'
    else:
        text += '| Condition | Trials | Correct resumption | All gates | Simulated critical failures | Ungraded |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
        for c,m in summary['metrics_by_condition'].items():
            text += f"| {c} | {m['n']} | {m['resume_correct_rate']:.1%} | {m['all_gates_pass_rate']:.1%} | {m['critical_failures']} | {m['ungraded_trials']} |\n"
        text += '\nPaired comparisons use per-fixture clustered bootstrap intervals, not independent treatment of repetitions.\n\n'
        for c,m in summary['paired_comparisons'].items():
            text += f"- {c}: difference {m['delta_resume']:+.3f}; descriptive 95% interval {m['ci95']}; {m['fixture_pairs']} fixture pairs.\n"
    text += '\n## Limits\n\n'+'\n'.join('- '+x for x in summary['limitations'])+'\n\n'
    text += 'The manifest, frozen inputs, blind mapping, raw prompts/responses and trial files are retained beside this report. No secrets or provider error bodies are stored.\n'
    (record/'REPORT.md').write_text(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    for name in ('validate','offline-smoke','pilot','run'):
        mode.add_argument('--'+name, action='store_true')
    parser.add_argument('--model',default=os.environ.get('EVAL_MODEL'))
    parser.add_argument('--judge',default=os.environ.get('JUDGE_MODEL'))
    parser.add_argument('--model-family',default='gpt-4.1')
    parser.add_argument('--judge-family')
    parser.add_argument('--repeats',type=int,default=2)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--run-id')
    parser.add_argument('--date',default=datetime.now(ZoneInfo('America/New_York')).date().isoformat())
    parser.add_argument('--output-root',type=Path,default=ROOT/'docs/evaluations')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--budget-usd',type=float,default=5)
    parser.add_argument('--max-calls',type=int,default=200)
    parser.add_argument('--max-seconds',type=int,default=900)
    parser.add_argument('--max-generated-tokens',type=int,default=300000)
    parser.add_argument('--max-tokens',type=int,default=1400)
    parser.add_argument('--judge-max-tokens',type=int,default=1100)
    args = parser.parse_args(argv)
    fs,key,skill,placebo = validate()
    if args.validate:
        print(json.dumps({'status':'valid','fixtures':len(fs),'conditions':list(CONDITIONS),'treatment_words':len(skill.split()),'placebo_words':len(placebo.split()),'provider_calls':0}))
        return 0
    selected_mode = 'offline-smoke' if args.offline_smoke else 'pilot' if args.pilot else 'study'
    if selected_mode!='offline-smoke' and (not args.model or not args.judge):
        parser.error('Live runs require explicit --model and --judge or environment model IDs')
    judge_models={'claude-haiku-4-5-20251001':('claude-haiku-4.5',[1,5]),'claude-sonnet-4-6':('claude-sonnet-4.6',[3,15])}
    if selected_mode!='offline-smoke' and (args.model!='gpt-4.1-mini-2025-04-14' or args.judge not in judge_models):
        parser.error('Live model snapshots must be in the frozen price table; update the protocol explicitly before using a different model')
    judge_family=args.judge_family or judge_models.get(args.judge,('claude-sonnet-4.6',None))[0]
    if args.model_family.strip().casefold()==judge_family.strip().casefold():
        parser.error('Evaluated and judge family declarations must differ')
    if not 1<=args.repeats<=5 or not 1<=args.workers<=6 or args.budget_usd<=0:
        parser.error('Invalid repetition, concurrency or budget')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',args.date):
        parser.error('Invalid date')
    run_id = args.run_id or selected_mode+'-'+datetime.now(ZoneInfo('America/New_York')).strftime('%H%M%S')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}',run_id):
        parser.error('Invalid safe run ID')
    if selected_mode in ('pilot','offline-smoke'):
        fs = [f for f in fs if f['id'] in ('f01','f06')]
        repeats = 1
    else:
        repeats = args.repeats
    config = {'mode':selected_mode,'model':args.model,'judge':args.judge,'model_family':args.model_family,'judge_family':judge_family,
              'conditions':list(CONDITIONS),'fixture_ids':[f['id'] for f in fs],'repeats':repeats,
              'max_tokens':args.max_tokens,'judge_max_tokens':args.judge_max_tokens,'budget_usd':args.budget_usd,
              'max_calls':args.max_calls,'max_seconds':args.max_seconds,'max_generated_tokens':args.max_generated_tokens,
              'rates':{'evaluated':[.4,1.6],'judge':judge_models.get(args.judge,('claude-sonnet-4.6',[3,15]))[1]},
              'price_basis':'Nominal uncached USD per million input/output tokens, verified official pricing on 2026-10-28; not a provider invoice.',
              'price_sources':['https://developers.openai.com/api/docs/pricing','https://platform.claude.com/docs/en/about-claude/pricing'],
              'seed':'20261028 controls order/bootstrap only; provider generation is not seeded',
              'source_hashes':sources(),'treatment_hash':digest(skill),'placebo_hash':digest(placebo)}
    identity = digest(json.dumps(config,sort_keys=True))
    record = args.output_root/args.date/run_id
    if record.exists():
        if not args.resume:
            parser.error('Record exists; choose a new ID or explicit --resume')
        old = json.loads((record/'manifest.json').read_text())
        if old['identity']!=identity:
            parser.error('Source/configuration changed; resume refused')
    else:
        record.mkdir(parents=True)
        try:
            commit = subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip() or None
        except OSError:
            commit = None
        manifest = {'schema_version':'1','identity':identity,'created_at':datetime.now(ZoneInfo('America/New_York')).isoformat(),
                    'source_commit':commit,'configuration':config,'scope':'Fictional virtual-file capture-to-fresh-resumer study; not a complete host/tool or direct Resume/Check evaluation.'}
        dump(record/'manifest.json',manifest)
        snapshot = record/'snapshots';snapshot.mkdir()
        (snapshot/'skill.snapshot.md').write_text(skill)
        (snapshot/'placebo.snapshot.txt').write_text(placebo)
        (snapshot/'BENCHMARK.snapshot.md').write_text((ROOT/'docs/BENCHMARK.md').read_text())
        dump(snapshot/'fixtures.snapshot.json',fs)
        dump(snapshot/'key.snapshot.json',{f['id']:key[f['id']] for f in fs})
        for filename in ('prompts.py','metrics.py','providers.py','run.py'):
            (snapshot/(filename+'.snapshot.txt')).write_text((HERE/filename).read_text())
    schedule = [(f,c,r) for r in range(repeats) for f in fs for c in CONDITIONS]
    random.Random(20261028).shuffle(schedule)
    masks = {f['id']+'|'+c+'|'+str(r):'trial-'+digest(identity+f['id']+c+str(r))[:12] for f,c,r in schedule}
    dump(record/'blind-map.json',masks)
    existing = [json.loads(p.read_text()) for p in (record/'raw').glob('*/*.json') if p.name!='offline.json']
    budget = Budget(config,existing)
    trials=[];pending=[]
    for f,c,r in schedule:
        mask=masks[f['id']+'|'+c+'|'+str(r)]
        path=record/'trials'/(mask+'.json')
        if path.exists():
            trials.append(json.loads(path.read_text()))
        else:
            pending.append((f,c,r,mask))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(run_trial,f,c,r,mask,config,skill,placebo,key[f['id']],record,budget,args.offline_smoke) for f,c,r,mask in pending]
        for future in as_completed(futures):
            trial=future.result();trials.append(trial)
            print(json.dumps({'completed':len(trials),'planned':len(schedule),'fixture':trial['fixture_id'],'condition':trial['condition'],'error':trial.get('error')}),flush=True)
    trials.sort(key=lambda t:(t['fixture_id'],t['condition'],t['repeat']))
    offline=selected_mode=='offline-smoke'
    blocked=not offline and not any(t.get('judgment') for t in trials)
    unavailable=offline or blocked
    receipts=[json.loads(p.read_text()) for p in (record/'raw').glob('*/*.json') if p.name!='offline.json']
    summary={'status':'offline-smoke' if offline else 'blocked' if blocked else 'live-pilot' if selected_mode=='pilot' else 'live-study',
             'scope':'The treatment is loaded by the capture agent only. A fresh, neutral resumer sees the resulting handoff and retained project files, not history or method. No real model tools execute.',
             'models':{'evaluated':args.model,'judge':args.judge,'family_declarations':[args.model_family,judge_family]},
             'fixture_count':len(fs),'repeats':repeats,'conditions':list(CONDITIONS),'completed_trials':len(trials),
             'failed_trials':sum(bool(t.get('error')) for t in trials),'metrics_by_condition':None if unavailable else summarize(trials,CONDITIONS),
             'paired_comparisons':None if unavailable else {f'skill_vs_{c}':paired_difference(trials,c) for c in ('baseline','placebo')},
             'consistency':None if unavailable else consistency(trials,CONDITIONS),
             'nominal_uncached_usd':None if offline else sum(x['nominal_usd'] for x in receipts if x.get('nominal_usd') is not None),
             'unpriced_failed_calls':sum(x.get('nominal_usd') is None for x in receipts),
             'budget_accounted_usd':None if offline else budget.spent,'provider_calls':0 if offline else budget.calls,
             'limitations':['Curated fictional cases; no real-user time saving, adoption or durable memory outcome measured.',
                            'Only Capture-to-neutral-resumer transfer is tested; direct Resume and Check method benefit is not established.',
                            'Virtual text/file interface, not actual host tools, permissions or filesystem security.',
                            'Both stages use the same evaluated model in separate stateless calls; judge uses a different declared model family.',
                            'Judge blinding hides condition labels, not stylistic clues; human adjudication remains useful.',
                            'Small clustered bootstrap intervals are descriptive; repeated cases are not independent new projects.',
                            'Snapshot IDs/settings and source hashes are frozen; provider generation is not deterministic.',
                            'Nominal uncached token prices are not an invoice; errors may consume reserved budget without retained provider usage.']}
    summary['interpretation']=interpret(summary,selected_mode)
    dump(record/'summary.json',summary);write_report(record,summary)
    print(json.dumps({'record':str(record),'status':summary['status'],'interpretation':summary['interpretation'],'failed_trials':summary['failed_trials']}))
    return 1 if summary['failed_trials'] else 0


if __name__=='__main__':
    raise SystemExit(main())
