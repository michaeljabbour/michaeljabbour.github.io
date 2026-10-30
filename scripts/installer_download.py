"""Export the single audited installer with an honest build-time source pin."""
import hashlib,json,os,re,shutil,subprocess

FILES={'capability.py','contract.schema.json','test_capability.py','LICENSE','README.md','PROVENANCE.md','index.html'}
FIELDS={'schema_version','prepared_at','canonical_repository_url','source_directory','download_base_url','download_manifest_url','source_commit','source_commit_rule','files','runtime_source_unchanged','schema_id','contract_version','model_calls','new_dependencies'}

def validate_package(manifest):
    if not isinstance(manifest,dict) or set(manifest)!=FIELDS or manifest['schema_version']!='capability-installer-public-package/v1':raise ValueError('Unsupported installer package fields')
    fixed={'canonical_repository_url':'https://github.com/michaeljabbour/michaeljabbour.github.io','source_directory':'tools','download_base_url':'https://michaeljabbour.github.io/reports/capability-installer/','download_manifest_url':'https://michaeljabbour.github.io/reports/capability-installer/manifest.json','source_commit':'__BUILD_GIT_SHA__','runtime_source_unchanged':True,'schema_id':'urn:amplifier:capability-contract:v1','contract_version':'amplifier-capability/v1','model_calls':0,'new_dependencies':False}
    if any(type(manifest[k]) is not type(v) or manifest[k]!=v for k,v in fixed.items()):raise ValueError('Installer package identity differs')
    for key in ['prepared_at','source_commit_rule']:
        if not isinstance(manifest[key],str) or not 1<=len(manifest[key])<=500:raise ValueError('Invalid installer metadata')
    if not isinstance(manifest['files'],list) or len(manifest['files'])!=7:raise ValueError('Unexpected installer file count')
    for entry in manifest['files']:
        if not isinstance(entry,dict) or set(entry)!={'path','sha256','bytes'} or not isinstance(entry['path'],str) or entry['path'] not in FILES or not isinstance(entry['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',entry['sha256']) or type(entry['bytes']) is not int or not 0<entry['bytes']<=1_000_000:raise ValueError('Invalid installer file record')
    if {r['path'] for r in manifest['files']}!=FILES:raise ValueError('Duplicate or missing installer file')
    return manifest

def verify_committed_package(root,head,manifest):
    for name in [*FILES,'PACKAGE.json']:
        try:tracked=subprocess.check_output(['git','-c','core.fsmonitor=false','-C',str(root),'show',head+':tools/'+name],stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as exc:raise ValueError('Installer package must be tracked in the committed source') from exc
        if tracked!=(root/'tools'/name).read_bytes():raise ValueError('Committed installer package differs from build input')

def write_installer(root,out):
    source=root/'tools';manifest=validate_package(json.loads((source/'PACKAGE.json').read_text()))
    if manifest.get('schema_version')!='capability-installer-public-package/v1':raise ValueError('Unsupported installer package')
    expected={entry['path']:entry for entry in manifest['files']}
    if set(expected)!={'capability.py','contract.schema.json','test_capability.py','LICENSE','README.md','PROVENANCE.md','index.html'}:raise ValueError('Unexpected installer file set')
    if any(p.is_symlink() for p in [source,*source.rglob('*')]):raise ValueError('Installer source must not contain symlinks')
    for name,entry in expected.items():
        body=(source/name).read_bytes()
        if len(body)!=entry['bytes'] or hashlib.sha256(body).hexdigest()!=entry['sha256']:raise ValueError('Installer package bytes differ')
    head=subprocess.check_output(['git','-c','core.fsmonitor=false','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    github=os.environ.get('GITHUB_ACTIONS')=='true';preview=os.environ.get('CAPABILITY_INSTALLER_PREVIEW')=='1' and not github
    commit=os.environ.get('GITHUB_SHA') if github else head
    if not re.fullmatch('[0-9a-f]{40}',commit or '') or commit!=head:raise ValueError('Installer needs the exact committed build revision')
    dirty=subprocess.check_output(['git','-c','core.fsmonitor=false','-C',str(root),'status','--porcelain=v1'],text=True)
    if dirty and not preview:raise ValueError('Installer publication requires committed source; use explicit local preview mode before commit')
    if not (preview and dirty):verify_committed_package(root,head,manifest)
    manifest['source_commit']=None if preview and dirty else commit
    manifest['preview_only']=bool(preview and dirty)
    manifest['source_commit_rule']='Uncommitted local preview; no immutable public source revision is claimed.' if manifest['preview_only'] else 'Exact committed source revision supplied by the build.'
    destination=out/'reports/capability-installer';destination.mkdir(parents=True,exist_ok=True)
    for name in expected:shutil.copyfile(source/name,destination/name)
    encoded=json.dumps(manifest,indent=2)+'\n'
    if '__BUILD_GIT_SHA__' in encoded:raise ValueError('Unresolved installer source marker')
    (destination/'manifest.json').write_text(encoded)
    return manifest


def validate_download(root,out,package,served):
    destination=out/'reports/capability-installer'
    validate_package(package)
    if set(served)!=FIELDS|{'preview_only'} or served.get('schema_version')!=package['schema_version'] or served.get('files')!=package['files']:raise ValueError('Served installer differs from reviewed package')
    expected={entry['path']:entry for entry in package['files']}
    if {p.name for p in destination.iterdir()}!=set(expected)|{'manifest.json'} or any(p.is_symlink() for p in destination.iterdir()):raise ValueError('Unexpected installer download payload')
    for name,entry in expected.items():
        body=(destination/name).read_bytes()
        if len(body)!=entry['bytes'] or hashlib.sha256(body).hexdigest()!=entry['sha256']:raise ValueError('Installer download hash differs')
    head=subprocess.check_output(['git','-c','core.fsmonitor=false','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    preview=os.environ.get('CAPABILITY_INSTALLER_PREVIEW')=='1' and os.environ.get('GITHUB_ACTIONS')!='true'
    if served.get('preview_only') is True:
        if not preview or served.get('source_commit') is not None:raise ValueError('Uncommitted preview cannot be published')
    elif served.get('preview_only') is not False or served.get('source_commit')!=head:raise ValueError('Installer source is not the current committed revision')
    if not served.get('preview_only'):verify_committed_package(root,head,package)
    for key in FIELDS-{'source_commit','source_commit_rule'}:
        if served.get(key)!=package[key]:raise ValueError('Served installer metadata differs')
    if '__BUILD_GIT_SHA__' in json.dumps(served):raise ValueError('Unresolved installer source marker')
    return True
