# Task 004: Architecture Review Playbook — Implementation

**Type:** impl (Green)
**depends-on:** task-004-architecture-review-playbook-test
**Target to create:** `references/flavors/architecture-review.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 4: Architecture Review"

## BDD Scenarios Covered

```gherkin
Scenario: User picks Architecture Review
  Given the flavor question has been asked
  When the user picks "Architecture Review"
  Then the skill reads references/flavors/architecture-review.md
    And the curriculum follows the architecture-review arc
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

## What to Implement

Create `references/flavors/architecture-review.md` following the 12-section template. Source: `best-practices.md` → "Flavor 4: Architecture Review".

1. **Section 1 — Audience snapshot.** Senior/staff engineer (5+ years) evaluating a codebase's architectural decisions to form a defensible opinion. Wants to answer: *would I build it this way? where will it hurt at scale? what would I change?*

2. **Section 2 — Why this approach works.** Cite DDIA's tradeoff-per-concept model, ATAM's structured quality-attribute scoring, ADR archives (Fowler, Joel Parker Henderson). Explain why abstract descriptions fail this audience and why concrete coupling graphs + stances win.

3. **Section 3 — Core question.** *"Would I build it this way, and where will it hurt at scale?"*

4. **Section 4 — Module arc (menu).** 5-6 modules:
   - Architectural thesis & constraints (what problem is this system's shape optimized for?)
   - Decision 1 + tradeoff
   - Decision 2 + tradeoff
   - (Optional) Decision 3 + tradeoff
   - Coupling & data flow critique
   - Scalability pressure points
   - Tech debt hotspots & verdict

   Each "decision + tradeoff" module uses the ADR-style structure from Section 5.

5. **Section 4b — Must-have element: Verdict lines.** State explicitly:
   - Every major decision module **ends with a Verdict line** — not optional.
   - Verdicts are stances, not summaries.
   - Provide an example: *"Verdict: This trade-off is justified at current scale but will become the scaling bottleneck above ~10k writes/sec. I would split the write path into a separate service before then."*
   - Without verdicts, the flavor has failed.

6. **Section 5 — Code block style ("Code ↔ ADR-style tradeoff").** Two columns. Left: real code. Right: a four-line block:
   - **Context** — what constraint this addresses
   - **Decision** — what this code chooses
   - **Consequence** — what the choice buys and what it costs
   - **Verdict** — opinionated stance (one line)

   Provide an example block using a real-world analog (e.g., "decision to use optimistic concurrency control").

7. **Section 6 — Quiz style.** Critical-judgment questions. Example archetypes:
   - *"Here's a new requirement: 10x traffic growth. Which of the decisions you just read about breaks first, and why?"*
   - *"You're adding a new compliance requirement (e.g., audit log). Which architectural choice makes this hardest?"*
   - *"Given the tradeoffs, where would you spend the next engineer-year of refactoring effort?"*

   Tests critical judgment, not recall.

8. **Section 7 — Metaphor strategy. PROHIBITED.** State explicitly:
   - **No metaphors.** Not "the database is a library." Not "the cache is a shortcut." Not "the queue is a mailbox."
   - **No restaurant, kitchen, bouncer, nightclub, or postal service analogies.**
   - Metaphors feel condescending to this audience.
   - Precision beats imagery. Use precise architectural vocabulary (backpressure, idempotency, eventual consistency, causal ordering, read-your-writes, etc.) directly.
   - The only exception is a **one-line** system-design vocabulary anchor when a term is first introduced — but even then, prefer the tooltip to a metaphor.

9. **Section 8 — Tooltip strategy. STINGY.** Tooltip only non-standard architectural vocabulary (e.g., "outbox pattern", "CQRS projection", project-coined terms). Assume the learner knows: CAP, ACID, BASE, idempotency, eventual consistency, backpressure, sharding, replication, consensus basics, 2PC, Paxos/Raft at a high level, read/write skew, isolation levels.

10. **Section 9 — Voice & tone.** Principled staff engineer with a thesis. *"This is defensible — but watch this seam."* Takes stances. Says "I'd change this" out loud. Opinionated. Never neutral-descriptive.

11. **Section 10 — Visual density target. DIAGRAM-HEAVY.** Coupling graphs, data flow diagrams, pressure-point overlays. Prose carries the *stance*; diagrams carry the *evidence*. Every decision module should have at least one coupling-or-flow diagram grounded in this specific codebase's actual structure — not generic theoretical diagrams.

12. **Section 11 — "Why should I care?" framing per module.** Each module frames the learning as "forming an informed opinion for your own hiring, contributing, or design decisions." Provide one-liners per module.

13. **Section 12 — Overrides to `content-philosophy.md`:**
    - **Replaces:** "Code ↔ Plain English" → Code ↔ ADR-style (Context / Decision / Consequence / Verdict).
    - **Replaces:** "Metaphors first, then reality" → **No metaphors.**
    - **Replaces:** "Quizzes test 'where would you look first'" → Quizzes test critical judgment under stressors.
    - **Relaxes:** "Max 2-3 sentences per text block" → tradeoff prose may run longer.
    - **Tightens:** tooltip strategy → only non-standard architectural terms.
    - **Keeps:** universal rules (no recycled metaphors — vacuously true here; original code only; etc.).

14. **Known pitfalls to avoid:**
    - Pure description without stance (the #1 failure).
    - Generic theoretical diagrams instead of this codebase's actual coupling graph.
    - Ignoring tech debt hotspots and distributed-monolith smells.
    - Using metaphors. Don't.

## Verification (Green)

Run `task-004-architecture-review-playbook-test.md` checklist.

## Commit Boundary

Single commit, suggested message:

```
feat: add architecture-review flavor playbook

Playbook for senior engineers forming a defensible opinion about a
codebase's architecture. Specifies the thesis → decisions + tradeoffs
→ verdict arc, the Code ↔ ADR-style block template, critical-judgment
quizzes, and mandatory verdict lines per decision. Explicitly
prohibits metaphors.

Part of the engineer-flavors design:
docs/plans/2026-04-05-engineer-flavors-design/
```
