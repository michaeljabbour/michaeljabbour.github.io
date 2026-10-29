#!/usr/bin/env python3
"""Build the static portfolio from its public-only catalogue."""

from pathlib import Path
from html import escape
import json
import hashlib
import shutil
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
E = lambda v: escape(str(v), quote=True)


def link(url, label, cls=""):
    return f'<a href="{E(url)}" class="{E(cls)}">{label}</a>'


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
    assert len(by_id) == len(projects) == 33
    assert "basic-learning" not in by_id
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    (OUT / ".nojekyll").touch()

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
        nav = [
            ("journey", "/journey/", "The journey"),
            ("capabilities", "/capabilities/", "All capabilities"),
            ("films", "/films/", "Films & demos"),
            ("about", "/about/", "About"),
        ]
        nav_html = "".join(
            f'<a href="{url}" aria-label="{label}"'
            + (' aria-current="page"' if active == ident else "")
            + f'> <span class="nav-full">{label}</span><span class="nav-short" aria-hidden="true">{ {"The journey": "Journey", "All capabilities": "Library", "Films & demos": "Watch", "About": "About"}.get(label, label) }</span></a>'
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
<main id="main">{body}</main>
<footer class="site-footer wrap"><div><h2 class="footer-name">Take it from here.</h2><p>Built by Michael. Here to pick up and make your own.</p></div><nav aria-label="Footer navigation"><a href="/journey/">Follow the work</a><a href="/capabilities/">All capabilities</a><a href="/films/">The films & demos</a><a href="https://github.com/michaeljabbour">GitHub</a></nav></footer>
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
            hero_art = f'''<div class="hero-story" id="story"><h2>{E(overview.get("title", "Good Work Has a Next Day"))}</h2><video controls playsinline preload="none" crossorigin="anonymous" poster="{E(asset_url(overview["poster"]))}" aria-label="Portfolio overview film" data-overview-video><source src="{E(asset_url(overview["src"]))}" type="video/mp4"><track kind="captions" srclang="en" label="English" src="{E(asset_url(overview["caption"]))}"></video>{transcript_link}<a class="story-to-journey" href="#journey">Find your place in the story</a></div>'''

    def journey_guide(home=False):
        intro = (
            (
                '<div class="journey-intro"><div><h2>Follow the work.</h2><p>Start with a person and a question. Find the part you need, and the tools that can help.</p></div><p class="journey-permission">A way through, with room to go back. You don’t need every step or every tool.</p></div>'
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
                chapter = f'''<a class="journey-film-link" href="/?moment={E(ident)}#story" data-story-moment="{E(ident)}" data-film-start="{stage["film_start"]}">Find this moment in the film <span>{moment // 60}:{moment % 60:02d}</span></a>'''
            level = "h3" if home else "h2"
            panels.append(
                f'''<section id="stage-{E(ident)}" class="journey-panel" data-stage-panel="{E(ident)}" aria-labelledby="question-{E(ident)}"><div class="journey-thinking"><p class="journey-moment">{n + 1} of 7 · {E(stage["title"])}</p><{level} id="question-{E(ident)}">{E(stage["question"])}</{level}><p class="journey-description">{E(stage["description"])}</p><div class="journey-output"><strong>Something to take with you</strong><p>{E(stage["output"])}</p></div><p class="journey-reflection">{E(stage["reflection"])}</p>{chapter}</div><div class="journey-tools"><h{int(level[1]) + 1}>Tools for this moment</h{int(level[1]) + 1}>{tools}<a class="journey-browse" href="/capabilities/?category={E(ident)}">Browse this part of the collection</a></div></section>'''
            )
        return f"""<section class="work-journey wrap" id="journey" data-journey>{intro}<nav class="journey-steps" aria-label="Moments in the work" data-journey-nav>{"".join(steps)}</nav><div class="journey-panels">{"".join(panels)}</div><div class="journey-controls" data-journey-controls hidden><button class="journey-previous" data-journey-previous type="button">Previous moment</button><p role="status" aria-live="polite" data-journey-status></p><button class="journey-next" data-journey-next type="button">Next moment</button></div></section>"""

    selected = [
        "right-shape",
        "decisioncraft",
        "taste-elegance",
        "sizzle",
        "project-handoff",
        "research",
    ]
    category_links = "".join(
        f"""<li><a href="/journey/#stage-{E(stage["id"])}"><span aria-hidden="true">{index + 1}</span>{E(stage["title"])}</a></li>"""
        for index, stage in enumerate(stages)
    )
    category_launcher = f"""<nav class="category-launcher wrap" aria-label="Work categories" data-category-launcher><div class="category-launcher-head"><p>Where are you starting?</p><a href="/capabilities/" aria-label="Browse all 33 capabilities">All 33</a></div><ol class="category-links">{category_links}</ol></nav>"""
    home = f"""{category_launcher}<section class="hero wrap"><div class="hero-copy"><p class="intro-line">A few useful things for working with AI.</p><h1>Good work<br>has a next day.</h1><p class="hero-description">Skills and tools for thinking things through, making things, and picking up where you left off.<br><span class="hero-invitation">Take what’s useful. Make it yours.</span></p><div class="button-row"><a class="button primary" href="#journey">Browse categories</a><a class="button secondary" href="/films/">Watch the films</a></div></div>{hero_art}</section>
{journey_guide(home=True)}
<section class="selected-section wrap section-space"><div class="section-heading"><div><h2>A few things to try.</h2><p>Pick one up. See what it opens.</p></div><a class="text-link" href="/capabilities/">See all 33</a></div><div class="feature-grid">{"".join(feature(by_id[i], n < 2) for n, i in enumerate(selected))}</div></section>
<section class="point-of-view wrap section-space"><div class="pov-title"><span class="thought-mark" aria-hidden="true">↳</span><h2>Bring your<br>own judgment.</h2></div><div class="pov-copy"><p>Follow the source. Look at the alternatives. Ask what would make the thing more useful.</p><p>That’s the thread here. Each capability has its own job, guide and source. Bring one into your work when it has something to offer.</p><a class="text-link" href="/about/">A little of the thinking behind it</a></div></section>
<section class="closing-section"><div class="wrap closing-content"><h2>Pick something up.<br>See where it goes.</h2><a class="button dark" href="/capabilities/">Find a place to start</a></div></section>"""
    write(
        "",
        shell(
            "Good work has a next day",
            "AI skills, tools and things to build on. Explore Michael Jabbour’s work, watch the films and find something useful.",
            home,
        ),
    )

    journey_page = f"""<section class="page-intro wrap journey-page-intro"><a class="back-link" href="/">Back to the start</a><h1>Start with a person.<br>Follow the work.</h1><p>{E(journey["intro"])}</p></section>{journey_guide()}<section class="journey-loop wrap"><p>A first version can send you back to the question. A new person can change the plan. Follow what you learn.</p><a class="text-link" href="/capabilities/">Or browse all 33 capabilities</a></section>"""
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
            f'''<article class="project-row" data-project data-category="{E(p["category"])}" data-format="{E(p["format"])}" data-search="{E(search.lower())}"><a class="row-art" href="{project_url(p)}">{poster(p)}</a><div class="row-body"><div class="row-meta"><span>{E(groups[p["category"]]["title"])}</span><span>{E(p["format"])}</span></div><h2><a href="{project_url(p)}">{E(p["title"])}</a></h2><p>{E(p["summary"])}</p></div><a class="row-action" href="{project_url(p)}" aria-label="Explore {E(p["title"])}">Explore <span aria-hidden="true">↗</span></a></article>'''
        )
    library = f"""<section class="page-intro wrap"><a class="back-link" href="/">Home</a><h1>What’s the<br>next thing?</h1><p>Thirty-three skills, tools and libraries. Each does a particular job. Find one for what you’re working on, then take a look inside.</p><a class="library-journey-link" href="/journey/">Find your place in the journey</a></section><section class="library-section wrap"><form id="project-filters" class="filters" role="search" action="/capabilities/"><div class="search-field"><label for="search">Find a capability</label><input id="search" type="search" name="q" placeholder="Try research, a film, a handoff…" autocomplete="off"></div><div><label for="category">What are you working on?</label><select id="category" name="category"><option value="all">All kinds of work</option>{options}</select></div><div><label for="format">Format</label><select id="format" name="format"><option value="all">All formats</option>{format_options}</select></div></form><noscript><p class="notice">All capabilities are listed below. Search and filters are available with JavaScript enabled.</p></noscript><div class="result-line"><p id="result-count" role="status" aria-live="polite">33 capabilities</p><button class="text-button" type="button" id="clear-filters" hidden>Clear filters</button></div><div class="project-list">{"".join(rows)}</div><div id="no-results" class="empty-state" hidden><h2>No match yet.</h2><p>Try a broader word, another kind of work, or reset the filters to see the whole collection.</p><button class="button primary" type="button" data-reset-filters>Show all capabilities</button></div></section><section class="format-guide wrap"><h2>A few formats, each with a purpose.</h2><div><p><strong>A skill</strong> guides how an agent approaches a task. You bring the host and the tools it needs.</p><p><strong>A smart tool</strong> combines guidance with a specific interface or mechanism.</p><p><strong>A tool or library</strong> provides a mechanism that other capabilities can use. Its own guide explains the runtime and dependencies.</p></div></section>"""
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

    about = """<section class="page-intro wrap about-intro"><a class="back-link" href="/">Home</a><h1>A little of the<br>thinking behind it.</h1><p>Skills, tools and experiments in making AI useful. Keep the thinking visible, make the thing with care, and leave someone a way in.</p></section><section class="about-body wrap"><div class="about-statement"><h2>Good work has<br>a next day.</h2><p>A first draft gives you something to react to. The next questions matter too: where the evidence came from, why a choice was made, what was checked, and how someone else can continue.</p><p>I build capabilities around those moments. Some help with research and judgment. Some help build software or direct creative work. Others keep the evidence, decisions and next steps close to the project.</p><p>They have different jobs and different shapes. You can start with one that fits the work in front of you.</p></div><div class="principles"><article><h3>Keep the evidence close.</h3><p>Make it possible to return to a source, inspect a claim and see what remains uncertain.</p></article><article><h3>Choose a shape that fits.</h3><p>A useful extension can be a small skill, a tool or a shared library. Let the job decide.</p></article><article><h3>Improve with a reason.</h3><p>Make the change intentional. Explain what it should help, and what would show that it did.</p></article><article><h3>Make the next step clear.</h3><p>A person returning tomorrow should have a place to begin, with the current state and the important decisions visible.</p></article></div></section><section class="closing-section"><div class="wrap closing-content"><h2>Take what’s useful.<br>Make it yours.</h2><div class="button-row"><a class="button dark" href="/capabilities/">Browse the capabilities</a><a class="text-link" href="https://github.com/michaeljabbour">Find me on GitHub</a></div></div></section>"""
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
            watch = f'''<section class="watch-section wrap" id="watch"><div class="detail-player"><video controls playsinline preload="none" crossorigin="anonymous" poster="{E(poster_path)}" aria-label="{E(p["title"])} {E(m.get("kind", "film"))}"><source src="{E(m["src"])}" type="video/mp4">{caption}<p>Your browser cannot play this video. <a href="{E(m["src"])}">Open the video file.</a></p></video></div><div class="media-links">{"".join(aux)}</div>{caption_note}</section>'''
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
            first_intro = "Install the skill first and provide the project or source material it needs. These starter prompts use illustrative examples; adapt them to your work."
            copy_label = "Copy starter prompt"
        elif p["format"] == "Smart tool":
            first_intro = "Follow the setup guide first. This starting brief helps you frame a task for the tool."
            copy_label = "Copy first step"
        else:
            first_intro = "Start with the native setup guide. This is first-use guidance for the tool or library, rather than an agent prompt."
            copy_label = "Copy first step"
        detail = f'''<section class="detail-heading wrap"><a class="back-link" href="/journey/#stage-{E(p["category"])}">{E(groups[p["category"]]["title"])}</a><p class="format">{E(p["format"])}</p><h1>{E(p["title"])}</h1><p class="detail-promise">{E(p["summary"])}</p><div class="button-row"><a class="button primary" href="{E(p["install_url"])}">Get started</a><a class="text-link" href="{E(p["repo_url"])}">View source on GitHub <span aria-hidden="true">↗</span></a></div></section>{watch}<section class="project-details wrap"><div class="project-description"><h2>What it’s for.</h2><p>{E(p["description"])}</p><p class="audience"><strong>Who it’s for</strong><br>{E(p["audience"])}</p><div class="output-example"><h3>A possible output</h3><p>{E(p["output"])}</p><p class="example-label">Illustrative example, not a measured result.</p></div>{('<div class="scope-note"><h3>Before you begin</h3><p>' + E(limits) + "</p></div>") if limits else ""}</div><aside class="first-use"><h2>Try a first step.</h2><p class="first-use-intro">{E(first_intro)}</p><p class="first-use-prompt" id="first-prompt">{E(p["first_prompt"])}</p><button class="copy-button" data-copy="first-prompt" type="button">{E(copy_label)}</button><p class="copy-status" role="status" aria-live="polite"></p><div class="start-links"><a href="{E(p["install_url"])}">Installation and prerequisites</a><a href="{E(p["site_url"])}">Full capability guide</a><a href="{E(p["repo_url"])}">Repository and license</a></div></aside></section>{related_html}'''
        stage_n = stage_index[p["category"]]
        stage = stages[stage_n]
        before = stages[stage_n - 1] if stage_n else None
        after = stages[(stage_n + 1) % len(stages)]
        previous_link = (
            f'<a href="/journey/#stage-{before["id"]}">Before this: {E(before["title"])}</a>'
            if before
            else ""
        )
        next_label = (
            "Start with a new question"
            if stage_n == len(stages) - 1
            else "Next: " + after["title"]
        )
        context = f"""<section class="journey-context wrap" aria-label="Continue the journey"><div><p>One part of the work</p><a href="/journey/#stage-{E(stage["id"])}">{stage_n + 1} · {E(stage["title"])}</a></div><nav aria-label="Previous and next moment">{previous_link}<a href="/journey/#stage-{after["id"]}">{E(next_label)}</a></nav></section>"""
        detail = (
            detail.replace(related_html, context + related_html)
            if related_html
            else detail + context
        )
        write(
            "capabilities/" + p["id"],
            shell(p["title"], p["summary"], detail, "capabilities", project_url(p)),
        )
    notfound = """<section class="page-intro wrap not-found"><p>404</p><h1>Let’s find<br>a way back.</h1><p>This page isn’t in the collection. Browse the capabilities or return to the homepage.</p><div class="button-row"><a class="button primary" href="/capabilities/">Browse capabilities</a><a class="text-link" href="/">Go home</a></div></section>"""
    (OUT / "404.html").write_text(
        shell(
            "Page not found",
            "Find your way back to Michael Jabbour’s AI capability collection.",
            notfound,
        )
    )
    urls = ["", "journey/", "capabilities/", "films/", "about/"] + [
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
