---
name: knowledge
description: "Build and query an inspectable graph of claims, evidence and relationships with source and time attached. Use when asked to ingest, connect, trace, challenge or explore knowledge from supplied material."
---

# Knowledge

Use the retained knowledge CLI or knowledge.lib. Run knowledge --help and knowledge <capability> --help for exact arguments. Its deterministic core uses Python and SQLite; model-backed extraction, reconciliation and answers are optional capabilities.

Build: choose the graph explicitly, preserve source identity and distinguish cooccurrence from an asserted semantic relationship. knowledge ingest --method cooccurrence provides a no-model path; use add for already structured evidence. Inspect extraction provenance before treating edges as facts.

Investigate: use path, evidence, contradictions, gaps and timeline to test a specific question. Read references/graph.v1.md when interpreting validity windows. Search rank and graph centrality are navigation signals. Candidate contradictions need judgment; a structural gap does not establish a scientific research gap. Supersede an obsolete relation instead of erasing its history.

Explore: generate the self-contained viewer or export the graph as documented in references/cli.v1.md. Numbered source passages support an answer; community summaries are navigation aids. Do not send private graph content to a provider without authorization. A host completion command is optional; deterministic graph reads require no API key.

The graph library, analysis algorithms, SQLite store, adapters, viewer and existing records are retained. Knowledge owns graph relationships; it does not absorb the separate general storage capability or silently migrate Memory.
