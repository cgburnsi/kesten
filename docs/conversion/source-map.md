# Conversion Source Map

## Purpose
Map source material to target conversion files so coverage is explicit and auditable.

## Mapping table
| Source Location | Content Summary | Markdown Target | LaTeX Target | Status | Ambiguity Severity | Notes |
|---|---|---|---|---|---|---|
| `docs/reference/Kesten_1968_original.pdf` (front matter), transcribed from `docs/latex/kesten_1968.tex` lines 52-96 | Abstract, Foreword, Summary | `docs/conversion/sections/00-front-matter.md` | pending (milestone 2) | reviewed | none | Converted in reading order; no unresolved critical ambiguities. |
| `docs/reference/Kesten_1968_original.pdf` (Introduction), transcribed from `docs/latex/kesten_1968.tex` lines 97-107 | Introduction | `docs/conversion/sections/01-introduction.md` | pending (milestone 2) | reviewed | none | Ref. [1]-[2] metadata pending bibliography pass. |
| `docs/reference/Kesten_1968_original.pdf` (Description of Analyses), transcribed from `docs/latex/kesten_1968.tex` lines 108-338 and verified against PDF pages 12-13 for equation clarity | Description of Analyses (one- and two-dimensional models) | `docs/conversion/sections/02-description-of-analyses.md` | pending (milestone 2) | reviewed | minor | Primary ambiguity in legacy transcription (Eq. 11) verified from source image; section passes milestone-1 QA with minor formatting debt only. |
| `docs/reference/Kesten_1968_original.pdf` (Discussion of One- and Two-Dimensional Steady-State Computer Programs), transcribed from `docs/latex/kesten_1968.tex` lines 339-1139 | Program discussion, input/output formats, and operational guidance | `docs/conversion/sections/03-discussion-of-programs.md` | pending (milestone 2) | converted | major | QA run recorded in `docs/conversion/qa_results.md`; table/listing completeness checks remain open due placeholders. |
| `docs/reference/Kesten_1968_original.pdf` (Description of Subroutines), transcribed from `docs/latex/kesten_1968.tex` lines 1140-2062 | Subroutine descriptions, equations, and flowchart references | `docs/conversion/sections/04-description-of-subroutines.md` | pending (milestone 2) | converted | major | QA run recorded in `docs/conversion/qa_results.md`; figure/listing completeness checks remain open due placeholders. |

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
