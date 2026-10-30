"""Build public-only category, knowledge-journey and verification pages."""
from html import escape
import json,re
from pathlib import Path
from urllib.parse import urlsplit
E=lambda value:escape(str(value),quote=True)

COLUMNS=['id','title','category','repository_url','head','published_head','publication_status','ci_status','pages_status','legacy_routing_status','current_build_check','portable_lifecycle','native_payload_install','local_preparation','static_coverage','task_behavior']
MODULES={'errorcache':'https://github.com/michaeljabbour/amplifier-bundle-errorcache','anthropic-fable':'https://github.com/michaeljabbour/amplifier-module-provider-anthropic-fable','context-memory':'https://github.com/michaeljabbour/amplifier-module-context-memory'}

def bounded_text(value,limit=1000):
    if not isinstance(value,str) or not 1<=len(value)<=limit:raise ValueError('Expected bounded public text')
    return value

def number(value):
    if type(value) is not int or not 0<=value<=1_000_000:raise ValueError('Expected bounded count')
    return value

def validate_status(data,ids,scope=None):
    scope=scope or json.loads((Path(__file__).resolve().parents[1]/'content/public-status-scope.json').read_text())
    top={'schema_version','updated_at','status','scope','records','triage_counts','counts','coverage_note','study_repositories','supplemental_module_repairs'}
    if not isinstance(data,dict) or set(data)!=top or data['schema_version']!='public-capability-status/v1':raise ValueError('Unsupported public status contract')
    for key in ['updated_at','status','scope','coverage_note']:bounded_text(data[key])
    if set(scope['capabilities'])!=ids or not isinstance(data['records'],list) or len(data['records'])!=33 or any(not isinstance(r,dict) for r in data['records']) or {r.get('id') for r in data['records']}!=ids:raise ValueError('Status must match 33 approved catalogue IDs')
    choices={'publication_status':{'published','pushed','verified','failed','pending','updating'},'ci_status':{'pass','fail','pending','success','failure','in-progress','queued','cancelled','skipped','not-yet-verified'},'pages_status':{'live','verified','pending','fail','failed','not-yet-verified'},'legacy_routing_status':{'verified','pending','fail','failed','not-yet-verified'},'current_build_check':{'pass','fail','pass-at-prior-revision','updating'},'portable_lifecycle':{'pass','native-interface','updating'},'native_payload_install':{'pass','not-applicable-or-updating'},'local_preparation':{'pass','updating'},'static_coverage':{'scoped-or-partial; no whole-program security verdict'},'task_behavior':{'One bounded opening-turn probe passed in Codex; another local model failed instruction adherence.','not-benchmarked-across-harnesses'}}
    for row in data['records']:
        if set(row)!=set(COLUMNS):raise ValueError('Unexpected public status field')
        approved=scope['capabilities'][row['id']]
        if row['title']!=approved['title'] or row['category']!=approved['category'] or row['repository_url'] not in approved['repository_urls']:raise ValueError('Public identity differs from approved scope')
        for key in ['head','published_head']:
            if row[key] is not None and (not isinstance(row[key],str) or not re.fullmatch('[0-9a-f]{40}',row[key])):raise ValueError('Invalid source commit identity')
        for key,allowed in choices.items():
            if not isinstance(row[key],str) or row[key] not in allowed:raise ValueError('Invalid public verification state')
    expected_counts={'capabilities':33,'current_build_check_passes':sum(r['current_build_check']=='pass' for r in data['records']),'portable_lifecycle_passes':sum(r['portable_lifecycle']=='pass' for r in data['records']),'native_payload_install_passes':sum(r['native_payload_install']=='pass' for r in data['records']),'current_local_preparation_passes':sum(r['local_preparation']=='pass' for r in data['records']),'published_records':sum(r['publication_status'] in {'published','pushed','verified'} for r in data['records'])}
    if data['counts']!=expected_counts or any(type(v) is not int for v in data['counts'].values()):raise ValueError('Public counters differ from rows')
    permitted_triage={'public_capabilities','reviewed_original_observations','unreviewed_original_observations','unique_original_contexts','historical_revised_observations_reconciled','unreviewed_revised_observations','relocated_source_observations_reconciled','reviewed_additional_observations','unreviewed_additional_observations','reviewed_focused_observations','unreviewed_focused_observations','focused_public_capability_contexts','focused_public_capability_observations','focused_supporting_or_shared_contexts','focused_supporting_or_shared_observations','repaired_issue_groups','pending_issue_groups','saved_static_attempts','static_model_calls'}
    if not isinstance(data['triage_counts'],dict) or not set(data['triage_counts'])<=permitted_triage:raise ValueError('Unknown triage field')
    for value in data['triage_counts'].values():number(value)
    studies=data['study_repositories']
    if not isinstance(studies,list) or len(studies)!=45 or any(not isinstance(x,dict) or set(x)!={'repository_url'} or not isinstance(x['repository_url'],str) for x in studies) or sorted(x['repository_url'] for x in studies)!=scope['study_repositories']:raise ValueError('Public study set differs from approved 45 URLs')
    modules=data['supplemental_module_repairs']
    if not isinstance(modules,list) or len(modules)>3:raise ValueError('Invalid supplemental component list')
    seen=set()
    for row in modules:
        if not isinstance(row,dict) or set(row)!={'id','repository_url','head','publication_status','test_matrix','test_scope','ci_status'}:raise ValueError('Unexpected component field')
        ident=row['id']
        if not isinstance(ident,str) or ident not in MODULES or ident in seen or row['repository_url']!=MODULES[ident]:raise ValueError('Component is outside approved public scope')
        seen.add(ident)
        if not isinstance(row['head'],str) or not re.fullmatch('[0-9a-f]{40}',row['head']):raise ValueError('Invalid component commit')
        if row['publication_status'] not in choices['publication_status'] or row['ci_status'] not in {'success','failure','pending','not-yet-verified','no-workflows-configured'}:raise ValueError('Invalid component state')
        if row['test_scope']!='Separate source-bound contract checks; runtime code parity is retained across documentation-only releases.':raise ValueError('Unknown component test scope')
        contracts={'native','legacy-sqlite'} if ident=='context-memory' else {'source-unit'}
        matrix=row['test_matrix']
        if not isinstance(matrix,list) or len(matrix)!=len(contracts) or any(not isinstance(x,dict) or set(x)!={'contract','passed','skipped'} for x in matrix) or {x['contract'] for x in matrix}!=contracts:raise ValueError('Invalid component test matrix')
        for test in matrix:number(test['passed']);number(test['skipped'])
    encoded=json.dumps(data,ensure_ascii=False)
    for rule in [r'/Users/',r'/var/folders/',r'/private/var/',r'file://',r'libfile_',r'(?i)\b(?:sk-|gh[pousr]_|github_pat_)[a-z0-9_]{16,}',r'(?i)bearer\s+[a-z0-9._-]{16,}',r'"(?:local_root_records|source_library_ids|canonical_campaign_targets|raw_logs|private_census)"']:
        if re.search(rule,encoded):raise ValueError('Public privacy check failed; value withheld')
    return data

