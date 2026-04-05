---
name: babysit-pr
description: Babysit a GitHub pull request by continuously polling CI checks, review comments, and mergeability state until the PR is ready to merge or requires user help. Diagnose failures, retry flaky failures, auto-fix branch-related issues, and address review feedback.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Agent
---

# PR Babysitter

## Objective
Babysit a PR persistently until one of these terminal outcomes occurs:

- The PR is merged or closed.
- CI is successful, there are no unaddressed review comments surfaced by the watcher, all review conversation threads are resolved, required review approval is not blocking merge, and there are no potential merge conflicts (PR is mergeable / not reporting conflict risk).
- A situation requires user help (CI infrastructure issues, repeated flaky failures after retry budget is exhausted, permission problems, or ambiguity that cannot be resolved safely).

Do not stop merely because a single snapshot returns `idle` while checks are still pending.

## Inputs
Accept any of the following:

- No PR argument: infer the PR from the current branch (`--pr auto`)
- PR number
- PR URL

## Core Workflow

1. When the user asks to "monitor"/"watch"/"babysit" a PR, start with the watcher's continuous mode (`--watch`) unless you are intentionally doing a one-shot diagnostic snapshot.
2. Run the watcher script to snapshot PR/CI/review state (or consume each streamed snapshot from `--watch`).
3. Inspect the `actions` list in the JSON response.
4. If `diagnose_ci_failure` is present, load `references/ci-classification.md` and follow its classification guidelines to inspect and classify the failure.
5. If the failure is likely caused by the current branch, patch code locally, commit, and push. Load `references/review-handling.md` and follow "Resolving Threads After Pushing a Fix" to resolve any review threads whose feedback was addressed by this fix.
6. If `process_review_comment` is present, load `references/review-handling.md` and follow its protocol to inspect and address surfaced review items.
7. If a review item is actionable and correct, patch code locally, commit, and push. Immediately resolve the corresponding review thread(s) per `references/review-handling.md`.
8. If `resolve_review_threads` is present, load `references/review-handling.md` and follow "Resolving Unresolved Conversation Threads" to resolve all addressed threads.
9. If the failure is likely flaky/unrelated and `retry_failed_checks` is present, rerun failed jobs with `--retry-failed-now`.
10. If `retrigger_review` is present, a required reviewer's review bot encountered an error. Push an empty commit to re-trigger the review: `git commit --allow-empty -m "ci(tooling): retrigger review (#<PR_NUMBER>)" && git push`. Do this at most 3 times per babysitting session. After pushing, wait for the review bot to start a new session (status changes from `failed` to `in_progress`) before acting on another `retrigger_review`. If the review bot still fails after 3 retrigger attempts, report the failure to the user as a blocker requiring manual intervention.
11. If both actionable review feedback and `retry_failed_checks` are present, prioritize review feedback first; a new commit will retrigger CI, so avoid rerunning flaky checks on the old SHA unless you intentionally defer the review change.
12. On every loop, verify mergeability / merge-conflict status (e.g. via `gh pr view`) in addition to CI and review state.
13. After any push or rerun action, immediately return to step 1 and continue polling on the updated SHA/state.
14. If you had been using `--watch` before pausing to patch/commit/push, relaunch `--watch` yourself in the same turn immediately after the push (do not wait for the user to re-invoke the skill).
15. Repeat polling until the PR is green + review-clean + mergeable, `stop_pr_closed` appears, or a user-help-required blocker is reached.
16. Maintain terminal/session ownership: while babysitting is active, keep consuming watcher output in the same turn; do not leave a detached `--watch` process running and then end the turn as if monitoring were complete.

**Before editing any files**, load `references/git-safety.md` and follow its rules for the duration of this session.

## Commands

### One-shot snapshot

```bash
python3 .claude/skills/babysit-pr/scripts/gh_pr_watch.py --pr auto --once
```

### Continuous watch (JSONL)

```bash
python3 .claude/skills/babysit-pr/scripts/gh_pr_watch.py --pr auto --watch
```

### Trigger flaky retry cycle (only when watcher indicates)

```bash
python3 .claude/skills/babysit-pr/scripts/gh_pr_watch.py --pr auto --retry-failed-now
```

### Explicit PR target

```bash
python3 .claude/skills/babysit-pr/scripts/gh_pr_watch.py --pr <number-or-url> --once
```

If this project later adds a required review bot, append `--require-approval-from '<bot-login>'` to the `--once` / `--watch` invocations.

## Monitoring Loop Pattern
Use this loop in a live session:

1. Run `--once`.
2. Read `actions`.
3. First check whether the PR is now merged or otherwise closed; if so, report that terminal state and stop polling immediately.
4. Check CI summary, new review items, and mergeability/conflict status.
5. Diagnose CI failures: load `references/ci-classification.md` and classify branch-related vs flaky/unrelated.
6. Process actionable review comments before flaky reruns when both are present; if a review fix requires a commit, push it and skip rerunning failed checks on the old SHA.
7. Retry failed checks only when `retry_failed_checks` is present and you are not about to replace the current SHA with a review/CI fix commit.
8. If you pushed a commit or triggered a rerun, report the action briefly and continue polling (do not stop).
9. After a review-fix push, proactively restart continuous monitoring (`--watch`) in the same turn unless a strict stop condition has already been reached.
10. If `resolve_review_threads` is present, load `references/review-handling.md` and resolve addressed threads using the GraphQL mutation.
11. If everything is passing, mergeable, not blocked on required review approval, there are no unaddressed review items, and all conversation threads are resolved, report success and stop.
12. If blocked on a user-help-required issue (infra outage, exhausted flaky retries, unclear reviewer request, permissions), report the blocker and stop.
13. Otherwise sleep according to the polling cadence and repeat.

When the user explicitly asks to monitor/watch/babysit a PR, prefer `--watch` so polling continues autonomously in one command. Use repeated `--once` snapshots only for debugging or when the user explicitly asks for a one-shot check.
Do not stop to ask the user whether to continue polling; continue autonomously until a strict stop condition is met or the user explicitly interrupts.
Do not hand control back to the user after a review-fix push just because a new SHA was created; restarting the watcher and re-entering the poll loop is part of the same babysitting task.

## Polling Cadence
Use adaptive polling and continue monitoring even after CI turns green:

- While CI is not green (pending/running/queued or failing): poll every 1 minute.
- After CI turns green: start at every 1 minute, then back off exponentially when there is no change (1m, 2m), capping at every 3 minutes.
- Reset the green-state polling interval back to 1 minute whenever anything changes (new commit/SHA, check status changes, new review comments, mergeability changes, review decision changes).
- If CI stops being green again (new commit, rerun, or regression): return to 1-minute polling.
- If any poll shows the PR is merged or otherwise closed: stop polling immediately and report the terminal state.

## Stop Conditions (Strict)
Stop only when one of the following is true:

- PR merged or closed (stop as soon as a poll/snapshot confirms this).
- PR is ready to merge: CI succeeded, no surfaced unaddressed review comments, all review conversation threads resolved, not blocked on required review approval, and no merge conflict risk. If `--require-approval-from` was passed, also require that each listed reviewer has submitted an APPROVED review (check `required_approvals.satisfied` in the snapshot).
- User intervention is required and cannot safely proceed alone.

Keep polling when:

- `actions` contains only `idle` but checks are still pending.
- CI is still running/queued.
- Review state is quiet but CI is not terminal.
- CI is green but mergeability is unknown/pending.
- CI is green and mergeable, but the PR is still open and you are waiting for possible new review comments or merge-conflict changes per the green-state cadence.
- The PR is green but blocked on review approval; continue polling on the green-state cadence and surface any new review comments.
- `--require-approval-from` was passed and a listed reviewer has not yet approved; continue polling and address any `CHANGES_REQUESTED` feedback from them. Report waiting status: `Waiting for required approval. Current state: <details from required_approvals>`.

## Output Expectations
Provide concise progress updates while monitoring and a final summary that includes:

- During long unchanged monitoring periods, avoid emitting a full update on every poll; summarize only status changes plus occasional heartbeat updates.
- Treat push confirmations, intermediate CI snapshots, and review-action updates as progress updates only; do not emit the final summary or end the babysitting session unless a strict stop condition is met.
- When CI first transitions to all green for the current SHA, emit a one-time celebratory progress update. Preferred style: `CI is all green! 33/33 passed. Still on watch for review approval.`
- Do not send the final summary while a watcher terminal is still running unless the watcher has emitted/confirmed a strict stop condition.

Final summary includes:
- Final PR SHA
- CI status summary
- Mergeability / conflict status
- Vercel web preview URL (fetch from the `vercel[bot]` comment on the PR using `gh api repos/{owner}/{repo}/issues/{pr_number}/comments --jq '.[] | select(.user.login == "vercel[bot]") | .body'` and extract the **web** project's Preview link). If the web deployment status is "Ignored" or "Canceled", report it as skipped instead of showing the URL.
- Fixes pushed
- Flaky retry cycles used
- Remaining unresolved failures or review comments

## References

- CI failure classification and Vercel logs: `references/ci-classification.md`
- Review comment handling and thread resolution: `references/review-handling.md`
- Git safety rules and commit conventions: `references/git-safety.md`
- Heuristics and decision tree: `references/heuristics.md`
- GitHub CLI/API details used by the watcher: `references/github-api-notes.md`
