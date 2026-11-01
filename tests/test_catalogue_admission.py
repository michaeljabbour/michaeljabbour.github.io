"""Admission boundaries use synthetic verification records, never live claims."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from catalogue_admission import ADDITIONAL_IDS, HISTORICAL_IDS, validate_catalogue
from check_release import validate_artifact


class AdditionAdmission(unittest.TestCase):
    def setUp(self):
        self.catalogue = json.loads((ROOT / "content/portfolio.json").read_text())
        self.mapping = json.loads((ROOT / "content/migration/mapping.json").read_text())
        self.prepared = json.loads((ROOT / "content/additions.json").read_text())
        self.prepared["publication_ready"] = False
        for entry in self.prepared["capabilities"]:
            entry.update(source_commit=None, repository_verified=False, verified_at=None)

    def verified(self):
        result = copy.deepcopy(self.prepared)
        result["publication_ready"] = True
        for entry in result["capabilities"]:
            entry.update(source_commit="a" * 40, repository_verified=True, verified_at="2020-01-01T00:00:00Z")
        return result

    def validate(self, publication=None, **kwargs):
        return validate_catalogue(self.catalogue, self.mapping, publication or self.prepared, **kwargs)

    def test_historical_33_can_build_without_additions(self):
        catalogue = copy.deepcopy(self.catalogue)
        catalogue["projects"] = [project for project in catalogue["projects"] if project["id"] in HISTORICAL_IDS]
        result = validate_catalogue(catalogue, self.mapping, {"schema_version": "portfolio-additions/v1", "publication_ready": True, "capabilities": []})
        self.assertTrue(result["publication_ready"])
        self.assertEqual(33, len(result["capability_ids"]))

    def test_unverified_36_requires_explicit_local_preview(self):
        with self.assertRaises(ValueError):
            self.validate()
        result = self.validate(preview=True)
        self.assertTrue(result["preview_only"])
        self.assertFalse(result["publication_ready"])
        self.assertEqual(36, len(result["capability_ids"]))

    def test_ci_rejects_even_verified_preview_override(self):
        with self.assertRaises(ValueError):
            self.validate(self.verified(), preview=True, ci=True)
        self.assertTrue(self.validate(self.verified(), ci=True)["publication_ready"])

    def test_flag_does_not_replace_pin_and_repository_verification(self):
        for changes in [
            {"repository_verified": False}, {"repository_verified": "true"},
            {"source_commit": None}, {"source_commit": "short"},
            {"source_commit": "0" * 40}, {"verified_at": None},
            {"verified_at": "2099-01-01T00:00:00Z"},
            {"verified_at": "2020-01-01T00:00:00"},
            {"repository_url": "https://github.com/other/unverified"},
        ]:
            with self.subTest(changes=changes):
                publication = self.verified()
                publication["capabilities"][0].update(changes)
                with self.assertRaises(ValueError):
                    self.validate(publication)

    def test_unknown_duplicate_or_unlisted_addition_is_rejected(self):
        for mode in ["unknown", "duplicate", "unlisted"]:
            with self.subTest(mode=mode):
                publication = self.verified()
                if mode == "unknown":
                    publication["capabilities"][0]["id"] = "another-capability"
                elif mode == "duplicate":
                    publication["capabilities"].append(copy.deepcopy(publication["capabilities"][0]))
                else:
                    publication["capabilities"].pop()
                with self.assertRaises(ValueError):
                    self.validate(publication, preview=True)

    def test_missing_historical_identity_or_rewritten_pair_is_rejected(self):
        catalogue = copy.deepcopy(self.catalogue)
        catalogue["projects"] = catalogue["projects"][1:]
        with self.assertRaises(ValueError):
            validate_catalogue(catalogue, self.mapping, self.verified())
        for change in ["id", "old_repository", "new_repository"]:
            mapping = copy.deepcopy(self.mapping)
            mapping["repositories"][0][change] = "stories"
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_catalogue(self.catalogue, mapping, self.verified())

    @patch.dict("os.environ", {"PORTFOLIO_PREVIEW": "0"})
    def test_artifact_cannot_promote_unverified_source_or_other_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "content/migration").mkdir(parents=True)
            (root / "dist").mkdir()
            (root / "content/portfolio.json").write_text(json.dumps(self.catalogue))
            (root / "content/migration/mapping.json").write_text(json.dumps(self.mapping))
            (root / "content/additions.json").write_text(json.dumps(self.prepared))
            verified = self.verified()
            admitted = self.validate(verified)
            artifact = {"schema_version": "portfolio-artifact/v1", "source_commit": "b" * 40,
                        "preview_only": False, "publication_ready": True,
                        "capability_ids": admitted["capability_ids"], "additional_sources": admitted["additions"]}
            (root / "dist/publication.json").write_text(json.dumps(artifact))
            (root / "dist/portfolio.json").write_text(json.dumps(self.catalogue))
            with self.assertRaises(ValueError):
                validate_artifact(root, for_publication=True)
            (root / "content/additions.json").write_text(json.dumps(verified))
            with patch("check_release.subprocess.check_output", side_effect=["b" * 40 + "\n", ""]):
                self.assertTrue(validate_artifact(root, for_publication=True)["publication_ready"])
            with patch.dict("os.environ", {"PORTFOLIO_PREVIEW": "1"}), self.assertRaises(ValueError):
                validate_artifact(root, for_publication=True)
            for changes in [{"source_commit": "c" * 40}, {"preview_only": True}, {"additional_sources": {}}]:
                changed = dict(artifact, **changes)
                (root / "dist/publication.json").write_text(json.dumps(changed))
                with self.subTest(changes=list(changes)), patch("check_release.subprocess.check_output", return_value="b" * 40 + "\n"), self.assertRaises(ValueError):
                    validate_artifact(root, for_publication=True)


if __name__ == "__main__":
    unittest.main()
