# Static portfolio checks

Run from the repository after building:

```sh
python3 scripts/build.py
python3 scripts/check.py
```

The checker uses the Python standard library and makes no network calls. It checks the generated public output against the reviewed content and media catalogues rather than treating a successful build as sufficient.

## Recorded result — October 29, 2026

The built portfolio passed with:

- 38 HTML pages, including all 33 unique capability routes, four content index pages and the 404 page.
- Seven work categories and 33 projects exposed in the library before JavaScript runs.
- 759 local references and 37 distinct local assets checked for existence; local fragments are checked against actual element IDs.
- 33 media players and 32 supplied caption tracks matched to `content/media.json`. The Decisioncraft demo has no supplied caption track in that record.
- Matching video source, poster, transcript, short-cut and capability-site destinations where supplied.
- Page titles, descriptions, canonical routes, language, page headings, unique IDs and main landmarks checked.
- Reviewed first-use text, appropriate native first-step labeling, source links and installation links present.
- Public catalogue equality and exact 37-route sitemap coverage checked.
- No unconfigured homepage film player. When `content/home-film.json` supplies a source, the checker requires one matching overview player, poster and English caption track, and the configured transcript link if supplied; local assets join the normal existence checks.
- No autoplay, unresolved build token, excluded-project marker, owner-workspace path or bounded credential-pattern match found in the 45 public text files scanned. Potential credential values are suppressed in error output.

The checker was also challenged with five deliberately broken copies of the output in a temporary directory. It rejected a missing local route, a missing fragment, an autoplay player, a removed provided caption track and a private workspace path. The real build output was unchanged by those negative controls. An additional temporary static fixture accepted a configured homepage overview and rejected the same configuration without its required caption. That fixture validates the checker’s output/configuration contract, not media encoding or playback.

## Scope

This is static output validation. It does not establish visual quality, filter interaction behavior, screen-reader usability, browser playback, caption timing, provider acceptance, native capability execution or usefulness to an outside user. Browser verification is recorded separately.

Media URL availability comes from the dated public observations in `content/media.json`; this checker preserves consistency with that record without re-requesting every external file. Public installation fragments were independently read from the destination HTML while preparing the catalogue. Neither record implies that all external destinations stay unchanged indefinitely.

The credential scan checks recognizable token and private-key patterns, not every possible form of secret or personal information. Public output is deliberately assembled from a small reviewed catalogue and local artwork rather than exporting the private owner workbook.
