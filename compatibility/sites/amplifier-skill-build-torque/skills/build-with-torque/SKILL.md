---
name: build-with-torque
description: Use when designing a Torque domain, authoring a bundle manifest and logic, wiring events/interfaces, or validating integration and schema changes.
license: MIT
---

# Build with Torque

Build a domain that still fits the rest of the application.

## Read the host before proposing a bundle

Inspect its mount plan, installed package versions, neighboring domain manifests, runtime contract tests, and existing registry. State the domain outcome and what is explicitly outside it. Decide whether configuration of an existing bundle is enough or a new domain responsibility is warranted. A shared process does not make private tables or source imports public interfaces.

## Choose the mode

- **Place:** trace domain ownership, data, events, and public query contracts. Use the [registry](references/REGISTRY.md) to understand the package roles, then verify actual availability and versions. Keep the kernel, schema, data layer, event bus, server, shell, CLI, and extensions in their native modules. A new skill is an authoring front door, not a replacement platform.
- **Author:** use the substantial [Bundle Authoring Guide](references/BUNDLE_AUTHORING.md) for manifest, logic class, route/interface implementation, scoped data, events, UI exports, tests, and integration. Read only the sections needed for the task. Use [AI setup context](references/AI_SETUP_PROMPT.md) for orientation; historical install and demo values there are examples, not deployment instructions.
- **Integrate:** declare a mount plan, dependencies, configuration, native gates, schema/data migration, and rollback. Verify on an isolated copy before any existing data changes.

## Preserve the non-obvious contracts

A bundle owns its tables; avoid cross-bundle source imports. Cross-domain calls go through the coordinator and declared dependencies. Public interfaces take named-argument objects; the manifest's query names and the class's implemented interfaces must agree in both directions. Route declarations need corresponding handlers. Authentication, validation, and application authorization are distinct checks; a declaration alone is not proof they ran.

Events describe past-tense facts using the domain/entity namespace, with a declared payload. Subscriptions should match published events and preserve idempotency/recovery assumptions. An optional dependency can be absent: define the degraded behavior and test it. Keep UI component export keys aligned with manifest routes, and use the current shell contract rather than copying another app's internals.

Intents explicitly declare context, allowed tools, goal, success criteria, and required confirmation. Runtime enforcement must be verified against the installed engine; a prompt promise is not a permission boundary. Use the application's existing authorization and provider setup. Do not install an AI runtime merely to author a non-AI domain.

## Prove the slice, then hand it over

Run the native manifest/contract validator and tests available in the host. Check a successful interface call, invalid input, unauthorized request, missing dependency, event reaction, state persistence, and failure recovery where applicable. A mocked unit test is not proof that HTTP, UI, or a real database migration works. For schema changes, retain data snapshot and rollback; a table rebuild rewrites data even when called a type change. Hot reload does not establish a production restart or migration.

Return changed bundle/mount-plan paths, ownership and contract decisions, exact native commands/results, actual runtime scope, migration status, and unresolved evidence. The reference mirrors are generated from the canonical docs with a hash check; edit the docs, not the generated copies. Documentation-content checks establish coverage and packaging, not framework behavior or user benefit.
