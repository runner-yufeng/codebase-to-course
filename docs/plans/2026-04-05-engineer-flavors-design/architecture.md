# Architecture: Engineer Flavors

## Current architecture (for reference)

```
codebase-to-course/
├── SKILL.md                         # Orchestrates: Phase 1 analysis → 2 curriculum → 2.5 briefs → 3 write → 4 review
└── references/
    ├── content-philosophy.md        # Content rules (vibe-coder tuned)
    ├── gotchas.md                   # Failure modes (vibe-coder tuned)
    ├── module-brief-template.md     # Brief template (vibe-coder tuned)
    ├── interactive-elements.md      # HTML/CSS patterns for quizzes, animations, etc.
    ├── design-system.md             # CSS tokens, colors, typography
    ├── styles.css                   # Verbatim-copied production CSS
    ├── main.js                      # Verbatim-copied production JS
    ├── _base.html                   # HTML shell template
    ├── _footer.html                 # Footer template
    └── build.sh                     # Assembles index.html from modules
```

Every content file is implicitly tuned to the vibe-coder audience.

## Target architecture

```
codebase-to-course/
├── SKILL.md                         # + Phase 0 flavor selection; delegates audience-specific rules to playbooks
└── references/
    ├── flavors/                     # NEW directory
    │   ├── vibe-coder.md            # NEW: vibe-coder playbook (existing behavior extracted)
    │   ├── onboarding.md            # NEW: polyglot-new-to-stack
    │   ├── pattern-learning.md      # NEW: mid-senior OSS study
    │   ├── architecture-review.md   # NEW: senior tradeoff analysis
    │   └── deep-understanding.md    # NEW: configurable generalist
    ├── content-philosophy.md        # MODIFIED: becomes shared base, overridable rules marked
    ├── gotchas.md                   # MODIFIED: adds per-flavor notes on tooltip + density gotchas
    ├── module-brief-template.md     # MODIFIED: adds `flavor:` field, per-flavor "why should I care?"
    ├── interactive-elements.md      # unchanged
    ├── design-system.md             # unchanged
    ├── styles.css                   # unchanged
    ├── main.js                      # unchanged
    ├── _base.html                   # unchanged
    ├── _footer.html                 # unchanged
    └── build.sh                     # unchanged
```

## SKILL.md changes

### New Phase 0: Flavor Selection

Inserted between the "First-Run Welcome" block (lines 10-22) and "Who This Is For" (line 25). Before any codebase analysis, the skill issues an `AskUserQuestion` with five options:

```
Question: "Who is this course for?"
Options:
  1. Vibe Coder — I'm learning without a CS background; I want to steer AI coding tools and understand code I didn't write myself.
  2. Onboarding — I'm an engineer joining this codebase; I want to ship my first PR without breaking things.
  3. Pattern Learning — I want to study this codebase and extract reusable techniques for my own work.
  4. Architecture Review — I'm evaluating this codebase's architecture and want to form an opinion about its tradeoffs.
  5. Deep Understanding — I want a thorough tour of how this system works, no specific use case.
```

The choice is persisted as a session variable (mental state only — no file writes). If the user picks "Other" and describes a goal, the skill maps it to the closest flavor or falls back to Deep Understanding with the user's goal noted.

**Only after Phase 0 does the skill read the matching `references/flavors/*.md` playbook.** From that point forward, every audience-dependent decision defers to the playbook.

### "Who This Is For" section (lines 25-39) → Replaced

The current single-audience paragraph becomes a one-sentence table:

```markdown
## Who This Is For

This skill generates courses for five audiences. You picked one in Phase 0; the matching playbook at `references/flavors/<flavor>.md` owns all audience-dependent content rules.

| Flavor | Learner | Playbook |
|---|---|---|
| Vibe Coder | Non-technical; uses AI coding tools | `references/flavors/vibe-coder.md` |
| Onboarding | Engineer new to this stack | `references/flavors/onboarding.md` |
| Pattern Learning | Engineer studying an OSS project | `references/flavors/pattern-learning.md` |
| Architecture Review | Senior engineer evaluating tradeoffs | `references/flavors/architecture-review.md` |
| Deep Understanding | Engineer wanting thorough comprehension | `references/flavors/deep-understanding.md` |
```

### "Why This Approach Works" (lines 41-49) → Moved to each playbook

Each flavor has its own "why this approach works" statement because the motivations differ. SKILL.md keeps a one-liner: *"Every flavor inverts traditional learning by meeting the learner where they already are — see your flavor's playbook for the specific framing."*

### Phase 2 "Curriculum Design" (lines 69-87) → Delegated

The current module-arc table (lines 75-83) is vibe-coder specific. It moves entirely out of SKILL.md. Phase 2 becomes:

