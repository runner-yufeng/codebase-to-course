# Task 001: Vibe Coder Playbook — Verification Rubric

**Type:** test (Red)
**depends-on:** (none — foundation task)
**Target to verify:** `references/flavors/vibe-coder.md` (to be created by task 001-impl)
**Source truth:** current `SKILL.md` + `references/content-philosophy.md` + `references/gotchas.md`

## BDD Scenarios

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

## Acceptance Criteria (Checklist)

The `-impl` task is Green when every item below is satisfied. Initially (Red) every item fails because the file does not exist.

### File existence and location
- [ ] `references/flavors/` directory exists.
- [ ] `references/flavors/vibe-coder.md` file exists.
- [ ] The file is valid Markdown (no broken headers, no stray tags).

### Structural compliance (per architecture.md "Playbook structure")
- [ ] Section 1: "Audience snapshot" exists.
- [ ] Section 2: "Why this approach works (for this audience)" exists.
- [ ] Section 3: "The learner's core question" exists.
- [ ] Section 4: "Module arc (menu)" exists and contains 4-7 module entries.
- [ ] Section 5: "Code block style" exists and specifies Code ↔ Plain English line-by-line translations.
- [ ] Section 6: "Quiz style" exists and specifies "where would you look" / "where would you add" scenario quizzes.
- [ ] Section 7: "Metaphor strategy" exists and states "heavy — everyday life metaphors" with the no-recycled-restaurant rule.
- [ ] Section 8: "Tooltip strategy" exists and states "ultra-aggressive — every term on first use per module".
- [ ] Section 9: "Voice & tone" exists and describes the "smart friend" persona.
- [ ] Section 10: "Visual density target" exists and specifies "infographic (50%+ visual, 2-3 sentence cap)".
- [ ] Section 11: "Why should I care? framing per module" exists and references "steer AI / debug / make smarter decisions".
- [ ] Section 12: "Overrides to content-philosophy.md" exists (for vibe coder, this should be empty or "no overrides — this is the baseline audience").

### Content preservation (no behavioral regression)
- [ ] The audience snapshot matches the current SKILL.md "Who This Is For" section (lines 25-39) in meaning — a non-technical user of AI coding tools whose goals are steering AI, detecting hallucinations, debugging, acquiring vocabulary, and building production-quality software without becoming a software engineer.
- [ ] The "why this approach works" text captures the "build first, understand later" inversion and the "meet the learner where they already are" framing from SKILL.md lines 41-49.
- [ ] The module arc is the current 7-module menu from SKILL.md lines 75-83 (what the app does → actors → communication → outside world → clever tricks → when things break → big picture).
- [ ] The module arc includes the note "This is a menu, not a checklist" and the guidance to adapt to codebase complexity.
- [ ] The tooltip strategy matches the "Be extremely aggressive with tooltips" rule from content-philosophy.md lines 52-59 (software names, developer terms, programming concepts, infrastructure terms, acronyms).
- [ ] The code block style is the current "Code ↔ Plain English Translations" rule from content-philosophy.md lines 28-33.

### Cross-reference integrity
- [ ] No broken links.
- [ ] References to `references/interactive-elements.md`, `references/design-system.md`, etc. use correct relative paths (relative to the skill root, e.g., `references/interactive-elements.md` not `../interactive-elements.md`).

## How to Run Verification

1. `ls references/flavors/vibe-coder.md` → exits 0.
2. For each Section N check, grep the file for the expected heading (e.g., `## 1. Audience snapshot`).
3. For content preservation checks, open the file and read the relevant section; compare semantically to the cited lines of the pre-refactor SKILL.md / content-philosophy.md (the source files at HEAD before this task's commit).
4. For cross-reference checks, grep for any `](./` or `](../` patterns and verify the paths resolve.

## Initial State (Red)

All checks fail because `references/flavors/vibe-coder.md` does not exist yet. The directory `references/flavors/` does not exist yet. This is the expected Red state.
