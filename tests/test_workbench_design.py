"""The workbench theme keeps truthful counts, readable text and real media."""
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from flow_views import flow_guide, load_flows


def luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in channels]
    return sum(x * weight for x, weight in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + .05) / (low + .05)


class WorkbenchDesign(unittest.TestCase):
    def test_text_color_pairs_meet_aa(self):
        css = (ROOT / 'assets/site.css').read_text()
        tokens = dict(re.findall(r'--([\w-]+):\s*(#[0-9a-f]{6})\b', css))
        for foreground in ['ink', 'muted', 'accent']:
            for background in ['paper', 'white', 'wash', 'grid']:
                with self.subTest(foreground=foreground, background=background):
                    self.assertGreaterEqual(contrast(tokens[foreground], tokens[background]), 4.5)
        for background in ['ink', 'accent']:
            self.assertGreaterEqual(contrast(tokens['white'], tokens[background]), 4.5)

    def test_flow_counts_match_membership_not_total_catalogue(self):
        catalogue = json.loads((ROOT / 'content/portfolio.json').read_text())
        projects = catalogue['projects']
        data = load_flows(ROOT, projects)
        stages = json.loads((ROOT / 'content/journey.json').read_text())['stages']
        html = flow_guide(data, projects, lambda project: '', stages)
        for flow in data['flows']:
            expected = sum(flow['id'] in data['memberships'][p['id']] for p in projects)
            button = re.search(r'<button[^>]+data-flow-filter="' + flow['id'] + r'"[^>]*>(.*?)</button>', html).group(1)
            self.assertIn(f'{expected} capabilities', button)
            self.assertIn(f'<strong>{flow["title"].replace("&", "&amp;")}</strong>', button)
        self.assertEqual(len(projects), len(re.findall(r'<article class="flow-capability"', html)))

    def test_workbench_does_not_require_external_resources(self):
        css = (ROOT / 'assets/site.css').read_text()
        self.assertNotIn('@import', css)
        self.assertNotIn('@font-face', css)
        self.assertIn('prefers-reduced-motion: reduce', css)
        self.assertIn('.flow-capability h3 { font-size: 22px; letter-spacing: -.01em;', css)
        # Native media, captions and poster source remain owned by the existing manifest.
        build = (ROOT / 'scripts/build.py').read_text()
        self.assertIn('<video controls playsinline preload="none"', build)
        self.assertIn('<track kind="captions"', build)
        self.assertIn('.hero-story video { border-radius: 2px; border:', css)
        self.assertNotRegex(css, r'\.hero-story video\s*\{[^}]*outline:')


if __name__ == '__main__':
    unittest.main()
