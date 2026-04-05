# Best Practices: Per-Flavor Content Rules

This document captures the audience research and content rules that will populate each flavor playbook. Citations reference the original sources found during the audience research phase.

## Cross-flavor principles (universal)

These survive the shift and live in `references/content-philosophy.md` as the base layer:

- **No recycled metaphors.** Even in flavors that use metaphors sparingly, the rule "never reuse, and never default to restaurant" holds.
- **Original code only.** Code snippets are exact copies from the real codebase — never modified or simplified. The learner should be able to open the real file and see the same code.
- **Quizzes test application, not memory.** The specific meaning of "application" varies per flavor, but definition-recall, file-name-recall, and syntax-recall are off-limits everywhere.
- **Show, don't tell.** Every flavor includes diagrams, animations, cards, and interactive elements. Only the density and ratio vary.
- **Interactive elements are mandatory.** Every module has at least one quiz, every course has at least one group chat animation and one data flow animation.
- **Glossary tooltips never clip.** Technical rule from `gotchas.md`; applies everywhere.

## Flavor 1: Vibe Coder (preserved)

**Content rules are unchanged from the current skill.** The `vibe-coder.md` playbook is extracted verbatim from the current SKILL.md + `content-philosophy.md`. This document does not re-catalog those rules; refer to the current files.

---

## Flavor 2: Onboarding

### Audience snapshot

A polyglot engineer (3+ years, strong in one stack) joining a codebase in an unfamiliar stack. Their panic isn't "I can't code" — it's "I don't know this team's *way*". They need a walked path into one real change, not an org chart or a history lesson.

### Real pain points (sourced)

