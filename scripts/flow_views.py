'''Three work flows, optional stages and one shared public catalogue.'''
import json
from html import escape

E = lambda value: escape(str(value), quote=True)
FLOW_ORDER = ['software', 'research', 'creative']
STAGE_ORDER = {
    'software': ['explore', 'plan', 'build', 'test', 'release', 'maintain'],
    'research': ['explore', 'gather', 'check', 'connect', 'explain', 'revisit'],
    'creative': ['explore', 'shape', 'make', 'review', 'package', 'share'],
}


def load_flows(root, projects):
    data = json.loads((root / 'content/flows.json').read_text())
    if set(data) != {'schema_version','flows','memberships','stage_memberships'} or data.get('schema_version') != 'capability-flows/v2':
        raise ValueError('Unsupported flow/stage schema')
    flows = data['flows']
    if [flow['id'] for flow in flows] != FLOW_ORDER:
        raise ValueError('The guide must contain the three reviewed flows')
    for flow in flows:
        if set(flow) != {'id','title','description','stages'} or any(set(stage) != {'id','title'} for stage in flow['stages']):
            raise ValueError('Unknown flow or stage fields must not enter public data')
        if [stage['id'] for stage in flow['stages']] != STAGE_ORDER[flow['id']]:
            raise ValueError('Flow stages must retain their reviewed optional navigation order')
        if any(not isinstance(stage.get('title'), str) or not stage['title'].strip() for stage in flow['stages']):
            raise ValueError('Stage labels must be visible text')
    memberships = data['memberships']
    stage_memberships = data['stage_memberships']
    ids = {project['id'] for project in projects}
    if set(memberships) != ids or set(stage_memberships) != ids:
        raise ValueError('Flow and stage memberships must match the public catalogue exactly')
    for ident, tags in memberships.items():
        if not isinstance(tags,list) or not tags or len(set(tags)) != len(tags) or not set(tags) <= set(FLOW_ORDER):
            raise ValueError('Invalid flow membership: ' + ident)
        assigned = stage_memberships[ident]
        if set(assigned) != set(tags):
            raise ValueError('Stages must be assigned only within the capability flow tags: ' + ident)
        for flow, stages in assigned.items():
            if not isinstance(stages,list) or not stages or len(stages) != len(set(stages)) or not set(stages) <= set(STAGE_ORDER[flow]):
                raise ValueError('Invalid stage membership: ' + ident)
    return data


def stage_tokens(project, data):
    assigned = data['stage_memberships'][project['id']]
    return ' '.join(flow + ':' + stage for flow in data['memberships'][project['id']] for stage in assigned[flow])


def search_text(project, category_titles):
    return ' '.join([project['title'], project['summary'], project['audience'], category_titles.get(project['category'], project['category']), project['format']]).lower()


def flow_links(project, data):
    by_id = {flow['id']: flow for flow in data['flows']}
    return '<ul class="flow-tags" aria-label="Kinds of work">' + ''.join(
        f'<li><a href="/#flow-{E(ident)}">{E(by_id[ident]["title"])}</a></li>'
        for ident in data['memberships'][project['id']]
    ) + '</ul>'


def stage_chooser(data, target):
    rows = []
    for flow in data['flows']:
        buttons = f'<button class="stage-all" type="button" data-stage-filter="all" data-stage-flow="{E(flow["id"])}" aria-pressed="false" aria-controls="{E(target)}">All stages</button>'
        buttons += ''.join(f'<button class="stage-choice" type="button" data-stage-filter="{E(stage["id"])}" data-stage-flow="{E(flow["id"])}" aria-pressed="false" aria-controls="{E(target)}">{E(stage["title"])}</button>' for stage in flow['stages'])
        rows.append(f'<div class="stage-row" data-stage-row="{E(flow["id"])}" role="group" aria-label="Stages for {E(flow["title"])}" hidden><div class="stage-track">{buttons}</div></div>')
    return '<div class="stage-filter" data-stage-group hidden><p>Filter by a stage. Start anywhere; these are optional ways to browse.</p>' + ''.join(rows) + '</div><input type="hidden" name="stage" value="all">'


def flow_guide(data, projects, poster, stages):
    buttons = ''.join(f'<button type="button" data-flow-filter="{E(flow["id"])}" aria-pressed="false" aria-controls="flow-results"><strong>{E(flow["title"])}</strong><span>{E(flow["description"])}</span></button>' for flow in data['flows'])
    categories = {stage['id']: stage['title'] for stage in stages}
    cards = ''.join(
        f'<article class="flow-capability" data-capability-id="{E(project["id"])}" data-flow-project="{E(project["id"])}" data-flows="{E(" ".join(data["memberships"][project["id"]]))}" data-stage-memberships="{E(stage_tokens(project,data))}" data-category="{E(project["category"])}" data-format="{E(project["format"])}" data-search="{E(search_text(project,categories))}"><a class="flow-art" href="/capabilities/{E(project["id"])}/">{poster(project)}</a><div><h3><a href="/capabilities/{E(project["id"])}/">{E(project["title"])}</a></h3><p>{E(project["summary"])}</p>{flow_links(project,data)}</div></article>'
        for project in projects
    )
    anchors = ''.join(f'<span id="stage-{E(stage["id"])}" data-legacy-category="{E(stage["id"])}" data-category-title="{E(stage["title"])}"></span>' for stage in stages)
    anchors += ''.join(f'<span id="flow-{E(flow["id"])}"></span>' for flow in data['flows'])
    return f'''<section class="work-flows wrap" id="journey" data-work-flows data-capability-browser>{anchors}<div class="flow-intro"><h2>What would you like to do?</h2><p>Choose a kind of work, then a stage to narrow the capabilities below. A capability can help in more than one place.</p></div><form class="flow-browser-controls" role="search" action="/#journey"><div class="flow-choices" aria-label="Choose a kind of work">{buttons}</div><input type="hidden" name="flow" value="all"><input type="hidden" name="category" value="all">{stage_chooser(data,'flow-results')}<div class="flow-search"><label for="home-capability-search">Find a capability</label><input id="home-capability-search" type="search" name="q" placeholder="Search names or tasks" autocomplete="off"></div></form><div class="flow-result-line"><p data-filter-status role="status" aria-live="polite">All {len(projects)} capabilities</p><button class="text-button" data-filter-clear type="button" hidden>Clear search and filters</button></div><noscript><p class="notice">All capabilities are listed below. Filtering is available with JavaScript enabled.</p></noscript><div class="flow-results" id="flow-results">{cards}</div><div class="empty-state" data-filter-empty hidden><h3>No matching capability.</h3><p>Try another word or stage, or show everything in the selected flow.</p><button type="button" class="button primary" data-reset-scope>Show all in this flow</button></div></section>'''
