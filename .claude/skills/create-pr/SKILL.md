---
name: create-pr
description: Create a pull request for the current branch following the project's PR conventions.
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

Create a pull request for the current branch.

Load `references/pr-conventions.md` for title format, body template, and constraints.

## Steps

1. **Gather context about changes**
   - Use your existing conversation context first
   - If you lack context, run `git status`, `git log main..HEAD --oneline`, and `git diff main...HEAD`
   - Also check for staged (`git diff --cached`) and unstaged (`git diff`) changes — these may need to be committed before creating the PR
   - If there are uncommitted changes, ask the user whether to commit them and what to include before proceeding

   **DO NOT proceed to Step 2 until:**
   - All changes intended for the PR are committed and pushed
   - There are no uncommitted changes the user wants included

2. **Draft and create the PR**
   - Follow the title format and body template from `references/pr-conventions.md`
   - Push to remote with `-u` flag if needed
   - Create PR using `gh pr create --base main`

   **Verify:** Confirm the `gh pr create` command succeeded and capture the PR URL.
   If the command fails (auth error, push rejected, conflict), report the error and stop — do not retry blindly.

3. **Return the PR URL**
