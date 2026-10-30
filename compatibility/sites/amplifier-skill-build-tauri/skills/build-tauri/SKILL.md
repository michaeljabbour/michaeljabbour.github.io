---
name: build-tauri
description: Use when creating or repairing Tauri 2 project structure, IPC, permissions, or sidecar lifecycle.
license: MIT
---

# Build with Tauri

Build a desktop app whose frontend and sidecar agree.

## Inspect the app before changing it

Read `package.json`, the frontend lockfile, `src-tauri/Cargo.toml`, `Cargo.lock`, configuration, capability files, Rust entrypoints, and the actual target platform. Record the versions. Decide whether the task belongs in the frontend, Rust shell, a plugin, or a companion process. Keep application-specific examples separate from Tauri's general protocol.

## Structure

Use [project structure](references/tauri2-project-structure/METHOD.md) to trace frontend build → shell configuration → Rust setup → bundle output. Preserve the project's package manager and platform setup. Run existing build commands, not a newly invented parallel build system. Check the packaged asset paths and CSP against actual configuration.

## IPC

Use [IPC patterns](references/tauri2-ipc-patterns/METHOD.md) as the baseline, with the [current corrections](references/current-contracts.md). Write a contract for command name, argument names/casing, serialized return/error values, caller window, and permission scope. Register all commands in the actual builder. Prefer commands for request/response, channels for ordered streaming tied to a request, and events for suitable broadcast notifications. Clean up every listener on unmount or cancellation; test failure and repeated mounting.

An `async` signature does not make blocking filesystem or CPU work nonblocking. Use an appropriate asynchronous API or a blocking task. Application commands and plugin permissions follow different rules: do not invent a per-command capability entry as a universal fix. Inspect the project's application-command ACL and the relevant plugin's generated permissions.

## Sidecar

Use [sidecar integration](references/tauri2-sidecar-integration/METHOD.md) and the current corrections. Define the binary name and target-triple artifact, allowed arguments, transport, readiness response/version, bounded timeout, stderr handling, restart policy, cancellation, and shutdown owner. A successful process spawn is not readiness. Keep the child handle; prefer graceful shutdown before a bounded kill fallback. Test startup failure, occupied port, crashed child, repeated launch, and application exit. Window destruction alone may not mean the application exits in a multi-window/tray app.

## Verify in layers

Run formatting/type/build checks first, then IPC checks with deliberately mismatched fields and rejected permissions, then the actual desktop app on the target OS. Confirm release packaging contains the correct sidecar architecture. A dev server success does not establish the installed app works. Record which layer ran and which remains blocked. This repository supplies reference patterns, not an executable contract fixture, Tauri compiler or desktop acceptance test. Create boundary checks in the actual app and record what they exercise.

Return changed interfaces, minimum permissions, version/source evidence, exact checks, and a reproducible unresolved case. Keep real-user usability and accessibility claims within the evidence actually collected.
