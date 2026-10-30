# ACM Conference Format Specification

**Organization:** Association for Computing Machinery (ACM)
**Primary Venue:** ACM SIGCHI and related conferences
**Official Site:** https://www.acm.org/publications/

---

## Document Format

### Paper Size
- **Review format:** Variable (template-controlled)
- **Camera-ready:** Conference-specific (often US Letter or A4)
- **Important:** Use official ACM template for correct sizing

### Layout Phases

**Review Phase:**
- **Layout:** Single-column (optimized for TAPS workflow)
- **Purpose:** Easy reading and annotation for reviewers
- **Requirement:** Use `manuscript,review` document class options

**Camera-Ready Phase:**
- **Layout:** Determined by conference (often two-column)
- **Purpose:** Final publication format
- **Requirement:** Use conference-specific document class option (e.g., `sigconf`)

### Margins and Text Area
- **Margins:** Template-controlled by `acmart` class
- **Text area:** Automatically calculated
- **Important:** Do NOT modify margins or use `\geometry` package
- **TAPS workflow:** Automated typesetting system handles final layout

### Font
- **Primary:** ACM fonts specified in template
- **Figure captions:** Times New Roman, 9pt bold
- **Body text:** Template-controlled (typically 9-10pt)
- **Consistency:** Follow template fonts exactly
- **Important:** Installing ACM fonts may be required for Word templates

### Column Layout
- **Review:** Single-column
- **Publication:** Often two-column (conference-dependent)
- **Flexibility:** Handled by document class options

---

## Page Limits

### Papers (Main Track)
- **Typical limit:** 8-10 pages (excluding references)
- **Variation:** Depends on conference (CHI, UIST, etc.)
- **Content:** Full research presentation
- **References:** Unlimited, do NOT count toward limit

### Extended Abstracts
- **Typical limit:** 4-6 pages (shorter format)
- **Purpose:** Work-in-progress, demonstrations, case studies
- **References:** Unlimited

### Posters and Demos
- **Limit:** 2-4 pages typically
- **Format:** Same template, condensed content

### References
- **Limit:** Unlimited pages
- **Placement:** After main content
- **Note:** References do NOT count toward page limit for most ACM venues

---

## Document Structure

### Required Sections (in order)
1. **Title** - Descriptive and concise
2. **Authors** - Names, affiliations, emails
3. **Abstract** - 150-250 words typical
4. **CCS Concepts** - ACM classification (required)
5. **Keywords** - 3-5 keywords for indexing
6. **Main Content** - Introduction, Related Work, Methods, Results, Discussion
7. **Acknowledgments** - Optional, may count toward page limit
8. **References** - Unlimited, ACM format required

### Abstract Guidelines
- **Length:** 150-250 words typical (check specific conference)
- **Format:** Single paragraph or structured (conference-dependent)
- **Content:** Problem, approach, findings, contribution
- **Placement:** After author block, before CCS concepts

### CCS Concepts (ACM Classification)
- **Required:** ACM Computing Classification System categories
- **Format:** Use ACM's CCS concept generator
- **Example:**
  ```latex
  \begin{CCSXML}
  <ccs2012>
  <concept>
  <concept_id>10003120.10003121</concept_id>
  <concept_desc>Human-centered computing~Visualization</concept_desc>
  <concept_significance>500</concept_significance>
  </concept>
  </ccs2012>
  \end{CCSXML}

  \ccsdesc[500]{Human-centered computing~Visualization}
  ```
- **Tool:** https://dl.acm.org/ccs/ccs.cfm

---

## Citation Style

### Format
- **Style:** Numbered sequential citations
- **In-text:** Bracketed numbers [1], [2], [3]
- **Multiple:** [1, 2] or [1]–[3] for ranges
- **ACM style:** "ACM SIGCHI Proceedings" in citation managers

### Citation Examples

**In-text citations:**
```latex
\documentclass[manuscript,review]{acmart}

% Single citation
See reference~\cite{Author2024}.  % Output: See reference [1].

% Multiple citations
Several studies~\cite{Auth1,Auth2,Auth3}.  % Output: [1, 2, 3] or [1]–[3]

% Narrative citation (if package supports)
Author et al.~\cite{Author2024} found...  % Output: Author et al. [1] found...
```

