# arXiv Preprint Format Specification

**Repository:** arXiv.org - Open-access preprint repository
**Maintained By:** Cornell University
**Official Site:** https://arxiv.org/

---

## Document Format

### File Format Requirements
- **Recommended:** TeX/LaTeX source (strongly preferred)
- **Alternative:** PDF (for non-TeX submissions, limited support)
- **NOT Accepted:**
  - DVI files
  - PostScript (PS) files
  - PDF created from TeX/LaTeX source (submit source instead)
  - Scanned documents

### Paper Size
- **Flexible:** No strict paper size requirement
- **Common:** US Letter or A4
- **Recommendation:** Match target conference format if preparing for submission
- **Note:** arXiv will generate PDF from your source

### File Naming Conventions
- **Case sensitive:** `myfile.tex` ≠ `MyFile.tex` ≠ `MYFILE.TEX`
- **Prohibited characters:** Spaces, question marks, asterisks
- **Recommended:** Lowercase, simple names
- **Examples:**
  - ✅ `paper.tex`, `main.tex`, `figure1.pdf`
  - ❌ `My Paper.tex`, `figure?.pdf`, `draft*.tex`

### Font Requirements
- **No restrictions:** Use standard LaTeX fonts
- **Embedding:** Fonts automatically embedded in generated PDF
- **Common choices:** Computer Modern, Times, Helvetica
- **Recommendation:** Use conference style if preparing for submission

---

## Page Limits

### No Official Limits
- **arXiv:** No page limit for preprints
- **Best practice:** Keep reasonable length (typically < 50 pages for main content)
- **Appendices:** Can be extensive for technical proofs
- **Recommendation:** Follow target conference guidelines if applicable

### Practical Considerations
- **Main paper:** Typically 8-15 pages for standard research
- **Extended versions:** 20-30 pages with additional appendices
- **Surveys/Reviews:** 30-50+ pages acceptable
- **Technical reports:** Can be longer with detailed proofs

---

## Document Structure

### Recommended Sections (for research papers)
1. **Title** - Descriptive and searchable
2. **Authors** - Names and affiliations
3. **Abstract** - 150-300 words (searchable and indexed)
4. **Main Content** - Introduction, Methods, Results, Discussion
5. **Acknowledgments** - Optional
6. **References** - Comprehensive bibliography
7. **Appendices** - Optional, for detailed proofs/experiments

### Abstract Guidelines
- **Length:** 150-300 words typical
- **Purpose:** Indexed and searchable on arXiv
- **Content:** Clear problem statement, approach, key results
- **SEO:** Use keywords that help discoverability
- **Note:** Abstract appears in search results and RSS feeds

### Title Guidelines
- **Descriptive:** Clear indication of content
- **Keywords:** Include important terms for search
- **Length:** Concise but informative (avoid excessive length)
- **Avoid:** Clickbait, excessive jargon

---

## Citation Style

### Complete Flexibility
- **Any style acceptable:** No arXiv-specific requirements
- **Recommendation:** Use target conference style if applicable
- **Common choices:** Author-year, numbered, alphabetical
- **Consistency:** Maintain consistent format throughout

### Citation Examples

**Author-year (natbib):**
```latex
\usepackage{natbib}
\bibliographystyle{plainnat}

% In text
\citet{Author2024} proposed...  % Author (2024) proposed...
See \citep{Author2024}.         % See (Author, 2024).
```

**Numbered:**
```latex
\bibliographystyle{plain}

% In text
See reference \cite{Author2024}.  % See reference [1].
```

**Alphabetical:**
```latex
\bibliographystyle{alpha}

% In text
See reference \cite{Author2024}.  % See reference [Auth24].
```

### arXiv Citations
- **arXiv papers:** Include arXiv identifier in bibliography
- **Format:** `arXiv:YYMM.NNNNN` (e.g., `arXiv:2401.12345`)
- **Example:**
  ```latex
  @article{author2024,
    title = {Paper Title},
    author = {Author, First},
    year = {2024},
    eprint = {2401.12345},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
  }
  ```

---

## Figures and Tables

### Figure Format Requirements

**For PDFLaTeX (recommended):**
- **Accepted:** `.pdf`, `.jpg`, `.png`
- **NOT accepted:** `.ps`, `.eps`
- **Recommendation:** PDF for vector graphics, PNG for rasters

