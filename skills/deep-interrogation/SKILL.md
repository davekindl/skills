---
name: deep-interrogation
description: 20-question deep interrogation of any business idea, product concept, or strategic decision. 4 phases (Strip/Validate/Stretch/Kill), 3 levels deep per question, draws conclusions. Combines First Principles, Mom Test, Hormozi 10x, Pre-mortem, Munger Inversion, Thiel Contrarian, and 14 other proven frameworks into one executable flow.
---

# Deep Interrogation — 20 Questions, 3 Levels Deep

> "The quality of your answers is determined by the quality of your questions." Every framework in this skill has been proven in practice — YC interviews, McKinsey engagements, Toyota production lines, Hormozi offer construction, Munger investment decisions.

## When to Use

Trigger on ANY of:
- "interrogate this idea"
- "deep interrogation"
- "20 questions on this"
- "stress test this concept"
- "is this idea any good"
- "validate this"
- "poke holes in this"
- "kill test this idea"
- "run the questions on this"
- Before any major build or planning commitment (as a pre-filter)
- Before any build-pipeline run (as validation)
- After a Hormozi audit (to verify the offer)
- When someone asks "what am I missing"

## How It Works

**Input:** A business idea, product concept, or strategic decision described in 2-5 sentences.

If `$ARGUMENTS` is provided, treat it as the idea to interrogate — skip asking for the idea and run the 20 questions directly against it. If `$ARGUMENTS` is empty, ask the user for the 2-5 sentence description (or infer it from the named project's context) before starting.

**Process:** 20 questions across 4 phases. For each question:
1. Answer it honestly from available context (codebase, research, market data, your project ecosystem)
2. If the answer raises a natural follow-up question, ask and answer that too
3. Go up to 3 levels deep per question (Q → Q.1 → Q.1.1)
4. Stop drilling when the answer is terminal (no further questions arise)

**Output:** Structured findings + a conclusion with go/no-go signal.

## The 4 Phases

### PHASE 1: STRIP (Questions 1-5)
*Goal: Remove assumptions. Find the real problem, the secret, and the timing.*

Frameworks: First Principles (Aristotle/Musk), Thiel Contrarian Trap, Sequoia "Why Now?", YC Earned Secret, 5 Whys

| Q# | Question | Framework | What It Catches |
|----|----------|-----------|-----------------|
| 1 | What are we assuming that might not be true? | First Principles | Hidden assumptions that feel like facts |
| 2 | If this industry didn't exist, how would you solve this need from scratch? | First Principles | Existing-solution anchoring |
| 3 | What important truth do few people agree with you on? | Thiel Contrarian | Whether there's a genuine secret or just a copy |
| 4 | Why didn't this exist 5 years ago, and why will it work starting today? | Sequoia "Why Now?" | Timing — the most overlooked factor in startup failure |
| 5 | What do you understand about this that others don't? | YC Earned Secret | Whether the builder has proprietary insight or just enthusiasm |

### PHASE 2: VALIDATE (Questions 6-10)
*Goal: Check if real humans have real pain and have spent real money. Past behavior, not opinions.*

Frameworks: Mom Test (Fitzpatrick), Jobs-To-Be-Done (Christensen), Genchi Genbutsu (Toyota)

| Q# | Question | Framework | What It Catches |
|----|----------|-----------|-----------------|
| 6 | When did a target customer last face this problem? What did they do? | Mom Test | Whether the pain is real or imagined |
| 7 | How much time/money are they ACTUALLY spending on this now? | Mom Test | Whether the cost justification is real or projected |
| 8 | Have they already PAID for something similar? | Mom Test | Willingness-to-pay evidence from behavior, not promises |
| 9 | What would make them go back to the old way? | JTBD | Switching cost reality — if it's zero, retention will be zero |
| 10 | Who decides to buy, and how fast can they decide? | JTBD | Decision cycle — solo founder can't survive a 6-month enterprise sales cycle |

### PHASE 3: STRETCH (Questions 11-14)
*Goal: Find the non-obvious angles. Discover what the product COULD be, not just what it IS.*

Frameworks: Hormozi 10x Price Test, 48-Hour Launch Test, SCAMPER (Reverse), Constraint Elimination

| Q# | Question | Framework | What It Catches |
|----|----------|-----------|-----------------|
| 11 | What would you deliver if you charged 10x? | Hormozi 10x | Whether you're thinking in features (commodity) or outcomes (premium) |
| 12 | If you had to launch a paid version in 48 hours, what ships? | 48-Hour Test | The irreducible core — if you can't describe it, you don't understand your value |
| 13 | What if you reversed who pays? | SCAMPER Reverse | Hidden marketplace or inverse business model |
| 14 | What if you eliminated the most expensive part? | Constraint Elimination | Whether the differentiator survives cost-cutting |

### PHASE 4: KILL (Questions 15-20)
*Goal: Try to destroy the idea before building it. If it survives, it's real.*

Frameworks: Pre-Mortem (Klein), Munger Inversion, Kill the Company (Bodell), Disconfirmation, Bandwidth Razor, Schlep+Mom Combo

| Q# | Question | Framework | What It Catches |
|----|----------|-----------|-----------------|
| 15 | It's 12 months from now, this failed catastrophically. Write the postmortem. | Pre-Mortem | Risks that optimism bias hides — people explain failures 2x better than they predict them |
| 16 | How would you GUARANTEE failure? List 7 ways. How many are currently true? | Munger Inversion | Active failure conditions — the most dangerous finding possible |
| 17 | You're the #1 competitor. How do you kill this in 90 days? | Kill the Company | Competitive vulnerability from the attacker's perspective |
| 18 | What specific evidence would make you abandon this? Write it down. | Disconfirmation | Motivated reasoning — if you can't answer this, you're already trapped |
| 19 | Can one person RUN this at steady-state, indefinitely? | Bandwidth Razor | Solo founder capacity — not "can I build it" but "can I OPERATE it" |
| 20 | Is the problem tedious enough competitors won't copy AND have prospects already spent money solving it? | Schlep+Mom Combo | The holy grail: defensible AND validated |

## Execution Rules

1. **Answer from context first.** Read the project's CLAUDE.md, megaplan, brief, research — don't guess. If the answer isn't in context, say "UNKNOWN — needs validation" and note what would answer it.

2. **Follow-up depth.** If your answer to Q[N] raises an obvious next question, ask and answer it as Q[N.1]. If THAT answer raises another, go to Q[N.1.1]. Stop at 3 levels. Format:
   ```
   **Q[N]: [question]**
   A: [answer]
     → Follow-up Q[N.1]: [raised question]
     A: [answer]
       → Follow-up Q[N.1.1]: [deeper question]
       A: [answer]
   ```

3. **Be brutal.** This skill exists to find the truth, not to validate the idea. If the idea is bad, say so. If 5/7 failure conditions are active, say so. If the builder hasn't talked to a single customer, say so.

4. **Check whether absence of activity is intentional before treating it as evidence.** Launch and outreach posture changes over time — sometimes a founder deliberately hasn't shipped or sold yet. Before treating "no sales / no outreach" as disconfirming evidence, establish the intended state. If go-to-market is deliberately on hold, unsent drafts and zero sends are NOT negative evidence — preparing ahead of a planned launch is smart. If the plan says the product should already be in-market against a named target list, then a lack of activity IS a valid negative signal — flag the gap and treat ship rate as a positive metric. Never assume "zero sends is fine" when the plan says otherwise.

5. **Growth intent filter.** For B2B/SMB ideas: always check whether the target customer even WANTS to grow. A content business selling to someone who doesn't want more customers has no market. Ask Q6 with this lens.

## Output Format

Write findings to `[project]/deep-interrogation-[date].md` with this structure:

```markdown
# Deep Interrogation — [Product/Idea Name]
**Date:** [ISO date]
**Input:** [2-3 sentence description of what was interrogated]

## Phase 1: Strip
[Q1-Q5 with answers and follow-ups]

## Phase 2: Validate
[Q6-Q10 with answers and follow-ups]

## Phase 3: Stretch
[Q11-Q14 with answers and follow-ups]

## Phase 4: Kill
[Q15-Q20 with answers and follow-ups]

## Conclusion

### Strongest Signal
[The single most important finding — positive or negative]

### Biggest Unvalidated Assumption
[The thing that could kill this if it turns out to be wrong]

### Go / No-Go / Conditional
[GO: build it. NO-GO: stop. CONDITIONAL: do X first, then reassess.]
[If CONDITIONAL, specify the exact test and threshold.]

### The Test That Costs Nothing
[A validation step that can be done in <3 hours with <EUR 10]
```

## Integration with Other Skills

| Trigger | What Happens |
|---------|-------------|
| Before a major build | Run interrogation first. If NO-GO, skip the build. If CONDITIONAL, run the test first. |
| After Hormozi audit | Run interrogation on the Hormozi'd offer to stress-test the value stack. |
| After a build pipeline's discovery phase | Run interrogation on the discovery output before committing to architecture. |
| Periodic product review | A maintenance pass can recommend re-running interrogation on stale products. |

## What This Skill Does NOT Do

- It does not build anything. It produces questions and answers only.
- It does not replace market research. It surfaces what research is MISSING.
- It does not make the decision. It presents findings. You decide.
- It does not sugarcoat. If the idea is bad, the conclusion says NO-GO.