### Bibliography Format
- **Order:** Numerical, in citation order
- **Numbering:** [1], [2], [3]...
- **Style:** ACM reference format (via `acmart` class)
- **Author names:** Full names preferred over initials

### Reference Examples

**Journal article:**
```latex
@article{author2024,
  author = {Author, First and Coauthor, Second},
  title = {Article Title Here},
  journal = {ACM Trans. Comput.-Hum. Interact.},
  volume = {31},
  number = {2},
  pages = {1--25},
  year = {2024},
  doi = {10.1145/1234567}
}
```

**Conference paper:**
```latex
@inproceedings{author2024conf,
  author = {Author, First and Coauthor, Second},
  title = {Paper Title Here},
  booktitle = {Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems},
  series = {CHI '24},
  year = {2024},
  pages = {1--12},
  doi = {10.1145/1234567}
}
```

---

## Figures and Tables

### Placement
- **Preferred:** Top or bottom of column/page
- **LaTeX option:** `\begin{figure}[t]` or `\begin{figure}[b]`
- **Wide figures:** `\begin{figure*}[t]` for two-column spanning
- **Inline:** Avoid mid-text placement

### Figure Format
- **Preferred:** Vector graphics (PDF, EPS, SVG)
- **Raster:** 300 DPI minimum for photos
- **Width:** Match column width (`\columnwidth` or `\textwidth`)
- **Quality:** High resolution, professionally rendered

### Figure Captions
- **Placement:** Below figures
- **Font:** Times New Roman, 9pt bold (template-controlled)
- **Format:** Spelled-out label: "Figure 1" not "Fig. 1"
- **Description:** Complete sentence describing the figure
- **Accessibility:** Describe content for screen readers

**Example:**
```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\columnwidth]{figure1.pdf}
  \caption{User performance across three conditions. Error bars show 95\% confidence intervals.}
  \label{fig:performance}
\end{figure}
```

### Table Formatting
- **Captions:** Above tables (standard practice)
- **Font:** Template-controlled
- **Format:** Spelled-out label: "Table 1" not "Tab. 1"
- **Rules:** Use `booktabs` for professional appearance
- **Alignment:** Left for text, right for numbers

**Example:**
```latex
\begin{table}[t]
  \caption{Comparison of interaction techniques}
  \label{tab:comparison}
  \begin{tabular}{lcc}
    \toprule
    Technique & Speed (s) & Accuracy (\%) \\
    \midrule
    Baseline & 5.2 & 85.3 \\
    Proposed & 3.8 & 92.1 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### Accessibility Requirements
- **Alt text:** Provide descriptive alternative text
- **Color:** Don't rely solely on color to convey information
- **Contrast:** Ensure sufficient contrast for readability
- **Screen readers:** Structure content for assistive technology
- **Required:** Follow SIGCHI Guide to Accessible Submission

---

## LaTeX Setup

### Document Class

**For Review Submission:**
```latex
\documentclass[manuscript,review,anonymous]{acmart}
```

**For Camera-Ready:**
```latex
\documentclass[sigconf]{acmart}
% Options: sigconf, sigchi, sigplan, acmsmall, acmlarge, etc.
```

### Required Packages (included in acmart)
- Citation management built-in
- Hyperref configured automatically
- Graphics support included
- Table formatting available

### Recommended Additional Packages
```latex
\usepackage{booktabs}     % Professional tables
\usepackage{subcaption}   % Subfigures
\usepackage{algorithm}    % Algorithms
\usepackage{algpseudocode}% Algorithm formatting
```

### Title and Author Block

**Review submission (anonymous):**
```latex
\title{Your Paper Title Here}

\author{Anonymous Authors}
\affiliation{Anonymous Institution}
\email{anonymous@email.com}

% Remove identifying information
```

**Camera-ready:**
```latex
\title{Your Paper Title Here}

\author{First Author}
\affiliation{
  \institution{University Name}
  \city{City}
  \country{Country}
}
\email{first@university.edu}

