# Diátaxis Template: Reference

**Mode**: Information-Oriented
**Purpose**: Provide comprehensive, factual information for lookup
**User Need**: "I need to know X"

## Template Structure

### 1. Overview: What This Documents
- **Pattern**: Scope and purpose statement
- **Tone**: Neutral, authoritative
- **Length**: 1-2 sentences

```markdown
{COMPONENT_NAME} provides {FUNCTIONALITY}. This reference documents all {ELEMENTS} with complete specifications and examples.
```

### 2. Quick Reference: At-a-Glance Summary
- **Pattern**: Table or list of key facts
- **Tone**: Dense, scannable
- **Format**: Table or definition list

```markdown
## Quick Reference

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| {PROPERTY_1} | {TYPE} | {DEFAULT} | {BRIEF_DESC} |
| {PROPERTY_2} | {TYPE} | {DEFAULT} | {BRIEF_DESC} |

**Common usage**: `{TYPICAL_INVOCATION}`
```

### 3. Detailed Specifications
- **Pattern**: Comprehensive coverage of each element
- **Tone**: Precise, unambiguous
- **Structure**: Subsections per element

```markdown
## {ELEMENT_NAME}

**Signature**: `{FUNCTION_SIGNATURE}`

**Description**: {WHAT_IT_DOES}. {BEHAVIOR_DETAILS}.

**Parameters**:
- `{PARAM_1}` ({TYPE}, {REQUIRED/OPTIONAL}, default: {DEFAULT}): {DESCRIPTION}. {CONSTRAINTS}.
- `{PARAM_2}` ({TYPE}, {REQUIRED/OPTIONAL}): {DESCRIPTION}. {VALID_VALUES}.

**Returns**: {RETURN_TYPE} - {RETURN_DESCRIPTION}

**Raises**:
- `{EXCEPTION_1}`: {WHEN_RAISED}
- `{EXCEPTION_2}`: {WHEN_RAISED}

**Example**:
```{LANGUAGE}
{CODE_EXAMPLE}
// Output: {EXPECTED_OUTPUT}
```

**See Also**: {RELATED_ELEMENT_1}, {RELATED_ELEMENT_2}
```

### 4. Configuration Options
- **Pattern**: Complete listing with descriptions
- **Tone**: Technical, exhaustive
- **Format**: Subsections or tables

```markdown
## Configuration

### {CONFIG_OPTION_1}

**Type**: {DATA_TYPE}
**Default**: {DEFAULT_VALUE}
**Valid Values**: {VALID_RANGE_OR_ENUM}

{DETAILED_DESCRIPTION}. {BEHAVIOR_IMPLICATIONS}.

**Example**:
```{FORMAT}
{CONFIG_EXAMPLE}
```

**Recommendation**: Set to {RECOMMENDED_VALUE} for {USE_CASE}.
```

### 5. Data Structures
- **Pattern**: Complete schema with all fields
- **Tone**: Formal, precise
- **Format**: Code block + field descriptions

```markdown
## Data Structures

### {STRUCTURE_NAME}

```{LANGUAGE}
{TYPE_DEFINITION}
```

**Fields**:
- `{FIELD_1}` ({TYPE}): {DESCRIPTION}. {CONSTRAINTS}.
- `{FIELD_2}` ({TYPE}): {DESCRIPTION}. {VALID_VALUES}.
- `{FIELD_3}` ({TYPE}, optional): {DESCRIPTION}. {DEFAULT_BEHAVIOR_IF_OMITTED}.

**Invariants**:
- {CONSTRAINT_1}
- {CONSTRAINT_2}
```

### 6. Edge Cases and Boundaries
- **Pattern**: Document behavior at limits
- **Tone**: Cautionary, complete
- **Format**: Bulleted or table

```markdown
## Edge Cases

| Condition | Behavior |
|-----------|----------|
| {EDGE_CASE_1} | {WHAT_HAPPENS} |
| {EDGE_CASE_2} | {WHAT_HAPPENS} |
| {EDGE_CASE_3} | {WHAT_HAPPENS} |

**Important**: {CRITICAL_LIMITATION}. {WORKAROUND_IF_ANY}.
```

## Key Principles

### DO: Reference Best Practices
✅ **Be comprehensive**: Document everything, even "obvious" details
✅ **Use consistent structure**: Same format for similar elements
✅ **Provide types**: Specify data types for all parameters/returns
✅ **List constraints**: Document valid ranges, required formats
✅ **Include examples**: Show correct usage for each element
✅ **Cross-reference**: Link related elements
✅ **State defaults**: Always specify default values
✅ **Document edge cases**: Explain behavior at boundaries

### DON'T: Reference Anti-Patterns
❌ **Explain concepts**: Don't teach (use Explanation mode)
❌ **Provide guidance**: Don't recommend when to use (use How-To)
❌ **Tell stories**: Don't add narrative (stay factual)
❌ **Hide details**: Don't omit "advanced" features
❌ **Use vague terms**: Don't say "large number" (specify limits)
❌ **Assume knowledge**: Don't skip parameter descriptions

## Topic Sentence Patterns

**Primary Pattern**: Definition + Importance
- "`{ELEMENT}` ({TYPE}) {WHAT_IT_DOES}. {WHY_IT_EXISTS_OR_IMPLICATIONS}."
- "`{CONFIG_OPTION}` controls {BEHAVIOR}. Set this to {VALUE} when {CONDITION}."

