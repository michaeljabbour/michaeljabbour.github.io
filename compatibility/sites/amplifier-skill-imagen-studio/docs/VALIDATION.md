# Local validation

Recorded 2026-10-28. Installation, source coverage, native software behavior, and user benefit are separate.

## Native adapter regression suite

**passed** — 36 passed, 1 opt-in checkout-contract test skipped; 85.33% line coverage. Provider-free MCP lifecycle, discovery, schema, timeout, error and cleanup tests.

`python -m pytest -q -p pytest_asyncio.plugin -p pytest_cov.plugin --cov=amplifier_module_tool_imagen --cov-fail-under=80 modules/tool-imagen/tests (plugin autoload disabled)`

## Retained deterministic policy record

**passed** — Exact July result reproduces: 5/5 typed policy cases, 5/5 unsafe mutations rejected. All seven bound apparatus files and dated result unchanged. This is deterministic fixture evidence, not stochastic-model effectiveness.

`python scripts/run_behavioral_evals.py --verify evals/results/2026-07-13.json`

## Native and portable workflow checks

**passed** — Static 5 YAML/1 canonical skill/12 scenarios; 6 tests pass, including local behavior and synthetic image→ASCII/HTML→PNG. No generation or real-user visual acceptance.

`python scripts/validate_bundle.py; python -m pytest -q -p pytest_asyncio.plugin evals/test_behavioral_harness.py tests (plugin autoload disabled)`

## Independent executable MCP contract

**passed** — Actual client adapter initialized an independently installed server, discovered/validated exactly 8 reviewed schemas, and cleaned up. Provider keys removed; no client tool call or provider package import.

`python scripts/check_external_contract.py --server <explicit-independent-installed-imagen-mcp> --output docs/evaluations/2026-10-28/external-mcp.json`

## Current style and frozen apparatus

**passed** — Local Ruff configuration makes checks independent of parent workspace defaults. Frozen byte-hashed July harness is excluded from formatting/import resorting; all other selected Python passes. Shared generated HTML literal and Python-compatible timezone spelling have narrow style exceptions.

`ruff check scripts tests modules/tool-imagen evals; ruff format --check scripts tests modules/tool-imagen evals`

## Canonical reference mirror gate

**passed** — Original production/ASCII bodies, native router/policy/schema generated into portable references; source/output hashes prevent hand-maintained drift.

`python3 scripts/sync_skill.py --check`

## Portable build and clean install

**passed** — Canonical ZIP bytes, local links, complete method/license, clean install and idempotent reinstall pass. No runtime starts.

`python3 scripts/capability.py build/check/doctor; install --dest <temporary-parent> twice`

## Explicit local native configuration

**passed** — Absolute local skill/module paths resolve; actual Foundation loader accepts YAML behavior with 2 tools and no provider/session. No activation.

`uv run --with PyYAML python scripts/local_runtime.py --output .capability-check/imagen-studio.yaml; Foundation load_bundle/validate_bundle`

The [dated record](evaluations/2026-10-28/consolidation.json) records the scope. No new paid generation, framework deployment, remote publication, or outside-user outcome is claimed.
