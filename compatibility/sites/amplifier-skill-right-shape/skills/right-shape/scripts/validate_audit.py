#!/usr/bin/env python3
"""Check a Right Shape audit machine record against a retained source inventory.

Reads files/stdin only. No model, network or source changes. Structural checks
cannot establish sound ownership, license status, audience demand or gate truth.
"""
import argparse
import json
from pathlib import Path
import sys
from validate_placement import read_rubric, validate as validate_placement


def text(value, field):
    if not isinstance(value,str) or not value.strip():raise ValueError(field+': non-empty text required')


def inventory_sources(inventory):
    if not isinstance(inventory,dict):raise ValueError('Source inventory must be an object')
    rows=inventory.get('sources',inventory.get('repositories',[]))
    result={}
    for source in rows:
        sid=source['id']
        if sid in result:raise ValueError('Duplicate source inventory ID: '+sid)
        paths=set(source.get('paths',source.get('files',{})))
        methods={p for p in paths if Path(p).name.lower()=='skill.md'}
        result[sid]={'revision':source['revision'],'paths':paths,
                     'methods':set(source.get('embedded_methods',methods)),
                     'fork':source.get('metadata',{}).get('fork')}
    if not result:raise ValueError('Source inventory is empty')
    return result


def validate_audit(audit,inventory):
    if not isinstance(audit,dict):raise ValueError('Audit must be an object')
    if audit.get('schema_version')!='right-shape-audit/v1':raise ValueError('Unsupported audit version')
    for key in ['sources','capabilities','routes','method_routes']:
        if not isinstance(audit.get(key),list):raise ValueError(key+' must be a list')
    rules=read_rubric((Path(__file__).resolve().parents[1]/'references/rubric.md').read_text())
    dispositions={row[0]for row in rules['dispositions']};known=inventory_sources(inventory)
    sources=audit['sources'];source_ids=[s['id']for s in sources]
    if len(set(source_ids))!=len(source_ids) or set(source_ids)!=set(known):raise ValueError('Source census coverage differs from the retained inventory')
    for source in sources:
        sid=source['id']
        if source['revision']!=known[sid]['revision']:raise ValueError('Source revision mismatch: '+sid)
        if source['primary_disposition']not in dispositions:raise ValueError('Unknown primary disposition: '+sid)
        if known[sid]['fork']is True and source['primary_disposition']!='Fork':raise ValueError('Confirmed fork needs its Fork source bucket: '+sid)
        if source['scope']not in ['public','supplemental']:raise ValueError('Unknown source scope: '+sid)
        text(source['bucket'],'source bucket')
    caps=audit['capabilities'];cap_ids=[c['id']for c in caps]
    if len(set(cap_ids))!=len(cap_ids):raise ValueError('Duplicate capability ID')
    for cap in caps:
        text(cap['id'],'capability ID');text(cap['promise'],'promise/asset value');text(cap['shape'],'shape')
        if cap['kind']not in ['public','internal','asset']:raise ValueError('Unknown capability kind')
        placement=cap['placement']
        if placement is not None:validate_placement(placement)
        elif cap['kind']=='public':raise ValueError('Public capability is missing a placement: '+cap['id'])
    path_count=0
    for route in audit['routes']:
        sid=route['source_id']
        if sid not in known or route['capability_id']not in cap_ids:raise ValueError('Route references an unknown source/capability')
        if route['source_revision']!=known[sid]['revision']:raise ValueError('Route revision mismatch: '+sid)
        if not isinstance(route['source_paths'],list) or not route['source_paths']:raise ValueError('Route needs a list of source paths')
        for path in route['source_paths']:
            text(path,'source path');path=path.rstrip('/')
            if path not in known[sid]['paths'] and not any(p.startswith(path+'/')for p in known[sid]['paths']):raise ValueError('Source path absent: '+sid+'/'+path)
            path_count+=1
        for field in ['target_repo','target_path','interface','reason']:text(route[field],field)
        if route['target_status']not in ['existing','proposed']:raise ValueError('Unknown target status')
        if route['action']not in dispositions:raise ValueError('Unknown route action')
        if route['role']not in ['method','tool','harness','adapter','eval','reference','research']:raise ValueError('Unknown route role')
    expected={(sid,p)for sid,s in known.items()for p in s['methods']}
    actual=[]
    for method in audit['method_routes']:
        key=(method['source_id'],method['path']);actual.append(key)
        for field in ['destination','provenance']:text(method[field],field)
    if len(set(actual))!=len(actual) or set(actual)!=expected:raise ValueError('Embedded method coverage differs from inventory')
    routed_caps={r['capability_id']for r in audit['routes']}
    if set(cap_ids)-routed_caps:raise ValueError('Capability/asset has no concrete source route')
    return {'valid':True,'sources':len(sources),'capability_and_asset_records':len(caps),
            'routes':len(audit['routes']),'source_path_occurrences':path_count,'embedded_methods':len(actual),
            'scope':'Structure/coverage only; semantic review and authorization remain necessary.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('audit',type=Path);parser.add_argument('--inventory',required=True,type=Path)
    args=parser.parse_args()
    try:result=validate_audit(json.loads(args.audit.read_text()),json.loads(args.inventory.read_text()))
    except (ValueError,KeyError,TypeError,OSError)as error:
        print(json.dumps({'valid':False,'error':str(error)}),file=sys.stderr);return 2
    print(json.dumps(result));return 0


if __name__=='__main__':sys.exit(main())
