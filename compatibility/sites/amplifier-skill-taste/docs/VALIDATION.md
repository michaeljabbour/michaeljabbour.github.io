# Local validation

Validation date: 2026-10-16. The preview used the user's local Microsoft Edge
browser, not a separately launched headless browser. This section records the
initial local checks before the later authorized public release.

## Build and file integrity

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check site/site.js
```

The integrity checker covers local HTML links and fragments, shipped Markdown
destinations, unique IDs, local CSS dependencies, the source textarea, both
canonical Markdown files, and the ZIP bundle. The source and reference in the
bundle match the local skill files byte for byte. The page reads its full anchors
and eight calibration questions directly from those files at build time.

## Browser observations

- Example selection updated the brief, proposal, map description, and points.
  The examples include gentle refinement, a conceptual jump, and reframing followed
  by refinement. Positions and paths are explicitly fictional conversation aids.
- Enter activated the baseline control, updated its pressed state and description,
  and hid the proposed point and path. Space activated the proposed view.
- Enter opened the verification disclosure. Its risk, verification method, and
  growth action were visible in the accessibility tree.
- Navigation reached the map and skill sections. The source link opened the
  disclosure and exposed the read-only canonical text.
- Prompt and skill copy controls reported success after activation. An additional
  attempt to verify the operating-system clipboard through developer tooling timed
  out; exact system clipboard contents are therefore not claimed as verified.
  The copied input's source fidelity is checked independently by the build check.
- Both real browser download actions completed. The downloaded Markdown and both
  ZIP entries matched the source files byte for byte at the time of that check.
  Subsequent skill wording refinements are covered by the final bundle integrity check.
- Layout inspection covered 320 × 800, 390 × 844, 768 × 1024, and the default
  1384 × 1119 viewport. Document width matched viewport width in each case.
  The phone and tablet map stacks above its controls. Graph paths were adjusted to
  clear quadrant headings. Temporary viewport overrides were reset after testing.

These checks are an implementation review, not user research or a comprehensive
accessibility certification. No screen-reader session, independent usability study,
or cross-browser suite was performed. Reduced-motion rules and a no-JavaScript
text fallback were inspected in source; their browser settings were not changed.

## Screenshots

The images contain only the local product page. They exclude browser tabs,
addresses, desktop content, and private files. They record layout checks during
implementation; later wording refinements may differ from those views.

- [Desktop map](screenshots/desktop-map.jpg)
- [Phone map](screenshots/phone-map.jpg)
- [Narrow phone map](screenshots/narrow-map.jpg)
- [Tablet map](screenshots/tablet-map.jpg)

The illustrative graph does not prove improvement. Real use still requires the
person's experience and reasoning, a shared brief, gate checks, evidence,
confidence, and a deliberate decision about what to retain.

## Upload privacy review

The 26 proposed source, documentation, and asset files passed a credential and
private-data pattern scan and an independent content review. All four screenshots
were inspected and contain only the product page; no EXIF, XMP, or IPTC metadata
was detected. Generated output, terminal logs, download test copies, and local
configuration are excluded from Git. Only the family CSS and its MIT notice were
copied from the reference. A single initial commit uses a generic project
contributor identity with a non-personal noreply address. No prior commit history
is imported. The initial repository upload was private. The later public release
was explicitly authorized, and adds the Pages workflow and publication
documentation to the same reviewed source.
