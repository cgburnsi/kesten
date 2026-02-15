# Conversion Acceptance Criteria

## Purpose
Define when a converted section is considered complete.

## Section-level definition of done
A converted section is done only if:
1. Source coverage is recorded in `docs/conversion/source-map.md`.
2. QA checklist passes (`docs/conversion/qa_checklist.md`).
3. Worklog status is updated to `reviewed` (`docs/conversion/worklog.md`).
4. Any ambiguities are documented in a "Conversion Notes" subsection.
5. Markdown and LaTeX sync rules are met for the active milestone.

## Milestone-specific acceptance
### Milestone 1
- Markdown is required and readable.
- LaTeX may be omitted unless needed to unblock milestone 2.

### Milestone 2
- LaTeX is required and treated as canonical.
- Markdown must be synced to canonical LaTeX content.

## Review sign-off template
- Source segment: 
- Target files:
- QA checklist: pass/fail
- Open ambiguities:
- Reviewer/date:
