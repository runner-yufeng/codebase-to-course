# Design: Engineer Flavors for codebase-to-course

**Date:** 2026-04-05
**Author:** brainstorming session (yufeng + Claude)
**Status:** Design complete, ready for implementation planning

## Context

The `codebase-to-course` skill currently has a single, sharply-tuned audience: the **"vibe coder"** — someone who ships software by instructing AI coding tools in natural language, with no formal CS background. Every content rule (aggressive glossary tooltips, line-by-line "Code ↔ Plain English" translations, restaurant-avoidance, "why should I care = steer AI better", 2-3 sentence text caps) follows from that single audience assumption.

The request: **make the skill also serve software engineers**, while keeping the vibe-coder experience intact for the users who already rely on it.

Naively rewriting SKILL.md for engineers would destroy the vibe-coder experience. Adding a few "if engineer..." asides would bloat SKILL.md and drift as content evolves. We need a first-class multi-audience architecture.

## Requirements

### Functional

1. **Five selectable flavors**, none of them a silent default:
   - **Vibe Coder** (existing, preserved verbatim)
   - **Onboarding** — polyglot engineer new to the stack
   - **Pattern Learning** — mid-to-senior studying an OSS project
   - **Architecture Review** — senior forming a stance on tradeoffs
   - **Deep Understanding** — generic engineer, no specific use case
2. **Mandatory first-run flavor prompt.** When the skill activates, it asks the user to pick a flavor via `AskUserQuestion` *before* any codebase analysis. No flavor guess from trigger phrases — always ask.
3. **Per-flavor content rules.** Each flavor owns: module arc, code-block style, quiz style, metaphor strategy, tooltip strategy, voice/tone, visual density, and the "why should I care?" framing.
4. **Shared interactive-elements backbone.** Quizzes, group chat animations, data flow animations, code blocks, and glossary tooltips exist in every flavor. Only their *content and annotation style* vary.
5. **Shared build pipeline.** The directory-based output, `styles.css`, `main.js`, `build.sh`, design system, and HTML skeletons are identical across flavors. Flavors only influence the HTML that the writing agents generate.
6. **Backward compatibility.** Every trigger phrase that works today still activates the skill. Vibe Coder must produce output indistinguishable from the current skill when selected.

### Non-functional

- **Progressive disclosure preserved.** SKILL.md must stay lean (~200-250 lines, similar to today). Flavor-specific rules live in `references/flavors/*.md` and are read only *after* the user picks.
- **Parallel-build path stays intact.** Phase 2.5 module briefs and Phase 3 parallel writing work identically for all flavors; briefs gain a `flavor:` field and point to the flavor playbook.
- **Additive, not destructive.** No file is deleted; the vibe-coder rules move into `references/flavors/vibe-coder.md` as-is and the existing `references/content-philosophy.md` + `references/gotchas.md` become the *shared base layer* with flavor-specific overrides.

## Rationale (summary)

Three candidate architectures were evaluated:

| Option | Verdict | Why |
|---|---|---|
| **Flavor Playbooks** (chosen) — `references/flavors/*.md`, one file per flavor, SKILL.md orchestrates | ✅ | Matches the existing progressive-disclosure pattern. SKILL.md stays lean. Each playbook is self-contained so parallel writing agents receive one file instead of composing base+deltas. Adding a sixth flavor = one new file. |
| **Inline branching** — all per-flavor rules in SKILL.md with `if FLAVOR=...` blocks | ❌ | Reverses commit `ea24c5e` ("slim SKILL.md"). SKILL.md would balloon past 30K chars. Hard to scan, easy to introduce branching bugs. |
| **Thin delta tables** — base SKILL.md + tiny override tables per flavor | ❌ | DRY, but writing agents must mentally merge base + delta at every decision point. Error-prone. Fuller playbooks cost more disk but are dramatically cheaper to reason about. |

See `architecture.md` for the structural design and `best-practices.md` for the per-flavor content rules backed by external research.

## Detailed Design (summary)

The skill gains a **Phase 0: Flavor Selection** before the current Phase 1 codebase analysis. Phase 0 calls `AskUserQuestion` with 5 options and stores the chosen flavor as a session variable. Every subsequent phase that currently references vibe-coder assumptions now delegates to the corresponding playbook under `references/flavors/`.

Five new files are created:
- `references/flavors/vibe-coder.md` — existing behavior, extracted from SKILL.md verbatim
- `references/flavors/onboarding.md`
- `references/flavors/pattern-learning.md`
- `references/flavors/architecture-review.md`
- `references/flavors/deep-understanding.md`

Three existing files become *shared base layers* with explicit "per-flavor overrides allowed" markers:
- `references/content-philosophy.md` — keeps show-don't-tell, visual density principle, quiz-application-not-memory, no-recycled-metaphors. Adds a header: "Flavor playbooks may override or tighten any rule marked `[overridable]` below."
- `references/gotchas.md` — keeps universal gotchas. Tooltip-aggressiveness and walls-of-text gotchas gain per-flavor notes.
- `references/module-brief-template.md` — adds a `flavor:` field at the top and makes the "Why should I care?" + "Key insight" fields explicitly flavor-dependent.

SKILL.md changes are minimal:
1. New Phase 0 section with the AskUserQuestion prompt
2. "Who This Is For" section becomes a table of 5 audiences (one row per flavor) instead of a vibe-coder-only description
3. Phase 2 "Curriculum Design" delegates module-arc selection to the flavor playbook
4. Phase 2.5 brief template references the flavor field
5. Phase 3 writing instructions tell agents to read their flavor playbook alongside existing references

The current single-audience module arc table (SKILL.md lines 75-83) is removed from SKILL.md and moved into each flavor playbook as a *different* arc, per audience research.

## Design Documents

- [Architecture](./architecture.md) — File structure, SKILL.md diff, per-flavor playbook outlines, interactive-element variance matrix
- [BDD Specifications](./bdd-specs.md) — Behavior scenarios for flavor selection, per-flavor content rules, and backward compatibility
- [Best Practices](./best-practices.md) — Per-flavor audience profiles, teaching pitfalls, and research-backed content rules with sources

## Out of scope

- **Writing full playbook content.** This design names what each playbook will contain; the implementation plan (next phase, via `superpowers:writing-plans`) will produce the actual prose.
- **A 6th "custom" flavor.** Users who pick "Other" in the AskUserQuestion fallback will be handled gracefully by the implementation, but a first-class Custom flavor is not in scope.
- **Retuning the visual design system.** `design-system.md` and `styles.css` are unchanged.
- **Changes to the parallel-build dispatcher.** The dispatcher already reads briefs and spawns agents; briefs just get a new field.
