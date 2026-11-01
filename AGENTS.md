# Working on the portfolio

- `content/flows.json` (v2) owns the three overlapping public work filters and their optional stage memberships. Each catalogue capability has one card and one detail route; membership can overlap. Preserve legacy category fragments in that shared view.
- `content/related-tools.json` contains only reviewed, public source comparisons. Do not copy private `.research/market` notes. Keep direct sources, meaningful distinctions and review dates. Empty lists remain explicitly unpublished.
- `content/journey.json` owns the legacy journey order and narration timings. Match its stage IDs across navigation, chapters, catalogue categories and capability context. Do not invent a narrated adaptation timestamp.
- The public catalogue is `content/portfolio.json`; media destinations are `content/media.json`. Keep all catalogue capabilities distinct. `content/additions.json` admits only the three owner-approved additions; never invent older repository aliases or include unreviewed local projects.
- Keep private audit records, local paths, credentials, customer claims and invented results out of the public source and `dist/`.
- Preserve real film artwork and media. Do not revoice, crop, render or generate film assets as part of a site change.
- Use plain language, visible labels, keyboard controls, reduced-motion support and native captioned media controls.
- Build with `python3 scripts/build.py`, check with `python3 scripts/check.py` and `node --check assets/site.js`. Inspect desktop and phone layouts after UI edits.
- The generated `dist/` directory is the only Pages artifact. Root paths target `michaeljabbour.github.io`.
- Keep the site free of backend services, analytics and runtime dependencies. Never add an unfinished media player as a placeholder.

- Use `python3 scripts/serve.py` for local preview with seekable video. The helper binds only to loopback and is not part of the deployed static artifact.

- `content/knowledge-journey.json` is a separate, explicitly proposed navigation through existing public capabilities. It has no narration timestamps and does not change the seven-stage build journey. Keep research and review records outside the public source. The public pages introduce capabilities and link to the blog.

- Public activation of additions requires real repository/head verification and a clean `check_release.py --for-publication` result. Local preview flags must never enter CI or authorize deployment. Keep the historical migration map at its exact original 33 identity/pair set.

- Show only the selected flow’s stage row, filter one shared card list and preserve flow/stage/search URL state. “All stages” keeps the flow. Stage membership describes a useful place for the capability, not an automated pipeline or proof of quality.
