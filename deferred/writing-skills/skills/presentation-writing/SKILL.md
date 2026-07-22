---
name: presentation-writing
description: Plan and write presentation CONTENT - narrative arc, one message per slide, meaningful headlines, complete on-slide support, and optional speaker notes - in a sober technical register. Use whenever the user wants to build, outline, draft, structure, tighten, or rewrite a deck, slides, talk, lecture, or teaching material, even when the output is a .pptx. Establish audience, outcomes, section arc, and per-slide contract BEFORE drafting slide text; ground every claim in a source; hand rendering and layout to a pptx/render skill.
---

# Presentation Writing

A slide communicates one complete teaching message. Its headline identifies the subject or supported
conclusion; its body supplies the definitions, attributes, mechanism, comparison, example, evidence,
implication, or action needed to understand that message. A deck develops an explanation or argument
in installments.

The goal is clarity through **distillation**, not minimalism. Use the least text that preserves the
complete meaning for a cold reader. Concision cannot remove the context required to identify the
object, understand the terminology, or follow the reasoning. A sparse slide is not automatically a
clear slide.

Work in two passes: get the **structure** right (arc to headlines), then the **language** right
(register to bullets). The most common failure is jumping to bullets before the spine is sound.

---

## 1. Workflow (top-down, then refine)

Each step is cheap to revise; later steps are expensive. Do them in order.

**Frame it.** Before any slides, write one short paragraph describing the **audience**, what they
already know, and what the session adds. State one to three concrete outcomes: what the audience
should understand, decide, produce, or be able to do afterward. A substantial teaching session can
have several related outcomes; compressing them into one slogan hides the actual scope.

**Build the spine.** Decompose the outcomes into a small number of sections. Name each section in
literal terms or state a specific conclusion it establishes. Read the section sequence in order: it
should explain how the session reaches the outcomes without relying on unexplained shorthand.

**Write headlines only.** For each slide write *only* the headline (§5), nothing else yet. Then run two tests:
- **Read-through (global):** read every headline top to bottom, ignoring bodies. They should narrate the deck alone. A gap, a non sequitur, or a deletable headline means the *structure* is wrong — fix it now.
- **Adjacency (local):** each slide connects to the one before and after, or it is cut or merged.

This is the highest-leverage moment in the process. Get it right before writing a bullet.

**Choose the support.** Only now fill each slide. Pick the *one* form that best proves the headline (§7). Bullets are the fallback for genuinely list-like content, not the default.

**Complete, then prune.** Remove repetition and delivery-only asides, but keep everything a reader
needs to understand the slide. Speaker notes are optional and must never contain definitions,
qualifications, or reasoning required to decode the rendered slide (§8).

```
Deck thesis
  Section claim
    Slide message
      Evidence, mechanism, example, or visual support
```

---

## 2. Every slide has a contract

Each slide answers four questions:

1. **What is the message?** The headline names the subject or states a supported conclusion.
2. **Why should the audience believe it?** A figure, table, equation, example, or bullets support it.
3. **What is read first?** One obvious entry point; understanding does not require reading everything.
4. **Why is this slide here?** It advances the argument and connects to its neighbors.

5. **Can a cold reader understand it?** Terms are defined on this slide or were explicitly defined
   earlier; the body makes the relationship among the elements clear.

**One message per slide does not mean one sentence per slide.** A message often needs several
attributes, steps, comparisons, or pieces of evidence. Split genuinely independent ideas; do not
strip a single idea of the context that makes it intelligible.

---

## 3. Ground every claim

Every specific on a slide — a number, a name, a mechanism, a result — must be true and traceable to a source. **Verify it before you write it.**

The failure mode is reaching for a plausible-sounding word to fill a slot: labeling an FX strategy *carry* when there is no rates data; calling nine case studies *nine markets* when several share one market; writing *"the strongest result is an artifact"* — fluent, and empty. A sentence that reads coherently but drifts from the facts is worse than a plain true one.

If you cannot verify a specific, cut it or label it as unresolved. Do not move an unsupported or
necessary claim into narration. **Report what is true; do not generate what sounds true.**

---

## 4. Calibrate to the audience

Know what the room already knows, but preserve the context needed to locate each idea in the session.
A familiar concept may earn a slide when it defines the shared vocabulary, connects two stages, or
supports a later technical decision. Do not manufacture a dramatic "non-obvious" turn to justify it.

Do not explain table-stakes back to experts — that point-in-time data matters, that survivorship bias exists. It is on every blog, and in the training data of any model writing the slide. Earning the slot means saying something they do not already know: not *"point-in-time matters"* but *"a back-adjustment choice can flip a model's sign."*

Never talk down, and never dramatize a basic point to make it feel like an insight.

---

## 5. Headlines: a claim, or a clean label — never decoration

For an **argument slide**, the headline is an assertion: it states the point, not the topic. For a **fact slide** — a dataset, an inventory, a reference table — a clean descriptive label plus consistent data beats a manufactured claim. Do not force an assertion onto a menu.

