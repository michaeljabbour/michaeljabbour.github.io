# PaperBanana Methodology

**Source:** arXiv 2601.23265 - "PaperBanana: Automating Academic Illustration for AI Scientists"
**Authors:** Dawei Zhu, Rui Meng, Yale Song, Xiyu Wei, Sujian Li, Tomas Pfister, Jinsung Yoon
**Affiliations:** Peking University, Google Cloud AI Research

---

## Overview

PaperBanana is a multi-agent framework for automating the generation of publication-ready academic illustrations. It addresses the final major bottleneck in AI-driven research workflows: creating high-quality figures and diagrams for research papers.

**Key Innovation:** Orchestrates specialized agents to handle different aspects of figure generation, with iterative refinement through self-critique.

**Coverage:**
- Methodology diagrams (system architecture, pipelines)
- Statistical plots (training curves, comparison charts)
- Architecture diagrams (neural networks, model structures)

---

## Multi-Agent Architecture

PaperBanana uses a **five-agent collaborative system** where each agent specializes in one aspect of figure generation.

### 1. Retriever Agent

**Purpose:** Extract relevant information from paper content

**Capabilities:**
- Semantic search through paper sections (abstract, methods, results)
- Identify key concepts, methods, and results
- Extract data for visualization
- Reference similar figures from literature (optional)
- Build terminology dictionary for labels

**Input:** Paper text (typically abstract + methods sections)

**Output:** Structured context with:
- Key concepts (technical terms, proper nouns)
- Methodology description
- Relationships between concepts (for diagram arrows)
- Terminology definitions (for tooltips/legends)
- Visual elements needed (boxes, arrows, graphs)

**Implementation:** `tool_paperbanana/retriever.py`

### 2. Planner Agent (Content)

**Purpose:** Determine what elements should be included in the figure

