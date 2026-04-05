# Task 004: Architecture Review Playbook — Verification Rubric

**Type:** test (Red)
**depends-on:** (none)
**Target to verify:** `references/flavors/architecture-review.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 4: Architecture Review"

## BDD Scenarios

```gherkin
Scenario: User picks Architecture Review
  Given the flavor question has been asked
  When the user picks "Architecture Review"
  Then the skill reads references/flavors/architecture-review.md
    And the curriculum follows the architecture-review arc (thesis & constraints → decisions with tradeoffs → coupling critique → scalability pressure points → tech debt verdict)
    And every major architectural decision includes a "Context / Decision / Consequence" block with an explicit verdict line
    And code blocks show "Code ↔ ADR-style tradeoff" annotations
    And metaphors are avoided entirely
    And tooltips are sparse — reserved for non-standard architectural vocabulary
    And the voice is principled-staff-engineer-with-a-thesis
    And the course never describes without taking a stance

Scenario: Architecture Review course contains no restaurant metaphors
  Given the flavor is Architecture Review
  When the skill writes any module
  Then no module uses a metaphor from everyday life
    And tradeoffs are expressed in precise architectural vocabulary
    And each decision block has a "what this buys / what it costs / where it'll break" structure
```

## Acceptance Criteria (Checklist)

### File existence
- [ ] `references/flavors/architecture-review.md` exists.
- [ ] File is valid Markdown.

### Structural compliance (12-section template)
- [ ] Section 1: "Audience snapshot" describes a senior/staff engineer evaluating architectural decisions to form a defensible opinion.
- [ ] Section 2: "Why this approach works" articulates why concrete + opinionated beats abstract + neutral.
- [ ] Section 3: "Core question" reads approximately: *"Would I build it this way, and where will it hurt at scale?"*
- [ ] Section 4: "Module arc" contains 5-6 modules following: thesis & constraints → decision 1 + tradeoff → decision 2 + tradeoff → coupling & data flow critique → scalability pressure points → tech debt hotspots & verdict.
- [ ] Section 5: "Code block style" specifies "Code ↔ ADR-style" — left: real code; right: Context / Decision / Consequence + Verdict line.
- [ ] Section 6: "Quiz style" specifies critical-judgment questions (*"which decision breaks first under stressor X?"*).
- [ ] Section 7: "Metaphor strategy" specifies **none** — and explicitly states metaphors feel condescending to this audience.
- [ ] Section 8: "Tooltip strategy" specifies **stingy** — only non-standard architectural vocabulary.
- [ ] Section 9: "Voice & tone" specifies "principled staff engineer with a thesis".
- [ ] Section 10: "Visual density" specifies **diagram-heavy** (coupling graphs, data flow, pressure-point overlays) with prose carrying the stance.
- [ ] Section 11: "Why should I care?" framing per module ties to "forming an informed opinion for hiring, contributing, or design decisions".
- [ ] Section 12: "Overrides" lists the rules this flavor overrides.

### Must-have element: Verdict lines
- [ ] The playbook states that **every major decision module ends with a Verdict line** — not optional.
- [ ] The playbook specifies that verdicts are stances, not summaries (example: *"This trade-off is justified at current scale but will become the scaling bottleneck above ~10k writes/sec."*).
- [ ] The playbook states explicitly: without verdicts, the flavor has failed.

### Content rules specific to Architecture Review
- [ ] The playbook requires **concrete evidence** — this codebase's actual coupling graph, not generic theoretical diagrams.
- [ ] The playbook includes the "Context / Decision / Consequence / Verdict" ADR-style template for decision modules.
- [ ] The playbook cites research exemplars (DDIA, ATAM, Fowler ADR bliki, Mozilla architecture review process, Ilograph).
- [ ] The playbook lists known pitfalls: pure description without stance, generic theoretical diagrams, ignoring tech debt, using metaphors.
- [ ] The playbook requires every decision module to have a "what this buys / what it costs / where it'll break" structure.

### Metaphor prohibition
- [ ] The playbook **explicitly states** that metaphors are prohibited in this flavor.
- [ ] The playbook **explicitly states** that "restaurant" and other everyday-life metaphors are off-limits.
- [ ] Section 7 is not empty — it affirmatively declares the no-metaphor rule and explains why (precision beats imagery; condescending to the audience).

### Cross-reference integrity
- [ ] No broken links.

## How to Run Verification

1. `ls references/flavors/architecture-review.md` → exits 0.
2. Grep for "Verdict" — must appear as part of the ADR-style template and as a "mandatory element" note.
3. Grep for "metaphor" — must appear in Section 7 in the prohibiting context.
4. Grep for "Context" and "Decision" and "Consequence" — all three must appear in Section 5 as part of the code-block template.
5. Read Section 4 and confirm the 5-6 module arc matches the design doc.
6. Read Section 9 and confirm the voice descriptor is "principled staff engineer" or equivalent phrase emphasizing a thesis/stance.

## Initial State (Red)

All checks fail because `references/flavors/architecture-review.md` does not exist yet.
