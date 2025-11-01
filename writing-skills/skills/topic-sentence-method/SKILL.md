---
name: topic-sentence-method
description: Paragraph structure with clear topic sentences. Use when writing structured content where each paragraph needs clear focus. Each paragraph previews its content in the first sentence for enhanced scannability.
---

# Topic Sentence Method

**Purpose**: Transform outline bullets into effective topic sentences that lead paragraphs and support hierarchical communication.

**Origin**: Adapted from composition theory (Bain 1866, Brooks & Warren 1949) and integrated with Pyramid Principle for technical and business writing.

**Use When**: Expanding hierarchical outlines into structured prose during the drafting phase.

---

## Core Principle

**The topic sentence states the paragraph's main point explicitly and connects it to the governing idea above it in the hierarchy.**

### Why Topic Sentences Matter

1. **Orientation**: Readers know immediately what the paragraph will discuss
2. **Hierarchy**: Explicit connection to parent message maintains logical flow
3. **Scannability**: Readers can extract key points by reading first sentences only
4. **Focus**: Writers stay on topic, preventing paragraph drift
5. **Evidence**: Clear claims make evidence requirements obvious

### Integration with Pyramid Principle

```
Governing Message (Tier 1)
├─ Supporting Message (Tier 2) ← Topic Sentence of Section
│  ├─ Key Point (Tier 3) ← Topic Sentence of Paragraph
│  │  ├─ Supporting detail (Tier 3/4)
│  │  ├─ Evidence (Tier 4)
│  │  └─ Example (Tier 4)
```

**Each topic sentence answers**: "How does this support the claim above?"

---

## Five Topic Sentence Patterns

### Pattern 1: Definition + Importance

**Structure**: Define concept, then state why it matters to parent claim.

**Formula**: `[Concept] is [definition]. This [importance/impact]...`

**Example** (Tutorial):
- Bullet: `• Type safety catches errors at compile time`
- Topic Sentence: *"Type safety is the practice of declaring variable types explicitly so the compiler can verify correct usage. This prevents an entire class of runtime errors that would otherwise require extensive testing to catch."*

**Example** (Explanation):
- Bullet: `• MECE reasoning prevents overlap and gaps`
- Topic Sentence: *"MECE (Mutually Exclusive, Collectively Exhaustive) reasoning is a principle that ensures arguments neither overlap nor leave gaps. This structural rigor makes communication 25% more comprehensible according to McKinsey's 2018 analysis."*

**Use For**: Introducing concepts, frameworks, principles, methodologies.

---

### Pattern 2: Action + Result

**Structure**: State the action, then describe the outcome that supports parent claim.

**Formula**: `[Action verb] [object] to [achieve result]. This [outcome]...`

**Example** (How-To):
- Bullet: `• Run tests before committing`
- Topic Sentence: *"Run your test suite before committing code to catch regressions early. This prevents broken code from reaching teammates and reduces debugging time by 40% in our analysis of 500 pull requests."*

**Example** (Tutorial):
- Bullet: `• Extract reusable components from duplicated code`
- Topic Sentence: *"Extract shared UI logic into reusable components when you find yourself copying code between files. This reduces maintenance burden and ensures consistent behavior across your application."*

**Use For**: Instructions, procedures, workflows, actionable recommendations.

---

### Pattern 3: Problem + Solution

**Structure**: Identify the problem, then state the solution that addresses parent claim.

**Formula**: `[Problem] occurs when [context]. [Solution] resolves this by [mechanism]...`

**Example** (Explanation):
- Bullet: `• Data drift degrades model accuracy over time`
- Topic Sentence: *"Data drift occurs when the statistical properties of production data diverge from training data distributions. Continuous monitoring with KL divergence tracking resolves this by triggering retraining before accuracy degrades below acceptable thresholds."*

**Example** (Reference):
- Bullet: `• Race conditions cause intermittent test failures`
- Topic Sentence: *"Race conditions in asynchronous tests produce non-deterministic failures that are difficult to reproduce. The `waitFor` helper resolves this by polling the DOM until the expected condition is met or timeout occurs."*

**Use For**: Troubleshooting, debugging, architectural decisions, design rationale.

---

### Pattern 4: Concept + Analogy

**Structure**: State abstract concept, then provide concrete analogy that illuminates parent claim.

**Formula**: `[Abstract concept] [technical definition]. Like [familiar analogy], [mapping]...`

**Example** (Tutorial):
- Bullet: `• Git branches allow parallel development`
- Topic Sentence: *"Git branches are independent lines of development that diverge from a common history. Like having multiple drafts of a document open simultaneously, branches let you experiment with changes without affecting the stable version until you're ready to merge."*

