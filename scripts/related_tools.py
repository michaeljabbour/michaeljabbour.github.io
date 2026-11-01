"""Render explicitly reviewed public comparisons, separate from private research."""
import json
import ipaddress
from datetime import date
from html import escape
from urllib.parse import urlsplit

E = lambda value: escape(str(value), quote=True)
CATEGORIES = {"skill-or-plugin": "Skills & plugins", "open-source": "Open source", "research": "Research & guidance", "commercial": "Commercial tools"}
RELATIONSHIPS = {"alternative": "Alternative", "complement": "Complement", "inspiration": "Inspiration", "actual-code-reuse": "Code reused"}
FIELDS = {"title", "url", "relevance", "difference", "reviewed_date", "category", "relationship"}
OPTIONAL = {"pricing_url", "pricing_model", "source_urls"}


def public_https(value):
    if not isinstance(value, str):
        return False
    try:
        url = urlsplit(value)
        host = (url.hostname or "").lower().rstrip(".")
        url.port  # Reject malformed ports without resolving or connecting.
    except ValueError:
        return False
    if url.scheme != "https" or not host or url.username or url.password:
        return False
    if host == "localhost" or host.endswith((".localhost", ".local")):
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return True  # Domain ownership/relevance is curated; no DNS lookup here.
    return address.is_global and not address.is_multicast


def load_related_tools(root, project_ids):
    data = json.loads((root / "content/related-tools.json").read_text())
    if data.get("schema_version") != "capability-related-tools/v1":
        raise ValueError("Unsupported related tools schema")
    capabilities = data.get("capabilities", {})
    if not isinstance(capabilities, dict) or not set(capabilities) <= set(project_ids):
        raise ValueError("Related tools must reference a public capability")
    for ident, entries in capabilities.items():
        seen = set()
        if not isinstance(entries, list):
            raise ValueError(f"Expected related entries: {ident}")
        for entry in entries:
            if not isinstance(entry, dict) or not FIELDS <= set(entry) or not set(entry) <= FIELDS | OPTIONAL:
                raise ValueError(f"Invalid related tool fields: {ident}")
            if any(not isinstance(entry[key], str) or not entry[key].strip() for key in FIELDS):
                raise ValueError(f"Empty related tool field: {ident}")
            url = urlsplit(entry["url"])
            if not public_https(entry["url"]) or entry["url"] in seen:
                raise ValueError(f"Expected unique public HTTPS source: {ident}")
            seen.add(entry["url"])
            if entry["category"] not in CATEGORIES or entry["relationship"] not in RELATIONSHIPS:
                raise ValueError(f"Invalid related tool classification: {ident}")
            reviewed = date.fromisoformat(entry["reviewed_date"])
            if reviewed > date.today():
                raise ValueError(f"Related source review cannot be future-dated: {ident}")
            if ("pricing_url" in entry) != ("pricing_model" in entry):
                raise ValueError(f"Pricing requires both a model and source URL: {ident}")
            if "pricing_url" in entry and (entry["category"] != "commercial" or not public_https(entry["pricing_url"]) or not isinstance(entry["pricing_model"], str) or not entry["pricing_model"].strip()):
                raise ValueError(f"Invalid commercial pricing source: {ident}")
            sources = entry.get("source_urls", [])
            if not isinstance(sources, list) or len(sources) != len(set(sources)) or not all(public_https(source) for source in sources):
                raise ValueError(f"Invalid supporting source URLs: {ident}")
    return capabilities


def render_related_tools(ident, curated):
    entries = curated.get(ident, [])
    content = '<p class="related-empty">A reviewed comparison list is not yet published for this capability.</p>'
    if entries:
        def supporting(entry):
            pricing = f'<p class="community-pricing">{E(entry["pricing_model"])} <a href="{E(entry["pricing_url"])}">Pricing and plans</a></p>' if "pricing_url" in entry else ""
            links = ''.join(f'<li><a href="{E(url)}">Supporting source {n + 1}</a></li>' for n, url in enumerate(entry.get("source_urls", [])))
            return pricing + ('<ul class="community-sources" aria-label="Supporting sources">' + links + '</ul>' if links else '')
        def render_entries(items):
            return '<div class="community-list">' + ''.join(
            f'<article><div class="community-meta"><span>{E(CATEGORIES[entry["category"]])}</span><span>{E(RELATIONSHIPS[entry["relationship"]])}</span></div><h3><a href="{E(entry["url"])}">{E(entry["title"])}</a></h3><p>{E(entry["relevance"])}</p><p><strong>Difference:</strong> {E(entry["difference"])}</p>{supporting(entry)}<p class="reviewed-date">Reviewed <time datetime="{E(entry["reviewed_date"])}">{E(entry["reviewed_date"])}</time></p></article>'
            for entry in items
            ) + '</div>'
        content = ''.join(
            f'<details class="community-group"><summary>{E(label)} <span>{len([entry for entry in entries if entry["category"] == category])} sources</span></summary>{render_entries([entry for entry in entries if entry["category"] == category])}</details>'
            for category, label in CATEGORIES.items() if any(entry["category"] == category for entry in entries)
        )
    return '<section class="community-research wrap" aria-labelledby="community-title"><h2 id="community-title">Related tools &amp; research</h2><p class="community-intro">Sources to compare or explore alongside this capability. A listing does not imply an integration, partnership or endorsement.</p>' + content + '</section>'
