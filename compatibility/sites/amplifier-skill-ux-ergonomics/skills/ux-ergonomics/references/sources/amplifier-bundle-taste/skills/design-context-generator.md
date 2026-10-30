---
name: design-context-generator
description: Use when establishing a project's design system — generates a `DESIGN.md` (or `AGENT_DESIGN.md`) reference document encoding the project's color palette, typography stack, spacing scale, component conventions, motion philosophy, and anti-patterns, so subsequent AI sessions can ground UI work in a consistent shared spec without re-deriving the design language each turn.
model_role: creative
---

# Design Context Generator

## Overview
A project's design language drifts every time a new AI session re-derives it from a vague prompt. The fix is the **lock once, reference forever** pattern: produce a single Markdown document that encodes the design system as concrete, AI-readable values (hex codes, font stacks, ms durations, spacing tokens), then have every subsequent session @-mention that document instead of re-inventing the palette.

This skill generates that document. The output is plain Markdown — no proprietary format, no external tool dependency. Any AI session that can read a file can consume it.

## When to Use
- Starting a new project and you want all future UI work to share one design spec.
- Consolidating an existing project whose design language is implicit (scattered across components, never written down).
- **Before invoking taste archetypes** (`minimalist-taste`, `brutalist-taste`, `soft-editorial-taste`). The seed doc lets all subsequent sessions agree on the dial values, palette, and component conventions the archetype is being applied to. Archetype + seed = reproducible output.
- After a significant design pivot, to re-baseline what "the design language" now is.

## What to Generate
The output document MUST contain these sections, with concrete values — never vague descriptors. "Charcoal Ink (#18181B)" not "dark text".

1. **Identity & Vibe** — One paragraph describing atmosphere, density (airy / balanced / dense), variance (symmetric / asymmetric / chaotic), and motion intensity (restrained / fluid / cinematic). Anchors every later decision.
2. **Color Palette** — Each color: descriptive name, hex code, functional role.
   - Canvas, primary surface, secondary surface
   - Primary text (off-black, never pure `#000000`), secondary text, muted text
   - Border / divider colors with explicit alpha
   - Accent color(s) — limit to 1 unless explicitly justified, saturation < 80%
   - Optional state colors (success, warning, error) with paired text colors
3. **Typography** — Concrete font stacks, not vibes.
   - Display / headings: full `font-family` stack, weight range, tracking, line-height
   - Body: stack, base size (px and rem), line-height (target 1.5–1.7), max line-length (~65ch)
   - Monospace: stack, when used (code, metadata, numerics in dense layouts)
   - Type scale: explicit values (e.g., 12 / 14 / 16 / 18 / 24 / 32 / 48 / 64 px or rem)
4. **Spacing Scale** — Named tokens with px values (e.g., `xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 40px, 2xl: 64px, section: 96px+`). Section padding, card padding, inline gap.
5. **Component Conventions** — For each common component, prescribe shape, state behavior, and constraints:
   - Buttons: primary / secondary / ghost. Padding, radius, hover state, active scale, disabled.
   - Form inputs: label position, helper text, error state, focus ring color.
   - Cards / surfaces: radius, border, shadow (with exact rgba), nested-architecture rules.
   - Tags / badges: shape, casing, tracking, allowed colors.
   - Loading / empty / error states: skeletal vs spinner, illustrated empty states, inline error pattern.
6. **Motion Philosophy** — Be specific.
   - Default Framer Motion physics: e.g., `{ stiffness: 100, damping: 20 }`
   - Default easing curve for CSS: e.g., `cubic-bezier(0.16, 1, 0.3, 1)` over 600–800ms
   - Scroll entry: `IntersectionObserver` only — never `window.addEventListener('scroll')`
   - Stagger delays: e.g., 80ms between list items
   - Hard rules: animate only `transform` and `opacity`; no layout-triggering properties
7. **Anti-Patterns (Project-Specific Bans)** — Named, enforceable bans for THIS project. Examples:
   - "No `rounded-3xl` on data tables — only on marketing surfaces."
   - "No `Inter` anywhere — use `Geist` exclusively."
   - "No pure black `#000000` — always `#0A0A0A` or warmer."
   - "No emojis in UI copy — Phosphor icons only."
   - "No `window.scroll` listeners — IntersectionObserver only."
   - Each ban must be checkable by a reviewer with a regex or visual inspection.

## Process
1. **Interview the user** (or read existing source files: `tailwind.config.*`, `theme.ts`, design tokens, a few representative components) to extract the design language.
2. **Draft each section** with concrete values. If the user is vague ("modern, clean"), force them to pick: airy or dense? Sans-only or sans+serif? One accent color — what hex?
3. **Resolve conflicts before writing** — if two extracted values disagree (two different blues in the codebase), pick one and note the choice.
4. **Write the document** as plain Markdown with the section headings above. Each value should be copy-paste usable in CSS / Tailwind / Framer Motion.
5. **Confirm the bans are testable** — every anti-pattern should be something a reviewer or a regex can detect.

## Output Location
- **Default:** `DESIGN.md` at the project root. Visible to teammates, version-controlled, shared spec.
- **Project-private:** `.amplifier/AGENT_DESIGN.md` if the user wants the agent-facing spec separated from any human-facing brand guidelines.

## Companion Usage
Subsequent AI sessions should @-mention the generated file at the start of any UI task: `@DESIGN.md` or `@.amplifier/AGENT_DESIGN.md`. Combined with a taste-skill archetype, this gives the agent both the project's specific values AND the archetype's compositional rules in one context.

## Bans (For This Skill's Output)
- Do **NOT** generate Stitch's proprietary semantic-design-language format or any other tool-specific dialect.
- Do **NOT** depend on any external screen-generation tool, MCP server, or design platform. The output must be readable by any AI session given only a filesystem.
- Do **NOT** emit vague descriptors ("dark blue", "modern font") in place of concrete values. Every color is a hex; every duration is in ms; every spacing is in px or rem.
- Do **NOT** auto-generate component code in this document — it is a spec, not a component library. Code lives in the codebase; this file describes it.
