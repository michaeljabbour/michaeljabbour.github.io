# Journey browser checks — October 29, 2026

Observed in the local in-app browser:

- Home and the dedicated journey page expose the same seven moments. Next from Improve reaches Create, then Adapt, then Continue. Adapt contains Migrate, Transfer and Pipeline, with no invented film chapter.
- One stage panel is visible at a time after enhancement. Native Home/End/ArrowLeft tab keys move focus and selection correctly: first, last, then Adapt at sixth. Previous is disabled at the first moment.
- Continue’s “Start with a new question” returns to Understand. Browser Back and Forward restore the prior and next selected stage. A reload preserves a stage deep link.
- Migrate’s detail page identifies its sixth-stage context, links back to it, and offers Create before it and Continue after it.
- A Create chapter link navigates to the homepage, selects Create and positions the overview at 51.08 seconds, paused. The native player and status both confirm the actual position.
- Initial chapter testing exposed the basic local server’s lack of byte-range support: it buffered only the opening and could not seek ahead. The replacement read-only preview helper returns valid partial content, and the same browser test then succeeds. Successful status is only announced after the seek completes.
- The preview helper returned exact bytes and HTTP 206 for beginning, middle and suffix ranges, and HTTP 416 for a range outside the file.
- Journey and Migrate layouts had document width equal to the viewport at 390px; the journey also fit 320px. Temporary viewport overrides are reset after checking.

Static checks, including all 33 memberships, six narration cue bindings, no-JS panels and all page links, are recorded separately in `QA-JOURNEY-STATIC.md`. This is a local UI/playback check, not a re-review of the film’s audio or creative quality, a formal design-method certification or a public deployment.
