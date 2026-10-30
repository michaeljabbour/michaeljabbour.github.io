# Matplotlib for Scientific Publications

Complete guide to creating publication-ready figures using matplotlib and SciencePlots.

**Philosophy:** Matplotlib + tikzplotlib is the gold standard for scientific figures. This guide provides templates for all common figure types in ML/AI papers.

---

## Table of Contents

1. [SciencePlots Style Guide](#scienceplots-style-guide)
2. [Configuration and Setup](#configuration-and-setup)
3. [Complete Figure Templates](#complete-figure-templates)
4. [Multi-Panel Figures](#multi-panel-figures)
5. [Color Palettes](#color-palettes)
6. [Conference-Specific Sizing](#conference-specific-sizing)
7. [tikzplotlib Integration](#tikzplotlib-integration)
8. [Common Issues and Fixes](#common-issues-and-fixes)

---

## SciencePlots Style Guide

### Available Styles

```python
import matplotlib.pyplot as plt
import scienceplots

# Core scientific styles
plt.style.use('science')           # Base scientific style
plt.style.use(['science', 'ieee']) # IEEE transactions
plt.style.use(['science', 'nature']) # Nature journal
plt.style.use(['science', 'scatter']) # Scatter plots

# Grid variations
plt.style.use(['science', 'grid'])  # With grid
plt.style.use(['science', 'no-latex']) # Without LaTeX rendering

# Color schemes
plt.style.use(['science', 'bright'])  # Bright colors
plt.style.use(['science', 'vibrant']) # Vibrant colors
plt.style.use(['science', 'muted'])   # Muted colors
plt.style.use(['science', 'high-contrast']) # High contrast
```

### Recommended Combinations

```python
# For NeurIPS/ICML papers
plt.style.use(['science', 'ieee', 'vibrant'])

# For ACL papers
plt.style.use(['science', 'nature', 'bright'])

# For arXiv preprints
plt.style.use(['science', 'grid', 'muted'])

# For colorblind-friendly plots
plt.style.use(['science', 'high-contrast'])
```

---

## Configuration and Setup

### Basic Import Block

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import scienceplots

# Configure matplotlib
plt.style.use(['science', 'ieee'])
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 11,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})
```

### Font Configuration

```python
# For LaTeX-rendered text (recommended)
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Times', 'Computer Modern Roman'],
})

# For non-LaTeX (fallback)
plt.rcParams.update({
    'text.usetex': False,
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial'],
})
```

---

## Complete Figure Templates

### Template 1: Training Curves with Error Regions

```python
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

def plot_training_curves(epochs, train_loss, val_loss, train_std, val_std,
                         save_path='training_curves.pdf'):
    """
    Plot training and validation curves with error regions.

    Args:
        epochs: Array of epoch numbers
        train_loss: Mean training loss per epoch
        val_loss: Mean validation loss per epoch
        train_std: Std dev of training loss
        val_std: Std dev of validation loss
        save_path: Output file path
    """
    fig, ax = plt.subplots(figsize=(3.5, 2.5))

    # Plot lines
    ax.plot(epochs, train_loss, label='Training', linewidth=1.5,
            color='#1f77b4', alpha=0.9)
    ax.plot(epochs, val_loss, label='Validation', linewidth=1.5,
            color='#ff7f0e', alpha=0.9)

    # Add error regions (±1 std)
    ax.fill_between(epochs, train_loss - train_std, train_loss + train_std,
                     alpha=0.2, color='#1f77b4')
    ax.fill_between(epochs, val_loss - val_std, val_loss + val_std,
                     alpha=0.2, color='#ff7f0e')

    # Labels and formatting
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('Training Progress')
    ax.legend(frameon=True, loc='upper right')
    ax.grid(True, alpha=0.3)

    # Optional: Add markers for best validation
    best_idx = np.argmin(val_loss)
    ax.scatter(epochs[best_idx], val_loss[best_idx],
               s=50, color='red', zorder=5, marker='*',
               label=f'Best (epoch {epochs[best_idx]})')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig, ax

# Example usage
epochs = np.arange(1, 101)
train_loss = 2.0 * np.exp(-epochs/30) + 0.1
val_loss = 2.2 * np.exp(-epochs/30) + 0.15 + 0.05 * np.sin(epochs/5)
train_std = 0.1 * np.exp(-epochs/40)
val_std = 0.12 * np.exp(-epochs/40)

plot_training_curves(epochs, train_loss, val_loss, train_std, val_std)
```

### Template 2: Comparison Bar Chart with Error Bars

```python
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

def plot_model_comparison(model_names, accuracies, std_devs,
                          save_path='model_comparison.pdf'):
    """
    Plot model comparison with error bars.

    Args:
        model_names: List of model names
        accuracies: Mean accuracy for each model
        std_devs: Standard deviation for each model
        save_path: Output file path
    """
    fig, ax = plt.subplots(figsize=(4, 2.5))

    x = np.arange(len(model_names))
    width = 0.6

    # Create bars with custom colors
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    bars = ax.bar(x, accuracies, width, yerr=std_devs,
                   color=colors[:len(model_names)],
                   alpha=0.8, capsize=5, ecolor='black',
                   error_kw={'linewidth': 1, 'elinewidth': 1})

    # Add value labels on bars
    for i, (bar, acc, std) in enumerate(zip(bars, accuracies, std_devs)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + std + 0.5,
                f'{acc:.1f}', ha='center', va='bottom', fontsize=8)

    # Highlight best model
    best_idx = np.argmax(accuracies)
    bars[best_idx].set_edgecolor('red')
    bars[best_idx].set_linewidth(2)

    # Formatting
    ax.set_ylabel('Accuracy (\%)')
    ax.set_title('Model Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, rotation=15, ha='right')
    ax.set_ylim(0, max(accuracies) * 1.15)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig, ax

# Example usage
models = ['Baseline', 'CNN', 'ResNet', 'Transformer', 'Ours']
accs = [75.2, 82.4, 87.1, 89.3, 91.7]
stds = [1.2, 0.9, 1.1, 0.8, 0.7]

plot_model_comparison(models, accs, stds)
```

### Template 3: Confusion Matrix Heatmap

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots

plt.style.use(['science', 'ieee'])

def plot_confusion_matrix(cm, class_names, normalize=True,
                          save_path='confusion_matrix.pdf'):
    """
    Plot confusion matrix heatmap.

    Args:
        cm: Confusion matrix (2D array)
        class_names: List of class names
        normalize: Whether to normalize by row
        save_path: Output file path
    """
    fig, ax = plt.subplots(figsize=(4, 3.5))

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        fmt = '.2f'
        vmax = 1.0
    else:
        fmt = 'd'
        vmax = cm.max()

    # Create heatmap
    sns.heatmap(cm, annot=True, fmt=fmt, cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Proportion' if normalize else 'Count'},
                vmin=0, vmax=vmax, ax=ax, linewidths=0.5,
                linecolor='gray')

    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_title('Confusion Matrix')

    # Rotate labels for readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    plt.setp(ax.get_yticklabels(), rotation=0)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig, ax

# Example usage
cm = np.array([[45, 3, 2],
               [2, 48, 0],
               [1, 1, 48]])
classes = ['Class A', 'Class B', 'Class C']

plot_confusion_matrix(cm, classes, normalize=True)
```

### Template 4: Attention Heatmap

```python
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

def plot_attention_heatmap(attention_weights, tokens_in, tokens_out,
                           save_path='attention_heatmap.pdf'):
    """
    Plot attention weights as heatmap.

    Args:
        attention_weights: 2D array (output_len x input_len)
        tokens_in: List of input tokens
        tokens_out: List of output tokens
        save_path: Output file path
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    im = ax.imshow(attention_weights, cmap='viridis', aspect='auto',
                   interpolation='nearest', vmin=0, vmax=1)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Attention Weight', rotation=270, labelpad=15)

    # Set ticks and labels
    ax.set_xticks(np.arange(len(tokens_in)))
    ax.set_yticks(np.arange(len(tokens_out)))
    ax.set_xticklabels(tokens_in, rotation=45, ha='right')
    ax.set_yticklabels(tokens_out)

    # Add text annotations for high attention
    for i in range(len(tokens_out)):
        for j in range(len(tokens_in)):
            if attention_weights[i, j] > 0.5:
                text = ax.text(j, i, f'{attention_weights[i, j]:.2f}',
                              ha='center', va='center', color='white',
                              fontsize=7)

    ax.set_xlabel('Input Tokens')
    ax.set_ylabel('Output Tokens')
    ax.set_title('Self-Attention Weights')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig, ax
```

### Template 5: t-SNE/UMAP Embeddings

```python
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

def plot_embeddings(embeddings, labels, title='t-SNE Visualization',
                   save_path='embeddings.pdf'):
    """
    Plot 2D embeddings colored by class.

    Args:
        embeddings: 2D array (n_samples x 2)
        labels: Class labels (n_samples,)
        title: Plot title
        save_path: Output file path
    """
    fig, ax = plt.subplots(figsize=(4, 3.5))

    unique_labels = np.unique(labels)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))

    for i, label in enumerate(unique_labels):
        mask = labels == label
        ax.scatter(embeddings[mask, 0], embeddings[mask, 1],
                  c=[colors[i]], label=f'Class {label}',
                  alpha=0.6, s=20, edgecolors='none')

    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.set_title(title)
    ax.legend(frameon=True, loc='best', markerscale=1.5)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig, ax
```

### Template 6: Ablation Study Results

```python
import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

def plot_ablation_study(component_names, accuracies, baseline_acc,
                       save_path='ablation_study.pdf'):
    """
    Plot ablation study showing impact of removing components.

    Args:
        component_names: List of component names
        accuracies: Accuracy when component is REMOVED
        baseline_acc: Full model accuracy
        save_path: Output file path
    """
    fig, ax = plt.subplots(figsize=(4, 2.5))

    # Calculate impact (negative means component is helpful)
    impact = np.array(accuracies) - baseline_acc
    x = np.arange(len(component_names))

    # Color bars by impact (red=harmful to remove, gray=neutral)
    colors = ['#d62728' if imp < -0.5 else '#7f7f7f' for imp in impact]

    bars = ax.barh(x, impact, color=colors, alpha=0.7)

    # Add baseline line
    ax.axvline(0, color='black', linestyle='--', linewidth=1,
               label='Full Model')

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, impact)):
        width = bar.get_width()
        ax.text(width - 0.2 if width < 0 else width + 0.2,
                bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', ha='right' if width < 0 else 'left',
                va='center', fontsize=8)

    ax.set_yticks(x)
    ax.set_yticklabels(component_names)
    ax.set_xlabel('Accuracy Change (\%)')
    ax.set_title(f'Ablation Study (Baseline: {baseline_acc:.1f}\%)')
    ax.grid(axis='x', alpha=0.3)
    ax.legend(loc='lower right')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    return fig, ax

# Example usage
components = ['Attention', 'Residual Conn.', 'LayerNorm', 'Dropout']
acc_without = [85.3, 88.1, 87.5, 89.8]
baseline = 91.2

plot_ablation_study(components, acc_without, baseline)
```

---

## Multi-Panel Figures

### Two-Column Layout (Side-by-Side)

```python
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 2.5))

# Left panel: Training curves
ax1.plot(epochs, train_loss, label='Training')
ax1.plot(epochs, val_loss, label='Validation')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('(a) Training Progress')
ax1.legend()

# Right panel: Comparison
ax2.bar(model_names, accuracies)
ax2.set_ylabel('Accuracy (\%)')
ax2.set_title('(b) Model Comparison')
ax2.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('two_panel.pdf', dpi=300, bbox_inches='tight')
```

### Grid Layout (2x2)

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(7, 5))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])  # Top-left
ax2 = fig.add_subplot(gs[0, 1])  # Top-right
ax3 = fig.add_subplot(gs[1, 0])  # Bottom-left
ax4 = fig.add_subplot(gs[1, 1])  # Bottom-right

# Add (a), (b), (c), (d) labels
for i, ax in enumerate([ax1, ax2, ax3, ax4]):
    ax.text(-0.1, 1.05, f'({chr(97+i)})', transform=ax.transAxes,
            fontsize=11, fontweight='bold', va='top')

plt.savefig('grid_layout.pdf', dpi=300, bbox_inches='tight')
```

### Complex Layout (Mixed Sizes)

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(7, 4))
gs = GridSpec(2, 3, figure=fig)

# Large plot on left (spans 2 rows)
ax_main = fig.add_subplot(gs[:, :2])

# Two smaller plots on right
ax_top = fig.add_subplot(gs[0, 2])
ax_bottom = fig.add_subplot(gs[1, 2])

plt.tight_layout()
plt.savefig('complex_layout.pdf', dpi=300, bbox_inches='tight')
```

---

## Color Palettes

### ColorBrewer Palettes (Colorblind-Friendly)

```python
# Qualitative (for categories)
CB_PAIRED = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c',
             '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00']

CB_SET2 = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3',
           '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3']

# Sequential (for heatmaps)
CB_BLUES = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1',
            '#6baed6', '#4292c6', '#2171b5', '#084594']

# Diverging (for positive/negative)
CB_RDBU = ['#67001f', '#b2182b', '#d6604d', '#f4a582',
           '#fddbc7', '#d1e5f0', '#92c5de', '#4393c3',
           '#2166ac', '#053061']

# Usage
plt.plot(x, y1, color=CB_PAIRED[0], label='Model A')
plt.plot(x, y2, color=CB_PAIRED[1], label='Model B')
```

### Scientific Color Cycles

```python
from cycler import cycler

# High-contrast cycle for line plots
line_cycler = cycler(color=['#0173b2', '#de8f05', '#029e73', '#cc78bc',
                             '#ca9161', '#fbafe4', '#949494', '#ece133'])

plt.rc('axes', prop_cycle=line_cycler)
```

---

## Conference-Specific Sizing

### NeurIPS (Single Column, 5.5" wide)

```python
plt.rcParams.update({
    'figure.figsize': (5.5, 3.5),  # Width matches column
    'font.size': 10,
    'axes.labelsize': 10,
    'legend.fontsize': 9,
})
```

### ICML (Two Column, 3.25" per column)

```python
plt.rcParams.update({
    'figure.figsize': (3.25, 2.5),  # Single column width
    'font.size': 9,
    'axes.labelsize': 9,
    'legend.fontsize': 8,
})

# For full-width figures (spanning both columns)
fig = plt.figure(figsize=(6.75, 3.0))
```

### IEEE (Two Column, 3.5" per column)

```python
plt.rcParams.update({
    'figure.figsize': (3.5, 2.5),   # Single column
    'font.size': 8,
    'axes.labelsize': 8,
    'legend.fontsize': 7,
})
```

---

## tikzplotlib Integration

### Basic Workflow

```python
import matplotlib.pyplot as plt
import tikzplotlib

# Create matplotlib figure
fig, ax = plt.subplots(figsize=(3.5, 2.5))
ax.plot([1, 2, 3], [1, 4, 2], label='Data')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.legend()

# Save as both PDF and TikZ
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
tikzplotlib.save('figure.tex')
```

### Advanced Configuration

```python
tikzplotlib.save(
    'figure.tex',
    axis_width='3.5in',
    axis_height='2.5in',
    tex_relative_path_to_data='./data/',
    externalize_tables=True,  # Save data to external files
    override_externals=True,
    strict=True,  # Fail on unsupported features
)
```

### LaTeX Integration

```latex
\documentclass{article}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\begin{document}
\begin{figure}[h]
  \centering
  \input{figure.tex}
  \caption{My matplotlib figure rendered in LaTeX.}
  \label{fig:example}
\end{figure}
\end{document}
```

---

## Common Issues and Fixes

### Issue 1: Fonts Don't Match LaTeX Document

**Problem:** Matplotlib fonts differ from LaTeX body text.

**Solution:**
```python
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman'],
})
```

### Issue 2: Figures Too Small in PDF

**Problem:** Saved figures appear tiny or blurry.

**Solution:**
```python
# Set DPI appropriately
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')

# Or use vectorized formats
plt.savefig('figure.svg', format='svg', bbox_inches='tight')
```

### Issue 3: Text Cut Off in Saved Figure

**Problem:** Axis labels or titles are cropped.

**Solution:**
```python
# Use tight_layout before saving
plt.tight_layout()
plt.savefig('figure.pdf', bbox_inches='tight', pad_inches=0.1)
```

### Issue 4: Legend Overlaps Data

**Problem:** Legend blocks important parts of the plot.

**Solution:**
```python
# Place legend outside plot area
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Or use best location
ax.legend(loc='best', framealpha=0.9)
```

### Issue 5: Colorblind-Unfriendly Colors

**Problem:** Default colors not accessible.

**Solution:**
```python
# Use colorblind-friendly palettes
from matplotlib import cm
colors = cm.get_cmap('tab10').colors  # Good default

# Or ColorBrewer
CB_SAFE = ['#e69f00', '#56b4e9', '#009e73', '#f0e442']
```

### Issue 6: tikzplotlib Conversion Errors

**Problem:** Some matplotlib features don't convert.

**Solution:**
```python
# Avoid these in plots destined for TikZ:
# - Transparency (alpha < 1) on complex objects
# - Custom transforms
# - 3D plots

# Check compatibility
tikzplotlib.get_tikz_code()  # Raises if incompatible
```

---

## Best Practices Checklist

### Before Creating Figure
- [ ] Know target conference (affects sizing)
- [ ] Choose colorblind-friendly palette
- [ ] Decide: matplotlib PNG or tikzplotlib TikZ?

### During Creation
- [ ] Use SciencePlots style
- [ ] Set appropriate figure size
- [ ] Label all axes with units
- [ ] Add legend if multiple series
- [ ] Use grid for readability (optional)

### Before Saving
- [ ] Call `plt.tight_layout()`
- [ ] Verify font sizes are readable
- [ ] Check color contrast
- [ ] Test in grayscale if required

### Saving
- [ ] Save as PDF at 300 DPI minimum
- [ ] Use `bbox_inches='tight'`
- [ ] Consider tikzplotlib for LaTeX integration
- [ ] Keep source code with data

### After Saving
- [ ] Verify figure in compiled PDF
- [ ] Check file size (< 1MB recommended)
- [ ] Ensure vector graphics (no pixelation when zoomed)

---

## Quick Reference

```python
# Standard scientific plot setup
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science', 'ieee'])
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Plot data
ax.plot(x, y, label='Data', linewidth=1.5)
ax.set_xlabel('X-axis Label')
ax.set_ylabel('Y-axis Label')
ax.set_title('Figure Title')
ax.legend(frameon=True)
ax.grid(True, alpha=0.3)

# Save
plt.tight_layout()
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

**Next Steps:**
- See @scientificpaper:context/imaging/tikz-patterns.md for TikZ diagrams
- See @scientificpaper:agents/figure-artist.md for AI-assisted generation
