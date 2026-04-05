# BDD Specifications: Engineer Flavors

These scenarios describe the user-observable behavior of the skill after the flavor system lands. They are written in Given / When / Then form for clarity, though the underlying "tests" are instruction-following checks — a reviewer reads the produced course and verifies each scenario holds.

## Feature: Flavor selection on first run

### Scenario: User invokes the skill with no flavor hint

```
Given the user has not yet picked a flavor in this session
  And the user says "turn this codebase into a course"
When the skill activates
Then the skill shows the First-Run Welcome message
  And the skill calls AskUserQuestion with exactly 5 options:
    1. Vibe Coder
    2. Onboarding
    3. Pattern Learning
    4. Architecture Review
    5. Deep Understanding
  And the skill does NOT begin codebase analysis until the user picks
```

### Scenario: User picks Vibe Coder

```
Given the flavor question has been asked
When the user picks "Vibe Coder"
Then the skill reads references/flavors/vibe-coder.md
  And all subsequent content follows the vibe-coder playbook
  And the produced course is byte-indistinguishable in structure from the pre-flavor skill output
  And the output contains line-by-line "Code ↔ Plain English" translations
  And every technical term receives a glossary tooltip on first use per module
```

### Scenario: User picks Onboarding

```
Given the flavor question has been asked
When the user picks "Onboarding"
Then the skill reads references/flavors/onboarding.md
  And the curriculum follows the onboarding module arc (mental model → dev loop → feature trace → conventions → PR norms → first change)
  And the final module simulates a first PR ("here's a realistic change — trace what you'd modify and why")
  And code blocks show "Code ↔ Convention" annotations (team's unwritten rules)
  And tooltips cover codebase-specific jargon and stack-specific terms but NOT general language basics
  And the voice is pragmatic-senior-teammate
```

### Scenario: User picks Pattern Learning

```
Given the flavor question has been asked
When the user picks "Pattern Learning"
Then the skill reads references/flavors/pattern-learning.md
  And the curriculum follows the pattern-learning arc (thesis → pattern 1 → pattern 2 → pattern 3 → composition → transfer)
  And every pattern is named explicitly (e.g., "this is the reactor pattern", "this is copy-on-write")
  And every pattern module ends with a "Transfer" callout stating where else this pattern applies
  And code blocks show "Code ↔ pattern name + reuse note" annotations
  And metaphors are used sparingly; formal pattern vocabulary is preferred
```

### Scenario: User picks Architecture Review

```
Given the flavor question has been asked
When the user picks "Architecture Review"
Then the skill reads references/flavors/architecture-review.md
  And the curriculum follows the architecture-review arc (thesis & constraints → decisions with tradeoffs → coupling critique → scalability pressure points → tech debt verdict)
  And every major architectural decision includes a "Context / Decision / Consequence" block with an explicit verdict line
  And code blocks show "Code ↔ ADR-style tradeoff" annotations
  And metaphors are avoided entirely
  And tooltips are sparse — reserved for non-standard architectural vocabulary
  And the voice is principled-staff-engineer-with-a-thesis
  And the course never describes without taking a stance
```

### Scenario: User picks Deep Understanding

```
Given the flavor question has been asked
When the user picks "Deep Understanding"
Then the skill reads references/flavors/deep-understanding.md
  And the curriculum follows the deep-understanding arc (problem → abstractions → flow → subsystem A → subsystem B → evolution)
  And code blocks show "Code ↔ mental-model diagram" annotations
  And tooltips are generous (audience variance is high)
  And the voice is curious-guide with layered reveal
```

### Scenario: User picks "Other" and provides custom intent

```
Given the flavor question has been asked
When the user picks "Other" and describes a goal in free text
Then the skill maps the goal to the closest flavor based on keywords
  And if mapping is ambiguous, the skill falls back to Deep Understanding and announces the fallback
  And the user's free-text goal is incorporated into the "why should I care?" framing of every module
```

## Feature: Per-flavor content rules enforcement

### Scenario: Onboarding course does not test syntax recall

