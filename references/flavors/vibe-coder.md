# Flavor Playbook: Vibe Coder

> **When to read this:** After Phase 0 flavor selection, once the user has picked "Vibe Coder." This playbook owns every audience-dependent decision for this flavor. The shared base layer at `references/content-philosophy.md` still applies for universal rules (no recycled metaphors, original code only, no horizontal scrollbars, one concept per screen, quizzes test application not memory, glossary tooltips never clip).

## 1. Audience snapshot

The learner is a **"vibe coder"** — someone who builds software by instructing AI coding tools in natural language, without a traditional CS education. They may have built the project themselves (without looking at the code), or they may have found an interesting open-source project on GitHub and want to understand how it's built. Either way, they don't yet understand what's happening under the hood.

**Assume zero technical background.** Every CS concept — from variables to APIs to databases — must be explained in plain language as if the learner has never encountered it. No jargon without definition. No "as you probably know."

**Their goals are practical, not academic:**
- Have enough technical knowledge to effectively **steer AI coding tools** — make better architectural and tech stack decisions.
- **Detect when AI is wrong** — spot hallucinations, catch bad patterns, know when something smells off.
- **Intervene when AI gets stuck** — break out of bug loops, debug issues, unblock themselves.
- Build more advanced software with **production-level quality and reliability**.
- Be **technically fluent** enough to discuss decisions with engineers confidently.
- **Acquire the vocabulary of software** — learn precise technical terms so they can describe requirements clearly and unambiguously to AI coding agents (e.g., knowing to say "namespace package" instead of "shared folder thing").

**They are NOT trying to become software engineers.** They want coding as a superpower that amplifies what they're already good at. They don't need to write code from scratch — they need to *read* it, *understand* it, and *direct* it.

## 2. Why this approach works (for this audience)

This flavor inverts traditional CS education. The old model is: memorize concepts for years → eventually build something → finally see the point (most people quit before step 3). This model is: **build something first → experience it working → now understand how it works.**

The learner already has context that traditional students don't — they've *used* the app, they know what it does, they may have even described its features in natural language. The course meets them where they are: "You know that button you click? Here's what happens under the hood when you click it."

Every module answers **"why should I care?"** before "how does it work?" The answer to "why should I care?" is always practical: *because this knowledge helps you steer AI better, debug faster, or make smarter architectural decisions.*

## 3. The learner's core question

> **"How does this thing I vibe-coded actually work under the hood?"**

Every module must connect back to answering some part of this question in a way the learner can act on.

## 4. Module arc (menu)

Structure the course as **4-6 modules** (up to 7-8 only if the codebase genuinely has that many distinct concepts worth teaching). Fewer, better modules beat more, thinner ones. The arc always starts from what the learner already knows (the user-facing behavior) and moves toward what they don't (the code underneath). Think of it as zooming in: start wide with the experience, then progressively peel back layers.