def status_csv(data):
    import csv,io
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=COLUMNS);writer.writeheader();writer.writerows(data['records']);return stream.getvalue()

def validate_csv(raw,data):
    import csv,io
    rows=list(csv.DictReader(io.StringIO(raw,newline='')))
    reader=csv.DictReader(io.StringIO(raw,newline=''))
    expected=[{key:'' if row[key] is None else str(row[key]) for key in COLUMNS} for row in data['records']]
    if reader.fieldnames!=COLUMNS or rows!=expected:raise ValueError('Public CSV must exactly match the validated 33-row JSON projection')
    return status_csv(data)

def category_body(projects,stages):
    parts=['<section class="page-intro wrap"><a class="back-link" href="/capabilities/">All capabilities</a><h1>Find the part<br>you need.</h1><p>Thirty-three distinct capabilities, organized around seven moments in the work. Start anywhere; the guide and source stay with each one.</p><div class="button-row"><a class="text-link" href="/journey/">Follow the build journey</a><a class="text-link" href="/journey/knowledge/">Explore the proposed knowledge journey</a><a class="text-link" href="/reports/capabilities/">See current checks</a></div></section>']
    for stage in stages:
        members=[p for p in projects if p['category']==stage['id']]
        parts.append('<section class="category-group wrap" id="category-'+E(stage['id'])+'"><div class="section-heading"><div><h2>'+E(stage['title'])+'</h2><p>'+E(stage['question'])+'</p></div><a class="text-link" href="/journey/#stage-'+E(stage['id'])+'">See this moment</a></div><div class="category-members">')
        for p in members:parts.append('<article data-category-capability="'+E(p['id'])+'"><h3><a href="/capabilities/'+E(p['id'])+'/">'+E(p['title'])+'</a></h3><p>'+E(p['summary'])+'</p><a href="/capabilities/'+E(p['id'])+'/">Guide and first step <span aria-hidden="true">↗</span></a></article>')
        parts.append('</div></section>')
    return ''.join(parts)

