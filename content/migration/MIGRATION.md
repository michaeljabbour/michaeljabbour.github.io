# Updating an existing capability installation

The repositories now use `amplifier-capability-*` names. Update the repository URL in your installation source while keeping the installed method folder, bundle alias, module ID, Python package and CLI command you already use.

[Download the complete repository map](mapping.json). It lists all 33 repositories, their previous names, canonical URLs and declared interfaces. Its commit links are identity snapshots; choose your upgrade revision separately.

## Git checkouts

For an existing Memory checkout, update its remote:

```sh
git remote set-url origin https://github.com/michaeljabbour/amplifier-capability-memory.git
git remote -v
git fetch origin
```

Fetching does not change your checked-out revision or overwrite local changes. Review and select the revision you want using your usual Git workflow.

## Amplifier bundles

Keep logical aliases such as `memory`, `knowledge` and `fast-decisions`. A repository name is not a replacement for an internal bundle namespace. For example, existing `memory:behaviors/memory` includes keep that namespace.

First record the existing source and alias, and back up the configuration you intend to change. Check your installed command syntax with `amplifier bundle add --help` and `amplifier bundle update --help`.

To register a canonical repository under an existing alias, use the same alias with a deliberately chosen revision:

```sh
amplifier bundle add 'git+https://github.com/michaeljabbour/amplifier-capability-memory@REVISION' --name memory
```

Replace `REVISION` with your existing tag or commit to change only the source address. To adopt newer code, review and select that newer revision explicitly. Reusing an existing alias replaces that alias's source registration. If that exact source URI is already registered under another alias, inspect the existing registration rather than creating a second name for it.

For a selected registered bundle, the current CLI also supports a targeted source check and update:

```sh
amplifier bundle update memory --source 'git+https://github.com/michaeljabbour/amplifier-capability-memory@REVISION' --check
amplifier bundle update memory --source 'git+https://github.com/michaeljabbour/amplifier-capability-memory@REVISION' -y
```

The update command resolves the bundle's includes and can reinstall dependencies for the selected source. Review the chosen code and dependencies before applying it; resolve any include failure before continuing. Check the resolved source and start a new session to confirm the chosen bundle loads. Keep the backup until that check succeeds.

Change only the selected portfolio source. A migration does not require `--all`, unrelated bundle upgrades, cache deletion or a restart of active sessions.

### Behavior sources and optional variants

A configured application behavior and a selectable root bundle can both legitimately refer to the same repository. Similar-looking URLs in update output do not establish duplicate registrations. Keep each role and its existing behavior path.

When changing a source URI, replace only the repository segment. Preserve its revision and fragment, including paths such as `#subdirectory=behaviors/memory.yaml`, if that fragment is already part of your installation. Do not add a fragment to a root installation that did not use one.

Application behavior registration is separate from a named root bundle. Adding another application source can leave both entries registered. Reconcile those entries deliberately using a backup and your installed CLI's application-bundle commands. The general `bundle remove` operation can affect multiple registries; it is not a safe blanket duplicate cleanup.

Keep the behavior variant you selected. This rename does not opt into additional Memory reflection/indexing behaviors, Fast Decisions routing modes, new providers or broader permissions.

## Agent Skills and native tools

For a method installed into an Agent Skills directory, change the fetch source and retain its declared folder name. In particular, Taste & Elegance remains `improve-taste-and-elegance`, and Forge remains `amplifier-skill-forge`.

Native tool interfaces also keep their names:

