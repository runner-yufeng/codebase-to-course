# Task 003: Pattern Learning Playbook — Implementation

**Type:** impl (Green)
**depends-on:** task-003-pattern-learning-playbook-test
**Target to create:** `references/flavors/pattern-learning.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 3: Pattern Learning"

## BDD Scenarios Covered

```gherkin
Scenario: User picks Pattern Learning
  Given the flavor question has been asked
  When the user picks "Pattern Learning"
  Then the skill reads references/flavors/pattern-learning.md
    And the curriculum follows the pattern-learning arc (thesis → pattern 1 → pattern 2 → pattern 3 → composition → transfer)
    And every pattern is named explicitly
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

## What to Implement

Create `references/flavors/pattern-learning.md` following the 12-section template. Source the content from `best-practices.md` → "Flavor 3: Pattern Learning".

1. **Section 1 — Audience snapshot.** Mid-to-senior engineer (3+ years) reading a well-regarded OSS project (Redis, Next.js, LangChain, Django, PostgreSQL, etc.) to extract reusable techniques for their own work. Already knows what caches, queues, schedulers *are* — wants the specific clever move this codebase made.

2. **Section 2 — Why this approach works.** The learner has general fluency but no framing device — without naming patterns and explicitly stating transfer contexts, reading good code degenerates into trivia collection. Cite Regehr's LLVM tour, AlgoCademy's framing argument, GitHub engineers' learning approach, and the aosabook model of author-written pattern chapters.

3. **Section 3 — Core question.** *"What clever thing is this codebase doing that I can reuse?"*

4. **Section 4 — Module arc (menu).** 4-6 modules in this structure:
   - Module 1: One-line thesis of this codebase (what problem does it solve uniquely well? what is the ONE idea that powers it?).
   - Modules 2-4 (or 2-5): Pattern modules, one per technique. Each is deep, not broad.
   - Penultimate: How these patterns compose (what emerges when they're combined?).
   - Final: Where each pattern transfers (beyond this codebase).
   - **Breadth is the enemy.** 4-6 is the ceiling. Do not add modules just to fill space.

5. **Section 4b — Must-have element: Transfer callouts.** State that every pattern module **ends with a "Transfer" callout box** — not optional. The callout lists at least 2-3 other contexts where the same pattern applies. Include an example:
   > **Transfer:** The reactor pattern applies anywhere you need to handle many concurrent I/O streams on a small number of threads. See also: Node.js event loop (reactor + callback queue); nginx worker processes (reactor + epoll); Go's netpoll (reactor + goroutines); libuv (reactor + thread pool).

   State explicitly: **without the Transfer callout, the pattern does not transfer and the flavor has failed.**

6. **Section 5 — Code block style ("Code ↔ pattern name + reuse note").** Two columns. Left: real code. Right: the formal pattern name in bold, followed by a 1-line "reuse when…" imperative. Provide an example:
   > **Reactor pattern.** A single thread multiplexes I/O across many connections via `epoll`. Reuse when you need to handle thousands of concurrent network clients on one core.

   Contrast this with the vibe-coder "line-by-line English" style: the right column is *not* translating the code; it is labeling the *pattern* the code embodies.

7. **Section 6 — Quiz style.** Transfer tests. Provide example archetypes:
   - *"Which of these three problems would this technique solve best? Why?"*
   - *"You're building [a specific new system]. Where would this pattern apply in your design?"*
   - *"Here's code from a different project [snippet] — which of the patterns you learned does this embody?"*

   **Explicitly prohibit** "what is this pattern called?" — the course already told them the name. The test is whether they can *recognize the problem shape* in a new context.

8. **Section 7 — Metaphor strategy.** **None to sparing.** Metaphors dilute precise pattern names. Prefer *"this is the outbox pattern"* over *"this is like leaving a note on the kitchen counter."* When a metaphor is used, it's in service of a crisp mental model, not as a primary teaching tool.

9. **Section 8 — Tooltip strategy.** Tooltip formal pattern names (reactor, copy-on-write, outbox, saga, CQRS projection, etc.) with a 1-line definition and a "see also" reference (other projects, well-known papers, or chapters of classic books). Tooltip project-specific jargon. Assume general CS vocabulary (async, hash tables, tree balance, ACID).

10. **Section 9 — Voice & tone.** Sharp peer showing off a trick. *"Look what they did here — this is the move."* Enthusiastic about cleverness, but technically precise. No hand-waving. No "kind of like".

11. **Section 10 — Visual density target.** **Denser prose.** The trick lives in the nuance of the mechanism — a module about a subtle locking strategy should be mostly prose + code. Diagrams still exist for the compositional view (how the patterns interlock) but are not mandatory per-module. The content-philosophy.md "50%+ visual" rule is **overridden** to "at least one visual element per module, but prose is the primary carrier".

12. **Section 11 — "Why should I care?" framing.** Each module frames the learning as "a technique you can steal for your own work". The writing agent should end every pattern module with a sentence starting "*You'd use this when…*" followed by the transfer contexts.

13. **Section 12 — Overrides to `content-philosophy.md`.** Explicitly list:
    - **Replaces:** "Code ↔ Plain English Translations" → Code ↔ Pattern name + reuse note.
    - **Replaces:** "Quizzes test 'where would you look first'" → Quizzes test transfer ("which problem does this solve?").
    - **Relaxes:** "50%+ visual" → at least one visual per module.
    - **Relaxes:** "Max 2-3 sentences per text block" → prose may run longer when the mechanism requires it.
    - **Relaxes:** "Aggressive tooltips" → tooltips for pattern names and OSS-specific jargon only; assume general CS vocabulary.
    - **Keeps:** universal rules (no recycled metaphors, original code only, etc.).

14. **Known pitfalls to avoid** (sub-section): course-as-tour, failing to name the transfer, over-explaining the domain.

## Verification (Green)

Run `task-003-pattern-learning-playbook-test.md` checklist.

## Commit Boundary

Single commit, suggested message:

```
feat: add pattern-learning flavor playbook

Playbook for engineers studying OSS codebases to extract reusable
techniques. Specifies the thesis → patterns → transfer arc, the
Code ↔ pattern-name block style, transfer-test quizzes, and
mandatory Transfer callouts.

Part of the engineer-flavors design:
docs/plans/2026-04-05-engineer-flavors-design/
```
