---
name: codebase-to-course
description: "Turn any codebase into a beautiful, interactive single-page HTML course that teaches how the code works. Supports five audience flavors — non-technical vibe coders, engineers onboarding to a new codebase, engineers studying OSS projects for reusable patterns, senior engineers doing architecture reviews, and engineers wanting deep end-to-end understanding. Asks the user to pick a flavor before building. Use this skill whenever someone wants to create an interactive course, tutorial, or educational walkthrough from a codebase or project. Also trigger when users mention 'turn this into a course,' 'explain this codebase interactively,' 'teach this code,' 'interactive tutorial from code,' 'codebase walkthrough,' 'learn from this codebase,' 'make a course from this project,' 'onboard me to this repo,' 'architectural review of this codebase,' or 'learn the patterns in this project.' This skill produces a stunning, self-contained HTML file with scroll-based navigation, animated visualizations, embedded quizzes, and flavor-specific code explanation blocks."
---

# Codebase-to-Course

Transform any codebase into a stunning, interactive course. The output is a **directory** containing a pre-built `styles.css`, `main.js`, per-module HTML files, and an assembled `index.html` — open it directly in the browser with no setup required (only external dependency: Google Fonts CDN). The course teaches how the code works through scroll-based modules, animated visualizations, embedded quizzes, and plain-English translations of code.

## First-Run Welcome

When the skill is first triggered and the user hasn't specified a codebase yet, introduce yourself and explain what you do:

> **I can turn any codebase into an interactive course that teaches how it works — no coding knowledge required.**
>
> Just point me at a project:
> - **A local folder** — e.g., "turn ./my-project into a course"
> - **A GitHub link** — e.g., "make a course from https://github.com/user/repo"
> - **The current project** — if you're already in a codebase, just say "turn this into a course"
>
> I'll read through the code, figure out how everything fits together, and generate a beautiful single-page HTML course with animated diagrams, plain-English code explanations, and interactive quizzes. The whole thing runs in your browser — no setup needed.

If the user provides a GitHub link, clone the repo first (`git clone <url> /tmp/<repo-name>`) before starting the analysis. If they say "this codebase" or similar, use the current working directory.

## Phase 0: Flavor Selection

**Before any codebase analysis**, ask the user to pick an audience "flavor." This is mandatory on first run — never guess from trigger phrases, never default. Different audiences need fundamentally different courses, and getting this wrong means building for the wrong learner.

Call the `AskUserQuestion` tool with exactly these five options:

1. **Vibe Coder** — *"I'm learning without a CS background; I want to steer AI coding tools and understand code I didn't write myself."*
2. **Onboarding** — *"I'm an engineer joining this codebase; I want to ship my first PR without breaking things."*
3. **Pattern Learning** — *"I want to study this codebase and extract reusable techniques for my own work."*
4. **Architecture Review** — *"I'm evaluating this codebase's architecture and want to form an opinion about its tradeoffs."*
5. **Deep Understanding** — *"I want a thorough tour of how this system works, no specific use case."*

After the user picks, **immediately read the matching playbook** at `references/flavors/<flavor>.md` and hold it in context for the rest of the session. From Phase 1 forward, every audience-dependent decision (module arc, code block style, quiz style, metaphor strategy, tooltip strategy, voice, visual density, "why should I care?" framing) defers to that playbook. The playbook is the source of truth for audience-specific rules; `references/content-philosophy.md` is the shared base layer with rules marked `[overridable]` that the playbook may tighten or replace.

**"Other" fallback.** If the user picks "Other" in the AskUserQuestion and describes a goal in free text, map it to the closest flavor by keyword:
- "contributing" / "new to" / "joining" / "first PR" / "ramp up" → **Onboarding**
- "evaluate" / "review" / "tradeoff" / "scale" / "architecture" → **Architecture Review**
- "how does it work" / "internals" / "tour" / "understand" / "end-to-end" → **Deep Understanding**
- "clever" / "patterns" / "techniques" / "steal" / "learn from" / "study" → **Pattern Learning**
- "non-technical" / "no coding background" / "vibe" → **Vibe Coder**

If the mapping is ambiguous, fall back to **Deep Understanding** and announce the fallback: *"I'll use the Deep Understanding flavor since your goal doesn't fit cleanly into the specialized flavors."* Preserve the user's free-text goal verbatim and weave it into the "why should I care?" framing of every module.

**Do NOT begin codebase analysis (Phase 1) until the user has picked a flavor and you have read the matching playbook.**

## Who This Is For

This skill generates courses for five audiences. The user picked one in Phase 0; the matching playbook at `references/flavors/<flavor>.md` owns all audience-dependent content rules. All rules below that reference a single audience have been moved into the playbooks.

