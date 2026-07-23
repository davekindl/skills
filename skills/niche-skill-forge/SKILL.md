---
name: niche-skill-forge
description: "Research-backed skill builder. Researches niche domains (APIs, tools, methodologies) across web, YouTube, Reddit, GitHub, and Context7, extracts tribal knowledge into technique cards, and produces a full package: SKILL.md + technique index + sourced dossier + test prompts + evolver config + Crystal Ball entries. Two phases: Phase 1 drafts from research, Phase 2 finalizes after manual validation. Trigger on: 'build me a skill for X', 'forge a skill', 'research and skill this niche', 'niche skill', 'skill forge', 'meta-skill', 'turn this into a skill', 'make a skill for this API/tool', 'capture this domain as a skill', 'we should have a skill for this'. Also triggers for specific API skills (ElevenLabs, Suno, Veo, kie.ai, Flux, Deepgram, etc.) or technique skills (prompting patterns, evaluation frameworks, agentic workflows)."
---

# NICHE SKILL FORGE -- Research-Backed Skill Builder

> "Research the niche. Extract the techniques. Encode the tribal knowledge. Ship the skill."

This is the industrialized version of how the gpt-image-2-techniques skill was built: research a domain widely, extract what actually works, encode it as operational knowledge in a SKILL.md with progressive disclosure architecture. The output isn't "use this API" -- it's "use these specific patterns the community discovered work best, in this order, with these gotchas."

This is a **meta-skill**. It produces other skills.

---

## Two-Phase Operation

### Phase 1: RESEARCH & DRAFT
Wide research -> extract techniques -> produce skill draft + dossier + test prompts. Hand to you for manual validation.

### Phase 2: FINALIZE
you report what worked, what didn't. Skill refines the draft, removes failed techniques, doubles down on validated ones, ships final package.

**Never skip Phase 1 -> manual test -> Phase 2.** The quality gate is your hands-on testing, not automated validation. Untested research-encoded techniques are slop in a different costume.

---

## When NOT to Use

- The user wants a **quick wrapper skill** with no research backing -- use `skill-creator` directly
- The niche is **your own methodology** that you already knows deeply -- skip research, encode via `skill-creator`
- The niche is **too broad** (e.g., "AI prompting") -- narrow to a specific tool/technique first
- A skill **already exists** for this niche -- extend it via an evolution loop instead of rebuilding
- The user wants a **business plan or strategy** around a niche -- use a strategy planner or `deep-interrogation`
- The user wants a **single image/asset** -- use `gpt-image-2-techniques` directly

---

## Trigger Examples

- "Build me a skill for ElevenLabs v3 audio production"
- "Forge a skill around Suno cadence prompts"
- "Research kie.ai Veo 3 and skill it"
- "We should have a skill for Flux Pro prompting"
- "Turn the Adam scar tissue methodology into a skill"
- "Meta-skill this niche: agentic RAG patterns"

---

## Phase 1: Research & Draft

### Step 1.0 -- Discovery (DO NOT SKIP)

Before burning research tokens, run discovery:

1. **Parse the request.** Extract: niche name, apparent type (API vs methodology), scope hints.
2. **Check for existing skills.** Scan your skills library and your skills library for overlapping skills. If one exists, propose extending via evolver instead of rebuilding.
3. **Auto-classify niche type:**
   - **Type A: API/Tool wrapper** -- triggered by API names, SDK mentions, endpoint references, tool names (ElevenLabs, Suno, kie.ai, Flux, Stripe, Pinecone, etc.)
   - **Type B: Methodology/Technique** -- triggered by framework names, pattern references, workflow descriptions (prompting patterns, evaluation frameworks, agentic workflows)
   - **Type H: Hybrid** -- both API + methodology (e.g., "agentic RAG patterns" = methodology + tool stacks)
   - If ambiguous, ask once using AskUserQuestion.
