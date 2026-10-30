# Component Catalog: amplifier-bundle-collaboration

> **Generated:** 2026-01-20 | **Phase:** 1 of 3 (Documentation Sprint)

## Overview

The Amplifier Collaboration Bundle enables multi-instance AI coordination through enterprise platforms (Microsoft 365, Slack, Google Workspace). This document catalogs all components in the bundle.

---

## Bundle Structure

```
amplifier-bundle-collaboration/
├── bundle.md                    # Main bundle definition
├── README.md                    # User documentation
├── ARCHITECTURE.md              # Technical architecture diagrams
│
├── agents/                      # Specialized AI personas
│   ├── setup-assistant.md       # Platform setup guide
│   ├── coordinator.md           # Multi-instance orchestration
│   ├── document-manager.md      # File/artifact operations
│   └── channel-communicator.md  # Messaging specialist
│
├── behaviors/                   # Reusable behavior definitions
│   ├── collaboration-protocol.md    # Channel communication patterns
│   └── workspace-conventions.md     # File organization standards
│
├── context/                     # Injected context files
│   └── collaboration-instructions.md  # Tool usage guide
│
├── recipes/                     # Multi-step workflows
│   ├── collaborative-task.yaml  # Full task with status posting
│   ├── task-handoff.yaml        # Create and post handoff
│   └── pickup-task.yaml         # Claim and continue work
│
├── docs/                        # Extended documentation
│   ├── M365_SETUP.md           # Microsoft 365 setup guide
│   └── MULTI_INSTANCE.md       # Coordination patterns
│
└── scripts/                     # Utility scripts
    ├── teams_post.sh           # Post to Teams via az CLI
    └── m365_post.py            # Python Teams posting utility
```

---

## Component Details

### 1. Bundle Definition (`bundle.md`)

| Property | Value |
|----------|-------|
| **Name** | `collaboration` |
| **Version** | 1.0.0 |
| **Description** | Multi-instance AI collaboration via M365, Slack, Google |

**External Module Dependencies:**
| Module | Source | Purpose |
|--------|--------|---------|
| `tool-collab-core` | git+github.com/michaeljabbour/amplifier-module-tool-collab-core | Shared interfaces |
| `tool-m365` | git+github.com/michaeljabbour/amplifier-module-tool-m365 | Microsoft 365 provider |
| `tool-slack` | git+github.com/michaeljabbour/amplifier-module-tool-slack | Slack provider |
| `tool-google` | git+github.com/michaeljabbour/amplifier-module-tool-google | Google Workspace provider |

---

### 2. Agents

| Agent | File | Purpose | Behaviors |
|-------|------|---------|-----------|
| **setup-assistant** | `agents/setup-assistant.md` (15.5KB) | Walks users through platform setup | None (standalone) |
| **coordinator** | `agents/coordinator.md` (1.9KB) | Orchestrates multi-instance workflows | collaboration-protocol, workspace-conventions |
| **document-manager** | `agents/document-manager.md` (1.8KB) | File operations specialist | workspace-conventions |
| **channel-communicator** | `agents/channel-communicator.md` (2.1KB) | Messaging specialist | collaboration-protocol |

---

### 3. Behaviors

| Behavior | File | Purpose |
|----------|------|---------|
| **collaboration-protocol** | `behaviors/collaboration-protocol.md` (2.4KB) | Defines channel usage patterns and message formats |
| **workspace-conventions** | `behaviors/workspace-conventions.md` (1.9KB) | Defines folder structure and file naming |

---

### 4. Recipes

| Recipe | File | Inputs | Steps | Purpose |
|--------|------|--------|-------|---------|
| **collaborative-task** | `recipes/collaborative-task.yaml` (2.0KB) | task_description, notify_channel, share_artifacts | 4 | Execute task with full status posting |
| **task-handoff** | `recipes/task-handoff.yaml` (1.6KB) | task_name, current_status, reason, next_steps | 2 | Create handoff doc and post to channel |
| **pickup-task** | `recipes/pickup-task.yaml` (2.3KB) | auto_claim | 5 | Scan handoffs, claim task, continue work |

---

### 5. Tools (via modules)

| Tool | Operations | Platform |
|------|------------|----------|
| `collab_channels` | list, read, post | All |
| `collab_documents` | list, upload, download | All |
| `collab_directory` | list_users, get_user | All |
| `collab_email` | send | M365, Google |

---

### 6. Channel Architecture

| Channel | Purpose | Message Types |
|---------|---------|---------------|
| `general` | Status broadcasts | 🚀 Starting, ✅ Complete, 📢 Update |
| `alerts` | Urgent issues | 🚨 Alert, ⚠️ Warning |
| `handoffs` | Task transfers | 🔄 Handoff, ✋ Claimed |

---

### 7. Document Conventions

**Folder Structure:**
```
Amplifier/
├── inbox/           # Tasks waiting pickup
├── in-progress/     # Currently active
├── completed/       # Finished artifacts
├── handoffs/        # Handoff context docs
└── shared/          # Reusable templates
```

**File Naming:** `[date]_[type]_[description].[ext]`
- Types: `report`, `handoff`, `data`, `draft`

---

## Statistics

| Category | Count |
|----------|-------|
| Agents | 4 |
| Behaviors | 2 |
| Recipes | 3 |
| Documentation files | 5 |
| Total lines of YAML (recipes) | ~150 |
| Total lines of Markdown (docs) | ~1,000 |

---

## Next Steps (Phase 2)

Document the provider interfaces:
- `CollaborationProvider` base class
- `M365Provider` implementation
- `SlackProvider` implementation
- `GoogleProvider` implementation

---

*Generated as part of the Codebase Documentation Sprint*
