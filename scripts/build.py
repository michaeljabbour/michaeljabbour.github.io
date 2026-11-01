#!/usr/bin/env python3
"""Build the static portfolio from its public-only catalogue."""

from pathlib import Path, PurePosixPath
from html import escape
import json
import hashlib
import shutil
import re
import subprocess
from datetime import date
from public_views import write_public_views
from installer_download import write_installer
from migration_view import write_migration
from flow_views import load_flows, flow_links, flow_guide
from related_tools import load_related_tools, render_related_tools
from catalogue_admission import current_admission, HISTORICAL_IDS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
E = lambda v: escape(str(v), quote=True)


def link(url, label, cls=""):
    return f'<a href="{E(url)}" class="{E(cls)}">{label}</a>'


def checked_compatibility_sites():
    """Return only complete, hash-pinned public snapshots from the manifest."""
    manifest = ROOT / "compatibility/manifest.json"
    if not manifest.exists():
        return []
    for parent in (ROOT / "compatibility", manifest):
        if parent.is_symlink():
            raise ValueError("Compatibility source must not contain symlinks")
    data = json.loads(manifest.read_text())
    if data.get("schema_version") != "static-compatibility/v1":
        raise ValueError("Unsupported compatibility manifest")
    sites = []
    prefixes = set()
    for site in data["sites"]:
        prefix = site["prefix"]
        if not re.fullmatch(r"amplifier-[a-z0-9-]+", prefix) or prefix in prefixes:
            raise ValueError("Invalid or duplicate compatibility prefix")
        prefixes.add(prefix)
        source = ROOT / "compatibility/sites" / prefix
        if any(p.is_symlink() for p in [source.parent, source, *source.rglob("*")]):
            raise ValueError("Compatibility source must not contain symlinks")
        expected = {}
        for entry in site["files"]:
            name = entry["path"]
            path = PurePosixPath(name)
            if (
                path.is_absolute() or ".." in path.parts or "\\" in name
                or path.as_posix() != name or name in expected or name == "."
            ):
                raise ValueError("Invalid or duplicate compatibility path")
            expected[name] = entry
        actual = {p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file()}
        if not expected or actual != set(expected):
            raise ValueError(f"Compatibility file list differs: {prefix}")
        for name, entry in expected.items():
            content = (source / name).read_bytes()
            if len(content) != entry["bytes"] or hashlib.sha256(content).hexdigest() != entry["sha256"]:
                raise ValueError(f"Compatibility content differs: {prefix}/{name}")
        sites.append((prefix, source, expected))
    actual_prefixes = {p.name for p in (ROOT / "compatibility/sites").iterdir()}
    if actual_prefixes != prefixes:
        raise ValueError("Unlisted compatibility source directory")
    return sites


def main():
    data = json.loads((ROOT / "content/portfolio.json").read_text())
    media = json.loads((ROOT / "content/media.json").read_text())
    journey = json.loads((ROOT / "content/journey.json").read_text())
    stages = journey["stages"]
    stage_by_id = {s["id"]: s for s in stages}
    stage_index = {s["id"]: n for n, s in enumerate(stages)}
    style_url = (
        "/assets/site.css?v="
        + hashlib.sha256((ROOT / "assets/site.css").read_bytes()).hexdigest()[:12]
    )
    behavior_url = (
        "/assets/site.js?v="
        + hashlib.sha256((ROOT / "assets/site.js").read_bytes()).hexdigest()[:12]
    )
    projects = data["projects"]
    by_id = {p["id"]: p for p in projects}
    groups = {c["id"]: c for c in data["categories"]}
    migration = json.loads((ROOT / "content/migration/mapping.json").read_text())
    admission = current_admission(ROOT, data, migration)
    assert len(by_id) == len(projects)
    assert "basic-learning" not in by_id
    flow_data = load_flows(ROOT, projects)
    curated_related = load_related_tools(ROOT, by_id)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / ".nojekyll").touch()
    for prefix, source, _ in checked_compatibility_sites():
        shutil.copytree(source, OUT / prefix)

    def project_url(p):
        return "/capabilities/" + p["id"] + "/"

    def film(p):
        return media.get("films", {}).get(p["id"], {})

    def poster(p, loading="lazy", cls=""):
        m = film(p)
        src = m.get("still") or m.get("local_poster") or m.get("poster")
        if src:
            src = "/" + src.lstrip("/") if not src.startswith("http") else src
            return f'<img class="{cls}" src="{E(src)}" width="960" height="540" loading="{loading}" alt="{E(p["title"])} artwork">'
        return f'<div class="poster-fallback {cls}"><span>{E(p["title"])}</span></div>'

    def shell(title, description, body, active="home", path="/", extra_head=""):
        preview_label = '<p class="notice wrap" data-local-preview>Local preview: this is not the published site.</p>' if admission["preview_only"] else ""
        nav = [
            ("journey", "/#journey", "Work flows"),
            ("capabilities", "/capabilities/", "All capabilities"),
            ("films", "/films/", "Films & demos"),
            ("about", "/about/", "About"),
            ("blog", "https://www.michaeljabbour.com/", "Blog"),
        ]
        nav_html = "".join(
            f'<a href="{url}" aria-label="{label}"'
            + (' aria-current="page"' if active == ident else "")
            + f'> <span class="nav-full">{label}</span><span class="nav-short" aria-hidden="true">{ {"Work flows": "Flows", "All capabilities": "Library", "Films & demos": "Watch", "About": "About"}.get(label, label) }</span></a>'
            for ident, url, label in nav
        )
        return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · Michael Jabbour</title><meta name="description" content="{E(description)}">
