# Task 007: SKILL.md Phase 0 + Delegation Refactor — Verification Rubric

**Type:** test (Red)
**depends-on:** (none — modifies SKILL.md independently)
**Target to verify:** `SKILL.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/architecture.md` → "SKILL.md changes"

## BDD Scenarios

```gherkin
Scenario: User invokes the skill with no flavor hint
  Given the user has not yet picked a flavor in this session
    And the user says "turn this codebase into a course"
  When the skill activates
  Then the skill shows the First-Run Welcome message
    And the skill calls AskUserQuestion with exactly 5 options:
      1. Vibe Coder
      2. Onboarding
      3. Pattern Learning
      4. Architecture Review
      5. Deep Understanding
    And the skill does NOT begin codebase analysis until the user picks

Scenario: User picks Vibe Coder
  (full scenario — see bdd-specs.md)

Scenario: User picks Onboarding
  (full scenario — see bdd-specs.md)

Scenario: User picks Pattern Learning
  (full scenario — see bdd-specs.md)

Scenario: User picks Architecture Review
  (full scenario — see bdd-specs.md)

Scenario: User picks Deep Understanding
  (full scenario — see bdd-specs.md)

Scenario: User picks "Other" and provides custom intent
  Given the flavor question has been asked
  When the user picks "Other" and describes a goal in free text
  Then the skill maps the goal to the closest flavor based on keywords
    And if mapping is ambiguous, the skill falls back to Deep Understanding and announces the fallback
    And the user's free-text goal is incorporated into the "why should I care?" framing of every module

Scenario: Flavor playbook is loaded at the right moment
  Given the skill is running Phase 0
  When the user picks a flavor
  Then the skill reads the matching references/flavors/<flavor>.md file
    And does NOT read any other flavor's playbook
    And SKILL.md remains the only always-loaded orchestration file

Scenario: Parallel writing agents receive their flavor playbook
  Given the flavor is any engineer flavor AND the codebase is complex AND Phase 2.5 briefs exist
  When Phase 3 parallel path dispatches writing agents
  Then each agent receives:
    - Its module brief (from course-name/briefs/)
    - references/content-philosophy.md
    - references/gotchas.md
    - references/flavors/<flavor>.md
    - Only the needed sections of interactive-elements.md and design-system.md
  And no agent receives playbooks for other flavors
  And no agent receives SKILL.md
```

## Acceptance Criteria (Checklist)

### Phase 0 insertion

- [ ] A new "## Phase 0: Flavor Selection" section exists in SKILL.md.
- [ ] Phase 0 is positioned **between** the existing "First-Run Welcome" section and the current "Who This Is For" section (approximately lines 23-24 of the current file).
- [ ] Phase 0 describes calling `AskUserQuestion` with exactly 5 options, each with a 1-line description.
- [ ] The 5 options are: Vibe Coder, Onboarding, Pattern Learning, Architecture Review, Deep Understanding (in that order).
- [ ] Phase 0 instructs the skill to **read the matching `references/flavors/<flavor>.md` file** after the user picks, before any codebase analysis.
- [ ] Phase 0 handles the "Other" fallback: map free-text goal to the closest flavor by keyword, fall back to Deep Understanding if ambiguous, announce the fallback.
- [ ] Phase 0 explicitly states: "the skill does NOT begin codebase analysis until the user has picked a flavor."

### "Who This Is For" replacement

- [ ] The current "## Who This Is For" paragraph (vibe-coder-only description, lines 25-39) has been **replaced** with a 5-row table (or equivalent structured form) listing each flavor with a one-line learner description and a link to the matching playbook under `references/flavors/`.
- [ ] No content rules (show don't tell, metaphors, tooltips, etc.) remain inline in this section — they have been delegated to the playbooks.

### "Why This Approach Works" replacement

- [ ] The current "## Why This Approach Works" paragraph (lines 41-49) has been reduced to a one-liner pointing readers to the selected flavor's Section 2 for the specific framing.

### Phase 2 delegation

- [ ] The current Phase 2 "Curriculum Design" section's **module arc table** (lines 75-83, the 7-row vibe-coder-specific menu) has been **removed from SKILL.md** and Phase 2 now instructs the skill to read the "Module Arc" section of the selected flavor playbook.
- [ ] Phase 2 retains the shared principle: "every module should connect back to the flavor's core learner goal."
- [ ] Phase 2 retains the shared "Mandatory interactive elements" list (Group Chat, Data Flow, Code block [per-flavor style], Quizzes, Glossary Tooltips) but notes that the code block *content style* is dictated by the playbook.

### Phase 2.5 flavor field

- [ ] Phase 2.5's module brief instructions mention that the brief template now includes a mandatory `Flavor:` field (which task 006 adds to the template).

### Phase 3 playbook loading

- [ ] The **Sequential path** reading list in Phase 3 adds `references/flavors/<your-flavor>.md` alongside `content-philosophy.md` and `gotchas.md`.
- [ ] The **Parallel path** brief dispatch instructions state that each writing agent receives `references/flavors/<flavor>.md` alongside existing references.
- [ ] The "what agents do NOT receive" list in Phase 3 still excludes SKILL.md and explicitly excludes playbooks for OTHER flavors.

### First-Run Welcome preserved

- [ ] The current "## First-Run Welcome" section (lines 10-22) remains intact — its text is unchanged. (Phase 0 sits after the welcome.)

### Trigger phrases preserved

- [ ] The current trigger phrase list in the frontmatter `description:` field still contains all existing phrases: "turn this into a course", "explain this codebase interactively", "teach this code", "interactive tutorial from code", "codebase walkthrough", "learn from this codebase", "make a course from this project".
- [ ] No trigger phrases are removed.

### Metadata

- [ ] The YAML frontmatter `description` field may be slightly updated to acknowledge the multi-audience capability, but must remain under the 1000-character practical limit and must preserve all existing trigger phrases.

### File size sanity

- [ ] SKILL.md is not dramatically longer after the refactor. The module arc table, Who This Is For section, and Why This Approach Works section are now shorter because they delegate to playbooks. SKILL.md should remain in the same ballpark as the current size (the file is ~220 lines today).

## How to Run Verification

1. Open `SKILL.md`. Confirm Phase 0 exists between First-Run Welcome and Who This Is For.
2. Grep for `## Phase 0` — must appear exactly once.
3. Grep for `AskUserQuestion` — must appear in Phase 0.
4. Grep for the 5 flavor names: `Vibe Coder`, `Onboarding`, `Pattern Learning`, `Architecture Review`, `Deep Understanding` — all five must appear.
5. Grep for `references/flavors/` — must appear in Phase 0, Who This Is For, and Phase 3.
6. Confirm the old module arc table (rows for "Meet the actors", "How the pieces talk", etc.) is no longer in SKILL.md.
7. Confirm the trigger phrases in the frontmatter `description:` are unchanged.
8. Line count sanity check (`wc -l SKILL.md`) — should not exceed ~280 lines.

## Initial State (Red)

- SKILL.md has no Phase 0 section.
- "Who This Is For" is still the vibe-coder-only paragraph.
- The module arc table is still in Phase 2.
- No references to `references/flavors/` exist in SKILL.md.
