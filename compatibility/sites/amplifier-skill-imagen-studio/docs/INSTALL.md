# Install Imagen Studio

## Portable method

Requires Git and Python 3.11+. From a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-imagen-studio.git
cd amplifier-skill-imagen-studio
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The destination is the parent of the `imagen-studio` folder. Select your host’s supported skills location. Refresh skill discovery, or point your agent at the complete installed folder and ask it to read `SKILL.md`.

Try this first:

```text
Use Imagen Studio in Guided mode to prepare a fictional product-card illustration. It needs a 4:3 composition, room for a heading and no text inside the image. Draft the brief and acceptance checks first; show the provider and cost before any generation.
```

## Install behavior and optional execution

Use `python3 scripts/capability.py doctor`, then `python3 scripts/capability.py install --dest <skills-parent>`. Keep the complete installed folder and license. Identical reinstall is idempotent; conflicts are refused unless you deliberately choose `--replace`, which retains a dated backup. Remove only that folder to uninstall. No native runtime, server, provider, or service is required to read and apply the method.

## Optional native work

The optional `scripts/local_runtime.py` materializes a local behavior with absolute checkout paths and this checkout’s canonical skill. Its generated file belongs in ignored `.capability-check/`, is local to this machine, and contains no provider keys. Compose it with your configured host/provider only when native execution is needed. It does not install or start the independent MCP server. Frozen v2.0.0 native entrypoints and policy evidence remain retained for compatibility; see the native release guide for those versioned instructions.

For a local native behavior, run `uv run --with PyYAML python scripts/local_runtime.py --output .capability-check/imagen-studio.yaml`. The materializer needs PyYAML (already present in a configured Amplifier Python environment); `uv run --with` keeps that development dependency separate. The generated behavior adds no provider/session and does not activate itself. Compose it deliberately into the existing host only when native execution is needed.