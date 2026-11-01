"""Three overlapping work filters over one public capability catalogue."""
import json
from html import escape

E = lambda value: escape(str(value), quote=True)
FLOW_ORDER = ["software", "research", "creative"]


def load_flows(root, projects):
    data = json.loads((root / "content/flows.json").read_text())
    if data.get("schema_version") != "capability-flows/v1":
        raise ValueError("Unsupported flow schema")
    flows = data["flows"]
    if [flow["id"] for flow in flows] != FLOW_ORDER:
        raise ValueError("The work guide must contain the three reviewed flows")
    memberships = data["memberships"]
    if set(memberships) != {project["id"] for project in projects}:
        raise ValueError("Flow memberships must match the public catalogue exactly")
    for ident, tags in memberships.items():
        if not tags or len(set(tags)) != len(tags) or not set(tags) <= set(FLOW_ORDER):
            raise ValueError(f"Invalid flow membership: {ident}")
    return data


def flow_links(project, data):
    by_id = {flow["id"]: flow for flow in data["flows"]}
    return '<ul class="flow-tags" aria-label="Kinds of work">' + "".join(
        f'<li><a href="/#flow-{E(ident)}">{E(by_id[ident]["title"])}</a></li>'
        for ident in data["memberships"][project["id"]]
    ) + '</ul>'


def flow_guide(data, projects, poster, stages):
    buttons = ''.join(
        f'<button type="button" data-flow-filter="{E(flow["id"])}" aria-pressed="false" aria-controls="flow-results"><strong>{E(flow["title"])}</strong><span>{E(flow["description"])}</span></button>'
        for flow in data["flows"]
    )
    cards = ''.join(
        f'<article class="flow-capability" data-flow-project="{E(project["id"])}" data-flows="{E(" ".join(data["memberships"][project["id"]]))}" data-category="{E(project["category"])}"><a class="flow-art" href="/capabilities/{E(project["id"])}/">{poster(project)}</a><div><h3><a href="/capabilities/{E(project["id"])}/">{E(project["title"])}</a></h3><p>{E(project["summary"])}</p>{flow_links(project,data)}</div></article>'
        for project in projects
    )
    # Old homepage category fragments still resolve to this single shared view.
    anchors = ''.join(f'<span id="stage-{E(stage["id"])}" data-legacy-category="{E(stage["id"])}" data-category-title="{E(stage["title"])}"></span>' for stage in stages)
    anchors += ''.join(f'<span id="flow-{E(flow["id"])}"></span>' for flow in data["flows"])
    return f'''<section class="work-flows wrap" id="journey" data-work-flows>{anchors}<div class="flow-intro"><h2>What would you like to do?</h2><p>Choose a kind of work, then open a capability. Some belong in more than one flow; none requires following a fixed sequence.</p></div><div class="flow-choices" aria-label="Choose a kind of work">{buttons}</div><div class="flow-result-line"><p data-flow-status role="status" aria-live="polite">All {len(projects)} capabilities</p><button class="text-button" data-flow-all type="button">Show all capabilities</button></div><noscript><p class="notice">All capabilities are listed below. Flow filtering is available with JavaScript enabled.</p></noscript><div class="flow-results" id="flow-results">{cards}</div></section>'''
