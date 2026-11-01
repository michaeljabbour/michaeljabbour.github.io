"""Canonical navigation must not regress to working-but-legacy URLs."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check import canonical_navigation_errors


class CanonicalNavigation(unittest.TestCase):
    def setUp(self):
        self.catalogue = json.loads((ROOT / "content/portfolio.json").read_text())
        self.media = json.loads((ROOT / "content/media.json").read_text())
        self.mapping = json.loads((ROOT / "content/migration/mapping.json").read_text())
        self.by_id = {row["id"]: row for row in self.mapping["repositories"]}

    def errors(self, catalogue=None, media=None, mapping=None):
        return canonical_navigation_errors(
            catalogue or self.catalogue,
            media or self.media,
            mapping or self.mapping,
        )

    def test_all_current_canonical_destinations_are_accepted(self):
        self.assertEqual([], self.errors())
        self.assertEqual(36, len(self.catalogue["projects"]))

    def test_each_legacy_repository_guide_install_and_film_link_is_rejected(self):
        # HTTPS and working redirects are not enough: every active destination
        # must use the canonical prefix from the independently maintained map.
        for index, project in enumerate(self.catalogue["projects"]):
            if project["id"] not in self.by_id:
                continue
            row = self.by_id[project["id"]]
            for field in ("repo_url", "site_url", "install_url", "film_url"):
                with self.subTest(capability=project["id"], field=field):
                    catalogue = copy.deepcopy(self.catalogue)
                    media = copy.deepcopy(self.media)
                    if field == "repo_url":
                        catalogue["projects"][index][field] = row["old_url"]
                    elif field == "film_url":
                        media["films"][project["id"]][field] = media["films"][project["id"]][field].replace(row["new_pages_url"], row["old_pages_url"], 1)
                    else:
                        catalogue["projects"][index][field] = project[field].replace(row["new_pages_url"], row["old_pages_url"], 1)
                    self.assertTrue(any(project["id"] in error and field in error for error in self.errors(catalogue, media)))

    def test_wrong_repository_host_and_query_are_not_canonical(self):
        for changed in (
            "https://github.example.invalid/michaeljabbour/amplifier-capability-unknowns",
            self.catalogue["projects"][0]["repo_url"] + "?legacy=1",
        ):
            catalogue = copy.deepcopy(self.catalogue)
            catalogue["projects"][0]["repo_url"] = changed
            self.assertTrue(self.errors(catalogue))

    def test_new_guides_use_the_main_site_and_actual_readme_setup(self):
        additions = {"articlecraft", "idea-talks", "stories"}
        for index, project in enumerate(self.catalogue["projects"]):
            if project["id"] not in additions:
                continue
            for field in ["repo_url", "site_url", "install_url"]:
                with self.subTest(capability=project["id"], field=field):
                    changed = copy.deepcopy(self.catalogue)
                    changed["projects"][index][field] = "https://example.invalid/unverified/"
                    self.assertTrue(any(project["id"] in error for error in self.errors(changed)))

    def test_missing_fragment_and_offsite_install_are_rejected(self):
        ident = self.catalogue["projects"][0]["id"]
        media = copy.deepcopy(self.media)
        media["films"][ident]["film_url"] = self.by_id[ident]["new_pages_url"]
        self.assertTrue(any("film_url" in e for e in self.errors(media=media)))
        catalogue = copy.deepcopy(self.catalogue)
        catalogue["projects"][0]["install_url"] = "https://example.invalid/#install"
        self.assertTrue(any("install_url" in e for e in self.errors(catalogue)))

    def test_legacy_mapping_and_missing_or_duplicate_identity_are_rejected(self):
        mapping = copy.deepcopy(self.mapping)
        row = mapping["repositories"][0]
        row["new_repository"] = row["old_repository"]
        row["new_url"] = row["old_url"]
        row["new_pages_url"] = row["old_pages_url"]
        self.assertTrue(any("canonical migration" in e for e in self.errors(mapping=mapping)))
        for rows in (self.mapping["repositories"][:-1], self.mapping["repositories"] + [self.mapping["repositories"][0]]):
            mapping = copy.deepcopy(self.mapping)
            mapping["repositories"] = copy.deepcopy(rows)
            self.assertTrue(any("exactly once" in e for e in self.errors(mapping=mapping)))

    def test_legacy_assets_and_historical_evidence_are_not_rewritten(self):
        # They are compatibility payloads, not active navigation. Their presence
        # must not cause a blanket rename or a false canonical-link failure.
        media = copy.deepcopy(self.media)
        ident = self.catalogue["projects"][0]["id"]
        row = self.by_id[ident]
        media["films"][ident]["src"] = row["old_pages_url"] + "assets/fixture.mp4"
        media["films"][ident]["checks"] = {"historical_url": row["old_pages_url"]}
        self.assertEqual([], self.errors(media=media))


if __name__ == "__main__":
    unittest.main()
