"""Publishing must bind the reviewed payload to real committed Git objects."""
import copy,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from installer_download import validate_package,verify_committed_package,FILES

class InstallerPublicationBoundary(unittest.TestCase):
    def setUp(self):self.package=json.loads((ROOT/'tools/PACKAGE.json').read_text())
    def test_rejects_hidden_metadata_and_malformed_file_records(self):
        cases=[]
        d=copy.deepcopy(self.package);d['private_notes']='FICTIONAL_PRIVATE_CANARY';cases.append(d)
        d=copy.deepcopy(self.package);d['files'][0]['private_notes']='FICTIONAL_PRIVATE_CANARY';cases.append(d)
        d=copy.deepcopy(self.package);d['files'][0]=copy.deepcopy(d['files'][1]);cases.append(d)
        d=copy.deepcopy(self.package);d['files'][0]['bytes']=True;cases.append(d)
        d=copy.deepcopy(self.package);d['files'][0]['sha256']='not-a-hash';cases.append(d)
        for data in cases:
            with self.assertRaises(ValueError):validate_package(data)
        validate_package(self.package)
    def test_clean_ignored_payload_is_not_proof_of_committed_source(self):
        with tempfile.TemporaryDirectory(prefix='installer-publish-') as temp:
            root=Path(temp);(root/'tools').mkdir()
            for name in [*FILES,'PACKAGE.json']:(root/'tools'/name).write_bytes((ROOT/'tools'/name).read_bytes())
            def git(*args):return subprocess.check_output(['git','-c','user.name=Fictional Test','-c','user.email=fixture@example.invalid','-C',str(root),*args],stderr=subprocess.DEVNULL).decode().strip()
            git('init','-q');(root/'.gitignore').write_text('tools/\n');git('add','.gitignore');git('commit','-qm','fixture');head=git('rev-parse','HEAD')
            self.assertEqual('',git('status','--porcelain'))
            with self.assertRaises(ValueError):verify_committed_package(root,head,self.package)
            git('add','-f','tools');git('commit','-qm','track fixture package');head=git('rev-parse','HEAD')
            verify_committed_package(root,head,self.package)
            (root/'tools/README.md').write_text('changed fixture')
            with self.assertRaises(ValueError):verify_committed_package(root,head,self.package)
if __name__=='__main__':unittest.main()
