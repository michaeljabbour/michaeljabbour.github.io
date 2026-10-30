# Install Build with Torque

## Portable method

Requires Git and Python 3.11+. From a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-build-torque.git
cd amplifier-skill-build-torque
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The destination is the parent of the `build-with-torque` folder. Select your host’s supported skills location. Refresh skill discovery, or point your agent at the complete installed folder and ask it to read `SKILL.md`.

Try this first:

```text
Use Build with Torque to design a maintenance-task bundle. It should react to asset changes without reading another bundle’s private tables. Inspect this host first, then propose its manifest, public interfaces, events and migration checks.
```

## Install behavior and optional execution

Use `python3 scripts/capability.py doctor`, then `python3 scripts/capability.py install --dest <skills-parent>`. Keep the complete installed folder and license. Identical reinstall is idempotent; conflicts are refused unless you deliberately choose `--replace`, which retains a dated backup. Remove only that folder to uninstall. No native runtime, server, provider, or service is required to read and apply the method.

## Optional native work

The original Torque installers and package guide remain in the repository. They clone/install framework packages and can change a user installation; they are separate from the portable installer and were not run here. Use the actual host CLI/contracts and isolated data for application checks. The skill does not retire or merge the kernel, CLI, services, extensions, or domain bundles.