def knowledge_body(data,by_id):
    parts=['<section class="page-intro wrap"><a class="back-link" href="/journey/">The build journey</a><p class="publication-label">Proposed journey</p><h1>From a question<br>to something worth sharing.</h1><p>A way through knowledge curation and creation: explore, collect, connect, test, make, refine and share. This is a proposed way to navigate the existing capabilities, not a claim of an automated end-to-end pipeline.</p></section><nav class="wrap knowledge-links" aria-label="Proposed knowledge journey"><ol class="category-links">']
    for n,stage in enumerate(data['stages']):parts.append('<li><a href="#knowledge-'+E(stage['id'])+'"><span aria-hidden="true">'+str(n+1)+'</span>'+E(stage['title'])+'</a></li>')
    parts.append('</ol></nav>')
    for stage in data['stages']:
        parts.append('<section class="knowledge-stage wrap" id="knowledge-'+E(stage['id'])+'"><div><p class="publication-label">Proposed · '+E(stage['title'])+'</p><h2>'+E(stage['question'])+'</h2><p>'+E(stage['description'])+'</p><p class="knowledge-output"><strong>Something to carry forward</strong><br>'+E(stage['output'])+'</p></div><div><h3>Existing capabilities to explore</h3><ul>')
        for ident in stage['capability_ids']:
            p=by_id[ident];parts.append('<li><a href="/capabilities/'+E(ident)+'/">'+E(p['title'])+'</a><p>'+E(p['summary'])+'</p></li>')
        parts.append('</ul></div></section>')
    parts.append('<section class="journey-loop wrap"><p>Testing can send you back to a source. Refining can uncover a factual question. Keep the evidence with the work and choose deliberately what to share.</p><a class="text-link" href="/capabilities/categories/">Browse all 33 capabilities</a></section>')
    return ''.join(parts)

