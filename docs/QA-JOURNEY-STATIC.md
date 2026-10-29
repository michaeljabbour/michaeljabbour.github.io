# Journey structure checks

The public guide connects a sequence of human questions to the tools that fit each part of the work. The source for its stages and story moments is `content/journey.json`.

Run after building:

```sh
python3 scripts/build.py
python3 scripts/check.py
```

The checker uses the standard library and makes no network calls. Its journey checks cover:

- The seven agreed stages in both the journey and catalogue, with visibility before adaptation and continuation last. Stable IDs keep Make it visible at 5, Take it somewhere new at 6 and Pick it up again at 7.
- Complete category coverage and valid suggested starting tools within each stage.
- Meaningful question, description, output and reflection fields.
- Exactly six positive, distinct story timestamps in sequence, bound to the actual meaning of their overview-caption cues. A timestamp merely pointing to some other real line does not pass. Adaptation must keep a null timestamp and receive no invented chapter link.
- Public `journey.json` equality with the reviewed source.
- One complete guide on the homepage and one on `/journey/`, with stage links, anchors and panels in source order.
- All 33 capability links exactly once per guide, within their actual catalogue category, and pointing to the corresponding detail page.
- The human question and expected output visible within each stage panel.
- Accessible stage-heading bindings, panels available before JavaScript runs, and labeled previous/next controls that wait for enhancement.
- Exact capability names on guide links, so a correct ID and destination cannot silently carry another tool’s name.
- Story links carrying the matching stage/time and pointing to the homepage’s story anchor.
- Readable chapter times within one second of their actual destinations.
- A journey-stage destination on each capability detail page.
- The new route in the sitemap, while preserving the existing media, installation, source, privacy and no-autoplay checks.

## Recorded result — October 29, 2026

The real build passes:

- 40 HTML pages: 38 public content routes, the 404 page and the supplied overview transcript.
- Seven categories, 33 capability pages and two complete journey guides.
- 66 journey-tool links: all 33 capabilities exactly once on the homepage guide and once on the dedicated guide.
- 12 story-chapter links: six actual narrated moments on each guide, with adaptation omitted from timed chapters.
- 1,026 local references and 40 local assets checked.
- 33 capability players, one supplied overview player and 32 provided capability-caption tracks preserved.
- 48 public text files checked for private markers and bounded credential patterns; no network calls.

Fourteen deliberately broken copies of the build were tested in isolated temporary folders. Every case was rejected for its relevant defect:

1. Swapping Create and Adapt in stage navigation.
2. Swapping their panels.
3. Giving the catalogue a different category order.
4. Moving a correctly named tool into the wrong stage.
5. Duplicating a tool instead of covering all 33 once.
6. Displaying another capability’s name on a tool link.
7. Pointing a stage link at a missing fragment.
8. Binding a panel to another stage’s question heading.
9. Hiding a stage before JavaScript runs.
10. Pointing a chapter at a real caption cue with the wrong meaning.
11. Assigning an invented Adapt chapter.
12. Showing a chapter time that differs from its destination.
13. Removing the previous-moment control.
14. Linking a capability detail page to a different primary stage.

The unmodified temporary baseline passed before those controls, and the real output was unchanged by them. A fresh check of the real build also passed afterward.

The narrated-opening mapping in `scripts/check.py` is intentionally independent of the renderer’s input data. If the supplied narration changes, review the meaning and timing of its six moments together rather than weakening this check to accept any existing cue.

These checks validate the output’s semantics and relationships. They do not prove usability, browser interaction behavior, caption timing, film highlight timing or effectiveness of the linked capabilities. Browser inspection is separate. The overview film and its narration are preserved; the guide’s order is not a claim that its existing board animation was repaired.
