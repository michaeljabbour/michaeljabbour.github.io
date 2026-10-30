> Preserved source method from `amplifier-tauri-skill` at `622249013ca64c725a79542184aec02b70f85c2b`. Original examples and runtime claims are historical; the canonical entry point defines current scope.

---
name: tauri2-sidecar-integration
description: Use when managing sidecar processes in Tauri 2.0 — spawning, health checking, communicating with, and gracefully shutting down companion processes.
---

# Tauri 2.0 Sidecar Integration

A sidecar is a companion process (Python, Node, Go, etc.) that Tauri spawns
and manages alongside the main app. Common use case: running a local API
server that the frontend and Rust backend communicate with.

## Declaring a Sidecar

In `tauri.conf.json`:

```json
{
  "bundle": {
    "externalBin": [
      "binaries/my-sidecar"
    ]
  }
}
```

Place the sidecar binary/script at `src-tauri/binaries/my-sidecar` (Tauri
appends the target triple automatically: `my-sidecar-x86_64-apple-darwin`).

## Spawning a Sidecar

### Using tauri-plugin-shell

```rust
use tauri_plugin_shell::ShellExt;

let sidecar = app.shell()
    .sidecar("my-sidecar")
    .expect("failed to create sidecar command");

let (mut rx, child) = sidecar
    .args(["--port", "8765"])
    .spawn()
    .expect("failed to spawn sidecar");

// Read stdout asynchronously
tauri::async_runtime::spawn(async move {
    while let Some(event) = rx.recv().await {
        match event {
            tauri_plugin_shell::process::CommandEvent::Stdout(line) => {
                println!("sidecar stdout: {}", String::from_utf8_lossy(&line));
            }
            tauri_plugin_shell::process::CommandEvent::Stderr(line) => {
                eprintln!("sidecar stderr: {}", String::from_utf8_lossy(&line));
            }
            _ => {}
        }
    }
});
```

## Health Checking

After spawning, verify the sidecar is ready before routing traffic:

```rust
async fn wait_for_sidecar(url: &str, max_retries: u32) -> Result<(), String> {
    let client = reqwest::Client::new();
    for attempt in 0..max_retries {
        match client.get(format!("{}/health", url)).send().await {
            Ok(resp) if resp.status().is_success() => return Ok(()),
            _ => {
                tokio::time::sleep(std::time::Duration::from_millis(500)).await;
            }
        }
    }
    Err("Sidecar failed to start".into())
}
```

## Communication Patterns

1. **HTTP/REST** — Sidecar runs an HTTP server, frontend/Rust calls it.
   Simplest pattern. Use for request/response.
2. **WebSocket** — Sidecar runs a WS server, frontend connects directly.
   Use for streaming/real-time updates.
3. **Stdin/Stdout** — Communicate via the shell plugin's stdio channels.
   Use for simple, line-based protocols.

## Graceful Shutdown

Kill the sidecar when the app exits:

```rust
// Store the child handle in app state
app.manage(SidecarState { child: Mutex::new(Some(child)) });

// On app exit
app.on_window_event(|window, event| {
    if let tauri::WindowEvent::Destroyed = event {
        if let Some(state) = window.try_state::<SidecarState>() {
            if let Ok(mut child) = state.child.lock() {
                if let Some(c) = child.take() {
                    let _ = c.kill();
                }
            }
        }
    }
});
```

## Guardrails

- Always health-check before assuming the sidecar is ready.
- Store the child process handle in Tauri's managed state for cleanup.
- Log sidecar stderr — silent failures are the #1 debugging pain point.
- For Python sidecars: bundle a standalone binary (PyInstaller/Nuitka) or
  ship the interpreter alongside the app.
