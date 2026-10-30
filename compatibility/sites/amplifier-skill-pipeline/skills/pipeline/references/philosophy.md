# CI/CD Bundle Philosophy

These principles govern every pipeline this bundle designs, generates, or audits.

## Pipeline Design and Rendering Are Separate Concerns

The Abstract Pipeline Representation (APR) captures *what* a pipeline does. Platform-specific configs capture *how* a particular CI/CD system expresses it. These two concerns must never be conflated.

Designing a pipeline means choosing stages, jobs, triggers, caching strategies, and security gates. Rendering a pipeline means translating those choices into GitHub Actions YAML, GitLab CI syntax, or Azure DevOps templates.

The APR is the single source of truth. Platform configs are derived artifacts.

## Detect, Don't Assume

The bundle inspects the project to infer what it needs — languages, frameworks, build tools, test runners, Docker presence, existing CI configs. It never assumes a project uses a particular stack.

When detection can't answer a question (deployment targets, branching strategy, environment promotion), the bundle asks. It does not guess. The hybrid Q&A model means: auto-detect what you can, ask only what you can't infer.

## Composability Over Hardcoding

The stage library is a collection of composable primitives, not a fixed pipeline template. Each stage primitive (build/docker, test/unit, security/sast) is self-contained and selected based on what the project actually needs.

Adding a new stage = writing a new context file. Adding a new platform = writing new platform context files. No agent code changes required for either.

## Platform Knowledge Is Data, Not Code

Platform-specific knowledge (GitHub Actions syntax, GitLab CI idioms, Azure DevOps templates) lives in context files, not in agent logic. The Platform Generator is one agent that loads different context files depending on the target platform.

This means platform support scales with content, not with code.

## Security-Aware Secrets Management

The bundle follows a try-active, fallback-to-guidance pattern for secrets:

- When it has secure access (authenticated CLI, appropriate permissions), it configures secrets directly
- When it can't verify security, it produces a setup checklist with platform-specific instructions
- It never asks for secret values — values never pass through agent context
- Every secret is classified by sensitivity (low/medium/high) with different handling for each

## Living Pipelines

A pipeline is not "done" after initial generation. The bundle supports revisiting, auditing, and optimizing pipelines over their lifetime. The APR enables drift detection — comparing intended pipeline design against actual platform configs.

## Scope Discipline

This bundle generates CI/CD pipeline configs. It does not generate cloud infrastructure, deployment targets, or application code. Pipeline deployment steps *reference* targets but the bundle stays in its lane.
