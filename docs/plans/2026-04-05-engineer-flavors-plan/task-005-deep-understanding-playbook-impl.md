# Task 005: Deep Understanding Playbook — Implementation

**Type:** impl (Green)
**depends-on:** task-005-deep-understanding-playbook-test
**Target to create:** `references/flavors/deep-understanding.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 5: Deep Understanding"

## BDD Scenarios Covered

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

## What to Implement

Create `references/flavors/deep-understanding.md` following the 12-section template. Source: `best-practices.md` → "Flavor 5: Deep Understanding".

1. **Section 1 — Audience snapshot.** A curious engineer, no specific forcing function. Broadest audience, least opinionated framing. Wants a thorough, satisfying tour of how the whole system works. May have varied experience — this is the most audience-varied flavor.

2. **Section 2 — Why this approach works.** Cite cognitive load theory: without a job-to-be-done, learners skim and retain little, so the course needs a strong narrative spine. Cite aosabook, Database Internals (databass.dev), Julia Evans zines as exemplars. **Include a disclaimer:** Deep Understanding's differentiation is **narrative completeness**, not sharpness — if the user wants sharpness, they should pick Pattern Learning or Architecture Review. Do not try to out-specialize the other flavors.

3. **Section 3 — Core question.** *"How does this system actually work, end-to-end?"*

4. **Section 4 — Module arc (menu).** 5-6 modules:
   - What problem the system solves (the reason for its existence)
   - The core abstractions (the 3-5 key data shapes / concepts)
   - Data & control flow (how requests move through the system)
   - Subsystem deep dive A (pick the most interesting subsystem)
   - Subsystem deep dive B (pick another)
   - Evolution & tradeoffs (how this system got to its current shape, what's next)

5. **Section 4b — Must-have element: progressive-depth reveal.** State explicitly:
   - Each module begins where the previous one stopped and zooms in **one more level**.
   - This cumulative-depth structure is what distinguishes Deep Understanding from a random walk.
   - The writing agent should explicitly transition between modules with phrases like "*now zoom in on…*" or "*that subsystem had a box labeled X — here's what's inside.*"
   - Without progressive-depth reveal, the flavor has failed and modules feel disconnected.

6. **Section 5 — Code block style ("Code ↔ mental-model").** Two columns. Left: real code. Right: a diagram or concise textual model of the *abstraction* the code implements. The goal is to let the reader step back from the syntax and see the shape. Example: code for a concurrent hash map's bucket lock → right column shows a labeled diagram of the bucket striping scheme.

7. **Section 6 — Quiz style.** Comprehension-tracing questions. Example archetypes:
   - *"Trace a request from entry to response. At step 3, what invariant holds?"*
   - *"Here's a modified version of the pipeline [altered snippet] — what property of the original does it break?"*
   - *"Why does [subsystem X] need [specific component Y]? What would happen if we removed it?"*

   Tests whether the reader can follow the flow and identify load-bearing assumptions.

8. **Section 7 — Metaphor strategy. MODERATE.** One good metaphor per subsystem to anchor the mental model — then drop it and switch to precise vocabulary. Do not sustain metaphors across modules. Never reuse a metaphor. Restaurant is forbidden (as always).

9. **Section 8 — Tooltip strategy. GENEROUS.** This audience has the highest variance in background. When in doubt, tooltip. Err on the side of too many. Assume nothing specific about the reader's prior stack experience.

10. **Section 9 — Voice & tone.** Curious guide, layered reveal. *"Zoom in — now you can see why they needed that."* Warm, patient, genuinely interested. Never condescending, never rushed. The voice should feel like someone thinking out loud as they explore, not reading from prepared notes.

11. **Section 10 — Visual density target. BALANCED.** Layered diagrams that progressively reveal structure. The first module shows a high-level black box; later modules show the same box decomposed. The 2-3 sentence text cap from content-philosophy.md is **observed** (this flavor doesn't relax it — unlike Pattern Learning and Architecture Review).

12. **Section 11 — "Why should I care?" framing per module.** *"This is how the system really works — the kind of understanding that makes you better at system design in general."* Provide one-liners per module.

13. **Section 12 — Overrides to `content-philosophy.md`:**
    - **Replaces:** "Code ↔ Plain English" → Code ↔ Mental-model diagram.
    - **Replaces:** "Quizzes test 'where would you look first'" → Quizzes test comprehension tracing and invariants.
    - **Keeps:** Max 2-3 sentences per text block (this flavor does not relax it).
    - **Keeps:** 50%+ visual.
    - **Keeps:** Aggressive tooltips (generous — closer to vibe-coder than to architecture-review).
    - **Keeps:** Metaphors-first rule but limited to one per subsystem.

14. **Known pitfalls to avoid:**
    - Overclaiming audience ("for everyone") and ending up for no one.
    - No narrative spine — without a driving question, modules feel disconnected.
    - Being a weaker version of Pattern Learning or Architecture Review.

## Verification (Green)

Run `task-005-deep-understanding-playbook-test.md` checklist.

## Commit Boundary

Single commit, suggested message:

```
feat: add deep-understanding flavor playbook

Playbook for engineers wanting thorough comprehension without a
specific use case. Specifies the problem → abstractions → flow →
subsystems → evolution arc, the Code ↔ mental-model block style,
comprehension-tracing quizzes, and mandatory progressive-depth
reveal across modules.

Part of the engineer-flavors design:
docs/plans/2026-04-05-engineer-flavors-design/
```
