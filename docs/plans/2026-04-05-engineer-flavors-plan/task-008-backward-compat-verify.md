# Task 008: Backward-Compatibility Verification

**Type:** verify (standalone, no impl pair)
**depends-on:** task-007-skill-md-updates-impl (the last task that can touch SKILL.md)
**Targets to verify:** `SKILL.md`, `references/styles.css`, `references/main.js`, `references/build.sh`, `references/_base.html`, `references/_footer.html`, `references/flavors/vibe-coder.md`

## BDD Scenarios

```gherkin
Scenario: Existing trigger phrases still activate the skill
  Given a user says any of:
    - "Turn this into a course"
    - "Explain this codebase interactively"
    - "Make a course from this project"
    - "Teach me how this code works"
    - "Interactive tutorial from this code"
  When the skill processes the request
  Then the skill activates
    And proceeds to Phase 0 (flavor selection)

Scenario: The build pipeline is unchanged
  Given any flavor is selected
  When Phase 3 completes and build.sh runs
  Then the output directory structure matches the current skill exactly:
    course-name/
      styles.css
      main.js
      _base.html
      _footer.html
      build.sh
      modules/*.html
      index.html
    And styles.css is byte-identical to references/styles.css
    And main.js is byte-identical to references/main.js

Scenario: Vibe Coder flavor preserves current experience
  Given a user who previously used the skill picks Vibe Coder
  When the skill produces the course
  Then the learner sees the same type of content they saw before the flavor system landed:
    - Line-by-line Code ↔ English translations
    - Aggressive glossary tooltips on every term
    - Warm "smart friend" voice
    - Infographic-style visual density
    - "Why should I care = steer AI better" framing
```

## Acceptance Criteria (Checklist)

### Build pipeline files — byte-identical to pre-refactor state

- [ ] `references/styles.css` has not been modified since task 007-impl. (Verify via `git diff HEAD~N -- references/styles.css` where N is the number of commits in the refactor sequence. Must show no changes.)
- [ ] `references/main.js` has not been modified. (Same method.)
- [ ] `references/build.sh` has not been modified.
- [ ] `references/_base.html` has not been modified.
- [ ] `references/_footer.html` has not been modified.
- [ ] `references/interactive-elements.md` has not been modified.
- [ ] `references/design-system.md` has not been modified.

### Trigger phrases preserved in SKILL.md

- [ ] The YAML frontmatter `description:` field in SKILL.md contains all of the following (case-insensitive substring match):
  - [ ] "turn this into a course"
  - [ ] "explain this codebase interactively"
  - [ ] "teach this code"
  - [ ] "interactive tutorial from code"
  - [ ] "codebase walkthrough"
  - [ ] "learn from this codebase"
  - [ ] "make a course from this project"
- [ ] No trigger phrases have been removed or reworded to the point of breaking keyword match.

### First-Run Welcome preserved

- [ ] The "## First-Run Welcome" section in SKILL.md is present and its text is semantically identical to the pre-refactor version. It may have minor typo fixes but should not be restructured.

### Vibe Coder playbook semantic equivalence

- [ ] `references/flavors/vibe-coder.md` exists (created by task 001-impl).
- [ ] The playbook's Section 4 (Module Arc) contains the same 7 module positions as the pre-refactor SKILL.md lines 75-83 table.
- [ ] The playbook's Section 5 (Code block style) specifies line-by-line "Code ↔ Plain English" translations matching the pre-refactor content-philosophy.md rules.
- [ ] The playbook's Section 8 (Tooltip strategy) specifies ultra-aggressive tooltipping matching the pre-refactor content-philosophy.md + gotchas.md rules.
- [ ] The playbook's Section 9 (Voice) specifies "smart friend" tone.
- [ ] The playbook's Section 10 (Visual density) specifies infographic-style (50%+ visual, 2-3 sentence cap).
- [ ] The playbook's Section 11 (Why should I care?) specifies the practical AI-steering framing.

### Output directory structure unchanged

- [ ] SKILL.md still documents the course output directory structure:
  ```
  course-name/
    styles.css
    main.js
    _base.html
    _footer.html
    build.sh
    modules/*.html
    index.html
  ```
- [ ] No new file types have been added to the course output structure (flavor playbooks live in the skill's own references/, not in the generated course).

### `references/flavors/` directory is isolated

- [ ] `references/flavors/` exists and contains exactly the 5 expected files: `vibe-coder.md`, `onboarding.md`, `pattern-learning.md`, `architecture-review.md`, `deep-understanding.md`.
- [ ] No other files in the repo reference `references/flavors/` except: SKILL.md (Phase 0 + Phase 3 + Reference Files section), `module-brief-template.md` (the Flavor field + Reference Files list), and the design/plan docs.

## How to Run Verification

1. `git diff <base-ref>..HEAD -- references/styles.css references/main.js references/build.sh references/_base.html references/_footer.html references/interactive-elements.md references/design-system.md` → empty output (no changes).
2. `grep -i "turn this into a course" SKILL.md` → match.
3. Repeat for each trigger phrase.
4. Open `SKILL.md` and visually confirm the First-Run Welcome section is intact.
5. Open `references/flavors/vibe-coder.md` and cross-check its Sections 4, 5, 8, 9, 10, 11 against the pre-refactor SKILL.md and content-philosophy.md semantically.
6. `ls references/flavors/` → exactly 5 `.md` files.

## Pass / Fail

Pass: all checks succeed. Fail: any check fails — the refactor has introduced a regression and must be corrected before merging.

## No implementation task

This is a pure verification task. If any check fails, the failing condition is traced back to whichever earlier task (001-007) introduced the regression, and that task's impl is corrected in a follow-up commit.