```markdown
### Phase 2: Curriculum Design

Read `references/flavors/<your-flavor>.md` → "Module Arc" section. Each flavor provides a curated menu of 4-6 modules tuned to its audience's primary question. Pick the modules that best fit the codebase.

**The key principle (shared across flavors):** every module should connect back to the flavor's core learner goal. If a module doesn't help that specific learner take the specific next action they want, cut it or reframe it.

**Mandatory interactive elements (shared across all flavors):** Group Chat Animation, Message Flow / Data Flow Animation, Code block (per-flavor style — see your playbook), Quizzes, Glossary Tooltips. See `references/interactive-elements.md` for HTML patterns. Your playbook tells you the *content style* for each element.
```

### Phase 2.5 "Module Briefs" (lines 112-126) → Add flavor field

The brief template at `references/module-brief-template.md` gains a mandatory top field: `Flavor: <name>`. Writing agents use this to know which playbook to pull content rules from.

### Phase 3 "Write modules" (lines 128-192) → Add playbook to required reading

Sequential path reading list adds: *"`references/flavors/<your-flavor>.md`"*
Parallel path brief dispatch adds: *"each agent also receives `references/flavors/<flavor>.md`"*

## Playbook structure (shared template)

Every playbook under `references/flavors/` follows the same 10-section template so writing agents know where to look:

```markdown
# Flavor Playbook: <Flavor Name>

## 1. Audience snapshot
Who they are, what they know, what they don't, what they're optimizing for.

## 2. Why this approach works (for this audience)
The motivation / pedagogy behind teaching this audience by walking a real codebase.

## 3. The learner's core question
One sentence — the question the course must answer.

## 4. Module arc (menu)
4-6 curated module titles + what each teaches + why it matters for this audience. This REPLACES the vibe-coder arc from the old SKILL.md lines 75-83.

## 5. Code block style
How the signature "code + explanation" block is framed for this audience. Specifies both the left (code) and right (annotation) content rules.

## 6. Quiz style
What to test, what NOT to test, example question archetypes.

## 7. Metaphor strategy
Heavy / moderate / sparing / none. Which metaphor families are fair game; which are off-limits.

## 8. Tooltip strategy
What's worth tooltipping at first use; what's assumed known; acronym rules.

## 9. Voice & tone
Voice persona, sentence-length tolerance, how much humor is welcome.

## 10. Visual density target
Infographic / balanced / denser prose. Text-block length ceiling.

## 11. "Why should I care?" framing per module
One-line framings the writing agent can adapt per module.

## 12. Overrides to content-philosophy.md
Explicit list of base-layer rules this flavor relaxes, tightens, or replaces.
```

## Per-flavor summary matrix

This matrix is the single-page reference for per-flavor deltas. Full per-playbook content is in `best-practices.md`.

