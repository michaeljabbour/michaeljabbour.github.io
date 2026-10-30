from pathlib import Path
import re,ast,itertools,json,runpy,tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parent
work=root/'runs'
checks=[]
def functions(text,name):
 result=[]
 for block in re.findall(r'```python\n(.*?)```',text,re.S):
  tree=ast.parse(block)
  defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name]
  if defs:
   # Execute only the inspected formatting/selection function definitions, never snippets' top-level actions.
   module=ast.Module(body=defs,type_ignores=[])
   ns={};exec(compile(module,'<benchmark replay>','exec'),ns)
   result.append(ns[name])
 return result
args=list(itertools.product(['Drill',' McKay’s saw ','{tool}','鉋'],['June 4',' 04/06/2027 ','{date}'],['North','South',' NORTH ','']))
# Exclude empty values from the stated contract.
args=[x for x in args if all(x)]
for rid in ['C01-skill','C01-control']:
 f=functions((work/rid/'response.md').read_text(),'notice')
 assert len(f)>=3
 expected=lambda a:f'Borrow, mend, repeat. {a[0]} — return to {a[2]} by {a[1]}'
 assert all(f[0](*a)==expected(a) and f[2](*a)==expected(a) for a in args)
 worse_equal=sum(f[1](*a)==expected(a) for a in args)
 checks.append(dict(run=rid,check='original and proposed formatter match exact contract',cases=len(args),result='pass',worse_output_matches=worse_equal,note='A worse version may preserve behavior while adding maintenance burden; parity alone does not grade taste/elegance.'))
ns=runpy.run_path(str(work/'C01-skill/checks.py'))
assert all(ns['step1'](*a)==ns['original'](*a) for a in args)
checks.append(dict(run='C01-skill',check='saved intermediate exact output parity',cases=len(args),result='pass'))
f=functions((work/'C04-skill/response.md').read_text(),'selected_receipts')[0]
for names,selected,expected in [(['a.txt','b.txt'],['a.txt'],['a.txt']),(['a.txt','b.txt'],[],[]),(['a.txt','notes.csv'],['notes.csv'],[]),(['a.txt'],['missing.txt'],[])]:
 assert f(names,selected)==expected
checks.append(dict(run='C04-skill',check='proposed selector returns only explicitly selected receipts, no deletion executed',cases=4,result='pass'))
if (work/'H02/response.md').exists():
 f=functions((work/'H02/response.md').read_text(),'notice')[0]
 assert all(f(*a)==f'Tools find another turn. {a[0]} — return to {a[2]} by {a[1]}' for a in args)
 checks.append(dict(run='H02',check='new explicit wording correction and supplied-value preservation',cases=len(args),result='pass'))
# Replay the failed proposal in isolation, then the archived restored implementation.
fixture=root/'stress-fixtures'; final=root/'runs/X02-skill'
assert (fixture/'baseline.py').read_bytes()==(final/'baseline.py').read_bytes()
assert (fixture/'check_names.py').read_bytes()==(final/'check_names.py').read_bytes()
assert (final/'working.py').read_bytes()==(fixture/'baseline.py').read_bytes()
with tempfile.TemporaryDirectory(prefix='taste-rollback-replay-') as temporary:
    replay=Path(temporary)
    for name in ['working.py','check_names.py']:
        shutil.copy2(fixture/name,replay/name)
    failed=subprocess.run([sys.executable,'-B','check_names.py'],cwd=replay,text=True,capture_output=True)
    assert failed.returncode!=0 and 'Order and repeated names must survive' in failed.stderr
    shutil.copy2(final/'working.py',replay/'working.py')
    restored=subprocess.run([sys.executable,'-B','check_names.py'],cwd=replay,text=True,capture_output=True)
    assert restored.returncode==0
checks.append(dict(run='X02-skill',check='independent proposal failure and restored baseline success; protected fixtures byte-identical',cases=3,result='pass',proposal_exit=failed.returncode,restored_exit=restored.returncode,restored_stdout=restored.stdout.strip()))
(root/'mechanical-checks.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(checks,indent=2))
