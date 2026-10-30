#!/usr/bin/env python3
"""One shared, deterministic capability discovery installer. Never runs capability code."""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path, PurePosixPath

CONTRACT = "amplifier-capability/v1"
RECEIPT = ".capability-install.json"
HARNESS_DIRS = {"claude-code": ".claude/skills", "codex": ".agents/skills", "gemini": ".agents/skills", "grok": ".agents/skills", "opencode": ".agents/skills", "amplifier": ".amplifier/skills"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

def sha(data): return hashlib.sha256(data).hexdigest()
def encoded(value): return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
def git(root, *args):
    return subprocess.check_output(["git", "-c", "core.fsmonitor=false", "-C", str(root), *args], stderr=subprocess.PIPE).decode().strip()

def relative(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or ".." in p.parts or "\\" in value:
        raise ValueError("Unsafe relative path: " + str(value))
    return p

def no_links(path, root):
    path = Path(path); root = Path(root)
    if not path.is_relative_to(root): raise ValueError("Path escapes root")
    p = root
    if p.is_symlink(): raise ValueError("Symlink root refused")
    for component in path.relative_to(root).parts:
        p = p / component
        if p.is_symlink(): raise ValueError("Symlink path refused: " + str(p))
    return path

def read_contract(path):
    d = json.loads(Path(path).read_text())
    if d.get("contract_version") != CONTRACT: raise ValueError("Unsupported contract_version")
    for field in ("id", "name", "kind", "engine", "promise"):
        if not isinstance(d.get(field), str) or not d[field]: raise ValueError("Missing field: " + field)
    if not SLUG.fullmatch(d['id']) or not SLUG.fullmatch(d['name']): raise ValueError("Unsafe capability identity")
    if not d['name'].startswith('amplifier-capability-'):raise ValueError('Public name must use capability identity')
    if d['kind'] not in ('skill','smart-tool','tool','library','agent','outer-harness'):raise ValueError('Unknown kind')
    if d['engine'] not in ("LLM", "Decision model", "Both", "None"): raise ValueError("Unknown engine")
    if 'version' not in d or d['version'] is not None and not isinstance(d['version'],str):raise ValueError('Invalid release version')
    if not isinstance(d.get('surfaces'),list) or not isinstance(d.get('legacy_names'),list):raise ValueError('Invalid surfaces or aliases')
    if any(x not in ('agent-skills','amplifier-bundle','cli','mcp','python-library') for x in d['surfaces']):raise ValueError('Unknown surface')
    for field in ("interfaces", "permissions", "dataflow", "engine_components", "source_policy"):
        if not isinstance(d.get(field), dict): raise ValueError("Missing contract: " + field)
    for name in d.get('legacy_names', []):
        if not isinstance(name, str) or not SLUG.fullmatch(name): raise ValueError("Unsafe legacy identity")
    skill = d.get('portable_method')
    if skill is not None:
        if not isinstance(skill, dict) or not SLUG.fullmatch(skill.get('name', '')) or len(skill['name'])>64: raise ValueError("Invalid portable method")
        relative(skill['path'])
        if not isinstance(skill.get('include',['.']),list):raise ValueError('Invalid portable include list')
        for name in skill.get('include', ['.']): relative(name)
    return d

def source_files(source, d, revision, verify_contract=True):
    source = Path(source).resolve()
    if not re.fullmatch(r'[0-9a-f]{40}', revision): raise ValueError("Pin must be an explicit full Git commit SHA")
    if git(source, 'rev-parse', 'HEAD') != revision: raise ValueError("Checkout HEAD differs from requested pin")
    if verify_contract:
        pinned=json.loads(subprocess.check_output(['git','-C',str(source),'show',revision+':capability.json']))
        if encoded(pinned)!=encoded(d):raise ValueError('Capability contract differs from the pinned canonical manifest')
    skill = d.get('portable_method')
    if skill is None: return {}, None
    folder = source / relative(skill['path'])
    no_links(folder, source)
    tracked = subprocess.check_output(['git','-c','core.fsmonitor=false','-C',str(source),'ls-files','-z']).decode().split('\0')
    files = {}
    for name in tracked:
        if not name: continue
        path = source / name
        if not path.is_relative_to(folder): continue
        rel = path.relative_to(folder).as_posix()
        includes = skill.get('include', ['.'])
        if not any(i == '.' or rel == i.rstrip('/') or rel.startswith(i.rstrip('/') + '/') for i in includes): continue
        if any(x in {'.git','.research','.venv','node_modules','__pycache__','.DS_Store'} for x in Path(rel).parts): continue
        if any(x.startswith('.env') for x in Path(rel).parts): raise ValueError("Environment files forbidden in method")
        no_links(path, source)
        if not path.is_file(): raise ValueError("Missing tracked source: " + name)
        blob = subprocess.check_output(['git','-C',str(source),'show',revision + ':' + name])
        if path.read_bytes() != blob: raise ValueError("Selected source differs from pin: " + name)
        files[rel] = sha(blob)
    if 'SKILL.md' not in files: raise ValueError("Portable method lacks tracked SKILL.md")
    if len([n for n in files if Path(n).name == 'SKILL.md']) != 1: raise ValueError("Portable method has multiple canonical entries")
    text = (folder/'SKILL.md').read_text()
    m = re.search(r'^name:\s*[\"\']?([a-z0-9-]+)[\"\']?\s*$', text.split('---',2)[1] if text.startswith('---') else '', re.M)
    if not m or m.group(1) != skill['name']: raise ValueError("SKILL frontmatter name must match installed folder")
    if not any('LICENSE' in Path(n).name.upper() for n in files): raise ValueError("Portable method must include its license")
    for rel in files:
        if not rel.endswith('.md'): continue
        for ref in re.findall(r'(?<!!)\[[^\]]+\]\(([^)\s]+)\)', (folder/rel).read_text()):
            from urllib.parse import unquote, urlsplit
            uri = urlsplit(ref)
            if uri.scheme or not uri.path: continue
            dest = ((folder/rel).parent / unquote(uri.path)).resolve()
            if not dest.is_relative_to(folder.resolve()) or not dest.is_file() or dest.relative_to(folder).as_posix() not in files:
                raise ValueError("Reference is not in portable package: " + ref)
    return files, folder

def tree_files(target):
    result = {}
    if not target.exists(): return result
    for p in target.rglob('*'):
        no_links(p,target)
        if p.is_file() and p != target / RECEIPT: result[p.relative_to(target).as_posix()] = sha(p.read_bytes())
    return result

def state(target, d):
    if not target.exists(): return {'status':'absent'}
    no_links(target, target.parent)
    if not target.is_dir(): return {'status':'foreign'}
    no_links(target/RECEIPT,target)
    try: receipt = json.loads((target/RECEIPT).read_text())
    except (OSError,ValueError): return {'status':'foreign'}
    identities = {d['id'],d['name'],*d.get('legacy_names',[])}
    if receipt.get('capability') not in identities or receipt.get('id') != d['id']: return {'status':'foreign'}
    expected = receipt.get('files')
    if not isinstance(expected,dict): return {'status':'foreign'}
    for rel,digest in expected.items():
        relative(rel)
        if not re.fullmatch(r'[0-9a-f]{64}',digest): raise ValueError("Invalid install receipt")
    actual = tree_files(target)
    return {'status':'owned-clean' if actual == expected else 'edited','files':actual,'receipt_hash':sha((target/RECEIPT).read_bytes())}

def targets(root,d,harness):
    if harness == 'claude': harness='claude-code'
    chosen = sorted(HARNESS_DIRS) if harness == 'all' else [harness]
    result = {}
    for h in chosen:
        if h not in HARNESS_DIRS: raise ValueError("Unknown harness: " + h)
        p = no_links(root / HARNESS_DIRS[h] / d['portable_method']['name'],root)
        result.setdefault(str(p),[]).append(h)
    return result

def plan(source,manifest,revision,root,harness,operation='install'):
    d = read_contract(manifest); root = Path(root).expanduser().resolve()
    files, folder = source_files(source,d,revision)
    if d.get('portable_method') is None:
        return {'operation':operation,'installable':False,'id':d['id'],'kind':d['kind'],'interfaces':d['interfaces'],'reason':'No portable method declared; use the deterministic library/CLI/MCP contract. No fake skill is generated.'}
    result = {'operation':operation,'installable':True,'id':d['id'],'name':d['name'],'root':str(root),'source':str(Path(source).resolve()),'revision':revision,'manifest_hash':sha(encoded(d)),
              'permissions':d['permissions'],'dataflow':d['dataflow'],'files':files,'targets':[],'execution':'Copies discovery files only; no capability code, dependency install, trust configuration or provider call.'}
    for path, harnesses in targets(root,d,harness).items(): result['targets'].append({'path':path,'harnesses':harnesses,**state(Path(path),d)})
    result['blocked'] = any(x['status'] in ('foreign','edited') for x in result['targets'])
    result['plan_hash'] = sha(encoded(result))
    return result

def apply_plan(p,d,folder,expect):
    if not p.get('installable'): raise ValueError("Native component has no discovery installation")
    if p['plan_hash'] != expect: raise ValueError("Preview changed; review a new plan")
    if p['blocked']: raise ValueError("Foreign or edited installation refused; no paths changed")
    root = Path(p['root']); state_dir = no_links(root/'.capability-state',root)
    tx = state_dir / ('transaction-' + uuid.uuid4().hex); tx.mkdir(parents=True)
    journal = {'schema_version':'capability-transaction/v1','id':d['id'],'portable_name':d['portable_method']['name'],'operation':p['operation'],'root':str(root),'moves':[],'status':'preparing'}
    try:
        for index, entry in enumerate(p['targets']):
            target = Path(entry['path']); no_links(target,root); target.parent.mkdir(parents=True,exist_ok=True)
            old = tx / ('previous-' + str(index))
            move={'target':str(target),'previous':str(old) if target.exists() else None}
            if target.exists(): os.replace(target,old)
            journal['moves'].append(move)
            if p['operation']=='install':
                staging=tx/('new-'+str(index));staging.mkdir()
                for rel in p['files']:
                    out=staging/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(folder/rel,out)
                receipt={'schema_version':'capability-install/v1','capability':d['name'],'id':d['id'],'revision':p['revision'],'manifest_hash':p['manifest_hash'],'files':p['files'],'harnesses':entry['harnesses']}
                (staging/RECEIPT).write_text(json.dumps(receipt,indent=2)+'\n');os.replace(staging,target)
                move['installed_hash']=sha(encoded(tree_files(target)));move['receipt_hash']=sha((target/RECEIPT).read_bytes())
        journal['status']='applied';(tx/'transaction.json').write_text(json.dumps(journal,indent=2)+'\n')
    except Exception:
        for move in reversed(journal['moves']):
            target=Path(move['target'])
            if target.exists(): shutil.rmtree(target)
            if move['previous']: os.replace(move['previous'],target)
        journal['status']='failed-and-restored';(tx/'transaction.json').write_text(json.dumps(journal,indent=2)+'\n');raise
    return {'operation':p['operation'],'transaction':str(tx/'transaction.json'),'status':'applied','source_execution':False}

def rollback(path):
    path=Path(path).resolve();j=json.loads(path.read_text());root=Path(j['root']).resolve()
    if not path.is_relative_to(root/'.capability-state') or j.get('status')!='applied': raise ValueError("Invalid rollback transaction")
    if not SLUG.fullmatch(j.get('portable_name','')) or j.get('operation') not in ('install','uninstall'):raise ValueError('Invalid rollback identity')
    allowed={str(root/p/j['portable_name']) for p in HARNESS_DIRS.values()}
    if len(j['moves'])!=len({m['target'] for m in j['moves']}):raise ValueError('Duplicate rollback target')
    for move in j['moves']:
        target=no_links(Path(move['target']),root)
        if str(target) not in allowed:raise ValueError('Rollback target is not a known discovery location')
        if j['operation']=='install':
            if sha(encoded(tree_files(target)))!=move['installed_hash'] or sha((target/RECEIPT).read_bytes())!=move['receipt_hash']: raise ValueError("Installed copy was edited; rollback refused")
        elif target.exists(): raise ValueError("Uninstall target was recreated; rollback refused")
        if move['previous']:
            if not Path(move['previous']).is_relative_to(path.parent):raise ValueError("Unsafe rollback backup")
            no_links(Path(move['previous']),path.parent)
    for i,move in enumerate(j['moves']):
        target=Path(move['target'])
        if target.exists():os.replace(target,path.parent/('rolled-back-'+str(i)))
        if move['previous']:os.replace(move['previous'],target)
    j['status']='rolled-back';path.write_text(json.dumps(j,indent=2)+'\n');return {'status':'rolled-back','transaction':str(path)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['describe','preview','install','uninstall','doctor','rollback'])
    parser.add_argument('--source',type=Path);parser.add_argument('--manifest',type=Path);parser.add_argument('--revision')
    parser.add_argument('--dest',type=Path);parser.add_argument('--harness',default='all',choices=[*HARNESS_DIRS,'claude','all'])
    parser.add_argument('--scope',default='project',choices=['project','user']);parser.add_argument('--apply',action='store_true');parser.add_argument('--expect-plan');parser.add_argument('--transaction',type=Path)
    args=parser.parse_args()
    try:
        if args.operation=='rollback':
            if not args.apply or not args.transaction:raise ValueError('Rollback requires --apply and --transaction')
            result=rollback(args.transaction)
        else:
            if not args.manifest:raise ValueError('--manifest is required')
            d=read_contract(args.manifest)
            if args.operation=='describe':result=d
            else:
                if not args.source or not args.revision:raise ValueError('--source and explicit --revision are required')
                if args.scope=='user' and not args.dest:raise ValueError('User scope requires an explicit --dest; no implicit home writes')
                dest=args.dest or Path.cwd()
                operation='uninstall' if args.operation=='uninstall' else 'install'
                result=plan(args.source,args.manifest,args.revision,dest,args.harness,operation)
                if args.operation=='doctor':
                    result['doctor']='discovery-files-only';result['healthy']=all(x['status']=='owned-clean' and x['files']==result['files'] for x in result.get('targets',[])) if result['installable'] else None
                elif args.operation in ('install','uninstall') and args.apply:
                    _,folder=source_files(args.source,d,args.revision);result=apply_plan(result,d,folder,args.expect_plan)
        print(json.dumps(result,indent=2));return 2 if result.get('healthy') is False else 0
    except (ValueError,OSError,KeyError,TypeError,subprocess.CalledProcessError) as error:
        print(json.dumps({'status':'error','error':str(error)}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
