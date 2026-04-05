---
name: create-and-babysit-pr
description: Create a pull request and then babysit it until CI passes, reviews are addressed, and it's ready to merge.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Agent, AskUserQuestion
---

# Create & Babysit PR

Chain `/create-pr` then `/babysit-pr` in a single invocation.

## Phase 1: Create PR

**You MUST read `.claude/skills/create-pr/SKILL.md` and follow its instructions exactly.** Do not skip reading it or improvise the PR creation process.

Critical constraints from that skill (repeated here as a safety net):
- **Base branch**: Always use `--base main`
- **Context**: Use `git log main..HEAD` and `git diff main...HEAD`

Capture the PR number and URL from the output.

**DO NOT proceed to Phase 2 until ALL of the following are true:**
- The `gh pr create` command completed successfully
- The PR URL has been confirmed in the output
- The PR number has been extracted and validated

**If Phase 1 fails** (push rejected, `gh` auth error, merge conflict on create, or any other error), report the failure and stop. Do not attempt Phase 2.

## Phase 2: Babysit PR

Immediately after the PR is created, execute the `/babysit-pr` skill (`.claude/skills/babysit-pr/SKILL.md`) targeting the newly created PR number.
