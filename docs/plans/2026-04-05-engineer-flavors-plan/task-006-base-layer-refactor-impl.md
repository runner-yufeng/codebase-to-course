# Task 006: Shared Base Layer Refactor — Implementation

**Type:** impl (Green)
**depends-on:** task-006-base-layer-refactor-test
**Targets to modify:**
- `references/content-philosophy.md`
- `references/gotchas.md`
- `references/module-brief-template.md`

**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/architecture.md` → "Changes to shared base files"

## BDD Scenarios Covered

```gherkin
Scenario: Flavor playbook is loaded at the right moment
  Given the skill is running Phase 0
  When the user picks a flavor
  Then the skill reads the matching references/flavors/<flavor>.md file
    And does NOT read any other flavor's playbook
    And SKILL.md remains the only always-loaded orchestration file

Scenario: Parallel writing agents receive their flavor playbook
  (as in the test task)
```

## What to Implement

### Change 1: `references/content-philosophy.md`

1. **Add a base-layer header banner** immediately after the existing `> **When to read this:**` blockquote (lines 1-3 of the current file). Insert a new blockquote:

   > **This is the shared base layer.** Flavor playbooks under `references/flavors/` may override or tighten any rule marked `[overridable]` below. The unchanged rules are universal across all flavors.

2. **Mark rules as `[overridable]` or `[universal]`.** Append the tag inline (after the heading or in the rule text) for each of the following. Use the exact token `[overridable]` / `[universal]` so grep-based verification works.

   Overridable:
   - "Max 2-3 sentences per text block" → append `[overridable]`
   - "Every screen must be at least 50% visual" → append `[overridable]`
   - "Every code snippet gets a side-by-side plain English translation" → append `[overridable]`
   - "Be extremely aggressive with tooltips" → append `[overridable]`
   - "Metaphors first, then reality" (the heading itself) → append `[overridable]`

   Universal:
   - "No recycled metaphors" → append `[universal]`
   - "No horizontal scrollbars on code" → append `[universal]`
   - "Use original code exactly as-is" → append `[universal]`
   - "One concept per screen" → append `[universal]`
   - "Quizzes That Test Application, Not Memory" (section heading) → append `[universal]`
   - Tooltip clipping rule ("Tooltip overflow fix:" paragraph) → append `[universal]`

3. **Do not delete any existing content.** The file should still fully describe the vibe-coder-default behavior when no override applies.

### Change 2: `references/gotchas.md`

1. **Under "Not Enough Tooltips"**, add a new paragraph after the existing rule-of-thumb paragraph:

   > *Flavor note:* Under-tooltipping is the #1 failure for Vibe Coder and Onboarding. For Pattern Learning, the failure mode shifts to missing *pattern names* (tooltip them with short definitions + see-alsos). For Architecture Review, err **light**, not heavy — tooltipping senior vocabulary feels condescending. For Deep Understanding, err generous — audience variance is high.

2. **Under "Walls of Text"**, add a new paragraph after the existing description:

   > *Flavor note:* The strict 50%-visual rule holds for Vibe Coder, Onboarding, and Deep Understanding. For Pattern Learning and Architecture Review, prose may run longer when the idea requires it — the real gotcha for those flavors becomes "walls of text with no visual anchors at all" rather than "any text block longer than 3 sentences."

3. **Do not delete any existing gotchas.**

### Change 3: `references/module-brief-template.md`

1. **Add a mandatory `Flavor:` field at the top of the template**, before the Teaching Arc section. Insert immediately after the `## Module N: [Title]` line:

   ```markdown
   **Flavor:** <vibe-coder | onboarding | pattern-learning | architecture-review | deep-understanding>
   ```

2. **Add a note to the Teaching Arc subsection** clarifying that the `Why should I care?` bullet's content is dictated by the selected flavor's playbook. A short sentence like: *"See `references/flavors/<flavor>.md` → Section 11 for the flavor-specific framing."*

3. **Add a new entry to the "Reference Files to Read" section** instructing the writing agent to always include `references/flavors/<flavor>.md` alongside the existing references.

4. **Do not delete any existing fields.**

## Verification (Green)

Run the checklist from `task-006-base-layer-refactor-test.md`. All checks pass.

## Commit Boundary

Single commit (touches three files but is conceptually one refactor), suggested message:

```
refactor: mark content-philosophy as shared base layer

Adds [overridable]/[universal] tags so flavor playbooks can express
per-audience overrides while preserving the current vibe-coder
defaults. Adds per-flavor notes to two gotchas (tooltips, density)
and a flavor field to the module brief template.

Part of the engineer-flavors design:
docs/plans/2026-04-05-engineer-flavors-design/
```
