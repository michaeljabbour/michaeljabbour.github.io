#!/usr/bin/env python3
"""Check the built public portfolio without making network calls."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
ORIGIN = "https://michaeljabbour.github.io"
FORMATS = {"Skill", "Smart tool", "Library", "Tool"}
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


def main() -> int:
    errors: list[str] = []
    checked_links: set[tuple[str, str]] = set()
    checked_assets: set[str] = set()

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
    projects = catalogue.get("projects", [])
    categories = catalogue.get("categories", [])
    ids = [p.get("id") for p in projects]
    category_ids = [c.get("id") for c in categories]
    require(
        len(ids) == len(set(ids)) == 33,
        "Catalogue must contain exactly 33 unique public capability IDs",
    )
    require(
        "basic-learning" not in ids,
        "Private learning experiment is excluded from the public catalogue",
    )
    require(
        len(category_ids) == len(set(category_ids)) == 7,
        "Seven unique work categories are required",
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
    html_files = sorted(OUT.rglob("*.html")) if OUT.exists() else []
    documents = {path: Document(path.read_text()) for path in html_files}
    require(
        len(html_files) == 38,
        "Build must contain 38 HTML pages (33 capability pages, four index pages and 404)",
    )
    expected_routes = {
        OUT / "capabilities" / ident / "index.html"
        for ident in ids
        if isinstance(ident, str)
    }
    actual_routes = set((OUT / "capabilities").glob("*/index.html"))
    require(
        actual_routes == expected_routes,
        "Built capability routes do not match the 33 catalogue IDs",
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

    for path, doc in documents.items():
        relative = path.relative_to(OUT)
        raw = path.read_text()
        require(
            doc.title.strip() and "Michael Jabbour" in doc.title,
            f"{relative}: meaningful owner-attributed title required",
        )
        descriptions = doc.select("meta", name="description")
        require(
            len(descriptions) == 1 and bool(descriptions[0].get("content")),
            f"{relative}: one nonempty description required",
        )
        canonical = doc.select("link", rel="canonical")
        route = (
            "/" + str(relative.parent).replace("\\", "/") + "/"
            if relative.parent != Path(".")
            else "/"
        )
        if path.name == "404.html":
            route = "/"  # The error page intentionally points visitors back to the homepage.
        require(
            len(canonical) == 1 and canonical[0].get("href") == ORIGIN + route,
            f"{relative}: canonical does not match its public route",
        )
        require(
            len(doc.select("h1")) == 1, f"{relative}: exactly one page heading required"
        )
        require(
            "main" in doc.ids and bool(doc.select("html", lang="en")),
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
            if tag == "button":
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

    library = documents.get(OUT / "capabilities/index.html")
    if library:
        rows = [
            a for tag, a in library.elements if tag == "article" and "data-project" in a
        ]
        require(
            len(rows) == 33,
            "Library must expose all 33 project rows before JavaScript runs",
        )
        library_ids = set()
        for attributes in library.select("a"):
            match = re.fullmatch(
                r"/capabilities/([^/]+)/", urlsplit(attributes.get("href", "")).path
            )
            if match:
                library_ids.add(match.group(1))
        require(
            library_ids == set(ids),
            "Library links do not cover exactly the 33 capability routes",
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
            and project["site_url"] in links
            and project["install_url"] in links,
            f"{ident}: source, guide and installation links are required",
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
                metadata.get("still") or metadata.get("local_poster") or metadata.get("poster") or ""
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
        in {".html", ".css", ".js", ".json", ".xml", ".txt", ".md", ".svg"}
    ]
    private_markers = [
        "/Users/",
        "file:///",
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
        for marker in private_markers:
            require(
                marker not in raw,
                f"{path.relative_to(OUT)}: private-workspace or excluded-project marker found",
            )
        for label, pattern in secret_patterns.items():
            require(
                not re.search(pattern, raw),
                f"{path.relative_to(OUT)}: possible {label} found (value suppressed)",
            )
    public_catalogue = load_json(OUT / "portfolio.json")
    require(
        public_catalogue == catalogue,
        "Public catalogue differs from reviewed source content",
    )
    sitemap = OUT / "sitemap.xml"
    if sitemap.exists():
        sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text()))
        expected_urls = {
            ORIGIN + route for route in ["/", "/about/", "/capabilities/", "/films/"]
        } | {ORIGIN + "/capabilities/" + ident + "/" for ident in ids}
        require(
            sitemap_urls == expected_urls,
            "Sitemap must cover the 37 public content routes exactly",
        )
    else:
        errors.append("Missing sitemap.xml")

    summary = {
        "status": "passed" if not errors else "failed",
        "pages": len(documents),
        "projects": len(projects),
        "categories": len(categories),
        "local_references": len(checked_links),
        "local_assets": len(checked_assets),
        "players": media_players,
        "home_players": home_players,
        "total_players": media_players + home_players,
        "caption_tracks": captions,
        "public_text_files_scanned": len(public_text_files),
        "network_calls": 0,
        "errors": errors,
    }
    print(json.dumps(summary, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
