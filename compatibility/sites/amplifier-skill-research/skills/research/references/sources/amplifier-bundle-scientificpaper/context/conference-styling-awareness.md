# Conference Styling Capability

This bundle supports multiple conference formats with official style files and conversion capabilities.

## Supported Conferences

- **NeurIPS** - Neural Information Processing Systems
- **ICML** - International Conference on Machine Learning
- **ACL** - Association for Computational Linguistics
- **IEEE** - IEEE Transactions and Conferences
- **ACM** - ACM SIGCHI and other ACM venues
- **arXiv** - arXiv preprint formatting
- **Stanford CS** - Stanford Computer Science thesis formatting

## When to Use Conference Formatting

Delegate to the **latex-expert** agent (from latex-authoring behavior) when:
- Creating a new paper in a specific conference format
- Converting an existing paper between formats
- Validating conference-specific requirements
- Debugging format-related LaTeX errors

## Key Format Differences

| Conference | Paper Size | Columns | Font Size | Citation Style |
|------------|-----------|---------|-----------|----------------|
| NeurIPS | US Letter | Single | 10pt Times | Flexible |
| ICML | US Letter | Two | 10pt Times | Numbered |
| ACL | **A4** ⚠️ | Two | 11pt Times | Author-year |
| IEEE | Letter/A4 | Two | 10pt Times | Numbered [1] |
| ACM | US Letter | Two | 9pt Serif | Numbered |

**Critical:** ACL requires A4 paper size (not US Letter)!

## Examples

<example>
user: 'Format this paper for NeurIPS submission'
assistant: 'I'll delegate to latex-expert to apply NeurIPS formatting.'
<commentary>Conference formatting requires latex-expert's template knowledge.</commentary>
</example>

<example>
user: 'Convert my NeurIPS paper to ICML format'
assistant: 'I'll delegate to latex-expert to handle the format conversion.'
<commentary>Format conversion requires understanding of both conference specs.</commentary>
</example>

## Implementation

Conference format specifications are stored in `context/conference-formats/*.md` and loaded on-demand by the latex-expert agent when needed. Templates are in `templates/*/`.
