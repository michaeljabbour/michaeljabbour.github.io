# Local validation

Recorded 2026-10-28. These are actual packaging and native software/source checks, not comparative usefulness evidence.

## Six native integrity tool suites

Status: **passed**.

`For each modules/tool-experiment-*/: PYTHONPATH=<module>/src python -m pytest <module>/tests -q`

174 tests: audit 50; block hypothesis 22; power 40; provenance 19; resume 14; stage analyzer 29. Isolated Python 3.12.11 with recorded test dependencies. No new empirical study or live model comparison.

## Autonomous experiment-loop shell checks

Status: **passed**.

`For each scripts/experiment-loop/tests/test_*.sh: bash <test>`

10 shell checks passed, including the isolated three-row keep/revert/promotion smoke loop; no new empirical result.

## Portable packaging and install

Status: **passed**.

`python3 scripts/capability.py build; python3 scripts/capability.py check; python3 scripts/capability.py doctor; python3 scripts/capability.py install --dest <temporary-parent> (twice)`

All operations passed. No runtime activation or effectiveness measured.

## Skill discovery metadata

Status: **passed**.

`<yaml-enabled-python> /path/to/skill-creator/scripts/quick_validate.py skills/research`

Skill is valid. This is a structural check, not a behavioral benchmark.

The [dated machine-readable record](evaluations/2026-10-28/consolidation.json) retains source revisions, check scope, and limitations. Native runtime gates stay separate from installation. No public repository, current service, user installation, or personal source checkout was changed.
