# Conversion Specification

## Purpose
Define how source materials are converted into Markdown during milestone 1 and milestone 2.

## Inputs
- `docs/reference/Kesten_1968_original.pdf`
- `docs/reference/Kesten_1968_Latex_Conversion.pdf`
- `docs/latex/kesten_1968.tex`
- `docs/fortran/*.f`

## Output location
- Store converted Markdown under `docs/conversion/` unless otherwise specified.
- Keep milestone-1 and milestone-2 artifacts clearly labeled in filenames or headings.

## Milestone 1 rules (quick, readable)
- Preserve section order and core technical meaning.
- Preserve equations in mathematically equivalent form.
- Preserve all table values and labels; table formatting may be simplified.
- Preserve figure captions and source references.
- Preserve Fortran code logic and comments; normalize indentation only if readability improves.
- Allow minor typography/layout differences and modern Markdown formatting.

## Milestone 2 rules (production-grade faithful)
- Preserve heading hierarchy and numbering parity with source.
- Preserve equation symbols, indices, and notation exactly.
- Preserve table layout, units, and labels exactly.
- Preserve citation and cross-reference integrity.
- Preserve Fortran structure and comment placement as faithfully as practical.
- Document any ambiguity explicitly in a "Conversion Notes" subsection.

## Conversion process
1. Select a small source section.
2. Convert it according to current milestone rules.
3. Run QA checklist (`docs/conversion/qa_checklist.md`).
4. Update progress in `docs/conversion/worklog.md`.
5. Commit as a focused docs change.

## Naming conventions
- Suggested section files: `docs/conversion/sections/<NN>-<slug>.md`.
- Use zero-padded section numbers where source numbering exists.
- Keep slugs lowercase with hyphens.

## Out of scope for conversion
- Numerical reinterpretation or model changes.
- Solver implementation decisions beyond faithful transcription and notes.