**For Traditional LaTeX:**
- **Accepted:** `.ps`, `.eps`
- **NOT accepted:** `.pdf`, `.jpg`, `.png`

**⚠️ CRITICAL:** arXiv does NOT convert figure formats. Ensure correct format before submission.

### Figure Organization
```
submission/
├── main.tex
├── figure1.pdf      # Correct format for pdflatex
├── figure2.png
├── diagram.pdf
└── styles/
    └── custom.sty
```

### Figure Best Practices
- **Resolution:** 300 DPI for raster images
- **Vector preferred:** Use PDF for diagrams, plots, charts
- **File size:** Compress large images (keep reasonable quality)
- **Testing:** Verify all figures compile locally before submission

### Table Formatting
- **No restrictions:** Use any LaTeX table package
- **Recommendation:** `booktabs` for professional appearance
- **Complex tables:** Consider breaking into multiple simpler tables

---

## LaTeX Setup

### Document Class
```latex
% Use standard article class or conference style
\documentclass{article}
% OR use target conference class
\documentclass{neurips_2024}
```

### Recommended Packages
```latex
\usepackage[utf8]{inputenc}    % UTF-8 encoding
\usepackage{graphicx}           % For figures
\usepackage{amsmath,amssymb}    % Mathematics
\usepackage{hyperref}           % Hyperlinks (configure properly!)
\usepackage{natbib}             % Citations (if using author-year)
\usepackage{booktabs}           % Professional tables
\usepackage{algorithm}          % Algorithms
\usepackage{algorithmic}        % Algorithm formatting
```

### Hyperref Configuration
```latex
% Configure hyperref to avoid common issues
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  citecolor=blue,
  urlcolor=blue,
  pdftitle={Your Paper Title},
  pdfauthor={Your Name},
  pdfsubject={Subject Area},
  pdfkeywords={keyword1, keyword2, keyword3}
}
```

### Title and Author Block
```latex
\title{Your Paper Title Here}

\author{
  First Author \\
  Institution \\
  \texttt{email@domain.com}
  \And
  Second Author \\
  Institution \\
  \texttt{email@domain.com}
}

\date{\today}  % Or specific date

\begin{document}
\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}
```

---

## Compilation and Preparation

### Local Compilation Workflow
```bash
# Standard workflow
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Or using latexmk (recommended)
latexmk -pdf main.tex
```

### Pre-Submission Checklist

**Required Files:**
- [ ] Main `.tex` file
- [ ] Compiled `.bbl` file (pre-compile bibliography!)
- [ ] All figure files in correct format (PDF/PNG/JPG for pdflatex)
- [ ] Custom style files (`.sty`) if used
- [ ] Any additional `.tex` files (if multi-file structure)

**File Verification:**
```bash
# Verify compilation
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# Check all figures referenced
grep -r "includegraphics" *.tex

# List all files for submission
ls -la
```

### Bibliography Compilation
```bash
# CRITICAL: Generate .bbl file before submission
pdflatex main.tex
bibtex main      # Creates main.bbl
pdflatex main.tex
pdflatex main.tex

# Verify .bbl file exists
ls -la main.bbl
```

**⚠️ IMPORTANT:** arXiv requires pre-compiled `.bbl` file. Do NOT submit just `.bib` file.

---

## Common Issues and Fixes

### Top 5 Common Mistakes

**1. Mixed Figure File Formats**
- **Problem:** Using both `.pdf` and `.eps` figures with pdflatex
- **Solution:** Use only `.pdf`, `.jpg`, `.png` for pdflatex
- **Fix:** Convert all figures to PDF format before submission

**2. Case Mismatch in Filenames**
- **Problem:** `\includegraphics{Figure1.pdf}` but file is `figure1.pdf`
- **Solution:** Ensure exact case match between code and filenames
- **Check:** Works on Windows/Mac but fails on Linux (arXiv uses Linux)

**3. Default Hyperref Failures**
- **Problem:** Hyperref package with default settings causes compilation errors
- **Solution:** Configure hyperref explicitly (see LaTeX Setup section)
- **Alternative:** Load hyperref last and use `\hypersetup{}`

**4. Missing or Mismatched Style Files**
- **Problem:** Using `\usepackage{custom}` but not including `custom.sty`
- **Solution:** Include all custom style files in submission
- **Check:** Verify all custom packages are in submission directory

