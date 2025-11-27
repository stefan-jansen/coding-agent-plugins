---
name: distinctive-design
description: Apply Anthropic's anti-AI-slop principles to create memorable, distinctive web interfaces. Use when frontend-engineer outputs feel generic or need elevation from "competent" to "memorable."
version: 1.0.0
---

# Distinctive Design Skill

This skill injects Anthropic's anti-"AI slop" design philosophy into your frontend work. Use it to elevate generic implementations into memorable, distinctive interfaces.

## When to Use This Skill

Invoke this skill when:
- Frontend code "works" but feels generic or forgettable
- You recognize Bootstrap/generic patterns in your output
- You want to evaluate whether a design is distinctive or "AI slop"
- Building hero sections, cards, layouts that need to stand out

## Core Philosophy

**Intentionality over intensity. Bold commitment over safe defaults.**

Every design choice should be **deliberate**. Generic choices (Inter font, centered layouts, uniform rounded corners) signal "I didn't think about this."

## The Anti-AI-Slop Checklist

Before finalizing any frontend work, verify:

### Typography

**AVOID (AI Slop):**
- Inter, Roboto, Arial, system fonts
- Same font for everything
- Default line-height and tracking

**DO INSTEAD:**
- Choose distinctive fonts that fit the project's tone
- Pair a display font (headlines) with a body font (content)
- Adjust line-height and letter-spacing intentionally

**Font Pairings for Applied AI Site:**
```css
/* Primary recommendation: Editorial authority meets modern clarity */
font-display: 'Instrument Serif', Georgia, serif;  /* Headlines */
font-body: 'Satoshi', system-ui, sans-serif;       /* Body text */

/* Alternative: Refined professional */
font-display: 'Cormorant Garamond', Georgia, serif;
font-body: 'Plus Jakarta Sans', system-ui, sans-serif;

/* Alternative: Modern distinctive */
font-display: 'Bebas Neue', Impact, sans-serif;
font-body: 'Inter Display', system-ui, sans-serif;  /* Display variant only */
```

### Color & Theme

**AVOID (AI Slop):**
- Purple gradients on white backgrounds
- Timid, evenly-distributed palettes
- Default DaisyUI theme colors

**DO INSTEAD:**
- Commit to a cohesive color identity
- Use **dominant colors with sharp accents**
- Build contrast through intentional color relationships

**Applied AI's Picasso Blue Period is GOOD:**
```css
/* Already distinctive - build on this */
--picasso-blue: #0a1628;      /* Deep, memorable primary */
--picasso-silver: #F8F8F6;    /* Warm contrast, not cold white */
--picasso-amber: #D4A574;     /* Warm accent, not generic blue CTA */
```

### Spatial Composition

**AVOID (AI Slop):**
- Everything centered
- Uniform 3-column grids
- Same padding on all sections
- `max-w-7xl mx-auto` everywhere

**DO INSTEAD:**
- Asymmetric layouts
- Grid-breaking elements
- Varying section widths
- Generous negative space OR controlled density (choose one)
- Overlapping elements for depth

**Break the Grid:**
```html
<!-- AVOID: Generic centered grid -->
<section class="py-16">
  <div class="max-w-7xl mx-auto">
    <h2 class="text-center">Title</h2>
    <div class="grid grid-cols-3 gap-8">
      <!-- identical cards -->
    </div>
  </div>
</section>

<!-- DO: Asymmetric, memorable layout -->
<section class="py-24">
  <div class="max-w-6xl ml-auto mr-8">  <!-- Offset right -->
    <h2 class="text-left text-6xl font-display">Title</h2>
  </div>
  <div class="mt-16 grid grid-cols-12 gap-4">
    <div class="col-span-5"><!-- Featured card, larger --></div>
    <div class="col-span-4 col-start-7"><!-- Secondary --></div>
    <div class="col-span-3 col-start-8 -mt-12"><!-- Overlapping --></div>
  </div>
</section>
```

