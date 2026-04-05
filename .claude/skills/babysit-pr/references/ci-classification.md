# CI Failure Classification

## GitHub Actions failures
For failures backed by GitHub Actions workflows (present in `failed_runs`):

- `gh run view <run-id> --json jobs,name,workflowName,conclusion,status,url,headSha`
- `gh run view <run-id> --log-failed`

## External check failures (Vercel, Netlify, etc.)
For failures from external services (present in `failed_external_checks`), the watcher provides:

- `output_title` and `output_summary`: contain the build error details from the check run output
- `details_url` / `link`: direct link to the deployment page for full logs

Use the `output_summary` to diagnose the failure. If the summary is insufficient, use the **Vercel CLI** to get full build logs.

### Getting detailed Vercel deployment logs

1. **Find the deployment URL from the Vercel bot comment** on the PR:
   ```bash
   gh api repos/{owner}/{repo}/issues/{pr_number}/comments --jq '.[] | select(.user.login == "vercel[bot]") | .body' | head -100
   ```
   The bot comment contains a table with deployment info. Look for:
   - The **Inspect** link (e.g., `https://vercel.com/runner-ai/web/<deployment-id>`) — extract the deployment URL or ID
   - The **Preview** link (e.g., `https://web-<hash>-runner-ai.vercel.app`) — this is the deployment URL

2. **Fetch build logs using Vercel CLI**:
   ```bash
   # Using the preview/deployment URL from the bot comment
   bunx vercel inspect <deployment-url> --scope runner-ai 2>&1
   bunx vercel logs <deployment-url> --scope runner-ai 2>&1
   ```
   - `vercel inspect` shows deployment metadata, build status, and error summary
   - `vercel logs` shows the full build output including compilation errors, type errors, and lint failures

3. **Alternative: use the details_url from the watcher** — the `details_url` field in `failed_external_checks` often points directly to the Vercel deployment page, which may contain a deployment URL you can use with the CLI.

4. **Fallback: GitHub Check Runs API** (less detailed):
   ```bash
   gh api repos/{owner}/{repo}/commits/{sha}/check-runs --jq '.check_runs[] | select(.conclusion == "failure") | {name, output}'
   ```

External checks cannot be retried via `gh run rerun`. Instead, fix the underlying issue, commit, and push — the external service will redeploy automatically on the new SHA.

## Classification guidelines
Prefer treating failures as branch-related when logs point to changed code (compile/test/lint/typecheck/snapshots/static analysis in touched areas).

Prefer treating failures as flaky/unrelated when logs show transient infra/external issues (timeouts, runner provisioning failures, registry/network outages, GitHub Actions infra errors).

If classification is ambiguous, perform one manual diagnosis attempt before choosing rerun.

Read `references/heuristics.md` for the complete decision tree and checklist.
