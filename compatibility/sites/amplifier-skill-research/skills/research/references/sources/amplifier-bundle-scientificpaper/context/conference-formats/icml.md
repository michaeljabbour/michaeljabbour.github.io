# ICML Conference Format Specification

**Conference:** International Conference on Machine Learning (ICML)
**Year:** 2025+ (updated specifications)
**Official Site:** https://icml.cc/

---

## Document Format

### Paper Size
- **Size:** US Letter (8.5" × 11") standard
- **Format:** PDF submission only
- **Font Embedding:** Type-1 fonts REQUIRED (not Type 3)

### Margins and Text Area
- **Margins:** Template-controlled, standard configuration
- **Layout:** Two-column format (do NOT alter)
- **Column separation:** Managed by `icml2025.sty`
- **Text area:** Defined by official style file

### Font
- **Family:** Times Roman (Times New Roman acceptable)
- **Size:** 10pt for body text
- **Spacing:** 11pt vertical spacing (leading)
- **Title:** Content words capitalized, template-controlled
- **Abstract heading:** 11pt bold, centered
- **Abstract body:** 10pt, 11pt spacing
- **Font encoding:** Type-1 fonts only (verify with `pdffonts`)

### Column Layout
- **Layout:** Two-column (required)
- **Important:** Do NOT modify column layout
- **Unlike:** NeurIPS which uses single-column

---

## Page Limits

### Main Paper
- **Limit:** 8 pages maximum (including figures, tables, but excluding references and appendices)
- **Content:** Introduction, Methods, Results, Discussion
- **Strict enforcement:** Do not compress formatting to fit more content

### References
- **Limit:** Unlimited pages
- **Placement:** After main content, before appendices
- **Note:** References do NOT count toward 8-page limit

### Appendices
- **Limit:** Unlimited pages
- **Content:** Proofs, additional experiments, extended analysis
- **Reviewers:** May or may not read appendices
- **Placement:** After references

---

## Document Structure

### Required Sections (in order)
1. **Title** - Content words capitalized
2. **Authors** - Names and affiliations (OMIT for review)
3. **Abstract** - One paragraph, 4-6 sentences
4. **Main Content** - Introduction, Methods, Results, Discussion
5. **Acknowledgments** - Optional, counts toward 8 pages
6. **References** - Unlimited, any consistent format
7. **Appendices** - Optional, unlimited

### Abstract Guidelines
- **Length:** One paragraph, 4-6 sentences
- **Format:** Single paragraph
- **Heading:** Centered, bold, 11pt
- **Body:** 10pt type, 11pt spacing
- **Indentation:** 0.25" on left and right margins
- **Content:** Background, problem, approach, key results, impact
- **Placement:** Immediately after title/author block

---

## Citation Style

### Flexibility
- **Any consistent style acceptable** - Author-year OR numeric
- **Common choices:** natbib, plain, numbered
- **Requirement:** Internal consistency throughout paper

### Citation Examples

**Author-year (natbib):**
```latex
\usepackage{natbib}

% In text
\citet{Author2025} proposed...  % Author (2025) proposed...
See \citep{Author2025}.         % See (Author, 2025).
```

**Numbered (alternative):**
```latex
\usepackage[numbers]{natbib}

% In text
See \cite{Author2025}.  % See [1].
Multiple \cite{Auth1,Auth2}.  % Multiple [1, 2].
```

### Bibliography Style
- **Style file:** `icml2025.sty` manages formatting
- **BibTeX:** Required for consistency
- **Format:** Must match chosen citation style
- **Flexibility:** plain, abbrv, unsrt, alpha all acceptable

---

## Figures and Tables

### Placement
- **Preferred:** Top or bottom of column
- **LaTeX option:** `\begin{figure}[t]` or `\begin{figure}[b]`
- **Two-column spanning:** `\begin{figure*}[t]` for wide figures
- **Avoid:** Mid-text placement disrupts reading flow

