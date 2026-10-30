# Build with Tauri

Make the desktop app work beyond the dev server.

Watch the [71-second film](https://michaeljabbour.github.io/amplifier-skill-build-tauri/#film): a sidecar that was running but not ready, and how the skill makes the desktop app wait for the real signal. The example in it is fictional.

A Tauri 2 development skill for the boundary between webview, Rust and companion processes. Turn “it opens” into clear contracts for requests, streaming, permissions and shutdown.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-build-tauri/) · [Read the method](skills/build-tauri/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Make frontend and Rust agree.** Specify command names, argument casing, serialized results and error handling before debugging both sides at once.
- **Know when a sidecar is ready.** Use a bounded readiness check, an owned child handle and explicit failure recovery.
- **Check the app people install.** Separate source checks, mocked IPC, the running desktop app and the packaged release.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-build-tauri.git
cd amplifier-skill-build-tauri
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/build-tauri` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use Build with Tauri on this Tauri 2 app. Its import sidecar starts slowly and the first request fails. Trace startup, define readiness and shutdown ownership, and propose the smallest fix with target-OS checks.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Map the app.** Inspect lockfiles, configuration, capabilities, Rust entrypoints and target operating system.
2. **Define the boundary.** Choose request/response, channel or event behavior; declare permissions and lifecycle ownership.
3. **Exercise the failure paths.** Test wrong fields, startup failure, repeated launch, cancellation and app exit before checking release packaging.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional contract: import sidecar
Ready: expected versioned health response before deadline
Startup failure: show reason, retry and cancel
Owner: application retains child handle
Exit: graceful stop, then bounded kill fallback
Release check: correct target-triple binary included
```

## What is checked

The retained references were reviewed against the linked official Tauri 2 contracts, and the portable package is checked. No desktop executable is supplied; operating-system lifecycle and release packaging must be tested in your app. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Retained implementation and references

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.

## Repository migration

This repository was renamed from `amplifier-skill-build-tauri` to `amplifier-capability-build-tauri`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.
