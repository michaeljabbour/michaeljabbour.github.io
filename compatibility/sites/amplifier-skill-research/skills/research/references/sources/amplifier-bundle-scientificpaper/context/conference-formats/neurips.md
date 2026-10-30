# NeurIPS Conference Format Specification

**Conference:** Neural Information Processing Systems (NeurIPS)
**Year:** 2024+ (updated specifications)
**Official Site:** https://neurips.cc/

---

## Document Format

### Paper Size
- **Size:** US Letter (8.5" × 11")
- **⚠️ NOT A4** - Use US Letter only

### Margins and Text Area
- **Text area:** 5.5" wide × 9" high
- **Left/Right margins:** Template-controlled (approximately 1.5")
- **Top/Bottom margins:** Template-controlled (approximately 1")
- **Margins managed by:** `neurips_2024.sty` style file

### Font
- **Family:** Times Roman (Times New Roman acceptable)
- **Size:** 10pt for body text
- **Title:** Bold, larger (template-controlled)
- **Authors:** Normal weight, template-controlled
- **Sections:** Bold, template-controlled
- **Font encoding:** Type 1 fonts required (not Type 3)

### Column Layout
- **Layout:** Single-column
- **Unlike:** ICML, IEEE, ACL which use two-column

---

## Page Limits

### Main Paper
- **Limit:** 9 pages (including figures, tables, but excluding references)
- **Content:** Introduction, Methods, Results, Discussion, Acknowledgments

### References
- **Limit:** Unlimited pages
- **Placement:** After main content
- **Note:** References do NOT count toward 9-page limit

### Supplementary Material
- **Limit:** Unlimited (separate PDF)
- **Content:** Proofs, additional experiments, code
- **Reviewers:** May not read supplementary material

---

## Document Structure

### Required Sections (in order)
1. **Title** - Concise and descriptive
2. **Authors** - Names and affiliations
3. **Abstract** - 250 words maximum
4. **Main Content** - Introduction, Methods, Results, Discussion
5. **Acknowledgments** - Optional, counts toward 9 pages
6. **References** - Unlimited, must be in correct format

### Abstract Guidelines
- **Length:** 250 words maximum
- **Format:** Single paragraph
- **Content:** Background, gap, approach, results, implications
- **Placement:** Immediately after author block

---

## Citation Style

### Flexibility
- **Author-year OR numeric** - Both acceptable
- **Recommendation:** Author-year with natbib for flexibility
- **Common choice:** `\usepackage{natbib}` with `\citep{}` and `\citet{}`

### Citation Examples

**Author-year (natbib):**
```latex
\usepackage{natbib}

% In text
\citet{Author2024} proposed...  % Author (2024) proposed...
See \citep{Author2024}.         % See (Author, 2024).
```

**Numbered (alternative):**
```latex
\usepackage[numbers]{natbib}

% In text
See \cite{Author2024}.  % See [1].
```

### Bibliography Style
- **Style file:** `neurips_2024.sty` includes bibliography formatting
- **BibTeX:** Required for consistency
- **Format:** Consistent with chosen citation style (author-year or numeric)

---

## Figures and Tables

### Placement
- **Preferred:** Top or bottom of page
- **LaTeX option:** `\begin{figure}[t]` or `\begin{figure}[b]`
- **Avoid:** Mid-text placement
- **Captions:** Below figures, above tables (LaTeX convention)

### Figure Format
- **Preferred:** Vector graphics (PDF, EPS)
- **Raster:** 300 DPI minimum if required
- **Width:** Typically `0.8\columnwidth` or `0.9\columnwidth`
- **Font size:** Match document font (10pt) or slightly smaller

### Figure Quality Requirements
- **Resolution:** High resolution, no pixelation
- **Text:** Readable at publication size
- **Colors:** Colorblind-friendly if possible
- **File size:** Reasonable (compress if very large)

### Table Formatting
- **Package:** `booktabs` recommended
- **Rules:** `\toprule`, `\midrule`, `\bottomrule`
- **Alignment:** Left for text, center/right for numbers
- **Numbers:** Align decimal points

---

## LaTeX Setup

### Document Class
```latex
\documentclass{article}
\usepackage{neurips_2024}
```

### Required Packages (included in style)
- `times` - Times Roman font
- `hyperref` - Hyperlinks (configured by style)
- `url` - URL formatting
- `amsmath, amssymb` - Mathematics (if needed)

### Recommended Additional Packages
```latex
\usepackage{graphicx}     % For figures
\usepackage{booktabs}     % For tables
\usepackage{algorithm}    % For algorithms
\usepackage{algorithmic}  % Algorithm formatting
\usepackage{natbib}       % Citations
```

### Title and Author Block
```latex
\title{Your Paper Title}

\author{
  First Author \\
  Institution \\
  \texttt{email@domain.com} \\
  \And
  Second Author \\
  Institution \\
  \texttt{email@domain.com}
}
```

---

## Compilation

### Standard Workflow
```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex  # Second pass for references
```

### Using latexmk (Recommended)
```bash
latexmk -pdf paper.tex
```

### Font Embedding Check
```bash
# Verify Type 1 fonts (not Type 3)
pdffonts paper.pdf

# Should show "Type 1" or "Type 1C" in Type column
```

---

## Common Issues

### Page Limit Exceeded
- **Check:** Count pages up to (not including) references
- **Solutions:**
  - Move details to appendix/supplementary
  - Compress figures or use multi-panel layouts
  - Tighten writing (remove redundancy)
  - Use smaller font for algorithms (within reason)

### Font Embedding Errors
- **Problem:** Type 3 fonts cause rejection
- **Solution:** Use Type 1 fonts (Times, Computer Modern)
- **Check:** `pdffonts paper.pdf` before submission

### Margin Violations
- **Problem:** Text extends beyond text area
- **Solution:** Let `neurips_2024.sty` handle margins
- **Avoid:** Manual margin adjustments with `\geometry`

### Citation Style Inconsistency
- **Problem:** Mixed citation styles in references
- **Solution:** Use BibTeX with consistent `.bib` entries
- **Tool:** BibTeX validator or bibliography manager

---

## Submission Requirements

### PDF Requirements
- **File format:** PDF only
- **Fonts:** Embedded, Type 1 (not Type 3)
- **Page size:** US Letter (8.5" × 11")
- **File size:** Reasonable (compress if > 10MB)
- **Hyperlinks:** Acceptable but not required

### Anonymity (For Review)
- **Author names:** Remove for initial submission
- **Affiliations:** Remove for initial submission
- **Acknowledgments:** Remove or anonymize
- **Self-citations:** Acceptable but avoid obvious identification
- **Final version:** Include full author information

### Checklist Before Submission
- [ ] Page count ≤ 9 (excluding references)
- [ ] Abstract ≤ 250 words
- [ ] Fonts embedded (Type 1)
- [ ] Paper size = US Letter
- [ ] References formatted consistently
- [ ] Figures high quality and readable
- [ ] Anonymized (if review submission)
- [ ] Supplementary material prepared (if applicable)

---

## Template Location

Official templates available at:
- **NeurIPS website:** https://neurips.cc/Conferences/2024/PaperInformation/StyleFiles
- **This bundle:** `@scientificpaper:templates/neurips/`

### Template Files
- `neurips_2024.sty` - Style file (required)
- `template.tex` - Example document structure
- `example.bib` - Example bibliography

---

## Differences from Other Conferences

| Aspect | NeurIPS | ICML | IEEE |
|--------|---------|------|------|
| Columns | Single | Two | Two |
| Page limit | 9 + refs | 8 + refs | 6-8 + refs |
| Font | 10pt Times | 10pt Times | 10pt Times |
| Citation | Flexible | Numbered | Numbered |
| Paper size | US Letter | US Letter | Letter/A4 |

---

## Additional Resources

- **LaTeX help:** https://www.latex-project.org/
- **BibTeX guide:** http://www.bibtex.org/
- **NeurIPS submission:** https://neurips.cc/Conferences/2024/CallForPapers

---

**Last Updated:** 2024
**Valid For:** NeurIPS 2024 and likely 2025+ (minor changes expected)