### Figure Format
- **Preferred:** Vector graphics (PDF, EPS)
- **Raster:** 300 DPI minimum if required
- **Width:** Single column: `0.9\columnwidth`, Double: `0.9\textwidth`
- **Font size:** Match document font (10pt) or 9pt for labels

### Figure Captions
- **Placement:** Below figures (NOT inside graphic)
- **Font:** 9-point type
- **Alignment:** Centered if single line, flush left if 2+ lines
- **Spacing:** At least 0.1 inches space before and after caption
- **Format:** "Figure 1. Description of the figure content."

### Figure Quality Requirements
- **Resolution:** High resolution, no pixelation
- **Text:** Readable at publication size
- **Colors:** Colorblind-friendly palettes recommended
- **Legibility:** All labels and text clearly visible
- **File size:** Reasonable (compress large images)

### Table Formatting
- **Package:** `booktabs` recommended for professional tables
- **Captions:** Above tables (9-point type)
- **Caption alignment:** Centered if single line, flush left if 2+ lines
- **Spacing:** At least 0.1 inches space before and after title
- **Rules:** `\toprule`, `\midrule`, `\bottomrule`
- **Alignment:** Left for text, center/right for numbers
- **Numbers:** Align decimal points using `siunitx` or manual alignment

---

## LaTeX Setup

### Document Class
```latex
\documentclass{article}
\usepackage{icml2025}
```

### Required Packages (included in style)
- `times` - Times Roman font
- `hyperref` - Hyperlinks (configured by style)
- `url` - URL formatting
- `natbib` - Citation management
- `amsmath, amssymb` - Mathematics

### Recommended Additional Packages
```latex
\usepackage{graphicx}     % For figures
\usepackage{booktabs}     % For tables
\usepackage{algorithm}    % For algorithms
\usepackage{algorithmic}  % Algorithm formatting
\usepackage{siunitx}      % Number formatting
```

### Title and Author Block

**For Review Submission (Anonymous):**
```latex
\icmltitlerunning{Short Title for Running Head}

\begin{document}
\twocolumn[
\icmltitle{Your Paper Title with Content Words Capitalized}

\begin{icmlauthorlist}
\icmlauthor{Anonymous Author 1}{anon}
\icmlauthor{Anonymous Author 2}{anon}
\end{icmlauthorlist}

\icmlaffiliation{anon}{Anonymous Institution}

\icmlcorrespondingauthor{Anonymous}{anonymous@email.com}

\icmlkeywords{Machine Learning, ICML}

\vskip 0.3in
]

\printAffiliationsAndNotice{}
```

**For Camera-Ready (With Authors):**
```latex
\begin{icmlauthorlist}
\icmlauthor{First Author}{inst1}
\icmlauthor{Second Author}{inst2}
\end{icmlauthorlist}

\icmlaffiliation{inst1}{University Name, Department}
\icmlaffiliation{inst2}{Company Name, Division}
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
# Verify Type-1 fonts (not Type 3)
pdffonts paper.pdf

# All fonts should show "Type 1" or "Type 1C" in Type column
# Type 3 fonts will cause REJECTION
```

### File Size Check
```bash
# Check file size (max 50MB for submission, 20MB for camera-ready)
ls -lh paper.pdf

# Compress if needed
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=paper_compressed.pdf paper.pdf
```

---

## Common Issues

### Page Limit Exceeded
- **Check:** Count pages up to (not including) references
- **Solutions:**
  - Move details to appendix
  - Compress figures or use multi-panel layouts
  - Tighten writing (remove redundancy)
  - Use smaller font for captions (9pt already minimum)
  - **DO NOT:** Compress formatting by reducing vertical spaces

### Font Embedding Errors
- **Problem:** Type 3 fonts cause automatic rejection
- **Solution:** Use Type 1 fonts (Times, Computer Modern)
- **Check:** `pdffonts paper.pdf` before submission
- **Common cause:** Screenshots or images with embedded fonts
- **Fix:** Recreate figures as vector graphics or high-quality rasters

