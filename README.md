# Michael Jabbour

A portfolio of AI skills, tools and libraries for work people can build on.

The site introduces the work, groups 33 public capabilities by the task they support, and gives each its own page with media, a first step, installation and source. Films stay hosted on their capability sites; this repository keeps lightweight copies of the existing poster artwork.

## Build and preview

Requires Python 3.10+ and Node.js for the JavaScript syntax check. The site itself has no runtime dependencies, external fonts, analytics or backend.

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check assets/site.js
python3 scripts/serve.py
```

Open `http://127.0.0.1:8781/`. The read-only local preview server supports byte ranges so chapter links can seek into the film; a basic HTTP server may not. This helper is not part of the deployed site. The build writes `dist/`, which is the deployment artifact. All routes use the root of `michaeljabbour.github.io`; preview the site at a server root, not a repository subpath.

## Content

- `content/portfolio.json`: owner introduction, seven task categories and 33 capability entries.
- `content/journey.json`: the seven human questions, their order, outcomes, tool selections and actual film chapter times.
- `content/media.json`: verified media destinations, local poster paths and observation scope.
- `assets/`: site styling, behavior and poster artwork.
- `scripts/build.py`: generates the homepage, journey, library, films, About, 33 detail pages, 404 and sitemap.
- `scripts/check.py`: checks routes, metadata, assets, media consistency and public-only content.
- `DESIGN.md`: design direction and rationale.

Edit the catalogue to change copy or related capabilities. Keep intended functions distinct from proven outcomes. Fictional outputs are labeled. Preserve each capability’s actual installation anchor, meaningful prerequisites and limits.

The overview film is now on the homepage. [Film setup notes](docs/OVERVIEW-FILM.md) describe its assets; [journey notes](docs/JOURNEY.md) explain how the human questions and tools connect. The sequence is: figure it out, make a call, build, improve, make it visible, take it somewhere new, pick it up again. Visitors can start anywhere and loop back. Chapter links use stage IDs and actual caption times; the unspoken adaptation moment has no invented timestamp.

## GitHub Pages

The target repository is `michaeljabbour/michaeljabbour.github.io`, with GitHub Pages configured to use GitHub Actions. `.github/workflows/pages.yml` builds and checks pull requests, then publishes reviewed changes on `main`. The public repository and Pages setting have been created. This local checkout has no remote configured; connecting and publishing its source remain separate actions.

It uploads only `dist/`. The public site contains no private audit, owner workbook, research records or local filesystem references. See GitHub’s [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) for the hosting contract. Actions are pinned to official repository commits verified October 29, 2026.

## Media and scope

All 28 rollout films were observed available on October 29. The collection also includes two earlier films, Sizzle’s reel, Taste’s lesson and Decisioncraft’s visual demo. Their formats are labeled individually. Media availability does not establish creative acceptance or capability effectiveness.

[Media provenance and observation notes](docs/MEDIA.md) distinguish direct URL checks from the producer’s report. [Content notes](docs/CONTENT.md) explain the catalogue’s scope. Site source is MIT licensed; existing film artwork and media retain the notices of their original repositories.
