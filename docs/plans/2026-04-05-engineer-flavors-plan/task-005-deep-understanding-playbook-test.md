# Task 005: Deep Understanding Playbook — Verification Rubric

**Type:** test (Red)
**depends-on:** (none)
**Target to verify:** `references/flavors/deep-understanding.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 5: Deep Understanding"

## BDD Scenarios

```gherkin
Scenario: User picks Deep Understanding
  Given the flavor question has been asked
  When the user picks "Deep Understanding"
  Then the skill reads references/flavors/deep-understanding.md
    And the curriculum follows the deep-understanding arc (problem → abstractions → flow → subsystem A → subsystem B → evolution)
    And code blocks show "Code ↔ mental-model diagram" annotations
    And tooltips are generous (audience variance is high)
    And the voice is curious-guide with layered reveal
```

## Acceptance Criteria (Checklist)

### File existence
- [ ] `references/flavors/deep-understanding.md` exists.
- [ ] File is valid Markdown.

### Structural compliance (12-section template)
- [ ] Section 1: "Audience snapshot" describes a generic curious engineer with no specific forcing function — broadest audience.
- [ ] Section 2: "Why this approach works" articulates the "narrative completeness" differentiation from the other engineer flavors.
- [ ] Section 3: "Core question" reads approximately: *"How does this system actually work, end-to-end?"*
- [ ] Section 4: "Module arc" contains 5-6 modules: problem → core abstractions → data & control flow → subsystem deep dive A → subsystem deep dive B → evolution & tradeoffs.
- [ ] Section 5: "Code block style" specifies "Code ↔ mental-model diagram" — left: real code; right: a diagram or concise textual model of the abstraction the code implements.
- [ ] Section 6: "Quiz style" specifies comprehension-tracing ("trace the request; what invariant holds at step 3?").
- [ ] Section 7: "Metaphor strategy" specifies **moderate** — one metaphor per subsystem to anchor the mental model, then drop.
- [ ] Section 8: "Tooltip strategy" specifies **generous** — audience variance is high.
- [ ] Section 9: "Voice & tone" specifies "curious guide, layered reveal".
- [ ] Section 10: "Visual density" specifies **balanced** — layered diagrams that progressively reveal.
- [ ] Section 11: "Why should I care?" framing ties to "becoming better at system design in general".
- [ ] Section 12: "Overrides" lists rules this flavor relaxes.

### Must-have element: progressive-depth reveal
- [ ] The playbook states that **each module should begin where the previous one stopped and zoom in one more level** — a cumulative depth structure.
- [ ] The playbook explicitly warns that without a progressive-depth structure, the flavor becomes a random walk.

### Differentiation from other flavors
- [ ] The playbook **explicitly warns** that Deep Understanding's differentiation is **narrative completeness**, not sharpness.
- [ ] The playbook explicitly says: if the user wants sharpness, they should pick Pattern Learning or Architecture Review; Deep Understanding should not try to out-specialize those flavors.

### Content rules specific to Deep Understanding
- [ ] The playbook lists known pitfalls: overclaiming audience ("for everyone"), no narrative spine, being a weaker version of other flavors.
- [ ] The playbook cites exemplars (aosabook, Database Internals, Julia Evans zines).

### Cross-reference integrity
- [ ] No broken links.

## How to Run Verification

1. `ls references/flavors/deep-understanding.md` → exits 0.
2. Grep for "progressive" or "layered reveal" — must appear in Section 4/4b/10.
3. Grep for "narrative completeness" — must appear as the flavor's differentiation statement.
4. Read Section 4 and confirm the 5-6 module arc matches.
5. Read Section 2 (or nearby) and confirm the explicit disclaimer against trying to out-specialize the other engineer flavors.

## Initial State (Red)

All checks fail because `references/flavors/deep-understanding.md` does not exist yet.
