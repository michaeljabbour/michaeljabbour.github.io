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

The target repository is `michaeljabbour/michaeljabbour.github.io`, with GitHub Pages configured to use GitHub Actions. `.github/workflows/pages.yml` builds and checks pull requests, then publishes reviewed changes on `main`. The public repository uses GitHub Actions for Pages. The workflow checks the build before publishing the static artifact from `main`.

- Portfolio: [michaeljabbour.github.io](https://michaeljabbour.github.io/)
- Source: [michaeljabbour/michaeljabbour.github.io](https://github.com/michaeljabbour/michaeljabbour.github.io)

It uploads only `dist/`. See GitHub’s [custom Pages workflow guide](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) for the hosting contract.

## Media

Films stay on their capability sites. Local posters and stills preserve the supplied artwork. Captions, transcripts and short cuts appear where available. [Media notes](docs/MEDIA.md) describe the assets; [content notes](docs/CONTENT.md) describe the catalogue. Site source is MIT licensed; media retain their original notices.

## Navigation and shared installation

The grouped catalogue keeps 33 capabilities distinct. The proposed knowledge journey is separate from the build journey. Writing and notes are on [Michael Jabbour’s blog](https://www.michaeljabbour.com/).

The shared installer lives in `tools/` and is served at `/reports/capability-installer/`. Its download manifest records the exact committed source revision and file hashes. For local editing, prefix build/check commands with `CAPABILITY_INSTALLER_PREVIEW=1`; commit before a production build.

Run `python3 -m unittest discover -s tests -v` and `python3 -m unittest discover -s tools -p test_capability.py -v` before building.
