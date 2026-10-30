# Setup Prompt

Copy and paste one of these prompts into your AI coding session to generate customized project coordination files from the templates.

---

## Full Setup

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

---

## Quick Setup (Tier 1 + AGENTS.md)

For a minimal start:

```
Read project-context/README.md to understand the coordination file system.
Then read project-context/templates/PROJECT_CONTEXT.md,
project-context/templates/GLOSSARY.md, and
project-context/templates/AGENTS.md. Scan the codebase and any existing
coordination files (READMEs, glossaries, AGENTS.md, onboarding docs) and
generate customized versions: PROJECT_CONTEXT.md and GLOSSARY.md inside
project-context/, and AGENTS.md at the project root. Do not modify
anything inside project-context/templates/.
```

---

## After Setup

### Claude Code users

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Create a symlink so both work:

```bash
ln -s AGENTS.md CLAUDE.md
```

### Aider users

Add the coordination files to your Aider config:

```yaml
# .aider.conf.yml
read:
  - AGENTS.md
  - project-context/PROJECT_CONTEXT.md
  - project-context/GLOSSARY.md
```

### All platforms

Commit the generated files (AGENTS.md + everything in project-context/) to your repo so they persist across clones.

---

## Session Start

```
Read project-context/PROJECT_CONTEXT.md and project-context/GLOSSARY.md
before starting any work. Check project-context/HANDOFF.md for what
happened last session and what to do next.
```

_(If AGENTS.md is at the project root, most agents read it automatically — you may not need to say this.)_

---

## Session End

```
Update project-context/HANDOFF.md with what we accomplished this session,
what's blocked, and what the next session should start with. Update any
other coordination files that changed (see the continuous improvement
contract in AGENTS.md).
```
