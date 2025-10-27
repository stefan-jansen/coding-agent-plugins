# DITA-Inspired Snippet Library

**Purpose**: Reusable content snippets for consistent CTAs, code blocks, evidence notes, and standard sections.

**Layer 3**: Content reuse mechanism (DITA-inspired conrefs)

---

## Usage

### In Outline (Phase 3)

Mark snippet insertion points:
```markdown
• Call to action
  [SNIPPET: cta-signup]
  Topic Sentence: "Sign up to receive updates on new content."
```

### In Draft (Phase 4)

`section-drafter` agent detects `[SNIPPET: name]` markers and inserts content from `snippets/[name].md`.

---

## Available Snippets

### cta-signup.md
Standard signup call-to-action with form placeholder.

### cta-contact.md
Contact call-to-action with email/social links.

### evidence-note.md
Disclosure note about evidence sources and transparency.

### code-block-python.md
Standard Python code block template with syntax highlighting.

### code-block-typescript.md
Standard TypeScript code block template.

### next-steps-tutorial.md
"Next Steps" section for tutorial endings.

### troubleshooting-template.md
Standard troubleshooting section structure.

---

## Creating New Snippets

1. Create `snippets/[name].md`
2. Write reusable markdown content
3. Use `{VARIABLE}` placeholders for customization
4. Reference in outline as `[SNIPPET: name]`

### Example Snippet

**File**: `snippets/api-endpoint-template.md`

```markdown
## API Endpoint: {ENDPOINT_NAME}

**Method**: `{HTTP_METHOD}`
**Path**: `{PATH}`

**Description**: {DESCRIPTION}

**Request Parameters**:
- {PARAM}: ({TYPE}) {DESCRIPTION}

**Response**:
```json
{EXAMPLE_RESPONSE}
```

**Errors**:
- {ERROR_CODE}: {ERROR_DESCRIPTION}
```

### Usage

```markdown
• GET /users endpoint
  [SNIPPET: api-endpoint-template]
  Variables:
    ENDPOINT_NAME: Get User List
    HTTP_METHOD: GET
    PATH: /api/v1/users
```

---

## Benefits

- **Consistency**: CTAs, code blocks, structures stay uniform
- **Efficiency**: Don't rewrite common elements
- **Maintainability**: Update snippet once, affects all uses
- **Quality**: Pre-written, reviewed content reduces errors

---

## Integration

**Phase 3** (`expand-outline`): Mark snippet insertion points
**Phase 4** (`section-drafter`): Insert snippets during drafting
**Phase 5** (`review-content`): Validates snippet consistency

---

## Snippet Library Location

`~/agents/plugins/structured-intelligence/resources/snippets/`

All snippets are markdown files with `.md` extension.
