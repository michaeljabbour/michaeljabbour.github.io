# Install Project Handoff

Bring the existing project notes, current request and relevant files. Capture a handoff, resume read-only, or check a record without inventing missing decisions.

## From the public source

Use Git and Python 3.11 or later. These commands install the complete method into a skills-parent directory:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-project-handoff.git
cd amplifier-skill-project-handoff
python3 scripts/install.py --dest ~/.agents/skills
```

Choose the discovery directory supported by your agent. `~/.agents/skills` is an example. Start a new session if your host only discovers skills at startup, then ask for Project Handoff by name with one task. Read the returned result and its sources before acting on it.

The installer refuses conflicting files. Keep your changes before deliberately replacing a copy. It does not register a host, start a service or prove model behavior.

## Without a checkout

Download the complete ZIP from [the public site](https://michaeljabbour.github.io/amplifier-skill-project-handoff/#use-skill), extract it and place the whole skill folder in your host’s skills directory. Keep all references, helpers and license files together. The single SKILL.md download is for reading; use the whole folder to install.

## What to expect

Bring the existing project notes, current request and relevant files. Capture a handoff, resume read-only, or check a record without inventing missing decisions.

The next collaborator needs to receive or read the saved record.
