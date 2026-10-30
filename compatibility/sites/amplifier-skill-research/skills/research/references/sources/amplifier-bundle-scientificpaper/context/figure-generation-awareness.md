# Figure Generation Capability

This bundle includes the **figure-artist** agent for creating publication-ready scientific figures.

## When to Delegate

Use the figure-artist agent when:
- Creating plots, charts, or data visualizations
- Generating architecture diagrams or flowcharts
- Converting matplotlib plots to LaTeX-compatible formats
- Need publication-quality vector graphics (SVG, PDF, TikZ)
- Creating neural network diagrams
- Designing conceptual illustrations

## Capabilities

### Core Tools
- **Matplotlib + SciencePlots** - Publication-quality plots with scientific styling
- **tikzplotlib** - Seamless Matplotlib → TikZ conversion for LaTeX
- **Seaborn** - Statistical graphics with beautiful defaults
- **TikZ/PGFPlots** - LaTeX-native diagrams and plots

### Specialized Tools
- **PlotNeuralNet** - Neural network architecture diagrams
- **Mermaid** - Fast flowchart and diagram generation
- **Graphviz** - Graph layouts and hierarchies

### Optional Enhancement
- **Gemini Imagen** - Conceptual illustrations (requires API key)
  - ⚠️ Not for data plots or mathematical diagrams
  - Use only for photorealistic/conceptual imagery

## Quality Veto Rules

The figure-artist applies PaperBanana-inspired quality checks:
- ❌ Low-quality artifacts (blurry, distorted, pixelated)
- ❌ Unprofessional colors (neon, jarring combinations)
- ❌ Black backgrounds (unless specifically requested)
- ❌ Text too small to read at publication scale
- ✅ Vector formats preferred (SVG, PDF, TikZ)
- ✅ 300 DPI minimum for raster images

## Examples

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

## Implementation

The figure-artist agent is a context sink that loads heavy imaging documentation only when spawned. This includes matplotlib guides, TikZ patterns, and quality rules.
