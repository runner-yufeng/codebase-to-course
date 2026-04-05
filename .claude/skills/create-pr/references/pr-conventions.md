# PR Conventions

## Title Format

Use [Conventional Commits](https://www.conventionalcommits.org/) style:

- `feat: {description}` — new feature
- `fix: {description}` — bug fix
- `refactor: {description}` — refactoring without behavior change
- `docs: {description}` — documentation only
- `test: {description}` — test changes only
- `chore: {description}` — tooling, deps, config
- `perf: {description}` — performance improvement
- `ci: {description}` — CI/CD changes

## Body Template

```markdown
## Summary
<1-3 bullet points describing the changes>

## Test plan
<bulleted checklist of testing steps>
```

## Constraints

- Title must be under 70 characters
- Base branch: always `--base main`
- Context: use `git log main..HEAD` and `git diff main...HEAD`
- Push with `-u` flag if the branch has no upstream