def report_body(data):
    counts=data['counts'];evidence_present=any(r.get('head') for r in data['records'])
    parts=['<section class="page-intro wrap"><a class="back-link" href="/capabilities/categories/">The capability collection</a><p class="publication-label">Status update · '+E(data['updated_at'][:16].replace('T',' ')+' UTC')+'</p><h1>What has<br>been checked.</h1><p>'+E(data['status'])+'</p><p>Source repair, packaging, live behavior and publication are separate checks. Each capability keeps its own guide and repository while the public names move to amplifier-capability-*.</p></section><section class="wrap status-overview">']
    if evidence_present:parts.append('<p>'+str(counts['current_build_check_passes'])+' current source builds/checks; '+str(counts['portable_lifecycle_passes'])+' method install/uninstall checks; '+str(counts['native_payload_install_passes'])+' native payload installation checks. These are bounded verification results.</p>')
    else:parts.append('<p>Current verification records are being refreshed after the repairs. An “updating” entry is unfinished evidence, not a failed capability. Browse its guide or source in the meantime.</p>')
    parts.append('<p>'+E(data['coverage_note'])+'</p><div class="button-row"><a href="status.json">Download public status JSON</a><a href="capability-status.csv">Download the 33-row status table</a><a href="/reports/capability-installer/">Shared installer and contract</a></div><div class="status-table"><table><caption>33 public capabilities and their separate verification states</caption><thead><tr><th>Capability</th><th>Source / build</th><th>Install / behavior</th><th>Publication / CI</th></tr></thead><tbody>')
    for row in data['records']:
        published=row.get('published_head');prepared=row.get('head');commit=('<a href="'+E(row['repository_url']+'/commit/'+published)+'"><code>'+E(published[:12])+'</code></a>') if published else 'Not yet published'
        parts.append('<tr><th scope="row"><a href="/capabilities/'+E(row['id'])+'/">'+E(row['title'])+'</a><br><a href="'+E(row['repository_url'])+'">Repository</a></th><td>'+('Prepared <code>'+E(prepared[:12])+'</code><br>' if prepared else '')+'Published: '+commit+'<br>Build/check: '+E(row['current_build_check'])+'</td><td>Method installation: '+E(row['portable_lifecycle'])+'<br>Native installation: '+E(row['native_payload_install'])+'<br>'+E(row['task_behavior'])+'</td><td>Publication: '+E(row['publication_status'])+'<br>CI: '+E(row['ci_status'])+'<br>Site: '+E(row['pages_status'])+'<br>Legacy routing: '+E(row['legacy_routing_status'])+'</td></tr>')
    parts.append('</tbody></table></div></section>')
    triage=data['triage_counts']
    if triage:
        parts.append('<section class="wrap public-study"><h2>Recorded findings, reviewed.</h2><p>'+E(triage.get('reviewed_original_observations',0))+' original observations across '+E(triage.get('unique_original_contexts',0))+' contexts, '+E(triage.get('reviewed_additional_observations',0))+' additional residual observations and '+E(triage.get('reviewed_focused_observations',0))+' saved focused warnings have dispositions. The focused total includes '+E(triage.get('focused_public_capability_observations',0))+' observations in public capability contexts and '+E(triage.get('focused_supporting_or_shared_observations',0))+' in related or shared contexts.</p><p>'+E(triage.get('repaired_issue_groups',0))+' affected-capability repair workstreams are closed, with '+E(triage.get('pending_issue_groups',0))+' pending confirmed source-defect workstreams. Workstreams are not a count of unique vulnerabilities. '+E(triage.get('saved_static_attempts',0))+' saved static attempts used '+E(triage.get('static_model_calls',0))+' model calls. These include overlapping narrow contexts and batches, rather than 33 whole-program security audits.</p></section>')
    if data.get('supplemental_module_repairs'):
        parts.append('<section class="wrap public-study"><h2>Supporting component updates.</h2><ul>')
        for module in data['supplemental_module_repairs']:
            matrix='; '.join(E(test['contract'])+': '+E(test['passed'])+' passed / '+E(test['skipped'])+' skipped' for test in module['test_matrix'])
            parts.append('<li><a href="'+E(module['repository_url'])+'">'+E(module['id'])+'</a>: '+matrix+'; '+E(module['publication_status'])+'; CI '+E(module['ci_status'])+'. <span>'+E(module['test_scope'])+'</span></li>')
        parts.append('</ul></section>')
    parts.append('<section class="wrap public-study"><h2>Public projects to study.</h2><p>A source list for continued research into capability design, packaging and documentation. Inclusion is not an endorsement, partnership or installed dependency.</p><ul>')
    for item in data['study_repositories']:
        url=item['repository_url'];parts.append('<li><a href="'+E(url)+'">'+E(url.removeprefix('https://github.com/'))+'</a></li>')
    parts.append('</ul></section>')
    return ''.join(parts)

def write_public_views(root,out,write,shell,projects,stages):
    ids={p['id'] for p in projects};by_id={p['id']:p for p in projects}
    knowledge=json.loads((root/'content/knowledge-journey.json').read_text())
    for stage in knowledge['stages']:
        if not set(stage['capability_ids'])<=ids:raise ValueError('Knowledge journey contains an unapproved capability')
    status=validate_status(json.loads((root/'content/public-capability-status.json').read_text()),ids)
    write('capabilities/categories',shell('Seven ways into the work','Browse 33 distinct public capabilities across seven moments.',category_body(projects,stages),'capabilities','/capabilities/categories/'))
    write('journey/knowledge',shell('From curation to creation','A proposed journey through existing research, knowledge and creative capabilities.',knowledge_body(knowledge,by_id),'journey','/journey/knowledge/'))
    write('reports/capabilities',shell('Capability checks','Current public capability verification and publication status.',report_body(status),'status','/reports/capabilities/'))
    report=out/'reports/capabilities';(report/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n')
    checked_csv=validate_csv((root/'content/public-capability-status.csv').read_text(),status)
    (report/'capability-status.csv').write_text(checked_csv,newline='')
    (out/'repo-categories.html').write_text(shell('Seven ways into the work','Browse 33 public capabilities across seven moments.',category_body(projects,stages),'capabilities','/repo-categories.html',extra_head='<meta name="robots" content="noindex">'))
