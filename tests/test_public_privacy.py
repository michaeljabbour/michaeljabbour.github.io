import hashlib
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from public_privacy import reviewed_example_text

class ReviewedExampleBinding(unittest.TestCase):
    def entry(self,raw,literal):
        digest=hashlib.sha256(raw.encode()).hexdigest()
        return {'sha256':digest,'reviewed_public_examples':[{'literal':literal,'reason':'Fictional documented example','reviewed_file_sha256':digest}]}
    def test_only_exact_reviewed_literal_is_removed(self):
        literal='file:///path/to/module';raw='Example '+literal+' UNREVIEWED_PRIVATE_SENTINEL'
        scrubbed=reviewed_example_text(raw,raw.encode(),self.entry(raw,literal))
        self.assertNotIn(literal,scrubbed);self.assertIn('UNREVIEWED_PRIVATE_SENTINEL',scrubbed)
    def test_changed_file_cannot_reuse_review(self):
        raw='file:///path/to/module';entry=self.entry(raw,raw)
        with self.assertRaises(ValueError):reviewed_example_text(raw+' changed',(raw+' changed').encode(),entry)
    def test_review_hash_must_match_exact_file(self):
        raw='file:///path/to/module';entry=self.entry(raw,raw);entry['reviewed_public_examples'][0]['reviewed_file_sha256']='0'*64
        with self.assertRaises(ValueError):reviewed_example_text(raw,raw.encode(),entry)
    def test_missing_literal_cannot_silently_mask_a_file(self):
        raw='ordinary public text';entry=self.entry(raw,'file:///path/to/module')
        with self.assertRaises(ValueError):reviewed_example_text(raw,raw.encode(),entry)
    def test_no_review_keeps_all_content(self):
        raw='UNREVIEWED_PRIVATE_SENTINEL'
        self.assertEqual(reviewed_example_text(raw,raw.encode(),{}),raw)
if __name__=='__main__':unittest.main()
