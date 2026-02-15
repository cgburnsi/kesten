# Conversion Specification

## Purpose
Define how source materials are converted into both Markdown and LaTeX during milestone 1 and milestone 2.

## Inputs
- `docs/reference/Kesten_1968_original.pdf`
- `docs/reference/Kesten_1968_Latex_Conversion.pdf`
- `docs/latex/kesten_1968.tex`
- `docs/fortran/*.f`

## Output policy
- Maintain both Markdown and LaTeX outputs.
- Milestone 1 canonical output: Markdown.
- Milestone 2 canonical output: LaTeX (used to build release PDFs).
- When Markdown and LaTeX differ in milestone 2, treat LaTeX as source of truth and update Markdown to match.

## Output location
- Markdown artifacts under `docs/conversion/`.
- LaTeX artifacts under `docs/latex/`.
- Keep milestone-1 and milestone-2 artifacts clearly labeled in filenames or headings.

## Milestone 1 rules (quick, readable)
- Preserve section order and core technical meaning.
- Preserve equations in mathematically equivalent form.
- Preserve all table values and labels; table formatting may be simplified.
- Preserve figure captions and source references.
- Preserve Fortran code logic and comments; normalize indentation only if readability improves.
- Allow minor typography/layout differences and modern Markdown formatting.
- LaTeX updates are optional in milestone 1 unless needed to unblock milestone 2.

## Milestone 2 rules (production-grade faithful)
- Produce faithful LaTeX suitable for generating canonical PDFs.
- Keep Markdown synchronized with the faithful LaTeX content.
- Preserve heading hierarchy and numbering parity with source.
- Preserve equation symbols, indices, and notation exactly.
- Preserve table layout, units, and labels exactly.
- Preserve citation and cross-reference integrity.
- Preserve Fortran structure and comment placement as faithfully as practical.
- Document any ambiguity explicitly in a "Conversion Notes" subsection.

## Conversion process
1. Select a small source section.
2. Convert it according to current milestone rules.
3. Update LaTeX (required in milestone 2; optional in milestone 1).
4. Run QA checklist (`docs/conversion/qa_checklist.md`).
5. Update progress in `docs/conversion/worklog.md`.
6. Commit as a focused docs change.

## Naming conventions
- Suggested section files: `docs/conversion/sections/<NN>-<slug>.md`.
- Use zero-padded section numbers where source numbering exists.
- Keep slugs lowercase with hyphens.
- Suggested LaTeX section files: `docs/latex/sections/<NN>-<slug>.tex`.

## Out of scope for conversion
- Numerical reinterpretation or model changes.
- Solver implementation decisions beyond faithful transcription and notes.
