# Provider Interfaces Reference

> **Generated:** 2026-01-20 | **Phase:** 2 of 3 (Documentation Sprint)

This document describes the collaboration provider interfaces implemented by the M365, Slack, and Google modules.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Collaboration Tools                           │
│  collab_channels | collab_documents | collab_directory | email  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 CollaborationProvider (Abstract)                 │
│                      (collab-core module)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ M365Provider  │   │ SlackProvider │   │GoogleProvider │
│  (tool-m365)  │   │ (tool-slack)  │   │(tool-google)  │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Microsoft     │   │    Slack      │   │   Google      │
│ Graph API     │   │    SDK        │   │ Workspace API │
└───────────────┘   └───────────────┘   └───────────────┘
```

---

## Data Models

All providers use these shared data classes from `collab-core`:

### User
```python
@dataclass
class User:
    id: str              # Platform-specific user ID
    display_name: str    # Human-readable name
    email: str | None    # Email address
    department: str | None  # Department/title
```

### Channel
```python
@dataclass
class Channel:
    id: str              # Platform-specific channel ID
    name: str            # Channel name
    description: str | None  # Channel description/purpose
    team_id: str | None  # Parent team/workspace ID
    team_name: str | None  # Parent team name
```

### Message
```python
@dataclass
class Message:
    id: str              # Message ID
    content: str         # Message content (may be HTML)
    sender: str          # Sender display name
    timestamp: str       # ISO timestamp
    channel_id: str | None  # Source channel
```

### Document
```python
@dataclass
class Document:
    id: str              # Document ID
    name: str            # File name
    path: str            # File path/location
    web_url: str | None  # Browser-accessible URL
    size: int | None     # File size in bytes
    is_folder: bool      # True if this is a folder
```

### Task
```python
@dataclass
class Task:
    id: str              # Task ID
    title: str           # Task title
    status: str          # Status (e.g., "complete", "in_progress")
    due_date: str | None # Due date
    assigned_to: str | None  # Assignee
```

---

## CollaborationProvider Interface

The abstract base class defines the contract all providers must implement:

| Category | Method | Description |
|----------|--------|-------------|
| **Directory** | `list_users(limit)` | List organization users |
| | `get_user(user_id)` | Get specific user |
| **Channels** | `list_channels(team_id)` | List available channels |
| | `get_messages(channel_id, limit, team_id)` | Read channel messages |
| | `post_message(channel_name, message, title)` | Post to channel |
| **Documents** | `list_documents(folder_path, site_id)` | List files |
| | `upload_document(name, content, folder_path)` | Upload file |
| | `download_document(document_id)` | Download file content |
| **Tasks** | `list_tasks(plan_id)` | List tasks/work items |
| **Email** | `send_email(to, subject, body, from_user)` | Send email |

---

## Provider Implementations

### M365Provider

**Module:** `amplifier-module-tool-m365`
**Backend:** Microsoft Graph API via `msgraph-sdk`

#### Configuration

| Env Variable | Required | Description |
|--------------|----------|-------------|
| `M365_TENANT_ID` | Yes | Azure AD tenant ID |
| `M365_CLIENT_ID` | Yes | App registration client ID |
| `M365_CLIENT_SECRET` | Yes | App registration secret |
| `M365_TEAMS_WEBHOOKS` | No | Webhook URLs: `general=url1,alerts=url2` |
| `M365_TEAM_ID` | No | Default team for channel operations |

#### Platform Mappings

| Abstract Concept | M365 Implementation |
|------------------|---------------------|
| Users | Azure AD Users |
| Channels | Teams Channels |
| Documents | SharePoint Drive |
| Tasks | Planner Tasks |
| Email | Outlook Mail |

#### Required Permissions (Azure AD)

| Permission | Type | Purpose |
|------------|------|---------|
| `User.Read.All` | Application | List/get users |
| `Group.Read.All` | Application | List teams |
| `Files.ReadWrite.All` | Application | SharePoint operations |
| `Mail.Send` | Application | Send email |
| `ChannelMessage.Read.All` | Application | Read channel messages |

#### Code Example
```python
from amplifier_module_tool_m365 import M365Provider

provider = M365Provider()  # Loads config from env

# List users
users = await provider.list_users(limit=10)

