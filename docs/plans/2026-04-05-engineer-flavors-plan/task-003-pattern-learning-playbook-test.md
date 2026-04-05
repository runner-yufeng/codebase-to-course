# Task 003: Pattern Learning Playbook — Verification Rubric

**Type:** test (Red)
**depends-on:** (none)
**Target to verify:** `references/flavors/pattern-learning.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 3: Pattern Learning"

## BDD Scenarios

```gherkin
Scenario: User picks Pattern Learning
  Given the flavor question has been asked
  When the user picks "Pattern Learning"
  Then the skill reads references/flavors/pattern-learning.md
    And the curriculum follows the pattern-learning arc (thesis → pattern 1 → pattern 2 → pattern 3 → composition → transfer)
    And every pattern is named explicitly (e.g., "this is the reactor pattern", "this is copy-on-write")
    And every pattern module ends with a "Transfer" callout stating where else this pattern applies
    And code blocks show "Code ↔ pattern name + reuse note" annotations
    And metaphors are used sparingly; formal pattern vocabulary is preferred

Scenario: Pattern Learning names every pattern explicitly
  Given the flavor is Pattern Learning
  When a module teaches a technique from the codebase
  Then the technique has a named label (formal pattern name or author-coined term)
    And the module includes a "Transfer" callout listing at least 2 other contexts where the pattern applies
    And code blocks are annotated with the pattern name in the right column
```

## Acceptance Criteria (Checklist)

### File existence
- [ ] `references/flavors/pattern-learning.md` exists.
- [ ] File is valid Markdown.

### Structural compliance (12-section template)
- [ ] Section 1: "Audience snapshot" describes a mid-to-senior engineer studying a well-regarded OSS project to extract reusable techniques.
- [ ] Section 2: "Why this approach works" articulates why framing + naming transforms "reading good code" from trivia into transferable knowledge.
- [ ] Section 3: "Core question" reads approximately: *"What clever thing is this codebase doing that I can reuse?"*
- [ ] Section 4: "Module arc" contains 4-6 modules following the structure: thesis → pattern 1 → pattern 2 → pattern 3 → composition → transfer.
- [ ] Section 5: "Code block style" specifies "Code ↔ pattern name + reuse note" — left: real code; right: formal pattern name + a 1-line "reuse when…" statement.
- [ ] Section 6: "Quiz style" specifies transfer tests ("which of these problems would this pattern solve?") and explicitly prohibits "what is this pattern called?" recall questions.
- [ ] Section 7: "Metaphor strategy" specifies **none to sparing** and justifies why (metaphors dilute pattern names).
- [ ] Section 8: "Tooltip strategy" specifies tooltipping formal pattern names + OSS-specific jargon with 1-line definitions and "see also" references.
- [ ] Section 9: "Voice & tone" specifies "sharp peer showing off a trick".
- [ ] Section 10: "Visual density" specifies **denser prose** — the trick lives in the nuance.
- [ ] Section 11: "Why should I care?" framing per module ties back to "steal a technique for your own work".
- [ ] Section 12: "Overrides" lists relaxed rules (2-3 sentence cap relaxed, 50%+ visual relaxed, code block style replaced).

### Must-have element: Transfer callouts
- [ ] The playbook states that **every pattern module ends with a "Transfer" callout** — not optional.
- [ ] The playbook specifies that the Transfer callout lists at least 2-3 other contexts where the same pattern applies.
- [ ] The playbook provides an example Transfer callout (e.g., naming reactor pattern transfers).
- [ ] The playbook clarifies that without the Transfer callout, the pattern does not transfer and the flavor has failed.

### Content rules specific to Pattern Learning
- [ ] The playbook requires **explicit naming** for every technique taught — "formal pattern name or author-coined term". Prohibits unnamed "clever tricks".
- [ ] The playbook cites research exemplars (aosabook, Julia Evans zines, Dan Luu's critique, Regehr's LLVM tour).
- [ ] The playbook lists known pitfalls: course-as-tour, failing to name the transfer, over-explaining the domain.
- [ ] The playbook emphasizes **depth over breadth**: 4-6 mechanisms deep, not a tour.

### Cross-reference integrity
- [ ] No broken links.

## How to Run Verification

1. `ls references/flavors/pattern-learning.md` → exits 0.
2. Grep for `## 4. Module arc` and confirm the thesis → patterns → transfer structure.
3. Grep for `Transfer` (capitalized) — must appear at least twice in Section 4b / 11 / example content.
4. Grep for "reactor", "copy-on-write", or any example formal pattern name to confirm examples are present.
5. Read Section 6 and confirm "what is this pattern called" is explicitly marked as a prohibited quiz archetype.
6. Read Section 12 and confirm the Code-↔-English base rule is explicitly overridden.

## Initial State (Red)

All checks fail because `references/flavors/pattern-learning.md` does not exist yet.