| Flavor | Learner | Playbook |
|---|---|---|
| Vibe Coder | Non-technical builder using AI coding tools | `references/flavors/vibe-coder.md` |
| Onboarding | Engineer new to this stack, shipping first PR | `references/flavors/onboarding.md` |
| Pattern Learning | Engineer studying an OSS project for reusable techniques | `references/flavors/pattern-learning.md` |
| Architecture Review | Senior engineer evaluating architectural tradeoffs | `references/flavors/architecture-review.md` |
| Deep Understanding | Engineer wanting thorough end-to-end comprehension | `references/flavors/deep-understanding.md` |

## Why This Approach Works

Every flavor inverts traditional learning by meeting the learner where they already are. See your selected flavor's playbook (Section 2) for the specific framing — what motivates this audience, what they already know, and how tracing real code in the course gives them leverage. The directory-based output (separating CSS/JS from content) is intentional across all flavors: AI never regenerates boilerplate, each module is written independently to keep output size small and quality high, and the assembled `index.html` works offline with zero setup.

---

## The Process

### Phase 1: Codebase Analysis

Before writing course HTML, deeply understand the codebase. Read all the key files, trace the data flows, identify the "cast of characters" (main components/modules), and map how they communicate. Thoroughness here pays off — the more you understand, the better the course.

**What to extract:**
- The main "actors" (components, services, modules) and their responsibilities
- The primary user journey (what happens when someone uses the app end-to-end)
- Key APIs, data flows, and communication patterns
- Clever engineering patterns (caching, lazy loading, error handling, etc.)
- Real bugs or gotchas (if visible in git history or comments)
- The tech stack and why each piece was chosen

**Figure out what the app does yourself** by reading the README, the main entry points, and the UI code. Don't ask the user to explain the product — they may not be familiar with it either. The course should open by explaining what the app does in plain language (a brief "here's what this thing does and why it's interesting") before diving into how it works. The first module should start with a concrete user action — "imagine you paste a YouTube URL and click Analyze — here's what happens under the hood."

### Phase 2: Curriculum Design

**Read your flavor's playbook first** — `references/flavors/<your-flavor>.md` → Section 4 "Module Arc." Each flavor provides its own curated module menu, tuned to its audience's core question. The Vibe Coder playbook holds the original 7-module menu; Onboarding, Pattern Learning, Architecture Review, and Deep Understanding each have their own 4-6 module arcs. Pick the modules that best fit the codebase.

**Shared principles across all flavors:**
- Structure the course as **4-6 modules**. Only go higher if the codebase genuinely has that many distinct concepts worth teaching. Fewer, better modules beat more, thinner ones.
- The arc starts from what the learner already knows and progressively peels back layers. The *specific* starting point depends on the flavor — user-facing behavior for Vibe Coder, the architectural thesis for Architecture Review, a one-line codebase thesis for Pattern Learning, etc. Your playbook tells you.
- Every module should connect back to the flavor's core learner goal. If a module doesn't help that specific learner take the specific next action they want, cut it or reframe it.
- This is a **menu, not a checklist** — adapt the arc to the codebase's complexity.

**Each module should contain:**
- 3-6 screens (sub-sections that flow within the module)
- At least one code block in the flavor-specific style (see your playbook Section 5 — Code ↔ English / Convention / Pattern name / ADR-style / Mental model)
- At least one interactive element (quiz, visualization, or animation)
- One or two callout boxes with insights (framing varies per flavor — "aha!" callouts for Vibe Coder, "Transfer" callouts for Pattern Learning, "Verdict" callouts for Architecture Review, etc.)
- A metaphor where the flavor allows it (see Section 7 of your playbook — Vibe Coder uses heavy metaphors, Onboarding and Pattern Learning use them sparingly, Architecture Review forbids them entirely, Deep Understanding uses moderate metaphors). The universal rule: **NEVER** reuse the same metaphor across modules and **NEVER** default to "restaurant."

**Mandatory interactive elements (every course, every flavor must include ALL of these):**
- **Group Chat Animation** — at least one across the course. iMessage/WeChat-style conversations between components. Tone varies per flavor (colloquial for Vibe Coder, colleague-banter for engineer flavors), but the element itself is universal.
- **Message Flow / Data Flow Animation** — at least one across the course. The step-by-step packet animation between actors. Labels vary per flavor (plain English for Vibe Coder, precise terms for engineer flavors).
- **Code blocks** — at least one per module, in the **flavor-specific style** (see your playbook Section 5). The CSS/JS patterns in `references/interactive-elements.md` are shared across flavors; only the right-column content changes.
- **Quizzes** — at least one per module, in the **flavor-specific style** (see your playbook Section 6 — scenario for Vibe Coder, procedural-fluency for Onboarding, transfer tests for Pattern Learning, critical-judgment for Architecture Review, comprehension-tracing for Deep Understanding).
- **Glossary Tooltips** — on every technical term on first use per module. **Scope varies per flavor** (ultra-aggressive for Vibe Coder, stack-specific for Onboarding, pattern-names for Pattern Learning, stingy for Architecture Review, generous for Deep Understanding). See your playbook Section 8.