**Example** (Explanation):
- Bullet: `• Type inference reduces boilerplate`
- Topic Sentence: *"Type inference allows compilers to deduce variable types from context without explicit annotations. Like a reader understanding pronouns from surrounding sentences, the compiler resolves types from how variables are used."*

**Use For**: Explaining abstractions, introducing unfamiliar concepts, teaching beginners.

---

### Pattern 5: Question + Answer

**Structure**: Pose the question readers are asking, then answer it to support parent claim.

**Formula**: `[Question]? [Answer]. [Elaboration/Evidence]...`

**Example** (How-To):
- Bullet: `• Choose PostgreSQL for complex queries and transactions`
- Topic Sentence: *"When should you choose PostgreSQL over MongoDB? Use PostgreSQL when your application requires complex joins, ACID transactions, or rich query capabilities. Our benchmark of 50 production applications shows PostgreSQL outperforms MongoDB by 3x on join-heavy workloads."*

**Example** (Explanation):
- Bullet: `• Backpropagation enables deep learning`
- Topic Sentence: *"How do neural networks learn from mistakes? Backpropagation calculates gradients by applying the chain rule from output back to input layers, allowing each weight to adjust proportionally to its contribution to error. This mathematical foundation made modern deep learning possible."*

**Use For**: Anticipating reader questions, addressing objections, clarifying confusion points.

---

## Choosing the Right Pattern

### By Diátaxis Mode

**Tutorial** (Learning-Oriented):
- Primary: Action + Result, Concept + Analogy
- Secondary: Definition + Importance
- Avoid: Heavy Problem + Solution (can overwhelm beginners)

**How-To** (Problem-Oriented):
- Primary: Action + Result, Problem + Solution
- Secondary: Question + Answer
- Avoid: Lengthy Definition + Importance (readers want solutions fast)

**Reference** (Information-Oriented):
- Primary: Definition + Importance, Problem + Solution
- Secondary: Question + Answer (for API parameters)
- Avoid: Concept + Analogy (just give facts)

**Explanation** (Understanding-Oriented):
- Primary: Concept + Analogy, Problem + Solution, Question + Answer
- Secondary: Definition + Importance
- All patterns useful for deep dives

### By Content Depth

**Shallow** (2-3 hierarchy levels, 800-1500 words):
- Use Pattern 1 (Definition) and Pattern 2 (Action)
- Keep topic sentences short (1-2 sentences max)
- Focus on clarity over comprehensiveness

**Medium** (3-4 levels, 2000-5000 words):
- Mix Pattern 2 (Action), Pattern 3 (Problem), Pattern 5 (Question)
- Topic sentences can be 2-3 sentences
- Balance clarity with depth

**Deep** (4+ levels, 5000+ words):
- Use all patterns strategically
- Pattern 4 (Analogy) for complex abstractions
- Pattern 5 (Question) to structure explorations
- Topic sentences can be full paragraphs (with internal topic sentence)

---

## Quality Criteria

### Strong Topic Sentences

✅ **Explicit**: States the point clearly, no implicit assumptions
✅ **Connected**: Links to parent message in hierarchy
✅ **Standalone**: Makes sense when read in isolation (scannability)
✅ **Evidence-Ready**: Makes falsifiable claims that evidence can support
✅ **Focused**: Single main point per sentence (compound sentences okay if tightly related)

**Example**:
*"Continuous integration reduces integration bugs by 60% in our analysis of 200 projects (Smith 2023). By running tests on every commit, teams catch incompatibilities before they compound into merge nightmares."*

✅ Explicit: States CI reduces bugs by 60%
✅ Connected: Supports parent claim about CI value
✅ Standalone: Complete thought with evidence
✅ Evidence-Ready: Cites Smith 2023 study
✅ Focused: Single point (bug reduction via testing)

### Weak Topic Sentences

❌ **Vague**: "CI is important for teams."
- *Why is it important? How does it support parent claim?*

❌ **Disconnected**: "Python was created by Guido van Rossum in 1991."
- *How does this history support the parent message about Python's value?*

❌ **Buried Lead**: "While many approaches exist, our experiments with 10 configurations over 6 months using various metrics revealed that approach B performs best."
- *Put the finding first: "Approach B outperformed 9 alternatives across 6 months of testing."*

❌ **Evidence-Free**: "Machine learning solves many problems effectively."
- *Which problems? How effectively? Says nothing falsifiable.*

❌ **Multi-Point**: "CI reduces bugs, improves velocity, enhances code quality, and increases team confidence."
- *Four claims need four topic sentences (or one governing sentence with 4 supporting paragraphs).*

