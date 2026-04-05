# Flavor Playbook: Onboarding

> **Audience in one line:** a polyglot engineer joining a codebase in a stack they don't yet know well. Goal: ship their first PR without breaking things.

> **This playbook overrides selected rules in `../content-philosophy.md`.** See Section 12 for the explicit list. Universal rules (no recycled metaphors, original code only, tooltip-clipping, no horizontal scrollbars) still apply.

---

## 1. Audience snapshot

A polyglot engineer with **3+ years of experience**, strong in one stack (say, Python/Django), joining a codebase in an unfamiliar one (say, Go + gRPC, or Rust + Axum, or TypeScript + Next.js app router). They are **not** beginners. They know what closures, async, classes, generics, and dependency injection are. They've shipped production code before.

What they don't have is this team's **way**. Their panic isn't "I can't code" — it's:

- *"I don't know where things live in this codebase."*
- *"I don't know which of the five ways to do X this team actually uses."*
- *"I don't know which tests I'm expected to write, or how the team wants errors handled, or what a reviewer will reject."*
- *"I need to ship something real in week one or two without looking lost."*

They are optimizing for **competent first contact**: a PR that looks like it was written by someone who has been on the team for six months, not six days. They want a walked path into one real change — not an org chart, not a history lesson, not a tour of every directory.

## 2. Why this approach works (for this audience)

Traditional onboarding fails polyglot engineers in three specific ways, all documented:

