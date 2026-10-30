# ACL Conference Format Specification

**Conference:** Association for Computational Linguistics (ACL)
**Year:** 2024+ (updated specifications)
**Official Site:** https://aclweb.org/

---

## Document Format

### Paper Size
- **Size:** A4 (21 cm × 29.7 cm) ONLY
- **⚠️ CRITICAL:** Papers with non-A4 page size will be REJECTED without review
- **NOT US Letter** - Use A4 exclusively

### Margins and Text Area
- **Margins:** Template-controlled by `acl.sty`
- **Layout:** Two-column format (required)
- **Column separation:** Managed by official style file
- **Important:** Do NOT modify margins or layout

### Font
- **Family:** Times New Roman (standard)
- **Size:** Template-controlled (typically 10-11pt)
- **Encoding:** Standard font encoding
- **Consistency:** Follow template fonts exactly

### Column Layout
- **Layout:** Two-column (required for all paper types)
- **Paper types:** Long papers, short papers, extended abstracts all use same format
- **Unlike:** ACM review format which uses single-column

---

## Page Limits

### Long Papers
- **Limit:** 8 pages maximum (excluding references)
- **Content:** Full research presentation
- **References:** Unlimited pages, do NOT count toward limit

### Short Papers
- **Limit:** 4 pages maximum (excluding references)
- **Content:** Focused contributions, preliminary results
- **References:** Unlimited pages, do NOT count toward limit

### Extended Abstracts
- **Limit:** Varies by year/venue
- **Content:** Summary of work (often published elsewhere)
- **Format:** Follows ACL two-column format

### References
- **Limit:** Unlimited pages
- **Placement:** After main content
- **Style:** `acl_natbib.bst` (APA-based format)

---

## Document Structure

### Required Sections (in order)
1. **Title** - Descriptive and concise
2. **Authors** - Names and affiliations
3. **Abstract** - Single paragraph summary
4. **Main Content** - Introduction, Methods, Results, Discussion
5. **Acknowledgments** - Optional (may count toward page limit)
6. **References** - Unlimited, must use acl_natbib.bst

### Abstract Guidelines
- **Length:** Single paragraph, concise
- **Format:** Standard paragraph (no special indentation)
- **Content:** Problem, approach, key findings, significance
- **Placement:** Immediately after author block

---

## Citation Style

### Required Package
- **Package:** natbib (strongly encouraged)
- **Style file:** `acl_natbib.bst` (required for bibliography)
- **Format:** Author-year citations following APA conventions

### Citation Commands

**In-text citations:**
```latex
\usepackage{natbib}

% Textual citation
\citet{Author2024} proposed...
% Output: Author (2024) proposed...

% Parenthetical citation
\citep{Author2024}
% Output: (Author, 2024)

% Within parentheses (no extra parens)
\citealp{Author2024}
% Output: Author, 2024

% Multiple citations
\citep{Author2024,Other2023}
% Output: (Author, 2024; Other, 2023)
```

### Bibliography Setup
```latex
% In document
\bibliographystyle{acl_natbib}
\bibliography{custom,anthology}
```

### Required Bibliography Files
The ACL style package includes:
- `acl.sty` - LaTeX style file
- `acl_natbib.bst` - Bibliography style
- `custom.bib` - Your custom bibliography
- `anthology.bib` - ACL Anthology bibliography (optional)

---

## Figures and Tables

### Placement
- **Preferred:** Top or bottom of column
- **LaTeX option:** `\begin{figure}[t]` or `\begin{figure}[b]`
- **Two-column spanning:** `\begin{figure*}[t]` for wide figures
- **Captions:** Follow standard ACL formatting

### Figure Format
- **Preferred:** Vector graphics (PDF, EPS)
- **Raster:** 300 DPI minimum if required
- **Width:** Single column: `0.9\columnwidth`, Double: `0.9\textwidth`
- **Font size:** Match document font or slightly smaller

### Figure Captions
- **Placement:** Below figures
- **Font:** Standard caption font from template
- **Alignment:** Left-aligned (standard)
- **Format:** "Figure 1: Description of the figure."

