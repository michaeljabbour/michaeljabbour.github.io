# Arithmetic regression record — 2026-10-28

**Observed model-authored ceilings failed; a deterministic check now rejects them.** This is a local regression record, not a Right Shape behavioral benchmark pass.

The retained numeric [observations](observed-failures.json) came from two earlier delegated application cards. One listed no failed gates but reported ceiling 6. The other listed all six failed gates but reported ceiling 1. Both failed the recorded canonical ceiling check. The original application records were not rewritten or converted into passing runs.

The portable validator and site now import one parser of the canonical rubric. The validator rejects false claimed sums, mapped need rungs and ceilings, as well as a placement above the computed maximum. It also rejects duplicate composition IDs, and reports that H4 alone calls for decomposition. No gate truth is inferred: an unsupported passing judgment can still be wrong even if its arithmetic is right.

Local tests include both observed failures, a mixed-cap counterexample, composition that attempts to exceed a cap, all 256 need vectors against all 64 gate subsets, invalid values, explicit lower-rung reasoning and a CLI run from a copied standalone folder. Test execution is recorded in the working-tree validation report when complete.

This verifies arithmetic and portable execution only. It does not establish that an LLM judges gates correctly, that the Audit method improves a portfolio, or that the skill is useful to outside users. The full controlled benchmark remains a plan.
