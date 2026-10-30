> Preserved source method from `amplifier-tauri-skill` at `622249013ca64c725a79542184aec02b70f85c2b`. Original examples and runtime claims are historical; the canonical entry point defines current scope.

---
name: tauri2-project-structure
description: Use when working on a Tauri 2.0 project to understand the standard layout, Cargo conventions, plugin system, and where different code belongs.
---

# Tauri 2.0 Project Structure

Standard layout for a Tauri 2.0 application with a web frontend.

## Directory Layout

```
my-tauri-app/
├── src/                    Frontend (React, Vue, Svelte, etc.)
│   ├── components/
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/              Rust native shell
│   ├── Cargo.toml          Rust dependencies + Tauri features
│   ├── tauri.conf.json     App config (window, security, bundle settings)
│   ├── capabilities/       Permission declarations
│   │   └── default.json
│   ├── src/
│   │   ├── main.rs         Entry point — setup, plugins, invoke handlers
│   │   └── lib.rs          Shared library code
│   └── icons/              App icons for all platforms
├── package.json            Frontend dependencies + build scripts
└── vite.config.ts          (or equivalent bundler config)
```

## Key Files

### `src-tauri/tauri.conf.json`

Central config: app name, window defaults, security policy, bundle targets
(DMG, MSI, AppImage). This is where you configure CSP, allowed APIs, and
sidecar declarations.

### `src-tauri/Cargo.toml`

Rust dependencies. Tauri features are enabled here:

```toml
[dependencies]
tauri = { version = "2", features = ["tray-icon", "protocol-asset"] }
tauri-plugin-shell = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

### `src-tauri/capabilities/default.json`

Declares what the frontend is allowed to do. Tauri 2.0 uses a capability-based
security model:

```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": ["core:default", "shell:allow-open"]
}
```

## Plugin System

Tauri 2.0 plugins are Rust crates registered in `main.rs`:

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_fs::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

Each plugin adds both Rust-side functionality and frontend bindings.
Add plugins via Cargo.toml + register in the builder chain.

## Build Commands

```bash
npm run tauri dev      # Development mode (hot reload)
npm run tauri build    # Production build (creates installer)
cargo build            # Rust-only build (from src-tauri/)
```
