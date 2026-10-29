# Browser checks — October 29, 2026

The static site was checked in the in-app browser at its local preview. The measurements below are observed CSS viewport widths, rather than requested window dimensions.

- Home/header/hero: 291px, 354px, 962px and 1309px. Document width equaled viewport width at each measurement. The revised heading, both calls to action and navigation fit.
- Films and demos: 33 correctly labeled entries at 354px; no autoplay. Decisioncraft is identified as a visual demo without a supplied caption track.
- Library: search for “handoff” returned one capability. An unmatched query showed the recovery action; resetting restored the collection. The continuation category returned five capabilities, and its Skill format intersection returned three. Filter state appeared in the URL and survived a reload.
- Detail: Project Handoff’s source/install/transcript/short-cut destinations, stated independence from Memory and first-use guidance were visible. The copy control placed the exact starter text on the clipboard and announced completion.
- Detail on phone: Cognitive Simulation’s long title, media, first-step/source links and reading layout fit at 354px. Its existing embedded film loaded and advanced with native controls, readyState 4 and no media error. This was a playback smoke check, not audio, pronunciation, caption-timing or creative acceptance.
- Revised home footer: the closing invitation and footer were inspected at 354px. The repeated formal self-introduction was absent. The final temporary viewport override was reset.

An independent reviewer viewed the correctly sized revised hero screenshots and found no visible clipping or overlap. Initial full-page browser captures were narrower than the measured viewport; normal viewport captures matched the CSS width and were used for the final visual review. Image lazy loading can leave offscreen artwork empty in an immediate full-page capture; the public assets are checked separately for existence.

The checks cover these observed flows and layouts. They do not constitute a complete assistive-technology or cross-browser audit, and do not establish usefulness or native runtime acceptance for the linked capabilities.

## Homepage category discovery — October 29, 2026

Fresh normal and query-varied live HTTP responses both contained the seven journey stages. The user could not find them, and inspection showed the full hero/player and guide introduction put the category tabs below the first screen. This establishes a discoverability issue; it does not diagnose the user's existing tab cache.

The homepage now places seven native category links directly under the header, before the hero. At 1280px all seven appear in a single row. At 390px and 320px they wrap into two columns; the category area ends at 421px and 444px respectively, inside the first screen. Document width equals viewport width. The fifth link opens Create and the sixth opens Adapt with the correct selected journey panel. The full guide and existing library remain available.

The live host sends a ten-minute cache lifetime for HTML, CSS and JavaScript. Shared page asset links now include a content hash so a newly loaded page requests its matching style and behavior. This does not force-reload an already open document.
