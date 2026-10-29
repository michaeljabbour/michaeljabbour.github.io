# Michael Jabbour

A portfolio of AI skills, tools and libraries for work people can build on.

The site introduces the work, groups 33 public capabilities by the task they support, and gives each its own page with media, a first step, installation and source. Films stay hosted on their capability sites; this repository keeps lightweight copies of the existing poster artwork.

## Build and preview

Requires Python 3.10+ and Node.js for the JavaScript syntax check. The site itself has no runtime dependencies, external fonts, analytics or backend.

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check assets/site.js
python3 -m http.server 8781 --directory dist
```

Open `http://localhost:8781/`. The build writes `dist/`, which is the deployment artifact. All routes use the root of `michaeljabbour.github.io`; preview the site at a server root, not a repository subpath.

## Content

- `content/portfolio.json`: owner introduction, seven task categories and 33 capability entries.
- `content/media.json`: verified media destinations, local poster paths and observation scope.
- `assets/`: site styling, behavior and poster artwork.
- `scripts/build.py`: generates the homepage, library, films, About, 33 detail pages, 404 and sitemap.
- `scripts/check.py`: checks routes, metadata, assets, media consistency and public-only content.
- `DESIGN.md`: design direction and rationale.

Edit the catalogue to change copy or related capabilities. Keep intended functions distinct from proven outcomes. Fictional outputs are labeled. Preserve each capability’s actual installation anchor, meaningful prerequisites and limits.

[Add the portfolio overview film](docs/OVERVIEW-FILM.md) when its final assets are ready. The build supports it without displaying an unfinished player.

## GitHub Pages

The intended repository is `michaeljabbour/michaeljabbour.github.io`, with GitHub Pages configured to use GitHub Actions. `.github/workflows/pages.yml` builds and checks pull requests, then publishes reviewed changes on `main`. The workflow is prepared locally; repository creation, remote setup and the first publication are separate actions.

It uploads only `dist/`. The public site contains no private audit, owner workbook, research records or local filesystem references. See GitHub’s [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) for the hosting contract. Actions are pinned to official repository commits verified October 29, 2026.

## Media and scope

All 28 rollout films were observed available on October 29. The collection also includes two earlier films, Sizzle’s reel, Taste’s lesson and Decisioncraft’s visual demo. Their formats are labeled individually. Media availability does not establish creative acceptance or capability effectiveness.

[Media provenance and observation notes](docs/MEDIA.md) distinguish direct URL checks from the producer’s report. [Content notes](docs/CONTENT.md) explain the catalogue’s scope. Site source is MIT licensed; existing film artwork and media retain the notices of their original repositories.