### Figure Quality Requirements
- **Resolution:** High resolution, clearly readable
- **Text:** All labels visible at publication size
- **Colors:** Accessible color schemes recommended
- **Consistency:** Uniform style across all figures

### Table Formatting
- **Package:** `booktabs` recommended for professional tables
- **Captions:** Above tables (LaTeX standard)
- **Rules:** `\toprule`, `\midrule`, `\bottomrule`
- **Alignment:** Left for text, right for numbers
- **Numbers:** Align decimal points for clarity

---

## LaTeX Setup

### Document Class
```latex
\documentclass[11pt,a4paper]{article}
\usepackage{acl}
\usepackage{times}
\usepackage{latexsym}
```

### Required Packages
```latex
\usepackage{acl}          % ACL style (REQUIRED)
\usepackage{times}        % Times New Roman font
\usepackage{latexsym}     % Additional symbols
\usepackage{natbib}       % Citations (strongly encouraged)
```

### Recommended Additional Packages
```latex
\usepackage{graphicx}     % For figures
\usepackage{booktabs}     % For tables
\usepackage{amsmath}      % Mathematics
\usepackage{amssymb}      % Mathematical symbols
\usepackage{url}          % URL formatting
\usepackage{hyperref}     % Hyperlinks (load last)
```

### Title and Author Block
```latex
\title{Your Paper Title Here}

\author{
  First Author \\
  Affiliation \\
  \texttt{email@domain.com}
  \And
  Second Author \\
  Affiliation \\
  \texttt{email@domain.com}
}

\begin{document}
\maketitle

\begin{abstract}
Your abstract text here. Single paragraph summarizing the paper.
\end{abstract}
```

---

## Compilation

### Standard Workflow
```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex  # Second pass for cross-references
```

### Using latexmk (Recommended)
```bash
latexmk -pdf paper.tex
```

### A4 Paper Size Verification
```bash
# Check page size in PDF
pdfinfo paper.pdf | grep "Page size"

# Should show: Page size: 595 x 842 pts (A4)
# NOT: 612 x 792 pts (letter)
```

### Font Check
```bash
# Verify fonts are embedded
pdffonts paper.pdf
```

---

## Common Issues

### Wrong Paper Size (CRITICAL)
- **Problem:** Using US Letter instead of A4 causes automatic rejection
- **Solution:** Use `a4paper` option in document class
- **Check:** `pdfinfo paper.pdf | grep "Page size"` should show A4 (595 x 842 pts)
- **LaTeX fix:**
  ```latex
  \documentclass[11pt,a4paper]{article}
  ```

### Page Limit Exceeded
- **Check:** Count pages up to (not including) references
- **Long papers:** 8 pages max
- **Short papers:** 4 pages max
- **Solutions:**
  - Tighten writing, remove redundancy
  - Compress figures or use multi-panel layouts
  - Move detailed analysis to appendix (if allowed)
  - Reduce whitespace in tables/figures

### Citation Format Errors
- **Problem:** Not using natbib or wrong bibliography style
- **Solution:** Use `\usepackage{natbib}` and `\bibliographystyle{acl_natbib}`
- **Common error:** Using plain.bst or other non-ACL styles
- **Fix:** Download acl_natbib.bst from official style files

### Modified Style File
- **Problem:** Modified acl.sty may cause rejection
- **Solution:** Use official acl.sty without modifications
- **Download:** https://github.com/acl-org/acl-style-files
- **Avoid:** Using templates from other conferences

### Bibliography Not Appearing
- **Problem:** Missing .bbl file or wrong bibliography style
- **Solution:** Run bibtex, check .bib file syntax
- **Workflow:**
  ```bash
  pdflatex paper.tex
  bibtex paper      # Creates .bbl file
  pdflatex paper.tex
  pdflatex paper.tex
  ```

### Column Layout Issues
- **Problem:** Figures breaking column layout
- **Solution:** Use `figure` for single column, `figure*` for double column
- **Avoid:** Manual column breaks or layout hacks

---

## Submission Requirements

