# AI Lab Workflow

## Principle

The AI Lab workflow keeps AI-assisted work reviewable, traceable, and small. The
repository should make it clear what was requested, what changed, why it changed,
and what remains uncertain.

## Standard Flow

1. Open or select an issue.
2. Define scope, acceptance criteria, and source material.
3. Create a focused branch.
4. Ask Codex to inspect before implementation.
5. Review the inspection result and adjust scope if needed.
6. Ask Codex to implement the approved change.
7. Run relevant checks.
8. Open a pull request.
9. Review the diff and risk notes.
10. Squash merge after approval.

Do not push directly to `main`.

## Codex Inspect Mode

Use inspect mode when the task is unclear, when repository context is needed, or
before implementation. Codex should report:

- Files inspected.
- Current repository state.
- Relevant constraints.
- Proposed files to change.
- Risks, missing sources, or questions.

Inspect mode should not modify files.

## Codex Implement Mode

Use implement mode after scope is clear. Codex should:

- Keep changes minimal and atomic.
- Avoid unrelated refactors.
- Preserve public content boundaries.
- Add or update documentation when the behavior or workflow changes.
- Run checks that match the change.
- Report diff summary and git status.

## Pull Request Requirements

Each pull request should include:

- Linked issue.
- Summary of changes.
- Files changed.
- Checks run.
- Public content and privacy review.
- Remaining risks or TODOs.

## Merge Policy

Use squash merge to keep `main` readable. The final commit message should be
short, factual, and scoped to the issue.

