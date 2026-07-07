# Writing Skills Library

**Version**: 1.1.0
**Type**: Skills Library Plugin
**Purpose**: Shared writing methodology skills for content frameworks

---

## Overview

The Writing Skills Library provides a centralized collection of proven writing methodologies that can be referenced by any content framework plugin. This eliminates duplication and provides a consistent set of techniques across all writing workflows.

## Philosophy

**Methodologies as shared resources, not duplicated components.**

Rather than each framework duplicating writing techniques, we extract proven methodologies into a shared library. Frameworks provide domain-specific workflows (positioning, research, drafting, review), while this library provides the underlying writing techniques.

---

## Skills Catalog

### 1. pyramid-principle
**Source**: Barbara Minto (McKinsey)
**Purpose**: Answer-first hierarchical structure
**Core Concept**: Start with the answer, then provide supporting arguments, then details

### 2. scqa-framework
**Source**: McKinsey/Minto
**Purpose**: Narrative structure for persuasive writing
**Structure**: Situation → Complication → Question → Answer

### 3. excellent-writing
**Source**: Multiple sources synthesized
**Purpose**: 15 core principles for clarity, precision, and engagement
**Covers**: Active voice, topic sentences, transitions, examples, coherence

### 4. diataxis-framework
**Source**: Daniele Procida
**Purpose**: Documentation mode selection based on user intent
**Modes**: Tutorial, How-To, Reference, Explanation

### 5. topic-sentence-method
**Source**: Academic writing tradition
**Purpose**: Paragraph structure with clear topic sentences
**Technique**: Each paragraph previews its content in the first sentence

### 6. information-mapping
**Source**: Robert Horn
**Purpose**: Chunking and scannability optimization
**Principles**: Chunking, labeling, consistency, relevance

### 7. plain-language
**Source**: Plain Language Movement
**Purpose**: Simplification and readability
**Techniques**: Active voice, short sentences, jargon elimination

### 8. seo-copywriting *(NEW in v1.1.0)*
**Source**: SEO best practices (Backlinko, Moz, Google)
**Purpose**: Content optimization for search engines and users
**Core Concepts**: Keyword placement, meta descriptions, heading hierarchy, E-E-A-T, search intent alignment
**Covers**: Title tags, URL structure, internal linking, long-tail keywords, schema markup

### 9. concise-web-copy *(NEW in v1.1.0)*
**Source**: Web usability research (Nielsen, Krug)
**Purpose**: Writing clear, impactful website content for scanners
**Techniques**: 50% test, active voice, bullet points, above-the-fold optimization
**Covers**: Landing pages, service descriptions, CTAs, mobile-first brevity

### 10. search-intent-alignment *(NEW in v1.1.0)*
**Source**: Modern SEO strategy
**Purpose**: Matching content to what users actually want when they search
**Four Intent Types**: Informational, Navigational, Transactional, Commercial Investigation
**Application**: SERP analysis, query modifiers, buyer journey mapping

---

## Usage

### As Plugin Dependency

Content frameworks can depend on this library:

```json
{
  "name": "content-marketing",
  "version": "1.2.0",
  "dependencies": ["writing-skills@local"]
}
```

### Direct Skill Invocation

When enabled, skills are accessible within Claude Code sessions:

```bash
# Reference skill in agent or command
skill:pyramid-principle
skill:diataxis-framework
skill:topic-sentence-method
```

### In Agent Definitions

Agents can reference skills for methodology guidance:

```markdown
## Skill References

Apply pyramid-principle for hierarchical structure.
Use scqa-framework for persuasive narrative.
Reference diataxis-framework for documentation mode selection.
```

---

## Installation

### As Plugin (Recommended)

Enable in your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "~/path/to/coding-agent-plugins"
      }
    }
  },
  "enabledPlugins": {
    "writing-skills@local": true
  }
}
```

### With Dependent Frameworks

Most content frameworks automatically enable writing-skills as a dependency. Check your framework's documentation for specific setup instructions.

---

## Dependent Frameworks

These frameworks leverage writing-skills:

- **content-marketing** v1.2+ - Marketing content production
- **ml3t-coauthor** v1.1+ - ML4T book production (optional)

Future frameworks can add writing-skills as a dependency to access these methodologies.

---

## Skill Details

Each skill is a markdown file providing:
- **Methodology overview** - Core concepts and principles
- **Application guidance** - When and how to use the technique
- **Examples** - Practical demonstrations
- **Common pitfalls** - What to avoid
- **References** - Original sources and further reading

---

## Design Principles

### 1. No Duplication
Each skill exists in exactly one location. Frameworks reference, not copy.

### 2. Framework Agnostic
Skills work with any writing workflow. No coupling to specific commands or agents.

### 3. Composable
Frameworks can pick which skills to use. No forced bundling.

### 4. Versioned
Skills evolve independently. Version compatibility clearly documented.

### 5. Well-Documented
Each skill includes theory, application, examples, and pitfalls.

---

## Version History

**v1.1.0** (2025-11-01):
- Added 3 SEO and web copy skills
- **seo-copywriting**: Technical SEO writing techniques for web content
- **concise-web-copy**: Landing page brevity and web scannability
- **search-intent-alignment**: Matching content to user search intent
- Total: 10 writing skills

**v1.0.0** (2025-11-01):
- Initial release
- 7 core writing methodology skills
- Extracted from content-marketing and structured-intelligence
- Eliminates skill duplication across frameworks

---

## Contributing

To add new skills or update existing ones:

1. Ensure skill is proven and widely applicable
2. Document methodology clearly with examples
3. Test with multiple frameworks
4. Update this README with skill catalog entry
5. Increment version appropriately (MINOR for new skills, PATCH for updates)

---

## Support

**Framework Integration**: See dependent framework documentation
**Skill Usage**: Reference individual skill files in `skills/` directory
**Issues**: Report to plugin marketplace maintainer

---

**Philosophy**: Shared methodologies, domain-specific workflows. Extract what's common, specialize what's unique.