### Column Layout Violations
- **Problem:** Modified column layout causes rejection
- **Solution:** Let `icml2025.sty` handle all layout
- **Avoid:** Manual layout adjustments, `\vspace` hacks, `\enlargethispage`

### Citation Style Inconsistency
- **Problem:** Mixed citation styles in references
- **Solution:** Use BibTeX with consistent `.bib` entries
- **Tool:** BibTeX validator or bibliography manager (Zotero, Mendeley)

### File Size Too Large
- **Problem:** Submission exceeds 50MB (or 20MB for camera-ready)
- **Solutions:**
  - Compress images before inclusion
  - Use JPEG for photos, PNG for diagrams
  - Reduce DPI to 300 for raster images
  - Use `gs` command above to compress PDF

### Double-Blind Violations
- **Problem:** Identifying information in review submission
- **Check:** Author names, affiliations, acknowledgments, obvious self-citations
- **Solution:** Use anonymous author blocks, remove/anonymize acknowledgments

---

## Submission Requirements

### PDF Requirements
- **File format:** PDF only
- **Fonts:** Embedded, Type-1 (not Type 3)
- **Page size:** US Letter (8.5" × 11")
- **File size:** Max 50MB (submission), max 20MB (camera-ready)
- **Hyperlinks:** Acceptable but not required

### Anonymity (For Review)
- **Author names:** Remove for initial submission
- **Affiliations:** Remove for initial submission
- **Acknowledgments:** Remove or anonymize
- **Self-citations:** Acceptable but avoid obvious identification
- **URLs:** Anonymize personal websites or institutional pages
- **Final version:** Include full author information

### Checklist Before Submission
- [ ] Page count ≤ 8 (excluding references and appendices)
- [ ] Abstract is 4-6 sentences, properly indented
- [ ] Fonts embedded (Type-1 only, verified with `pdffonts`)
- [ ] File size ≤ 50MB for submission
- [ ] Two-column layout preserved (not modified)
- [ ] References formatted consistently
- [ ] Figures high quality and readable
- [ ] Figure captions below figures (9pt)
- [ ] Table captions above tables (9pt)
- [ ] Anonymized (if review submission)
- [ ] No compressed formatting (vertical spaces intact)

---

## Template Location

Official templates available at:
- **ICML website:** https://icml.cc/Conferences/2025/StyleFiles
- **Overleaf:** https://www.overleaf.com/latex/templates/icml2025-template/
- **This bundle:** `@scientificpaper:templates/icml/`

### Template Files
- `icml2025.sty` - Style file (required)
- `example_paper.pdf` - Example formatted paper
- `template.tex` - Example document structure
- `example.bib` - Example bibliography

---

## Differences from Other Conferences

| Aspect | ICML | NeurIPS | ACL | IEEE |
|--------|------|---------|-----|------|
| Columns | Two | Single | Two | Two |
| Page limit | 8 + refs | 9 + refs | 8 + refs | 6-8 + refs |
| Font | 10pt Times | 10pt Times | Times | 10pt Times |
| Citation | Flexible | Flexible | natbib | Numbered |
| Paper size | Letter | Letter | A4 Only | Letter/A4 |
| Abstract | Indented 0.25" | Standard | Standard | Standard |
| File size limit | 50MB/20MB | ~10MB | Variable | Variable |

---

## Additional Resources

- **LaTeX help:** https://www.latex-project.org/
- **BibTeX guide:** http://www.bibtex.org/
- **ICML submission:** https://icml.cc/Conferences/2025/CallForPapers
- **Font verification:** `pdffonts` command (part of poppler-utils)
- **Overleaf:** https://www.overleaf.com (online LaTeX editor)

---

**Last Updated:** 2025
**Valid For:** ICML 2025 and likely 2026+ (check for minor updates each year)
