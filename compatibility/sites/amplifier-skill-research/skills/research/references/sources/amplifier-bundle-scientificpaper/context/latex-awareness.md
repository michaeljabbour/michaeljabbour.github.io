# LaTeX Authoring Capability

This bundle includes specialized agents for LaTeX authoring and paper structuring.

## Available Agents

### latex-expert

**When to delegate:** LaTeX compilation, conference formatting, error debugging

Use the latex-expert agent when:
- Compiling LaTeX documents
- Converting between conference formats
- Debugging LaTeX errors
- Applying conference-specific formatting
- Validating document structure

### paper-architect

**When to delegate:** Paper structure planning, outline creation, section organization

Use the paper-architect agent when:
- Planning paper structure and outline
- Organizing sections (Introduction, Methods, Results, Discussion)
- Crafting abstracts and contribution statements
- Structuring arguments and flow
- IMRaD methodology guidance

## Capabilities

- **LaTeX compilation** - pdflatex, bibtex, latexmk
- **Multi-conference formatting** - NeurIPS, ICML, IEEE, ACL, ACM, arXiv, Stanford CS
- **Error diagnosis** - Clear explanations of LaTeX errors
- **Template management** - Official style files in `templates/`
- **Paper structure** - IMRaD methodology, abstract composition

## Examples

<example>
user: 'Compile my paper for NeurIPS'
assistant: 'I'll delegate to latex-expert to compile with NeurIPS formatting.'
<commentary>Conference-specific compilation requires the latex-expert's context.</commentary>
</example>

<example>
user: 'Help me structure a paper on neural architecture search'
assistant: 'I'll delegate to paper-architect to design the structure and outline.'
<commentary>Structural planning requires the paper-architect's methodology expertise.</commentary>
</example>

<example>
user: 'I'm getting a LaTeX error about undefined control sequence'
assistant: 'I'll delegate to latex-expert to diagnose and fix the error.'
<commentary>Error debugging requires latex-expert's compilation knowledge.</commentary>
</example>

## Implementation

Both agents are context sinks that load heavy documentation only when spawned. This keeps root sessions lean while providing full expertise when needed.
