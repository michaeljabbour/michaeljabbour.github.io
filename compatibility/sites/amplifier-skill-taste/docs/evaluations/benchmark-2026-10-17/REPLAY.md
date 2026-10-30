# Replaying and reviewing this benchmark

Run the deterministic code checks from the repository root:

```sh
python3 docs/evaluations/benchmark-2026-10-17/replay_checks.py
```

To rerun task behavior, start a new agent for each selected manifest entry without prior conversation history. Give it that entry's exact user prompt and the frozen skill/reference for skill conditions; for controls, do not provide skill files. Use a new isolated output directory and fresh fixtures, rather than overwriting archived evidence. The public task wrappers under runs/ are privacy-normalized historical copies: the original personal checkout prefix is the literal `<benchmark-checkout>`. Historical suffixes and all task substance remain unchanged; substitute the new sandbox and snapshot paths and record that substitution. See [PUBLIC-PROVENANCE.json](PUBLIC-PROVENANCE.json) for the original and public-copy hashes. Some historical suffixes predate the frozen file rename to `SKILL.snapshot.md`. Start X02 from stress-fixtures/, whose working.py is the original failing proposal, not the already-restored runs/X02-skill/working.py.

Do not expose checks, condition keys, prior responses or reviewer judgments to task runners. Use the supplied four common and case-specific checks for grading. Start fresh independent grading agents with opaque response IDs. Preserve raw judgments before adjudication. Historical masked packets, responses and judgments are unchanged. Original wrapper bytes remain in Git history and an owner-local backup; the published wrappers are explicitly normalized copies, not raw byte-identical execution logs. Resolve packet filenames in their archive folder for a new run.

This suite is now known to the skill maintainer. A revision tested on its failures is a regression test, not a held-out generalization test. Add and freeze genuinely new short-refinement cases before testing that revision, and report original, revised and held-out results separately.
