# GitHub CLI / API Notes For `babysit-pr`

## Primary commands used

### PR metadata

- `gh pr view --json number,url,state,mergedAt,closedAt,headRefName,headRefOid,headRepository,headRepositoryOwner`

Used to resolve PR number, URL, branch, head SHA, and closed/merged state.

### PR checks summary

- `gh pr checks --json name,state,bucket,link,workflow,event,startedAt,completedAt`

Used to compute pending/failed/passed counts and whether the current CI round is terminal.

### Workflow runs for head SHA

- `gh api repos/{owner}/{repo}/actions/runs -X GET -f head_sha=<sha> -f per_page=100`

Used to discover failed workflow runs and rerunnable run IDs.

### Failed log inspection (GitHub Actions)

- `gh run view <run-id> --json jobs,name,workflowName,conclusion,status,url,headSha`
- `gh run view <run-id> --log-failed`

Used to classify branch-related vs flaky/unrelated failures for GitHub Actions workflows.

### External check run details (Vercel, Netlify, etc.)

- `gh api repos/{owner}/{repo}/commits/{sha}/check-runs`

Used to fetch `output` (title, summary, text) for failed checks not backed by GitHub Actions.
The watcher surfaces these as `failed_external_checks` in the snapshot, including `output_title`,
`output_summary`, `details_url`, and `link`.

### Retry failed jobs only

- `gh run rerun <run-id> --failed`

Reruns only failed jobs (and dependencies) for a workflow run.
Does not apply to external checks (Vercel, etc.) — those redeploy automatically on push.

## Review-related endpoints

- Issue comments on PR:
  - `gh api repos/{owner}/{repo}/issues/<pr_number>/comments?per_page=100`
- Inline PR review comments:
  - `gh api repos/{owner}/{repo}/pulls/<pr_number>/comments?per_page=100`
- Review submissions:
  - `gh api repos/{owner}/{repo}/pulls/<pr_number>/reviews?per_page=100`

**Pagination warning**: The GitHub REST API defaults to 30 results per page. When
fetching reviews for dismissal (outside the watcher script), always use `--paginate`
to ensure all reviews are retrieved. The watcher script handles this internally via
`gh_api_list_paginated()`, but manual `gh api` calls in the skill workflow must
include `--paginate` explicitly. Without it, PRs with >30 reviews (common with
active bot reviewers) will silently miss `CHANGES_REQUESTED`
reviews beyond the first page.

## JSON fields consumed by the watcher

### `gh pr view`

- `number`
- `url`
- `state`
- `mergedAt`
- `closedAt`
- `headRefName`
- `headRefOid`

### `gh pr checks`

- `bucket` (`pass`, `fail`, `pending`, `skipping`)
- `state`
- `name`
- `workflow`
- `link`

### Actions runs API (`workflow_runs[]`)

- `id`
- `name`
- `status`
- `conclusion`
- `html_url`
- `head_sha`

### Check Runs API (`failed_external_checks[]`)

- `name`
- `conclusion`
- `details_url`
- `html_url`
- `link`
- `output_title`
- `output_summary`
