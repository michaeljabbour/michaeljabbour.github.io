---
name: imagen-studio
description: Use when directing an image, choosing and refining concrete drafts, delivering an artifact pack, or converting image and ASCII art.
license: MIT
---

# Imagen Studio

Direct the image, choose the draft, and refine the actual file.

## Select the smallest useful route

Honor an explicit mode. Otherwise use **Fast** for one clear low-risk task, **Guided** for a meaningful ambiguity, and **Studio** for campaigns/batches, consequential edits, costly work, or reference assets. Use **ASCII** when characters are the intended medium; an existing source can be converted entirely locally. Do not generate an image merely because generation is available.

Read the relevant procedure: [visual-asset production](references/design-visual-asset.md), [image/ASCII conversion](references/image-ascii-art.md), and [production policy](references/image-production-policy.md). The original detailed production guide retains versioned provider examples; do not copy their parameters without checking the mounted schema and current provider documentation. The [router](references/imagen-awareness.md) and [artifact schema](references/artifact-manifest.schema.json) are generated from the retained native sources. For the native adapter read [MCP boundary](references/mcp-boundary.md).

## Direct, approve, and refine artifacts

Normalize the brief into intended use, scene/subject, style, dimensions/safe areas, literal text, source references, preserve constraints, acceptance criteria, and approver. Use an available specialist only when its judgment resolves a real ambiguity. A fully specified Fast request does not need a full delegation pipeline.

Before a Studio generation, show the brief, available provider/model and parameters, draft count, approximate cost, and relevant source-data handling; use the existing user authorization or obtain approval at that boundary. Keep drafts separate, labeled and hashed. Show previews and obtain the user's concrete selection. Do not silently choose a winner or reinterpret a selected prompt as approval of every future output.

Refine the selected file or last accepted ancestor. Preserve geometry, identity, literal text, or other user constraints explicitly. A fundamentally new composition or rerender is a new candidate requiring its own review. Retain rejected branches and error state without overwriting the accepted source. Follow the source workflow's bounded direction loops; do not retry indefinitely or change provider to evade a content decision.

## Inspect the file you will deliver

Technical facts require actual bytes: format, dimensions, hash, file path, parent, parameters, and any processed metadata. Visual QA requires the exact pixels in a vision-capable context. A successful write, filename, hash, or serialized base64 text is not visual access. When pixels cannot be reviewed, state visual QA pending and show the file for human review; do not invent a pass.

Deliver the exact candidate with useful preview, stable file, concise alt text, transcript of literal on-image text, lineage/manifest, and actual QA/approval status. Do not claim a provenance credential, watermark state, authenticity, or metadata removal unless it was produced and checked. The schema is a record shape, not cryptographic proof of approval.

## ASCII work

Read the ASCII reference and run `python3 scripts/asciiart.py --help` from the installed skill folder. Conversion needs Pillow, but no provider/server. Choose width, character aspect, luminance ramp, inversion, contrast, and output form for the intended display. For a weak rendering first inspect source contrast/composition; do not repeatedly change a ramp to conceal a poor source. A rasterized ASCII image remains a separate artifact. Generation or provider upload is optional and separately authorized.

## Execution and evidence boundary

If a needed tool/server is missing, return the concrete brief, local conversion, or blocked execution step. Do not install a provider or upload sources implicitly. Native tools are discovered against an eight-name reviewed allowlist, use mounted argument schemas, and retain lifecycle/error/cleanup behavior. Software fixtures and the retained deterministic policy gate are not proof every model follows these instructions, and prior provider canaries are historical results rather than a new live check.