4. **Scope the research.** Propose boundaries:
   ```
   Niche: [name]
   Type: [A/B/H]
   IN scope: [what we'll research]
   OUT of scope: [what we won't -- prevents creep]
   Estimated research: ~[N] tool calls, ~[M] minutes
   ```
5. **Let you confirm or adjust** before proceeding.

### Step 1.1 -- Capture Niche Intent

After discovery confirms scope, lock in:

1. **What is the niche?** API/tool name, methodology name, or domain phrase
2. **Scope boundaries?** What's IN scope, what's OUT (avoid scope creep)
3. **Existing context?** Has you already shared docs, prompts, or links? Read those first -- they're the highest-signal source.

Max 2 clarifying questions. Don't over-interrogate.

### Step 1.2 -- Research Protocol (Wide Cast)

Read `references/research-protocol.md` for full details. Summary of sources to hit:

1. **your existing context** -- Grep for the niche keyword in the current project
2. **Context7** -- `resolve-library-id` + `get-library-docs` for SDK/library niches
3. **Official docs** -- WebFetch the canonical source
4. **Web search** -- WebSearch for best practices, techniques, common mistakes, cost optimization
5. **YouTube** -- use the `yt-search` skill for tutorials and expert breakdowns with transcripts
6. **Reddit / forums** -- WebSearch for `site:reddit.com [niche]`, gotcha threads, prompt-sharing threads
7. **GitHub** -- WebSearch for repos, real example code, awesome-lists

> **Note:** This 7-source flow runs inline today. It could move to parallel subagents (one per source tier) to cut wall-time and isolate the token-heavy fetching from the main context -- a future refactor, not a requirement.

**Token discipline:**
- Cap research at ~15-20 tool calls for Type A, ~10-15 for Type B
- Save fetched content to `./research-[niche]/*.md` files -- never flood context
- Extract -> close file -> keep only the distilled finding in context

**Track every source.** Every technique needs a citation. No invented "best practices."

### Context Pressure Protocol

Research is token-heavy. Manage context actively:

```
After Step 1.2 (research complete):
  1. Write all raw findings to ./research-[niche]/raw-findings.md
  2. Run /compact preserving: niche name, type, scope, technique count, source count
  3. Re-read only the extracted technique cards
  4. Continue to Step 1.3

After Step 1.3 (extraction complete):
  1. Write all technique cards to ./research-[niche]/extracted-techniques.md
  2. If context > 60%, run /compact preserving: niche name, extracted technique IDs, anti-pattern IDs
  3. Re-read extracted-techniques.md
  4. Continue to Step 1.4
```

### Step 1.3 -- Technique Extraction

Read `references/extraction-templates.md` for the per-niche-type extraction templates.

For each finding, capture:

```yaml
technique: [short name]
what: [what it does in one sentence]
how: [the actual mechanism/parameter/prompt pattern]
source: [URL + author/channel + date]
confidence: high | medium | low
recency: [date of source]
cross_confirmed: [count of independent sources that mentioned this]
test_prompt: [a concrete prompt or command you can run to validate]
```

**Surface contradictions explicitly.** If two sources disagree, surface both with their sources -- don't pick a winner. That's what Phase 1 testing is for.

### Step 1.4 -- Draft the SKILL.md

The output skill uses **progressive disclosure architecture** (matching gpt-image-2-techniques pattern):