These five element types are the backbone of every course in every flavor. Other interactive elements (architecture diagrams, layer toggles, pattern cards, etc.) are optional and should be added when they fit. But the five above must ALWAYS be present — no exceptions.

**Do NOT present the curriculum for approval — just build it.** The user wants a course, not a planning document. Design the curriculum internally, then go straight to building. If they want changes, they'll tell you after seeing the result.

**After designing the curriculum, decide which build path to use:**

- **Simple codebase** (single-purpose CLI, small web app, library, one clear entry point, 5 or fewer modules) → go directly to Phase 3 Sequential.
- **Complex codebase** (full-stack app, multiple services, content-heavy site, monorepo, or 6+ modules) → go to Phase 2.5 first, then Phase 3 Parallel.

### Phase 2.5: Module Briefs (complex codebases only)

For complex codebases, write a brief for each module before writing any HTML. This is the critical step that enables parallel writing — each brief gives an agent everything it needs without re-reading the codebase.

Read `references/module-brief-template.md` for the template structure. Read `references/content-philosophy.md` for the shared base rules and your selected playbook at `references/flavors/<flavor>.md` for the flavor-specific rules that should guide brief writing.

**For each module, write a brief to `course-name/briefs/0N-slug.md` containing:**
- **`Flavor:` field at the top** (matches the flavor picked in Phase 0) — writing agents use this to know which playbook to read
- Teaching arc (metaphor, opening hook, key insight — note that metaphor policy and "why should I care?" framing vary per flavor)
- Pre-extracted code snippets (copy-pasted from the codebase with file paths and line numbers)
- Interactive elements checklist with enough detail to build them (including which code-block style to use — per your flavor's Section 5)
- Which sections of which reference files the writing agent needs
- What the previous and next modules cover (for transitions)

The code snippets are the critical token-saving step. By pre-extracting them into the brief, writing agents never need to read the codebase at all.

### Phase 3: Build the Course

The course output is a **directory**, not a single file. All CSS and JS are pre-built reference files — never regenerate them. Your job is to write only the HTML content.

**Output structure:**
```
course-name/
  styles.css       ← copied verbatim from references/styles.css
  main.js          ← copied verbatim from references/main.js
  _base.html       ← customized shell (title, accent color, nav dots)
  _footer.html     ← copied verbatim from references/_footer.html
  build.sh         ← copied verbatim from references/build.sh
  briefs/          ← module briefs (complex codebases only, can delete after build)
  modules/
    01-intro.html
    02-actors.html
    ...
  index.html       ← assembled by build.sh (do not write manually)
```

**Step 1 (both paths): Setup** — Create the course directory. Copy these four files verbatim using Read + Write (do not regenerate their contents):
- `references/styles.css` → `course-name/styles.css`
- `references/main.js` → `course-name/main.js`
- `references/_footer.html` → `course-name/_footer.html`
- `references/build.sh` → `course-name/build.sh`

**Step 2 (both paths): Customize `_base.html`** — Read `references/_base.html`, then write it to `course-name/_base.html` with exactly three substitutions:
- Both instances of `COURSE_TITLE` → the actual course title
- The four `ACCENT_*` placeholders → the chosen accent color values (pick one palette from the comments in `_base.html`)
- `NAV_DOTS` → one `<button class="nav-dot" ...>` per module

**Step 3: Write modules** — This is where the paths diverge.

#### Sequential path (simple codebases)

Read `references/flavors/<your-flavor>.md`, `references/content-philosophy.md`, and `references/gotchas.md`. Then write modules one at a time. For each module, write `course-name/modules/0N-slug.html` containing only the `<section class="module" id="module-N">` block and its contents. Do not include `<html>`, `<head>`, `<body>`, `<style>`, or `<script>` tags.

Read `references/interactive-elements.md` for HTML patterns for each interactive element type. Read `references/design-system.md` for visual conventions.

#### Parallel path (complex codebases)

Dispatch modules to subagents in batches of up to 3. Each agent receives:
- Its module brief (from `course-name/briefs/`) — brief's `Flavor:` field tells the agent which playbook is active
- `references/flavors/<flavor>.md` — the selected flavor's playbook (audience-specific content rules)
- `references/content-philosophy.md` and `references/gotchas.md` — shared base layer
- Only the sections of `references/interactive-elements.md` and `references/design-system.md` listed in the brief

Each agent writes its module file(s) to `course-name/modules/`. Short modules (3 screens, one quiz) can be paired — two briefs given to one agent.

**What agents do NOT receive:** the full codebase (snippets are in the brief), SKILL.md, other modules' briefs, **playbooks for other flavors**, or unneeded reference file sections.

After all agents finish, do a quick consistency check in the main context: nav dots match modules, transitions between modules are coherent, no obvious tone shifts.

**Step 4 (both paths): Assemble** — Run `build.sh` from the course directory:
```bash
cd course-name && bash build.sh
```
This produces `index.html`. Open it in the browser.

**Critical rules:**
- **Never regenerate** `styles.css` or `main.js` — always copy from references
- Module files contain only `<section>` content — no boilerplate
- Use CSS `scroll-snap-type: y proximity` (NOT `mandatory`)
- Use `min-height: 100dvh` with `100vh` fallback on `.module`
- Interactive element JS is in `main.js`; wire up via `data-*` attributes and CSS class names as shown in `references/interactive-elements.md`
- Chat containers need `id` attributes; flow animations need `data-steps='[...]'` JSON on `.flow-animation`

### Phase 4: Review and Open

After running `build.sh`, open `index.html` in the browser. Walk the user through what was built and ask for feedback on content, design, and interactivity.

---

## Design Identity

The visual design should feel like a **beautiful developer notebook** — warm, inviting, and distinctive. Read `references/design-system.md` for the full token system, but here are the non-negotiable principles:

- **Warm palette**: Off-white backgrounds (like aged paper), warm grays, NO cold whites or blues
- **Bold accent**: One confident accent color (vermillion, coral, teal — NOT purple gradients)
- **Distinctive typography**: Display font with personality for headings (Bricolage Grotesque, or similar bold geometric face — NEVER Inter, Roboto, Arial, or Space Grotesk). Clean sans-serif for body (DM Sans or similar). JetBrains Mono for code.
- **Generous whitespace**: Modules breathe. Max 3-4 short paragraphs per screen.
- **Alternating backgrounds**: Even/odd modules alternate between two warm background tones for visual rhythm
- **Dark code blocks**: IDE-style with Catppuccin-inspired syntax highlighting on deep indigo-charcoal (#1E1E2E)
- **Depth without harshness**: Subtle warm shadows, never black drop shadows

---

## Reference Files

The `references/` directory contains detailed specs. **Read them only when you reach the relevant phase** — not upfront. This keeps context lean.

- **`references/flavors/<flavor>.md`** — Audience-specific playbook for the flavor picked in Phase 0 (one of `vibe-coder.md`, `onboarding.md`, `pattern-learning.md`, `architecture-review.md`, `deep-understanding.md`). Owns the module arc, code block style, quiz style, metaphor/tooltip strategy, voice, visual density, and "why should I care?" framing for your audience. Read during Phase 0 (immediately after the user picks), Phase 2 (curriculum design), Phase 2.5 (briefs), and Phase 3 (module writing). **Read only the playbook matching the selected flavor — not the others.**
- **`references/content-philosophy.md`** — Shared base layer: visual density rules, metaphor guidelines, quiz design, tooltip rules, code translation guidance. Rules marked `[overridable]` may be tightened or replaced by the selected flavor playbook; rules marked `[universal]` apply unchanged across all flavors. Read during Phase 2.5 (briefs) and Phase 3 (writing modules).
- **`references/gotchas.md`** — Common failure points checklist. Includes per-flavor notes on tooltip aggressiveness and visual density. Read during Phase 3 and Phase 4 (review).
- **`references/module-brief-template.md`** — Template for Phase 2.5 module briefs. Includes the mandatory `Flavor:` field. Read only for complex codebases using the parallel path.
- **`references/design-system.md`** — Complete CSS custom properties, color palette, typography scale, spacing system, shadows, animations, scrollbar styling. Unchanged across all flavors. Read during Phase 3 when writing module HTML.
- **`references/interactive-elements.md`** — Implementation patterns for every interactive element: drag-and-drop quizzes, multiple-choice quizzes, code↔English translations, group chat animations, message flow visualizations, architecture diagrams, pattern cards, callout boxes. CSS/JS/HTML patterns are shared across all flavors; only the *content* inside the elements varies per flavor (see your playbook). Read the relevant sections during Phase 3.
