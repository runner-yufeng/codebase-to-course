# Task 002: Onboarding Playbook — Verification Rubric

**Type:** test (Red)
**depends-on:** (none — independent playbook)
**Target to verify:** `references/flavors/onboarding.md` (to be created by task 002-impl)
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 2: Onboarding"

## BDD Scenarios

```gherkin
Scenario: User picks Onboarding
  Given the flavor question has been asked
  When the user picks "Onboarding"
  Then the skill reads references/flavors/onboarding.md
    And the curriculum follows the onboarding module arc (mental model → dev loop → feature trace → conventions → PR norms → first change)
    And the final module simulates a first PR ("here's a realistic change — trace what you'd modify and why")
    And code blocks show "Code ↔ Convention" annotations (team's unwritten rules)
    And tooltips cover codebase-specific jargon and stack-specific terms but NOT general language basics
    And the voice is pragmatic-senior-teammate

Scenario: Onboarding course does not test syntax recall
  Given the flavor is Onboarding
  When the skill writes any quiz question
  Then no question asks "what is the correct syntax for X"
    And no question asks "what does keyword Y do in language Z"
    And questions focus on "where would you change things" and "what convention does this team follow"
```

## Acceptance Criteria (Checklist)

The `-impl` task is Green when every item below is satisfied.

### File existence
- [ ] `references/flavors/onboarding.md` exists.
- [ ] File is valid Markdown.

### Structural compliance (12-section playbook template from architecture.md)
- [ ] Section 1: "Audience snapshot" describes a polyglot engineer (3+ years, strong in one stack, new to this stack).
- [ ] Section 2: "Why this approach works" articulates why a walked-through-first-PR model beats org-chart-dumps.
- [ ] Section 3: "The learner's core question" reads approximately: *"Where does X live and how do I change it the way this team would?"*
- [ ] Section 4: "Module arc (menu)" contains 6 modules in this order: (1) 10-minute mental model, (2) dev loop (setup/run/test), (3) one end-to-end feature trace, (4) local conventions, (5) PR & review norms, (6) your first change.
- [ ] Section 5: "Code block style" specifies "Code ↔ Convention" — left: real code; right: the team's unwritten rule the code obeys, expressed as a short imperative.
- [ ] Section 6: "Quiz style" specifies procedural-fluency scenarios and explicitly prohibits syntax-recall and keyword-definition questions.
- [ ] Section 7: "Metaphor strategy" specifies **sparing** — only for unfamiliar infra, not for language/framework basics.
- [ ] Section 8: "Tooltip strategy" specifies: tooltip codebase-specific jargon and stack-specific terms; assume language/framework basics known.
- [ ] Section 9: "Voice & tone" specifies "pragmatic senior teammate, 'here's what I wish I'd known week one'".
- [ ] Section 10: "Visual density target" specifies **balanced** — diagrams for flows, numbered step cards for workflows, prose acceptable for conventions.
- [ ] Section 11: "Why should I care? framing" repeatedly ties modules back to "ship first PR without breaking things".
- [ ] Section 12: "Overrides to content-philosophy.md" explicitly overrides the "line-by-line Code ↔ Plain English" rule and relaxes the aggressive-tooltip rule for stack basics.

### Must-have final module rule
- [ ] The playbook states that the **final module is prescriptive, not optional**: a simulated first PR where the learner traces which files they'd touch, what tests they'd add, and what the PR description would look like.
- [ ] The playbook includes an example realistic change for the simulated-PR module (any concrete example).

### Content rules specific to Onboarding
- [ ] The playbook cites at least one of the research exemplars (Stripe, Zapier, GitHub blog) to motivate the approach.
- [ ] The playbook lists the known teaching pitfalls: org-chart dumps, teaching language basics, skipping test conventions, table-of-contents style modules.
- [ ] The "why should I care" framing is NOT the vibe-coder framing ("steer AI better"). It is the onboarding framing ("ship first PR without breaking things").

### Cross-reference integrity
- [ ] No broken links.
- [ ] Any references to `interactive-elements.md` or `design-system.md` use correct relative paths.

## How to Run Verification

1. `ls references/flavors/onboarding.md` → exits 0.
2. Grep for each expected section heading.
3. Read Section 4 and confirm the 6 module titles match exactly.
4. Read Section 6 and confirm it contains the phrase "syntax" or "keyword" in the *prohibited* context.
5. Read the final module description and confirm it contains "first PR" as a prescriptive requirement, not an option.

## Initial State (Red)

All checks fail because `references/flavors/onboarding.md` does not exist yet.
