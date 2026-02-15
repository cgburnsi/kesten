# Known Formatting Deltas

This file tracks non-blocking visual/layout differences between the converted LaTeX output and the legacy source document.

## Current deltas (2026-02-15)
- Overfull table/listing rows in `docs/latex/sections/03-discussion-of-programs.tex` (wide fixed-width numeric blocks in sample I/O tables).
- One oversized float warning in `docs/latex/sections/05-description-of-subroutines.tex` (flowchart figure page fit).
- One TikZ node-border warning in `docs/latex/sections/05-description-of-subroutines.tex` that does not change output semantics.
- Bibliography entries are now wired and rendered, but several legacy references (3-11) still have incomplete publication metadata due scan limitations.

## Acceptance impact
- These deltas are classified as formatting or bibliography-metadata debt.
- They do not block milestone-2 semantic fidelity or reproducible PDF generation.