---

## Integration with Outline Expansion

### Workflow

1. **Receive hierarchical outline** with bullets from `outline-expander` agent
2. **Identify parent message** for each bullet
3. **Choose appropriate pattern** based on:
   - Diátaxis mode (Tutorial/HowTo/Reference/Explanation)
   - Content type (definition, instruction, explanation, etc.)
   - Audience expertise level
4. **Draft topic sentence** using pattern formula
5. **Validate**:
   - Does it support parent message?
   - Is it explicit and standalone?
   - Does it prepare for evidence/details to follow?
6. **Refine** for clarity and flow

### Example Transformation

**Input** (from outline-expander):
```
Message: "CI/CD pipelines reduce deployment risk"
├─ • Automated testing catches bugs early
├─ • Staged rollouts limit blast radius
└─ • Rollback capabilities enable quick recovery
```

**Output** (with topic sentences):

**Topic Sentence 1** (Action + Result):
*"Automated test suites run on every commit to catch bugs before they reach production. This early detection reduces post-deployment hotfixes by 80% in our analysis of 300 deployments."*

**Topic Sentence 2** (Problem + Solution):
*"Deploying to all users simultaneously risks widespread outages if critical bugs slip through testing. Staged rollouts limit blast radius by deploying to 5%, 25%, 50%, then 100% of traffic with automated health checks between stages."*

**Topic Sentence 3** (Action + Result):
*"Configure one-click rollback in your CI/CD pipeline to revert to the previous stable version when issues arise. This capability enables recovery in under 2 minutes versus 30+ minutes for manual rollbacks, minimizing user impact."*

---

## Common Pitfalls

### Pitfall 1: Topic Sentence as Transition

❌ **Don't**: "Now let's discuss testing strategies."
✅ **Do**: "Comprehensive testing strategies catch 95% of regressions before deployment (Jones 2024)."

**Why**: Transitions don't make claims readers can scan. State the point.

### Pitfall 2: Burying the Lead

❌ **Don't**: "After extensive research and consideration of multiple frameworks over several months, we decided that React offers the best balance of factors."
✅ **Do**: "React offers the best balance of performance, ecosystem, and learning curve for our team's needs. Our evaluation of 5 frameworks over 3 months scored React highest across 12 criteria."

**Why**: Readers scan first sentences. Put conclusion first, details second (Pyramid Principle).

### Pitfall 3: False Specificity

❌ **Don't**: "Machine learning algorithms can achieve high accuracy."
✅ **Do**: "Gradient boosted decision trees achieved 94.2% accuracy on our fraud detection dataset, outperforming neural networks by 3 percentage points."

**Why**: Vague claims like "high accuracy" convey no information. Quantify with evidence.

### Pitfall 4: Multiple Claims

❌ **Don't**: "Docker improves portability, simplifies dependencies, enables microservices, and scales efficiently."
✅ **Do**: "Docker containers bundle applications with their dependencies, ensuring consistent behavior across environments."
- *Then use 4 supporting paragraphs for portability, dependencies, microservices, scalability.*

**Why**: One topic sentence, one claim. Multiple claims need multiple paragraphs.

### Pitfall 5: Disconnected from Hierarchy

❌ **Don't** (under "Why use type systems?"):
"TypeScript was released by Microsoft in 2012."

✅ **Do** (under "Why use type systems?"):
"TypeScript's type system catches 15% of bugs at compile time that would otherwise require runtime testing (Google 2017)."

**Why**: Every topic sentence must advance the parent claim. Historical trivia doesn't support "why use type systems" unless it's relevant to adoption/maturity.

---

## Examples by Diátaxis Mode

### Tutorial Example

**Context**: Teaching beginners to use Git branches
**Hierarchy**: "Git branches enable safe experimentation"
**Bullets**:
- `• Create branch for new features`
- `• Work independently of main branch`
- `• Merge when ready`

**Topic Sentences** (Action + Result + Concept + Analogy):

1. *"Create a new branch when starting any feature or experiment to isolate your changes from stable code. Use `git checkout -b feature-name` to create and switch to a new branch in one command."*

2. *"Work on your feature branch as if it's a private draft—commits here don't affect the main branch. Like editing a copy of a document, you can experiment freely knowing the original remains intact."*

3. *"Merge your feature branch back to main when your work is complete and tested. The `git merge feature-name` command integrates your changes, combining both histories into a unified timeline."*

**Pattern Choices**: Action + Result for instructions, Analogy for abstract concepts, keeps tutorial concrete and actionable.

### How-To Example

