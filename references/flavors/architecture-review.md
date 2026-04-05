# Flavor Playbook: Architecture Review

> For the senior/staff engineer who wants to form a **defensible opinion** about this codebase's architecture. Not a tour. Not a tutorial. A structured review that ends in stances.

---

## 1. Audience snapshot

A senior or staff engineer (5+ years, often 10+) evaluating a codebase's architectural decisions to form a defensible opinion. They are not trying to learn what a cache is, how an HTTP handler works, or why you would use a queue. They already know.

**What they actually want to answer:**

- *Would I build it this way?*
- *Where will it hurt at scale?*
- *What would I change — and in what order?*
- *Which seams are load-bearing, and which are one incident away from breaking?*

**What they already know** (assume, do not re-teach):

- CAP, ACID, BASE
- Idempotency, eventual consistency, causal ordering, read-your-writes
- Backpressure, sharding, replication strategies
- Consensus at a high level (Paxos, Raft, 2PC)
- Common failure modes: split brain, thundering herd, retry storms, cache stampedes
- Isolation levels and the usual write skew / phantom read traps

**Contexts for reading the course:**

- **Hiring / due diligence** — is this team shipping good engineering?
- **Contributing / acquisition target** — where should I engage, and where are the foot-guns?
- **Design inspiration** — what decisions here would I steal or avoid in my own system?

They are not here for comfort. They are here for a thesis they can argue with.

---

## 2. Why this approach works (for this audience)

Abstract architectural descriptions fail this audience. They have read a dozen "here's how our system works" posts that never take a stance, never quantify a tradeoff, and never name where the design will break. The signal-to-noise ratio is catastrophically low for readers who already hold the general vocabulary.

**Concrete + opinionated beats abstract + neutral, every time.** This is why the research exemplars — all of them — insist on grounded tradeoff reasoning:

- **Kleppmann's _Designing Data-Intensive Applications_.** Every concept ends in a tradeoff. No chapter describes a technique without also describing the workload it fails on. ([DDIA Ch.1](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/ch01.html))
- **ATAM (Architecture Tradeoff Analysis Method).** A structured quality-attribute scoring method — explicitly designed so architects cannot hide behind adjectives like "scalable" or "robust." Every claim maps to a scenario, a sensitivity point, and a tradeoff point.
- **Martin Fowler's ADR bliki.** ADRs force the author to write down Context, Decision, and Consequence for every non-trivial call — the minimum scaffold for a defensible opinion. ([Fowler ADR](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html))
- **Joel Parker Henderson's ADR examples repo.** A public archive showing what ADRs look like in practice across dozens of real systems. ([ADR examples](https://github.com/joelparkerhenderson/architecture-decision-record))
- **Mozilla Firefox's architecture review process.** States the core problem directly: *"architecturally significant decisions are often not documented, and how they interrelate is not easily understood."* The review process exists to drag that tacit knowledge into the open. ([Mozilla ARP](https://mozilla.github.io/firefox-browser-architecture/text/0006-architecture-review-process.html))
- **Ilograph: 7 Common Mistakes in Architecture Diagrams.** Names the biggest failure mode — diagrams that are generic, unanchored, and do not reflect the actual system. ([Ilograph](https://www.ilograph.com/blog/posts/diagram-mistakes/))
- **ARDURA architecture review checklist.** Distributed monoliths and shared-DB coupling are the most damaging anti-patterns, and they are invisible from prose alone. You need the graph. ([ARDURA](https://ardura.consulting/blog/software-architecture-review-checklist/))

The through-line: **concrete coupling graphs + explicit stances transfer; abstract descriptions do not.**

This flavor exists to drag the tacit "would I build it this way?" reasoning out of the reader's head and onto the page, module by module, verdict by verdict.

---

## 3. The learner's core question

> **"Would I build it this way, and where will it hurt at scale?"**

Every module must advance an answer to that question. A module that describes the system without moving the needle on the reader's stance has failed this flavor.

---

## 4. Module arc (menu)

5 to 6 modules. The arc is **thesis → decisions + tradeoffs → coupling critique → scalability pressure → tech debt verdict**. Each module is grounded in *this* codebase's actual structure — never generic theoretical diagrams.

### Module 1 — Architectural thesis & constraints
**What it teaches:** The one-line thesis of this system's shape. What problem is the architecture optimized for? What is it deliberately *not* optimizing for? What were the hard constraints (team size, latency budget, consistency requirements, regulatory posture, storage economics) that forced the shape?

**Why it matters to this learner:** Without the thesis, every subsequent decision looks arbitrary. With it, the tradeoffs become legible.

### Module 2 — Decision 1 + tradeoff (ADR-style)
**What it teaches:** The single most load-bearing architectural decision — pick the one that, if reversed, would require rewriting the most code. Render it as an ADR block: Context / Decision / Consequence / **Verdict**.

**Why it matters:** This is where the reader starts separating "defensible" from "accidental."

### Module 3 — Decision 2 + tradeoff (ADR-style)
**What it teaches:** A second non-obvious decision — preferably one that interacts with Decision 1. Same ADR structure, same verdict requirement.

**Why it matters:** Interaction effects between decisions are where architectures actually break. This module exposes the seam.

### Module 4 (optional) — Decision 3 + tradeoff (ADR-style)
**What it teaches:** A third decision only if the codebase warrants it — typically a data model choice, a consistency-vs-availability call, or a sync-vs-async boundary. Omit this module for smaller systems rather than padding.

**Why it matters:** Three decisions is usually the ceiling before reader fatigue sets in. If there are more, pick the three that interlock.

### Module 5 — Coupling & data flow critique
**What it teaches:** A concrete coupling graph and a data flow diagram, both grounded in the actual repo layout. Identifies shared-DB coupling, hidden synchronous calls across service boundaries, circular dependencies, and distributed-monolith smells. Diagrams carry the evidence; prose carries the stance.

**Why it matters:** Distributed monoliths are invisible from code-level reading. They only show up when you draw the graph. This is where ARDURA-checklist-style critique earns its keep.

### Module 6 — Scalability pressure points & tech debt verdict
**What it teaches:** Where does this system break first under growth? Concrete pressure-point overlays on the coupling graph: the write path that becomes the bottleneck at 10x traffic, the shared table that becomes the hot shard, the synchronous call that becomes the cascading-failure fuse. Ends with an explicit tech-debt ranking: *"if you had one engineer-year, where would you spend it, and why?"*

**Why it matters:** This is the verdict module for the whole course. The reader should leave with a ranked refactor plan they could defend in a design review.

**Module count rule:** 5 modules minimum (thesis + 2 decisions + coupling + verdict), 6 maximum (add the optional third decision). More than 6 dilutes the thesis.

---

## 4b. Must-have element — Verdict lines

> **Every major decision module ends with a Verdict line. This is not optional. Without verdicts, the flavor has failed.**

### What a Verdict is

A **Verdict** is an opinionated stance expressed as one or two sentences. It names where the tradeoff holds, where it breaks, and — when possible — what the author would do instead and under what trigger condition.

### What a Verdict is not

- Not a summary. ("This module covered the write path.") Summaries describe; verdicts commit.
- Not a hedge. ("There are pros and cons to this approach.") Hedges refuse to commit; verdicts commit.
- Not a compliment. ("This is a clean implementation.") Compliments describe quality; verdicts name the failure condition.

### Example Verdict (reference template)

> **Verdict:** This trade-off is justified at current scale but will become the scaling bottleneck above ~10k writes/sec. I would split the write path into a separate service before then, and I would trigger that split the quarter the p99 latency on `POST /orders` crosses 250ms.

Notice the structure: (1) current status — *justified at current scale*; (2) failure condition — *above ~10k writes/sec*; (3) remediation — *split the write path*; (4) trigger — *p99 crosses 250ms*. A verdict that lacks all four is weaker. A verdict that has all four is defensible under cross-examination.

### Rule

Every decision module (Modules 2, 3, and optional 4) must end with at least one Verdict line at the module level, and every Code ↔ ADR-style block within those modules must contain its own Verdict line at the block level. Module 6 (tech debt hotspots) must end with a ranked verdict: where would you spend the next engineer-year, and why.

**Without verdicts, the flavor has failed.** Say this out loud to any sub-agent drafting a module: if there is no stance, the module is rejected.

---

## 5. Code block style: Code ↔ ADR-style

Two columns. Left column: the real code, verbatim from the repository — never modified, never simplified, never pseudo-coded. Right column: a four-line ADR-style block.

### The four lines

| Line | What it says |
|---|---|
| **Context** | What constraint this code addresses. The real-world pressure that forced the author's hand. |
| **Decision** | What this code chooses — the specific technique, boundary, or tradeoff encoded in the shown snippet. |
| **Consequence** | What the choice buys and what it costs. Both halves required. No free lunches. |
| **Verdict** | Opinionated stance. One line. See Section 4b for the structure. |

### Example block (reference template)

**Left column** (real code from the repo — this is illustrative only; the actual block uses verbatim repo code):

```python
# orders/service.py
async def place_order(user_id: str, cart: Cart) -> Order:
    async with db.transaction() as tx:
        existing = await tx.fetch_one(
            "SELECT id FROM orders WHERE idempotency_key = $1",
            cart.idempotency_key,
        )
        if existing:
            return await load_order(tx, existing["id"])
        order = await tx.insert(Order.from_cart(user_id, cart))
        await tx.execute(
            "UPDATE inventory SET reserved = reserved + $1 "
            "WHERE sku = $2 AND stock - reserved >= $1",
            cart.quantity, cart.sku,
        )
    return order
```

**Right column** (the ADR block):

> **Context.** Order placement must be idempotent under client retries and must never oversell inventory. The team chose strong consistency over availability for this path because oversells are customer-visible and cost refunds.
>
> **Decision.** Optimistic concurrency control, single Postgres transaction, idempotency key enforced at the write path, inventory reservation in the same transaction as the order insert.
>
> **Consequence.** Buys: linearizable order placement, no oversells, retry-safe at the API boundary. Costs: every order takes a row lock on `inventory.sku`, serializing all writes against a single hot SKU; throughput on any single SKU is bounded by transaction duration plus network RTT.
>
> **Verdict.** Correct at current volume. This becomes the first bottleneck during a flash sale — a single hot SKU will serialize on the inventory row and queue will back up. I would add a reservation-shard layer (per-SKU sub-rows or per-SKU in-memory token bucket with async reconciliation) before the next planned sales spike, and I would trigger the migration the week a single SKU crosses 50 orders/sec in production traffic.

Every code block in a decision module follows this structure. The writing agent copies the real code on the left, writes the four-line ADR on the right, and does not ship the block without the Verdict line.

---

## 6. Quiz style: critical judgment under stressors

Quizzes in this flavor test **critical judgment**, not recall. The reader already has the vocabulary. They do not need to be asked "what is eventual consistency" — they need to be asked "which of the decisions you just read about breaks first when you 10x the traffic."

### Question archetypes

1. **Stressor questions.** *"Here's a new requirement: 10x traffic growth over the next 18 months. Which of the three decisions from this course breaks first, and why? What's the failure mode — is it latency, throughput, consistency, or availability?"*

2. **Requirement-change questions.** *"You're adding a new compliance requirement: a tamper-evident audit log for every state change. Which architectural choice in this system makes this hardest to retrofit, and what does the minimum-viable retrofit look like?"*

3. **Refactor-priority questions.** *"Given the tradeoffs named in Modules 2–4, where would you spend the next engineer-year of refactoring effort? Rank the three decisions and defend the ranking."*

4. **Failure-mode questions.** *"Imagine the database goes down for 30 seconds. Walk through what breaks, in what order, and what recovers automatically. Where are the manual intervention points?"*

5. **"Where's the seam?" questions.** *"If the team had to split this monolith into two services tomorrow, where's the least-damaging seam and why?"*

### What to never ask

- *"What is CAP?"* The reader knows.
- *"Which file contains X?"* This is not Onboarding.
- *"What is the name of this pattern?"* This is not Pattern Learning.
- *"Describe the data flow."* Description is not judgment. Reframe as "where in the data flow does the first bottleneck appear under load, and why?"

### Quality bar

Every quiz must be answerable only by someone who read this course and engaged with its stance. A generic senior engineer should be able to make a credible guess — but the correct answer should cite a specific decision from a specific module. If a reader could answer the quiz without the course, the quiz is too weak.

---

## 7. Metaphor strategy: PROHIBITED

> **No metaphors.** Not one. Not a gentle one. Not "just to set the scene." None.

This section is not optional framing — it is a rule, and it is the single rule most likely to be violated by writing agents trained on general pedagogy. Say it out loud before drafting each module: **no metaphors.**

### What is banned

- **No restaurant metaphors.** The database is not a kitchen. The queue is not a waiter. The cache is not a pantry. The load balancer is not a maître d'.
- **No postal service metaphors.** Messages are not letters. The message broker is not a post office. Dead-letter queues are not undeliverable mail bins (even though that one is almost the etymology — do not go there).
- **No bouncer or nightclub metaphors.** Authentication is not a bouncer. Rate limiting is not a velvet rope.
- **No highway / traffic metaphors.** The network is not a freeway. Congestion control is not an onramp meter.
- **No library / book metaphors.** The database is not a library. The index is not a card catalog.
- **No office metaphors.** Services are not employees. The scheduler is not a manager.
- **No any-other-everyday-life metaphor.** If you find yourself typing "it's like a…", delete it and use the precise architectural term instead.

### Why

**Metaphors feel condescending to this audience.** A staff engineer being told "the write-ahead log is like a diary where the database writes down what it's about to do" experiences this as talking down. They already know what a WAL is. The metaphor adds zero new information and signals that the author misjudged the audience.

**Precision beats imagery.** The staff-engineer audience has a rich shared vocabulary — *backpressure, idempotency, eventual consistency, causal ordering, read-your-writes, write amplification, head-of-line blocking, retry storm, cascading failure, split brain, thundering herd, hot partition, fan-out, fan-in, circuit breaker, bulkhead, choreography vs orchestration, outbox pattern, saga, CQRS projection, materialized view, snapshot isolation, serializability, strict serializability, linearizability, sequential consistency, monotonic reads, bounded staleness.* Use those terms directly. They are more precise than any metaphor, and using them signals that the author is writing to peers, not to students.

**Metaphors dilute tradeoff analysis.** The whole point of this flavor is to ground decisions in their failure conditions and scaling limits. A metaphor obscures the limit — a WAL "like a diary" does not tell you at what fsync rate the disk becomes the bottleneck; the phrase "write amplification becomes disk-bound above ~30k syncs/sec on NVMe with default group commit" does.

### The single exception

None. Not even a small one. If a term is unfamiliar to some readers, use a **tooltip** (Section 8), not a metaphor. Tooltips are the escape hatch; metaphors are not.

### Self-check before shipping a module

Search the draft for the tokens: *"like a"*, *"imagine"*, *"think of this as"*, *"it's basically a"*, *"picture"*. If any hit lands on a pedagogical metaphor, rewrite it in precise terms. If the tempting metaphor is "restaurant," "kitchen," "bouncer," "librarian," or "postal service" — stop drafting and re-read this section.

---

## 8. Tooltip strategy: STINGY

Tooltips in this flavor are reserved for **non-standard architectural vocabulary**. Err light, not heavy.

### Tooltip

- **Project-coined terms.** Service names, internal domain vocabulary, custom abstractions ("the `Orchestrator`", "the `Ledger` subsystem"). Tooltip once at first use.
- **Non-canonical pattern names.** "Outbox pattern", "CQRS projection", "event sourcing snapshot", "saga compensation" — tooltip on first use with a one-line definition and a "see also" link to the canonical reference (usually DDIA, microservices.io, or the original paper).
- **Niche distributed-systems jargon.** Terms that a strong senior would know but a strong-in-a-different-niche senior might not: "HLC" (hybrid logical clock), "Hermes consensus", "Paxos quorum intersection", "ABD register." Tooltip the first time.
- **Custom metrics.** If the course mentions `inventory_hot_shard_writes_per_sec` or a similar project-specific metric, tooltip the first time.

### Do NOT tooltip (assume known)

- CAP, ACID, BASE
- Idempotency, eventual consistency, strong consistency, monotonic reads, read-your-writes
- Backpressure, sharding, replication, leader election
- Consensus basics: Paxos, Raft, 2PC
- Isolation levels: read committed, repeatable read, snapshot isolation, serializable
- Write skew, phantom reads, lost updates
- Common failure modes: split brain, thundering herd, cache stampede, retry storm, cascading failure
- Circuit breaker, bulkhead, rate limiter, load shedder
- Queue, topic, partition, offset, broker
- Primary key, foreign key, index, materialized view

If the author finds themselves tooltipping one of the above, the tooltip is wrong — delete it and trust the reader.

### Density target

A well-written Architecture Review module has **zero to three tooltips**. A module with more than five tooltips is almost certainly over-explaining and should be edited down.

---

## 9. Voice & tone

**Principled staff engineer with a thesis.** The voice takes stances. It says "I would change this" out loud. It is never neutral-descriptive.

### What the voice sounds like

- *"This is defensible at current scale — but watch this seam."*
- *"The team clearly prioritized throughput over latency here, and they were right to. The question is whether that tradeoff survives the next 10x."*
- *"I would split the write path before this becomes the incident everyone remembers."*
- *"The coupling between `Billing` and `Inventory` is the kind of thing that looks fine in a diagram and destroys you on a Tuesday."*

### What the voice does not sound like

- *"There are a number of considerations when evaluating this architecture."* (No stance. Reject.)
- *"The system uses PostgreSQL for persistence."* (Pure description. Reject.)
- *"This is a great implementation!"* (Compliment, not verdict. Reject.)
- *"It's kind of like when you…"* (Metaphor. Reject — see Section 7.)

### Tone calibration

- **Confident, not arrogant.** The voice is an experienced peer, not a lecturer and not a hot-take artist. Stances are defended with concrete constraints and failure conditions, not with rhetorical flourish.
- **Specific, not abstract.** Every claim cites a file, a function, a table, a metric, or a failure mode. If a sentence cannot be grounded, cut it.
- **Direct, not hedging.** "This is wrong" beats "this might arguably be suboptimal." Hedge only where the evidence genuinely doesn't support a stance — and when hedging, say *why* the evidence is insufficient.
- **Dry humor is welcome.** A well-placed "and then the on-call engineer discovers, at 3am, that this retry loop is unbounded" lands. Slapstick does not.
- **Sentence length is unrestricted.** The 2-3 sentence cap from `content-philosophy.md` is relaxed here — tradeoff prose sometimes needs a full paragraph to land. Use paragraphs when precision requires them; use short sentences for verdicts.

---

## 10. Visual density target: DIAGRAM-HEAVY

**Diagrams carry the evidence. Prose carries the stance.** Every major module must contain at least one diagram grounded in the actual structure of *this* codebase — not a generic theoretical sketch.

### Required diagram types

1. **Coupling graph.** A node-edge graph of the actual modules / services / packages in this repo, with edges annotated by call type (sync, async, shared-DB read, shared-DB write, event). Renders the distributed-monolith risk visible. Required in Module 5.

2. **Data flow diagram.** A directed graph showing how a representative request or event moves through the system. Annotations label each hop with latency class and failure mode. Required in Module 5.

3. **Pressure-point overlay.** The coupling graph from (1) re-rendered with the scaling pressure points highlighted — the hot shard, the sync call across a service boundary, the single-writer table. Required in Module 6.

4. **ADR-adjacent sketch.** Each decision module (2, 3, optional 4) should have at least one small diagram showing the specific boundary or seam the decision creates. Not a generic box-and-arrow sketch; specifically the boundary *this* code draws.

### Grounding requirement

Every diagram must be traceable back to real files in the repo. A node labeled `OrderService` should correspond to a real directory or package. An edge labeled `sync HTTP` should correspond to a real call site that a reader could grep for. **Generic theoretical diagrams — the kind that look the same for any e-commerce app — are explicitly forbidden.** Ilograph names "generic, unanchored diagrams" as the #1 architecture-diagram failure mode, and this flavor is where that failure mode is most dangerous.

### Prose-to-diagram ratio

Roughly 50/50, but with a crucial twist: **prose should never describe what the diagram already shows.** Prose carries the *stance* — "this coupling means the `Inventory` service cannot be deployed independently; that violates the implicit service-boundary contract" — while the diagram carries the *evidence*. If the prose is narrating the diagram, the prose is wasted.

### Interactive elements

Every module still includes the universal interactive elements: at least one quiz, at least one group chat animation somewhere in the course, at least one data flow animation. The Architecture Review flavor particularly benefits from:

- **Spot the tradeoff rationale.** A quiz variant where the reader is shown a diff and asked which of two annotations better explains the tradeoff.
- **Pressure-point hover overlays.** Interactive coupling graph where hovering a node reveals the scaling limit and the failure mode.

These are stronger affordances than the vibe-coder's "drag the file to the right box" style.

---

## 11. "Why should I care?" framing per module

Every module ties back to the core use case: **forming an informed opinion for your own hiring, contributing, or design decisions.** One-liners the writing agent can adapt:

| Module | "Why should I care?" framing |
|---|---|
| Architectural thesis & constraints | *"If you can't name the thesis in one sentence, you can't defend your opinion of the system. This module gives you the sentence."* |
| Decision 1 + tradeoff | *"This is the decision that, if reversed, would rewrite the most code. Knowing why it was made — and whether you agree — is the first move in any architecture review."* |
| Decision 2 + tradeoff | *"Interaction effects between decisions are where systems break. This module shows you the second decision and where it rubs against the first."* |
| Decision 3 + tradeoff (optional) | *"A third decision worth disagreeing with. By this point you should be forming a ranked list of what you'd change."* |
| Coupling & data flow critique | *"This is where distributed-monolith smells become visible. If you're evaluating this codebase for a job or an acquisition, this is the module you come back to."* |
| Scalability pressure points & tech debt verdict | *"This is the module that tells you where you'd spend your first engineer-year. Walk away with a ranked refactor plan you could defend in a design review."* |

The framing is always practical: hiring, contributing, designing. Never "for your general understanding" — that's Deep Understanding's frame.

---

## 12. Overrides to `content-philosophy.md`

This flavor overrides the base layer in several explicit ways. When a writing agent sees a conflict between this playbook and `content-philosophy.md`, **this playbook wins** for architecture-review courses.

### Replaces

- **"Code ↔ Plain English"** → **Code ↔ ADR-style.** Right column becomes a four-line block: Context / Decision / Consequence / Verdict. See Section 5.
- **"Metaphors first, then reality"** → **No metaphors. Not one.** See Section 7. This is the strongest override in the system.
- **"Quizzes test 'where would you look first'"** → **Quizzes test critical judgment under stressors.** See Section 6.

### Relaxes

- **"Max 2-3 sentences per text block"** → relaxed. Tradeoff prose may run a full paragraph when precision requires it. The gotcha is no longer "text blocks too long" but "text blocks with no visual anchor at all."
- **"Every screen must be at least 50% visual"** → relaxed to "every major module must contain a grounded diagram." Pure-prose tradeoff analysis is permitted when the diagram already appeared earlier in the module.

### Tightens

- **"Be extremely aggressive with tooltips"** → **stingy.** Only non-standard architectural vocabulary. See Section 8. Over-tooltipping in this flavor is a failure mode; under-tooltipping is nearly free.

### Keeps (unchanged from base)

- **No recycled metaphors** — vacuously true here; no metaphors at all.
- **Original code only** — no paraphrased, simplified, or synthetic snippets. The reader must be able to open the real file and see the same bytes.
- **Quizzes test application, not memory** — the specific "application" here is critical judgment under stressors, but the base rule stands.
- **One concept per screen** — a single decision per ADR block, a single pressure point per overlay.
- **Glossary tooltips never clip** — the technical rendering rule from `gotchas.md`.
- **Interactive elements are mandatory** — every module ships with at least one quiz and the course includes a group chat and data flow animation, per base rules.

---

## Known pitfalls (do not ship a module with any of these)

1. **Pure description without stance.** The #1 failure. Every module that describes the system without taking a position has failed this flavor. If a reviewer reads the module and cannot tell what the author thinks, rewrite.
2. **Generic theoretical diagrams.** Box-and-arrow sketches that could belong to any e-commerce app, any event-driven system, any CRUD backend. Forbidden. Diagrams must be grounded in the actual file structure of this repository. ([Ilograph's #1 diagram-mistake.](https://www.ilograph.com/blog/posts/diagram-mistakes/))
3. **Ignoring tech debt.** Skipping Module 6 or softening it into a "things we might improve" list. Tech debt hotspots and distributed-monolith smells are the *whole point* of this flavor. ([ARDURA checklist.](https://ardura.consulting/blog/software-architecture-review-checklist/))
4. **Using metaphors.** Do not. See Section 7. If you catch yourself typing "it's like…", stop, delete, and use the precise term.
5. **Missing verdicts.** Any decision module without a Verdict line has failed the flavor. Any ADR block without a Verdict line has failed the block. See Section 4b. **Without verdicts, the flavor has failed.**
6. **Over-tooltipping.** Tooltipping CAP, ACID, or idempotency signals that the author misjudged the audience. See Section 8.
7. **Hedging in the verdict line.** "There are arguments on both sides" is not a verdict. Verdicts commit. If the evidence genuinely doesn't support a stance, explain *why* — but don't disguise indecision as balance.
8. **Module bloat.** More than 6 modules dilutes the thesis. If the codebase has more than 3 decisions worth covering, pick the 3 that interlock most tightly and cut the rest.

---

## The single rule that matters most

> **Every major decision module ends with a Verdict line. Without verdicts, the flavor has failed.**

Say it before drafting. Say it during review. Say it before shipping. The Architecture Review flavor exists to produce defensible opinions; a course without verdicts is a tour, and this audience did not come for a tour.
