# Project Context

Markdown templates that give AI agents persistent project memory across sessions.

Drop this into any repo, run one prompt, and your agent knows your project structure, terminology, decisions, failure patterns, and current state — every session, without re-explaining.

Works with Amplifier, Claude Code, Codex, Cursor, Windsurf, GitHub Copilot, and any agent that reads `AGENTS.md`.

## Quick Start

**1. Add to your project:**

```bash
# Option A: Clone into your repo
git clone https://github.com/michaeljabbour/project-context.git project-context

# Option B: Add as a submodule (gets updates when you pull)
git submodule add https://github.com/michaeljabbour/project-context.git project-context
```

**2. Generate your project's coordination files.**

Open an AI coding session and give it the prompt from [`SETUP_PROMPT.md`](SETUP_PROMPT.md):

```
Read project-context/README.md first to understand the coordination file
system — its tiers, cognitive modes, and maintenance expectations. Then
read all the templates in project-context/templates/. Scan the codebase
to understand the project — its structure, language, dependencies, and
current state. Look for any existing files that already serve coordination
functions (READMEs, CONTRIBUTING guides, decision logs, changelogs,
onboarding docs, architecture docs, glossaries, AGENTS.md, etc.) and
consolidate their relevant content into the new format rather than
starting from scratch. Generate customized versions of each coordination
file inside the project-context/ directory (alongside the templates/
folder) — do not modify anything inside project-context/templates/
(those are the versioned source of truth). Start with PROJECT_CONTEXT.md
and GLOSSARY.md (Tier 1), then STRUCTURE.md, WAYSOFWORKING.md, and
HANDOFF.md (Tier 2). Ask me before generating Tier 3 files
(PROVENANCE.md, EXPERIMENT_JOURNAL.md) or the optional
CLAIMS_TRACKER.md. Finally, generate AGENTS.md at the project root
(not inside project-context/) — this is the entry point that tells
any AI agent about the coordination system and how to maintain it.
```

**3. That's it.** The generated `AGENTS.md` at your project root tells any AI agent to read the coordination files automatically. No need to repeat instructions each session.

> **For Claude Code users:** Claude Code reads `CLAUDE.md` rather than `AGENTS.md`. Create a symlink so both work: `ln -s AGENTS.md CLAUDE.md`

---

## How It's Organized

```
your-project/
├── AGENTS.md                       # ← Generated at root (auto-read by most AI agents)
└── project-context/                # Cloned into your repo
    ├── templates/                  # Versioned source of truth — don't edit
    │   ├── AGENTS.md
    │   ├── PROJECT_CONTEXT.md
    │   ├── GLOSSARY.md
    │   ├── STRUCTURE.md
    │   ├── WAYSOFWORKING.md
    │   ├── HANDOFF.md
    │   ├── PROVENANCE.md
    │   ├── EXPERIMENT_JOURNAL.md
    │   └── CLAIMS_TRACKER.md
    │
    │   # After setup, generated files appear here:
    ├── PROJECT_CONTEXT.md          # ← Generated, project-specific
    ├── GLOSSARY.md
    ├── STRUCTURE.md
    ├── WAYSOFWORKING.md
    ├── HANDOFF.md
    ├── PROVENANCE.md
    ├── EXPERIMENT_JOURNAL.md
    └── CLAIMS_TRACKER.md           # (optional)
```

**Templates** are the versioned reference — they never change per-project. **Generated files** are your project-specific living documents. AGENTS.md is the only file at the project root — the universal entry point that tells agents where the coordination files are and how to maintain them.

---

## The Files

Nine templates, organized by how often agents need them.

### Root Entry Point

| File | Purpose |
|------|---------|
| **AGENTS.md** | Lives at the **project root**. Entry point for any AI agent. Session protocol (what to read, what to update) and continuous improvement contract (how to keep all other files growing). |

### Tier 1 — Always Read (<1000 tokens combined)

| File | Purpose |
|------|---------|
| **PROJECT_CONTEXT.md** | Current project state at a glance: phase, version, team, active milestone. |
| **GLOSSARY.md** | Terminology contract. "We say X, we mean Y, we do NOT mean Z." |

### Tier 2 — Read When Working