<meta name="theme-color" content="#f5f7fa"><meta property="og:title" content="{E(title)} · Michael Jabbour"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="website"><meta property="og:url" content="https://michaeljabbour.github.io{E(path)}">
<meta property="og:image" content="https://michaeljabbour.github.io/assets/social.png"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="canonical" href="https://michaeljabbour.github.io{E(path)}">
<link rel="stylesheet" href="{style_url}"><script src="{behavior_url}" defer></script>{extra_head}</head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header wrap"><a class="identity" href="/" aria-label="Michael Jabbour home"><span class="monogram" aria-hidden="true">mj</span><span>michael jabbour</span></a>
<nav aria-label="Main navigation">{nav_html}</nav><a class="source-link" href="https://github.com/michaeljabbour">GitHub <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 15 15 5M5 5h10v10"/></svg></a></header>
{preview_label}<main id="main">{body}</main>
<footer class="site-footer wrap"><div><h2 class="footer-name">AI capabilities for practical work.</h2><p>Explore source code, setup requirements and a concrete first task.</p></div><nav aria-label="Footer navigation"><a href="/#journey">Browse work flows</a><a href="/capabilities/">All capabilities</a><a href="/films/">The films & demos</a><a href="https://www.michaeljabbour.com/">Blog</a><a href="/migration/">Update an installation</a><a href="https://github.com/michaeljabbour">GitHub</a></nav></footer>
</body></html>'''

    def write(path, text):
        folder = OUT / path
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(text)

    def feature(p, wide=False):
        return f'''<article class="feature {"feature-wide" if wide else ""}"><a class="feature-art" href="{project_url(p)}">{poster(p)}<span class="art-open" aria-hidden="true">Explore</span></a><div class="feature-copy"><p class="format">{E(p["format"])}</p><h3><a href="{project_url(p)}">{E(p["title"])}</a></h3><p>{E(p["summary"])}</p></div></article>'''

    hero_a, hero_b, hero_c = [
        by_id[i] for i in ["sizzle", "unknowns", "project-handoff"]
    ]
    hero_art = f'''<div class="hero-art" aria-label="A glimpse of the work"><span class="start-note">Start anywhere.</span><a class="hero-shot shot-main" href="{project_url(hero_a)}">{poster(hero_a, "eager")}<span><b>Sizzle</b> Direct the story.</span></a><a class="hero-shot shot-second" href="{project_url(hero_b)}">{poster(hero_b, "eager")}<span><b>Unknowns</b> Find the question.</span></a><a class="hero-shot shot-third" href="{project_url(hero_c)}">{poster(hero_c, "eager")}<span><b>Project Handoff</b> Leave a next step.</span></a><span class="art-caption">A story, a question, a way back in.</span></div>'''
    overview_file = ROOT / "content/home-film.json"
    if overview_file.exists():
        overview = json.loads(overview_file.read_text())
        if overview.get("src"):

            def asset_url(value):
                return (
                    value if value.startswith("https://") else "/" + value.lstrip("/")
                )

            assert overview.get("poster") and overview.get("caption"), (
                "Overview film needs a poster and captions."
            )
            transcript_link = (
                link(asset_url(overview["transcript"]), "Read the transcript")
                if overview.get("transcript")
                else ""
            )
            hero_art = f'''<div class="hero-story" id="story"><h2>{E(overview.get("title", "Good Work Has a Next Day"))}</h2><video controls playsinline preload="none" crossorigin="anonymous" poster="{E(asset_url(overview["poster"]))}" aria-label="Portfolio overview film" data-overview-video><source src="{E(asset_url(overview["src"]))}" type="video/mp4"><track kind="captions" srclang="en" label="English" src="{E(asset_url(overview["caption"]))}"></video>{transcript_link}<a class="story-to-journey" href="#journey">Browse the work flows</a></div>'''

    def journey_guide(home=False):
        intro = (
            (
                '<div class="journey-intro"><div><h2>Choose a category for your task.</h2><p>Find a capability for research, planning, software, review, creative production, migration or project continuity.</p></div><p class="journey-permission">Start with one capability. Each page explains the required input, setup and output.</p></div>'
            )
            if home
            else ""
        )
        steps = []
        panels = []
        for n, stage in enumerate(stages):
            ident = stage["id"]
            steps.append(
                f'''<a id="step-{E(ident)}" href="#stage-{E(ident)}" data-stage-link="{E(ident)}"><span class="step-number" aria-hidden="true">{n + 1}</span><span>{E(stage["title"])}</span></a>'''
            )
            members = [p for p in projects if p["category"] == ident]
            ranked = {key: i for i, key in enumerate(stage["lead_ids"])}
            members.sort(key=lambda p: ranked.get(p["id"], 99))
            tools = "".join(
                f'''<a class="journey-tool" data-journey-tool="{E(p["id"])}" href="{project_url(p)}"><span class="journey-tool-image">{poster(p)}</span><span><strong>{E(p["title"])}</strong><span>{E(p["summary"])}</span></span><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h12m-5-5 5 5-5 5"/></svg></a>'''
                for p in members
            )
            chapter = ""
            if stage["film_start"] is not None:
                moment = round(stage["film_start"])
                chapter_label = "Find the media examples in the film" if ident == "create" else "Find this moment in the film"
                chapter = f'''<a class="journey-film-link" href="/?moment={E(ident)}#story" data-story-moment="{E(ident)}" data-film-start="{stage["film_start"]}">{E(chapter_label)} <span>{moment // 60}:{moment % 60:02d}</span></a>'''
            level = "h3" if home else "h2"
            panels.append(
                f'''<section id="stage-{E(ident)}" class="journey-panel" data-stage-panel="{E(ident)}" aria-labelledby="question-{E(ident)}"><div class="journey-thinking"><p class="journey-moment">{n + 1} of 7 · {E(stage["title"])}</p><{level} id="question-{E(ident)}">{E(stage["question"])}</{level}><p class="journey-description">{E(stage["description"])}</p><div class="journey-output"><strong>Expected result</strong><p>{E(stage["output"])}</p></div><p class="journey-reflection">{E(stage["reflection"])}</p>{chapter}</div><div class="journey-tools"><h{int(level[1]) + 1}>Capabilities in this category</h{int(level[1]) + 1}>{tools}<a class="journey-browse" href="/capabilities/?category={E(ident)}">Browse this category</a></div></section>'''
            )
        return f"""<section class="work-journey wrap" id="journey" data-journey>{intro}<nav class="journey-steps" aria-label="Moments in the work" data-journey-nav>{"".join(steps)}</nav><div class="journey-panels">{"".join(panels)}</div><div class="journey-controls" data-journey-controls hidden><button class="journey-previous" data-journey-previous type="button">Previous category</button><p role="status" aria-live="polite" data-journey-status></p><button class="journey-next" data-journey-next type="button">Next category</button></div></section>"""

    selected = [
        "right-shape",
        "decisioncraft",
        "taste-elegance",
        "sizzle",
        "project-handoff",
        "research",
    ]
    legacy_chapters = '<div hidden aria-hidden="true">' + ''.join(
        f'<a href="/?moment={E(stage["id"])}#story" data-story-moment="{E(stage["id"])}" data-film-start="{stage["film_start"]}">{E(stage["title"])}</a>'
        for stage in stages if stage["film_start"] is not None
    ) + '</div>'
    home = f"""<section class="hero wrap"><div class="hero-copy"><p class="intro-line">A collection of {len(projects)} capabilities.</p><h1>AI tools for research, software, and creative work.</h1><p class="hero-description">Choose a capability for a specific task. Read the required input, setup and output, then try the first task with your own material.</p><div class="button-row"><a class="button primary" href="#journey">Browse work flows</a><a class="button secondary" href="/films/">Watch the films</a></div></div>{hero_art}</section>
{flow_guide(flow_data, projects, poster, stages)}{legacy_chapters}
<section class="point-of-view wrap section-space"><div class="pov-title"><span class="thought-mark" aria-hidden="true">↳</span><h2>Bring your<br>own judgment.</h2></div><div class="pov-copy"><p>Follow the source. Look at the alternatives. Ask what would make the thing more useful.</p><p>Each capability has a defined job, guide and source repository. Compare that job with your task before installing or running the capability.</p><a class="text-link" href="/about/">About the capability collection</a></div></section>
<section class="closing-section"><div class="wrap closing-content"><h2>Find a capability<br>for your next task.</h2><a class="button dark" href="/capabilities/">Browse all capabilities</a></div></section>"""
    write(
        "",
        shell(
            "AI tools for research, software, and creative work",
            f"Explore {len(projects)} AI capabilities for research, software and creative work, with input requirements, setup and a concrete first task.",
            home,
        ),
    )

    journey_page = f"""<section class="page-intro wrap journey-page-intro"><a class="back-link" href="/">Back to the start</a><h1>Start with a person.<br>Follow the work.</h1><p>{E(journey["intro"])}</p></section>{journey_guide()}<section class="journey-loop wrap"><p>A first version can send you back to the question. A new person can change the plan. Follow what you learn.</p><a class="text-link" href="/capabilities/">Or browse all {len(projects)} capabilities</a><a class="text-link" href="/journey/knowledge/">Proposed: from curation to creation</a></section>"""
    write(
        "journey",
        shell(
            "Follow the work",
            "Find your place in the work: seven human questions, with the AI capabilities that can help at each moment.",
            journey_page,
            "journey",
            "/journey/",
        ),
    )

    flow_options = "".join(f'<option value="{E(f["id"])}">{E(f["title"])}</option>' for f in flow_data["flows"])
    options = "".join(
        f'<option value="{E(c["id"])}">{E(c["title"])}</option>'
        for c in data["categories"]
    )
    formats = sorted(set(p["format"] for p in projects))
    format_options = "".join(f'<option value="{E(f)}">{E(f)}</option>' for f in formats)
    rows = []
    for p in projects:
        search = " ".join(
            [
                p["title"],
                p["summary"],
                p["audience"],
                groups[p["category"]]["title"],
                p["format"],
            ]
        )
        rows.append(
            f'''<article class="project-row" data-project data-category="{E(p["category"])}" data-flows="{E(" ".join(flow_data["memberships"][p["id"]]))}" data-format="{E(p["format"])}" data-search="{E(search.lower())}"><a class="row-art" href="{project_url(p)}">{poster(p)}</a><div class="row-body"><div class="row-meta"><span>{E(groups[p["category"]]["title"])}</span><span>{E(p["format"])}</span></div><h2><a href="{project_url(p)}">{E(p["title"])}</a></h2><p>{E(p["summary"])}</p>{flow_links(p, flow_data)}</div><a class="row-action" href="{project_url(p)}" aria-label="Explore {E(p["title"])}">Explore <span aria-hidden="true">↗</span></a></article>'''
        )
    library = f"""<section class="page-intro wrap"><a class="back-link" href="/">Home</a><h1>Find an AI capability<br>for your task.</h1><p>Browse {len(projects)} capabilities by kind of work or technical format. Each page states the intended user, input, action, output and prerequisites before a first task.</p><a class="library-journey-link" href="/#journey">Browse the three work flows</a></section><section class="library-section wrap"><form id="project-filters" class="filters" role="search" action="/capabilities/"><div class="search-field"><label for="search">Find a capability</label><input id="search" type="search" name="q" placeholder="Try research, a film, a handoff…" autocomplete="off"></div><div><label for="flow">Kind of work</label><select id="flow" name="flow"><option value="all">All work flows</option>{flow_options}</select></div><select id="category" name="category" aria-label="Legacy task category" hidden><option value="all">All task areas</option>{options}</select><div><label for="format">Technical format</label><select id="format" name="format"><option value="all">All formats</option>{format_options}</select></div></form><noscript><p class="notice">All capabilities are listed below. Search and filters are available with JavaScript enabled.</p></noscript><div class="result-line"><p id="result-count" role="status" aria-live="polite">{len(projects)} capabilities</p><button class="text-button" type="button" id="clear-filters" hidden>Clear filters</button></div><div class="project-list">{"".join(rows)}</div><div id="no-results" class="empty-state" hidden><h2>No match yet.</h2><p>Try a broader word, another kind of work, or reset the filters to see the whole collection.</p><button class="button primary" type="button" data-reset-filters>Show all capabilities</button></div></section><section class="format-guide wrap"><h2>Technical formats and setup.</h2><div><p><strong>A skill</strong> guides how an agent approaches a task. You bring the host and the tools it needs.</p><p><strong>A smart tool</strong> combines guidance with a specific interface or mechanism.</p><p><strong>A tool or library</strong> provides a mechanism that other capabilities can use. Its own guide explains the runtime and dependencies.</p></div></section>"""
    write(
        "capabilities",
        shell(
            "Capabilities",
            "Find an AI capability by the work you need to do. Browse research, decisions, building, creative work and collaboration.",
            library,
            "capabilities",
            "/capabilities/",
        ),
    )

    film_tiles = []
    for p in projects:
        m = film(p)
        if not m.get("src") or not m.get("available"):
            continue
        label = m.get("label") or "Watch film"
        film_tiles.append(
            f'''<article class="film-card"><a class="film-art" href="{project_url(p)}#watch">{poster(p)}<span class="play-disc" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m9 5 11 7-11 7z"/></svg></span></a><div class="film-card-copy"><h2><a href="{project_url(p)}#watch">{E(p["title"])}</a></h2><p>{E(p["summary"])}</p><a class="text-link" href="{project_url(p)}#watch">{E(label)}</a></div></article>'''
        )
    films_html = f"""<section class="page-intro wrap"><a class="back-link" href="/">Home</a><h1>See the work<br>in motion.</h1><p>Captioned films, lessons and a visual demo that introduce the capabilities. Pick one to see its purpose and approach.</p></section><section class="wrap film-library"><div class="film-grid">{"".join(film_tiles)}</div><p class="library-footnote">Media is hosted on each capability’s own site. The individual page links its transcript and short cut when available.</p></section>"""
    write(
        "films",
        shell(
            "Films and demos",
            "Watch the films, lessons and demos behind Michael Jabbour’s AI capabilities.",
            films_html,
            "films",
            "/films/",
        ),
    )

    about = """<section class="page-intro wrap about-intro"><a class="back-link" href="/">Home</a><h1>About the capability<br>collection.</h1><p>A public collection of AI capabilities for research, software development, review, creative production and project continuity.</p></section><section class="about-body wrap"><div class="about-statement"><h2>Good work has<br>a next day.</h2><p>A first draft gives you something to react to. The next questions matter too: where the evidence came from, why a choice was made, what was checked, and how someone else can continue.</p><p>I build capabilities around those moments. Some help with research and judgment. Some help build software or direct creative work. Others keep the evidence, decisions and next steps close to the project.</p><p>They have different jobs and different shapes. You can start with one that fits the work in front of you.</p><p>For writing and notes, visit <a href="https://www.michaeljabbour.com/">my blog</a>.</p></div><div class="principles"><article><h3>Keep the evidence close.</h3><p>Make it possible to return to a source, inspect a claim and see what remains uncertain.</p></article><article><h3>Choose a shape that fits.</h3><p>A useful extension can be a small skill, a tool or a shared library. Let the job decide.</p></article><article><h3>Improve with a reason.</h3><p>Make the change intentional. Explain what it should help, and what would show that it did.</p></article><article><h3>Make the next step clear.</h3><p>A person returning tomorrow should have a place to begin, with the current state and the important decisions visible.</p></article></div></section><section class="closing-section"><div class="wrap closing-content"><h2>Choose a capability<br>for your task.</h2><div class="button-row"><a class="button dark" href="/capabilities/">Browse the capabilities</a><a class="text-link" href="https://github.com/michaeljabbour">Find me on GitHub</a></div></div></section>"""
    write(
        "about",
        shell(
            "About",
            "Michael Jabbour’s approach to AI capabilities: keep evidence close, choose the right shape and make the next step clear.",
            about,
            "about",
            "/about/",
        ),
    )

    for p in projects:
        m = film(p)
        watch = ""
        workflow = ""
        if p.get("workflow_image"):
            paths = {"articlecraft": "docs/workflow.svg", "idea-talks": "docs/workflow.svg", "stories": "skills/stories/assets/workflow.svg"}
            if p["id"] not in admission["additions"] or p["workflow_image"] != "/assets/workflows/" + p["id"] + ".svg" or p.get("workflow_path") != paths.get(p["id"]):
                raise ValueError("Workflow image must use its admitted local asset and source path")
            public_pin = admission["additions"][p["id"]]["source_commit"] or "main"
            workflow_source_url = p["repo_url"] + "/blob/" + public_pin + "/" + p["workflow_path"]
            workflow = f'<section class="capability-workflow wrap" aria-labelledby="workflow-title"><h2 id="workflow-title">How the work moves</h2><img src="{E(p["workflow_image"])}" alt="{E(p["workflow_alt"])}" loading="lazy"><p><a href="{E(workflow_source_url)}">Workflow from the capability documentation</a> · <a href="/assets/workflows/{E(p["id"])}.LICENSE.txt">MIT license</a></p></section>'
        if m.get("available") and m.get("src"):
            poster_path = (
                m.get("still") or m.get("local_poster") or m.get("poster") or ""
            )
            if poster_path and not poster_path.startswith("http"):
                poster_path = "/" + poster_path.lstrip("/")
            caption = (
                f'<track kind="captions" src="{E(m["caption"])}" srclang="en" label="English">'
                if m.get("caption")
                else ""
            )
            aux = []
            if m.get("transcript"):
                aux.append(link(m["transcript"], "Read transcript"))
            if m.get("cut"):
                aux.append(link(m["cut"], "Watch 15-second cut"))
            if m.get("film_url"):
                aux.append(link(m["film_url"], "Open on the capability site"))
            caption_note = (
                ""
                if m.get("caption")
                else '<p class="caption-note">Visual demo; no caption track. The full capability guide explains the example.</p>'
            )
            watch = f'''<section class="watch-section wrap" id="watch"><h2 class="media-heading">Video introduction</h2><div class="detail-player"><video controls playsinline preload="none" crossorigin="anonymous" poster="{E(poster_path)}" aria-label="{E(p["title"])} {E(m.get("kind", "film"))}"><source src="{E(m["src"])}" type="video/mp4">{caption}<p>Your browser cannot play this video. <a href="{E(m["src"])}">Open the video file.</a></p></video></div><div class="media-links">{"".join(aux)}</div>{caption_note}</section>'''
        related = [
            by_id[i] for i in p.get("related", []) if i in by_id and i != p["id"]
        ][:3]
        related_html = (
            f"""<section class="related-section wrap section-space"><div class="section-heading"><h2>Another part of the work.</h2><a class="text-link" href="/capabilities/">Back to the collection</a></div><div class="related-grid">{"".join(feature(r) for r in related)}</div></section>"""
            if related
            else ""
        )
        limits = p.get("limitations") or ""
        if isinstance(limits, list):
            limits = " ".join(limits)
        if p["format"] == "Skill":
            first_intro = "Install the complete skill folder, then ask your agent to perform this task with the project or source material you select."
            copy_label = "Copy starter prompt"
        elif p["format"] == "Smart tool":
            first_intro = "Follow the native setup guide first, then use this task with your selected input. Confirm which operations are authorized before execution."
            copy_label = "Copy first step"
        else:
            first_intro = "Install and configure the native tool or library first. Follow the operating steps below with an input you select."
            copy_label = "Copy first step"
        guide_link = "" if p["id"] in admission["additions"] else f'<a href="{E(p["site_url"])}">Full capability guide</a>'
        setup_link = f'<p><a href="{E(p["install_url"])}">Read the repository installation steps</a></p>' if p["id"] in admission["additions"] else ""
        requirements = "".join(f"<li>{E(item)}</li>" for item in p["prerequisites"])
        detail = f'''<section class="detail-heading wrap">
<a class="back-link" href="/#stage-{E(p["category"])}">{E(groups[p["category"]]["title"])}</a>
{flow_links(p, flow_data)}<p class="format">Technical format: {E(p["format"])}</p><h1>{E(p["title"])}</h1>
<p class="detail-promise">{E(p["summary"])}</p>
<div class="button-row"><a class="button primary" href="#first-task">Try the first task</a><a class="text-link" href="{E(p["repo_url"])}">View source on GitHub <span aria-hidden="true">↗</span></a></div></section>
<section class="project-details wrap" aria-label="Purpose, input, output and setup">
<div class="project-description"><h2>What {E(p["title"])} does</h2>
<p>{E(p["description"])}</p>
<dl class="capability-facts"><div><dt>For</dt><dd>{E(p["audience"])}</dd></div>
<div><dt>Bring</dt><dd>{E(p["input"])}</dd></div>
<div><dt>Action</dt><dd>{E(p["action"])}</dd></div>
<div><dt>Output</dt><dd>{E(p["result"])}</dd></div></dl>
<section class="setup-note" id="setup" aria-labelledby="setup-title"><h3 id="setup-title">Runtime and prerequisites</h3>
<p>{E(p["runtime"])}</p><ul>{requirements}</ul>{setup_link}</section></div>
<aside class="first-use" id="first-task" aria-labelledby="first-task-title"><h2 id="first-task-title">Your first task</h2>
<p class="first-use-intro">{E(first_intro)}</p><p class="first-use-prompt" id="first-prompt">{E(p["first_prompt"])}</p>
<button class="copy-button" data-copy="first-prompt" type="button">Copy first task</button><p class="copy-status" role="status" aria-live="polite"></p>
<div class="start-links"><a href="{E(p["install_url"])}">Installation guide</a>{guide_link}<a href="{E(p["repo_url"])}">Repository and license</a></div></aside></section>
{workflow}{watch}
<section class="capability-scope wrap" aria-label="Example and limitations"><div class="output-example"><h2>Example output</h2><p>{E(p["output"])}</p><p class="example-label">Fictional illustration, not a result from your task or measured user evidence.</p></div>
{('<div class="scope-note"><h2>Limitations</h2><p>' + E(limits) + "</p></div>") if limits else ""}</section>{related_html}'''
        context = f'<section class="journey-context wrap" aria-label="Explore related work"><div><h2>Explore by kind of work</h2>{flow_links(p, flow_data)}</div><a href="/capabilities/">Browse all capabilities</a></section>'
        detail += render_related_tools(p["id"], curated_related)
        detail = (
            detail.replace(related_html, context + related_html)
            if related_html
            else detail + context
        )
        write(
            "capabilities/" + p["id"],
            shell(p["title"], p["summary"], detail, "capabilities", project_url(p)),
        )
    write_public_views(ROOT, OUT, write, shell, projects, stages)
    write_installer(ROOT, OUT)
    write_migration(ROOT, OUT, write, shell, HISTORICAL_IDS)

    notfound = """<section class="page-intro wrap not-found"><p>404</p><h1>Let’s find<br>a way back.</h1><p>This page isn’t in the collection. Browse the capabilities or return to the homepage.</p><div class="button-row"><a class="button primary" href="/capabilities/">Browse capabilities</a><a class="text-link" href="/">Go home</a></div></section>"""
    (OUT / "404.html").write_text(
        shell(
            "Page not found",
            "Find your way back to Michael Jabbour’s AI capability collection.",
            notfound,
        )
    )
    urls = ["", "journey/", "capabilities/", "films/", "about/", "capabilities/categories/", "journey/knowledge/", "reports/capability-installer/", "migration/"] + [
        "capabilities/" + p["id"] + "/" for p in projects
    ]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(
            "<url><loc>https://michaeljabbour.github.io/" + u + "</loc></url>"
            for u in urls
        )
        + "</urlset>"
    )
    (OUT / "journey.json").write_text(
        json.dumps(journey, ensure_ascii=False, indent=2) + "\n"
    )
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://michaeljabbour.github.io/sitemap.xml\n"
    )
    publication = {"schema_version": "portfolio-artifact/v1", "source_commit": subprocess.check_output(["git", "-c", "core.fsmonitor=false", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(), "preview_only": admission["preview_only"], "publication_ready": admission["publication_ready"], "capability_ids": admission["capability_ids"], "additional_sources": admission["additions"]}
    (OUT / "publication.json").write_text(json.dumps(publication, indent=2) + "\n")
    (OUT / "portfolio.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "pages": len(list(OUT.rglob("*.html"))),
                "capabilities": len(projects),
                "media": len(film_tiles),
                "output": str(OUT),
            }
        )
    )


if __name__ == "__main__":
    main()
