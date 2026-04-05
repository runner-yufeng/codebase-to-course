# Task 001: Vibe Coder Playbook — Implementation

**Type:** impl (Green)
**depends-on:** task-001-vibe-coder-playbook-test
**Target to create:** `references/flavors/vibe-coder.md`
**Sources (read-only):** current `SKILL.md`, `references/content-philosophy.md`, `references/gotchas.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 1: Vibe Coder (preserved)"; `docs/plans/2026-04-05-engineer-flavors-design/architecture.md` → "Playbook structure (shared template)"

## BDD Scenarios Covered

```gherkin
Scenario: User picks Vibe Coder
  Given the flavor question has been asked
  When the user picks "Vibe Coder"
  Then the skill reads references/flavors/vibe-coder.md
    And all subsequent content follows the vibe-coder playbook
    And the produced course is byte-indistinguishable in structure from the pre-flavor skill output
    And the output contains line-by-line "Code ↔ Plain English" translations
    And every technical term receives a glossary tooltip on first use per module

Scenario: Vibe Coder flavor preserves current experience
  Given a user who previously used the skill picks Vibe Coder
  When the skill produces the course
  Then the learner sees the same type of content they saw before the flavor system landed:
    - Line-by-line Code ↔ English translations
    - Aggressive glossary tooltips on every term
    - Warm "smart friend" voice
    - Infographic-style visual density
    - "Why should I care = steer AI better" framing

Scenario: Vibe Coder course tooltips every technical term
  Given the flavor is Vibe Coder
  When the skill writes module HTML
  Then every technical term has a glossary tooltip on first use per module
    And acronyms always have tooltips on first use
    And the aggressiveness matches the current pre-flavor skill output
```

## What to Implement

1. **Create the directory** `references/flavors/` if it does not already exist.

2. **Create the file** `references/flavors/vibe-coder.md` following the 12-section playbook template from `architecture.md` ("Playbook structure (shared template)").

3. **Populate each section** by extracting content from the current `SKILL.md` and `references/content-philosophy.md`. This task is primarily an extraction, not new writing — the goal is preservation:

   | Playbook section | Source to extract from |
   |---|---|
   | 1. Audience snapshot | `SKILL.md` lines 25-39 ("Who This Is For") |
   | 2. Why this approach works | `SKILL.md` lines 41-49 ("Why This Approach Works") |
   | 3. The learner's core question | Derive from SKILL.md's framing: "How does this thing I vibe-coded actually work under the hood?" |
   | 4. Module arc (menu) | `SKILL.md` lines 69-87 (Phase 2 curriculum design section, including the 7-module table and the "menu not a checklist" note) |
   | 5. Code block style | `content-philosophy.md` lines 28-33 ("Code ↔ English Translations") |
   | 6. Quiz style | `content-philosophy.md` lines 65-89 ("Quizzes That Test Application, Not Memory") |
   | 7. Metaphor strategy | `content-philosophy.md` lines 38-41 ("Metaphors First, Then Reality") |
   | 8. Tooltip strategy | `content-philosophy.md` lines 49-63 ("Glossary Tooltips — No Term Left Behind") and `gotchas.md` "Not Enough Tooltips" |
   | 9. Voice & tone | Derive from SKILL.md line 29 ("like a smart friend explaining things, not a professor lecturing") |
   | 10. Visual density target | `content-philosophy.md` lines 7-27 ("Show, Don't Tell — Aggressively Visual") |
   | 11. "Why should I care?" framing | `SKILL.md` lines 31-37 (the practical goals list: steer AI, detect bugs, intervene, vocabulary) |
   | 12. Overrides to content-philosophy.md | Short note: "No overrides — vibe coder is the baseline audience the base layer was originally written for." |

4. **Preserve intent, not verbatim copies.** Where content-philosophy.md uses second-person imperative voice for the agent ("Be extremely aggressive with tooltips"), reframe it in the playbook as a rule in third person ("Tooltips on every technical term, first use per module"). The playbook is a spec for the writing agent; the base file is a set of shared principles.

5. **Do not duplicate universal rules.** The playbook should only restate rules that are vibe-coder-specific. Rules that remain shared (no recycled metaphors, original code only, no horizontal scrollbars) stay in `content-philosophy.md` as the base layer. The vibe-coder playbook mentions them by reference, not by repeating them.

## Verification (Green)

Run the checklist from `task-001-vibe-coder-playbook-test.md`. Every check should pass:
1. File and directory exist.
2. All 12 sections are present with correct headings.
3. Content preservation checks pass — the extracted rules match the source in meaning.
4. No broken cross-references.

## Commit Boundary

Single commit, suggested message:

```
feat: extract vibe-coder behavior into flavor playbook

First of five flavor playbooks. Preserves current skill behavior
verbatim under references/flavors/vibe-coder.md in preparation for
the Phase 0 flavor selection system.

Part of the engineer-flavors design:
docs/plans/2026-04-05-engineer-flavors-design/
```
