# Git Safety Rules

- Work only on the PR head branch.
- Avoid destructive git commands.
- Do not switch branches unless necessary to recover context.
- Before editing, check for unrelated uncommitted changes. If present, stop and ask the user.
- After each successful fix, commit and `git push`, then re-run the watcher.
- If you interrupted a live `--watch` session to make the fix, restart `--watch` immediately after the push in the same turn.
- Do not run multiple concurrent `--watch` processes for the same PR/state file.
- A push is not a terminal outcome; continue the monitoring loop unless a strict stop condition is met.

## Commit message conventions

- `fix: CI failure on PR #<n>`
- `fix: address PR review feedback (#<n>)`