| Canonical repository | Python distribution | Commands |
|---|---|---|
| [Imagen Provider](https://github.com/michaeljabbour/amplifier-capability-imagen-provider) | `imagen` | `imagen`, `imagen-mcp`, `imagen-mcp-cli` |
| [Team Access](https://github.com/michaeljabbour/amplifier-capability-team-access) | `addteam` | `addteam` |
| [TeaserKit](https://github.com/michaeljabbour/amplifier-capability-teaserkit) | `teaserkit` | `teaserkit` |
| [Data](https://github.com/michaeljabbour/amplifier-capability-data) | `amplifier-data` | `amplifier-data-doctor` |

Keep existing MCP registration names, tool IDs and client settings. For a Git-based package installation, update the repository URL in your dependency declaration or lockfile and retain the intended revision. Use that capability's installation guide for its actual package or server command; there is no universal `pip install amplifier-capability-*` package name.

## Redirects, Pages and version pins

GitHub redirects old repository web and Git URLs after a rename, while the old repository name remains available for that redirect. Updating remotes explicitly avoids depending on it. Project Pages addresses and hosted GitHub Action `uses:` references need separate handling. See [GitHub's repository rename guidance](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

Use each capability's [portfolio guide](https://michaeljabbour.github.io/) to find its current documentation. An old Pages address is not evidence that the repository migration failed. Existing tags and commit pins retain their meaning: changing a URL does not turn an older pinned release into the latest code or create a new package release.

Additional verified historic repository redirects are `amplifier-bundle-cua` → Desktop Tasks, `amplifier-bundle-memory` → Memory and `amplifier-bundle-teamwork` → Good Teammate. Their internal bundle names remain `cua`, `memory` and `teamwork-standalone`, respectively.

`amplifier-smart-tool-visualizer` is a separate archived repository, not an alias for Knowledge. If your source explicitly names Visualizer, assess that source separately rather than applying a rename substitution to it.

## Rollback

Restore the backed-up source registration or dependency declaration and its previous revision, then verify it in a new session. For a Git checkout, restore the previous remote URL if needed. Keep existing caches, installed data and active-session state intact while checking the result.

## Repository names

The map below covers the renamed public capabilities. Installed names that differ from the repository name are intentional.

| Previous repository | Canonical repository | Keep these installed names |
|---|---|---|
| `amplifier-smart-tool-decisioncraft` | `amplifier-capability-decisioncraft` | folder `decisioncraft`; CLI `decisioncraft` |
| `amplifier-skill-market-fit` | `amplifier-capability-market-fit` | folder `market-fit`; bundle `market-fit` |
| `amplifier-skill-right-shape` | `amplifier-capability-right-shape` | folder `right-shape`; bundle `right-shape` |
| `amplifier-skill-sizzle` | `amplifier-capability-sizzle` | folder `sizzle` |
| `amplifier-skill-taste` | `amplifier-capability-taste-elegance` | folder `improve-taste-and-elegance`; bundle `taste-elegance` |
| `amplifier-skill-worth-using` | `amplifier-capability-worth-using` | folder `worth-using`; bundle `worth-using` |
| `amplifier-skill-build-amplifier` | `amplifier-capability-build-amplifier` | folder `build-amplifier` |
| `amplifier-skill-build-tauri` | `amplifier-capability-build-tauri` | folder `build-tauri` |
| `amplifier-skill-build-torque` | `amplifier-capability-build-with-torque` | folder `build-with-torque` |
| `amplifier-skill-cognitive-simulation` | `amplifier-capability-cognitive-simulation` | folder `cognitive-simulation`; bundle `cognitive-research` |
| `amplifier-skill-constraint-builder` | `amplifier-capability-constraint-builder` | folder `constraint-builder`; bundle `harness-machine` |
| `amplifier-skill-desktop-tasks` | `amplifier-capability-desktop-tasks` | folder `desktop-tasks`; bundle `cua` |
| `amplifier-smart-tool-fast-decisions` | `amplifier-capability-fast-decisions` | folder `fast-decisions`; bundle `fast-decisions`; CLI `amplifier-fast-decisions`, `afast` |
| `amplifier-skill-forge` | `amplifier-capability-forge` | folder `amplifier-skill-forge` |
| `amplifier-skill-good-teammate` | `amplifier-capability-good-teammate` | folder `good-teammate`; bundle `teamwork-standalone` |
| `amplifier-tool-imagen-provider` | `amplifier-capability-imagen-provider` | CLI `imagen-mcp`, `imagen-mcp-cli`, `imagen` |
| `amplifier-skill-imagen-studio` | `amplifier-capability-imagen-studio` | folder `imagen-studio`; bundle `imagen` |
| `amplifier-skill-intent-to-plan` | `amplifier-capability-intent-to-plan` | folder `intent-to-plan`; bundle `idd` |
| `amplifier-smart-tool-knowledge` | `amplifier-capability-knowledge` | folder `knowledge`; bundle `knowledge`; CLI `knowledge` |
| `amplifier-skill-long-read` | `amplifier-capability-long-read` | folder `long-read` |
| `amplifier-skill-memory` | `amplifier-capability-memory` | folder `memory`; bundle `memory` |
| `amplifier-skill-migrate` | `amplifier-capability-migrate` | folder `migrate`; bundle `gm` |
| `amplifier-skill-pipeline` | `amplifier-capability-pipeline` | folder `pipeline`; bundle `cicd` |
| `amplifier-skill-preceptor` | `amplifier-capability-preceptor` | folder `preceptor`; bundle `preceptor` |
| `amplifier-skill-project-handoff` | `amplifier-capability-project-handoff` | folder `project-handoff`; bundle `project-handoff` |
| `amplifier-skill-research` | `amplifier-capability-research` | folder `research`; bundle `research` |
| `amplifier-skill-session-doctor` | `amplifier-capability-session-doctor` | folder `session-doctor`; bundle `provider-doctor` |
| `amplifier-tool-team-access` | `amplifier-capability-team-access` | CLI `addteam` |
| `amplifier-smart-tool-teaserkit` | `amplifier-capability-teaserkit` | CLI `teaserkit` |
| `amplifier-skill-transfer` | `amplifier-capability-transfer` | folder `transfer`; bundle `hgt` |
| `amplifier-skill-ux-ergonomics` | `amplifier-capability-ux-ergonomics` | folder `ux-ergonomics`; bundle `ux-ergonomist` |
| `amplifier-skill-unknowns` | `amplifier-capability-unknowns` | folder `unknowns`; bundle `unknowns`; CLI `unknowns` |
| `amplifier-tool-data` | `amplifier-capability-data` | CLI `amplifier-data-doctor` |