### Motion & Animation

**AVOID (AI Slop):**
- Generic hover:shadow-xl
- Scattered micro-interactions
- Default fade-in on everything

**DO INSTEAD:**
- One well-orchestrated page load > many micro-interactions
- Staggered reveals with animation-delay
- Purposeful scroll-triggered animations
- Motion that guides attention

**Orchestrated Animation:**
```css
/* Staggered reveal on page load */
.reveal-item { opacity: 0; transform: translateY(20px); }
.reveal-item.visible {
  animation: reveal 0.6s ease forwards;
}
.reveal-item:nth-child(1) { animation-delay: 0ms; }
.reveal-item:nth-child(2) { animation-delay: 100ms; }
.reveal-item:nth-child(3) { animation-delay: 200ms; }

@keyframes reveal {
  to { opacity: 1; transform: translateY(0); }
}
```

### Backgrounds & Details

**AVOID (AI Slop):**
- Solid white backgrounds
- Basic linear gradients
- No texture or depth

**DO INSTEAD:**
- Grain/noise textures (aged-canvas feel for Picasso aesthetic)
- Layered transparencies
- Subtle patterns that reinforce identity
- Depth through shadow and layering

**Add Texture:**
```css
/* Subtle grain overlay - matches "Picasso" aged-canvas feel */
.grain-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/static/img/noise.png');
  opacity: 0.03;
  pointer-events: none;
}

/* Layered gradient for depth */
.depth-gradient {
  background:
    linear-gradient(180deg, rgba(10,22,40,0.02) 0%, transparent 30%),
    linear-gradient(0deg, rgba(10,22,40,0.05) 0%, transparent 20%);
}
```

## Applied AI Design Philosophy: "Analytical Warmth"

**Concept:** The visual language of rigorous analysis meets human-centered consulting.

**Visual Principles:**
1. **Deep blues and warm silvers** - Trust without coldness
2. **Editorial typography** - Authority (serif headlines) + clarity (sans body)
3. **Geometric accents** - Suggests structure and methodology
4. **Grain textures** - Human craft in digital precision
5. **Purposeful motion** - Guides, doesn't distract
6. **Asymmetric compositions** - Dynamic thinking, not template output

**What Makes It Unforgettable:**
The wave animation creates the "one thing someone remembers." Extend this through subtle geometric patterns and purposeful motion throughout. Each page should feel like a carefully crafted presentation.

## Component Patterns (Non-Generic)

### Cards That Stand Out

```html
<!-- AVOID: Generic Bootstrap card -->
<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-xl">
  <h3>Title</h3>
  <p>Content</p>
</div>

<!-- DO: Distinctive card with character -->
<article class="group relative bg-gradient-to-br from-white to-slate-50
               border-l-4 border-picasso-amber p-8
               hover:border-l-8 transition-all duration-300">
  <div class="absolute -top-3 left-6 text-6xl font-display text-picasso-blue/10">
    01
  </div>
  <h3 class="font-display text-2xl mt-4">Title</h3>
  <p class="text-slate-600 mt-2 leading-relaxed">Content</p>
  <div class="mt-6 flex items-center gap-2 text-picasso-amber
              opacity-0 group-hover:opacity-100 transition-opacity">
    <span class="text-sm font-medium">Explore</span>
    <svg class="w-4 h-4 transform group-hover:translate-x-1 transition-transform">
      <!-- arrow icon -->
    </svg>
  </div>
</article>
```

### Hero Sections That Command Attention

