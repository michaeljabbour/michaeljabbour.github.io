"""Ensure public downloads cannot publish private or contradictory metadata."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from public_views import validate_status,validate_csv,status_csv

class PublicMetadataBoundary(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'content/public-capability-status.json').read_text())
        self.ids={r['id'] for r in self.data['records']}
    def test_valid_snapshot_and_csv_agree(self):
        validate_status(self.data,self.ids)
        self.assertEqual(status_csv(self.data),validate_csv(status_csv(self.data),self.data))
    def test_unrelated_private_csv_is_rejected(self):
        with self.assertRaises(ValueError):validate_csv('private_notes\nFICTIONAL_PRIVATE_CANARY\n',self.data)
    def test_missing_or_changed_csv_rows_are_rejected(self):
        rows=status_csv(self.data).splitlines(keepends=True)
        for raw in [''.join(rows[:-1]),''.join(rows).replace(self.data['records'][0]['title'],'FICTIONAL_PRIVATE_CANARY',1),''.join(rows+rows[1:2])]:
            with self.assertRaises(ValueError):validate_csv(raw,self.data)
    def test_nested_unreviewed_object_cannot_be_public_text(self):
        for field in ['title','category']:
            changed=copy.deepcopy(self.data);changed['records'][0][field]={'private':'FICTIONAL_PRIVATE_CANARY'}
            with self.assertRaises(ValueError):validate_status(changed,self.ids)
    def test_study_set_cannot_expand_or_change(self):
        changed=copy.deepcopy(self.data);changed['study_repositories'][0]['repository_url']='https://github.com/fictional/private-canary'
        with self.assertRaises(ValueError):validate_status(changed,self.ids)
    def test_module_test_values_are_typed_and_scoped(self):
        changed=copy.deepcopy(self.data);changed['supplemental_module_repairs'][0]['test_matrix'][0]['passed']={'private':'FICTIONAL_PRIVATE_CANARY'}
        with self.assertRaises(ValueError):validate_status(changed,self.ids)
    def test_unknown_status_and_inconsistent_counts_are_rejected(self):
        changed=copy.deepcopy(self.data);changed['records'][0]['pages_status']='not-yet-verified-but-pass'
        with self.assertRaises(ValueError):validate_status(changed,self.ids)
        changed=copy.deepcopy(self.data);changed['counts']['published_records']=(changed['counts']['published_records']+1)%34
        with self.assertRaises(ValueError):validate_status(changed,self.ids)
if __name__=='__main__':unittest.main()
