# Local validation

Recorded 2026-10-28. These are actual packaging and native software/source checks, not comparative usefulness evidence.

## Native host unit suite

Status: **passed**.

`<configured-amplifier-python> -m unittest discover -s tests -v`

693 tests passed after the local-discovery correction; fake/isolated services and Foundation composition. No current project enrollment or provider inference.

## Isolated native bundle validation

Status: **passed**.

`<configured-amplifier-python> scripts/validate_bundle.py`

Root/self-include schema; local composition retaining provider/session; local module preparation; empty replay. No provider call, enrollment, remote Foundation include, or cache reuse.

## Portable packaging and install

Status: **passed**.

`python3 scripts/capability.py build; python3 scripts/capability.py check; python3 scripts/capability.py doctor; python3 scripts/capability.py install --dest <temporary-parent> (twice)`

All operations passed. No runtime activation or effectiveness measured.

## Skill discovery metadata

Status: **passed**.

`<yaml-enabled-python> /path/to/skill-creator/scripts/quick_validate.py skills/good-teammate`

Skill is valid. This is a structural check, not a behavioral benchmark.

The original native validation history and its limits are preserved in [NATIVE-VALIDATION.md](NATIVE-VALIDATION.md).

The [dated machine-readable record](evaluations/2026-10-28/consolidation.json) retains source revisions, check scope, and limitations. Native runtime gates stay separate from installation. No public repository, current service, user installation, or personal source checkout was changed.

## Local canonical skill configuration

The explicit local materializer emits a YAML behavior pointing at the actual checkout’s method and native module paths. Actual Foundation loading/validation and two configuration plus two guidance tests pass; no activation or provider/session replacement occurs. The original Git self-source remains the release-compatibility path. A composition-only check had missed the older loader’s lack of namespace source resolution; this was corrected before publication.
