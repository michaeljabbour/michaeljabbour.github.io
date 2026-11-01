"""Build public-only category and knowledge-journey pages with a legacy blog redirect."""
from html import escape
import json,re
from pathlib import Path
from urllib.parse import urlsplit
E=lambda value:escape(str(value),quote=True)

def category_body(projects,stages):
    parts=['<section class="page-intro wrap"><a class="back-link" href="/capabilities/">All capabilities</a><h1>Browse seven<br>capability categories.</h1><p>Find the capabilities across research, planning, software, review, creative production, migration and project continuity. Each capability page explains input, output, setup and a first task.</p><div class="button-row"><a class="text-link" href="/#journey">Open the category guide</a><a class="text-link" href="/journey/knowledge/">Explore the proposed knowledge journey</a></div></section>']
    for stage in stages:
        members=[p for p in projects if p['category']==stage['id']]
        parts.append('<section class="category-group wrap" id="category-'+E(stage['id'])+'"><div class="section-heading"><div><h2>'+E(stage['title'])+'</h2><p>'+E(stage['question'])+'</p></div><a class="text-link" href="/#stage-'+E(stage['id'])+'">See this moment</a></div><div class="category-members">')
        for p in members:parts.append('<article data-category-capability="'+E(p['id'])+'"><h3><a href="/capabilities/'+E(p['id'])+'/">'+E(p['title'])+'</a></h3><p>'+E(p['summary'])+'</p><a href="/capabilities/'+E(p['id'])+'/">Guide and first step <span aria-hidden="true">↗</span></a></article>')
        parts.append('</div></section>')
    return ''.join(parts)

def knowledge_body(data,by_id):
    parts=['<section class="page-intro wrap"><a class="back-link" href="/#journey">The build journey</a><p class="publication-label">Proposed journey</p><h1>From knowledge curation<br>to creation.</h1><p>A way through knowledge curation and creation: explore, collect, connect, test, make, refine and share. This is a proposed way to navigate the existing capabilities, not a claim of an automated end-to-end pipeline.</p></section><nav class="wrap knowledge-links" aria-label="Proposed knowledge journey"><ol class="category-links">']
    for n,stage in enumerate(data['stages']):parts.append('<li><a href="#knowledge-'+E(stage['id'])+'"><span aria-hidden="true">'+str(n+1)+'</span>'+E(stage['title'])+'</a></li>')
    parts.append('</ol></nav>')
    for stage in data['stages']:
        parts.append('<section class="knowledge-stage wrap" id="knowledge-'+E(stage['id'])+'"><div><p class="publication-label">Proposed · '+E(stage['title'])+'</p><h2>'+E(stage['question'])+'</h2><p>'+E(stage['description'])+'</p><p class="knowledge-output"><strong>Something to carry forward</strong><br>'+E(stage['output'])+'</p></div><div><h3>Existing capabilities to explore</h3><ul>')
        for ident in stage['capability_ids']:
            p=by_id[ident];parts.append('<li><a href="/capabilities/'+E(ident)+'/">'+E(p['title'])+'</a><p>'+E(p['summary'])+'</p></li>')
        parts.append('</ul></div></section>')
    parts.append('<section class="journey-loop wrap"><p>Testing can send you back to a source. Refining can uncover a factual question. Keep the evidence with the work and choose deliberately what to share.</p><a class="text-link" href="/capabilities/categories/">Browse all capabilities</a></section>')
    return ''.join(parts)

def write_public_views(root,out,write,shell,projects,stages):
    ids={p['id'] for p in projects};by_id={p['id']:p for p in projects}
    knowledge=json.loads((root/'content/knowledge-journey.json').read_text())
    for stage in knowledge['stages']:
        if not set(stage['capability_ids'])<=ids:raise ValueError('Knowledge journey contains an unapproved capability')
    write('capabilities/categories',shell('Seven ways into the work','Browse the distinct public capabilities across seven task areas.',category_body(projects,stages),'capabilities','/capabilities/categories/'))
    write('journey/knowledge',shell('From curation to creation','A proposed journey through existing research, knowledge and creative capabilities.',knowledge_body(knowledge,by_id),'journey','/journey/knowledge/'))
    redirect='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Blog · Michael Jabbour</title><meta name="description" content="Writing and notes from Michael Jabbour."><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=https://www.michaeljabbour.com/"><link rel="canonical" href="https://www.michaeljabbour.com/"></head><body><main id="main"><h1>Blog</h1><p><a href="https://www.michaeljabbour.com/">Read Michael Jabbour’s blog</a>.</p></main></body></html>'
    write('reports/capabilities',redirect)
    (out/'repo-categories.html').write_text(shell('Seven ways into the work','Browse the public capabilities across seven task areas.',category_body(projects,stages),'capabilities','/repo-categories.html',extra_head='<meta name="robots" content="noindex">'))