**Context**: Solving production debugging problem
**Hierarchy**: "Distributed tracing reveals performance bottlenecks"
**Bullets**:
- `• Instrument services with trace IDs`
- `• Visualize request flows`
- `• Identify slow operations`

**Topic Sentences** (Problem + Solution + Action + Result):

1. *"Debugging slow requests across 10+ microservices requires correlating logs from each service—a manual nightmare. Instrument every service to propagate trace IDs in request headers, allowing tools like Jaeger to stitch logs into unified timelines."*

2. *"Visualize complete request flows using Jaeger's UI to see which services handled each request and how long each step took. This timeline view reveals whether delays come from database queries, service calls, or processing logic."*

3. *"Identify slow operations by sorting traces by duration and examining spans exceeding 95th percentile latency. Our team reduced P95 latency from 2.3s to 400ms by optimizing the top 5 slowest spans this analysis revealed."*

**Pattern Choices**: Problem + Solution addresses reader's pain point, Action + Result provides concrete outcomes, builds urgency.

### Reference Example

**Context**: API documentation for database connection pool
**Hierarchy**: "Connection pool configuration affects performance"
**Parameters**:
- `• minConnections` - Minimum pool size
- `• maxConnections` - Maximum pool size
- `• idleTimeout` - Idle connection lifetime

**Topic Sentences** (Definition + Importance + Question + Answer):

1. *"`minConnections` (integer, default: 2) sets the minimum number of database connections kept alive in the pool. Setting this too low causes latency spikes when idle pools must establish new connections under sudden load."*

2. *"`maxConnections` (integer, default: 10) caps the maximum number of concurrent database connections the pool can maintain. Set this to your database's connection limit divided by your application instance count to prevent exhausting database capacity."*

3. *"How long should idle connections stay alive? `idleTimeout` (integer, milliseconds, default: 600000) closes connections that remain unused for this duration, balancing resource conservation with connection reuse. Set to 10 minutes (600000ms) for typical web applications."*

**Pattern Choices**: Definition + Importance for parameters, Question + Answer for complex configuration, provides facts without narrative.

### Explanation Example

**Context**: Understanding why gradient descent works
**Hierarchy**: "Gradient descent finds function minima iteratively"
**Concepts**:
- `• Gradients point toward steepest increase`
- `• Step size affects convergence`
- `• Local minima can trap optimization`

**Topic Sentences** (Concept + Analogy + Problem + Solution):

1. *"Gradients represent the direction of steepest increase in a function's output at a given point. Like a hiker reading a topo map to find the steepest uphill path, gradient descent reads these directional derivatives—then walks downhill instead, toward the minimum."*

2. *"Step size (learning rate) controls how far to move in the gradient's direction each iteration. Too large and the algorithm overshoots the minimum like a hiker taking huge steps past the valley; too small and convergence requires thousands of iterations like taking tiny shuffles downhill."*

3. *"Local minima trap gradient descent in suboptimal solutions when the algorithm finds a small valley but not the deepest one. Techniques like momentum (building velocity to jump over small hills) and random restarts (starting from multiple positions) help escape these traps to find better solutions."*

**Pattern Choices**: Analogy makes abstract concepts concrete, Problem + Solution addresses known limitation, builds deep understanding.

---

## Summary

**The topic sentence method transforms hierarchical outlines into scannable, evidence-ready prose by:**

1. **Making claims explicit** - No implicit assumptions
2. **Connecting to hierarchy** - Each sentence supports parent message
3. **Enabling scannability** - First sentences convey structure
4. **Preparing for evidence** - Claims are falsifiable and specific
5. **Maintaining focus** - One main point per paragraph

**Five patterns handle most cases:**
- Definition + Importance (concepts)
- Action + Result (instructions)
- Problem + Solution (troubleshooting)
- Concept + Analogy (abstractions)
- Question + Answer (anticipated questions)

**Choose pattern based on Diátaxis mode and content type, not template-filling.**

**Integration point**: The `outline-expander` agent produces bullets; the `section-drafter` agent (Phase 4) converts them to topic sentences using this methodology.

---

## References

- Bain, A. (1866). *English Composition and Rhetoric*. Original composition theory.
- Brooks, C., & Warren, R.P. (1949). *Modern Rhetoric*. Topic sentence pedagogy.
- Minto, B. (2009). *The Pyramid Principle*. Integration with hierarchical thinking.
- Williams, J.M., & Bizup, J. (2017). *Style: Lessons in Clarity and Grace*. Modern application.
- Strunk, W., & White, E.B. (2000). *The Elements of Style*. Clarity and concision principles.
