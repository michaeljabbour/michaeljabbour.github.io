> Original native guide, preserved at source commit `622249013ca64c725a79542184aec02b70f85c2b`. Install locations, model names, service availability, and claims below are historical and must be verified before use. Current portable installation is in INSTALL.md.

# amplifier-tauri-skill

Generic [Tauri 2.0](https://tauri.app/) development skills for AI coding assistants. These skills teach standard Tauri project structure, IPC patterns, and sidecar integration -- not specific to any one Tauri app.

## Skills Included

| Skill | Description |
|-------|-------------|
| `tauri2-project-structure` | Standard Tauri 2.0 layout, Cargo conventions, plugin system |
| `tauri2-ipc-patterns` | Commands, events, invoke between Rust and frontend |
| `tauri2-sidecar-integration` | Managing sidecar processes: spawn, health check, communication |

## Install from GitHub

### Quick Install (Amplifier + Claude Code)

```bash
git clone https://github.com/michaeljabbour/amplifier-tauri-skill.git ~/dev/amplifier-tauri-skill
cd ~/dev/amplifier-tauri-skill
./install.sh
```

This creates symlinks in both `~/.amplifier/skills/` and `~/.claude/skills/`,
so every Amplifier session and every Claude Code session sees the same skills.
Update anytime with `git pull` — symlinks mean both tools pick up changes
instantly.

### Amplifier Bundle YAML (alternative)

If you prefer git-sourced skills fetched on the fly:

```yaml
tools:
  - module: tool-skills
    config:
      skills:
        - "git+https://github.com/michaeljabbour/amplifier-tauri-skill@main"
```

### Kepler Desktop

Already configured via `behaviors/skills.yaml`. Nothing to install.

### Other Tools (Cursor, Warp, etc.)

```bash
git clone https://github.com/michaeljabbour/amplifier-tauri-skill.git
```

Point your tool at the `SKILL.md` files in each subdirectory.

## Related Skill Repos

These three repos layer on top of each other:

```
amplifier-skill            -- Core Amplifier patterns (delegation, CLI, agents)
amplifier-kepler-skill     -- Kepler-specific (desktop distribution)
amplifier-tauri-skill      -- Generic Tauri 2.0 (this repo)
```

Install all three for full-stack Kepler development:

```yaml
# In your bundle YAML (git sources -- always up to date)
tools:
  - module: tool-skills
    config:
      skills:
        - "git+https://github.com/michaeljabbour/amplifier-skill@main"
        - "git+https://github.com/michaeljabbour/amplifier-kepler-skill@main"
        - "git+https://github.com/michaeljabbour/amplifier-tauri-skill@main"
```

Or clone and symlink all three globally:

```bash
mkdir -p ~/.amplifier/skills

# amplifier-skill (single skill at repo root)
mkdir -p ~/.amplifier/skills/amplifier-skill
ln -sf ~/dev/amplifier-skill/SKILL.md ~/.amplifier/skills/amplifier-skill/SKILL.md

# kepler skills (4 skills)
for skill in kepler-architecture kepler-dev-setup kepler-sidecar-patterns kepler-bundle-composition; do
  mkdir -p ~/.amplifier/skills/$skill
  ln -sf ~/dev/amplifier-kepler-skill/$skill/SKILL.md ~/.amplifier/skills/$skill/SKILL.md
done

# tauri skills (3 skills)
for skill in tauri2-project-structure tauri2-ipc-patterns tauri2-sidecar-integration; do
  mkdir -p ~/.amplifier/skills/$skill
  ln -sf ~/dev/amplifier-tauri-skill/$skill/SKILL.md ~/.amplifier/skills/$skill/SKILL.md
done
```

## Repository Layout

```text
.
├── README.md
├── .gitignore
├── tauri2-project-structure/
│   └── SKILL.md
├── tauri2-ipc-patterns/
│   └── SKILL.md
└── tauri2-sidecar-integration/
    └── SKILL.md
```
