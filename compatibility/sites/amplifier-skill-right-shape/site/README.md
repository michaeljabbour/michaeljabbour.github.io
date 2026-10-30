# Website

This page follows the Amplifier Smart Tools family's static Python build, visual
language, two-column hero, local assets, fine rules, and restrained navigation.
The generated `_site/` directory works on any static host, including a repository
subpath on GitHub Pages. All product links are relative or page anchors.
`.github/workflows/pages.yml` builds, checks, and publishes `_site/` from `main`.

## Build and preview

From the repository root with Python 3.11 or later:

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open `http://127.0.0.1:8000`. The build uses only Python's standard library.

## Edit

- `site.json`: metadata and explicitly fictional placements. The build recomputes each
  placement from the rubric (need bands, gate caps, shape checks) and refuses one whose
  rung is above min(need, ceiling), drops lower without a stated tiebreak, or omits an
  honest move when need exceeds the ceiling.
- `template.html`: semantic page content and layout.
- `style.css`: product styles and responsive behavior on top of the family theme.
- `site.js`: switching placements, the rubric calculator, and copy feedback. The
  calculator reads its bands, caps and labels from attributes the build writes from
  the rubric. Every placement is rendered at build time, so the page reads without
  JavaScript.
- `assets/`: original SVG favicon and share illustration.
- `../skills/right-shape/references/rubric.md` and `../docs/BENCHMARK.md`: the source
  for the questions, shapes, ladder, need scales, gates, checks, engines, contract,
  dispositions, diagnosis and benchmark rows. Do not fork the method into another
  content file.

The portable ZIP also includes the conditional Audit reference, MIT notice and optional arithmetic validator. The builder imports the same validator/parser, so there is no second set of gate values.

## Theme provenance

`theme/style.css` is an unmodified snapshot of the Amplifier Smart Tools family theme
v0.1.0. `theme/LICENSE` keeps its original MIT notice. The product template, ladder,
calculator, SVG assets and styles are new.

## Design notes

- Paper `#f6f4ee`, ink `#252823`, muted `#64685e`, rules `#d8d8cc`, gold `#80642f`
  from the family; indigo accent `#574a78` for this skill, and a brick red for the
  ceiling line.
- Georgia headings and Arial body, system fallbacks, no font requests.
- The ladder is the one expressive element: the placed rung filled, what the job
  wants dashed in gold, rungs above the ceiling greyed.
- No automatic movement. Reduced motion is respected.

## Deployment

The Pages source is GitHub Actions. The workflow separates build and deployment,
checks the output before upload, and uploads only `_site/`. Keep asset, navigation,
and download paths relative so repository-subpath hosting works.