| Don't (label, on an argument slide) | Do (assertion) |
|---|---|
| Point-in-Time Data | Point-in-time data prevents impossible trading decisions |
| Cross-Validation | Cross-validation must respect the trading clock |
| Results | Performance decays once leakage is removed |

**Distill; don't lean on contrast.** The *"A, not B"* / *"measures X, not Y"* shape is a legitimate tool — *"Backtesting is falsification, not confirmation"* is sharp because the contrast *is* the point. Nothing here is forbidden. The fault is **overuse and repetition**: when several headlines in one deck run on the same negation, it stops carrying meaning and reads as a verbal tic. Budget it — once or twice per deck, where the distinction is real and the audience genuinely conflates the two. Everywhere else, state the thing directly: prefer *"Costs decide what survives"* over *"Cost modeling, not the model, decides what survives."* And watch the weak cases — *"A prediction is not a trade"* is well-intended but borderline obvious; either earn it or cut it.

Generative forms to pattern against (all direct, none built on negation):
```
[Technical choice] determines [practical consequence]
[Model behavior] depends on [data or validation condition]
[Process step] reduces [specific failure mode]
[Artifact] estimates [a process]
```

Good headlines are concrete, specific to the slide, free of hype, jokes, and slogans. Prefer a clean
descriptive label when an assertion would be manufactured. A conclusion belongs in the headline only
when the slide supplies the evidence or mechanism that supports it.

**Fit the headline on one line.** Word count is not length — an 11-word headline can still wrap. A title that breaks to a second line and strands a one- or two-word orphan (*"…read the / future"*) reads as unfinished. Rank order:

1. **One line - the strong default.** If it does not fit, first remove repetition or an empty
   qualifier. Never cut the object, condition, or consequence that gives the headline meaning.
2. **Two full, balanced lines at a smaller headline size** — only when the claim genuinely needs the words. Balance the break so neither line is a lone orphan, and step the H1 size down so it reads as a deliberate two-line title, not an overflow.

Never accept a headline that wraps to a ragged second line at the default size. This is a rendered
visual check, not a word-count exercise.

**Know the budget before you write, so you don't iterate.** Estimate characters-per-line as `usable_width_px / (0.52 × headline_px)` — the 0.52 is roughly the title-case average advance of a bold sans (Inter/Helvetica), letter-spacing included. Write *to* that number: if the budget is ~40 characters, aim for ≤ 36 to absorb wide-letter variance. Record the per-theme, per-archetype budget once in the project's brand/typography docs and reuse it — e.g. an ml4t Marp course deck records content-slide H1 ≈ **40 chars** (target ≤ 36) in `production/brand/typography.md`.

---

## 6. Bullets, completeness, and density

A bullet earns its place only if it does **one of four jobs**: define a distinction · identify a mechanism · name a failure mode · state an implication. A bullet that restates the headline does none of these — cut it.

Use as many bullets as the message requires, usually three to six. Each bullet should express one
complete attribute, mechanism, distinction, or implication. Aim for one clean rendered line or an
intentional two-line block; occasional longer bullets are acceptable when the technical meaning
requires them. Avoid a run of bullets that each leave one word on a second line.

Do not enforce a universal word count. Appropriate density depends on the slide type:

- A table or annotated figure may carry most of the explanation.
- A conceptual slide often needs several complete bullets plus a definition or example.
- An agenda or reference slide should favor explicit labels over compressed claims.
- A single-sentence slide is a rare deliberate pause, not a substitute for an introduction,
  explanation, or agenda.

Use one level of nesting by default. Use a second level only when the hierarchy is genuinely part of
the idea.

Craft: keep bullets **parallel** where appropriate, make each understandable on its own, and
front-load the informative words. Fragments and sentences are both valid. Choose the form that
states the content most clearly.

**Reading budget:** establish the gist quickly, then let the audience inspect the supporting detail.
Reading and listening compete, but a slide deck is also a durable course artifact. A student should
be able to revisit the rendered slide later without reconstructing the missing lecture.

```
Headline: Cross-validation must respect the trading clock
- Training data must precede validation data     (mechanism)
- Overlapping labels break observation independence   (failure mode)
- Tuning decisions can leak across folds         (failure mode)
- Metric stability matters more than single-fold accuracy   (implication)
```

---

## 7. Prefer structure over words

When a slide has too much text, ask whether the idea is better shown as structure:

```
Explains a relationship  → diagram
Lists parallel facts     → bullets
Compares alternatives    → table
Shows a sequence         → flow / timeline
Shows where things break → pipeline diagram with failure points
Rests on one result      → chart with ONE emphasized takeaway
Rests on one idea        → a single number or a minimal annotated equation
```

For a figure, say *what it shows* in the headline ("Returns decay with holding period"), never "Results." One primary figure per slide.