**5. Locally-Pathed Figure References**
- **Problem:** `\includegraphics{/Users/me/figures/fig1.pdf}`
- **Solution:** Use relative paths only: `\includegraphics{figures/fig1.pdf}`
- **Organization:** Keep all files in submission directory structure

### Bibliography Not Appearing
- **Problem:** References section is empty or missing
- **Solution:** Include compiled `.bbl` file in submission
- **Workflow:**
  ```bash
  pdflatex main.tex
  bibtex main      # Must run this!
  pdflatex main.tex
  pdflatex main.tex
  ```
- **Verify:** Check that `main.bbl` file exists and has content

### Hyperref Errors
- **Problem:** Compilation fails with hyperref-related errors
- **Solution:** Load hyperref last and configure properly
- **Fix:**
  ```latex
  % Load other packages first
  \usepackage{graphicx}
  \usepackage{amsmath}
  % Load hyperref LAST
  \usepackage{hyperref}
  \hypersetup{colorlinks=true}
  ```

### File Upload Failures
- **Problem:** arXiv rejects file upload
- **Common causes:**
  - Prohibited characters in filenames
  - Missing required files
  - Incorrect figure formats
- **Solution:** Review error message, fix issues, re-upload

### Source Files Publicly Accessible
- **Problem:** LaTeX comments contain sensitive information
- **Solution:** Clean source files before submission
- **Actions:**
  - Remove internal comments
  - Remove proprietary notes
  - Remove confidential information
  - Remove debug code
- **Reminder:** Source files are PUBLICLY accessible on arXiv

---

## Submission Process

### arXiv Submission Workflow

1. **Create Account:** Register at arXiv.org
2. **Get Endorsement:** May be required for first submission or new category
3. **Prepare Files:** Compile locally, verify all files included
4. **Upload Source:** Submit TeX/LaTeX source files (not just PDF)
5. **Review Output:** Check arXiv-generated PDF
6. **Submit:** Complete metadata and submit for moderation

### Endorsement System
- **New users:** May require endorsement from established arXiv author
- **New categories:** Submitting to new subject area may require endorsement
- **Process:** Request endorsement through arXiv system
- **Timeline:** Usually 1-2 days for endorsement

### Metadata Requirements
- **Title:** Match title in paper
- **Authors:** All authors with affiliations
- **Abstract:** Copy from paper (plain text, no LaTeX)
- **Categories:** Primary and optional secondary categories
- **Comments:** Optional notes (e.g., "Submitted to ICML 2025")
- **MSC/ACM classes:** Optional classification codes

### Licensing
- **Required:** Grant arXiv.org irrevocable license to distribute
- **Your rights:** Retain copyright and other distribution rights
- **Policies:** Accept Submittal Agreement, Code of Conduct, Moderation and Privacy Policies

---

## Submission Requirements

### File Organization
```
submission/
├── main.tex           # Main document
├── main.bbl           # Compiled bibliography (REQUIRED)
├── references.bib     # BibTeX file (optional but recommended)
├── figures/
│   ├── figure1.pdf
│   ├── figure2.png
│   └── diagram.pdf
├── styles/
│   └── custom.sty     # If using custom styles
└── sections/          # If multi-file
    ├── intro.tex
    └── methods.tex
```

### Checklist Before Submission
- [ ] LaTeX source compiles locally without errors
- [ ] All figures in correct format (PDF/PNG/JPG for pdflatex)
- [ ] Filenames are case-consistent and simple (no spaces or special chars)
- [ ] `.bbl` file included (bibliography pre-compiled)
- [ ] All custom style files included
- [ ] No locally-pathed references (`/Users/...` or `C:\...`)
- [ ] Hyperref configured (if used)
- [ ] Source files cleaned (no sensitive comments)
- [ ] Abstract is clear and searchable
- [ ] Title includes relevant keywords
- [ ] All co-authors listed correctly
- [ ] Appropriate arXiv category selected

---

## arXiv Categories

### Major Categories
- **cs.** - Computer Science (cs.AI, cs.LG, cs.CV, cs.CL, cs.NE, etc.)
- **math.** - Mathematics (math.OC, math.ST, math.NA, etc.)
- **stat.** - Statistics (stat.ML, stat.ME, stat.TH, etc.)
- **physics.** - Physics (physics.data-an, etc.)
- **eess.** - Electrical Engineering and Systems Science
- **q-bio.** - Quantitative Biology

