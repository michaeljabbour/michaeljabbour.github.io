> Original native guide, preserved at source commit `79b64cb33cb7ea123c8004733282bfcc29837f8d`. Install locations, model names, service availability, and claims below are historical and must be verified before use. Current portable installation is in INSTALL.md.

# amplifier-bundle-research

**Superpowers for scientific rigor — for anyone who needs a defensible written artifact.**

Patent briefs, policy positions, white papers, literature reviews, workshop papers, grant applications, full journal articles. Same discipline, same scaffolding — output shaped to the venue.

---

## Install

```bash
amplifier bundle add --app git+https://github.com/michaeljabbour/amplifier-bundle-research@main
amplifier bundle use research
amplifier
```

No YAML edits and no API keys beyond the one Amplifier already uses.

## Why it exists

Scientific rigor is a set of habits: ask a precise question, lock the method before you see the data, report honestly against yourself, cite properly, and format for the reader. Working researchers learn these over a decade; everyone else reinvents the mistakes.

This bundle encodes the habits. A patent attorney, a policy analyst, a founder drafting a technical white paper, or a first-time researcher all get the same scaffolding and the same honest critic — shaped to what they are making.

## How you use it

A six-step pipeline, available as slash commands. The `research-coordinator` also routes natural-language requests to the right step.

| Command | What it does |
|---------|--------------|
| `/question` | Sharpen a vague idea into a precise, defensible claim. |
| `/study-plan` | Lock the methodology *before* results exist — writes a hash-sealed pre-registration. |
| `/execute` | Run the analysis, gather prior art, or pull the evidence. |
| `/critique` | An honest peer reviewer: names limitations, flags overclaiming, separates confirmatory from exploratory. |
| `/draft` | Produce the artifact in the right structure for the audience. |
| `/publish` | Format for the target venue (LaTeX / DOCX / brief). Gated until critique has run and any honest-pivots are acknowledged. |

### Or jump straight to a document type

```bash
amplifier run "Run the patent-brief recipe on: Novel rolling-ROI control for AI agent sessions"
amplifier run "Run the white-paper recipe on: Return on Inference — when model spend pays back"
amplifier run "Run the empirical-paper recipe on: Reflection tokens improve long-horizon reasoning"
```

Document recipes: **patent-brief, policy-brief, white-paper, empirical-paper, benchmark-paper, replication-study, grant-proposal, literature-review, idea-generation, paperbanana-figure.**

### Just want to write a paper?

If you want the paper-authoring slice only — LaTeX, conference formatting, citations, and figures, without the pre-registration and experiment machinery — use the bundled lean variant:

```bash
amplifier bundle add ./bundles/paper-only.md
amplifier run --bundle research-paper-only "Draft a NeurIPS paper on ..."
```

(This absorbs the former `amplifier-bundle-scientificpaper`, which was a strict subset of this bundle and is now retired.)

## What's inside

| Component | Count | Highlights |
|-----------|-------|------------|
| **Specialist agents** | 14 | hypothesis-designer, methodologist, preregistration-reviewer, statistician, literature-scout, idea-generator, honest-critic, ml-paper-reviewer, research-paper-architect, research-technical-writer, research-citation-manager, venue-formatter, figure-designer, research-coordinator |
| **Runtime modes** | 6 | the `/question → /publish` pipeline, registered as slash commands |
| **Document recipes** | 10 | one per artifact type, end-to-end |
| **Discipline behaviors** | 12 | honest-pivot, exploratory-labeling, stop-slop, cross-vendor-judge, cache-only-verification, plus the paper-authoring composite |
| **Experiment-integrity tools** | 6 | audit, power analysis, provenance check, resume/repair, stage analysis, hypothesis blocking |
| **Figure generation** | 1 | PaperBanana multi-agent pipeline with 8 quality veto rules (`modules/tool-paperbanana`) |
| **Venue knowledge** | 9 | NeurIPS, ICML, ACL, IEEE, ACM, arXiv + USPTO patent, policy memo, NSF/NIH grant |

Plus a reproducibility stack (`environment.yml`, `Dockerfile.research`, execution/evidence-log schemas), LaTeX templates and skeletons, and utility scripts for compilation, validation, and figure generation.

## Architecture

![Bundle architecture](../bundle.png)

The diagram (`bundle.dot`) shows the pipeline spine, the specialist agents grouped by the stage they serve, and the supporting tools and knowledge. Regenerate the PNG with `dot -Tpng bundle.dot -o bundle.png`.

## Local development

```bash
git clone https://github.com/michaeljabbour/amplifier-bundle-research.git
cd amplifier-bundle-research

# Standalone dev composition (adds a provider so it runs without --app)
amplifier run --bundle ./bundles/dev.yaml "your prompt here"
```

See [`bundles/dev.yaml`](https://github.com/michaeljabbour/amplifier-bundle-research/blob/79b64cb33cb7ea123c8004733282bfcc29837f8d/bundles/dev.yaml) and [`docs/HANDOFF.md`](https://github.com/michaeljabbour/amplifier-bundle-research/blob/79b64cb33cb7ea123c8004733282bfcc29837f8d/docs/HANDOFF.md) for the full workflow.

## Provenance

Thin wrappers over [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills), orchestrated with a [Superpowers](https://github.com/microsoft/amplifier-bundle-superpowers)-style mode workflow, informed by [Denario](https://github.com/AstroPilot-AI/Denario)'s multi-agent topology. Full specification in [`docs/SPEC.md`](https://github.com/michaeljabbour/amplifier-bundle-research/blob/79b64cb33cb7ea123c8004733282bfcc29837f8d/docs/SPEC.md); credits and lineage in [`docs/LINEAGE.md`](https://github.com/michaeljabbour/amplifier-bundle-research/blob/79b64cb33cb7ea123c8004733282bfcc29837f8d/docs/LINEAGE.md).

## v0.9.0 (2026-05-29) — Autonomous experiment loop

Full empirical lifecycle inside a single session: data → analysis → honest conclusion. The loop runs propose → collect → analyze → decide → log against a hash-locked FROZEN apparatus, terminating in a held-out promotion gate confirmatory re-run + Benjamini–Hochberg + cross-vendor multi-LLM judge panel. Output is a defensible FINDING — confirmatory or honest null — not a hill-climb.

**New:**
- `skills/conducting-autonomous-experiments/SKILL.md` — discipline guide for the loop
- `recipes/autonomous-experiment-loop.yaml` + iteration body + promotion gate
- `agents/experiment-runner.md` — execution agent with integrity guardrails
- `templates/experiment-ledger.yaml` — schema for the hash-sealed ledger
- `context/autonomous-loop-awareness.md` — loop-state context for agents
- `scripts/experiment-loop/` — helpers (hash-lock, ledger writer, BH correction)

Reached via `/execute` only when the locked plan declares `experiment_loop`; plans without one behave exactly as before.

**Attribution:** Pattern transfer, idea-level, from [Karpathy autoresearch `program.md`](https://github.com/karpathy/autoresearch) (MIT): propose → run → measure → keep/revert → log against a frozen apparatus with git as ledger. GPU/PyTorch/CUDA training code intentionally NOT imported — only the discipline, hardened with pre-registration hash-lock, n>1 variance, guardrails, integrity audit, held-out promotion gate, and cross-vendor judge panel.

## License

MIT.
