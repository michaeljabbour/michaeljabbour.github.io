# Working on the portfolio

- The public catalogue is `content/portfolio.json`; media destinations are `content/media.json`. Keep all 33 capabilities distinct unless the owner changes the scope.
- Keep private audit records, local paths, credentials, customer claims and invented results out of the public source and `dist/`.
- Preserve real film artwork and media. Do not revoice, crop, render or generate film assets as part of a site change.
- Use plain language, visible labels, keyboard controls, reduced-motion support and native captioned media controls.
- Build with `python3 scripts/build.py`, check with `python3 scripts/check.py` and `node --check assets/site.js`. Inspect desktop and phone layouts after UI edits.
- The generated `dist/` directory is the only Pages artifact. Root paths target `michaeljabbour.github.io`.
- Keep the site free of backend services, analytics and runtime dependencies. Never add an unfinished media player as a placeholder.