- **"Code culture shock."** Weeks are lost to environment setup and undocumented tooling. New engineers can read the code just fine; they cannot run it, test it, or deploy it the way the team expects. ([lonetrouper on DEV](https://dev.to/lonetrouper/onboarding-engineers-in-an-era-of-code-explosion-5ef9); [Cortex 2025 guide](https://www.cortex.io/post/developer-onboarding-guide))
- **Implicit knowledge trapped in senior heads.** The "why" isn't written down, only the "where." The codebase tells you what it does; only a senior can tell you *what the team will reject in review*. ([Multiplayer](https://www.multiplayer.app/blog/improving-developer-onboarding/))
- **Onboarding docs dump context instead of walking a change.** New engineers are handed architecture diagrams and team rosters before they've touched a single line of code. They memorize nothing and ship nothing. ([HubSpot product blog](https://product.hubspot.com/blog/onboarding-engineers-how-to-tackle-the-first-30-days))

The playbook this flavor teaches inverts that. Three exemplars show why:

- **Stripe's "spin-up project"** pairs a new engineer with a buddy and a small, real, well-scoped change from day one. The learning happens *around* a concrete PR, not before it. ([leportella.com](https://leportella.com/new-eng-stripe/))
- **Zapier's personalized onboarding doc** is a week-by-week living knowledge base, not a static handbook. It walks new engineers through the loop they'll actually live in. ([Zapier engineering](https://zapier.com/engineering/engineer-onboarding/))
- **GitHub engineers' end-to-end module traversal** — "follow one module deeply" beats "skim all modules." Depth on one feature is transferable; breadth over twenty isn't. ([GitHub blog](https://github.blog/developer-skills/application-development/how-github-engineers-learn-new-codebases/))

The through-line: **a walked path into one real change beats any amount of orientation material.** This playbook turns that into a six-module arc that ends in a simulated first PR.

## 3. The learner's core question

> **"Where does X live, and how do I change it the way this team would?"**

Every module in this flavor must bend toward that question. If a module doesn't help the learner locate things or internalize local conventions, it doesn't belong.

## 4. Module arc (menu)

**The six modules are prescriptive in order** — unlike the Vibe Coder flavor's adaptable menu. The arc is a ladder: each rung assumes the one below. Skipping ahead means the learner can't land the next rung.

| # | Module | Purpose | Why it matters for onboarding |
|---|---|---|---|
| 1 | **10-minute mental model** | One diagram + one paragraph: what the system does, what the major pieces are, and the shape of a request moving through them. | The learner needs a frame to hang every later detail on. Without it, module 3 becomes noise. |
| 2 | **Dev loop (setup, run, test)** | The exact commands to clone, install, run locally, run the tests, and reload on change. Plus the one or two tools that are non-obvious. | Environment setup is where most onboarding time is lost. Get them to "I can run the tests" before anything else. |
| 3 | **One end-to-end feature trace** | Pick one real feature. Walk it from HTTP entry (or CLI, or event) through handlers, services, storage, and back. Name every file as you go. | Depth on one feature beats a tour of twenty. It teaches *where things live* in a way no directory map can. |
| 4 | **Local conventions** | The team's unwritten rules: naming, error handling, folder layout, test placement, logging, config, DI. The stuff a reviewer will flag. | Code style in an unfamiliar codebase is about the team's taste, not the language. This module is where reviewer-rejection risk collapses. |
| 5 | **PR & review norms** | How a PR is opened here, what the description should contain, what reviewers look for first, and how fast review typically lands. | Polyglots know *how* to write a PR in general — they need the local protocol. |
| 6 | **Your first change** (see 4b) | A simulated first PR. **Not optional.** | This is the entire point of the flavor. Everything else exists to make this module succeed. |

**Key constraint:** modules 1–5 are *scaffolding for module 6*. If any earlier module drifts into "teach the framework" or "tour the org," cut it back. The course exists to deliver a successful first change.

### 4b. Must-have final module: "Your first change"

**This module is prescriptive, not optional.** An onboarding course without a simulated-first-PR module has failed — no matter how good modules 1–5 were. It is the difference between a course and a README.

The module walks the learner through a **realistic, concrete change request**. The change must be small enough to trace in one module but real enough that the files touched, tests added, and PR description feel like an actual team workflow.

**Example realistic change for this module** (the course writer picks one that fits the codebase):

> *Add an `avatar_url` field to the user profile response. It lives in the user service; the existing profile endpoint returns `id`, `name`, `email`. Your job: add the field to the database model, plumb it through the service layer, expose it on the API, and add a test for the new field.*

The module walks through that change in three parts:

1. **Which files you'd touch, in order.** A numbered walkthrough that names every real file. Not "the model layer" — the actual filename from the codebase. The order matters: usually data model → service → handler → test → docs. State the order *and* the reason for it.
2. **What tests you'd add.** Point at the closest existing test file, show its shape, and describe the new test case the learner would add. Call out any testing convention the team enforces (fixtures, table tests, snapshot tests, coverage thresholds, etc.).
3. **What the PR description would look like.** A short worked example of a PR description that matches the team's norms from module 5: title format, body sections (what/why/how), screenshots or logs if the team expects them, reviewer tagging, linked issue.

Structure this module in the HTML output as:

- An **opener** naming the change request verbatim.
- A **numbered step card** sequence for part 1 (the file walk).
- A **code block (Code ↔ Convention)** for part 2 showing the new test, with the right column giving the convention the test obeys.
- A **callout box** for part 3 with the draft PR description.
- A **quiz** asking the learner to re-order a shuffled list of files they'd touch for a *different* small change — tests whether they've internalized the walked path, not memorized this specific one.

Explicitly **do not** tell the learner to actually write the code. This is a trace, not homework. The point is to show them the path so that when the real first PR arrives, it feels familiar.

## 5. Code block style: "Code ↔ Convention"

**Left column:** real code, copied verbatim from the codebase (universal rule).

**Right column:** the team's **unwritten rule the code obeys**, expressed as a single short imperative.

The right column is **not** a line-by-line English translation of the code. It is **one rule, with the code as evidence of it**. If there's no rule to state, the code doesn't belong in a Code ↔ Convention block — use a plain code snippet or a diagram instead.

**Example entry 1:**

> **Code (left):**
> ```go
> if err != nil {
>     return fmt.Errorf("fetch user %s: %w", id, err)
> }
> ```
> **Convention (right):** *Errors are always wrapped with `fmt.Errorf` and a context prefix naming the operation. Never return a bare `err`. Never use `errors.New` inside a function that already has a wrapped error upstream.*

**Example entry 2:**

> **Code (left):**
> ```go
> func (h *UserHandler) GetProfile(ctx context.Context, req *GetProfileRequest) (*Profile, error) {
>     ...
> }
> ```
> **Convention (right):** *Handlers take `ctx context.Context` as the first parameter. Always. Even when the handler doesn't currently use it — the next person's retry/cancellation logic needs the seam.*

**Why this works for onboarding:** the polyglot already reads the code fluently. They don't need to be told what `fmt.Errorf` does. What they need is the team's standing decision about how to use it. That decision is what gets a PR approved or rejected.

## 6. Quiz style

**Test procedural fluency**, not language knowledge. The questions should probe whether the learner can *act inside this codebase*, not whether they can define a term.

**Example archetypes:**

- *"You need to add a new `/v2/users/:id/preferences` endpoint that returns a list of notification settings. In what order do you touch files, and what's the first test you write?"*
- *"A reviewer left this comment on a PR: 'this doesn't match how we do errors.' Which of these four code snippets is the reviewer most likely objecting to, and why?"*
- *"The team uses three logging helpers: `log.Info`, `log.Event`, and `log.Audit`. In which of the following situations would you use `log.Event`?"*

**Explicitly prohibited question archetypes:**

- **Syntax recall.** *"What is the correct syntax for a Go error-wrapping call?"* — NO. The polyglot knows the syntax or can look it up in 10 seconds.
- **Keyword definition.** *"What does the `defer` keyword do in Go?"* / *"What does the `async` keyword do in Python?"* — NO. Assume language basics.
- **Function return values.** *"What does `http.StatusOK` return?"* — NO. This is a trivia question, not a fluency test.
- **File name recall.** *"What's the exact path to the user service?"* — NO. Test *ordering and reasoning about files*, not memorization.

**Rule of thumb:** if a question could be answered by a fresh Stack Overflow search in under 30 seconds, it's the wrong question. Ask about things that require reading *this* codebase.

## 7. Metaphor strategy

**Sparing.** Use a metaphor only when you hit genuinely unfamiliar infrastructure — the kind of thing the polyglot may not have touched in their previous stack. Good candidates: message queues, event loops, reactive streams, actor systems, backpressure, sharding topologies.

**Never use metaphors for language or framework basics.** The audience already has closures, async, classes, generics, and dependency injection. A restaurant analogy for "what an async function does" insults their experience and wastes the text budget.

**No everyday-life metaphors.** No restaurants, bouncers, post offices, kitchens, libraries. The polyglot wants cross-stack analogies (*"the way this actor mailbox works is closer to a Python queue than a Go channel — here's why"*), not pedagogical imagery.

When you do use a metaphor, use it once, anchor the mental model, and drop it. Don't sustain the metaphor across a whole module.

## 8. Tooltip strategy

**Tooltip only these two categories:**

1. **The codebase's own jargon.** Internal service names, custom decorators, domain terms, project-coined abbreviations. Examples: `"UserMailer"`, `"the Dispatcher"`, `"Green Path"`, `"Tier-2 tenant"`. If a senior on the team would say the word without defining it, tooltip it.
2. **Stack-specific terminology unfamiliar to a polyglot.** When the target stack has vocabulary the learner's home stack does not, tooltip it at first use. Examples: Go's `context.Context`, Rust's `?` operator and lifetimes, React Server Components, Django's `F` expressions.

**Do not tooltip:**

- Standard language features (closures, async/await, classes, generics, interfaces, traits, decorators, lambdas). The audience has these.
- Common framework concepts (middleware, dependency injection, request handlers, ORMs). The audience has these too.
- Industry-standard acronyms (API, REST, CLI, HTTP, JSON, SQL, CRUD, TLS). Assume known.

**Acronym rule:** tooltip **project-coined** acronyms on first use (e.g., `"TPF — Tenant Policy Filter, our row-level ACL helper"`). Skip the standard ones.

**Tooltip density target:** noticeably lower than Vibe Coder flavor. If a Vibe Coder course tooltips 60 terms, an Onboarding course of the same length tooltips 15–20.

## 9. Voice & tone

**Pragmatic senior teammate.** The voice of the engineer sitting next to the new hire on day three saying: *"Here's what I wish I'd known week one."*

- **Welcoming, but not gushing.** The learner is a peer, not a student. Don't congratulate them for basic comprehension.
- **Direct.** No filler. If the convention is "wrap every error," say "wrap every error." Don't lead with a paragraph about the philosophy of error handling.
- **Occasionally dry.** Light, situational humor is welcome — *"Yes, this factory function is doing five things. I'm sorry. We're refactoring it."* Don't force jokes.
- **No handholding lectures.** Do not explain what a function is. Do not reintroduce concepts the audience learned in college.
- **Sentence length: medium.** Not Vibe Coder's punchy two-liners, not Pattern Learning's dense prose. A conventions section can run 4–6 sentences when the rule requires it.
- **Use "we" sparingly.** Using "we" for the team is fine when pointing at conventions (*"we don't use that helper in new code"*). Using "we" for the learner (*"let's explore…"*) is too soft — drop it.

## 10. Visual density target

**Balanced.** Not infographic-heavy (that's Vibe Coder), not prose-heavy (that's Pattern Learning). The target mix:

- **Diagrams** for the end-to-end feature trace (module 3) — **mandatory**. A sequence or call-graph diagram that shows the request crossing every file.
- **Numbered step cards** for the dev loop (module 2) and the PR workflow (modules 5 and 6). Step cards are the right shape for "do this, then this."
- **Prose** for local conventions (module 4). Conventions do not diagram well — they're rules, and rules read better as short lists and paragraphs than as icons in boxes.
- **Code blocks** (Code ↔ Convention format) throughout modules 3, 4, and 6.

The 2–3 sentence ceiling from `content-philosophy.md` is **relaxed** for conventions sections in module 4 — a single rule sometimes needs 4–6 sentences to explain its edge cases. The ceiling **still applies** to opening hooks, quiz explanations, and callout boxes.

## 11. "Why should I care?" framing per module

Every module ties back to the outcome: **"this is what you need to ship your first PR without breaking something."** The framing is never about "steering AI better" (that's Vibe Coder) and never about "learning how the system works for its own sake" (that's Deep Understanding). It is always about *shipping a competent first change*.

One-line framing the writing agent can adapt for each module:

1. **10-minute mental model** → *"Before you touch anything, you need a frame to hang the next ten thousand details on. Ten minutes here saves a week of confusion."*
2. **Dev loop** → *"You can't ship a PR you can't run. This is the five-minute setup that most new engineers spend a week on."*
3. **End-to-end feature trace** → *"This is the trip your own code will make. Once you've walked it once, you know where to put new things."*
4. **Local conventions** → *"These are the unwritten rules a reviewer will reject your PR over. They're not in the docs. They're here."*
5. **PR & review norms** → *"Your code might be right and your PR still bounces — because PR etiquette is local. Here's the local version."*
6. **Your first change** → *"A dry run of the real thing. When the actual first ticket lands, it should feel like a reread."*

## 12. Overrides to `content-philosophy.md`

This flavor modifies the shared base layer as follows.

**Replaces:**

- **"Code ↔ Plain English Translations" → "Code ↔ Convention".** The signature code block uses a single team rule in the right column, not a line-by-line English translation. See Section 5. This is the biggest departure from the Vibe Coder default and the core of the Onboarding flavor.

**Relaxes:**

- **"Be extremely aggressive with tooltips" → stack-and-jargon-only.** The aggressive-tooltipping rule is relaxed for language and framework basics. Tooltip codebase jargon and unfamiliar stack terms only. See Section 8.
- **"Max 2–3 sentences per text block" → relaxed in conventions sections.** Module 4 (Local Conventions) and convention callouts in other modules may exceed 2–3 sentences when a rule needs the edge cases spelled out. The ceiling still applies to hooks, quiz explanations, and callout boxes.
- **"Every screen must be at least 50% visual" → balanced.** Still visual, but prose-acceptable in conventions. See Section 10.
- **"Metaphors first, then reality" → sparing metaphors, reality-first.** Metaphors are used only for unfamiliar infrastructure and never for language basics. See Section 7.

**Keeps (universal rules, not overridden):**

- No recycled metaphors — even in sparing use, never default to restaurants, bouncers, or post offices.
- Original code only — every snippet is a verbatim copy from the real codebase.
- Quizzes test application, not memory (the definition of "application" for this flavor is *procedural fluency inside this codebase*).
- Show, don't tell — diagrams for flows, step cards for workflows, callouts for key moves.
- Interactive elements are mandatory — every module has at least one quiz; the course has at least one group chat animation and one data flow animation.
- Glossary tooltips never clip (technical rule from `../gotchas.md`).
- No horizontal scrollbars on code blocks.
- One concept per screen.

---

## Known pitfalls to avoid

Four failure modes show up every time someone writes an onboarding course without this playbook. Name them out loud so the writing agent refuses them:

- **Dumping org chart and history before the learner cares.** Who reports to whom, when the company was founded, the history of the rewrite from Java to Go — none of it helps the learner ship. If it belongs anywhere, it belongs in an appendix the learner reads in month two. Do not open a module with it. Do not close a module with it.
- **Teaching language or framework basics.** The polyglot already has closures, async, generics, and dependency injection. Every paragraph spent re-explaining them is a paragraph stolen from the team's actual conventions. Assume the language; teach the team.
- **Skipping test-writing conventions.** This is the most common silent failure. Teams have strong opinions about how tests are structured (fixtures, table tests, snapshots, mocking strategy, coverage thresholds). New engineers frequently ship code-correct PRs that get rejected for test-convention violations. Module 4 must cover tests; module 6 must add a test to the simulated change.
- **Modules that read like a README table of contents.** *"The `auth` directory handles authentication. The `db` directory handles the database. The `api` directory handles the API."* This is dead prose and teaches nothing. Prefer: pick one feature, trace it through those directories, and let the directory layout emerge from the walk.

---

## Pointers

- Interactive element HTML patterns: `../interactive-elements.md`
- Design tokens and visual language: `../design-system.md`
- Universal rules and overridable base rules: `../content-philosophy.md`
- Shared failure modes to avoid: `../gotchas.md`
