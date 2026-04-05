# Task 006: Shared Base Layer Refactor — Verification Rubric

**Type:** test (Red)
**depends-on:** (none — modifies existing files independently)
**Target to verify:** `references/content-philosophy.md`, `references/gotchas.md`, `references/module-brief-template.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/architecture.md` → "Changes to shared base files"

## BDD Scenarios

```gherkin
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

Related content-rule scenarios (covered indirectly — the base layer must *allow* these rules to be expressed by flavor playbooks):

```gherkin
Scenario: Onboarding course does not test syntax recall (base layer must allow this override)
Scenario: Architecture Review course contains no restaurant metaphors (base layer must allow this override)
Scenario: Vibe Coder course tooltips every technical term (base layer must still express this as the default when no override applies)
```

## Acceptance Criteria (Checklist)

### `references/content-philosophy.md` changes

- [ ] A header banner has been added near the top of the file (after the `> **When to read this:**` block) stating: *"This is the shared base layer. Flavor playbooks under `references/flavors/` may override or tighten any rule marked `[overridable]` below. The unchanged rules are universal across all flavors."*
- [ ] The following rules are marked `[overridable]` (inline tag next to the heading or rule):
  - [ ] "Max 2-3 sentences per text block" (under "Show, Don't Tell — Aggressively Visual")
  - [ ] "Every screen must be at least 50% visual"
  - [ ] "Every code snippet gets a side-by-side plain English translation" (under "Code ↔ English Translations")
  - [ ] "Be extremely aggressive with tooltips" (under "Glossary Tooltips — No Term Left Behind")
  - [ ] "Metaphors first, then reality"
- [ ] The following rules are explicitly marked universal / non-overridable (with a `[universal]` tag or equivalent):
  - [ ] "No recycled metaphors"
  - [ ] "No horizontal scrollbars on code"
  - [ ] "Use original code exactly as-is"
  - [ ] "One concept per screen"
  - [ ] "Quizzes test application, not memory"
  - [ ] "Glossary tooltips never clip" (technical rule)
- [ ] No content rules are deleted — the file remains functional as the vibe-coder base layer.

### `references/gotchas.md` changes

- [ ] The "Not Enough Tooltips" gotcha has a new *Flavor note:* rider paragraph describing per-flavor aggressiveness:
  - Vibe Coder and Onboarding: under-tooltipping is critical failure
  - Pattern Learning: missing pattern names is the failure mode
  - Architecture Review: err **light**, not heavy
  - Deep Understanding: err generous
- [ ] The "Walls of Text" gotcha has a new *Flavor note:* rider paragraph describing per-flavor density:
  - The 50%-visual rule is strict for Vibe Coder and Onboarding
  - Pattern Learning and Architecture Review may run denser prose
  - The gotcha becomes "walls of text with no visual anchors at all" for those flavors
- [ ] No existing gotchas are deleted.

### `references/module-brief-template.md` changes

- [ ] A new mandatory field `**Flavor:** <vibe-coder | onboarding | pattern-learning | architecture-review | deep-understanding>` has been added at the top of the template (before or as part of the "Teaching Arc" block).
- [ ] A note has been added that the "Why should I care?" field content is dictated by the flavor playbook.
- [ ] A note has been added that the writing agent must read `references/flavors/<flavor>.md` in addition to the existing reference files.
- [ ] The existing fields remain unchanged.

### Cross-file consistency

- [ ] All three files continue to parse as valid Markdown.
- [ ] The `[overridable]` tag used in content-philosophy.md is consistent (same token across all uses).
- [ ] The references to `references/flavors/` use correct relative paths.

## How to Run Verification

1. Open `references/content-philosophy.md`. Confirm the header banner exists.
2. Grep for `[overridable]` — at least 5 occurrences (one per overridable rule).
3. Grep for `[universal]` or equivalent — at least 6 occurrences (or the rules are listed together under a "Universal rules" heading).
4. Open `references/gotchas.md`. Grep for `Flavor note:` — must appear twice (under "Not Enough Tooltips" and "Walls of Text").
5. Open `references/module-brief-template.md`. Grep for `Flavor:` — must appear at least once in the template (not just prose).
6. Confirm none of the original rule/section headings have been deleted from any of the three files.

## Initial State (Red)

- `content-philosophy.md` has no header banner and no `[overridable]` tags.
- `gotchas.md` has no *Flavor note:* riders.
- `module-brief-template.md` has no `Flavor:` field.