**Secondary Pattern**: Question + Answer (for configuration decisions)
- "When should you set `{OPTION}` to {VALUE}? Use {VALUE} when {CONDITION}."

**Avoid**: Action + Result (too instructional), Concept + Analogy (too abstract), Problem + Solution (too narrative)

## Example Entry

**Good Reference Entry**:
```markdown
## maxConnections

**Type**: `integer`
**Default**: `10`
**Valid Range**: `1-1000`

`maxConnections` caps the maximum number of concurrent database connections the pool can maintain. When this limit is reached, new connection requests wait in a queue until an existing connection is released.

**Configuration**:
```yaml
database:
  maxConnections: 20
```

**Calculation**: Set to `database_connection_limit / application_instance_count`. For example, PostgreSQL's default 100-connection limit with 5 application instances yields `maxConnections=20` per instance.

**Edge Cases**:
- If set to `1`: Serializes all database operations (eliminates concurrency)
- If exceeds database limit: Connection requests fail with `FATAL: remaining connection slots are reserved`
- If set above `1000`: Pool overhead may degrade performance

**Performance Impact**: Higher values increase memory usage (~10KB per connection). Lower values reduce throughput under load.

**See Also**: `minConnections`, `connectionTimeout`
```

**Analysis**:
- ✅ Type and valid range specified
- ✅ Default value stated
- ✅ Behavior described precisely
- ✅ Configuration example shown
- ✅ Calculation guidance provided
- ✅ Edge cases documented
- ✅ Performance implications noted
- ✅ Related config cross-referenced
- ✅ Neutral tone, no opinions

## Diátaxis Mode Integration

### When to Use Reference Mode
- **User Intent**: Information-seeking, needs factual details
- **User State**: Competent, knows what to look up
- **Content Goal**: Provide complete, authoritative specification
- **Success Metric**: User finds needed information quickly

### Relationship to Other Modes
- **Reference ← Tutorial**: User encountered element in tutorial, looks up details
- **Reference ↔ How-To**: User switches between How-To steps and Reference lookups
- **Reference ← Explanation**: After understanding concept, user refers back for specifics

### Evidence Integration in Reference
- **Use for specifications**: Cite standards, official docs
- **Example**: "Complies with JSON Schema Draft 2020-12 specification"
- **Use for limits**: Cite benchmarks for performance characteristics
- **Example**: "Handles up to 100,000 concurrent connections (AWS ECS benchmark, 2023)"
- **Keep factual**: Evidence should establish facts, not persuade

## Variable Placeholders

Replace these during content generation:

- `{COMPONENT_NAME}`: What's being documented (e.g., "Connection Pool API")
- `{FUNCTIONALITY}`: What it does (e.g., "manages database connections")
- `{ELEMENTS}`: What's documented (e.g., "configuration options and methods")
- `{PROPERTY_N}`: Property name (e.g., "maxConnections")
- `{TYPE}`: Data type (e.g., "integer", "string", "boolean")
- `{DEFAULT}`: Default value (e.g., "10", "null", "true")
- `{ELEMENT_NAME}`: Function/method/class name
- `{FUNCTION_SIGNATURE}`: Complete signature with types
- `{PARAM_N}`: Parameter name
- `{REQUIRED/OPTIONAL}`: Whether parameter is required
- `{CONSTRAINTS}`: Valid ranges, formats, patterns
- `{RETURN_TYPE}`: What function returns
- `{EXCEPTION_N}`: Exception/error name
- `{WHEN_RAISED}`: Conditions triggering exception
- `{CONFIG_OPTION_N}`: Configuration setting name
- `{VALID_RANGE_OR_ENUM}`: Allowed values
- `{STRUCTURE_NAME}`: Data structure name (e.g., "UserConfig")
- `{FIELD_N}`: Field in data structure
- `{EDGE_CASE_N}`: Boundary condition
- `{WHAT_HAPPENS}`: Behavior at edge case

## Usage by section-drafter Agent

1. **Load this template** when `diataxis_mode === "reference"`
2. **Use Definition + Importance** topic sentence pattern
3. **Maintain neutral tone** - no opinions or guidance
4. **Be comprehensive** - document all elements, even obvious ones
5. **Use consistent structure** - same format for similar elements
6. **Include types always** - never omit data types
7. **Provide examples** - show correct usage for each element
8. **Cross-reference** - link related elements
9. **Document edge cases** - explain behavior at boundaries

## Quality Checklist

Before finalizing Reference content, verify:

- [ ] All elements documented (no omissions)
- [ ] Data types specified for all parameters/returns
- [ ] Default values stated explicitly
- [ ] Valid ranges/constraints documented
- [ ] Examples provided for each element
- [ ] Edge cases and boundaries covered
- [ ] Errors/exceptions documented with conditions
- [ ] Cross-references to related elements included
- [ ] Neutral tone maintained (no "should/shouldn't")
- [ ] Consistent structure across similar elements
- [ ] Technical accuracy verified
- [ ] Scannable format (tables, lists, code blocks)

---

**Template Version**: 1.0.0 (SIF Plugin)
**Last Updated**: 2025-10-27
**References**: Diátaxis Framework (Procida 2017), SIF skills/diataxis-framework/SKILL.md
