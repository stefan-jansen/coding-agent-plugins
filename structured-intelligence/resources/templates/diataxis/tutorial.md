# Diátaxis Template: Tutorial

**Mode**: Learning-Oriented
**Purpose**: Guide beginners through hands-on learning journey
**User Need**: "I want to learn how to do X"

## Template Structure

### 1. Introduction: What You'll Learn
- **Pattern**: State learning outcome explicitly
- **Tone**: Encouraging, supportive
- **Length**: 2-3 sentences

```markdown
In this tutorial, you'll learn {SKILL} by {APPROACH}. By the end, you'll be able to {OUTCOME}. No prior experience with {PREREQUISITE} required—we'll cover everything you need.
```

### 2. Prerequisites: What You Need
- **Pattern**: List required knowledge, tools, setup
- **Tone**: Clear, actionable
- **Format**: Bulleted checklist

```markdown
## Before You Begin

You'll need:
- {TOOL_1} installed ({VERSION})
- {TOOL_2} configured
- Basic understanding of {CONCEPT}
- Approximately {TIME} to complete
```

### 3. Step-by-Step Instructions
- **Pattern**: Action + Expected Result per step
- **Tone**: Active voice, imperative mood
- **Structure**: Numbered steps with sub-bullets

```markdown
## Step 1: {ACTION_VERB} {OBJECT}

{ACTION_SENTENCE}. Run this command:

```bash
{COMMAND}
```

You'll see output like this:
```
{EXPECTED_OUTPUT}
```

**What you accomplished**: {LEARNING_POINT}. This {SIGNIFICANCE}.
```

### 4. Verification: Check Your Work
- **Pattern**: How to confirm success
- **Tone**: Celebratory when successful
- **Format**: Test command + expected result

```markdown
## Verify Your Setup

Check that everything works:

```bash
{VERIFICATION_COMMAND}
```

✅ **Success**: You should see {SUCCESS_INDICATOR}
❌ **Troubleshooting**: If you see {ERROR}, try {FIX}
```

### 5. What You Learned: Reinforce Concepts
- **Pattern**: Recap key concepts from hands-on work
- **Tone**: Reflective, connecting practice to theory
- **Format**: Bulleted learnings with brief explanation

```markdown
## What You Learned

Through this tutorial, you learned:
- **{CONCEPT_1}**: {BRIEF_EXPLANATION}
- **{CONCEPT_2}**: {HOW_IT_WORKED_IN_PRACTICE}
- **{CONCEPT_3}**: {WHY_IT_MATTERS}
```

### 6. Next Steps: Continue Learning
- **Pattern**: Suggest progressive next tutorials
- **Tone**: Encouraging, builds confidence
- **Format**: Ordered list of increasing difficulty

```markdown
## Next Steps

Now that you've mastered {SKILL}, try these next:

1. **{NEXT_TUTORIAL_1}** - Build on what you learned
2. **{NEXT_TUTORIAL_2}** - Explore advanced techniques
3. **{REFERENCE_DOC}** - Deep dive into details

Ready to continue? Start with [{NEXT_TUTORIAL_1}]({LINK}).
```

## Key Principles

### DO: Tutorial Best Practices
✅ **Start simple**: Use the simplest possible example that demonstrates the concept
✅ **Guarantee success**: Every step should have verifiable success criteria
✅ **Explain why**: Connect actions to learning outcomes
✅ **Build progressively**: Each step builds on previous understanding
✅ **Celebrate wins**: Acknowledge completion of each milestone
✅ **Provide escape hatches**: Link to troubleshooting when things go wrong

### DON'T: Tutorial Anti-Patterns
❌ **Assume knowledge**: Don't skip prerequisites or assume "obvious" steps
❌ **Explain everything**: Don't deep-dive into theory (save for Explanation mode)
❌ **Give options**: Don't present multiple approaches—tutorials follow one path
❌ **Skip verification**: Don't move forward without confirming previous step worked
❌ **Dump code**: Don't provide large code blocks without explaining what they do
❌ **Lose focus**: Don't diverge into related topics—stay on learning path

## Topic Sentence Patterns

