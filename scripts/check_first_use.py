#!/usr/bin/env python3
"""Check visitor essentials and reading order in the built capability pages.

This verifies presentation and source fidelity, not runtime acceptance or usefulness.
"""
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELS = ['Research & evidence', 'Decisions & planning', 'Software & automation',
          'Review & testing', 'Images, videos & demos', 'Migration & deployment',
          'Memory & handoff']

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = {}
        self.position = 0
        self.labels = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.position += 1
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate id: ' + attrs['id'])
            self.ids[attrs['id']] = self.position
        if tag == 'nav':
            self.labels.append(attrs.get('aria-label'))

def validate(root=ROOT):
    data = json.loads((root/'content/portfolio.json').read_text())
    projects = data['projects']
    failures = []
    def require(ok, message):
        if not ok:
            failures.append(message)
    require(len(projects) == 33, 'Expected the approved 33-capability catalog')
    require([c['title'] for c in data['categories']] == LABELS, 'Category labels differ from visitor brief')
    for project in projects:
        ident = project['id']
        body = (root/'dist/capabilities'/ident/'index.html').read_text()
        page = Page()
        page.feed(body)
        for key in ['audience', 'input', 'action', 'result', 'runtime', 'first_prompt']:
            value = project.get(key)
            require(isinstance(value, str) and bool(value.strip()), ident+': missing '+key)
            if isinstance(value, str):
                require(value in unescape(body), ident+': rendered '+key+' differs from catalog')
        requirements = project.get('prerequisites')
        require(isinstance(requirements, list) and bool(requirements)
                and all(isinstance(p,str) and bool(p.strip()) for p in requirements),
                ident+': prerequisites must be a nonempty list')
        for anchor in ['setup','first-task','watch']:
            require(anchor in page.ids, ident+': missing '+anchor)
        if all(k in page.ids for k in ['setup','first-task','watch']):
            require(page.ids['setup'] < page.ids['watch'] and page.ids['first-task'] < page.ids['watch'],
                    ident+': setup and actual first task must precede video')
        require('Fictional illustration, not a result from your task or measured user evidence.' in body,
                ident+': example and task must be distinguished')
        require('>Limitations</h2>' in body and '>Runtime and prerequisites</h3>' in body,
                ident+': limits and prerequisites need separate headings')
        require('fictional' not in project['first_prompt'].lower(),
                ident+': first task must use real selected input, not a fictional walkthrough')
        if project['format'] in {'Tool','Library'}:
            require(not project['first_prompt'].startswith('Use '), ident+': preserve native operating instructions')
        require(page.labels.count('Main navigation') == 1, ident+': exactly one main navigation required')
    home = (root/'dist/index.html').read_text()
    require('AI tools for research, software, and creative work.' in unescape(home), 'Missing direct hero')
    require('data-category-launcher' not in home, 'Duplicate category launcher must remain absent')
    require(not any(p['id'] in {'articlecraft','idea-talks','stories'} for p in projects), 'Staged additions are not public')
    return {'status':'failed' if failures else 'passed','capabilities':len(projects),'errors':failures,
            'scope':'Rendered presentation/source fidelity only; no native, host, provider or human-outcome claim.'}

if __name__ == '__main__':
    result = validate()
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if result['errors'] else 0)
