# Changelog

All notable changes to the project coordination templates.

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes to template structure (renamed files, removed sections)
- **MINOR**: New templates, new sections in existing templates, new features
- **PATCH**: Fixes to wording, formatting, or examples

---

## [2.2.0] - 2026-04-13

### Changed
- **AGENTS.md template streamlined**: 105 lines → 51 lines. Removed YAML frontmatter (no platform needs it), HTML comment directives, redundant file reference table (already in PROJECT_CONTEXT.md), and cross-platform notes (moved to repo README). What remains: session protocol + continuous improvement contract — the content that matters.
- **README rewritten**: Added platform compatibility table (Amplifier, Codex, Claude Code, Cursor, Windsurf, GitHub Copilot, Aider), cross-platform guidance, Claude Code symlink instructions. Tighter structure.
- **SETUP_PROMPT.md updated**: Includes Claude Code symlink step and Aider config note in post-setup section.

---

## [2.1.0] - 2026-04-13

### Added
- **AGENTS.md template** (Tier 0) -- root-level entry point for any AI agent
  - Session protocol (what to read on start, what to update on end)
  - Continuous improvement contract (when to update which coordination file)
  - Cross-platform notes (Claude Code, Cursor, GitHub Copilot)
- `.gitignore` for generated coordination files (project-specific, not part of template repo)

### Changed
- Setup prompt now generates AGENTS.md at the project root as the final step
- Quick setup prompt includes AGENTS.md generation
- Session end prompt references the continuous improvement contract
- README updated with AGENTS.md documentation and Tier 0 designation

---

## [2.0.0] - 2026-04-13

### Changed
- **Breaking:** Generated files now go inside project-context/ instead of project root
- All prompts updated to use project-context/ paths
- Added .gitignore for generated files

---

## [1.0.0] - 2026-04-13

### Added
- Initial release of 8 project coordination templates
- **PROJECT_CONTEXT.md** (Tier 1) -- current project state at a glance
- **GLOSSARY.md** (Tier 1) -- terminology contract with anti-definitions
- **STRUCTURE.md** (Tier 2) -- directory layout and file routing table
- **WAYSOFWORKING.md** (Tier 2) -- session loop, failure patterns, error recovery protocol
- **HANDOFF.md** (Tier 2) -- session continuity between work sessions
- **PROVENANCE.md** (Tier 3) -- decision journal with structured IDs
- **EXPERIMENT_JOURNAL.md** (Tier 3) -- scientific experiment record with archival policy
- **CLAIMS_TRACKER.md** (Extension) -- patent/IP tracking (optional)
- YAML frontmatter on all templates (type, tier, priority, tokens_estimate)
- HTML comment agent directives for machine-readable behavioral hints
- Structured entry IDs for cross-referencing between files
- Tiered loading system (Tier 1 always, Tier 2 when working, Tier 3 on demand)
- SETUP_PROMPT.md with ready-to-use prompts for full setup, quick setup, session start, and session end
