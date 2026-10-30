# Capability installer

Use one pinned capability through its declared interfaces. This shared installer reads `capability.json`, previews permissions/dataflow and copies the complete portable method into a project. Public repository names use `amplifier-capability-*`; existing method folders, imports, CLI commands and tool IDs remain stable.

The implementation is maintained once in [the public catalog's tools directory](https://github.com/michaeljabbour/michaeljabbour.github.io/tree/main/tools). It needs Python 3.11+ and Git. It does not call a model, start native capability code, install dependencies or change account settings. Code-only capabilities return their library/CLI/MCP installation descriptions; they do not receive a fabricated skill wrapper.

## Obtain pinned source

The [download manifest](https://michaeljabbour.github.io/reports/capability-installer/manifest.json) records the exact 40-character `source_commit` and each download's SHA256. Use that commit when obtaining this installer; do not infer a release from a moving branch.

```sh
git clone --filter=blob:none --sparse https://github.com/michaeljabbour/michaeljabbour.github.io.git capability-catalog
git -C capability-catalog sparse-checkout set tools
# Replace the value below with source_commit from the published download manifest.
installer_revision=FULL_40_CHARACTER_SOURCE_COMMIT
git -C capability-catalog checkout --detach "$installer_revision"
```

The sparse clone obtains the installer without the compatibility media. A full clone is optional.

You can also download `capability.py`, `contract.schema.json` and the license from the [installer downloads](https://michaeljabbour.github.io/reports/capability-installer/). Compare their SHA256 values with that manifest before use.

This Market Fit example uses a complete method pinned to a public source revision:

```sh
git clone https://github.com/michaeljabbour/amplifier-capability-market-fit.git market-fit-source
git -C market-fit-source checkout 7ec77c6d056fd0b80b19eb93689d86098a4bf7ec
python3 capability-catalog/tools/capability.py describe --manifest market-fit-source/capability.json
python3 capability-catalog/tools/capability.py preview --source market-fit-source --manifest market-fit-source/capability.json --revision 7ec77c6d056fd0b80b19eb93689d86098a4bf7ec --dest /path/to/project --harness all
```

Review the exact source pin, file hashes, destination directories, permissions, dataflow and `plan_hash`. Apply precisely that reviewed plan:

```sh
python3 capability-catalog/tools/capability.py install --source market-fit-source --manifest market-fit-source/capability.json --revision 7ec77c6d056fd0b80b19eb93689d86098a4bf7ec --dest /path/to/project --harness all --apply --expect-plan PLAN_HASH_FROM_PREVIEW
python3 capability-catalog/tools/capability.py doctor --source market-fit-source --manifest market-fit-source/capability.json --revision 7ec77c6d056fd0b80b19eb93689d86098a4bf7ec --dest /path/to/project --harness all
```

Without `--apply`, installation only previews. Changed source or existing copies require a new preview. The tool refuses foreign/edited copies, escaping or symlink paths, environment files and missing portable references. Only tracked files matching the source pin enter the copy. Local research remains outside it.

## Discovery locations

These declared compatibility paths deduplicate six harness IDs into three physical directories, relative to the explicit project destination:

| Harness ID | Directory |
|---|---|
| `claude-code` (alias `claude`) | `.claude/skills` |
| `codex`, `gemini`, `grok`, `opencode` | `.agents/skills` |
| `amplifier` | `.amplifier/skills` |

Directory placement is not proof that a particular harness/version discovers the method or follows it. Start a fresh host session when required and verify its actual result. Installation does not grant runtime permissions. User-scope installation requires an explicitly supplied destination; no home directory is silently chosen.

## Remove or restore

Preview `uninstall` with the same source, manifest, revision, destination and harness arguments. Add `--apply --expect-plan PLAN_HASH_FROM_PREVIEW` to apply the reviewed removal. Foreign/edited files remain protected and removed copies are preserved in a transaction directory.

```sh
python3 capability-catalog/tools/capability.py rollback --transaction /path/to/project/.capability-state/transaction-ID/transaction.json --apply
```

Rollback refuses intervening edits and restores the previous copy or absence. Backups remain available. The installer does not edit Git ignore/configuration files.

## Check the installer

Run the boundary tests before changing the installer:

```sh
python3 -m unittest discover -s capability-catalog/tools -p test_capability.py -v
```

Contract `version: null` means no recorded release version. Every installation through this shared portable installer requires an exact Git revision.
