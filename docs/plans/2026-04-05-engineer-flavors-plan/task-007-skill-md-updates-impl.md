# Task 007: SKILL.md Phase 0 + Delegation Refactor — Implementation

**Type:** impl (Green)
**depends-on:** task-007-skill-md-updates-test
**Target to modify:** `SKILL.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/architecture.md` → "SKILL.md changes"

## BDD Scenarios Covered

Every scenario from "Feature: Flavor selection on first run" in `bdd-specs.md`, plus "Flavor playbook is loaded at the right moment" and "Parallel writing agents receive their flavor playbook". See `task-007-skill-md-updates-test.md` for the full Gherkin text — the rubric there is the source of truth for acceptance.

## What to Implement

This task modifies SKILL.md in four logical sub-edits. All four must happen in a single commit. Keep SKILL.md's existing voice and progressive-disclosure structure intact.

### Sub-edit 1: Insert Phase 0 section

**Location:** Between the current "First-Run Welcome" section (ends around line 22) and the current "Who This Is For" section (begins around line 25).

**Content:** A new `## Phase 0: Flavor Selection` section that:

1. States that flavor selection is **mandatory on first run before any codebase analysis**.
2. Describes calling `AskUserQuestion` with exactly 5 options, in this order:
   - **Vibe Coder** — "I'm learning without a CS background; I want to steer AI coding tools and understand code I didn't write myself."
   - **Onboarding** — "I'm an engineer joining this codebase; I want to ship my first PR without breaking things."
   - **Pattern Learning** — "I want to study this codebase and extract reusable techniques for my own work."
   - **Architecture Review** — "I'm evaluating this codebase's architecture and want to form an opinion about its tradeoffs."
   - **Deep Understanding** — "I want a thorough tour of how this system works, no specific use case."
3. After the user picks, the skill reads `references/flavors/<flavor>.md` and holds it in context for the rest of the session. From that point, every audience-dependent decision defers to the playbook.
4. Handles the "Other" fallback: if the user provides free-text intent, map it to the closest flavor via keyword matching (e.g., "contributing" / "new to" → Onboarding; "evaluate" / "review" / "tradeoff" → Architecture Review; "how does it work" / "internals" → Deep Understanding; "clever" / "patterns" / "techniques" → Pattern Learning). If ambiguous, fall back to Deep Understanding and announce the fallback. The free-text goal is preserved and woven into the "why should I care?" framing of every module.
5. Explicitly states: "Do NOT begin codebase analysis until the user has picked a flavor."

### Sub-edit 2: Replace "Who This Is For"

**Location:** Current lines 25-39 (the paragraph describing vibe-coder audience).

**New content:** A short intro sentence followed by a 5-row table:

```markdown
## Who This Is For

This skill generates courses for five audiences. The user picked one in Phase 0; the matching playbook at `references/flavors/<flavor>.md` owns all audience-dependent content rules.

| Flavor | Learner | Playbook |
|---|---|---|
| Vibe Coder | Non-technical; uses AI coding tools | `references/flavors/vibe-coder.md` |
| Onboarding | Engineer new to this stack | `references/flavors/onboarding.md` |
| Pattern Learning | Engineer studying an OSS project | `references/flavors/pattern-learning.md` |
| Architecture Review | Senior engineer evaluating tradeoffs | `references/flavors/architecture-review.md` |
| Deep Understanding | Engineer wanting thorough comprehension | `references/flavors/deep-understanding.md` |
```

All content rules (show don't tell, metaphors, tooltips, etc.) that currently live inline in this section are **removed from SKILL.md** and live in the playbooks / content-philosophy base layer.

### Sub-edit 3: Reduce "Why This Approach Works"

**Location:** Current lines 41-49.

**New content:** Replace the paragraph with a one-liner:

> Every flavor inverts traditional learning by meeting the learner where they already are. See your flavor's playbook (Section 2) for the specific framing.

Remove the vibe-coder-specific "build first, understand later" elaboration from SKILL.md — it now lives in `vibe-coder.md`.

### Sub-edit 4: Delegate Phase 2 curriculum design

**Location:** Current Phase 2 section (lines 69-87).

**Remove:** The entire 7-row module arc table (current lines 75-83) and the per-row purpose explanations. This table is vibe-coder-specific and is moved into `vibe-coder.md`.

**Keep:**
- The "Structure the course as 4-6 modules" guidance (shared).
- The "fewer, better modules beat more, thinner ones" principle (shared).
- The "zoom-in" arc principle at a high level (shared).
- The "mandatory interactive elements" list (shared): Group Chat, Data Flow, Code block (**per-flavor style — see your playbook**), Quizzes, Glossary Tooltips.
- The "do not present the curriculum for approval — just build it" rule (shared).
- The simple-vs-complex codebase branching for sequential vs parallel build paths (shared).

**Add:** An explicit instruction at the top of Phase 2: *"Read `references/flavors/<your-flavor>.md` → 'Module Arc' section. Each flavor provides its own curated module menu. Pick the modules that best fit the codebase."*

### Sub-edit 5: Phase 2.5 and Phase 3 playbook loading

1. **Phase 2.5 instructions** — add a sentence: *"Each brief includes a `Flavor:` field at the top (see `references/module-brief-template.md`). Writing agents use this to know which playbook to read."*

2. **Phase 3 Sequential path reading list** — add `references/flavors/<your-flavor>.md` to the list of files the agent reads before writing modules. Place it before `content-philosophy.md` and `gotchas.md`.

3. **Phase 3 Parallel path dispatch** — add `references/flavors/<flavor>.md` to the list of files each parallel writing agent receives. Update the "What agents do NOT receive" list to mention that agents do not receive playbooks for other flavors.

### Sub-edit 6: Frontmatter description field (optional)

The YAML `description:` field at the top of SKILL.md may be slightly updated to acknowledge multi-audience support. If updated:

- Preserve all existing trigger phrases verbatim.
- Add phrases that signal the new flavors (e.g., "onboard to a codebase", "architectural review of a codebase", "learn patterns from this project"). But **do not remove or reword** any existing phrases.
- Stay under the practical length limit.

If this sub-edit is risky (e.g., the description field is hitting a length limit), skip it. The Phase 0 AskUserQuestion is the authoritative way to select a flavor; trigger phrases do not need to auto-detect.

## Unchanged elements (do not touch)

- The "First-Run Welcome" section (current lines 10-22) — intact.
- The "The Process" header (current line ~51).
- Phase 1: Codebase Analysis (current lines 55-67) — intact.
- The "Design Identity" section (current lines 199-210) — intact.
- The "Reference Files" section (current lines 213-222) — intact, except it may gain a bullet for `references/flavors/` describing the new directory.
- All trigger phrases in the frontmatter `description` field.

## Verification (Green)

Run the checklist from `task-007-skill-md-updates-test.md`. Every item should pass.

## Commit Boundary

Single commit, suggested message:

```
feat: add Phase 0 flavor selection to SKILL.md

Replaces the vibe-coder-only audience framing with a mandatory
first-run flavor picker across 5 options. Delegates audience-
dependent rules (module arc, content philosophy overrides) to
per-flavor playbooks under references/flavors/. Preserves all
existing trigger phrases and the First-Run Welcome block.

Completes the engineer-flavors design:
docs/plans/2026-04-05-engineer-flavors-design/
```
