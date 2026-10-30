# Install

This is a content-only bundle: markdown, YAML, and skill definitions. There is no `pyproject.toml`, no Python package, and nothing to build. Installing it means registering it with Amplifier's bundle resolver, not compiling anything.

## Prerequisites

- A working Amplifier install (`amplifier` on your `PATH`).
- Network access to GitHub (`https://github.com/michaeljabbour/amplifier-bundle-ergonomics`), so Amplifier can resolve the git URI.
- Nothing else. No Python dependencies, no build step.

## Path A -- try it with no install

Amplifier resolves `git+https://...` bundle references directly; nothing is written to your project.

```bash
amplifier run --bundle "git+https://github.com/michaeljabbour/amplifier-bundle-ergonomics@main" "Review this agent workflow for user control, recovery, and measurable UX outcomes"
```

## Path B -- install for your own CLI use

Register the bundle, then set it active:

```bash
amplifier bundle add "git+https://github.com/michaeljabbour/amplifier-bundle-ergonomics@main"
amplifier bundle use ux-ergonomist
```

**The name after `bundle use` is the registered bundle name, `ux-ergonomist` -- not the repo name, `amplifier-bundle-ergonomics`.** This is the single most common point of confusion for this repo: `amplifier bundle use amplifier-bundle-ergonomics` (or `ergonomics`) will fail. The namespace comes from the `bundle.name` field in `bundle.md`, not from the git remote.

## Path C -- compose into your own bundle

Two forms, depending on how much you want to pull in.

```yaml
# Whole bundle: agents, behavior, skills, modes, recipes, context -- plus
# foundation and amplifier-bundle-modes, pulled in transitively
includes:
  - bundle: git+https://github.com/michaeljabbour/amplifier-bundle-ergonomics@main
```

```yaml
# Behavior only: this bundle's 4 agents, 8 skills, and context. Nothing else.
includes:
  - bundle: git+https://github.com/michaeljabbour/amplifier-bundle-ergonomics@main#subdirectory=behaviors/ux-ergonomist.yaml
```

| Include form | Pulls in transitively |
|---|---|
| Whole bundle (`...@main`, no fragment) | `foundation`, `amplifier-bundle-modes`, plus this bundle's own agents, skills, context, modes, and recipes |
| Behavior only (`#subdirectory=behaviors/ux-ergonomist.yaml`) | This bundle's 4 agents, 8 skills, and context, and nothing else -- **neither** `foundation` **nor** `amplifier-bundle-modes`. Your composition must supply those separately if it needs them (e.g. core tools and `delegate` from foundation, or mode activation from amplifier-bundle-modes). |

## Path D -- local development

```bash
git clone https://github.com/michaeljabbour/amplifier-bundle-ergonomics
cd amplifier-bundle-ergonomics
amplifier run --bundle ./bundle.md "Review this agent workflow for user control, recovery, and measurable UX outcomes"
```

Validate structure before pushing changes:

```bash
python -m pip install pyyaml
python tests/validate_bundle.py
```

## What you get after install

- 4 agents: `ux-ergonomist`, `evidence-researcher`, `accessibility-auditor`, `human-agent-designer`
- 8 skills: `task-analysis`, `ux-evidence-synthesis`, `cognitive-walkthrough`, `accessibility-evaluation`, `human-agent-authority-map`, `ux-acceptance-criteria`, `usability-study-design`, `ergonomics-verification`
- 6 modes: the `ergonomics-frame` -> `ergonomics-finish` interactive workflow
- 6 recipes: `ergonomic-review`, `agent-experience-review`, `research-to-decision`, `ergonomics-full-cycle`, `longitudinal-agent-impact-review`, `sociotechnical-workflow-review`

**Namespace rule:** everything above is addressed under the `ux-ergonomist` namespace -- the registered bundle name -- never `ergonomics` or `amplifier-bundle-ergonomics` (the repo name). For instance, this bundle's skills are wired as "@ux-ergonomist:skills" (see the capability table below), not "@ergonomics:skills".

## Capability requirements and caveats

| Capability | Requires | Notes |
|---|---|---|
| Modes (`ergonomics-frame` etc.) | `amplifier-bundle-modes` in the composition | Pulled in transitively by the whole-bundle include path. **Not** pulled in by the behavior-only path -- add it yourself if you compose the behavior alone and want the interactive workflow. |
| Recipes | The Recipes capability (`tool-recipes`) in the running Amplifier application | Recipes are data; the tool that executes them is supplied by the host app, not by this bundle. |
| Skills | `tool-skills`, configured with `config.skills: ["@ux-ergonomist:skills"]` | Wired in `behaviors/ux-ergonomist.yaml`, with an explicit module `source:` so the tool mounts even when only the behavior is composed. When the whole bundle is used, foundation also brings its own `tool-skills` entry (for the Microsoft-curated skill collection); Amplifier merges same-module `tools:` entries by module id, so both skill lists accumulate rather than conflict. `@`-mention sources resolve at the session's first request rather than at mount time, so the skills are available from the model's first turn onward, not necessarily before it. |

## Verify your install

After Path A, B, or D, ask the agent to list its skills:

```text
List every skill you can see via load_skill(list=true).
```

You should see all 8 skills named above (`task-analysis`, `ux-evidence-synthesis`, `cognitive-walkthrough`, `accessibility-evaluation`, `human-agent-authority-map`, `ux-acceptance-criteria`, `usability-study-design`, `ergonomics-verification`).

If you installed the whole bundle (Path A, B, or D -- not the behavior-only compose), you can also check the interactive workflow:

```text
/ergonomics-frame
Review the failed-job recovery workflow for operations analysts.
```

A response that engages with framing the review, rather than an unknown-command or missing-tool error, confirms `amplifier-bundle-modes` is active.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `amplifier bundle use amplifier-bundle-ergonomics` (or `ergonomics`) fails, or the bundle can't be found | Confusing the repo name with the registered bundle name | Use `amplifier bundle use ux-ergonomist` |
| `/ergonomics-frame` (or any mode) doesn't activate | `amplifier-bundle-modes` isn't in the composition | Use the whole-bundle include path (Path A, B, or D), or add `amplifier-bundle-modes` explicitly if composing the behavior alone |
| Skills don't appear in `load_skill(list=true)` | The `config.skills` wiring didn't resolve, or you checked before the session's first request | Confirm `behaviors/ux-ergonomist.yaml` still has the `tools: - module: tool-skills` block; skills resolve at the first request, so ask any question first, then list |
| Recipes fail with a missing-tool error | The host Amplifier application doesn't have the Recipes capability (`tool-recipes`) installed | Install/enable `tool-recipes` in your application composition -- this bundle ships only the recipe YAML, not the executor |
