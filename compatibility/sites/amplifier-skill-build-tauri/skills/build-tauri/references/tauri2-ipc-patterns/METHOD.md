> Preserved source method from `amplifier-tauri-skill` at `622249013ca64c725a79542184aec02b70f85c2b`. Original examples and runtime claims are historical; the canonical entry point defines current scope.

---
name: tauri2-ipc-patterns
description: Use when implementing communication between Rust backend and web frontend in Tauri 2.0 — commands, events, and invoke patterns.
---

# Tauri 2.0 IPC Patterns

Tauri uses two IPC mechanisms: **commands** (request/response) and **events**
(pub/sub). Both cross the Rust-to-frontend boundary.

## Commands (Invoke Pattern)

### Rust Side

Define a command with the `#[tauri::command]` attribute:

```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// Async commands for I/O operations:
#[tauri::command]
async fn read_data(path: String) -> Result<String, String> {
    std::fs::read_to_string(&path).map_err(|e| e.to_string())
}
```

Register commands in the builder:

```rust
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, read_data])
        .run(tauri::generate_context!())
        .expect("error");
}
```

### Frontend Side

Call commands with `invoke`:

```typescript
import { invoke } from "@tauri-apps/api/core";

const greeting = await invoke<string>("greet", { name: "World" });
const data = await invoke<string>("read_data", { path: "/tmp/data.txt" });
```

## Events (Pub/Sub Pattern)

### Emit from Rust to Frontend

```rust
use tauri::Emitter;

app.emit("download-progress", ProgressPayload { percent: 50 })?;
```

### Listen in Frontend

```typescript
import { listen } from "@tauri-apps/api/event";

const unlisten = await listen<{ percent: number }>("download-progress", (event) => {
    console.log(`Progress: ${event.payload.percent}%`);
});

// Clean up when done
unlisten();
```

### Emit from Frontend to Rust

```typescript
import { emit } from "@tauri-apps/api/event";
await emit("user-action", { action: "save" });
```

## Patterns and Guardrails

1. **Commands for request/response.** Use when the frontend needs a result.
2. **Events for streaming/notifications.** Use when Rust pushes updates.
3. **Serialize with serde.** All command args/returns must be serde-compatible.
4. **Error handling via Result.** Return `Result<T, String>` from commands —
   the error string surfaces in the frontend `invoke` rejection.
5. **Permissions required.** Commands need capability permissions in
   `capabilities/default.json` to be callable from the frontend.
6. **Avoid blocking the main thread.** Use `async` commands for I/O, database,
   or network operations.
