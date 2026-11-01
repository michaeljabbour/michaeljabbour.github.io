#!/usr/bin/env python3
"""Check the built public portfolio without making network calls."""

from __future__ import annotations

import json
import hashlib
import math
import re
import sys
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit
from build import checked_compatibility_sites
from public_privacy import reviewed_example_text
from flow_views import load_flows
from related_tools import load_related_tools
from catalogue_admission import HISTORICAL_IDS, ADDITIONAL_IDS, current_admission

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
ORIGIN = "https://michaeljabbour.github.io"
FORMATS = {"Skill", "Smart tool", "Library", "Tool"}
STAGE_ORDER = [
    "understand",
    "choose",
    "build",
    "improve",
    "create",
    "adapt",
    "continue",
]
CHAPTER_OPENINGS = {
    "understand": "You find the question nobody asked.",
    "choose": "You decide who it’s for, and what shape it should take.",
    "build": "Then you build it, and you check what it can do, and where it has to stop.",
    "improve": "You make it easier to use.",
    "create": "You show it in pictures, in film, and in the product itself.",
    "continue": "And you keep the record, so the next person has somewhere to start.",
}
FIELDS = {
    "id",
    "title",
    "summary",
    "description",
    "audience",
    "category",
    "format",
    "repo_url",
    "site_url",
    "install_url",
    "first_prompt",
    "output",
    "limitations",
    "related",
}


class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.elements: list[tuple[str, dict[str, str | None]]] = []
        self.ids: list[str] = []
        self.title = ""
        self._title = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.elements.append((tag, attributes))
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "title":
            self._title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False

    def handle_data(self, value):
        if self._title:
            self.title += value

    def select(self, tag, **attributes):
        return [
            a
            for t, a in self.elements
            if t == tag and all(a.get(k) == v for k, v in attributes.items())
        ]


class JourneyMarkup(HTMLParser):
    """Keep ancestry and readable text for guide-to-stage membership checks."""

    VOID = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = {
            "tag": tag,
            "attrs": dict(attrs),
            "parents": tuple(self.stack),
            "text": "",
        }
        self.nodes.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break

    def handle_data(self, value):
        for node in self.stack:
            node["text"] += value

    def descendants(self, parent, attribute):
        return [
            node
            for node in self.nodes
            if attribute in node["attrs"]
            and any(ancestor is parent for ancestor in node["parents"])
        ]


def canonical_navigation_errors(catalogue, media, migration):
    """Reject legacy or off-repository navigation without rewriting asset URLs."""
    errors = []
    projects = catalogue.get("projects", [])
    rows = migration.get("repositories", [])
    ids = [project.get("id") for project in projects]
    row_ids = [row.get("id") for row in rows]
    if (
        migration.get("schema_version") != "amplifier-repository-migration/v1"
        or len(row_ids) != len(set(row_ids))
        or set(row_ids) != HISTORICAL_IDS
        or not HISTORICAL_IDS <= set(ids)
        or not set(ids) <= HISTORICAL_IDS | ADDITIONAL_IDS
    ):
        errors.append("Canonical migration map must cover each public capability exactly once")
    by_id = {row.get("id"): row for row in rows}
    films = media.get("films", {})
    for project in projects:
        ident = project.get("id", "<missing>")
        row = by_id.get(ident)
        if row is None:
            if ident in ADDITIONAL_IDS:
                expected_repo = "https://github.com/michaeljabbour/amplifier-capability-" + ident
                if project.get("repo_url") != expected_repo or project.get("site_url") != ORIGIN + "/capabilities/" + ident + "/" or project.get("install_url") != expected_repo + "#setup":
                    errors.append(f"{ident}: new capability must use its canonical repository, main-site guide and actual README setup anchor")
            continue
        repository = row.get("new_repository", "")
        repo_url = "https://github.com/michaeljabbour/" + repository
        site_url = ORIGIN + "/" + repository + "/"
        if (
            not re.fullmatch(r"amplifier-capability-[a-z0-9]+(?:-[a-z0-9]+)*", repository)
            or row.get("new_url") != repo_url
            or row.get("new_pages_url") != site_url
        ):
            errors.append(f"{ident}: canonical migration destination is invalid")
            continue
        for field, expected in (("repo_url", repo_url), ("site_url", site_url)):
            if project.get(field) != expected:
                errors.append(f"{ident}: {field} must use its canonical migration destination")
        install = urlsplit(project.get("install_url", ""))
        if (
            install.fragment not in {"install", "use-skill"}
            or install._replace(fragment="").geturl() != site_url
        ):
            errors.append(f"{ident}: install_url must use its canonical guide and documented fragment")
        film = urlsplit(films.get(ident, {}).get("film_url", ""))
        if not film.fragment or film._replace(fragment="").geturl() != site_url:
            errors.append(f"{ident}: film_url must use its canonical guide and film fragment")
    return errors


