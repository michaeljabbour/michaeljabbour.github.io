# Tauri 2 boundary corrections

Checked against official Tauri documentation on 2026-10-28. These pages can change; record installed versions and recheck before implementation.

- [Calling Rust](https://v2.tauri.app/develop/calling-rust/): register commands in the real invoke handler. Async commands run in async tasks; blocking operations still need an appropriate async API or blocking task. Channels support request-bound streaming; events serve broadcasts with listener cleanup.
- [Capabilities](https://v2.tauri.app/security/capabilities/): distinguish application-command access from plugin ACLs. The preserved older IPC guide overstates that every application command universally needs its own capability permission. Inspect application command restrictions and actual plugin permission definitions before changing access.
- [Embedding external binaries](https://v2.tauri.app/develop/sidecar/): `externalBin` declarations map to platform-specific target-triple artifacts. A spawn acknowledgement is not readiness or task completion. Match the shell permission scope when exposing sidecar spawn through the frontend.

Preserved code snippets are patterns, not compiled application fixtures. In particular, the earlier `async read_data` uses blocking `std::fs`; prefer the appropriate async filesystem API or bounded blocking task. A window `Destroyed` handler is not a universal application-exit policy for multi-window or tray apps. Own shutdown at the actual app lifecycle boundary and test it on each target OS.