| File | Purpose |
|------|---------|
| **STRUCTURE.md** | Directory layout, naming conventions, routing table ("I have X, where does it go?"). |
| **WAYSOFWORKING.md** | Session loop, proven workflows, named failure patterns (symptom/cause/fix), verification commands. |
| **HANDOFF.md** | Session continuity. What happened last, what's blocked, what to do next. Rewritten every session. |

### Tier 3 — Read When Investigating

| File | Purpose |
|------|---------|
| **PROVENANCE.md** | Decision journal. Why things are the way they are, what was tried and abandoned. |
| **EXPERIMENT_JOURNAL.md** | Scientific record. Hypothesis before results, raw data, root cause analysis. |

### Extension — Optional

| File | Purpose |
|------|---------|
| **CLAIMS_TRACKER.md** | Patent/IP tracking. Claims, prior art maps, prosecution timeline. |

---

## Why It Works

These files are organized by **cognitive mode**, not by topic. Each maps to a different kind of thinking an agent does:

| File | Thinking Mode | Agent's Question |
|------|--------------|-----------------|
| AGENTS.md | Self-regulation | "What are my obligations?" |
| PROJECT_CONTEXT | Orientation | "Where am I?" |
| GLOSSARY | Semantic grounding | "What do these terms mean?" |
| STRUCTURE | Spatial reasoning | "Where do things go?" |
| WAYSOFWORKING | Procedural reasoning | "How do I work here?" |
| HANDOFF | Session continuity | "What just happened?" |
| PROVENANCE | Causal reasoning | "Why was it done this way?" |
| EXPERIMENT_JOURNAL | Scientific reasoning | "What was tried?" |

Agents load only the context relevant to their current task. Less noise, more accurate behavior, and knowledge that compounds across sessions instead of evaporating.

**Three mechanisms drive the compounding:**

1. **The terminology table** (GLOSSARY.md) acts as a type system for natural language. The "Does NOT Mean" column constrains interpretation the way a type signature constrains code.

2. **Named failure patterns** (WAYSOFWORKING.md) create institutional memory. An agent in session 12 benefits from session 3's pain without repeating it.

3. **The continuous improvement contract** (AGENTS.md) makes the system self-maintaining. Agents update files as they work — no human prompting required.

---

## Maintaining the Files

| File | When to Update |
|------|---------------|
| AGENTS.md | Rarely — only when session protocol or contract changes |
| PROJECT_CONTEXT.md | Every session (current phase, milestone) |
| GLOSSARY.md | When new terms emerge |
| HANDOFF.md | End of every session (rewrite completely) |
| STRUCTURE.md | When directory layout changes |
| WAYSOFWORKING.md | When something breaks or a better pattern emerges |
| PROVENANCE.md | When decisions are made |
| EXPERIMENT_JOURNAL.md | After every experiment |
| CLAIMS_TRACKER.md | When claims evolve |

---

## Platform Compatibility

`AGENTS.md` is the [cross-platform standard](https://agents.md/) for AI agent instructions, stewarded by the Agentic AI Foundation under the Linux Foundation. It's natively supported by most AI coding tools.

| Platform | Reads AGENTS.md? | Notes |
|----------|-----------------|-------|
| **Amplifier** | Yes | Native |
| **OpenAI Codex** | Yes | Originated the convention |
| **GitHub Copilot** | Yes | Also reads CLAUDE.md and .github/copilot-instructions.md |
| **Cursor** | Yes | Also reads .cursorrules |
| **Windsurf** | Yes | Auto-scoped by directory |
| **Claude Code** | No — reads CLAUDE.md | Symlink: `ln -s AGENTS.md CLAUDE.md` |
| **Aider** | Via config | Add `read: AGENTS.md` to `.aider.conf.yml` |

For repos used across multiple platforms, `AGENTS.md` is the canonical file. Symlink or copy for tools that need their own filename.

---

## Updating Templates

This repo uses [semantic versioning](https://semver.org/). To get template updates:

```bash
cd project-context && git pull        # If cloned directly
git submodule update --remote project-context  # If submodule
```

Template updates don't affect your generated files. Re-run the setup prompt to incorporate new template features.

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## License

[MIT](LICENSE)
