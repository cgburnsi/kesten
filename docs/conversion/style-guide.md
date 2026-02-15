# Conversion Style Guide

## Purpose
Define formatting conventions used across conversion outputs to keep Markdown and LaTeX consistent.

## Markdown conventions
- Headings: use ATX style (`#`, `##`, `###`) with sentence-case titles.
- Equations (inline): `$...$`
- Equations (display):
  ```
  $$
  ...
  $$
  ```
- Tables: use pipe tables with explicit units in header labels.
- Code blocks (Fortran): fenced blocks with `fortran` info string.
- File references: use relative project paths in backticks.

## LaTeX conventions
- Keep sectioning aligned with source (`\section`, `\subsection`, etc.).
- Prefer explicit equation environments for numbered equations.
- Preserve source notation and symbol naming exactly in milestone 2.
- Keep comments concise and only for ambiguity notes.

## Cross-format consistency rules
- Equation variable names and indices must match across Markdown and LaTeX.
- Table values, labels, and units must match across Markdown and LaTeX.
- Figure captions and references must be semantically identical.

## Citation/reference conventions
- Markdown: use numeric bracket citations (for example, `[1]`, `[2]`) and keep a `## References` section at the end of each converted document/chapter.
- LaTeX: use BibTeX with a dedicated `.bib` file and standard `\cite{key}` commands.
- Keep citation keys stable and human-readable (for example, `kesten1968`, `fortran-main`).
- Ensure Markdown reference numbering and LaTeX bibliography entries point to the same source records.

## Open decisions
- Heading numbering: use standard report-style numbering synchronized with source hierarchy in milestone 2.
- Line wrapping: use default LaTeX/editor behavior for now; revisit only if readability degrades.