### Choosing Categories
- **Primary:** Main subject area (required)
- **Secondary:** Additional relevant categories (optional)
- **Cross-listing:** Paper appears in multiple category listings
- **Examples:**
  - Machine learning paper: Primary `cs.LG`, Secondary `stat.ML`
  - Computer vision: Primary `cs.CV`, Secondary `cs.AI`

---

## Best Practices

### For Conference Submissions
If preparing for conference submission:
- **Use conference style:** Include conference LaTeX class
- **Follow conference format:** Match formatting requirements
- **Version note:** Add comment: "Submitted to CONFERENCE 2025"
- **Update after acceptance:** Replace with "Accepted at CONFERENCE 2025"

### For Journal Submissions
- **Preprint first:** Submit to arXiv before journal (check journal policy)
- **Version tracking:** Update arXiv when journal version changes
- **DOI:** Include journal DOI in arXiv metadata after publication

### Version Management
- **Versioning:** arXiv automatically versions (v1, v2, v3, etc.)
- **Updates:** Can submit revised versions
- **Changelog:** Include version notes in comments field
- **Withdrawal:** Can withdraw paper (creates permanent withdrawal notice)

### Maximizing Discoverability
- **Title:** Include key terms people might search
- **Abstract:** Use standard terminology in your field
- **Categories:** Choose all relevant categories
- **Comments:** Add conference/journal information
- **Keywords:** Use in PDF metadata (via `\hypersetup`)

---

## Differences from Conference Formats

| Aspect | arXiv | NeurIPS | ICML | ACL | IEEE |
|--------|-------|---------|------|-----|------|
| Paper size | **Flexible** | Letter | Letter | A4 | Letter/A4 |
| Page limit | **None** | 9 + refs | 8 + refs | 8 + refs | 6-8 |
| Format | **Source required** | PDF | PDF | PDF | PDF |
| Citation | **Any style** | Flexible | Flexible | natbib | Numbered |
| Figures | **Format strict** | Flexible | Flexible | Flexible | Flexible |
| Review | **No review** | Peer review | Peer review | Peer review | Peer review |
| Timeline | **Immediate** | Months | Months | Months | Months |
| Versioning | **Yes (v1,v2...)** | No | No | No | No |
| Updates | **Allowed** | No | No | No | No |

**Key Differences:**
- arXiv accepts ANY length
- Source files REQUIRED (not just PDF)
- Figure format is STRICT (no conversion)
- No peer review (moderation only)
- Versioning supported
- Publicly accessible immediately

---

## Additional Resources

- **arXiv Help:** https://info.arxiv.org/help/
- **Submission Guide:** https://info.arxiv.org/help/submit/index.html
- **TeX Submissions:** https://info.arxiv.org/help/submit_tex.html
- **Moderation:** https://info.arxiv.org/help/moderation/index.html
- **FAQ:** https://info.arxiv.org/help/faq/
- **Categories:** https://arxiv.org/category_taxonomy

---

## Troubleshooting Commands

```bash
# Test compilation locally
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# Check for all figure references
grep -r "includegraphics" *.tex

# Verify .bbl file exists and has content
cat main.bbl

# List all files (check for spaces or special characters)
ls -la

# Check figure formats
file figures/*

# Find all .tex files
find . -name "*.tex"

# Check for absolute paths (BAD)
grep -r "/Users/\|/home/\|C:\\\\" *.tex

# Verify UTF-8 encoding
file -i *.tex
```

---

## Testing with Overleaf

If unsure about submission, test on Overleaf first:

1. **Upload to Overleaf:** Create project, upload all files
2. **Compile:** Verify compilation works
3. **Download source:** Download source files from Overleaf
4. **Submit to arXiv:** Upload downloaded source to arXiv
5. **Benefit:** Overleaf environment similar to arXiv

---

**Last Updated:** 2024
**Valid For:** arXiv submissions 2024+
**Critical Reminders:**
- Source files are PUBLICLY accessible
- Pre-compile .bbl file (required!)
- Figure formats must be exact (no conversion)
- Clean all sensitive comments before submission
