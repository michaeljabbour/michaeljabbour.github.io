# Local validation

Recorded 2026-10-28. Installation, source coverage, native software behavior, and user benefit are separate.

## Canonical reference mirror gate

**passed** — AI setup, Bundle Authoring, and Registry mirrors match canonical sources plus their recorded source/output hashes.

`python3 scripts/sync_skill.py --check`

## Retained documentation checks

**passed** — 47 Node tests and 59 Python tests pass. These verify documentation coverage only; no Torque framework/runtime or app deployment result is claimed.

`node --test test/docs.test.js; python -m pytest test/test_phase3_docs.py test/test_phase4_docs.py -q`

## Portable build and clean install

**passed** — Canonical ZIP bytes, local links, complete method/license, clean install and idempotent reinstall pass. No runtime starts.

`python3 scripts/capability.py build/check/doctor; install --dest <temporary-parent> twice`

The [dated record](evaluations/2026-10-28/consolidation.json) records the scope. No new paid generation, framework deployment, remote publication, or outside-user outcome is claimed.
