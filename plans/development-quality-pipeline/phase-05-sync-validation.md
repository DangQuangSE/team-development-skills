# Phase 5: Sync and Validation

## Goal

Install the new workflow on Claude, Codex, and Antigravity and validate the complete artifact graph.

## Design Constraints

- Preserve platform-specific hooks and compact/SRS configuration.
- Antigravity uses `.agents`, not `.agent`.
- Skills mirror canonical contents exactly; hook adapters may differ.
- Do not leave eval workspaces or temporary test artifacts in the repository.

## Files

- Update canonical README, AGENTS, context routing, and init documentation.
- Add/mirror skills and command/workflow wrappers.
- Merge platform hook registrations and adapters.

## Success Criteria

- All JSON parses and all Python files compile.
- Canonical and mirrored skill directories have no content differences.
- Search confirms every command, hook, and skill registration.
- Receipt happy path and stale-file rejection are demonstrated with temporary files outside the repository.