# Post to Teams
await provider.post_message(
    channel_name="general",
    title="Status Update",
    message="Task complete!"
)
```

---

### SlackProvider

**Module:** `amplifier-module-tool-slack`
**Backend:** Slack SDK (`slack_sdk`)

#### Configuration

| Env Variable | Required | Description |
|--------------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Bot user OAuth token (`xoxb-...`) |
| `SLACK_APP_TOKEN` | No | App-level token for Socket Mode |
| `SLACK_WEBHOOKS` | No | Webhook URLs: `general=url1,alerts=url2` |

#### Platform Mappings

| Abstract Concept | Slack Implementation |
|------------------|---------------------|
| Users | Workspace Members |
| Channels | Slack Channels (public/private) |
| Documents | File uploads (limited) |
| Tasks | Not supported |
| Email | Not supported |

#### Required Scopes

| Scope | Purpose |
|-------|---------|
| `users:read` | List/get users |
| `users:read.email` | Get user emails |
| `channels:read` | List channels |
| `channels:history` | Read messages |
| `chat:write` | Post messages |
| `files:read` | Read files |
| `files:write` | Upload files |

#### Code Example
```python
from amplifier_module_tool_slack import SlackProvider

provider = SlackProvider()  # Loads config from env

# List channels
channels = await provider.list_channels()

# Post message
await provider.post_message(
    channel_name="alerts",
    message="🚨 Urgent issue detected"
)
```

---

### GoogleProvider

**Module:** `amplifier-module-tool-google`
**Backend:** Google Workspace APIs (Admin SDK, Chat, Drive, Gmail, Tasks)

#### Configuration

| Env Variable | Required | Description |
|--------------|----------|-------------|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Yes | Path to service account JSON key |
| `GOOGLE_DELEGATED_USER` | No | User email for domain-wide delegation |
| `GOOGLE_CHAT_WEBHOOKS` | No | Webhook URLs: `general=url1,alerts=url2` |

#### Platform Mappings

| Abstract Concept | Google Implementation |
|------------------|----------------------|
| Users | Admin SDK Directory |
| Channels | Google Chat Spaces |
| Documents | Google Drive |
| Tasks | Google Tasks |
| Email | Gmail API |

#### Required Scopes

```python
SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user.readonly",
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat.messages",
    "https://www.googleapis.com/auth/chat.messages.create",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/tasks",
]
```

#### Code Example
```python
from amplifier_module_tool_google import GoogleProvider

provider = GoogleProvider()  # Loads config from env

# List users (requires domain-wide delegation)
users = await provider.list_users(limit=25)

# Upload to Drive
doc = await provider.upload_document(
    name="report.md",
    content="# Report\n...",
    folder_path="Amplifier/completed"
)
```

---

## Provider Comparison

| Feature | M365 | Slack | Google |
|---------|------|-------|--------|
| **Users/Directory** | ✅ Full | ✅ Full | ✅ Full |
| **Channels** | ✅ Teams | ✅ Full | ✅ Chat Spaces |
| **Read Messages** | ✅ | ✅ | ✅ |
| **Post Messages** | ✅ Webhook/API | ✅ Webhook/API | ✅ Webhook/API |
| **Documents** | ✅ SharePoint | ⚠️ Limited | ✅ Drive |
| **Tasks** | ✅ Planner | ❌ | ✅ Tasks |
| **Email** | ✅ Outlook | ❌ | ✅ Gmail |
| **Auth Type** | OAuth2 (App) | Bot Token | Service Account |

---

## Provider Registry

Providers register themselves on import:

```python
# In each provider module's __init__.py:
from amplifier_module_tool_collab_core import register_provider
from .providers.m365 import M365Provider

register_provider("m365", M365Provider)
```

To use a provider:

```python
from amplifier_module_tool_collab_core import get_provider, list_providers

# See what's available
print(list_providers())  # ['m365', 'slack', 'google']

# Get a configured instance
provider = get_provider("m365")
```

---

## Next Steps (Phase 3)

Create usage examples demonstrating:
1. Basic operations per provider
2. Multi-instance handoff workflow
3. Document upload/download patterns
4. Cross-provider compatibility

---

*Generated as part of the Codebase Documentation Sprint*
