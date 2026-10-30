# Optional Amplifier integration

The portable skill folder is independently installable without Amplifier or Memory. These adapters add discovery, a working mode and a capture recipe to an existing Amplifier host; the method remains in the same skill folder.

## From a local checkout

Use the absolute path of this checkout in the file URI:

```sh
amplifier bundle add "file:///path/to/amplifier-skill-project-handoff/behaviors/project-handoff.yaml" --app
```

Start a new session, then ask for `project-handoff` or use `/handoff`. Use `/mode off` to leave the working posture. This command is a documented opt-in, not an installation already performed on your host.

For a reviewed Capture, invoke `@project-handoff:recipes/project-handoff-capture.yaml` with `project` describing the authorized project/task and `destination` naming one handoff file. It drafts without edits, pauses for the exact text to be reviewed, and saves only after the explicit `save` response. A changed source/destination or a leave-alone verdict stops the save path. Resume and Check need no write recipe.

The recipe uses the calling session's `self` agent. The Project Handoff bundle must be loaded so its references resolve. It is intentionally a legacy/self recipe rather than claiming a schema-v2 independent execution closure.

## What was checked

The local `recipes` tool validated this recipe as valid, with no recipe warnings, on 2026-10-28. The surrounding installed Amplifier host produced provider-cache/editable-install provenance warnings during the validation command. Those host warnings were not repaired as part of this skill build. Recipe validation establishes syntax/structure; it does not establish a full live approval/save execution or compatibility with every host.

The portable folder, installer and ZIP are tested separately without provider credentials, Memory, a daemon or any Amplifier package. No remote install or published bundle URL is claimed for this local release.