\author{Second Author}
\affiliation{
  \institution{Company Name}
  \city{City}
  \country{Country}
}
\email{second@company.com}
```

### CCS Concepts and Keywords
```latex
% Use ACM's CCS generator: https://dl.acm.org/ccs/ccs.cfm
\begin{CCSXML}
<ccs2012>
<!-- Generated XML here -->
</ccs2012>
\end{CCSXML}

\ccsdesc[500]{Human-centered computing~Visualization}
\ccsdesc[300]{Human-centered computing~User studies}

\keywords{keyword1, keyword2, keyword3, keyword4}
```

### Document Body
```latex
\begin{document}

\maketitle

\begin{abstract}
Your abstract text here. Concise summary of the research.
\end{abstract}

\section{Introduction}
Your introduction...

\section{Related Work}
Literature review...

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}

\end{document}
```

---

## Compilation

### Standard Workflow
```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex  # Final pass for cross-references
```

### Using latexmk (Recommended)
```bash
latexmk -pdf paper.tex
```

### Accessibility Check
```bash
# Use ACM's accessibility checker (if available)
# Or Adobe Acrobat's accessibility checker
# Verify document structure, alt text, reading order
```

---

## Common Issues

### Template Version Mismatch
- **Problem:** Using outdated acmart.cls
- **Solution:** Download latest from ACM or CTAN
- **Check:** `\listfiles` in LaTeX to see version
- **Update:** Get latest acmart package

### Missing CCS Concepts
- **Problem:** CCS classification required but missing
- **Solution:** Use ACM's CCS generator tool
- **URL:** https://dl.acm.org/ccs/ccs.cfm
- **Format:** Copy generated XML and LaTeX commands

### Wrong Document Class Option
- **Problem:** Using `sigconf` for review (should be `manuscript,review`)
- **Solution:** Check conference requirements for correct option
- **Review:** `\documentclass[manuscript,review,anonymous]{acmart}`
- **Camera-ready:** `\documentclass[sigconf]{acmart}` or conference-specific

### Accessibility Violations
- **Problem:** Missing alt text, poor color contrast, improper structure
- **Solution:** Follow SIGCHI Guide to Accessible Submission
- **Check:** Use accessibility validation tools
- **Required:** Accessible PDFs for submission

### Page Limit Exceeded
- **Check:** Count pages excluding references
- **Solutions:**
  - Tighten writing, reduce redundancy
  - Compress figures or multi-panel layouts
  - Move details to supplementary material
  - Reduce whitespace in tables
  - **Do NOT:** Hack margins or font sizes

### Bibliography Format Errors
- **Problem:** Inconsistent reference formatting
- **Solution:** Use BibTeX with `ACM-Reference-Format` style
- **Required:** `\bibliographystyle{ACM-Reference-Format}`
- **Check:** All references have proper fields (DOI recommended)

---

## Submission Requirements

### PDF Requirements
- **File format:** PDF only
- **Accessibility:** Must meet accessibility standards
- **Fonts:** Embedded (usually automatic with acmart)
- **Quality:** Professional, publication-ready
- **File size:** Reasonable (typically < 20MB)

### Accessibility Compliance
- **Required for all submissions**
- **Checklist:**
  - [ ] Proper document structure (headings, lists, tables)
  - [ ] Alt text for all figures and images
  - [ ] Sufficient color contrast (WCAG AA or better)
  - [ ] Tagged PDF for screen readers
  - [ ] Logical reading order
  - [ ] No information conveyed by color alone
- **Guide:** SIGCHI Guide to Accessible Submission
- **Tools:** Adobe Acrobat Accessibility Checker, PAC 3

### TAPS Workflow
- **The ACM Publishing System (TAPS)**
- **Process:**
  1. Submit LaTeX source files (not just PDF)
  2. TAPS compiles and generates final PDF
  3. Review and approve the output
  4. TAPS publishes to ACM Digital Library
- **Benefits:** Consistent formatting, metadata extraction, accessibility

### Checklist Before Submission
- [ ] Page count within limit (excluding references)
- [ ] Using correct acmart document class option
- [ ] CCS concepts included (generated from ACM tool)
- [ ] Keywords provided (3-5 typical)
- [ ] References use ACM-Reference-Format style
- [ ] Full author names in references (not just initials)
- [ ] Figures have descriptive captions ("Figure 1" not "Fig. 1")
- [ ] Tables have captions above ("Table 1" not "Tab. 1")
- [ ] Accessibility requirements met (alt text, contrast, structure)
- [ ] Anonymous submission (if review phase)
- [ ] LaTeX source files prepared for TAPS (if required)

---

## Template Location

Official templates available at:
- **ACM Publications:** https://www.acm.org/publications/proceedings-template
- **Overleaf ACM Templates:** https://www.overleaf.com/gallery/tagged/acm
- **CTAN acmart:** https://ctan.org/pkg/acmart
- **GitHub (SIGCHI):** https://github.com/sigchi/Document-Formats
- **This bundle:** `@scientificpaper:templates/acm/`

### Template Files
- `acmart.cls` - Document class (required)
- `ACM-Reference-Format.bst` - Bibliography style
- `sample-sigconf.tex` - Conference template example
- `sample-manuscript.tex` - Manuscript template example

---

## Differences from Other Conferences

| Aspect | ACM | NeurIPS | ICML | IEEE | ACL |
|--------|-----|---------|------|------|-----|
| Review layout | **Single-column** | Single | Two | Two | Two |
| Final layout | Variable | Single | Two | Two | Two |
| Page limit | 8-10 + refs | 9 + refs | 8 + refs | 6-8 + refs | 8 + refs |
| Citation | Numbered | Flexible | Flexible | Numbered | natbib |
| Accessibility | **Required** | Optional | Optional | Optional | Optional |
| CCS concepts | **Required** | No | No | Keywords | No |
| Author names | **Full names** | Variable | Variable | Variable | Variable |
| TAPS workflow | **Yes** | No | No | PDF eXpress | No |
| Figure labels | **Spelled out** | Abbreviated OK | Abbreviated OK | Abbreviated | Variable |

**Key Difference:** ACM's strict accessibility requirements and TAPS workflow are unique.

---

## ACM-Specific Best Practices

### CCS Concept Selection
- **Choose 3-5 concepts** from ACM Computing Classification System
- **Assign significance:** 500 (high), 300 (medium), 100 (low)
- **Be specific:** Use fine-grained categories when appropriate
- **Tool:** Use official generator at https://dl.acm.org/ccs/ccs.cfm

### Author Metadata
- **ORCID:** Include ORCID identifiers if available
- **Affiliations:** Complete institution, city, country
- **Emails:** Provide valid contact emails
- **Multiple affiliations:** Supported in acmart

### Rights and Permissions
- **Copyright:** ACM copyright transfer required for accepted papers
- **Options:** Exclusive rights, author-pays (open access), or other agreements
- **Timing:** Usually handled during camera-ready preparation
- **Effect:** May restrict self-archiving (check ACM policy)

### Citation Manager Setup
For Zotero or Mendeley:
- **Style:** Select "ACM SIGCHI Proceedings"
- **Format:** Numbered, in citation order
- **Fields:** Include DOI when available
- **Export:** BibTeX format for LaTeX

---

## Additional Resources

- **ACM Author Center:** https://authors.acm.org/
- **ACM Publications:** https://www.acm.org/publications/
- **CCS Generator:** https://dl.acm.org/ccs/ccs.cfm
- **SIGCHI Resources:** https://sigchi.org/resources/
- **Accessibility Guide:** https://sigchi.org/resources/guides-for-authors/accessibility/
- **TAPS Information:** https://www.acm.org/publications/taps/
- **LaTeX acmart documentation:** https://ctan.org/pkg/acmart

---

## Troubleshooting Commands

```bash
# Check LaTeX compilation
pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex

# Verify acmart version
grep "\\ProvidesClass{acmart}" acmart.cls

# Count pages (excluding references)
# Check PDF manually - references start after main content

# Validate accessibility (requires tool)
# Use Adobe Acrobat: View > Tools > Accessibility > Full Check

# Check file size
ls -lh paper.pdf
```

---

**Last Updated:** 2024
**Valid For:** ACM conferences 2024+ (CHI, UIST, CSCW, etc.)
**Critical Reminders:**
- Accessibility compliance is REQUIRED
- Use spelled-out labels: "Figure 1" not "Fig. 1"
- Include CCS concepts from ACM classification
- Prepare for TAPS workflow (submit source files)
