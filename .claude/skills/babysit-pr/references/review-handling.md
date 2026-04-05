# Review Comment Handling

## Sources
The watcher surfaces review items from:

- PR issue comments
- Inline review comments
- Review submissions (COMMENT / APPROVED / CHANGES_REQUESTED)

It surfaces trusted human review authors (repo OWNER/MEMBER/COLLABORATOR, plus the authenticated operator) and approved review bots.
On a fresh watcher state file, existing pending review feedback may be surfaced immediately. This is intentional so already-open review comments are not missed.

## Addressing actionable comments

When you agree with a comment and it is actionable:

1. Patch code locally.
2. Commit with `fix(<scope>): address PR review feedback (#<n>)`.
3. Push to the PR head branch.
4. Reply to each addressed inline comment and resolve the thread (see "Resolving Threads After Pushing a Fix" below).
5. If a `CHANGES_REQUESTED` review has all its threads resolved, dismiss the stale review:
   ```bash
   # Find ALL blocking review IDs (--paginate is required; without it, PRs with >30 reviews silently miss later pages)
   gh api repos/{owner}/{repo}/pulls/{pr}/reviews --paginate --jq '.[] | select(.state == "CHANGES_REQUESTED") | {id, author: .user.login}'
   # Dismiss each one
   gh api repos/{owner}/{repo}/pulls/{pr}/reviews/{review_id}/dismissals -X PUT -f message="All threads resolved. Fixes pushed in <sha>."
   # Verify reviewDecision has cleared after all dismissals
   gh pr view {pr} -R {owner}/{repo} --json reviewDecision --jq '.reviewDecision'
   ```
   **Important**: The GitHub REST API defaults to 30 results per page. Always use `--paginate` when fetching reviews to avoid missing `CHANGES_REQUESTED` reviews beyond the first page.
6. Resume watching on the new SHA immediately (do not stop after reporting the push).
7. If monitoring was running in `--watch` mode, restart `--watch` immediately after the push in the same turn.

## Non-actionable comments

If you disagree or the comment is non-actionable/already addressed, **reply to the inline comment** with a brief explanation before continuing the watcher loop. This is required so that review bots that track author engagement can detect that the concern was acknowledged.

```bash
# Reply to dismiss a non-actionable inline comment
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
  -f body="Acknowledged — intentionally keeping as-is. <brief reason>"
```

Then resolve the thread:
```bash
gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "<thread_node_id>"}) { thread { isResolved } } }'
```

If a code review comment/thread is already marked as resolved in GitHub, treat it as non-actionable and safely ignore it — no reply is needed.

## Triggering bot re-review after dismissal without code changes

When you dismiss a bot's `CHANGES_REQUESTED` review because the feedback was a false positive (no code changes needed), the bot will not automatically re-review — bots are triggered by push events, not review-request events.

To trigger a re-review, push an empty commit:
```bash
git commit --allow-empty -m "ci(tooling): trigger bot re-review"
git push
```

Then resume the polling loop on the new SHA. The bot should pick up the push event and submit a new review.

## Comment severity classification

Classify each review comment before acting:

- **Must fix**: Technically correct, actionable in the current branch, no conflict with user intent, can be made safely without unrelated refactors.
- **Discuss**: Ambiguous, requires clarification, or needs product/design decisions the user has not made.
- **Skip**: Already resolved, bot noise, conflicts with explicit user instructions, or codebase is in a dirty/unrelated state.

Address **Must fix** items immediately. For **Discuss** items, stop and ask the user. For **Skip** items, reply with a brief dismissal reason (per "Non-actionable comments" above), resolve the thread, and continue the watcher loop.

## Resolving Unresolved Conversation Threads

GitHub branch protection may require all review conversation threads to be resolved before merging. The watcher reports `unresolved_threads` with `count` and `thread_ids` in each snapshot. When `resolve_review_threads` appears in `actions`:

1. The watcher has detected unresolved threads that block merge, but no new review items to process.
2. For each thread ID in `unresolved_threads.thread_ids`, determine if the feedback was already addressed (by a prior commit, autofix bot, or manual fix).
3. If the feedback has been addressed, resolve the thread:
   ```bash
   gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "<thread_node_id>"}) { thread { isResolved } } }'
   ```
4. If you are unsure whether a thread's feedback was addressed, read the thread comments and the relevant code diff to decide.
5. Do NOT resolve threads whose feedback has NOT been addressed — leave them open for the reviewer.
6. After resolving threads, continue the watcher loop to verify the count drops to zero.

## Resolving Threads After Pushing a Fix

**Every time you push a commit that addresses review feedback, you MUST resolve the related threads in the same action — before resuming polling.** This applies to both review-comment-driven fixes and CI-failure fixes that also address a review comment.

1. Identify which review threads your fix addresses. Match by file path, line range, and comment content.
2. Reply to each addressed inline comment with a brief note referencing the fix commit:
   ```bash
   # Reply to an inline review comment
   gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body="Fixed in <sha>."
   ```
   For issue-level comments:
   ```bash
   gh api repos/{owner}/{repo}/issues/{pr}/comments -f body="Addressed in <sha>."
   ```
3. Resolve each corresponding thread:
   ```bash
   gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "<thread_node_id>"}) { thread { isResolved } } }'
   ```
4. If a `CHANGES_REQUESTED` review now has all its threads resolved, dismiss the stale review:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{pr}/reviews --paginate --jq '.[] | select(.state == "CHANGES_REQUESTED") | {id, author: .user.login}'
   gh api repos/{owner}/{repo}/pulls/{pr}/reviews/{review_id}/dismissals -X PUT -f message="All threads resolved. Fixes pushed in <sha>."
   ```
5. Only then resume the watcher / return to the polling loop.

**Do not skip this step.** Leaving threads unresolved after pushing the fix causes unnecessary extra poll cycles and may block merge if branch protection requires all threads resolved.
