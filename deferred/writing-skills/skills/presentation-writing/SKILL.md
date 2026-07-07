---
name: presentation-writing
description: Plan and write presentation CONTENT — narrative arc, one message per slide, headlines, supporting bullets/figures, speaker notes — in a sober, distilled, technical register (graduate textbook, not marketing deck). Use whenever the user wants to build, outline, draft, structure, tighten, or rewrite a deck, slides, talk, lecture, or teaching material — even if they don't say "skill," and even when the output is a .pptx. Establish deck thesis, audience, section arc, and per-slide contract BEFORE drafting slide text; ground every claim in a source; hand rendering and layout to a pptx/render skill.
---

# Presentation Writing

A slide is a structured claim, supported by the minimum evidence the audience needs to understand it, believe it, and remember it. A deck is an argument delivered in installments.

The goal is not to sound clever, and not to cover a topic. The goal is clarity through **distillation**: the fewest words that carry the message, every one of them true. Less is usually more. Explain when the idea genuinely needs it; default to less.

Work in two passes — get the **structure** right (arc → headlines), then the **language** right (register → bullets). The most common failure is jumping to bullets before the spine is sound.

---

## 1. Workflow (top-down, then refine)

Each step is cheap to revise; later steps are expensive. Do them in order.

**Frame it.** Before any slides, write one short paragraph: the **audience** (what they already know; what gap or misconception you are correcting) and the **core promise** in one sentence — "After this session, the audience should understand that…". If the promise needs two sentences, the talk has two talks in it.

**Build the spine.** Decompose the promise into **4–6 sections, maximum**. Write each as a *one-sentence claim*, not a topic. Read the section claims in order: they should form an argument that reaches the promise.

**Write headlines only.** For each slide write *only* the headline (§5), nothing else yet. Then run two tests:
- **Read-through (global):** read every headline top to bottom, ignoring bodies. They should narrate the deck alone. A gap, a non sequitur, or a deletable headline means the *structure* is wrong — fix it now.
- **Adjacency (local):** each slide connects to the one before and after, or it is cut or merged.

This is the highest-leverage moment in the process. Get it right before writing a bullet.

**Choose the support.** Only now fill each slide. Pick the *one* form that best proves the headline (§7). Bullets are the fallback for genuinely list-like content, not the default.

**Prune.** Enforce the limits (§6). Move every caveat, derivation, and aside to speaker notes (§8).

```
Deck thesis
  Section claim
    Slide message
      Evidence, mechanism, example, or visual support
```

---

## 2. Every slide has a contract

Each slide answers four questions:

1. **What is the message?** The headline states the point; it does not name the topic.
2. **Why should the audience believe it?** A figure, table, equation, example, or bullets support it.
3. **What is read first?** One obvious entry point; understanding does not require reading everything.
4. **Why is this slide here?** It advances the argument and connects to its neighbors.

**One message per slide.** Two ideas means two slides. Everything else follows from this.

---

## 3. Ground every claim

Every specific on a slide — a number, a name, a mechanism, a result — must be true and traceable to a source. **Verify it before you write it.**

The failure mode is reaching for a plausible-sounding word to fill a slot: labeling an FX strategy *carry* when there is no rates data; calling nine case studies *nine markets* when several share one market; writing *"the strongest result is an artifact"* — fluent, and empty. A sentence that reads coherently but drifts from the facts is worse than a plain true one.

If you cannot verify a specific, cut it or leave it for the speaker. **Report what is true; do not generate what sounds true.**

---

## 4. Calibrate to the audience

Know what the room already knows. The headline must be **non-obvious to this audience**. If a practitioner would think "obviously," the slide is wasted — cut it, or find the non-obvious turn.

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

Good headlines are 6–12 words, concrete, specific to the slide, free of hype, jokes, and slogans.

**Fit the headline on one line.** Word count is not length — an 11-word headline can still wrap. A title that breaks to a second line and strands a one- or two-word orphan (*"…read the / future"*) reads as unfinished. Rank order:

1. **One line — the strong default.** If it doesn't fit, *make it shorter*: cut a qualifier, not the meaning. Shortening a headline is almost always an improvement, not a sacrifice.
2. **Two full, balanced lines at a smaller headline size** — only when the claim genuinely needs the words. Balance the break so neither line is a lone orphan, and step the H1 size down so it reads as a deliberate two-line title, not an overflow.

Never accept a headline that wraps to a ragged second line at the default size.

**Know the budget before you write, so you don't iterate.** Estimate characters-per-line as `usable_width_px / (0.52 × headline_px)` — the 0.52 is roughly the title-case average advance of a bold sans (Inter/Helvetica), letter-spacing included. Write *to* that number: if the budget is ~40 characters, aim for ≤ 36 to absorb wide-letter variance. Record the per-theme, per-archetype budget once in the project's brand/typography docs and reuse it — e.g. an ml4t Marp course deck records content-slide H1 ≈ **40 chars** (target ≤ 36) in `production/brand/typography.md`.

---

## 6. Bullets and density (defaults, not laws)

A bullet earns its place only if it does **one of four jobs**: define a distinction · identify a mechanism · name a failure mode · state an implication. A bullet that restates the headline does none of these — cut it.

Default limits:
- **3–5 bullets** per slide; 6 is the ceiling. Fewer than 3 — ask whether you need bullets at all.
- **6–12 words** per bullet; **2 lines maximum**. A third line is a paragraph in disguise.
- **~55–75 words of slide text total.** No paragraphs.
- **One level of nesting**; two is the hard maximum.

Craft: keep bullets **parallel** (same grammatical kind), make each **stand alone**, and **front-load the informative word**. Fragments, not sentences.

**Reading budget:** the gist in ~3 seconds, the full slide in ~10–15 while still listening. Reading and listening compete; if the slide demands reading, the speaker has lost the room.

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

## 8. Speaker notes carry the nuance

Slides carry the message; notes carry what would crowd it — caveats, examples, derivations, references, edge cases, implementation detail. A good slide is understood in 10–15 seconds; the spoken explanation can take minutes. Pruned material is relocated, not lost.

---

## 9. Voice: sober, literal, distilled

Target a graduate technical-textbook register. Direct, analytical, practitioner-oriented, sophisticated without jargon-stacking.

**Terms of art vs. jargon.** Correct domain vocabulary — *embargo*, *information coefficient*, *walk-forward* — is expected; define on first use if needed. Jargon is obscurity for its own sake, or a fancy word where a plain one is exact. Reach for the plain word.

**Sentence style.** Short, declarative, active.
- Prefer: "Overlapping labels reduce the independence of validation observations."
- Avoid the passive inversion, and avoid throat-clearing ("It is important to note that…").

**The figurative rule.** The enemy is *figurative and dramatized* language, not punch. A sharp, literal claim is excellent. A metaphor about death, war, magic, secrets, or domination — or a marketing verb — breaks the register, however true the point.
- Don't: "Data is where strategies die" · "this mistake kills your backtest" · "unlock alpha" · "the model crushes the benchmark."
- Do: "A back-adjustment choice can flip a model's sign" · "a timing error can invalidate a backtest" · "feature design sets the information available to the model" · "the model improves on the benchmark under these validation conditions."

Also avoid: intensifiers (*massively*, *huge*, *game-changing*), exclamation marks, emoji, rhetorical-question headlines, and vague quantifiers (*a lot of*, *tons of*).

---

## 10. Self-check before accepting a slide

1. Read the headlines alone — do they tell the whole story?
2. One message per slide, one obvious entry point?
3. Headline a claim (argument slide) or a clean label (fact slide) — never decoration?
4. Every specific true and traceable to a source — no filler that merely sounds right?
5. Non-obvious to *this* audience — no table-stakes explained back, no dramatized basics?
6. Contrast headlines used sparingly — not several in one deck running on the same negation?
7. Headline fits one line at the default size — no wrap to a ragged orphan (else shorten it, or commit to two balanced lines at a smaller size)?
8. Bullets do one of the four jobs, stand alone, parallel; within density and reading budget?
8. Tables: each column one dimension; detail moved to notes?
9. Voice sober and literal — terms correct, no hype, no figurative framing?

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
  Speaker notes: ...
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