**Primary Pattern**: Action + Result
- "Create a new {COMPONENT} to {ACHIEVE_GOAL}."
- "Configure {SETTING} to enable {FEATURE}."
- "Run {COMMAND} to verify {OUTCOME}."

**Secondary Pattern**: Concept + Analogy (when introducing new concepts)
- "{CONCEPT} is {SIMPLE_DEFINITION}. Like {FAMILIAR_ANALOGY}, it {MAPPING}."

**Avoid**: Problem + Solution (too advanced), Definition + Importance (too abstract)

## Example Paragraph

**Good Tutorial Paragraph**:
```markdown
Create a new React component to display user information. Add a new file `UserProfile.tsx` in your `components/` directory:

```tsx
interface UserProfileProps {
  name: string;
  email: string;
}

export function UserProfile({ name, email }: UserProfileProps) {
  return (
    <div className="user-profile">
      <h2>{name}</h2>
      <p>{email}</p>
    </div>
  );
}
```

Save the file and run `npm start`. You'll see your new component available for import. **What you accomplished**: You created a reusable component that accepts props, a core React pattern you'll use throughout your applications.
```

**Analysis**:
- ✅ Action-oriented ("Create", "Add", "Save")
- ✅ Concrete code example with context
- ✅ Verification step ("run npm start")
- ✅ Learning reinforcement ("What you accomplished")
- ✅ Forward-looking ("pattern you'll use")

## Diátaxis Mode Integration

### When to Use Tutorial Mode
- **User Intent**: Learning-oriented, wants hands-on experience
- **User State**: Beginner or new to specific technology
- **Content Goal**: Build competence through practice
- **Success Metric**: User can reproduce the skill independently

### Relationship to Other Modes
- **Tutorial → How-To**: After learning basics, users apply skills to specific problems
- **Tutorial ← Explanation**: Deep understanding comes after hands-on practice
- **Tutorial → Reference**: Users look up specific details they encountered in tutorial

### Evidence Integration in Tutorials
- **Keep light**: Too much evidence disrupts learning flow
- **Use for confidence**: Cite when establishing best practices ("industry standard approach")
- **Example**: "TypeScript's type system catches 15% of bugs at compile time (Google 2017), which is why we're using it in this tutorial."

## Variable Placeholders

Replace these during content generation:

- `{SKILL}`: The skill being taught (e.g., "create React components")
- `{APPROACH}`: How skill is taught (e.g., "building a user profile")
- `{OUTCOME}`: What user can do after (e.g., "build your own reusable components")
- `{PREREQUISITE}`: Required background (e.g., "React")
- `{TOOL_1}`, `{TOOL_2}`: Required software (e.g., "Node.js v18+")
- `{TIME}`: Estimated completion time (e.g., "30 minutes")
- `{ACTION_VERB}`: Imperative action (e.g., "Create", "Configure", "Deploy")
- `{COMMAND}`: Code to run (e.g., "npm install react")
- `{EXPECTED_OUTPUT}`: What user should see (e.g., "✓ react@18.2.0")
- `{LEARNING_POINT}`: Concept taught (e.g., "components are reusable UI building blocks")
- `{NEXT_TUTORIAL_1}`: Logical next step (e.g., "Add State to Components")

## Usage by section-drafter Agent

1. **Load this template** when `diataxis_mode === "tutorial"`
2. **Apply structure patterns** to outline bullets
3. **Use topic sentence patterns** (Action + Result primarily)
4. **Maintain supportive tone** throughout
5. **Include verification steps** after action sequences
6. **Reinforce learning** with "What you accomplished" notes
7. **Build progressively** from simple to complex

## Quality Checklist

Before finalizing Tutorial content, verify:

- [ ] Every step has verifiable success criteria
- [ ] Code examples are complete and runnable
- [ ] Commands include expected output
- [ ] Learning outcomes explicitly stated
- [ ] Next steps provided for continued learning
- [ ] Tone is encouraging, not condescending
- [ ] Prerequisites clearly listed
- [ ] Estimated time provided
- [ ] Troubleshooting guidance included
- [ ] "What you learned" recap at end

---

**Template Version**: 1.0.0 (SIF Plugin)
**Last Updated**: 2025-10-27
**References**: Diátaxis Framework (Procida 2017), SIF skills/diataxis-framework/SKILL.md
