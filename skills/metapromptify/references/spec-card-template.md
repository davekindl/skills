# Tool Spec Card Template

Fill this out for any tool you want to metapromptify. The more precise you are about the processing logic and scoring, the better the meta-prompt will be.

---

```markdown
# Tool Spec Card: [Tool Name]

## Purpose
[1-2 sentences: what this tool does and who it's for]

## Problem It Solves
[What pain point or need does this address? Why would someone use this instead of doing it manually?]

## Inputs
[What does the user provide? List each input with its type and whether it's required or optional]

- **[Input 1]** (required): [description]
- **[Input 2]** (required): [description]
- **[Input 3]** (optional): [description]

## Processing Logic
[This is the heart of the spec card. Describe step-by-step what the tool does with the inputs. Include:]

### Steps
1. [First thing the tool does with the input]
2. [Second processing step]
3. [How it scores/evaluates/analyzes]
4. [How it generates recommendations]

### Scoring System (if applicable)
[How does the tool rate/score/evaluate? What dimensions? What scale?]

- **[Dimension 1]**: [what it measures, scale]
- **[Dimension 2]**: [what it measures, scale]

### Frameworks Used
[Any named methodologies, scoring rubrics, or decision frameworks the tool applies]

## Output Sections
[What does the final deliverable contain? List each section of the output]

1. **[Section Name]**: [what it contains, 1 sentence]
2. **[Section Name]**: [what it contains]
3. **[Section Name]**: [what it contains]

## What Makes This Unique
[1-2 sentences: what separates this tool from generic advice or a simple ChatGPT prompt? What methodology or insight is baked in that a naive user wouldn't know to ask for?]

## Edge Cases & Constraints
[What doesn't it handle? When should the user NOT use this? Any known limitations?]

- [Edge case 1]
- [Constraint 1]

## Example Output (optional)
[If you have a sample output or can describe what a good result looks like, include it here. This helps the meta-prompt calibrate quality expectations.]
```

---

## Tips for Writing Good Spec Cards

- **Be specific about scoring logic.** "Rate on a scale of 1-10" is weak. "Score on 5 dimensions (market readiness, competitive position, internal capability, timing, resource fit) each 0-20, weighted sum = total" is strong.
- **Include the WHY behind steps.** Not just "research competitors" but "research competitors to find gaps in their offering that the target company's pain points map to — this becomes the differentiation angle in the outreach."
- **Name the output sections explicitly.** The meta-prompt will generate these exact sections. If you want a "Competitive Landscape" section, say so. If you want "Custom Outreach Email," say so.
- **Describe the unique methodology.** Every tool has a perspective. Crystal Ball's consulting tool doesn't just "find companies" — it scores them on multiple dimensions, cross-references competitors, finds decision makers, maps assumed pain points, and generates preemptive objection handling. That methodology IS the product.