```markdown
---
name: [niche-name]
description: "[Pushy trigger description -- keywords from research]"
# Optional frontmatter fields (include only when the niche needs them):
# allowed-tools: [comma-separated tool allowlist -- restricts what the skill can call]
# disable-model-invocation: true   # set when the skill should be user-invoked only, never auto-triggered
# model: [opus | sonnet | haiku]   # pin a model for this skill's work
# paths: [glob(s) scoping which files the skill operates on]
# context: fork                    # run the skill in a forked context to isolate token-heavy work
---

# [NICHE NAME] -- [Short Tagline]

> "[One-sentence positioning]"

## Architecture
[Directory tree showing progressive disclosure structure]

## Discovery Workflow
[4-step: parse request -> scan _index.md -> propose top 3 techniques -> execute]

## Core Techniques
[3-7 numbered techniques, each with: what, how, when, gotcha, example]
[For details, point to techniques/library/*.md]

## Anti-Patterns
[What NOT to do -- sourced from forum complaints and Reddit gotcha threads]

## When NOT to Use
[Explicit boundaries with alternatives]

## Cost & Performance Notes
[Token costs, API costs, latency expectations]
```

### Step 1.5 -- Produce the Full Package

Output package structure (progressive disclosure):

```
[niche-name]/
+-- SKILL.md                              <- Operating instructions (under 500 lines)
+-- techniques/
|   +-- _index.md                         <- One-liner per technique (discovery scan target)
|   +-- library/
|       +-- [category-1].md               <- Full technique details (loaded on demand)
|       +-- [category-2].md
+-- references/
|   +-- [domain-specific].md              <- Supporting docs from research
+-- research-dossier.md                   <- Sourced findings, organized
+-- test-prompts.md                       <- 5-10 concrete prompts for you to run
+-- evolver-config.md                     <- Config for evolver autoresearch loop
+-- crystal-ball-entries.md               <- Evidence entries (if your flagship product active)
+-- CHANGELOG.md                          <- Version tracking (initial build + future evolutions)
```

**For Type A (API/Tool) niches, also generate:**
```
+-- [niche]_client.py                     <- Reusable API wrapper module
    Contents:
    - Auth setup (env var or config-based)
    - Core API calls as functions
    - Polling for async APIs
    - Error handling for known failure modes
    - Cost estimation helper
```

**research-dossier.md** must include:
- Every technique with its sources cited
- Confidence ratings
- Contradictions surfaced
- Sources organized by type (docs / video / reddit / github)

**test-prompts.md** must include:
- 5-10 concrete, runnable prompts you can paste into Claude Code or the target tool
- Each prompt maps to one technique from the dossier
- Format: `## Test [N]: [technique name]` -> prompt -> expected outcome -> "Does this work? Y/N + notes"

**evolver-config.md** must specify:
- The skill file to evolve
- A 1-10 scoring rubric tailored to this niche
- Recommended execution mode:
  - **Controlled:** methodology skills, creative tools, anything with subjective quality
  - **Autonomous:** API wrappers with measurable output quality (image gen, TTS, video gen)
- Stopping conditions

**crystal-ball-entries.md** -- conditional:
1. Check if your project folder exists
2. If yes, read the evidence format from the latest wave file, generate 2-5 entries
3. If no, skip and note: "Crystal Ball entries deferred -- your flagship product not found"

**CHANGELOG.md:**
```markdown
# [niche-name] Changelog

## v1.0.0 -- [YYYY-MM-DD] -- Initial Build
- Built via niche-skill-forge Phase 1
- [N] techniques extracted from [M] sources
- Status: Phase 1 draft -- awaiting manual validation

## v1.1.0 -- [YYYY-MM-DD] -- Phase 2 Validation
- [N] techniques validated, [M] failed, [K] partial
- Failed techniques moved to anti-patterns
- Status: Production
```

### Step 1.6 -- Hand-Off to you

End Phase 1 with:

```
PHASE 1 COMPLETE -- [niche-name] skill draft ready for manual validation.

Package location: your skills library[niche-name]\
                  (or your skills library[niche-name]\ for global install)

Next steps:
1. Review the draft SKILL.md and technique index
2. Run the test prompts (test-prompts.md) -- mark each Pass/Fail with notes
3. When you have results, come back and say "finalize" or paste your test results

Estimated test time: [X] minutes (based on number of test prompts)
```

Stop. Wait for you.

---

## Phase 2: Finalize