**Tables:** every column is one consistent dimension and every cell the same kind of thing. A column that holds a data source on one row, a property on the next, and a date range on a third is padding — split it into real columns or cut it.

---

## 8. Speaker notes are optional

Slides carry the complete teaching message. Notes may contain timing, delivery cues, additional
examples, optional derivations, or answers to likely questions. They must not carry definitions,
conditions, caveats, source qualifications, or reasoning that the audience needs to understand the
rendered artifact. When the project does not use speaker notes, nothing is missing from the slides.

---

## 9. Voice: sober, literal, distilled

Target a graduate technical-textbook register. Direct, analytical, practitioner-oriented, sophisticated without jargon-stacking.

**Terms of art vs. jargon.** Correct domain vocabulary such as *embargo*, *information
coefficient*, and *walk-forward* is expected; define it on first use if needed. Jargon is obscurity
for its own sake, or a fancy word where a plain one is exact. Reach for the plain word.

**Sentence style.** Short, declarative, active.
- Prefer: "Overlapping labels reduce the independence of validation observations."
- Avoid the passive inversion, and avoid throat-clearing ("It is important to note that…").

**The figurative rule.** The enemy is *figurative and dramatized* language, not punch. A sharp,
literal claim is excellent. A metaphor about death, war, magic, secrets, or domination, or a
marketing verb, breaks the register, however true the point.
- Don't: "Data is where strategies die" · "this mistake kills your backtest" · "unlock alpha" · "the model crushes the benchmark."
- Do: "A back-adjustment choice can flip a model's sign" · "a timing error can invalidate a backtest" · "feature design sets the information available to the model" · "the model improves on the benchmark under these validation conditions."

Also avoid: intensifiers (*massively*, *huge*, *game-changing*), exclamation marks, emoji, rhetorical-question headlines, and vague quantifiers (*a lot of*, *tons of*).

**Punctuation.** Do not use em dashes. Use a colon, comma, semicolon, parentheses, or a plain hyphen.

---

## 10. Self-check before accepting a slide

1. Read the headlines alone - do they identify the full sequence and subject matter without hidden
   context?
2. One complete message per slide, not merely one sentence, with one obvious entry point?
3. Headline a supported conclusion or a clean literal label - never decoration or a manufactured
   claim?
4. Every specific true and traceable to a source — no filler that merely sounds right?
5. Non-obvious to *this* audience — no table-stakes explained back, no dramatized basics?
6. Contrast headlines used sparingly — not several in one deck running on the same negation?
7. Headline renders as one clean line or intentional balanced lines, with no ragged orphan?
8. Bullets and other support provide the definitions, mechanism, evidence, implication, and action
   needed for a cold reader?
9. Secondary text uses normal hierarchy unless it is strictly citation or provenance?
10. No isolated bottom takeaway competes with the headline?
11. Tables: each column one dimension, with enough context on the slide to interpret it?
12. Voice sober and literal - terms correct, no hype, no figurative framing?

If any item fails, revise.

---

## 11. Output format for agents

Never produce a slide as an isolated list of bullets. Produce the structure first, then drafts:

```
Deck thesis: ...
Audience: ...
Section arc:
1. <one-sentence claim>   (4–6 sections)

Slide plan:
Slide N: <headline>
  Purpose: <role in the arc>
  Support: <bullets | figure | table | equation>

Slide drafts:
Slide N:
  Headline: ...
  Bullets:
  - ...
  Optional speaker notes: ...
```

**For the invoking human:** don't ask for "slides" from content directly. Ask first for the thesis, section arc, and slide plan; approve those; *then* let the agent draft slide text. This forces the hierarchical reasoning the rest of this skill depends on.

---

## Worked example (technical register)

**Thesis:** A backtest's headline Sharpe mostly measures your methodology, not your strategy.
**Section claim:** Most backtest performance is manufactured by leakage.

- **Slide** — *Headline:* "A backtest measures your methodology before your edge."
  - Look-ahead bias inflates returns before any trade   (failure mode)
  - Survivorship-filtered universes delete the losers in advance   (failure mode)
  - Parameter search overfits noise that will not recur   (mechanism)
- **Slide** — *Headline:* "Standard k-fold cross-validation puts the future in the training set."
  - Random folds train on data that postdates the test   (mechanism)
  - Autocorrelation makes adjacent observations near-duplicates   (mechanism)
  - Purging and embargo restore the temporal boundary   (implication)
- **Slide (figure)** — *Headline:* "Performance decays once leakage is removed."
  - Support: equity curves, naive k-fold vs. purged walk-forward; annotate the gap.

Headlines alone narrate the section; each bullet stands on its own and does one of the four jobs; the register stays literal and grounded.

---

## Handoff to rendering

Once structure and writing are approved, pass the per-slide spec — headline, chosen support, speaker notes — to the **pptx/render skill** for generation, layout, and visual design. Keep this skill's writing discipline through the handoff; let the renderer own styling, not wording.