```html
<!-- AVOID: Generic centered hero -->
<section class="py-24 text-center">
  <h1 class="text-5xl font-bold">We Do AI</h1>
  <p class="mt-4 text-gray-600">Description here</p>
  <button class="mt-8 btn btn-primary">Get Started</button>
</section>

<!-- DO: Asymmetric hero with presence -->
<section class="min-h-screen relative overflow-hidden bg-picasso-blue">
  <!-- Wave animation layer (already exists) -->
  <canvas id="wave-canvas" class="absolute inset-0 z-0"></canvas>

  <div class="relative z-10 pt-32 pb-24 pl-8 md:pl-16 lg:pl-24">
    <div class="max-w-3xl">
      <p class="text-picasso-amber font-medium tracking-wide uppercase text-sm mb-6">
        Enterprise AI Consulting
      </p>
      <h1 class="font-display text-5xl md:text-7xl text-picasso-silver leading-tight">
        Transform Decisions<br/>
        <span class="text-picasso-amber">Into Results</span>
      </h1>
      <p class="mt-8 text-picasso-silver/80 text-xl max-w-xl leading-relaxed">
        We help business leaders deploy AI that actually works—
        predictable, measurable, trustworthy.
      </p>
      <div class="mt-12 flex flex-wrap gap-4">
        <a href="/contact" class="btn bg-picasso-amber text-white
                                   hover:bg-picasso-amber/90 border-none px-8">
          Start a Conversation
        </a>
        <a href="/services" class="btn btn-ghost text-picasso-silver
                                    border-picasso-silver/30 hover:bg-white/10">
          See Our Approach
        </a>
      </div>
    </div>
  </div>
</section>
```

### Lists That Have Rhythm

```html
<!-- AVOID: Simple bullet list -->
<ul class="list-disc pl-6 space-y-2">
  <li>Item one</li>
  <li>Item two</li>
</ul>

<!-- DO: List with visual rhythm -->
<ul class="space-y-6">
  <li class="flex items-start gap-4">
    <span class="flex-shrink-0 w-8 h-8 rounded-full bg-picasso-blue/10
                 flex items-center justify-center text-picasso-blue font-display">
      1
    </span>
    <div>
      <h4 class="font-medium text-slate-900">Item One</h4>
      <p class="text-slate-600 mt-1">Supporting description</p>
    </div>
  </li>
  <li class="flex items-start gap-4 relative">
    <div class="absolute left-4 -top-6 w-px h-6 bg-picasso-blue/20"></div>
    <span class="flex-shrink-0 w-8 h-8 rounded-full bg-picasso-blue/10
                 flex items-center justify-center text-picasso-blue font-display">
      2
    </span>
    <div>
      <h4 class="font-medium text-slate-900">Item Two</h4>
      <p class="text-slate-600 mt-1">Supporting description</p>
    </div>
  </li>
</ul>
```

## Quick Reference: AI Slop vs. Distinctive

| Element | AI Slop | Distinctive |
|---------|---------|-------------|
| **Font** | Inter, Roboto | Instrument Serif + Satoshi |
| **Layout** | Centered, symmetric | Asymmetric, offset |
| **Grid** | 3-col uniform | Varied spans, overlap |
| **Cards** | rounded-lg shadow-md | Border accents, numbered |
| **Motion** | hover:shadow-xl | Orchestrated page load |
| **Background** | bg-white | Grain texture, gradients |
| **Spacing** | py-16 everywhere | Varied: py-12 to py-32 |
| **Headlines** | text-4xl font-bold | text-6xl font-display |

## Integration with frontend-engineer Agent

This skill **enhances** the frontend-engineer agent, not replaces it.

**Workflow:**
1. **frontend-engineer** builds the technical implementation
2. **distinctive-design** skill evaluates and elevates
3. Apply distinctive patterns before finalizing

**Trigger phrase:** "Make this distinctive" or "Evaluate for AI slop"

## Resources

- Anthropic Skills Reference: `~/applied-ai/anthropic-skills/frontend-design/SKILL.md`
- Website Audit Report: `~/applied-ai/website/.claude/work/frontend-audit.md`
- Tailwind Config: `~/applied-ai/website/theme/static_src/tailwind.config.js`

---

*Distinctive Design Skill v1.0.0*
*Based on Anthropic's frontend-design principles*
*Adapted for Applied AI's Picasso Blue Period aesthetic*
