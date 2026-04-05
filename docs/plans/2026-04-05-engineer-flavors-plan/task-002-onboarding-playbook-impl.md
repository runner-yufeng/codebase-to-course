# Task 002: Onboarding Playbook — Implementation

**Type:** impl (Green)
**depends-on:** task-002-onboarding-playbook-test
**Target to create:** `references/flavors/onboarding.md`
**Design reference:** `docs/plans/2026-04-05-engineer-flavors-design/best-practices.md` → "Flavor 2: Onboarding"; `docs/plans/2026-04-05-engineer-flavors-design/architecture.md` → "Playbook structure (shared template)"

## BDD Scenarios Covered

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

## What to Implement

Create `references/flavors/onboarding.md` following the 12-section playbook template. Source the content from the design doc — **do not invent new material**.

1. **Section 1 — Audience snapshot.** Describe a polyglot engineer with 3+ years of experience, strong in one stack, joining a codebase in an unfamiliar stack. Their panic isn't "I can't code" — it's "I don't know this team's way." Source: `best-practices.md` → "Flavor 2 → Audience snapshot".

2. **Section 2 — Why this approach works.** Articulate the "walked path into one real change" motivation. Cite the research exemplars (Stripe's spin-up project, Zapier's personalized onboarding doc, GitHub engineers' end-to-end module traversal). Source: `best-practices.md` → "Flavor 2 → Real pain points" and "Exemplars".

3. **Section 3 — Core question.** *"Where does X live and how do I change it the way this team would?"*

4. **Section 4 — Module arc (menu).** The six modules are prescriptive in order (unlike vibe coder's adaptable menu). Each module entry should name the module + 1-line purpose + 1-line "why it matters for onboarding":
   - 10-minute mental model
   - Dev loop (setup, run, test)
   - One end-to-end feature trace
   - Local conventions (naming, errors, tests, folder layout)
   - PR & review norms
   - Your first change (see Section 4b)

5. **Section 4b — Must-have final module.** Mark the "Your first change" module as **not optional**. Specify that it walks the learner through a realistic change request ("add a new field to the user profile response") by tracing: (a) which files they'd touch in order, (b) what tests they'd add, (c) what the PR description would look like. Include a template for how this module should be structured in the HTML output. Source: `best-practices.md` → "Flavor 2 → The must-have final module".

6. **Section 5 — Code block style ("Code ↔ Convention").** Specify the two-column format: left = real code verbatim from the codebase; right = the team's unwritten rule the code obeys, expressed as a short imperative. Provide 2 example annotation entries (e.g., *"Errors are always wrapped with `fmt.Errorf` and a context prefix — never return a bare error."* and *"Handlers take `ctx` as the first param. Always."*). Clarify that the right column is *not* line-by-line English translation — it's a single rule with code as evidence.

7. **Section 6 — Quiz style.** Specify procedural-fluency scenarios. Provide 1-2 example question archetypes (e.g., *"You need to add a new `/v2/users/:id/preferences` endpoint. In what order do you touch files, and what's the first test you write?"*). **Explicitly prohibit** syntax-recall, keyword-definition, and "what does this function return" style questions. Source: `best-practices.md` → "Flavor 2 → Content rules → Quiz style".

8. **Section 7 — Metaphor strategy.** **Sparing.** Only for genuinely unfamiliar infra (message queues, event loops). Never for language/framework basics (closures, async, classes) — the audience already knows those. No everyday-life metaphors (restaurant, bouncer, etc.).

9. **Section 8 — Tooltip strategy.** Tooltip: (a) the codebase's own jargon (internal service names, custom decorators, domain terms), (b) stack-specific terminology when the stack is unfamiliar to a polyglot. Assume language/framework basics known. Acronyms: tooltip project-coined ones; assume standard ones (API, REST, CLI) known.

10. **Section 9 — Voice & tone.** Pragmatic senior teammate. *"Here's what I wish I'd known week one."* Welcoming, direct, occasionally dry. No handholding lectures. Sentence length: medium. Humor: sparing, situational.

11. **Section 10 — Visual density target.** **Balanced.** Diagrams for the end-to-end trace (mandatory), numbered step cards for the PR workflow, prose for conventions (conventions do not diagram well). The 2-3 sentence ceiling from content-philosophy.md is **relaxed** for conventions sections but still applies to opening hooks and quiz explanations.

12. **Section 11 — "Why should I care?" framing per module.** Each module ties back to the outcome: "this is what you need to ship your first PR without breaking something." Provide a one-line framing for each of the 6 modules that the writing agent can adapt.

13. **Section 12 — Overrides to `content-philosophy.md`.** Explicitly list which base-layer rules this flavor relaxes or replaces:
    - **Replaces:** "Code ↔ Plain English Translations" → Code ↔ Convention.
    - **Relaxes:** "Be extremely aggressive with tooltips" → restrict to codebase jargon + unfamiliar stack terms.
    - **Relaxes:** "Max 2-3 sentences per text block" → conventions sections may exceed this when the rule requires it.
    - **Keeps:** all universal rules (no recycled metaphors, original code only, quizzes test application, show don't tell, no horizontal scrollbars, tooltip clipping rule).

14. **Known pitfalls to avoid.** Include a short sub-section listing the pitfalls from `best-practices.md`:
    - Dumping org chart and history before the learner cares.
    - Teaching language/framework basics.
    - Skipping test-writing conventions.
    - Modules that read like a README table of contents.

## Verification (Green)

Run `task-002-onboarding-playbook-test.md` checklist. Every item should pass.

## Commit Boundary

Single commit, suggested message:

```
feat: add onboarding flavor playbook

Playbook for engineers joining a codebase in an unfamiliar stack.
Specifies the 6-module arc ending in a simulated first PR, the
Code ↔ Convention block style, and the procedural-fluency quiz
rules.

Part of the engineer-flavors design:
docs/plans/2026-04-05-engineer-flavors-design/
```