| Dimension | Vibe Coder | Onboarding | Pattern Learning | Architecture Review | Deep Understanding |
|---|---|---|---|---|---|
| **Core question** | "How does this thing I vibe-coded actually work under the hood?" | "Where does X live and how do I change it the way this team would?" | "What clever thing is this codebase doing that I can reuse?" | "Would I build it this way, and where will it hurt at scale?" | "How does this system actually work, end-to-end?" |
| **Ideal arc** | What the app does → actors → communication → outside world → clever tricks → when things break → big picture (current 7-module menu) | 10-min mental model → dev loop → end-to-end feature trace → local conventions → PR & review norms → your first change | One-line thesis → pattern 1 → pattern 2 → pattern 3 → how patterns compose → where they transfer | Architectural thesis & constraints → decision 1 + tradeoff → decision 2 + tradeoff → coupling & data flow critique → scalability pressure points → tech debt verdict | Problem the system solves → core abstractions → data & control flow → subsystem A → subsystem B → evolution & tradeoffs |
| **Code block style** | Code ↔ line-by-line plain English | Code ↔ convention (team's unwritten rule) | Code ↔ named pattern + "reuse when…" | Code ↔ ADR-style (Context / Decision / Consequence) | Code ↔ mental-model diagram |
| **Quiz style** | "Where would you add this feature?" / "Where would you debug this symptom?" | "You need to add endpoint X — which files, in what order?" | "Which problem would this pattern solve?" | "Here's a new requirement — which decision breaks first?" | "Trace the request. What invariant holds at step 3?" |
| **Metaphor strategy** | Heavy — everyday life metaphors for every concept | Sparing — only for unfamiliar infra | None to sparing — pattern names preferred over metaphors | None — precision beats imagery | Moderate — one metaphor per subsystem, then drop |
| **Tooltip strategy** | Ultra-aggressive (every term) | Codebase jargon + stack-specific terms; assume language/framework basics | Formal pattern names + OSS-specific jargon | Architectural vocabulary only when non-standard | Generous (audience is varied) |
| **Voice** | Smart friend, warm, no jargon | Pragmatic senior teammate, "here's what I wish I knew" | Sharp peer showing off a trick, "look what they did here" | Principled staff engineer with a thesis | Curious guide, layered reveal |
| **Visual density** | Infographic (50%+ visual, 2-3 sentence cap) | Balanced (diagrams for flows, prose for conventions) | Denser prose (trick lives in nuance) | Diagram-heavy (coupling graphs) + prose stance | Balanced (layered diagrams) |
| **Why should I care?** | Steer AI better, debug faster, make smarter architectural decisions | Ship first PR without breaking things | Steal reusable techniques | Form a defensible opinion | Curiosity / comprehension |

## Interactive-element variance

Every flavor includes the same element *types*; only content and annotation change:

| Element | Universal? | Per-flavor variance |
|---|---|---|
| Glossary tooltips | Yes | **Scope** (what's tooltipped) — see matrix row above |
| Code block (2-column) | Yes | **Right-column content** — see matrix row above |
| Multiple-choice quizzes | Yes | **Question archetype** — see matrix row above |
| Group chat animation | Yes (mandatory) | **Tone** — colloquial (vibe) → colleague-banter (engineer flavors) |
| Data flow animation | Yes (mandatory) | **Labels** — vibe: plain English; engineer: precise terms |
| Architecture diagram | Optional | More important for Architecture Review flavor |
| Drag-and-drop | Optional | Targets differ (vibe: "which file?"; pattern: "which pattern?") |
| "Spot the bug" | Optional | Architecture Review variant: "spot the tradeoff rationale" |
| Callout boxes | Yes | "Aha!" moments (vibe) vs "Tradeoff" / "Transfer" callouts (engineer) |

All HTML/CSS/JS patterns in `interactive-elements.md` stay unchanged — only the HTML content the writing agents produce varies.

## Changes to shared base files

### `content-philosophy.md`

Add a header banner after line 1:

> **This is the shared base layer.** Flavor playbooks under `references/flavors/` may override or tighten any rule marked `[overridable]` below. The unchanged rules are universal across all flavors.

Mark the following as `[overridable]`:
- "Max 2-3 sentences per text block" (overridable — Architecture Review and Pattern Learning allow longer blocks for tradeoff prose)
- "Every screen must be at least 50% visual" (overridable — Pattern Learning may go denser)
- "Every code snippet gets a side-by-side plain English translation" (overridable — all engineer flavors transform this block)
- "Be extremely aggressive with tooltips" (overridable — only Vibe Coder and Deep Understanding remain ultra-aggressive)
- "Metaphors first, then reality" (overridable — Architecture Review drops metaphors entirely)

Mark as universal (unchanged, non-overridable):
- No recycled metaphors
- No horizontal scrollbars on code
- Use original code exactly as-is
- One concept per screen
- Quizzes test application, not memory
- Glossary tooltips never clip (technical rule)

### `gotchas.md`

Add per-flavor notes to two gotchas:

**"Not Enough Tooltips"** gets a rider:
> *Flavor note:* Under-tooltipping is the #1 failure for Vibe Coder and Onboarding. For Pattern Learning it means missing pattern names. For Architecture Review, minimal tooltipping is correct — err *light*, not heavy. For Deep Understanding, err generous.

**"Walls of Text"** gets a rider:
> *Flavor note:* The 50%-visual rule is strict for Vibe Coder and Onboarding. Pattern Learning and Architecture Review may run denser prose when the idea requires it — the gotcha becomes "walls of text with no visual anchors at all," not "any text block longer than 3 sentences."

### `module-brief-template.md`

Add a new mandatory top field:

```markdown
**Flavor:** <vibe-coder | onboarding | pattern-learning | architecture-review | deep-understanding>
```

And a note that `Teaching Arc → "Why should I care?"` is dictated by the flavor playbook.

## Loading order (runtime)

When the skill runs:

1. **First-run welcome** (SKILL.md lines 10-22, unchanged)
2. **Phase 0: Flavor Selection** — new; reads nothing, just asks
3. **Read the selected flavor playbook** — `references/flavors/<flavor>.md` — before any analysis
4. **Phase 1: Codebase Analysis** — unchanged (always based on actual code)
5. **Phase 2: Curriculum Design** — consults playbook's Module Arc section
6. **Phase 2.5: Module Briefs** (complex codebases) — briefs reference the flavor
7. **Phase 3: Write Modules** — writing agents receive flavor playbook alongside existing references
8. **Phase 4: Review and Open** — unchanged

Context budget: the flavor playbook is loaded once in Phase 2 and kept in context through Phase 3 (sequential path) or distributed to sub-agents (parallel path).

## Backward compatibility

- All current trigger phrases still activate the skill.
- Vibe Coder flavor, when selected, produces output byte-identical to the current skill (modulo prose improvements). The `vibe-coder.md` playbook is extracted verbatim from the current SKILL.md content.
- The current "First-Run Welcome" text is preserved.
- The directory-based output structure is identical across flavors.
- `build.sh`, `styles.css`, `main.js`, `_base.html`, `_footer.html` — zero changes.
