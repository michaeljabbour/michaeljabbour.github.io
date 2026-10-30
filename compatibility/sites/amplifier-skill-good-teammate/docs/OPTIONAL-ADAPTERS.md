# Optional coordination and transport adapters

Good Teammate supplies judgment about whom to ask, authority, useful updates, attribution and preserved qualifications. Its portable folder works with a plain file or an existing authorized transport. Installing it does not install a provider, enroll a project or grant permission to contact anyone.

## The retained Collaboration owner

The separate [Collaboration bundle](https://github.com/michaeljabbour/amplifier-bundle-collaboration/tree/d44ab2bf26fd68807b5e0b43fb884301886bac3e) remains the home of its native composition and workflows. Five credited architecture/protocol references are included here; that reference extraction is not a physical merge of its transport implementation.

| Content | Actual retained home | Role and limit |
|---|---|---|
| `bundle.md` | Collaboration source above | Composes separately owned provider modules. A declaration is not proof of a currently configured or tested deployment. |
| `agents/coordinator.md`, `agents/channel-communicator.md`, `agents/document-manager.md`, `agents/setup-assistant.md` | Same source, `agents/` | Native specialist and setup configuration; not required by the portable method. |
| `recipes/collaborative-task.yaml`, `recipes/pickup-task.yaml`, `recipes/task-handoff.yaml` | Same source, `recipes/` | Native multi-instance, document and channel workflows. Current-runner compatibility and authority need their own checks. |
| `scripts/m365_post.py`, `scripts/teams_post.sh` | Same source, `scripts/` | Direct Microsoft Graph/CLI posting utilities. No credential or message operation was performed in this consolidation. |
| `docs/M365_SETUP.md`, `docs/MULTI_INSTANCE.md`, `docs/USAGE_EXAMPLES.md` | Same source, `docs/` | Historical setup and usage references; inspect current provider scopes and SDKs before use. |

## Provider code stays with its owners

Read-only public metadata and source declarations were checked on 2026-10-28:

| Owner | Exact implementation surface | Scope |
|---|---|---|
| [Collaboration core](https://github.com/michaeljabbour/amplifier-collab-core/tree/c474691609721c451800f364bc57b590b383a54f) | `amplifier_module_tool_collab_core/providers/base.py`, `tools/channels.py`, `tools/directory.py`, `tools/documents.py`, `tools/email.py` | Shared `CollaborationProvider` types/interface and callable tool surfaces. The older repository URL redirects to this current owner. |
| [M365 adapter](https://github.com/michaeljabbour/amplifier-module-tool-m365/tree/e112c3b944b02163c82a98c9f4701ca33690966b) | `amplifier_module_tool_m365/providers/m365.py` | Microsoft Graph configuration/provider implementation; retains its own credentials and native package. |
| [Slack adapter](https://github.com/michaeljabbour/amplifier-module-tool-slack/tree/e14fa3c1fd59f82e2882393960352dd8a22e67c9) | `amplifier_module_tool_slack/providers/slack.py` | Slack configuration/provider implementation; interface declarations do not establish every operation is supported. |
| [Google adapter](https://github.com/michaeljabbour/amplifier-module-tool-google/tree/878dd6b217784329aa9cfb725a4fe5a5af9e25ff) | `amplifier_module_tool_google/providers/google.py` | Google Workspace service-account/provider implementation; authorization and product availability are separate checks. |

These are retained infrastructure owners, not new method brands or mandatory dependencies. This pass inspected repository trees and provider declarations; it did not instantiate providers, read credentials, send messages, upload documents or establish live API support. No tests directory was present in the inspected trees; that observation does not rule out checks elsewhere.

Team Access handles repository/team access operations. It is not a replacement for these messaging/document providers. Good Teammate can share its contribution/meaning contract with either surface while the native code keeps its own owner and lifecycle.

## Before claiming a replacement

Map each tool, native namespace, recipe, credential scope, failure and recovery interface to an actual destination. Validate composition and credential-free fixtures against the current host. A real external action requires the user's existing authorization and evidence of that exact result. Until those gates pass, keep the native Collaboration source and adapters available; reference extraction alone does not justify archival.
