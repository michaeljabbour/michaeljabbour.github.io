# Build with Torque

Add a domain without tangling the application.

Watch the [70-second film](https://michaeljabbour.github.io/amplifier-skill-build-torque/#film): a master key into another domain’s tables, and how the skill keeps each domain on its own floor. The example in it is fictional.

An authoring skill for Torque developers. Give a bundle a clear responsibility, connect it through declared interfaces and events, and plan data changes before they reach an existing store.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-build-torque/) · [Read the method](skills/build-with-torque/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Keep domains independent.** Own tables inside a bundle and call other domains through declared coordinator interfaces.
- **Make integration inspectable.** Align manifest queries, routes, handlers, events and UI exports with the installed host contracts.
- **Treat data changes deliberately.** Include migration, restart and rollback in the slice instead of assuming hot reload proves readiness.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-build-torque.git
cd amplifier-skill-build-torque
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/build-with-torque` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use Build with Torque to design a maintenance-task bundle. It should react to asset changes without reading another bundle’s private tables. Inspect this host first, then propose its manifest, public interfaces, events and migration checks.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Place the responsibility.** Inspect the current mount plan and neighboring bundles; decide whether configuration or a new domain is needed.
2. **Author the contract.** Declare data ownership, named inputs, dependencies, events and degraded behavior.
3. **Integrate on an isolated copy.** Exercise success, invalid input, authorization, missing dependencies, persistence and recovery.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional bundle: maintenance tasks
Owns: task records and task state
Depends on: declared asset query interface
Consumes: asset.updated with declared payload
Optional dependency absent: task history still readable
Acceptance: event replay is idempotent; migration can roll back
```

## What is checked

Canonical reference hashes and 106 documentation checks passed. They establish reference coverage, not a deployed framework. Native package availability and app behavior need checking against your installed Torque environment. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Retained implementation and references

[Bundle Authoring](docs/BUNDLE_AUTHORING.md), [Registry](REGISTRY.md), [native platform guide](docs/NATIVE-README.md), [migration](docs/MIGRATION.md) and [validation](docs/VALIDATION.md) retain the substantial Torque references. Canonical reference hashes are checked with `python3 scripts/sync_skill.py --check`. The framework, services and package identities remain independently owned. Native source-URL availability must be checked before attempting the historical setup instructions.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.

<details>
<summary>Retained platform guide (source snapshot)</summary>

These historical native platform instructions are preserved for reference and documentation checks. They are separate from the independently installable authoring skill above. Verify current package and source availability before following them.

# Torque

A composable monolith framework for Node.js. Build full-stack applications by composing independent **bundles** -- each with its own schema, API, events, and UI -- into a single deployable process.

Instead of a monolith that grows into a tangle, or microservices that scatter complexity across the network, Torque gives you **isolated domains in one process** with enforced contracts between them.

## Getting Started

See **[QUICKSTART.md](./QUICKSTART.md)** for the full setup walkthrough.

### Install from npm (recommended)

```bash
npm install -g @torquedev/cli
npm install @torquedev/core @torquedev/schema
```

Then create and run an app:

```bash
torque new zero-to-trello --template kanban
cd zero-to-trello && npm install
AUTH_SECRET=change-me npm run seed
AUTH_SECRET=change-me npm start
```

Open http://localhost:9292 -- log in with `demo@example.com` / `demo1234`.

### Install from source (for contributors)

```bash
mkdir -p ~/torque-dev && cd ~/torque-dev
gh repo clone torque-framework/torque
bash torque/install-dev.sh ~/torque-dev
```

**Prerequisites:** Node.js 22+. GitHub CLI (`gh auth status`) required for source install.

## How It Works

An application is defined by a **mount plan** -- a YAML file that declares which bundles to load:

```yaml
app:
  name: "my-app"

bundles:
  identity:
    source: "git+https://github.com/torque-framework/torque-bundle-identity.git@main"
    config:
      jwt_secret: "${AUTH_SECRET}"

  workspace:
    source: "git+https://github.com/torque-framework/torque-bundle-workspace.git@main"

  kanban:
    source: "git+https://github.com/torque-framework/torque-bundle-kanban.git@main"
```

At boot, the kernel reads the mount plan, resolves bundles from git, creates SQLite tables, wires events, and starts the server. Changing what your app does means editing YAML, not rewriting code.

## Architecture

```
Mount Plan (YAML)
    |
Kernel (resolver -> registry -> boot)        @torquedev/core  @torquedev/schema (type validation)
    |
+----------+----------+----------+
| identity | kanban   | search   |           Bundles (independent git repos)
| JWT auth | cards    | FTS      |
+----------+----------+----------+
    |           |           |
DataLayer    EventBus    Coordinator          Services
 (SQLite)   (pub/sub)   (cross-bundle RPC)
    |
Shell (React + MUI)                          @torquedev/shell-react
```

**Each bundle** is its own git repo containing:
- `manifest.yml` -- declares schema, events, interfaces, routes, and dependencies
- `logic.js` -- implements the bundle's behavior as a single class
- `agent.md` -- (optional) AI agent definition for the bundle's domain

Bundles are isolated by design:
- **No cross-bundle imports** -- bundles never `import` from each other
- **Scoped data access** -- each bundle only sees its own tables
- **Coordinator for RPC** -- cross-bundle calls go through a capability-restricted proxy that enforces declared dependencies at runtime
- **Events for reactions** -- bundles publish facts (past-tense events); other bundles subscribe

## Security & Contract Validation

- **@torquedev/schema runtime validation** -- all bundle inputs and outputs validated against declared schemas at the kernel boundary
- **JWT enforcement** -- identity bundle gates protected routes with signed tokens verified on every request
- **Default deny authorization** -- capability-restricted coordinator blocks undeclared cross-bundle calls; access must be explicitly granted in the manifest
- **HTTP hardening** -- CORS, rate limiting, and input sanitization applied by the server service before requests reach bundle logic
- **SQL safety** -- parameterized queries and scoped table access prevent injection and data leaks across bundle boundaries

## Intents

Torque supports an AI-first development model using intents. Instead of writing routes and controllers, you declare three primitives:

| Primitive | Answers | Example |
|-----------|---------|---------|
| **Context** | *What* data is involved | Schema fields, which fields to vector-index |
| **Behavior** | *How* to execute | Allowed tools, which require human confirmation |
| **Intent** | *Why* -- the goal | Trigger condition, success criteria |

The kernel compiles each Intent into a REST endpoint, an agent tool schema, and a HookBus hook -- automatically. Safety is enforced at runtime (tool allowlists, confirmation gates), not via prompt engineering.

See the [Intents Tutorial](./docs/INTENTS_TUTORIAL.md) for the full walkthrough.

### Agent Runtime

`POST /api/intents/{bundle}/{intent}` triggers a ClaudeRuntime execution via `claude-agent-sdk`. Each request runs a full agent loop: context retrieval, tool calls, confirmation gates, and a structured response. Intents declare their contracts in the manifest:

- **success criteria** — the goal condition the agent must satisfy before returning
- **allowed tools** — an explicit allowlist of bundle methods the agent may call
- **human confirmation** — tools that require user approval before execution

No prompt engineering. Safety is structural.

### Observability & Security

One-line opt-in via `behaviors:` in your mount plan bundle entry:

- **Observability** (`behaviors: [observability]`) — OTel spans on every route and coordinator call, structured JSON logs with trace IDs, automatic trace correlation across bundles
- **Security** (`behaviors: [security-hardened]`) — RBAC role checks before route handlers, rate limiting per user/IP, CSRF validation on state-mutating routes, audit logging of all write operations

## Ecosystem

### Install Modes

| Script | Clones | Use When |
|--------|--------|----------|
| `install.sh` | 4 core repos (torque, core, foundation, cli) | You just want to build apps |
| `install-dev.sh` | All 29 repos + symlinks | You're working on the framework itself |
| `dev-link.sh` | (nothing) | Re-creates `@torquedev/*` symlinks after adding repos |

`install-dev.sh` calls both `install.sh` and `dev-link.sh` internally, so it's the only script you need for a full setup.

### Framework Repos

| Repo | Package | Role |
|------|---------|------|
| [torque](https://github.com/torque-framework/torque) | -- | Entry point, installer, docs |
| [torque-core](https://github.com/torque-framework/torque-core) | `@torquedev/core` | Kernel: resolver, registry, HookBus, intents |
| [torque-foundation](https://github.com/torque-framework/torque-foundation) | `@torquedev/foundation` | Catalog, context docs, agents, recipes |
| [torque-cli](https://github.com/torque-framework/torque-cli) | `@torquedev/cli` | CLI tool: `torque new`, `generate`, `start`, etc. |
| [torque-schema](https://github.com/torque-framework/torque-schema) | `@torquedev/schema` | Type validators and contract checking (zero deps) |

### Services

| Repo | Package | Role |
|------|---------|------|
| torque-service-datalayer | `@torquedev/datalayer` | Bundle-scoped SQLite storage |
| torque-service-eventbus | `@torquedev/eventbus` | Pub/sub with contract validation |
| torque-service-server | `@torquedev/server` | Express + SPA serving + bundle routes |

### UI

| Repo | Package | Role |
|------|---------|------|
| torque-ui-kit | `@torquedev/ui-kit` | Declarative UI element descriptors |
| torque-shell-react | `@torquedev/shell-react` | React + MUI shell with auto-wiring |

### Extensions

| Repo | Package | Role |
|------|---------|------|
| torque-ext-authorization | `@torquedev/ext-authorization` | RBAC role checks |
| torque-ext-soft-delete | `@torquedev/ext-soft-delete` | Soft-delete mixin |
| torque-ext-async-events | `@torquedev/ext-async-events` | Async job queue + retry |
| torque-ext-search | `@torquedev/ext-search` | SQLite FTS5 full-text search |
| torque-ext-storage | `@torquedev/ext-storage` | Local file storage adapter |

### Bundles (13 released)

| Bundle | Description | Depends On |
|--------|-------------|------------|
| identity | Authentication, JWT sessions | -- |
| pipeline | Stage-based workflow engine | -- |
| pulse | Activity timeline | -- |
| tasks | Task management | -- |
| graphql | GraphQL API + GraphiQL | -- |
| workspace | Organizations, members, invites | -- |
| profile | User profiles, preferences | -- |
| admin | Roles, permissions, RBAC | -- |
| search | Full-text search, typeahead | -- |
| boards | Boards within workspaces | workspace |
| kanban | Lists, cards, labels, checklists | boards |
| activity | Activity feed, comments, notifications | kanban, boards |
| realtime | WebSocket broadcast | kanban, boards |

## CLI

```bash
torque new <name> [--template kanban]          # Create a new app
torque generate scaffold <name> <field:type>   # Rails-style CRUD bundle
torque generate bundle <name>                  # Empty bundle skeleton
torque generate intent <bundle> <name>         # Intent triplet (Context + Behavior + Intent)
torque start [--port 9292]                     # Start the server
torque dev                                     # Start with file watching and hot reload
torque validate                                # Check composability contracts
torque doctor                                  # Diagnose common issues
torque info <bundle>                           # Show bundle details
torque console                                 # REPL with live kernel
torque ai "<prompt>"                           # AI assistant with full context
torque list [behaviors|agents|recipes|skills]  # Browse foundation resources
torque recipe execute <name>                   # Run a multi-step workflow
torque update                                  # Pull latest across repos
torque deploy [--plan production]                  # Build & deploy to configured server
torque clean [--deps|--data|--all]             # Remove artifacts
```

See [torque-cli](https://github.com/torque-framework/torque-cli) for full command documentation.

### Integration Testing

For integration tests that run your bundle through real HTTP, install the test helpers package:

```bash
npm install --save-dev @torquedev/test-helpers
```

See the [Bundle Authoring Guide](./docs/BUNDLE_AUTHORING.md#integration-testing) for a full usage example with `createTestApp()`.

## Deployment

Deploy to any VPS with Docker:

```bash
torque deploy
```

This builds a Docker image, transfers it to your server via SSH, and starts the container. Configure in `config/deploy.yml`:

```yaml
server: 203.0.113.10
user: deploy
port: 9292
env:
  AUTH_SECRET: ${AUTH_SECRET}
  NODE_ENV: production
```

By default, `torque deploy` uses `docker save | ssh docker load` — no registry needed. Add `registry: ghcr.io/your-org` to use push/pull instead.

The generated `Dockerfile` mounts `/app/data` as a volume so your SQLite database persists across deploys.

## API Documentation

Torque auto-generates API documentation from your bundle manifests.

| Endpoint | Description |
|----------|-------------|
| `GET /openapi.json` | Machine-readable OpenAPI 3.0 spec covering all mounted bundle routes |
| `GET /api/docs` | Interactive Swagger UI (requires `swagger-ui-dist` in your project) |

Both are generated at boot from the `api.routes` and `validate:` blocks declared in each bundle's manifest. No manual spec maintenance required.

To enable the Swagger UI:

```bash
npm install swagger-ui-dist
```

Then visit `http://localhost:9292/api/docs` after starting the server.

## Updating

Pull latest across all repos:

```bash
bash ~/torque-dev/torque/install-dev.sh ~/torque-dev
```

## Documentation

| Document | Location |
|----------|----------|
| Package Registry | [REGISTRY.md](./REGISTRY.md) |
| Quickstart | [QUICKSTART.md](./QUICKSTART.md) |
| Bundle Authoring Guide | [docs/BUNDLE_AUTHORING.md](./docs/BUNDLE_AUTHORING.md) |
| AI Setup Prompt | [docs/AI_SETUP_PROMPT.md](./docs/AI_SETUP_PROMPT.md) |
| Intents Tutorial | [docs/INTENTS_TUTORIAL.md](./docs/INTENTS_TUTORIAL.md) |
| Design Principles | `torque-foundation/context/DESIGN_PRINCIPLES.md` |
| Domain Conventions | `torque-foundation/context/DOMAIN_CONVENTIONS.md` |
| Event Patterns | `torque-foundation/context/EVENT_PATTERNS.md` |
| Migration Guide | `torque-foundation/context/MIGRATION_GUIDE.md` |
| Bundle Catalog | `torque-foundation/catalog/bundles.yml` |

## License

MIT — see [LICENSE](./LICENSE)

</details>

## Repository migration

This repository was renamed from `amplifier-skill-build-torque` to `amplifier-capability-build-with-torque`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.
