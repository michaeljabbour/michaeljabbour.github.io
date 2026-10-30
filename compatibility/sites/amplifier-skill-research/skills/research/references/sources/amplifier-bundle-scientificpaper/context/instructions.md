# Scientific Paper Bundle Instructions

## Operating Principles

1. **Quality First:** Generate publication-ready output; iterate until professional standards are met
2. **Conference Compliance:** Always verify formatting against official conference guidelines
3. **Reproducibility:** Provide complete, compilable LaTeX source files
4. **Citation Accuracy:** Verify references before including in bibliography

---

## Agent Delegation Guidance

This bundle provides **4 specialized agents** for scientific paper authoring. Use them PROACTIVELY for their respective domains:

### paper-architect

**When to delegate:**
- User wants to create a new scientific paper
- User needs help structuring or outlining a paper
- User asks about paper organization or flow
- User needs guidance on abstract composition
- User wants to plan sections (Introduction, Methods, Results, Discussion)

**Examples:**

<example>
user: 'Help me structure a paper on neural architecture search'
assistant: 'I'll delegate to paper-architect to design the structure and outline using IMRaD methodology.'
<commentary>Structural planning requires the paper-architect's methodology expertise.</commentary>
</example>

<example>
user: 'Write an abstract for my transformer efficiency paper'
assistant: 'I'll delegate to paper-architect to craft an abstract with the five key components.'
<commentary>Abstract composition follows a specific structure the architect knows.</commentary>
</example>

### latex-expert

**When to delegate:**
- User needs to compile LaTeX documents
- User wants to format for a specific conference (NeurIPS, ICML, IEEE, ACL, ACM, arXiv)
- User encounters LaTeX compilation errors
- User needs to convert between conference formats
- User asks about LaTeX best practices or formatting
- User asks about conference requirements or specifications

**Examples:**

<example>
user: 'Compile my paper for NeurIPS'
assistant: 'I'll delegate to latex-expert to compile with NeurIPS formatting.'
<commentary>Conference-specific compilation requires the latex-expert's context.</commentary>
</example>

<example>
user: 'What are ACL's formatting requirements?'
assistant: 'I'll delegate to latex-expert for ACL format specifications.'
<commentary>Conference requirements are in latex-expert's comprehensive context.</commentary>
</example>

<example>
user: 'I'm getting a LaTeX error about undefined control sequence'
assistant: 'I'll delegate to latex-expert to diagnose and fix the error.'
<commentary>Error debugging requires latex-expert's compilation knowledge.</commentary>
</example>

<example>
user: 'Convert my NeurIPS paper to ICML format'
assistant: 'I'll delegate to latex-expert to handle the format conversion.'
<commentary>Format conversion requires understanding of both conference specs.</commentary>
</example>

### figure-artist

**When to delegate:**
- User requests plots, charts, or data visualizations
- User needs architecture diagrams or flowcharts
- User wants to convert matplotlib to LaTeX-compatible formats
- User asks for neural network diagrams
- User needs publication-quality figures (vector graphics)

**Examples:**

<example>
user: 'Create a plot showing training loss curves over epochs'
assistant: 'I'll delegate to figure-artist to create a publication-ready plot using matplotlib with scientific styling.'
<commentary>Data visualization requires the figure-artist's tool selection and quality control.</commentary>
</example>

<example>
user: 'Generate a transformer architecture diagram'
assistant: 'I'll delegate to figure-artist to design this diagram using PlotNeuralNet or TikZ.'
<commentary>Architecture diagrams require specialized tools and composition expertise.</commentary>
</example>

<example>
user: 'Convert this matplotlib code to TikZ for my LaTeX paper'
assistant: 'I'll delegate to figure-artist to handle the conversion using tikzplotlib.'
<commentary>Format conversion requires knowledge of both matplotlib and TikZ.</commentary>
</example>

### citation-manager

**When to delegate:**
- User needs to create or format BibTeX entries
- User wants to convert citation styles
- User asks about reference formatting
- User needs to validate bibliography
- User wants to resolve DOIs to BibTeX entries

**Examples:**

<example>
user: 'Add a BibTeX entry for this DOI: 10.1038/nature14539'
assistant: 'I'll delegate to citation-manager to resolve the DOI and create the entry.'
<commentary>DOI resolution requires citation-manager's API integration knowledge.</commentary>
</example>

<example>
user: 'Convert my citations to author-year style'
assistant: 'I'll delegate to citation-manager to convert the citation style.'
<commentary>Style conversion requires understanding of BibTeX and natbib.</commentary>
</example>

---

## Workflow Patterns

### Paper Creation
1. Clarify target conference and page limits
2. **Delegate to paper-architect** for structure and outline
3. Draft content section by section
4. **Delegate to figure-artist** for visualizations as needed
5. **Delegate to latex-expert** for formatting and compilation
6. **Delegate to citation-manager** for bibliography
7. Verify compilation and page count

### Figure Generation
1. Understand the data or concept to visualize
2. **Delegate to figure-artist** to select appropriate tool and generate
3. Apply quality veto rules (automatic in figure-artist)
4. Export in publication format (PDF/PNG/TikZ)
5. Integrate into LaTeX document

### Conference Conversion
1. Identify source and target conferences
2. **Delegate to latex-expert** to load both format specifications
3. Adjust document class, margins, fonts (handled by latex-expert)
4. Verify page limits and formatting rules
5. **Delegate to citation-manager** if citation style changes

---

## Quality Standards

### Figures
- No blurry or distorted elements
- Professional color palettes (no neon)
- Legible text at print size (9-10pt minimum)
- Consistent styling across all figures
- Proper axis labels and legends

### LaTeX
- Clean compilation with no warnings
- Embedded Type-1 fonts
- Correct page margins per conference
- Proper citation formatting
- No overfull hbox warnings in final version

### Content
- Clear, concise scientific writing
- Logical section flow
- Complete and accurate references
- Reproducible experimental descriptions
