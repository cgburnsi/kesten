# Conversion QA Checklist

Run this checklist for each converted section before marking it `reviewed`.

## Content integrity
- [ ] Section title matches source intent.
- [ ] Section ordering relative to adjacent sections is correct.
- [ ] No missing paragraphs that carry technical meaning.
- [ ] No added claims not supported by source.

## Equations and symbols
- [ ] Variables and subscripts/superscripts are preserved.
- [ ] Equation relationships are mathematically equivalent (milestone 1) or exact (milestone 2).
- [ ] Equation numbering/callouts are preserved where required.

## Tables and figures
- [ ] Table values are complete and accurate.
- [ ] Units and labels are preserved.
- [ ] Figure captions and references are present.

## Fortran listings
- [ ] Statements preserved in correct order.
- [ ] Labels, continuations, and comments are preserved or explicitly noted.
- [ ] No logic changes introduced during formatting.

## References and notes
- [ ] Citations/cross-references remain traceable.
- [ ] Ambiguities are captured in a "Conversion Notes" subsection.

## Final check
- [ ] Worklog updated in `docs/conversion/worklog.md`.
- [ ] File paths and links render correctly in Markdown preview.