### PDF Requirements
- **File format:** PDF only
- **Paper size:** A4 (21 cm × 29.7 cm) - VERIFIED
- **Fonts:** Embedded (check with pdffonts)
- **File size:** Reasonable (typically < 10MB)
- **Quality:** Professional, publication-ready

### Style Compliance
- **Style file:** Official acl.sty (unmodified)
- **Bibliography:** acl_natbib.bst style
- **Citations:** natbib commands (\citet, \citep)
- **Format:** Two-column A4 layout

### Checklist Before Submission
- [ ] Page size is A4 (verified with pdfinfo)
- [ ] Page count ≤ 8 (long) or ≤ 4 (short), excluding references
- [ ] Using official acl.sty (unmodified)
- [ ] Bibliography style is acl_natbib.bst
- [ ] Using natbib for citations
- [ ] Two-column layout preserved
- [ ] Fonts embedded in PDF
- [ ] Abstract is concise single paragraph
- [ ] Figures high quality and readable
- [ ] References formatted consistently
- [ ] No identifying information (if anonymous review)

---

## Template Location

Official templates available at:
- **ACL Style Files GitHub:** https://github.com/acl-org/acl-style-files
- **ACL Formatting Guide:** https://acl-org.github.io/ACLPUB/formatting.html
- **Overleaf Template:** https://www.overleaf.com/latex/templates/acl-conference-template/
- **This bundle:** `@scientificpaper:templates/acl/`

### Template Files
- `acl.sty` - Style file (required, do not modify)
- `acl_natbib.bst` - Bibliography style (required)
- `template.tex` - Example document structure
- `custom.bib` - Example bibliography
- `anthology.bib` - ACL Anthology references (optional)

---

## Differences from Other Conferences

| Aspect | ACL | NeurIPS | ICML | IEEE |
|--------|-----|---------|------|------|
| Paper size | **A4 Only** | Letter | Letter | Letter/A4 |
| Columns | Two | Single | Two | Two |
| Page limit | 8/4 + refs | 9 + refs | 8 + refs | 6-8 + refs |
| Font | Times | 10pt Times | 10pt Times | 10pt Times |
| Citation | **natbib required** | Flexible | Flexible | Numbered |
| Bib style | acl_natbib.bst | Flexible | Flexible | IEEEtran |
| Critical rule | A4 or reject | Type-1 fonts | Type-1 fonts | - |

**Key Difference:** ACL's strict A4 requirement is unique and causes most rejections when violated.

---

## ACL-Specific Best Practices

### Linguistic Content
- **Terminology:** Use standard NLP/CL terminology
- **Datasets:** Cite properly, include availability information
- **Reproducibility:** Include code/data availability statements
- **Ethics:** Consider ethical implications (required for some ACL venues)

### Writing Style
- **Clarity:** Write for international audience
- **Examples:** Include linguistic examples where appropriate
- **Notation:** Define all notation clearly
- **Abbreviations:** Define on first use

### Citation Practices
- **ACL Anthology:** Use anthology.bib for ACL papers when possible
- **Author names:** Full names preferred
- **Consistency:** Maintain consistent citation format throughout
- **Self-citation:** Allowed but keep anonymous for review

---

## Additional Resources

- **ACL Website:** https://aclweb.org/
- **Style Files:** https://github.com/acl-org/acl-style-files
- **Formatting Guide:** https://acl-org.github.io/ACLPUB/formatting.html
- **LaTeX help:** https://www.latex-project.org/
- **natbib documentation:** https://ctan.org/pkg/natbib
- **Overleaf:** https://www.overleaf.com (for online editing)

---

## Troubleshooting Commands

```bash
# Check PDF page size (CRITICAL for ACL)
pdfinfo paper.pdf | grep "Page size"
# Must show: 595 x 842 pts (A4)

# Check fonts are embedded
pdffonts paper.pdf

# Validate LaTeX compilation
pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex

# Count pages (excluding references)
# Manually check PDF - references start after main content
```

---

**Last Updated:** 2024
**Valid For:** ACL 2024 and likely 2025+ (minor changes possible)
**Critical Reminder:** A4 paper size is NON-NEGOTIABLE for ACL submissions
