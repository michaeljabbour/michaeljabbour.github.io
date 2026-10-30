# Local validation — 2026-10-28

**Publication update, October 28, 2026:** The [public source](https://github.com/michaeljabbour/amplifier-skill-project-handoff) and [live site](https://michaeljabbour.github.io/amplifier-skill-project-handoff/) are released. Fresh anonymous source installation and the live four-file ZIP were verified. The sections below retain the earlier local validation scope and study limits; they do not describe the current publication state. No study result or frozen input changed for publication.


The initial evaluation built Project Handoff locally. At that stage it had not been pushed or published. It was not installed globally or used by an outside user in the evaluation.

## Portable package

- The build and repository checks passed: one canonical skill, resolved relative references, byte-matched raw download and ZIP, fictional examples, local assets, theme notice and reduced-motion support.
- A clean temporary skills directory installed exactly four files: `project-handoff/SKILL.md`, `LICENSE.md`, `references/method.md` and `references/handoff-contract.md`. Check mode passed and every ZIP member matched the installed bytes. Provider-key, token and Memory environment variables were removed for this test. No Amplifier package, Memory service or database was used.
- The 21 unit tests passed, covering the installer and evaluation machinery. These are code checks, not evidence of improved handoffs.
- JavaScript syntax validation passed. The desktop and phone preview showed no horizontal document overflow at effective CSS widths of 1309 and 354 pixels. Example switching and both incorrect/correct answer feedback worked. Keyboard and final benchmark-panel checks are recorded in the final verification below.
- The optional Amplifier recipe validated through the local `recipes` tool. The surrounding host emitted cache/editable-install warnings; full approval/save execution was not tested. See [AMPLIFIER.md](AMPLIFIER.md).

## Behavioral study

[study-1](evaluations/2026-10-28/study-1/REPORT.md) completed 60 transfer trials and 180 provider calls across ten fictional projects, three conditions and two repetitions. Capture used the treatment; a separate neutral resumer received the resulting handoff and retained files. Direct effects of the Resume and Check method were not tested. No real model tools executed.

The automated judge recorded correct resumption in 20/20 skill, 20/20 baseline and 17/20 placebo trials. The placebo condition had two recorded critical failures and one ungraded trial; the latter remains in its denominator. The skill-versus-baseline difference was zero. The frozen interpretation is: **no effectiveness conclusion**. These automatic scores are provisional evidence, not accepted human labels.

[Pilot semantic review](evaluations/2026-10-28/pilot-3/SEMANTIC-SPOT-REVIEW.md) identified overgenerous correctness judgments: a pending test was treated as evidence of missing parser functionality in all three conditions. The [secondary coding-agent study review](evaluations/2026-10-28/study-1/STUDY-QUALITY-REVIEW.md) covered 17 trials across all ten fixtures. It disputes both automatic critical-execution labels, finds unsupported statements in some passing skill records, and retains the invalid judgment. It is not a human-user study or fully independent blinded adjudication. The apparent placebo deficit cannot support a benefit claim. The review verified that all 312 retained source/raw/result files stayed unchanged. Nothing was rerolled or silently regraded to obtain a favorable result. Failed instrument-development pilots remain available.

The main study's nominal uncached token cost was USD 0.7910956, not an invoice. No time saved, user adoption, return use or persistent learning was measured.

## Right Shape application tests

The sibling Right Shape skill and canonical rubric were supplied unchanged to independent model calls. Both the actual design and an explicitly fictional unsafe, Memory-dependent variant were tested. Initial calls made scoring, gate-ceiling and composition errors; a second attempt also exposed a local review-parser defect. The structured third record still failed canonical gate-ceiling checks. These are retained failures, not passing tests or evidence of Right Shape efficacy.

The supported design is a caller-applied skill for a bounded handoff. The installer and distribution bundle are packaging; the optional recipe does not turn the method into an autonomous agent. Runtime isolation, model budgets and control of outbound channels depend on the host and cannot be guaranteed by portable prose. The unsafe variant is rejected. See [RIGHT-SHAPE-REVIEW.md](RIGHT-SHAPE-REVIEW.md) for the application record and adjudication.

## Final verification

The final site displays the provisional three-condition table, disputed critical flags, invalid judgment, descriptive intervals, source records and quality review. It makes no benefit or safety claim. The results table fits inside a horizontally scrollable phone region rather than expanding the document; the region has a visible keyboard focus outline, an accessible label and working ArrowRight scrolling. At an effective phone width of 354 pixels, document width remained 354 and keyboard scrolling revealed additional results columns. The desktop layout also passed the geometry check. Example switching and incorrect/correct answer feedback were verified in the browser; the report reader's disclosures also open with Enter.

Final build, repository/link checks and JavaScript syntax checks passed: 28 local page links/assets/fragments, 47 shipped Markdown links and a byte-matched four-file ZIP. The selected study export preserved all 317 files byte for byte. All 14 frozen main-study input hashes still match the run manifest. A value-safe scan of the source and evaluation records found no high-confidence API-token/private-key signatures; this is a scoped pattern check, not a general security certification.

The reviewer helper now refuses unpriced provider/model pairs before creating a run or calling a provider, and reserves cost at each supported model's documented rates. Its rejection path was checked without another paid review. The prior recorded application outputs remain unchanged.

The sibling Right Shape checkout remained clean. Browser sizing overrides were removed after inspection. The initial delivery was a local checkout; public source and site verification were completed afterward at the links above. Global host installation and outside-user acceptance remain separate.
