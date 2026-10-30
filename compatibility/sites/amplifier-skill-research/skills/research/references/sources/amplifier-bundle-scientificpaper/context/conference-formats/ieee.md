# IEEE Conference Format Specification

**Organization:** Institute of Electrical and Electronics Engineers (IEEE)
**Format:** Conference Proceedings
**Official Site:** https://www.ieee.org/conferences/publishing/

---

## Document Format

### Paper Size
- **Primary:** US Letter (8.5" × 11")
- **Alternative:** A4 (21 cm × 29.7 cm) - check specific conference
- **Note:** Most IEEE conferences accept either format
- **Recommendation:** Use Letter for consistency with most venues

### Margins and Text Area

**For US Letter:**
- **Left margin:** 0.7 inches (18mm)
- **Right margin:** 0.7 inches (18mm)
- **Top margin:** 1 inch (25mm)
- **Bottom margin:** 1 inch (25mm)

**For A4:**
- **Top margin:** 19mm (0.75")
- **Bottom margin:** 43mm (1.69")
- **Left margin:** 14.32mm (0.56")
- **Right margin:** 14.32mm (0.56")

### Font
- **Primary:** Times New Roman
- **Alternatives (acceptable):**
  - Nimbus Roman No 9
  - Liberation fonts
- **Title:** 24 point, bold
- **Author names:** 12 point
- **Body text:** 10-12 point (10pt recommended)
- **Section headings:** Bold, numbered
- **Subsection headings:** Italic or bold-italic

### Column Layout
- **Layout:** Two-column (required)
- **Column separation:** 0.25 inches (6.35mm) white space
- **Column width:** Automatically calculated by template
- **Important:** Do not modify column layout

---

## Page Limits

### Main Paper
- **Typical limit:** 6-8 pages (varies by conference)
- **Check:** Specific conference call for papers
- **Content:** Introduction, Methods, Results, Discussion
- **Note:** Some conferences include references in page limit, others don't

### References
- **Limit:** Varies by conference
- **Some venues:** References count toward page limit
- **Other venues:** References unlimited
- **Check:** Conference-specific guidelines

### Extended Versions
- **Journal extensions:** Often allowed with 30%+ new content
- **Invited papers:** May have different page limits
- **Workshop papers:** Typically shorter (4-6 pages)

---

## Document Structure

### Required Sections (in order)
1. **Title** - Descriptive and concise (24pt, bold)
2. **Authors** - Names, affiliations, email addresses
3. **Abstract** - 150-250 words, single paragraph
4. **Keywords** - 3-5 keywords for indexing
5. **Main Content** - Numbered sections (I, II, III, IV...)
6. **Acknowledgments** - Optional, before references
7. **References** - Numbered list in order of citation

### Abstract Guidelines
- **Length:** 150-250 words typical
- **Format:** Single paragraph, italic (template-controlled)
- **Content:** Purpose, methods, results, conclusions
- **Placement:** After author block, before main content
- **Note:** No citations in abstract (generally)

### Keywords
- **Count:** 3-5 keywords or phrases
- **Format:** Separated by commas or semicolons
- **Placement:** Immediately after abstract
- **Purpose:** IEEE Xplore indexing

---

## Citation Style

### Format
- **Style:** Numbered sequential citations
- **In-text:** Bracketed numbers [1], [2], [3]
- **Sequential:** [1, 2] or [1]-[3] for ranges
- **Required:** Consistent numbering throughout

### Citation Examples

**In-text citations:**
```latex
\documentclass[conference]{IEEEtran}
\usepackage{cite}

% Single citation
See reference \cite{Author2024}.  % Output: See reference [1].

% Multiple citations
Several studies \cite{Auth1,Auth2,Auth3}.  % Output: [1]-[3] or [1, 2, 3]

% Range citation
Prior work \cite{Auth1,Auth2,Auth3,Auth4}.  % Output: [1]-[4]
```

### Reference List Format
- **Order:** Numerical, in order of first citation
- **Alternative:** Alphabetical by lead author's last name (less common)
- **Numbering:** [1], [2], [3]...
- **Style:** IEEE style (see examples below)

### Reference Examples

```latex
% Journal article
\bibitem{journal}
A. Author and B. Coauthor, ``Article title,'' \emph{Journal Name},
vol. 10, no. 3, pp. 123--145, Mar. 2024.

% Conference paper
\bibitem{conf}
C. Author, ``Paper title,'' in \emph{Proc. IEEE Conf. Name},
City, Country, 2024, pp. 1--5.

% Book
\bibitem{book}
D. Author, \emph{Book Title}, 3rd ed. City, State: Publisher, 2024.

% Website
\bibitem{web}
E. Author. ``Page title.'' Website Name. City, State.
Accessed: Month Day, Year. [Online]. Available: http://url
```

---

## Figures and Tables

### Placement
- **Preferred:** Top or bottom of column
- **LaTeX option:** `\begin{figure}[t]` or `\begin{figure}[b]`
- **Two-column spanning:** `\begin{figure*}[t]` for wide figures
- **Float control:** Use IEEEtran controls

### Figure Format
- **Preferred:** Vector graphics (PDF, EPS for LaTeX; WMF, EMF for Word)
- **Raster:** 300-600 DPI for photos, 600-1200 DPI for line art
- **Color:** RGB for digital, CMYK for print (check conference requirements)
- **Width:** Match column width

### Figure Captions
- **Placement:** BELOW figures (IEEE standard)
- **Format:** "Fig. X. Caption text explaining the figure."
- **Font:** 8-10 point (typically 9pt)
- **Numbering:** Sequential, Arabic numerals
- **Multi-part:** Label subfigures as (a), (b), (c)

**Example:**
```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.9\columnwidth]{figure1.pdf}
\caption{Experimental results showing performance improvement.
(a) Training accuracy. (b) Validation accuracy.}
\label{fig:results}
\end{figure}
```

### Table Formatting
- **Captions:** ABOVE tables (IEEE standard)
- **Format:** "TABLE I\nCAPTION TEXT IN ALL CAPITALS"
- **Numbering:** Roman numerals (I, II, III, IV...)
- **Font in caption:** Match body font
- **Rules:** Horizontal lines only (top, bottom, after header)

**Example:**
```latex
\begin{table}[t]
\centering
\caption{COMPARISON OF METHODS}
\label{tab:comparison}
\begin{tabular}{|l|c|c|}
\hline
Method & Accuracy & Time \\
\hline
Baseline & 85.3\% & 10ms \\
Proposed & 92.1\% & 8ms \\
\hline
\end{tabular}
\end{table}
```

### Figure and Table Quality
- **Resolution:** High quality, no pixelation
- **Text in graphics:** 9-10 point font size recommended
- **Acceptable fonts in graphics:**
  - Helvetica
  - Times New Roman
  - Arial
  - Cambria
  - Symbol
- **Consistency:** Use same font across all graphics
- **Legibility:** All labels readable at publication size

---

## LaTeX Setup

### Document Class
```latex
\documentclass[conference]{IEEEtran}
% Options: conference, journal, technote, peerreview
```

### Required/Recommended Packages
```latex
% Citations
\usepackage{cite}         % Compress citation ranges

% Graphics
\usepackage{graphicx}     % For figures
\usepackage{epsfig}       % For EPS figures (if needed)

% Mathematics
\usepackage{amsmath}      % AMS math
\usepackage{amssymb}      % AMS symbols

% Algorithms
\usepackage{algorithmic}  % Algorithm formatting
\usepackage{algorithm}    % Algorithm floats

% URLs
\usepackage{url}          % URL formatting

% Hyperlinks (optional, load last)
\usepackage{hyperref}     % PDF hyperlinks
```

### Title and Author Block

**Single affiliation:**
```latex
\title{Your Paper Title Here}

\author{
  \IEEEauthorblockN{First Author, Second Author, Third Author}
  \IEEEauthorblockA{
    Department Name\\
    University Name\\
    City, State ZIP\\
    Email: \{first, second, third\}@university.edu
  }
}
```

**Multiple affiliations:**
```latex
\author{
  \IEEEauthorblockN{First Author\IEEEauthorrefmark{1},
                    Second Author\IEEEauthorrefmark{2}}
  \IEEEauthorblockA{\IEEEauthorrefmark{1}University One,
                    email@uni1.edu}
  \IEEEauthorblockA{\IEEEauthorrefmark{2}Company Two,
                    email@company.com}
}
```

### Document Body
```latex
\begin{document}
\maketitle

\begin{abstract}
Your abstract text here. Concise summary of the paper.
\end{abstract}

\begin{IEEEkeywords}
keyword1, keyword2, keyword3, keyword4
\end{IEEEkeywords}

\section{Introduction}
Your introduction text...

\section{Related Work}
Literature review...

\end{document}
```

---

## Compilation

### Standard Workflow
```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex  # Final pass
```

### Using latexmk
```bash
latexmk -pdf paper.tex
```

### Check PDF Quality
```bash
# Check page size
pdfinfo paper.pdf | grep "Page size"

# Check fonts
pdffonts paper.pdf

# Check file size
ls -lh paper.pdf
```

---

## Common Issues

### Page Limit Exceeded
- **Check:** Specific conference requirements (6, 8, or other limit)
- **Solutions:**
  - Compress figures or use multi-panel layouts
  - Tighten writing, remove redundancy
  - Move details to separate technical report
  - Use smaller captions (within reason)

### Citation Numbering Errors
- **Problem:** Citations out of order or incorrect numbering
- **Solution:** Use BibTeX with `\cite{}` commands
- **Package:** `cite` package compresses ranges automatically
- **Check:** References numbered in order of first appearance

### Figure/Table Caption Errors
- **Figure problem:** Caption above figure (wrong!)
- **Solution:** Caption must be BELOW figures
- **Table problem:** Caption below table (wrong!)
- **Solution:** Caption must be ABOVE tables
- **Remember:** "Figures below, Tables above"

### Column Breaking Issues
- **Problem:** Figures breaking column layout
- **Solution:** Use `figure` for single column, `figure*` for double column
- **Balance:** Use `\balance` command at end of paper for even columns

### Font Issues
- **Problem:** Inconsistent fonts in figures
- **Solution:** Use Times, Helvetica, or Arial consistently
- **Size:** 9-10 point for graphics text
- **Embedding:** Ensure all fonts embedded in PDF

### Template Modifications
- **Problem:** Modified IEEEtran class causes formatting errors
- **Solution:** Use official IEEEtran.cls without modifications
- **Download:** Get latest version from IEEE or CTAN

---

## Submission Requirements

### PDF Requirements
- **File format:** PDF only (IEEE PDF eXpress may be required)
- **Page size:** Letter or A4 (as specified by conference)
- **Fonts:** All fonts embedded
- **Quality:** Professional, publication-ready
- **File size:** Typically < 10MB (check conference limits)

### IEEE PDF eXpress
Many IEEE conferences require PDF validation:
```
1. Create account at IEEE PDF eXpress site
2. Upload your PDF
3. System checks compliance
4. Download validated PDF
5. Submit validated PDF to conference
```

### Copyright Form
- **Required:** IEEE copyright form for all accepted papers
- **Timing:** Usually after acceptance
- **Process:** Electronic copyright transfer
- **Note:** May affect ability to post on arXiv (check policy)

### Checklist Before Submission
- [ ] Page count within limit (check specific conference)
- [ ] Two-column layout preserved
- [ ] Using IEEEtran document class
- [ ] Abstract 150-250 words
- [ ] Keywords provided (3-5)
- [ ] Numbered citations [1], [2], [3]
- [ ] References in IEEE format
- [ ] Figure captions BELOW figures
- [ ] Table captions ABOVE tables (all caps)
- [ ] All fonts embedded in PDF
- [ ] PDF validated through IEEE PDF eXpress (if required)
- [ ] Copyright form submitted (if accepted)

---

## Template Location

Official templates available at:
- **IEEE Template Selector:** https://www.ieee.org/conferences/publishing/templates.html
- **Overleaf IEEE Templates:** https://www.overleaf.com/gallery/tagged/ieee
- **CTAN (LaTeX):** https://ctan.org/pkg/ieeetran
- **This bundle:** `@scientificpaper:templates/ieee/`

### Template Files
- `IEEEtran.cls` - Document class (required)
- `IEEEtran.bst` - Bibliography style
- `bare_conf.tex` - Conference template
- `bare_jrnl.tex` - Journal template

---

## Differences from Other Conferences

| Aspect | IEEE | NeurIPS | ICML | ACL |
|--------|------|---------|------|-----|
| Columns | Two | Single | Two | Two |
| Page limit | 6-8* | 9 + refs | 8 + refs | 8 + refs |
| Font | 10pt Times | 10pt Times | 10pt Times | Times |
| Citation | **Numbered** | Flexible | Flexible | natbib |
| Paper size | Letter/A4 | Letter | Letter | **A4 Only** |
| Fig captions | **Below** | Below | Below | Below |
| Table captions | **Above (CAPS)** | Above | Above | Above |
| Section numbers | **Required** | Optional | Optional | Optional |
| Keywords | **Required** | Optional | Optional | Optional |

*Varies by specific conference

---

## IEEE-Specific Best Practices

### Section Numbering
- **Use:** Roman numerals (I, II, III, IV...)
- **Subsections:** A, B, C or 1, 2, 3
- **Format:**
  ```latex
  \section{Introduction}        % I. Introduction
  \subsection{Background}       % A. Background
  \subsubsection{Detail}        % 1) Detail
  ```

### Equation Numbering
- **Format:** Sequential (1), (2), (3)...
- **Placement:** Right-aligned
- **Reference:** Use `\eqref{label}` for automatic formatting

### Copyright Notice
For camera-ready papers:
```latex
\IEEEoverridecommandlockouts
\IEEEpubid{\makebox[\columnwidth]{978-1-xxxx-xxxx-x/24/\$31.00~\copyright~2024 IEEE \hfill} \hspace{\columnsep}\makebox[\columnwidth]{ }}
```

### Biography Section (Optional for some journals)
```latex
\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{photo.jpg}}]{Author Name}
Biography text here.
\end{IEEEbiography}
```

---

## Additional Resources

- **IEEE Author Center:** https://ieeeauthorcenter.ieee.org/
- **IEEE Publication Services:** https://www.ieee.org/conferences/publishing/
- **IEEEtran Documentation:** http://www.michaelshell.org/tex/ieeetran/
- **LaTeX help:** https://www.latex-project.org/
- **IEEE Xplore:** https://ieeexplore.ieee.org/ (to see published examples)

---

## Troubleshooting Commands

```bash
# Validate PDF page size
pdfinfo paper.pdf | grep "Page size"

# Check font embedding
pdffonts paper.pdf

# Complete build with bibliography
pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex

# Count pages
pdfinfo paper.pdf | grep "Pages"

# Compress PDF if too large
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf paper.pdf
```

---

**Last Updated:** 2024
**Valid For:** IEEE conference publications 2024+
**Important:** Always check specific conference requirements as guidelines vary by venue