- **"Code culture shock."** Weeks lost to environment setup and undocumented tooling. *([lonetrouper on DEV](https://dev.to/lonetrouper/onboarding-engineers-in-an-era-of-code-explosion-5ef9); [Cortex 2025 guide](https://www.cortex.io/post/developer-onboarding-guide))*
- **Implicit knowledge trapped in senior heads.** The "why" isn't written down, only the "where." *([Multiplayer](https://www.multiplayer.app/blog/improving-developer-onboarding/))*
- **Onboarding docs dump context instead of walking a change.** *([HubSpot product blog](https://product.hubspot.com/blog/onboarding-engineers-how-to-tackle-the-first-30-days))*

### Exemplars

- **Stripe's "spin-up project"** — a small, well-scoped, real task with a buddy. *([leportella.com](https://leportella.com/new-eng-stripe/))*
- **Zapier's personalized onboarding doc** — week-by-week, living knowledge base. *([Zapier engineering](https://zapier.com/engineering/engineer-onboarding/))*
- **GitHub engineers' end-to-end module traversal** — "follow one module deeply" beats "skim all modules." *([GitHub blog](https://github.blog/developer-skills/application-development/how-github-engineers-learn-new-codebases/))*

### Content rules

- **Module arc:** `10-minute mental model → dev loop (setup, run, test) → one end-to-end feature trace → local conventions → PR & review norms → your first change`
- **Code block style ("Code ↔ Convention"):** Left = real code. Right = the team's unwritten rule it obeys, expressed as a short imperative. Example right-column entries: *"Errors are always wrapped with `fmt.Errorf` and a context prefix — never return a bare error."* / *"Handlers take `ctx` as the first param. Always."*
- **Quiz style:** Procedural-fluency scenarios. *"You need to add a new `/v2/users/:id/preferences` endpoint. In what order do you touch files, and what's the first test you write?"*
- **Metaphor strategy:** Sparing. Only for genuinely unfamiliar infra (message queues, event loops). The audience is technical — metaphors should feel like cross-stack analogies, not pedagogy.
- **Tooltip strategy:** Tooltip the **codebase's own jargon** (internal service names, custom decorators, domain terms) and **stack-specific** terminology. Assume language/framework basics (closures, async, classes) are known.
- **Voice:** Pragmatic senior teammate. *"Here's what I wish I'd known week one."* Welcoming, direct, occasionally dry. No handholding lectures.
- **Visual density:** Balanced. Diagrams for the end-to-end trace, numbered step cards for the PR workflow, prose for conventions (conventions don't diagram well).
- **"Why should I care?" framing:** Everything ties back to "this is what you need to ship your first PR without breaking something."

### Known pitfalls to avoid

- Dumping org chart and history before the learner cares.
- Teaching language/framework basics — the polyglot already has them.
- Skipping test-writing conventions (the real blocker for first PR).
- Modules that read like a README table of contents.

### The must-have final module

**Onboarding is the only flavor where the final module is prescriptive: a simulated first PR.** The learner is walked through a realistic change ("add a new field to the user profile response") and has to trace which files they'd touch, what tests they'd add, and what the PR description would look like. Without this module, the onboarding flavor has failed.

---

## Flavor 3: Pattern Learning

### Audience snapshot

Mid-to-senior engineer reading a well-regarded OSS project (Redis, Next.js, LangChain, Django, PostgreSQL, etc.) to extract reusable techniques. They already know what caches, queues, and schedulers *are* — they want the *specific clever move* this codebase made.

### Real pain points (sourced)

- **Million-LOC codebases feel daunting.** Without a framing device, reading great code degenerates into trivia. *([Regehr: Tourist's Guide to LLVM](https://blog.regehr.org/archives/1453))*
- **No framing = no transfer.** Patterns don't stick unless named and tied to reuse contexts. *([AlgoCademy](https://algocademy.com/blog/strategies-for-learning-from-codebase-of-open-source-projects/))*
- **Engineers skip commit messages and ADRs where the rationale actually lives.** *([GitHub blog](https://github.blog/developer-skills/application-development/how-github-engineers-learn-new-codebases/))*

### Exemplars

- **Architecture of Open Source Applications (aosabook)** — author-written chapters framed as "lessons that transfer." *([aosabook.org](https://aosabook.org/en/))*
- **Julia Evans' zines** — zoom into 3-5 mechanisms, skip the 500 things you're "supposed to know." *([jvns.ca](https://jvns.ca/))*
- **Dan Luu on good eng blogs** — "reveal specific implementation decisions, not vague high-level content." *([danluu.com](https://danluu.com/corp-eng-blogs/))*

### Content rules

- **Module arc:** `One-line thesis of this codebase → pattern 1 (mechanism) → pattern 2 → pattern 3 → how the patterns compose → where each transfers`. 4-6 modules. Breadth is the enemy.
- **Code block style ("Code ↔ Pattern + Transfer"):** Left = real code. Right = the named pattern/technique followed by a "reuse when…" note. Example: *"**Reactor pattern** — a single thread multiplexes I/O across many connections via `epoll`. Reuse when you need to handle thousands of concurrent network clients on one core."*
- **Quiz style:** Transfer tests. *"Which of these three problems would this technique solve best? Why?"* Never "what is this pattern called?" — the course already told them. Test whether they can *recognize the problem shape* in a new context.
- **Metaphor strategy:** None to sparing. Metaphors dilute precise pattern names. Prefer *"this is the outbox pattern"* over *"this is like leaving a note on the kitchen counter."* The audience values precision.
- **Tooltip strategy:** Tooltip **formal pattern names** (reactor, copy-on-write, outbox, saga, CQRS projections) with a 1-line definition and a "see also" reference. Assume general CS vocabulary.
- **Voice:** Sharp peer showing off a trick. *"Look what they did here — this is the move."* Enthusiastic about cleverness, but technically precise.
- **Visual density:** Denser prose. The trick lives in the nuance of the mechanism. Diagrams still exist for the compositional view, but a module about a subtle locking strategy should be mostly prose + code.
- **"Why should I care?" framing:** *"Here's a technique you can steal for your own work."*

### Known pitfalls to avoid

- Treating the course as a tour (*"this directory does X, this does Y"*). Dead on arrival.
- Failing to name the transfer — every pattern needs an explicit "you'd use this when…" sentence.
- Over-explaining the domain (the reader knows what a cache is; they want the eviction trick).

### The must-have element

**Every pattern module ends with a Transfer callout.** A named callout box listing 2-3 other contexts where the same pattern applies. Without this, the pattern doesn't transfer and the flavor has failed.

---

## Flavor 4: Architecture Review

### Audience snapshot

Senior/staff engineer evaluating a codebase's architectural decisions to form a defensible opinion. They're asking: *would I build it this way? Where will it hurt at scale? What would I change?*

### Real pain points (sourced)

- **Architecture reviews stay abstract instead of grounding in concrete instances.** *([Ilograph: 7 mistakes in architecture diagrams](https://www.ilograph.com/blog/posts/diagram-mistakes/))*
- **"Architecturally significant decisions are often not documented, and how they interrelate is not easily understood."** *([Mozilla Firefox architecture review process](https://mozilla.github.io/firefox-browser-architecture/text/0006-architecture-review-process.html))*
- **Distributed monoliths and shared-DB coupling are the most damaging anti-patterns but invisible from prose.** *([ARDURA checklist](https://ardura.consulting/blog/software-architecture-review-checklist/))*

### Exemplars

- **Kleppmann's _Designing Data-Intensive Applications_** — every concept ends in a tradeoff. *([O'Reilly DDIA Ch.1](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch01.html))*
- **ATAM (Architecture Tradeoff Analysis Method)** — structured quality-attribute scoring. *([DevCom review process](https://devcom.com/tech-blog/successful-software-architecture-review-step-by-step-process/))*
- **ADR archives** — Fowler's ADR bliki and Joel Parker Henderson's examples repo. *([Fowler ADR](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html); [ADR examples repo](https://github.com/joelparkerhenderson/architecture-decision-record))*

### Content rules

- **Module arc:** `Architectural thesis & constraints → decision 1 + tradeoff → decision 2 + tradeoff → coupling & data flow critique → scalability pressure points → tech debt hotspots & verdict`. 5-6 modules.
- **Code block style ("Code ↔ ADR-style tradeoff"):** Left = real code. Right = a three-line ADR-style block: **Context** (what constraint this addresses) / **Decision** (what this code chooses) / **Consequence** (what the choice buys and what it costs). Plus a **Verdict** line: opinionated stance.
- **Quiz style:** Critical judgment. *"Here's a new requirement: 10x traffic growth. Which of the decisions you just read about breaks first, and why?"* Test whether the learner can apply the architectural reasoning to a novel stressor.
- **Metaphor strategy:** **None.** Metaphors feel condescending to this audience. Precision beats imagery.
- **Tooltip strategy:** **Stingy.** Only tooltip non-standard architectural vocabulary (e.g., "outbox pattern", "CQRS projection", project-coined terms). Assume CAP, ACID, idempotency, eventual consistency, backpressure, etc. are known.
- **Voice:** Principled staff engineer with a thesis. *"This is defensible — but watch this seam."* Takes stances. Says "I'd change this" out loud.
- **Visual density:** Diagram-heavy. Coupling graphs, data flow diagrams, pressure-point overlays. Prose carries the *stance*; diagrams carry the *evidence*.
- **"Why should I care?" framing:** *"Forming an informed opinion about this codebase's architecture — for your own hiring, contributing, or design decisions."*

### Known pitfalls to avoid

- Pure description without stance. Senior engineers want a thesis.
- Generic theoretical diagrams instead of *this codebase's actual* coupling graph.
- Ignoring tech debt hotspots and distributed-monolith smells — those are the whole point.
- Using metaphors. Don't.

### The must-have element

**Every major decision module ends with a Verdict line.** Not a summary — a stance. *"This trade-off is justified at current scale but will become the scaling bottleneck above ~10k writes/sec."* Without verdicts, the flavor has failed.

---

## Flavor 5: Deep Understanding

### Audience snapshot

Curious engineer with no specific forcing function. Broadest audience, least opinionated framing. Wants a thorough, satisfying tour of how the whole system works.

### Real pain points (sourced)

- **Without a job-to-be-done, learners skim and retain little.** Cognitive load theory — extraneous load dominates when intrinsic motivation is weak. *([Training Industry](https://trainingindustry.com/articles/content-development/balancing-mental-demands-cognitive-load-theory-in-training-design/))*
- **Tutorials default to either "tour the folders" or "lecture the concepts."** Both lose this audience.

### Exemplars

- **aosabook chapters** — "how it works and why it's built that way" narrative template.
- **Database Internals (databass.dev)** — layered depth, each chapter expands a black box.
- **Julia Evans zines** — make internals feel concrete and fun without a task. *([jvns.ca](https://jvns.ca/))*

### Content rules

- **Module arc:** `What problem the system solves → core abstractions → data & control flow → subsystem deep dive A → subsystem deep dive B → evolution & tradeoffs`. 5-6 modules.
- **Code block style ("Code ↔ Mental model"):** Left = real code. Right = a diagram or concise textual model of the *abstraction* the code implements. The goal is to let the reader step back from the syntax and see the shape.
- **Quiz style:** Comprehension tracing. *"Trace a request from entry to response. At step 3, what invariant holds?"* Tests whether the reader can follow the flow and identify load-bearing assumptions.
- **Metaphor strategy:** Moderate. One good metaphor per subsystem to anchor the mental model — then drop it and switch to precise vocabulary. Do not sustain metaphors across modules.
- **Tooltip strategy:** **Generous.** This audience has the highest variance in background. When in doubt, tooltip.
- **Voice:** Curious guide, layered reveal. *"Zoom in — now you can see why they needed that."*
- **Visual density:** Balanced. Layered diagrams that progressively reveal structure.
- **"Why should I care?" framing:** *"This is how the system really works — the kind of understanding that makes you better at system design in general."*

### Known pitfalls to avoid

- Overclaiming audience ("for everyone") and ending up for no one.
- No narrative spine — without a driving question, modules feel disconnected.
- Being a weaker version of the other three flavors. Deep Understanding's differentiation is **narrative completeness**, not sharpness. If a user wants sharpness, they should pick Pattern Learning or Architecture Review.

### The must-have element

**A progressive reveal structure across modules.** Each module should begin where the previous one stopped and zoom in one more level. Without a sense of cumulative depth, Deep Understanding becomes a random walk.

---

## Summary: the one-page rule set

| Rule | Vibe | Onboard | Pattern | Arch | Deep |
|---|---|---|---|---|---|
| 2-3 sentence text cap | ✅ | ✅ | relaxed | relaxed | ✅ |
| 50%+ visual | ✅ | ✅ | relaxed | diagram-heavy | ✅ |
| Line-by-line Code↔English | ✅ | ❌ | ❌ | ❌ | ❌ |
| Aggressive tooltips | ✅ | stack-only | pattern-names-only | stingy | generous |
| Metaphors | heavy | sparing | sparing | **none** | moderate |
| Must name every pattern | — | — | ✅ | — | — |
| Must end in first-PR sim | — | ✅ | — | — | — |
| Must include verdict per decision | — | — | — | ✅ | — |
| Must include transfer callouts | — | — | ✅ | — | — |
| Must have progressive-depth reveal | — | — | — | — | ✅ |

## Sources

Grouped by flavor for reference when writing playbooks.

**Onboarding:**
- [Onboarding Engineers in an Era of Code Explosion (DEV)](https://dev.to/lonetrouper/onboarding-engineers-in-an-era-of-code-explosion-5ef9)
- [Cortex: Developer Onboarding 2025 Guide](https://www.cortex.io/post/developer-onboarding-guide)
- [Multiplayer: Improving Developer Onboarding](https://www.multiplayer.app/blog/improving-developer-onboarding/)
- [Leportella: What it's like to be a new engineer at Stripe](https://leportella.com/new-eng-stripe/)
- [Zapier Engineering: How We Onboard New Engineers](https://zapier.com/engineering/engineer-onboarding/)
- [GitHub Blog: How GitHub engineers learn new codebases](https://github.blog/developer-skills/application-development/how-github-engineers-learn-new-codebases/)
- [HubSpot Product: Onboarding Engineers — First 30 Days](https://product.hubspot.com/blog/onboarding-engineers-how-to-tackle-the-first-30-days)

**Pattern Learning:**
- [Architecture of Open Source Applications (aosabook)](https://aosabook.org/en/)
- [Julia Evans / wizardzines](https://jvns.ca/)
- [The New Stack on Julia Evans' zines](https://thenewstack.io/julia-evans-bite-size-zines-break-it-down/)
- [Dan Luu: How good corporate eng blogs are written](https://danluu.com/corp-eng-blogs/)
- [John Regehr: A Tourist's Guide to the LLVM Source Code](https://blog.regehr.org/archives/1453)
- [AlgoCademy: Strategies for Learning from OSS Codebases](https://algocademy.com/blog/strategies-for-learning-from-codebase-of-open-source-projects/)

**Architecture Review:**
- [O'Reilly: DDIA Ch.1 — Trade-Offs in Data Systems Architecture](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch01.html)
- [ARDURA: Software Architecture Review Checklist](https://ardura.consulting/blog/software-architecture-review-checklist/)
- [DevCom: Successful Software Architecture Review Process](https://devcom.com/tech-blog/successful-software-architecture-review-step-by-step-process/)
- [Mozilla Firefox: Architecture Review Process](https://mozilla.github.io/firefox-browser-architecture/text/0006-architecture-review-process.html)
- [Ilograph: 7 Common Mistakes in Architecture Diagrams](https://www.ilograph.com/blog/posts/diagram-mistakes/)
- [Martin Fowler: Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- [Joel Parker Henderson: ADR examples repo](https://github.com/joelparkerhenderson/architecture-decision-record)

**Deep Understanding:**
- [Training Industry: Cognitive Load Theory in Training Design](https://trainingindustry.com/articles/content-development/balancing-mental-demands-cognitive-load-theory-in-training-design/)
- aosabook, Julia Evans' zines (reused from above)

**General:**
- [arXiv 2504.04553: Understanding Codebases Like a Professional](https://arxiv.org/html/2504.04553v2)
