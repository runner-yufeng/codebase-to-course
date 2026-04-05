# Implementation Plan: Engineer Flavors for codebase-to-course

**Date:** 2026-04-05
**Source design:** [`docs/plans/2026-04-05-engineer-flavors-design/`](../2026-04-05-engineer-flavors-design/_index.md)
**Status:** Plan ready for execution

## Goal

Implement the five-flavor architecture designed in the companion design folder: extract the current behavior into `references/flavors/vibe-coder.md`, add four new engineer flavor playbooks (`onboarding`, `pattern-learning`, `architecture-review`, `deep-understanding`), refactor the three audience-dependent base files into a shared base layer, and add a mandatory Phase 0 flavor selection to SKILL.md.

## Constraints

- **Additive, not destructive.** No existing file is deleted. `SKILL.md` is modified in place; the three base-layer files (`content-philosophy.md`, `gotchas.md`, `module-brief-template.md`) are modified in place; the five new playbook files are created under `references/flavors/`.
- **Zero changes to build pipeline.** `styles.css`, `main.js`, `build.sh`, `_base.html`, `_footer.html`, `design-system.md`, and `interactive-elements.md` are untouched.
- **Backward compatibility.** When a user picks Vibe Coder, the output must be indistinguishable from the pre-flavor skill. All current trigger phrases must still activate the skill.
- **Red-Green TDD adapted for a docs project.** Every feature has a `-test` task producing a verification checklist, followed by an `-impl` task that makes the content changes. The checklist is initially failing (Red) and transitions to passing (Green) after impl.
- **No code generation in tasks.** Task files describe *what* to implement and point to `best-practices.md` / `architecture.md` sections for content. They do not pre-write the prose.
- **One task per file.** Each task has its own `.md` file under this plan folder.

## Architecture (summary — full detail in design folder)

```
codebase-to-course/
├── SKILL.md                            # MODIFIED: + Phase 0 flavor selection; delegates to playbooks
└── references/
    ├── flavors/                        # NEW directory
    │   ├── vibe-coder.md               # NEW: existing behavior extracted
    │   ├── onboarding.md               # NEW
    │   ├── pattern-learning.md         # NEW
    │   ├── architecture-review.md      # NEW
    │   └── deep-understanding.md       # NEW
    ├── content-philosophy.md           # MODIFIED: base-layer header + [overridable] markers
    ├── gotchas.md                      # MODIFIED: per-flavor riders on two gotchas
    ├── module-brief-template.md        # MODIFIED: `flavor:` field
    └── (other files unchanged)
```

## Task Ordering & Dependencies

Red-Green pairs (each impl depends on its paired test):

```
001-test ─► 001-impl    (Vibe Coder playbook)
002-test ─► 002-impl    (Onboarding playbook)
003-test ─► 003-impl    (Pattern Learning playbook)
004-test ─► 004-impl    (Architecture Review playbook)
005-test ─► 005-impl    (Deep Understanding playbook)
006-test ─► 006-impl    (Shared base-layer refactor)
007-test ─► 007-impl    (SKILL.md Phase 0 + delegation)

008-verify              (Backward-compat) — depends on 007-impl
009-verify              (E2E integration) — depends on 001-impl..007-impl
```

**Parallelizable:** Tasks 001 through 007 are independent from each other (different files, different scenarios). Any executor may launch them in parallel or batches. Only the standalone verification tasks (008, 009) have cross-task dependencies.

## BDD Scenario → Task Coverage

| BDD Scenario | Covered by |
|---|---|
| User invokes the skill with no flavor hint | 007-test |
| User picks Vibe Coder | 001-test, 007-test |
| User picks Onboarding | 002-test, 007-test |
| User picks Pattern Learning | 003-test, 007-test |
| User picks Architecture Review | 004-test, 007-test |
| User picks Deep Understanding | 005-test, 007-test |
| User picks "Other" and provides custom intent | 007-test |
| Onboarding course does not test syntax recall | 002-test |
| Architecture Review course contains no restaurant metaphors | 004-test |
| Pattern Learning names every pattern explicitly | 003-test |
| Vibe Coder course tooltips every technical term | 001-test |
| Every flavor includes the mandatory interactive elements | 009-verify |
| Interactive-element HTML patterns unchanged across flavors | 009-verify |
| Existing trigger phrases still activate the skill | 008-verify |
| The build pipeline is unchanged | 008-verify |
| Vibe Coder flavor preserves current experience | 001-test, 008-verify |
| Flavor playbook is loaded at the right moment | 007-test, 009-verify |
| Parallel writing agents receive their flavor playbook | 007-test, 009-verify |

## Execution Plan

Each task is a standalone `.md` file in this folder. Red (test) tasks come before Green (impl) tasks for the same feature.

- [Task 001: Vibe Coder Playbook — Test](./task-001-vibe-coder-playbook-test.md)
- [Task 001: Vibe Coder Playbook — Impl](./task-001-vibe-coder-playbook-impl.md)
- [Task 002: Onboarding Playbook — Test](./task-002-onboarding-playbook-test.md)
- [Task 002: Onboarding Playbook — Impl](./task-002-onboarding-playbook-impl.md)
- [Task 003: Pattern Learning Playbook — Test](./task-003-pattern-learning-playbook-test.md)
- [Task 003: Pattern Learning Playbook — Impl](./task-003-pattern-learning-playbook-impl.md)
- [Task 004: Architecture Review Playbook — Test](./task-004-architecture-review-playbook-test.md)
- [Task 004: Architecture Review Playbook — Impl](./task-004-architecture-review-playbook-impl.md)
- [Task 005: Deep Understanding Playbook — Test](./task-005-deep-understanding-playbook-test.md)
- [Task 005: Deep Understanding Playbook — Impl](./task-005-deep-understanding-playbook-impl.md)
- [Task 006: Shared Base Layer Refactor — Test](./task-006-base-layer-refactor-test.md)
- [Task 006: Shared Base Layer Refactor — Impl](./task-006-base-layer-refactor-impl.md)
- [Task 007: SKILL.md Phase 0 + Delegation — Test](./task-007-skill-md-updates-test.md)
- [Task 007: SKILL.md Phase 0 + Delegation — Impl](./task-007-skill-md-updates-impl.md)
- [Task 008: Backward-Compatibility Verification](./task-008-backward-compat-verify.md)
- [Task 009: End-to-End Flavor Flow Verification](./task-009-e2e-flavor-flow-verify.md)

## Verification Strategy

For this docs-only project, "verification" means reading the produced file(s) and confirming they match the acceptance criteria. Each `-test` task produces a concrete, grep-able checklist. The `-impl` task is complete only when all checklist items pass.

Task 008 is a cold-read of the file tree: byte-compare unchanged files, grep SKILL.md for the current trigger phrases, confirm the vibe-coder playbook preserves every rule from the pre-refactor state.

Task 009 is an integration rubric: given a hypothetical codebase, walk the skill through each flavor's pipeline mentally and verify the loaded references, module arc choice, and mandatory-element coverage match expectations.

## Out of Scope (for this plan)

- Updating the README.md to mention engineer flavors. (Can be a follow-up plan.)
- Authoring a "custom" 6th flavor that maps user free-text intent to a generated playbook.
- Retuning `design-system.md` tokens or `interactive-elements.md` HTML patterns.
- Changing the parallel-build dispatcher logic beyond adding one field to the brief template.