Triggered by any of:
- "finalize [anything]"
- "phase 2"
- "test results for [anything]"
- "here's what worked"
- "skill results"
- Any message containing test pass/fail data after a Phase 1 handoff

### Step 2.1 -- Ingest Test Results

Ask you for the test results. Accept any format:
- Marked-up test-prompts.md
- Pasted notes
- Verbal report ("test 1, 3, 5 worked; test 2 failed because X; test 4 was meh")

Categorize each technique:
- **Validated** -- keep, promote to core
- **Partial** -- keep with caveat documented
- **Failed** -- remove from SKILL.md, document in anti-patterns

### Step 2.2 -- Refine the SKILL.md

- Strip failed techniques from the technique index and library files
- Promote validated techniques to the top of their category
- Add a "What Doesn't Work" section if 2+ techniques failed (scar tissue -- high value)
- Update the description to emphasize validated capabilities
- Add a "Validated: [date]" timestamp footer
- Update CHANGELOG.md with Phase 2 results

### Step 2.3 -- Final Package

Same structure as Phase 1, updated with:
- Failed techniques removed from `techniques/` directory
- `test-results.md` added with your actual outcomes, dated
- `evolver-config.md` updated with rubric refined by what actually mattered
- `research-dossier.md` updated with test result per technique

### Step 2.4 -- Installation

```
PHASE 2 COMPLETE -- [niche-name] skill finalized.

Installed at: your skills library[niche-name]\
The skill is now globally available across all projects.
Test by triggering it: "[example trigger phrase]"

Evolver: when ready to harden further, run "evolve [niche-name]" using the included config.
```

---

## Output Discipline (Both Phases)

- **Never paste full source content into context.** Save to scratch files, extract, close.
- **Cite every technique.** No source = doesn't go in the skill.
- **Distinguish docs claims from community claims.** Docs say what they say; Reddit says what actually happens.
- **Recency matters for fast-moving APIs.** Flag any source >12 months old explicitly.
- **No invented techniques.** If you didn't find it in research, don't put it in the skill.
- **Use /compact checkpoints.** Research is token-heavy. Save progress to disk and compact.

---

## Anti-Patterns

- **Skipping Phase 1 -> manual test -> Phase 2.** The whole point is research + validation. Skipping validation produces sophisticated slop.
- **Putting too much in SKILL.md.** Keep it under 500 lines. Push depth into `techniques/library/`. Progressive disclosure.
- **Generic descriptions.** "A skill for X" is weak. The description is the trigger -- pack it with the keywords from the research.
- **No anti-patterns section.** What doesn't work is as valuable as what does. Forum complaints are gold.
- **Mixing niches.** One skill = one niche. If research uncovers a sibling niche, log it as a future skill, don't bloat the current one.
- **Building without test prompts.** If you can't think of how you would test the techniques, you don't understand the niche yet -- research more.
- **Flat output structure.** Always use progressive disclosure: SKILL.md -> _index.md -> library/*.md. Never dump all techniques into one file.
- **Skipping discovery.** Always check for existing skills and confirm scope before burning research tokens.

---

## Reference Files

| File | Read When |
|------|-----------|
| `references/research-protocol.md` | Before starting research -- full source list and search patterns |
| `references/extraction-templates.md` | When extracting techniques -- per-niche-type templates |
| `references/package-templates.md` | When producing the final package -- file templates |

---

## Connection to Innovation Methodology

This skill operationalizes steps 1, 3, 4, 7, 8 of your methodology:
- **Step 1 (Absorb)** -- wide research across web/YouTube/Reddit/GitHub
- **Step 3 (Extract method)** -- technique extraction with sources
- **Step 4 (Package for distribution)** -- SKILL.md is the packaged method
- **Step 7 (Industrialize)** -- this skill IS the industrialized loop
- **Step 8 (Build tools embodying the method)** -- every output skill is one such tool
