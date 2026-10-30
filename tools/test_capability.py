import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC=importlib.util.spec_from_file_location('capability',Path(__file__).with_name('capability.py'))
cap=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(cap)

class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name).resolve();self.source=self.base/'source';self.source.mkdir();self.dest=self.base/'project'
        self.skill=self.source/'skills'/'fixture';self.skill.mkdir(parents=True)
        (self.skill/'SKILL.md').write_text('---\nname: fixture\ndescription: Test fixture\n---\nRead [guide](guide.md).\n')
        (self.skill/'guide.md').write_text('Fixture method.\n');(self.skill/'LICENSE').write_text('MIT fixture\n')
        subprocess.run(['git','init','-q',str(self.source)],check=True)
        self.commit()
        self.data={'contract_version':cap.CONTRACT,'id':'fixture','name':'amplifier-capability-fixture','legacy_names':['amplifier-skill-fixture'],'version':None,'kind':'skill','engine':'LLM','promise':'A fixture','surfaces':['agent-skills'],'interfaces':{'method':'caller-applied'},'permissions':{'installation':{'network':False,'execution':False}},'dataflow':{'installation':'local copy'},'portable_method':{'name':'fixture','path':'skills/fixture','include':['.']}}
        self.data.update({'engine_components':{'caller':'LLM'},'source_policy':{'revision':'explicit full SHA'}})
        self.manifest=self.source/'capability.json';self.save()
    def tearDown(self):self.tmp.cleanup()
    def commit(self):
        subprocess.run(['git','-C',str(self.source),'add','.'],check=True)
        subprocess.run(['git','-C',str(self.source),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--no-gpg-sign','-qm','fixture'],check=True)
        self.rev=cap.git(self.source,'rev-parse','HEAD')
    def save(self):self.manifest.write_text(json.dumps(self.data));self.commit()
    def plan(self,h='all',operation='install'):return cap.plan(self.source,self.manifest,self.rev,self.dest,h,operation)
    def apply(self,p=None):
        p=p or self.plan();return cap.apply_plan(p,self.data,self.skill,p['plan_hash'])
    def test_preview_has_no_writes(self):
        p=self.plan();self.assertFalse(self.dest.exists());self.assertEqual(3,len(p['targets']));self.assertFalse(p['blocked'])
    def test_pin_is_required_and_exact(self):
        with self.assertRaises(ValueError):cap.source_files(self.source,self.data,'main')
        with self.assertRaises(ValueError):cap.source_files(self.source,self.data,'0'*40)
    def test_contract_is_bound_to_the_source_pin(self):
        altered={**self.data,'promise':'different'}
        with self.assertRaises(ValueError):cap.source_files(self.source,altered,self.rev)
    def test_selected_dirty_source_is_rejected(self):
        (self.skill/'guide.md').write_text('changed')
        with self.assertRaises(ValueError):self.plan()
    def test_untracked_private_material_not_copied(self):
        (self.skill/'private.txt').write_text('private')
        self.assertNotIn('private.txt',self.plan()['files'])
    def test_rejects_name_mismatch(self):
        self.data['portable_method']['name']='wrong';self.save()
        with self.assertRaises(ValueError):self.plan()
    def test_rejects_escape_in_manifest(self):
        self.data['portable_method']['path']='../outside';self.save()
        with self.assertRaises(ValueError):self.plan()
    def test_install_dedupes_six_harnesses_and_do_not_execute(self):
        p=self.plan();self.apply(p)
        self.assertEqual(3,len(list(self.dest.glob('*/skills/fixture'))))
        self.assertEqual(['codex','gemini','grok','opencode'],next(x['harnesses'] for x in p['targets'] if '.agents' in x['path']))
        self.assertTrue(all(x['status']=='owned-clean' for x in self.plan()['targets']))
    def test_plan_confirmation_detects_target_changes(self):
        p=self.plan();self.apply(p);new=self.plan()
        with self.assertRaises(ValueError):cap.apply_plan(new,self.data,self.skill,p['plan_hash'])
    def test_foreign_destination_never_overwritten(self):
        target=self.dest/'.agents/skills/fixture';target.mkdir(parents=True);(target/'mine').write_text('retain')
        p=self.plan();self.assertTrue(p['blocked'])
        with self.assertRaises(ValueError):self.apply(p)
        self.assertEqual('retain',(target/'mine').read_text());self.assertFalse((self.dest/'.claude').exists())
    def test_edited_install_refused(self):
        self.apply();p=self.plan();target=Path(p['targets'][0]['path']);(target/'guide.md').write_text('edited')
        p=self.plan();self.assertTrue(p['blocked'])
        with self.assertRaises(ValueError):self.apply(p)
    def test_extra_nested_receipt_counts_as_edit(self):
        self.apply();target=Path(self.plan()['targets'][0]['path']);(target/'extra').mkdir();(target/'extra'/cap.RECEIPT).write_text('keep')
        self.assertTrue(self.plan()['blocked'])
    def test_legacy_identity_upgrade_is_recognized(self):
        self.apply();target=Path(self.plan()['targets'][0]['path']);receipt=json.loads((target/cap.RECEIPT).read_text());receipt['capability']='amplifier-skill-fixture';(target/cap.RECEIPT).write_text(json.dumps(receipt))
        self.assertFalse(self.plan()['blocked']);self.apply()
    def test_symlink_parent_is_refused(self):
        outside=self.base/'outside';outside.mkdir();self.dest.mkdir();(self.dest/'.agents').symlink_to(outside,target_is_directory=True)
        with self.assertRaises(ValueError):self.plan()
    def test_symlink_receipt_is_refused(self):
        self.apply();target=Path(self.plan()['targets'][0]['path']);receipt=target/cap.RECEIPT;outside=self.base/'outside.json';outside.write_bytes(receipt.read_bytes());receipt.unlink();receipt.symlink_to(outside)
        with self.assertRaises(ValueError):self.plan()
    def test_traversal_receipt_is_refused(self):
        self.apply();target=Path(self.plan()['targets'][0]['path']);receipt=json.loads((target/cap.RECEIPT).read_text());receipt['files']['../outside']='0'*64;(target/cap.RECEIPT).write_text(json.dumps(receipt))
        with self.assertRaises(ValueError):self.plan()
    def test_install_rollback_restores_absence(self):
        result=self.apply();cap.rollback(result['transaction']);self.assertTrue(all(x['status']=='absent' for x in self.plan()['targets']))
    def test_upgrade_rollback_restores_prior_version(self):
        self.apply();(self.skill/'guide.md').write_text('version two');self.commit();result=self.apply();cap.rollback(result['transaction'])
        self.assertTrue(all((Path(x['path'])/'guide.md').read_text()=='Fixture method.\n' for x in self.plan()['targets']))
    def test_rollback_refuses_intervening_edits(self):
        result=self.apply();target=Path(self.plan()['targets'][0]['path']);(target/'guide.md').write_text('keep mine')
        with self.assertRaises(ValueError):cap.rollback(result['transaction'])
        self.assertEqual('keep mine',(target/'guide.md').read_text())
    def test_uninstall_is_reversible(self):
        self.apply();p=self.plan(operation='uninstall');r=cap.apply_plan(p,self.data,self.skill,p['plan_hash']);self.assertTrue(all(x['status']=='absent' for x in self.plan()['targets']));cap.rollback(r['transaction']);self.assertTrue(all(x['status']=='owned-clean' for x in self.plan()['targets']))
    def test_failed_second_target_restores_first(self):
        self.apply();before=self.plan();real=cap.shutil.copyfile;calls=[]
        def fail(src,dst):
            calls.append(str(dst))
            if len(calls)==4:raise OSError('planted copy failure')
            return real(src,dst)
        with patch.object(cap.shutil,'copyfile',side_effect=fail):
            with self.assertRaises(OSError):self.apply()
        after=self.plan();self.assertEqual(before['plan_hash'],after['plan_hash'])
    def test_native_component_not_faked_as_skill(self):
        self.data['portable_method']=None;self.data['kind']='library';self.data['engine']='None';self.save();p=self.plan();self.assertFalse(p['installable']);self.assertFalse(self.dest.exists())
    def test_claude_alias_preserves_pilot_key(self):
        self.assertEqual(self.plan('claude')['targets'],self.plan('claude-code')['targets'])
    def test_missing_doctor_has_nonzero_status(self):
        r=subprocess.run([sys.executable,str(Path(__file__).with_name('capability.py')),'doctor','--manifest',str(self.manifest),'--source',str(self.source),'--revision',self.rev,'--dest',str(self.dest)],capture_output=True,text=True)
        self.assertEqual(2,r.returncode);self.assertFalse(json.loads(r.stdout)['healthy']);self.assertFalse(self.dest.exists())
    def test_forged_duplicate_rollback_is_refused(self):
        result=self.apply();path=Path(result['transaction']);j=json.loads(path.read_text());j['moves'].append(j['moves'][0]);path.write_text(json.dumps(j))
        with self.assertRaises(ValueError):cap.rollback(path)
        self.assertTrue(all(x['status']=='owned-clean' for x in self.plan()['targets']))

if __name__=='__main__':unittest.main()