| Module Position | Purpose | Why it matters for a vibe coder |
|---|---|---|
| 1 | "Here's what this app does — and what happens when you use it" | Start with the product (what it does, why it's interesting), then trace a core user action into the code. Grounds everything in something concrete. |
| 2 | Meet the actors | Know which components exist so you can tell AI "put this logic in X, not Y" |
| 3 | How the pieces talk | Understand data flow so you can debug "it's not showing up" problems |
| 4 | The outside world (APIs, databases) | Know what's external so you can evaluate costs, rate limits, and failure modes |
| 5 | The clever tricks | Learn patterns (caching, chunking, error handling) so you can request them from AI |
| 6 | When things break | Build debugging intuition so you can escape AI bug loops |
| 7 | The big picture | See the full architecture so you can make better decisions about what to build next |

**This is a menu, not a checklist.** Pick the modules that serve the codebase — a simple CLI tool needs 4, not 7. Adapt the arc to the codebase's complexity. Every module should connect back to a practical skill — steering AI, debugging, making decisions. If a module doesn't help the learner DO something better, cut it or reframe it until it does.

## 5. Code block style

**Line-by-line Code ↔ Plain English translations.** Every code snippet gets a side-by-side plain English translation. Left panel: real code from the project with syntax highlighting. Right panel: line-by-line plain English explaining what each line does. This is the single most valuable teaching tool for non-technical learners.

- The right-column annotation is **plain English**, not pattern names or ADR-style prose — describe what the line *does* in the kind of words a smart friend would use at a coffee shop.
- Translation coverage is **every line that runs**, not just the "interesting" ones. A non-technical learner can't tell which lines matter until they've been walked through all of them.
- See `references/interactive-elements.md` for the two-column HTML pattern; see `references/content-philosophy.md` "Code ↔ English Translations" for the shared rules around horizontal scrollbars and original-code preservation.

## 6. Quiz style

**"Where would you look / where would you add" scenario quizzes.** Test whether the learner can use their knowledge to take an action, not whether they can regurgitate definitions. Question archetypes, in order of value:

1. **"What would you do?" scenarios** — e.g., "You want to add a 'save to favorites' feature. Which files would you need to change?" This is the gold standard.
2. **Debugging scenarios** — "A user reports X is broken. Based on what you learned, where would you look first?" Tests whether they understood the architecture.
3. **Architecture decisions** — "You're building a similar app from scratch. Would you put this logic in the frontend or backend? Why?" Tests whether they understood the *reasoning* behind design choices.
4. **Tracing exercises** — "When a user does X, trace the path the data takes."

**What NOT to quiz:** definitions (that's what tooltips are for), file-name recall, syntax details, or anything answerable by scrolling up.

**Quiz tone:** Wrong answers get encouraging, non-judgmental explanations ("Not quite — here's why..."). Correct answers get brief reinforcement of the underlying principle ("Exactly! This works because..."). Never punitive, never score-focused — the quiz is a thinking exercise, not an exam. One quiz per module at the end, 3-5 questions each.

## 7. Metaphor strategy

**Heavy — everyday-life metaphors for every new concept.** Introduce every new idea with a metaphor from everyday life, then immediately ground it: "In our code, this looks like..." The metaphor builds intuition; the code grounds it in reality.

- A database is a library with a card catalog. Auth is a bouncer checking IDs. An event loop is an air traffic controller. Message passing is a postal system. API rate limiting is a nightclub with a capacity limit.
- Pick the metaphor that makes the concept click for a non-technical reader, not the one that's easiest to reach for.
- The no-recycled-metaphors rule (no "restaurant" crutch, no reusing a metaphor across modules) is universal and lives in `references/content-philosophy.md` — it applies here as written.

## 8. Tooltip strategy

**Ultra-aggressive — every technical term, first use per module.** If there is even a 1% chance a non-technical person doesn't know a word, tooltip it. Under-tooltipping is the #1 failure mode for this flavor (see `references/gotchas.md` → "Not Enough Tooltips").

Tooltip scope includes:
- **Software names** the learner might not know (Blender, GIMP, Audacity, etc.).
- **Everyday developer terms** (REPL, JSON, flag, CLI, API, SDK, etc.).
- **Programming concepts** (function, variable, dictionary, class, module, etc.).
- **Infrastructure terms** (PATH, pip, namespace, entry point, etc.).
- **Acronyms** — always tooltipped on first use, no exceptions.

**The vocabulary IS the learning.** One of the key goals is for learners to acquire the precise technical vocabulary they need to communicate with AI coding agents. Each tooltip should teach the term in a way that helps the learner USE it in their own instructions — e.g., "A **flag** is an option you add to a command to change its behavior — like adding '--json' to get structured data instead of plain text. When talking to AI, you'd say 'add a flag for verbose output.'"

**Rule of thumb:** if a term wouldn't appear in everyday conversation with a non-technical friend, tooltip it. Err heavily on the side of too many. The only exception is terms the user already knows well from their own domain (e.g., AI/ML concepts for someone already in AI).

Use `cursor: pointer` on tooltipped terms (not `cursor: help`) — a pointer feels clickable and inviting; the question-mark cursor feels clinical.

## 9. Voice & tone

**Smart friend explaining things, not a professor lecturing.** Warm, inviting, jargon-free. The learner should feel like they're hanging out with someone who knows this stuff and is excited to share it, not sitting in a lecture hall.

- Use humor where natural, never forced.
- Give components personality — they're "characters" in a story, not abstract boxes on a diagram.
- Use "aha!" callout boxes for universal CS insights the learner can carry to other codebases.
- Sentence length should stay short. If a sentence feels dense, break it in half.

## 10. Visual density target

**Infographic — at least 50% visual, 2-3 sentence text cap.** The course should feel closer to an infographic than a textbook.

- Max **2-3 sentences** per text block. If you're writing a fourth sentence, stop and convert it into a visual instead.
- No text block should ever be wider than the content width AND taller than ~4 lines. If it is, break it up with a visual element.
- Every screen must be **at least 50% visual** (diagrams, code blocks, cards, animations, badges — anything that isn't a paragraph).
- Every module should have at least one "hero visual" — a diagram, animation, or interactive element that dominates the screen and teaches the core concept at a glance.

**Convert text to visuals by default:**
- A list of 3+ items → cards with icons.
- A sequence of steps → flow diagram with arrows or numbered step cards.
- "Component A talks to Component B" → animated data flow or group chat visualization.
- "This file does X, that file does Y" → visual file tree with annotations or icon + one-liner badges.
- Explaining what code does → code ↔ English translation block (not a paragraph *about* the code).
- Comparing two approaches → side-by-side columns with visual contrast.

Use generous spacing between elements (`--space-8` to `--space-12` between sections); alternate full-width visuals with narrow text blocks for rhythm.

## 11. "Why should I care?" framing per module

Every module opens with a practical answer to "why should I care?" The answer is always one of:

- **Steer AI better** — knowing this lets you give sharper instructions to AI coding tools.
- **Debug faster** — knowing this helps you spot where a bug must live, or break out of an AI bug loop.
- **Make smarter architectural decisions** — knowing this helps you evaluate tradeoffs when choosing a stack, a library, or a data model.
- **Acquire vocabulary** — knowing the precise term for this thing lets you describe it to an AI agent without hand-waving.

Adapt one of these framings to every module. If a module can't answer "why should I care?" in these terms, cut it or reframe it until it can.

## 12. Overrides to content-philosophy.md

**No overrides — vibe coder is the baseline audience the base layer was originally written for.** Every rule in `references/content-philosophy.md` applies verbatim, including the overridable ones (2-3 sentence cap, 50% visual minimum, line-by-line code translations, aggressive tooltipping, metaphors-first). The playbook above restates the vibe-coder-specific *settings* of those rules but does not relax or tighten any of them relative to the base.
