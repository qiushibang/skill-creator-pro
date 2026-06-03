# GitHub Project Optimization Plan (2026-06-03)

## Goal

Optimize the public GitHub repository for `skill-creator-pro` so it presents as a clean source repository instead of a mixed source-and-generated-artifacts dump.

## Approved Approach

Adopt plan B:

- rewrite and improve `README.md`
- keep the two overview boards at the very top of the README
- remove public-repo noise such as generated artifacts and system files
- keep the repository source-focused
- keep `evals/` for now, but do not aggressively prune it in this pass

## Changes

### README
- keep the two board visuals first
- add clearer sections for positioning, scenarios, features, quick start, structure, outputs, and validation
- make the repo understandable to a first-time GitHub visitor

### Cleanup
Remove tracked noise from the repository history going forward:
- `.DS_Store`
- `.pytest_cache/`
- `dist/`
- `reports/`

Strengthen `.gitignore` so these stay untracked.

### Non-goals
- no workflow redesign
- no major `evals/` restructuring in this pass
- no release automation changes in this pass

## Acceptance Criteria

- README becomes public-facing and useful
- generated outputs are no longer tracked in Git
- `.gitignore` blocks them from coming back
- repository remains testable locally
- cleanup is committed and pushed to GitHub