**Capabilities:**
- Identify essential vs. extraneous information
- Maintain faithfulness to paper content (avoid hallucination)
- Ensure conciseness (avoid clutter)
- Plan visual hierarchy (what's primary vs. secondary)
- Map relationships for connections (arrows, edges)

**Input:** Context from Retriever

**Output:** Content plan with:
- Elements to include (limited to ~8 for clarity)
- Hierarchy (priority levels)
- Relationships (source → target pairs)
- Labels (text for each element)

**Implementation:** `tool_paperbanana/planner.py` (plan_content method)

### 3. Stylist Agent (Style Planning)

**Purpose:** Design visual aesthetics

**Capabilities:**
- Select color schemes (ColorBrewer palettes, colorblind-safe)
- Choose fonts and typography (conference-appropriate)
- Determine layout and composition (horizontal/vertical/grid)
- Apply conference-specific styling (NeurIPS, ICML, ACL, IEEE, ACM)
- Calculate appropriate dimensions (column vs. page width)

**Input:**
- Context from Retriever
- Style requirements (conference, colorblind_safe, width)

**Output:** Style plan with:
- Color scheme (hex codes)
- Font family and size
- Layout type
- Dimensions (width × height in inches)
- Output format (PDF/SVG/TikZ/PNG)

**Conference Specifications:**

| Conference | Column Width | Page Width | Preferred Fonts |
|------------|--------------|------------|-----------------|
| NeurIPS    | 5.5"         | 5.5"       | Times, Computer Modern |
| ICML       | 3.25"        | 6.75"      | Times |
| ACL        | 3.33"        | 6.75"      | Times |
| IEEE       | 3.5"         | 7.0"       | Times |
| ACM        | 3.33"        | 6.75"      | Libertine |

**Implementation:** `tool_paperbanana/planner.py` (plan_style method)

### 4. Visualizer Agent

**Purpose:** Generate the actual figure

**Capabilities:**
- Render methodology diagrams (boxes, arrows, pipelines)
- Create statistical plots (training curves, bar charts)
- Generate architecture diagrams (neural networks, layers)
- Support multiple output formats (PDF, TikZ, SVG, PNG)
- Apply style plan (colors, fonts, layout)
- Position elements based on layout type

**Layout Types:**

**Horizontal (Pipeline):**
```
┌──────┐    ┌──────┐    ┌──────┐
│Stage1│ -> │Stage2│ -> │Stage3│
└──────┘    └──────┘    └──────┘
```

**Vertical (Architecture):**
```
┌─────────────┐
│   Layer 3   │
├─────────────┤
│   Layer 2   │
├─────────────┤
│   Layer 1   │
└─────────────┘
```

**Grid (Network):**
```
○──○──○
│  │  │
○──○──○
│  │  │
○──○──○
```

**Input:**
- Content plan (what to include)
- Style plan (how to render)

**Output:** Figure object with:
- File path
- Format
- Dimensions
- Metadata (num_elements, layout)

**Implementation:** `tool_paperbanana/visualizer.py`

### 5. Critic Agent

**Purpose:** Quality validation and refinement guidance

**Capabilities:**
- Apply 8 quality veto rules (see below)
- Generate structured critique
- Identify specific improvement areas
- Track refinement iterations
- Calculate severity (pass/minor/major/critical)

**Input:**
- Generated figure
- Quality rules to enforce

**Output:** Critique with:
- Overall pass/fail status
- Rules passed/failed
- Issues list (with severity)
- Human-readable summary
- Severity level

**Implementation:** `tool_paperbanana/critic.py`

---

## Quality Veto Rules (Red Lines)

8 non-negotiable quality standards from PaperBanana research:

### 1. No Low-Quality Artifacts
**Rule:** Avoid grid artifacts, blur, distorted shapes, or pixelation
**Rationale:** Artifacts indicate low-quality generation and appear unprofessional
**Check:** Inspect image for visible quality degradation
**Severity if failed:** Major

### 2. Professional Colors
**Rule:** No jarring neon colors, use ColorBrewer palettes, ensure good contrast
**Rationale:** Neon colors are harsh and unprofessional; poor contrast reduces readability
**Check:** Verify color palette is from ColorBrewer or similar professional set
**Severity if failed:** Major

### 3. No Black Backgrounds
**Rule:** Use white or light backgrounds only
**Rationale:** Black backgrounds are considered unprofessional in academic papers and waste ink
**Check:** Verify background color is white or light (RGB > 200)
**Severity if failed:** Major

### 4. Modern Style
**Rule:** Appropriate fonts (Times, Helvetica), minimal clip-art, no Comic Sans
**Rationale:** Outdated styles or excessive decoration detract from scientific content
**Check:** Verify font family is professional and decoration is minimal
**Severity if failed:** Minor

### 5. Vector Preferred
**Rule:** Use PDF/SVG/TikZ over PNG when possible
**Rationale:** Vector formats scale without quality loss and are standard for publications
**Check:** Verify output format is vector (PDF/SVG/TikZ)
**Severity if failed:** Minor

### 6. Appropriate Aspect Ratio
**Rule:** Match conference column/page width requirements
**Rationale:** Extreme aspect ratios don't fit publication layouts and may be rejected
**Check:** Verify aspect ratio is between 0.3 and 3.0
**Severity if failed:** Major

### 7. Clear Labels
**Rule:** All text, axes, legends must be legible at print size (≥8pt at final size)
**Rationale:** Illegible labels render the figure useless
**Check:** Verify figure dimensions allow for readable text (min 2" × 1.5")
**Severity if failed:** Major

### 8. Data Integrity
**Rule:** Accurate representation of data, no misleading visualizations
**Rationale:** Scientific integrity requires faithful data representation
**Check:** Verify data is not distorted, truncated, or misrepresented
**Severity if failed:** Critical

---

## Quality Evaluation Metrics

PaperBanana evaluates figures on **4 dimensions** (from PaperBananaBench):

### 1. Faithfulness
- Does the figure accurately represent the paper content?
- Are all included elements relevant and correct?
- No hallucinated or fabricated information?

### 2. Conciseness
- Are unnecessary elements excluded?
- Is visual hierarchy clear (focus on important elements)?
- Is the figure cluttered or clean?

### 3. Readability
- Are labels clear and legible?
- Is color contrast sufficient?
- Is the layout intuitive?

### 4. Aesthetics
- Does the figure look professional?
- Are colors harmonious?
- Is the style modern and appropriate?

---

## Iterative Refinement Process

PaperBanana uses a **closed-loop refinement** approach:

```
1. Generate Initial Figure
        ↓
2. Apply Critic (8 veto rules)
        ↓
3. All rules passed? → DONE ✓
        ↓ (Some rules failed)
4. Refine Based on Critique
        ↓
5. Increment iteration counter
        ↓
6. Reached max_iterations? → STOP (return best attempt)
        ↓ (No, continue)
   Go to step 2
```

**Default:** 3 maximum iterations

**Stopping Conditions:**
- All quality rules pass → Success ✓
- Max iterations reached → Return best attempt (may have issues)

**Refinement Strategies:**
- Failed "colors" → Swap to different ColorBrewer palette
- Failed "aspect_ratio" → Adjust figure dimensions
- Failed "labels" → Increase font size or figure size
- Failed "artifacts" → Switch to vector format

---

## Implementation in tool-paperbanana

The tool module implements this architecture with clear separation:

```
tool_paperbanana/
├── mount.py          # Orchestrator - coordinates all agents
├── retriever.py      # Stage 1: Context extraction
├── planner.py        # Stages 2-3: Content + style planning
├── visualizer.py     # Stage 4: Figure generation
├── critic.py         # Stage 5: Quality validation
└── utils.py          # Shared data structures and constants
```

**Key Design Decisions:**

1. **Synchronous orchestration** - Each stage completes before next begins
2. **matplotlib-based** - Uses matplotlib for generation (reliable, no external APIs)
3. **Configurable quality rules** - Can enable/disable specific veto rules
4. **Conference-aware** - Automatically adapts to target conference specs
5. **Self-contained** - All logic in Python, no external services required

---

## Usage Patterns

### Pattern 1: Simple Agent Use

```
"Create a methodology diagram for my transformer paper"
```

**Flow:**
1. figure-artist agent receives request
2. Decides to use tool-paperbanana (complex diagram)
3. Extracts paper content from context
4. Calls tool-paperbanana with defaults
5. Returns generated figure with LaTeX integration code

### Pattern 2: Direct Tool Use

```python
result = tool.execute({
    "paper_content": "Abstract: ...\nMethods: ...",
    "figure_type": "methodology",
    "style_requirements": {
        "conference": "neurips",
        "colorblind_safe": True,
        "width": "page"
    },
    "quality_rules": ["no_low_quality_artifacts", "professional_colors", ...],
    "max_iterations": 3
})
```

**Flow:**
1. Direct tool invocation
2. Full control over all parameters
3. Returns detailed metadata about iterations and quality checks

### Pattern 3: Recipe Workflow

```bash
amplifier run "execute recipes/paperbanana-figure.yaml with \
  paper_content='...' \
  figure_type='methodology' \
  conference='neurips'"
```

**Flow:**
1. **Stage 1 (Planning):** Extract context, plan figure, request approval
2. **[Approval Gate]** User reviews plan
3. **Stage 2 (Generation):** Generate figure, validate quality
4. **Stage 3 (Refinement):** If quality issues, refine and re-validate

---

## Integration with figure-artist Agent

The figure-artist agent uses tool-paperbanana **intelligently**:

### When to Use PaperBanana

✅ **Use for:**
- Complex methodology diagrams requiring multiple refinement iterations
- User explicitly requests "PaperBanana-style" or "automated refinement"
- Figures that must meet strict publication quality standards
- Architecture diagrams for academic papers
- When automatic quality validation is needed

❌ **Don't use for:**
- Simple training curves, bar charts, scatter plots
- User has specific matplotlib/seaborn requirements
- Need fine-grained control over every plot element
- Quick prototyping or draft figures

### Decision Logic

```python
if "methodology" in request or "architecture" in request:
    use_paperbanana = True
elif "quality" in request or "publication-ready" in request:
    use_paperbanana = True
elif "automated refinement" in request or "paperbanana" in request:
    use_paperbanana = True
else:
    # Use matplotlib/seaborn directly for simpler plots
    use_paperbanana = False
```

---

## Comparison with Other Approaches

| Approach | Strengths | Weaknesses | Best For |
|----------|-----------|------------|----------|
| **PaperBanana** | Automated refinement, quality guarantees, publication-ready | Slower (iterative), less control | Complex diagrams, final figures |
| **matplotlib** | Fast, full control, familiar API | Manual refinement, no quality checks | Data plots, quick drafts |
| **TikZ** | Perfect for LaTeX, mathematical diagrams | Steep learning curve, manual coding | Mathematical diagrams, precise control |
| **PlotNeuralNet** | Specialized for NN diagrams | One-trick pony (only NN architectures) | Neural network architectures |

---

## Benchmark: PaperBananaBench

The original PaperBanana paper introduced a benchmark with:

- **292 test cases** from NeurIPS 2025 papers
- **4 evaluation dimensions:** Faithfulness, Conciseness, Readability, Aesthetics
- **Human evaluation:** Expert judges rate generated figures

**Key Results:**
- PaperBanana consistently outperforms baseline approaches
- Iterative refinement improves quality scores by ~20%
- Quality veto rules reduce rejection-worthy issues by ~80%

---

## References

- **Paper:** https://arxiv.org/abs/2601.23265
- **Project Website:** https://dwzhu-pku.github.io/PaperBanana/
- **Research Notes:** @scientificpaper:research/arxiv-paper-research.md
- **Tool Implementation:** @scientificpaper:modules/tool-paperbanana/
- **Behavior Bundle:** @scientificpaper:behaviors/paperbanana.yaml
- **Recipe:** @scientificpaper:recipes/paperbanana-figure.yaml

---

## Future Enhancements

Potential improvements for Phase 2:

1. **Gemini API Integration** - Use Gemini-3-Pro as VLM judge (as in original paper)
2. **Specialized Agents** - Break out into 5 separate agent files for fine-grained control
3. **TikZ Generation** - Native TikZ code generation (not just matplotlib→tikzplotlib)
4. **Reference-Driven** - Learn from curated examples from top-tier papers
5. **Advanced Layouts** - Support for multi-panel figures, complex compositions

---

**Status:** Phase 1 complete - tool operational with matplotlib-based generation and all 8 quality veto rules.
