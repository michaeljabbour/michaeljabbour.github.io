# Michael Jabbour

A portfolio of AI skills, tools and libraries for work people can build on.

The site introduces the work, groups public capabilities by the task they support, and gives each its own page with media, a first step, installation and source. Films stay hosted on their capability sites; this repository keeps lightweight copies of the existing poster artwork.

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

- `content/portfolio.json`: owner introduction, seven task categories and capability entries.
- `content/journey.json`: the seven human questions, their order, outcomes, tool selections and actual film chapter times.
- `content/media.json`: verified media destinations, local poster paths and observation scope.
- `assets/`: site styling, behavior and poster artwork.
- `scripts/build.py`: generates the homepage, journey, library, films, About, capability detail pages, 404 and sitemap.
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

The grouped catalogue keeps capabilities distinct. The proposed knowledge journey is separate from the build journey. Writing and notes are on [Michael Jabbour’s blog](https://www.michaeljabbour.com/).

The shared installer lives in `tools/` and is served at `/reports/capability-installer/`. Its download manifest records the exact committed source revision and file hashes. For local editing, prefix build/check commands with `CAPABILITY_INSTALLER_PREVIEW=1`; commit before a production build.

Run `python3 -m unittest discover -s tests -v` and `python3 -m unittest discover -s tools -p test_capability.py -v` before building.

## Additional capabilities and local preview

`content/additions.json` uses version 2 to admit the six owner-approved additions: ArticleCraft, Idea Talks, Stories, Claim Review, Delivery Packager and Guided Practice alongside the original catalogue. Version 1 remains valid for the first three writing additions only. The manifest records their canonical repositories, exact source commits and repository verification. The historical migration map continues to describe only the original 33 repository renames. New capabilities do not acquire invented legacy names.

Until those repositories and pins have been verified, render a private local preview explicitly:

```sh
PORTFOLIO_PREVIEW=1 CAPABILITY_INSTALLER_PREVIEW=1 python3 scripts/build.py
PORTFOLIO_PREVIEW=1 CAPABILITY_INSTALLER_PREVIEW=1 python3 scripts/check.py
```

Preview flags cannot authorize a public build in GitHub Actions. Public publication requires committed source, verified addition records and a matching artifact receipt:

```sh
python3 scripts/check_release.py --for-publication
```

The workflow checks that boundary before upload and binds deployment to the guard's source SHA and ready output. Review the actual public repository/head evidence before marking an addition verified; changing a flag is not evidence that a repository exists.

## Flow and stage navigation

`content/flows.json` uses `capability-flows/v2`: three work flows, their six optional browsing stages and explicit per-capability assignments. A capability can have several tags or stages while keeping one card and one detail route. Stages filter the same list; they do not execute a recipe or require an order.

The homepage and library use the same flow/stage/search state. For example, `/?flow=software&stage=test#journey` and `/capabilities/?flow=creative&stage=make` can be bookmarked. “All stages” retains the current flow. Legacy category and film chapter URLs remain supported. `dist/flows.json` exports the reviewed navigation data.