def main() -> int:
    errors: list[str] = []
    checked_links: set[tuple[str, str]] = set()
    checked_assets: set[str] = set()
    legacy_template_notes: list[str] = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def load_json(path):
        try:
            return json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Cannot read {path.relative_to(ROOT)}: {type(exc).__name__}")
            return {}

    catalogue = load_json(ROOT / "content/portfolio.json")
    media = load_json(ROOT / "content/media.json")
    journey = load_json(ROOT / "content/journey.json")
    migration_source = load_json(ROOT / "content/migration/mapping.json")
    errors.extend(canonical_navigation_errors(catalogue, media, migration_source))
    try:
        admission = current_admission(ROOT, catalogue, migration_source)
        served_admission = load_json(OUT / "publication.json")
        require(served_admission.get("preview_only") is admission["preview_only"] and served_admission.get("publication_ready") is admission["publication_ready"] and served_admission.get("additional_sources") == admission["additions"] and served_admission.get("capability_ids") == admission["capability_ids"], "Built publication admission differs from reviewed inputs")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors.append("Invalid catalogue admission: " + str(exc))
    projects = catalogue.get("projects", [])
    categories = catalogue.get("categories", [])
    ids = [p.get("id") for p in projects]
    category_ids = [c.get("id") for c in categories]
    require(
        len(ids) == len(set(ids)) and HISTORICAL_IDS <= set(ids) and set(ids) <= HISTORICAL_IDS | ADDITIONAL_IDS,
        "Catalogue must retain the historical identities and only the named admitted additions",
    )
    require(
        "basic-learning" not in ids,
        "Private learning experiment is excluded from the public catalogue",
    )
    require(
        len(category_ids) == len(set(category_ids)) == 7,
        "Seven unique work categories are required",
    )
    require(
        category_ids == STAGE_ORDER,
        "Catalogue category order must match the journey order",
    )
    for project in projects:
        ident = project.get("id", "<missing>")
        require(FIELDS <= set(project), f"{ident}: required catalogue field missing")
        for key in FIELDS - {"related"}:
            require(
                isinstance(project.get(key), str)
                and bool(project.get(key, "").strip()),
                f"{ident}: {key} must be nonempty text",
            )
        require(
            project.get("category") in category_ids, f"{ident}: unknown work category"
        )
        require(project.get("format") in FORMATS, f"{ident}: unknown format")
        related = project.get("related", [])
        require(
            isinstance(related, list)
            and bool(related)
            and len(related) == len(set(related)),
            f"{ident}: related IDs must be a nonempty unique list",
        )
        require(
            all(r in ids and r != ident for r in related),
            f"{ident}: related capability is unknown or self-referential",
        )
        for key in ("repo_url", "site_url", "install_url"):
            url = urlsplit(project.get(key, ""))
            require(
                url.scheme == "https" and bool(url.netloc),
                f"{ident}: {key} must use an absolute HTTPS URL",
            )
        install = urlsplit(project.get("install_url", ""))
        site = urlsplit(project.get("site_url", ""))
        require(
            install.fragment in {"install", "use-skill"}
            and install._replace(fragment="") == site,
            f"{ident}: installation destination must be the capability site's documented section",
        )
        if project.get("format") in {"Library", "Tool"}:
            require(
                not project.get("first_prompt", "").startswith("Use "),
                f"{ident}: a native mechanism needs first-use guidance, not an invented coaching invocation",
            )
        require(
            "fictional" in project.get("output", "").lower(),
            f"{ident}: sample output needs an explicit fictional label",
        )

    require(OUT.is_dir(), "Build dist before running the checker")
    legacy_paths = set()
    try:
        compatibility_sites = checked_compatibility_sites()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid compatibility source: {exc}")
        compatibility_sites = []
    legacy_entries = {}
    for prefix, _, expected in compatibility_sites:
        destination = OUT / prefix
        actual = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
        require(actual == set(expected), f"{prefix}: copied compatibility file list differs")
        require(
            not any(p.is_symlink() for p in [destination, *destination.rglob("*")]),
            f"{prefix}: copied compatibility symlink is forbidden",
        )
        for name, entry in expected.items():
            path = destination / name
            legacy_entries[path] = entry
            legacy_paths.add(path)
            require(
                path.is_file() and path.stat().st_size == entry["bytes"]
                and hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"],
                f"{prefix}/{name}: copied compatibility content differs",
            )
    html_files = sorted(OUT.rglob("*.html")) if OUT.exists() else []
    documents = {path: Document(path.read_text()) for path in html_files}
    overview_pages = int((OUT / "assets/overview/transcript/index.html").exists())
    require(
        len([p for p in html_files if p not in legacy_paths]) == len(ids) + 12 + overview_pages,
        "Build page count must match the admitted capability routes, shared routes, compatibility pages and configured overview transcript",
    )
    expected_routes = {
        OUT / "capabilities" / ident / "index.html"
        for ident in ids
        if isinstance(ident, str)
    }
    actual_routes = set((OUT / "capabilities").glob("*/index.html"))
    require(
        actual_routes == expected_routes | {OUT / "capabilities/categories/index.html"},
        "Built capability routes differ from the admitted catalogue IDs plus the category index",
    )

    def target_for(reference: str, origin: Path):
        parsed = urlsplit(reference)
        if parsed.scheme in {"mailto", "tel", "data"}:
            return None, None
        if parsed.scheme or parsed.netloc:
            return None, None
        raw_path = unquote(parsed.path)
        path = (
            OUT / raw_path.lstrip("/")
            if raw_path.startswith("/")
            else origin.parent / raw_path
        )
        if not raw_path:
            path = origin
        elif raw_path.endswith("/") or path.is_dir():
            path /= "index.html"
        path = path.resolve()
        if not path.is_relative_to(OUT.resolve()):
            errors.append(
                f"{origin.relative_to(OUT)}: local reference escapes the public output"
            )
            return None, None
        return path, unquote(parsed.fragment)

    def check_reference(reference: str, origin: Path, asset=False):
        parsed = urlsplit(reference)
        require(
            parsed.scheme.lower() not in {"javascript", "file"},
            f"{origin.relative_to(OUT)}: forbidden URL scheme",
        )
        target, fragment = target_for(reference, origin)
        if target is None:
            return
        checked_links.add((str(origin.relative_to(OUT)), reference))
        require(
            target.is_file(),
            f"{origin.relative_to(OUT)}: missing local destination {reference}",
        )
        if target.is_file() and fragment:
            require(
                target in documents and fragment in documents[target].ids,
                f"{origin.relative_to(OUT)}: missing fragment {reference}",
            )
        if asset:
            checked_assets.add(str(target.relative_to(OUT)))

    installer_index=OUT / "reports/capability-installer/index.html"
    for path, doc in documents.items():
        homepage_template=path not in legacy_paths
        relative = path.relative_to(OUT)
        raw = path.read_text()
        require(
            doc.title.strip() and (not homepage_template or "Michael Jabbour" in doc.title),
            f"{relative}: meaningful owner-attributed title required",
        )
        descriptions = doc.select("meta", name="description")
        require(
            not homepage_template or (len(descriptions) == 1 and bool(descriptions[0].get("content"))),
            f"{relative}: one nonempty description required",
        )
        canonical = doc.select("link", rel="canonical")
        route = (
            "/" + str(relative.parent).replace("\\", "/") + "/"
            if relative.parent != Path(".")
            else "/"
        )
        if path == OUT / "reports/capability-installer/index.html":
            route = "/reports/capability-installer/"
        if path.name == "repo-categories.html":
            route = "/repo-categories.html"
        if path.name == "404.html":
            route = "/"  # The error page intentionally points visitors back to the homepage.
        if homepage_template:
            require(
                len(canonical) == 1 and canonical[0].get("href") == ("https://www.michaeljabbour.com/" if path == OUT/"reports/capabilities/index.html" else ORIGIN + route),
                f"{relative}: canonical does not match its public route",
            )
        if path in legacy_paths and len(doc.select("h1")) != 1:
            legacy_template_notes.append(f"{relative}: preserved legacy example heading structure")
        else:
            require(len(doc.select("h1")) == 1, f"{relative}: exactly one page heading required")
        require(
            path in legacy_paths or (("main" in doc.ids or (not homepage_template and bool(doc.select("main")))) and bool(doc.select("html", lang="en"))),
            f"{relative}: language and main landmark required",
        )
        require(
            not [ident for ident, count in Counter(doc.ids).items() if count > 1],
            f"{relative}: duplicate element IDs",
        )
        for tag, attributes in doc.elements:
            for field in ("href", "src", "poster"):
                if attributes.get(field):
                    check_reference(
                        attributes[field],
                        path,
                        asset=field in {"src", "poster"} or tag in {"script", "link"},
                    )
            if (
                tag == "meta"
                and attributes.get("property") == "og:image"
                and attributes.get("content", "").startswith(ORIGIN + "/")
            ):
                check_reference(attributes["content"][len(ORIGIN) :], path, asset=True)
            elif (
                path in legacy_paths and tag == "meta"
                and attributes.get("property") == "og:image" and attributes.get("content")
            ):
                check_reference(attributes["content"], path, asset=True)
            if tag in {"video", "audio"}:
                require(
                    "autoplay" not in attributes,
                    f"{relative}: autoplay is not permitted",
                )
                require(
                    "controls" in attributes, f"{relative}: media needs native controls"
                )
            if tag == "img":
                require("alt" in attributes, f"{relative}: image alternative missing")
            if tag == "button" and path not in legacy_paths:
                require(
                    attributes.get("type") in {"button", "submit"},
                    f"{relative}: explicit button type required",
                )
            if tag == "label" and attributes.get("for"):
                require(
                    attributes["for"] in doc.ids,
                    f"{relative}: label targets a missing control",
                )
        require("@@" not in raw, f"{relative}: unresolved build token")

    home_navigation=documents.get(OUT/'index.html')
    if home_navigation:
        require(not any('data-category-launcher' in attrs for _,attrs in home_navigation.elements),'Homepage must not duplicate its inline journey with a top category launcher')
        require('Where are you starting?' not in (OUT/'index.html').read_text(),'Removed homepage launcher must not return')
        main_journey=home_navigation.select('a',**{'aria-label':'Work flows'})
        require(len(main_journey)==1 and main_journey[0].get('href')=='/#journey','Main Work flows navigation must target the inline homepage content')
    try:
        flow_data = load_flows(ROOT, projects)
        curated_related = load_related_tools(ROOT, ids)
        require(home_navigation is not None, "Missing homepage flow guide")
        if home_navigation:
            flow_rows = [attrs for _,attrs in home_navigation.elements if "data-flow-project" in attrs]
            require(len(flow_rows) == len(ids) and {row["data-flow-project"] for row in flow_rows} == set(ids), "Homepage must show one shared card per capability before JavaScript")
            require([attrs["data-flow-filter"] for _,attrs in home_navigation.elements if "data-flow-filter" in attrs] == ["software","research","creative"], "Homepage must have three named work flow choices")
            for row in flow_rows:
                require(row.get("data-flows", "").split() == flow_data["memberships"].get(row["data-flow-project"]), "Homepage flow tags differ from reviewed membership")
            require(set("stage-" + category for category in STAGE_ORDER) <= set(home_navigation.ids), "Legacy category anchors must remain available")
            require(not any("data-journey" in attrs for _,attrs in home_navigation.elements), "Homepage must not duplicate the flow guide with the old sequential journey")
        for ident in ids:
            detail_doc = documents.get(OUT / "capabilities" / ident / "index.html")
            require(detail_doc is not None and "community-title" in detail_doc.ids, f"{ident}: missing related tools and research section")
    except (OSError,ValueError,KeyError,TypeError) as exc:
        errors.append("Invalid work-flow or related-tools data: " + str(exc))
    library = documents.get(OUT / "capabilities/index.html")
    if library:
        rows = [
            a for tag, a in library.elements if tag == "article" and "data-project" in a
        ]
        require(
            len(rows) == len(ids),
            "Library must expose all catalogue project rows before JavaScript runs",
        )
        library_ids = set()
        for attributes in library.select("a"):
            match = re.fullmatch(
                r"/capabilities/([^/]+)/", urlsplit(attributes.get("href", "")).path
            )
            if match and match.group(1) != "categories":
                library_ids.add(match.group(1))
        require(
            library_ids == set(ids),
            "Library links do not cover exactly the catalogue capability routes",
        )
        for key in ("search", "category", "format", "result-count", "no-results"):
            require(
                key in library.ids,
                f"Library is missing the {key} filter/result control",
            )

    films = media.get("films", {})
    require(
        set(films) == set(ids),
        "Media catalogue must cover exactly the public project IDs",
    )
    media_players = captions = 0
    for project in projects:
        ident = project["id"]
        path = OUT / "capabilities" / ident / "index.html"
        doc = documents.get(path)
        metadata = films.get(ident, {})
        if not doc:
            continue
        links = {a.get("href") for a in doc.select("a")}
        require(
            project["repo_url"] in links
            and (ident in ADDITIONAL_IDS or project["site_url"] in links)
            and project["install_url"] in links,
            f"{ident}: source, guide and installation links are required",
        )
        require(
            "/#stage-" + project["category"] in links,
            f"{ident}: detail page needs its primary journey-stage destination",
        )
        require(
            "first-prompt" in doc.ids
            and project["first_prompt"] in unescape(path.read_text()),
            f"{ident}: reviewed first-use text must appear on the page",
        )
        copy_buttons = [
            a for a in doc.select("button") if a.get("data-copy") == "first-prompt"
        ]
        require(
            len(copy_buttons) == 1,
            f"{ident}: one copy action must target the first-use text",
        )
        if project.get("format") in {"Library", "Tool"}:
            require(
                "Copy starter prompt" not in path.read_text(),
                f"{ident}: native first-use guidance must not be labelled a starter prompt",
            )
        if metadata.get("available") and metadata.get("src"):
            players = doc.select("video")
            require(
                len(players) == 1,
                f"{ident}: available media needs exactly one video player",
            )
            require(
                any(a.get("src") == metadata["src"] for a in doc.select("source")),
                f"{ident}: video source differs from media.json",
            )
            expected_poster = (
                metadata.get("still")
                or metadata.get("local_poster")
                or metadata.get("poster")
                or ""
            )
            if expected_poster and not expected_poster.startswith("http"):
                expected_poster = "/" + expected_poster.lstrip("/")
            require(
                bool(players) and players[0].get("poster") == expected_poster,
                f"{ident}: player poster differs from media.json",
            )
            if metadata.get("caption"):
                require(
                    any(
                        a.get("src") == metadata["caption"]
                        and a.get("kind") == "captions"
                        and a.get("srclang") == "en"
                        for a in doc.select("track")
                    ),
                    f"{ident}: provided caption track must be exposed",
                )
                require(
                    bool(players) and players[0].get("crossorigin") == "anonymous",
                    f"{ident}: cross-origin captions need an explicit media CORS mode",
                )
                captions += 1
            for key in ("transcript", "cut", "film_url"):
                if metadata.get(key):
                    require(
                        metadata[key] in links,
                        f"{ident}: {key} destination differs from media.json",
                    )
            media_players += 1
        else:
            require(
                not doc.select("video"), f"{ident}: do not show an unavailable player"
            )

    # The overview is optional; only configured, supplied assets may create a home player.
    home = documents.get(OUT / "index.html")
    home_config_path = ROOT / "content/home-film.json"
    home_config = load_json(home_config_path) if home_config_path.exists() else {}
    home_players = len(home.select("video")) if home else 0
    if home_config.get("src"):

        def home_asset(value):
            if not isinstance(value, str) or not value.strip():
                return ""
            return value if value.startswith("https://") else "/" + value.lstrip("/")

        require(
            home_players == 1, "Configured overview needs exactly one homepage player"
        )
        for field in ("src", "poster", "caption"):
            value = home_config.get(field)
            require(
                isinstance(value, str) and bool(value.strip()),
                f"Overview: {field} is required",
            )
            if isinstance(value, str):
                parsed = urlsplit(value)
                require(
                    not parsed.scheme or parsed.scheme == "https",
                    f"Overview: {field} must be a local asset or stable HTTPS URL",
                )
                require(
                    ".." not in Path(parsed.path).parts,
                    f"Overview: {field} must stay within the public asset tree",
                )
        if home:
            players = home.select("video")
            require(
                any(
                    a.get("src") == home_asset(home_config.get("src"))
                    for a in home.select("source")
                ),
                "Overview video differs from home-film.json",
            )
            require(
                bool(players)
                and players[0].get("poster") == home_asset(home_config.get("poster")),
                "Overview poster differs from home-film.json",
            )
            require(
                any(
                    a.get("src") == home_asset(home_config.get("caption"))
                    and a.get("kind") == "captions"
                    and a.get("srclang") == "en"
                    for a in home.select("track")
                ),
                "Overview supplied captions must be exposed",
            )
            require(
                bool(players) and players[0].get("crossorigin") == "anonymous",
                "Overview cross-origin captions need an explicit media CORS mode",
            )
            if home_config.get("transcript"):
                require(
                    home_asset(home_config["transcript"])
                    in {a.get("href") for a in home.select("a")},
                    "Overview transcript differs from home-film.json",
                )
    else:
        require(
            home_players == 0,
            "No overview player may appear before a source is configured",
        )

    # A guide is a sequence of human questions, with every tool in its actual stage.
    stages = journey.get("stages", [])
    stage_ids = [stage.get("id") for stage in stages if isinstance(stage, dict)]
    require(
        stage_ids == STAGE_ORDER,
        "Journey stage order must keep visibility before adaptation and continuation last",
    )
    require(
        set(stage_ids) == set(category_ids),
        "Journey stages must cover exactly the seven catalogue categories",
    )
    require(
        all(
            isinstance(journey.get(key), str) and journey[key].strip()
            for key in ("title", "intro")
        ),
        "Journey needs a title and introduction",
    )
    by_stage = {stage.get("id"): stage for stage in stages if isinstance(stage, dict)}
    by_project = {project["id"]: project for project in projects}
    expected_chapters = {}
    for stage in stages:
        if not isinstance(stage, dict):
            errors.append("Journey stages must be objects")
            continue
        ident = stage.get("id", "<missing>")
        for field in ("title", "question", "description", "output", "reflection"):
            require(
                isinstance(stage.get(field), str)
                and len(stage.get(field, "").strip()) >= 8,
                f"{ident}: journey {field} needs meaningful text",
            )
        leads = stage.get("lead_ids", [])
        require(
            isinstance(leads, list) and bool(leads) and len(leads) == len(set(leads)),
            f"{ident}: recommended starting tools must be a unique nonempty list",
        )
        require(
            all(
                lead in by_project and by_project[lead]["category"] == ident
                for lead in leads
            ),
            f"{ident}: starting tool belongs to a different or unknown stage",
        )
        start = stage.get("film_start")
        if start is not None:
            valid = (
                type(start) in (int, float) and math.isfinite(start) and 0 < start < 90
            )
            require(
                valid,
                f"{ident}: story moment needs a positive time within the 90-second film",
            )
            if valid:
                expected_chapters[ident] = float(start)
    require(
        len(set(expected_chapters.values())) == len(expected_chapters),
        "Story chapters must not share one moment under different stages",
    )
    require(
        set(expected_chapters) == set(CHAPTER_OPENINGS),
        "Only the six narrated moments may have story chapters; adaptation has no narrated chapter",
    )
    require(
        by_stage.get("adapt", {}).get("film_start") is None,
        "Adaptation must not receive an invented film timestamp",
    )
    require(
        list(expected_chapters.values()) == sorted(expected_chapters.values()),
        "Spoken story chapters must follow the journey order",
    )
    captions_file = ROOT / "assets/overview/portfolio.vtt"
    if captions_file.exists():
        cue_starts = set()
        cue_texts = {}
        for stamp, text in re.findall(
            r"(?m)^(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->[^\n]*\n(.+?)(?=\n\s*\n|\Z)",
            captions_file.read_text(),
            flags=re.DOTALL,
        ):
            hour, minute, second = stamp.split(":")
            start = int(hour) * 3600 + int(minute) * 60 + float(second)
            cue_starts.add(start)
            cue_texts[start] = " ".join(text.split())
        for ident, start in expected_chapters.items():
            matching_cues = [cue for cue in cue_starts if abs(start - cue) < 0.05]
            require(
                bool(matching_cues),
                f"{ident}: story moment must bind to an actual overview-caption cue",
            )
            require(
                ident in CHAPTER_OPENINGS
                and any(
                    cue_texts[cue] == CHAPTER_OPENINGS.get(ident)
                    for cue in matching_cues
                ),
                f"{ident}: story moment must bind to its narrated meaning, not another valid cue",
            )
    else:
        require(
            not expected_chapters, "Story chapters need their actual caption source"
        )
    require(
        load_json(OUT / "journey.json") == journey,
        "Public journey differs from its reviewed source",
    )
    require(OUT / "journey/index.html" in documents, "Missing dedicated journey page")
    guides_checked = journey_tools_checked = chapter_links_checked = 0
    for guide_path in (OUT / "journey/index.html",):
        if guide_path not in documents:
            continue
        markup = JourneyMarkup(guide_path.read_text())
        guides = [node for node in markup.nodes if "data-journey" in node["attrs"]]
        require(
            len(guides) == 1,
            f"{guide_path.relative_to(OUT)}: exactly one complete journey guide is required",
        )
        for guide in guides:
            guides_checked += 1
            navs = markup.descendants(guide, "data-journey-nav")
            require(
                len(navs) == 1 and navs[0]["tag"] == "nav",
                f"{guide_path.relative_to(OUT)}: journey needs a navigation landmark",
            )
            links = markup.descendants(guide, "data-stage-link")
            panels = markup.descendants(guide, "data-stage-panel")
            require(
                [node["attrs"].get("data-stage-link") for node in links] == stage_ids,
                f"{guide_path.relative_to(OUT)}: stage navigation differs from journey order",
            )
            require(
                [node["attrs"].get("data-stage-panel") for node in panels] == stage_ids,
                f"{guide_path.relative_to(OUT)}: stage panels differ from journey order",
            )
            controls = markup.descendants(guide, "data-journey-controls")
            require(
                len(controls) == 1 and "hidden" in controls[0]["attrs"],
                f"{guide_path.relative_to(OUT)}: enhanced journey controls must wait for JavaScript",
            )
            if controls:
                for attribute in ("data-journey-previous", "data-journey-next"):
                    buttons = markup.descendants(controls[0], attribute)
                    require(
                        len(buttons) == 1
                        and buttons[0]["tag"] == "button"
                        and buttons[0]["attrs"].get("type") == "button"
                        and bool(buttons[0]["text"].strip()),
                        f"{guide_path.relative_to(OUT)}: journey needs a labeled {attribute} control",
                    )
            for node in links:
                attrs = node["attrs"]
                ident = attrs.get("data-stage-link")
                require(
                    node["tag"] == "a"
                    and attrs.get("id") == "step-" + str(ident)
                    and attrs.get("href") == "#stage-" + str(ident),
                    f"{guide_path.relative_to(OUT)}: stage link does not point to its panel",
                )
                require(
                    ident in by_stage
                    and by_stage[ident]["title"] in " ".join(node["text"].split()),
                    f"{guide_path.relative_to(OUT)}: stage navigation label differs from its stage",
                )
                require(
                    bool(navs) and any(parent is navs[0] for parent in node["parents"]),
                    f"{guide_path.relative_to(OUT)}: stage link is outside the journey navigation",
                )
            all_tools = markup.descendants(guide, "data-journey-tool")
            require(
                Counter(node["attrs"].get("data-journey-tool") for node in all_tools)
                == Counter(ids),
                f"{guide_path.relative_to(OUT)}: each catalogue capability must appear exactly once in the guide",
            )
            journey_tools_checked += len(all_tools)
            for panel in panels:
                ident = panel["attrs"].get("data-stage-panel")
                stage = by_stage.get(ident, {})
                require(
                    panel["tag"] == "section"
                    and panel["attrs"].get("id") == "stage-" + str(ident),
                    f"{guide_path.relative_to(OUT)}: stage panel needs the correct section anchor",
                )
                require(
                    "hidden" not in panel["attrs"]
                    and panel["attrs"].get("aria-hidden") != "true",
                    f"{guide_path.relative_to(OUT)}: {ident} must remain available without JavaScript",
                )
                heading_id = "question-" + str(ident)
                headings = [
                    node
                    for node in markup.nodes
                    if any(parent is panel for parent in node["parents"])
                    and node["attrs"].get("id") == heading_id
                ]
                require(
                    panel["attrs"].get("aria-labelledby") == heading_id
                    and len(headings) == 1
                    and headings[0]["tag"] in {"h2", "h3"}
                    and " ".join(headings[0]["text"].split())
                    == " ".join(stage.get("question", "").split()),
                    f"{guide_path.relative_to(OUT)}: {ident} must be labeled by its actual question heading",
                )
                text = " ".join(panel["text"].split())
                for field in ("question", "output"):
                    require(
                        " ".join(stage.get(field, "").split()) in text
                        and bool(stage.get(field)),
                        f"{guide_path.relative_to(OUT)}: {ident} must expose its human question and output",
                    )
                actual_tools = markup.descendants(panel, "data-journey-tool")
                expected_tools = {
                    project["id"]
                    for project in projects
                    if project["category"] == ident
                }
                require(
                    {node["attrs"].get("data-journey-tool") for node in actual_tools}
                    == expected_tools,
                    f"{guide_path.relative_to(OUT)}: {ident} tool membership differs from the catalogue",
                )
                for node in actual_tools:
                    tool_id = node["attrs"].get("data-journey-tool")
                    require(
                        node["tag"] == "a"
                        and node["attrs"].get("href")
                        == "/capabilities/" + str(tool_id) + "/",
                        f"{guide_path.relative_to(OUT)}: journey tool must open its matching capability",
                    )
                    tool_titles = [
                        child["text"].strip()
                        for child in markup.nodes
                        if child["tag"] == "strong"
                        and any(parent is node for parent in child["parents"])
                    ]
                    require(
                        tool_id in by_project
                        and tool_titles == [by_project.get(tool_id, {}).get("title")],
                        f"{guide_path.relative_to(OUT)}: journey tool label must name its actual capability",
                    )
            chapter_links = markup.descendants(guide, "data-story-moment")
            require(
                Counter(
                    node["attrs"].get("data-story-moment") for node in chapter_links
                )
                == Counter(expected_chapters.keys()),
                f"{guide_path.relative_to(OUT)}: spoken story moments must match the available chapters",
            )
            for node in chapter_links:
                attrs = node["attrs"]
                ident = attrs.get("data-story-moment")
                parsed = urlsplit(attrs.get("href", ""))
                try:
                    start = float(attrs.get("data-film-start", ""))
                except (TypeError, ValueError):
                    start = float("nan")
                require(
                    ident in expected_chapters
                    and math.isfinite(start)
                    and abs(start - expected_chapters.get(ident, -1)) < 0.001,
                    f"{guide_path.relative_to(OUT)}: {ident} chapter time differs from its stage",
                )
                require(
                    node["tag"] == "a"
                    and parsed.path == "/"
                    and parse_qs(parsed.query).get("moment") == [ident]
                    and parsed.fragment == "story",
                    f"{guide_path.relative_to(OUT)}: {ident} chapter link points to the wrong story destination",
                )
                visible_times = re.findall(r"\b(\d+):(\d{2})\b", node["text"])
                require(
                    len(visible_times) == 1
                    and ident in expected_chapters
                    and abs(
                        int(visible_times[0][0]) * 60
                        + int(visible_times[0][1])
                        - expected_chapters.get(ident, -100)
                    )
                    < 1,
                    f"{guide_path.relative_to(OUT)}: {ident} visible chapter time must match its destination",
                )
                chapter_links_checked += 1
    if expected_chapters:
        require(
            bool(home) and "story" in home.ids,
            "Chapter navigation needs the homepage story anchor",
        )

    # Check local CSS references too: an HTML-only walk misses missing background/font assets.
    for css in OUT.rglob("*.css"):
        for match in re.finditer(
            r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", css.read_text()
        ):
            check_reference(match.group(1).strip(), css, asset=True)

    public_text_files = [
        p
        for p in OUT.rglob("*")
        if p.is_file()
        and p.suffix.lower()
        in {".html", ".css", ".js", ".json", ".xml", ".txt", ".md", ".svg", ".csv", ".py"}
    ]
    private_markers = [
        "/Users/",
        "file://",
        "mj-public-repo-consolidation",
        "portfolio-evidence.html",
        "records/visibility",
        "records/retirements",
        "amplifier-bitcoin-devtools",
        "hip-flexor-fix-website",
    ]
    secret_patterns = {
        "GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b",
        "OpenAI-style key": r"\bsk-(?:proj-)?[A-Za-z0-9_-]{25,}\b",
        "AWS access key": r"\bAKIA[A-Z0-9]{16}\b",
        "private key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    }
    for path in public_text_files:
        raw = path.read_text()
        # Only original-byte/hash-bound public examples may be removed for this scan.
        private_text = raw
        if path in legacy_entries:
            try:
                private_text = reviewed_example_text(private_text, path.read_bytes(), legacy_entries[path])
            except ValueError:
                errors.append(f"{path.relative_to(OUT)}: public example review binding differs")
        for marker in private_markers:
            require(
                marker not in private_text,
                f"{path.relative_to(OUT)}: private-workspace or excluded-project marker found",
            )
        for label, pattern in secret_patterns.items():
            require(
                not re.search(pattern, raw),
                f"{path.relative_to(OUT)}: possible {label} found (value suppressed)",
            )
    category_doc = documents.get(OUT / "capabilities/categories/index.html")
    require(category_doc is not None, "Missing category index")
    if category_doc:
        category_ids = [attrs.get("data-category-capability") for _, attrs in category_doc.elements if attrs.get("data-category-capability")]
        require(len(category_ids) ==len(ids) and set(category_ids) ==set(ids), "Category index must keep all catalogue capabilities distinct")
    knowledge_doc = documents.get(OUT / "journey/knowledge/index.html")
    require(knowledge_doc is not None, "Missing proposed knowledge journey")
    if knowledge_doc:
        require(not any(attrs.get("data-film-start") for _, attrs in knowledge_doc.elements), "Proposed knowledge journey must not invent narrated timestamps")
    # Owner-facing readiness inputs and reports are deliberately private.
    for name in ['content/public-capability-status.json','content/public-capability-status.csv','content/public-status-scope.json']:
        require(not (ROOT/name).exists(),'Retired internal status input must stay outside public source')
    require(not (OUT/'reports/capabilities/status.json').exists() and not (OUT/'reports/capabilities/capability-status.csv').exists(),'Internal status downloads must not be published')
    for path in html_files:
        if path in legacy_paths:continue
        raw=path.read_text();doc=documents[path]
        for phrase in ['Built by Michael.','All 33 prepared source releases','current source builds/checks','Finite finding triage','ending-board revision planned','Published and playable does not mean final creative review']:
            require(phrase not in raw,f'{path.relative_to(OUT)}: internal presentation note must not return')
        if doc.select('nav',**{'aria-label':'Main navigation'}):
            blog=doc.select('a',**{'aria-label':'Blog'})
            require(len(blog)==1 and blog[0].get('href')=='https://www.michaeljabbour.com/',f'{path.relative_to(OUT)}: primary Blog link must be direct')
            require(not doc.select('a',**{'aria-label':'Status'}),f'{path.relative_to(OUT)}: internal Status navigation must not return')
    old_status=documents.get(OUT/'reports/capabilities/index.html')
    require(old_status is not None and old_status.select('meta',**{'http-equiv':'refresh'})==[{'http-equiv':'refresh','content':'0; url=https://www.michaeljabbour.com/'}],'Old status HTML route must be only the blog redirect/fallback')
    migration=load_json(OUT/'migration/mapping.json')
    require(migration==load_json(ROOT/'content/migration/mapping.json'),'Served migration map must match reviewed source')
    require(len(migration.get('repositories',[]))==33 and {row['id'] for row in migration.get('repositories',[])}==HISTORICAL_IDS,'Migration map must retain33 approved identities')
    require(OUT/'migration/index.html' in documents,'Migration guide missing')
    # The download is the reviewed package, with an exact build-time commit pin.
    try:
        import os,subprocess
        package=load_json(ROOT/'tools/PACKAGE.json');served=load_json(OUT/'reports/capability-installer/manifest.json')
        from installer_download import validate_download
        validate_download(ROOT,OUT,package,served)
    except (OSError,KeyError,TypeError,ValueError) as exc:
        errors.append('Invalid installer download: '+str(exc))
    public_catalogue = load_json(OUT / "portfolio.json")
    require(
        public_catalogue == catalogue,
        "Public catalogue differs from reviewed source content",
    )
    sitemap = OUT / "sitemap.xml"
    if sitemap.exists():
        sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text()))
        expected_urls = {
            ORIGIN + route
            for route in ["/", "/about/", "/capabilities/", "/films/", "/journey/", "/capabilities/categories/", "/journey/knowledge/", "/reports/capability-installer/", "/migration/"]
        } | {ORIGIN + "/capabilities/" + ident + "/" for ident in ids}
        require(
            sitemap_urls == expected_urls,
            "Sitemap must cover the42 public content routes exactly",
        )
    else:
        errors.append("Missing sitemap.xml")

    summary = {
        "status": "passed" if not errors else "failed",
        "pages": len(documents),
        "projects": len(projects),
        "categories": len(categories),
        "journey_guides": guides_checked,
        "journey_tool_links": journey_tools_checked,
        "story_chapter_links": chapter_links_checked,
        "local_references": len(checked_links),
        "local_assets": len(checked_assets),
        "players": media_players,
        "home_players": home_players,
        "total_players": media_players + home_players,
        "caption_tracks": captions,
        "public_text_files_scanned": len(public_text_files),
        "owner_pages": len(documents)-sum(p in legacy_paths for p in documents),
        "legacy_html_pages": sum(p in legacy_paths for p in documents),
        "legacy_template_notes": legacy_template_notes,
        "network_calls": 0,
        "errors": errors,
    }
    print(json.dumps(summary, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
