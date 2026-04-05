# Task 009: End-to-End Flavor Flow Verification

**Type:** verify (standalone, no impl pair)
**depends-on:** task-001-vibe-coder-playbook-impl, task-002-onboarding-playbook-impl, task-003-pattern-learning-playbook-impl, task-004-architecture-review-playbook-impl, task-005-deep-understanding-playbook-impl, task-006-base-layer-refactor-impl, task-007-skill-md-updates-impl
**Target to verify:** full skill execution flow for each of the 5 flavors

## BDD Scenarios

```gherkin
Scenario: Every flavor includes the mandatory interactive elements
  Given any flavor is selected
  When the skill finishes building the course
  Then the output contains at least one Group Chat Animation across modules
    And the output contains at least one Data Flow Animation across modules
    And every module contains at least one code block (in the flavor-specific style)
    And every module contains at least one quiz
    And every module uses glossary tooltips (scope varies per flavor)

Scenario: Interactive-element HTML patterns are unchanged across flavors
  Given any flavor is selected
  When the writing agent produces a quiz HTML block
  Then the HTML follows the patterns in references/interactive-elements.md exactly
    And the CSS class names match those in styles.css
    And the main.js engines pick up the elements via the documented data-* attributes

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

This is an integration-level check. Rather than running the skill on a live codebase (which would require executing Claude Code end-to-end), this task walks through the skill's instructions **mentally or on paper** and verifies that each flavor's pipeline is internally consistent.

### Walkthrough per flavor

For each of the 5 flavors, trace the full pipeline from a hypothetical trigger phrase to a hypothetical completed course. The following must be true for each:

- [ ] **Phase 0** — the flavor is selectable via the AskUserQuestion with the correct label and description.
- [ ] **Phase 0 → playbook load** — SKILL.md's Phase 0 instructs the skill to read `references/flavors/<this-flavor>.md`. Confirm the file exists (created by tasks 001-005).
- [ ] **Phase 1** — codebase analysis instructions are identical across all flavors. No flavor-specific branching in Phase 1.
- [ ] **Phase 2** — the module arc chosen matches the playbook's Section 4. Walk each module title and confirm it exists in the playbook.
- [ ] **Phase 2.5** (if complex codebase) — the module brief template includes the `Flavor:` field (task 006 impl). Each brief would specify the current flavor.
- [ ] **Phase 3** — the writing agent's required reading includes the playbook. For sequential path, confirm SKILL.md Phase 3 instructions include `references/flavors/<flavor>.md`. For parallel path, confirm the dispatch list includes it.
- [ ] **Phase 4** — review and open is identical across flavors (no change needed).

### Mandatory interactive elements across all flavors

For each flavor's playbook, confirm that it does NOT remove or make optional any of the 5 mandatory element types:

- [ ] Group Chat Animation — mentioned as required (or inherited from shared rules in SKILL.md / content-philosophy.md).
- [ ] Message Flow / Data Flow Animation — mentioned as required.
- [ ] Code block (of the flavor-specific style) — every module must have one.
- [ ] Quiz — every module must have at least one.
- [ ] Glossary tooltips — mentioned (scope varies per flavor, but never absent).

### HTML patterns unchanged

- [ ] `references/interactive-elements.md` has not been modified (task 008 covers this byte-check; this task confirms the content-level implication: every playbook instructs writing agents to use the patterns in interactive-elements.md verbatim).
- [ ] No flavor playbook redefines CSS class names, data-attribute names, or JS function names for interactive elements.

### Context isolation

- [ ] Phase 3 parallel path instructions in SKILL.md explicitly state that each agent receives **only its flavor's playbook**, not all five.
- [ ] Phase 3 instructions still exclude SKILL.md and other flavors' playbooks from the agent's context.

### Flavor-specific "must-have element" enforcement

For each engineer flavor, confirm the must-have element is present in the playbook AND documented as required:

- [ ] **Onboarding**: the "simulated first PR" final module is marked as prescriptive (not optional). See task 002 checklist.
- [ ] **Pattern Learning**: every pattern module has a mandatory Transfer callout. See task 003 checklist.
- [ ] **Architecture Review**: every decision module has a mandatory Verdict line. See task 004 checklist.
- [ ] **Deep Understanding**: the progressive-depth reveal structure is mandatory. See task 005 checklist.
- [ ] **Vibe Coder**: aggressive tooltipping on every term is mandatory. See task 001 checklist.

### Mapping consistency

- [ ] The flavor labels in Phase 0 (SKILL.md) match the filenames under `references/flavors/` exactly:
  - "Vibe Coder" → `vibe-coder.md`
  - "Onboarding" → `onboarding.md`
  - "Pattern Learning" → `pattern-learning.md`
  - "Architecture Review" → `architecture-review.md`
  - "Deep Understanding" → `deep-understanding.md`
- [ ] The "Who This Is For" table in SKILL.md matches the same mapping.

### Base-layer overrides wire up correctly

- [ ] Each engineer flavor's Section 12 (Overrides) references only rules that exist in `content-philosophy.md` with the `[overridable]` tag.
- [ ] No flavor tries to override a rule marked `[universal]`.
- [ ] The "no recycled metaphors" universal rule is honored by all flavors (including Architecture Review, which trivially satisfies it by forbidding metaphors entirely).

## How to Run Verification

This task is performed by reading the files in this order and cross-checking against the checklist:

1. Read `SKILL.md` (current, post-task-007 state).
2. Read all 5 playbooks under `references/flavors/`.
3. Read `references/content-philosophy.md` (post-task-006 state).
4. Read `references/module-brief-template.md` (post-task-006 state).

For each flavor, simulate a full skill run mentally:
- The user says a trigger phrase.
- The skill shows the welcome, then asks the flavor question.
- The user picks this flavor.
- The skill reads the playbook.
- The skill analyzes the codebase (pretend).
- The skill designs a curriculum using the playbook's module arc.
- The skill writes modules according to the playbook's content rules.
- The skill runs build.sh.
- The skill opens the course.

At each step, confirm SKILL.md and the playbook agree on what happens next.

## Pass / Fail

Pass: every check succeeds for every flavor. Fail: any internal inconsistency (a missing file, a mismatch between a playbook and SKILL.md, an undocumented override, a missing must-have element) — the regression is traced back to its source task and corrected.

## No implementation task

This is the integration-level check that the full design has landed correctly. It has no paired impl task. Any failures are corrected in the relevant earlier task's impl.