```
Given the flavor is Onboarding
When the skill writes any quiz question
Then no question asks "what is the correct syntax for X"
  And no question asks "what does keyword Y do in language Z"
  And questions focus on "where would you change things" and "what convention does this team follow"
```

### Scenario: Architecture Review course contains no restaurant metaphors

```
Given the flavor is Architecture Review
When the skill writes any module
Then no module uses a metaphor from everyday life
  And tradeoffs are expressed in precise architectural vocabulary
  And each decision block has a "what this buys / what it costs / where it'll break" structure
```

### Scenario: Pattern Learning names every pattern explicitly

```
Given the flavor is Pattern Learning
When a module teaches a technique from the codebase
Then the technique has a named label (formal pattern name or author-coined term)
  And the module includes a "Transfer" callout listing at least 2 other contexts where the pattern applies
  And code blocks are annotated with the pattern name in the right column
```

### Scenario: Vibe Coder course tooltips every technical term

```
Given the flavor is Vibe Coder
When the skill writes module HTML
Then every technical term has a glossary tooltip on first use per module
  And acronyms always have tooltips on first use
  And the aggressiveness matches the current pre-flavor skill output
```

## Feature: Shared interactive-elements backbone

### Scenario: Every flavor includes the mandatory interactive elements

```
Given any flavor is selected
When the skill finishes building the course
Then the output contains at least one Group Chat Animation across modules
  And the output contains at least one Data Flow Animation across modules
  And every module contains at least one code block (in the flavor-specific style)
  And every module contains at least one quiz
  And every module uses glossary tooltips (scope varies per flavor)
```

### Scenario: Interactive-element HTML patterns are unchanged across flavors

```
Given any flavor is selected
When the writing agent produces a quiz HTML block
Then the HTML follows the patterns in references/interactive-elements.md exactly
  And the CSS class names match those in styles.css
  And the main.js engines pick up the elements via the documented data-* attributes
```

## Feature: Backward compatibility

### Scenario: Existing trigger phrases still activate the skill

```
Given a user says any of:
  - "Turn this into a course"
  - "Explain this codebase interactively"
  - "Make a course from this project"
  - "Teach me how this code works"
  - "Interactive tutorial from this code"
When the skill processes the request
Then the skill activates
  And proceeds to Phase 0 (flavor selection)
```

### Scenario: The build pipeline is unchanged

```
Given any flavor is selected
When Phase 3 completes and build.sh runs
Then the output directory structure matches the current skill exactly:
  course-name/
    styles.css
    main.js
    _base.html
    _footer.html
    build.sh
    modules/*.html
    index.html
  And styles.css is byte-identical to references/styles.css
  And main.js is byte-identical to references/main.js
```

### Scenario: Vibe Coder flavor preserves current experience

```
Given a user who previously used the skill picks Vibe Coder
When the skill produces the course
Then the learner sees the same type of content they saw before the flavor system landed:
  - Line-by-line Code ↔ English translations
  - Aggressive glossary tooltips on every term
  - Warm "smart friend" voice
  - Infographic-style visual density
  - "Why should I care = steer AI better" framing
```

## Feature: Progressive disclosure of flavor content

### Scenario: Flavor playbook is loaded at the right moment

```
Given the skill is running Phase 0
When the user picks a flavor
Then the skill reads the matching references/flavors/<flavor>.md file
  And does NOT read any other flavor's playbook
  And SKILL.md remains the only always-loaded orchestration file
```

### Scenario: Parallel writing agents receive their flavor playbook

```
Given the flavor is any engineer flavor AND the codebase is complex AND Phase 2.5 briefs exist
When Phase 3 parallel path dispatches writing agents
Then each agent receives:
  - Its module brief (from course-name/briefs/)
  - references/content-philosophy.md
  - references/gotchas.md
  - references/flavors/<flavor>.md          # new
  - Only the needed sections of interactive-elements.md and design-system.md
  And no agent receives playbooks for other flavors
  And no agent receives SKILL.md
```
