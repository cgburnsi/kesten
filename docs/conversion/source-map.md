# Conversion Source Map

## Purpose
Map source material to target conversion files so coverage is explicit and auditable.

## Mapping table
| Source Location | Content Summary | Markdown Target | LaTeX Target | Status | Ambiguity Severity | Notes |
|---|---|---|---|---|---|---|
| `docs/reference/Kesten_1968_original.pdf` (front matter), transcribed from `docs/latex/sections/00-front-matter.tex` | Abstract, Foreword, Summary | `docs/conversion/sections/00-front-matter.md` | `docs/latex/sections/00-front-matter.tex` | reviewed | none | Converted in reading order; no unresolved critical ambiguities. |
| `docs/reference/Kesten_1968_original.pdf` (Introduction), transcribed from `docs/latex/sections/01-introduction.tex` | Introduction | `docs/conversion/sections/01-introduction.md` | `docs/latex/sections/01-introduction.tex` | reviewed | none | Citation references converted to BibTeX keys and compiled in milestone-2 build. |
| `docs/reference/Kesten_1968_original.pdf` (Description of Analyses), transcribed from `docs/latex/sections/02-description-of-analyses.tex` and verified against PDF pages 12-13 for equation clarity | Description of Analyses (one- and two-dimensional models) | `docs/conversion/sections/02-description-of-analyses.md` | `docs/latex/sections/02-description-of-analyses.tex` | reviewed | minor | Legacy Eq. (11) ambiguity text removed after prior page-image verification; minor status remains for bibliography metadata gaps in numbered legacy references. |
| `docs/reference/Kesten_1968_original.pdf` (Discussion of One- and Two-Dimensional Steady-State Computer Programs), transcribed from `docs/latex/sections/03-discussion-of-programs.tex` plus `docs/latex/sections/04-list-of-symbols.tex` | Program discussion, input/output formats, and operational guidance | `docs/conversion/sections/03-discussion-of-programs.md` | `docs/latex/sections/03-discussion-of-programs.tex` + `docs/latex/sections/04-list-of-symbols.tex` | reviewed | minor | Inline placeholders remain for readability, but full omitted blocks are preserved in-file under Fidelity Annex for QA completeness. |
| `docs/reference/Kesten_1968_original.pdf` (Description of Subroutines), transcribed from `docs/latex/sections/05-description-of-subroutines.tex` plus `docs/latex/sections/06-appendix-ii-program-listings.tex` | Subroutine descriptions, equations, and flowchart references | `docs/conversion/sections/04-description-of-subroutines.md` | `docs/latex/sections/05-description-of-subroutines.tex` + `docs/latex/sections/06-appendix-ii-program-listings.tex` | reviewed | minor | Inline placeholders remain for readability, but full omitted blocks are preserved in-file under Fidelity Annex for QA completeness. |

## Coverage checks
- Every source section/page range must map to at least one target file.
- No target section should exist without a source mapping.
- Ambiguous mappings must include rationale in Notes.
- Process sections in document order from abstract to end.

## Status values
- `not started`
- `in progress`
- `converted`
- `reviewed`
- `blocked`

## Ambiguity severity values
- `none`
- `minor`
- `major`
- `critical`
