"""Reject broken shared-card memberships and unsafe/unreviewed comparison data."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from flow_views import load_flows, flow_guide
from related_tools import load_related_tools, render_related_tools


class PublicDataContracts(unittest.TestCase):
    def setUp(self):
        self.projects = json.loads((ROOT / "content/portfolio.json").read_text())["projects"]
        self.flows = json.loads((ROOT / "content/flows.json").read_text())
        self.related = json.loads((ROOT / "content/related-tools.json").read_text())

    def load(self, name, data, callback):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "content").mkdir()
            (root / "content" / name).write_text(json.dumps(data))
            return callback(root, self.projects if name == "flows.json" else [x["id"] for x in self.projects])

    def test_overlapping_flows_render_each_capability_once(self):
        flows = load_flows(ROOT, self.projects)
        html = flow_guide(flows, self.projects, lambda project: "", [])
        for project in self.projects:
            self.assertEqual(1, html.count('data-flow-project="' + project["id"] + '"'))
        self.assertGreater(len(flows["memberships"]["taste-elegance"]), 1)

    def test_missing_unknown_and_duplicate_memberships_are_rejected(self):
        for mutate in [
            lambda data: data["memberships"].pop("knowledge"),
            lambda data: data["memberships"].update({"not-public": ["research"]}),
            lambda data: data["memberships"].update({"knowledge": ["research", "research"]}),
            lambda data: data["memberships"].update({"knowledge": ["unreviewed"]}),
        ]:
            with self.subTest(mutate=mutate):
                data = copy.deepcopy(self.flows)
                mutate(data)
                with self.assertRaises(ValueError):
                    self.load("flows.json", data, load_flows)

    def test_stage_assignments_cannot_drift_between_flows(self):
        for mutate in [
            lambda data: data.update({"private_notes": "Do not publish raw review notes"}),
            lambda data: data["stage_memberships"].pop("knowledge"),
            lambda data: data["stage_memberships"]["knowledge"].update({"creative": ["make"]}),
            lambda data: data["stage_memberships"]["knowledge"].update({"research": ["build"]}),
            lambda data: data["stage_memberships"]["knowledge"].update({"research": ["connect", "connect"]}),
            lambda data: data["flows"][0]["stages"].reverse(),
        ]:
            data = copy.deepcopy(self.flows)
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                self.load("flows.json", data, load_flows)

    def test_reviewed_stage_examples_have_exact_members(self):
        examples = {
            ("software", "build"): {"build-amplifier", "build-tauri", "build-with-torque", "forge", "desktop-tasks", "image-provider", "migrate", "transfer", "data-substrate"},
            ("research", "explain"): {"research", "decisioncraft", "taste-elegance", "project-handoff", "articlecraft"},
            ("creative", "share"): {"project-handoff", "good-teammate", "idea-talks", "stories"},
        }
        for (flow, stage), expected in examples.items():
            actual = {ident for ident, assigned in self.flows["stage_memberships"].items() if stage in assigned.get(flow, [])}
            with self.subTest(flow=flow, stage=stage):
                self.assertEqual(expected, actual)

    def test_private_urls_future_reviews_and_unsupported_relationships_rejected(self):
        for changed in [
            {"url": "file:///private/notes.md"},
            {"url": "https://user:secret@example.invalid/source"},
            {"url": "https://localhost/private"},
            {"url": "https://localhost.:443/private"},
            {"url": "https://service.localhost/private"},
            {"url": "https://laptop.local/private"},
            {"url": "https://127.0.0.1/private"},
            {"url": "https://10.0.0.2/private"},
            {"url": "https://169.254.169.254/private"},
            {"url": "https://[::1]/private"},
            {"url": "https://[fd00::1]/private"},
            {"reviewed_date": "2099-01-01"},
            {"relationship": "partner"},
            {"pricing_url": "https://example.invalid/pricing"},
            {"source_urls": ["http://example.invalid/unsupported"]},
        ]:
            with self.subTest(fields=list(changed)):
                data = copy.deepcopy(self.related)
                data["capabilities"]["knowledge"][0].update(changed)
                with self.assertRaises(ValueError):
                    self.load("related-tools.json", data, load_related_tools)

    def test_duplicate_source_and_unknown_capability_rejected(self):
        data = copy.deepcopy(self.related)
        data["capabilities"]["knowledge"].append(copy.deepcopy(data["capabilities"]["knowledge"][0]))
        with self.assertRaises(ValueError):
            self.load("related-tools.json", data, load_related_tools)
        data = copy.deepcopy(self.related)
        data["capabilities"]["unreleased"] = data["capabilities"].pop("knowledge")
        with self.assertRaises(ValueError):
            self.load("related-tools.json", data, load_related_tools)

    def test_four_source_groups_escape_text_and_show_review_dates(self):
        entries = load_related_tools(ROOT, [x["id"] for x in self.projects])
        entries["knowledge"][0]["title"] = '<script>alert("no")</script>'
        html = render_related_tools("knowledge", entries)
        self.assertEqual(4, html.count('<details class="community-group">'))
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertEqual(18, html.count('<time datetime='))
        self.assertIn("not yet published", render_related_tools("not-curated", {}))

    def test_single_source_group_uses_singular_label(self):
        entry = self.related["capabilities"]["knowledge"][0]
        html = render_related_tools("knowledge", {"knowledge": [entry]})
        self.assertIn("1 source</span>", html)
        self.assertNotIn("1 sources", html)


if __name__ == "__main__":
    unittest.main()
