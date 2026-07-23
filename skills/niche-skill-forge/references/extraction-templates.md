# Extraction Templates -- Niche Skill Forge

Per-niche-type templates for distilling research into structured techniques.

---

## TYPE A: API / Tool Wrapper

For: ElevenLabs, Suno, kie.ai (Veo/Sora/Kling), Flux, gptimage2, GitHub Actions, Stripe webhooks, Pinecone, etc.

### Technique Card Template

```yaml
technique_id: T01
name: [Short memorable name, e.g. "Cadence Capitalization"]
type: parameter | prompt_pattern | workflow | gotcha | cost_hack

what:
  one_liner: "What this technique does in one sentence"
  longer: "2-3 sentence explanation if needed"

how:
  mechanism: "The actual lever -- parameter name, prompt structure, API call shape"
  example: |
    [Concrete code/prompt/config example, copy-paste ready]

when_to_use:
  sweet_spot: "When this is clearly the right move"
  avoid_when: "When this backfires"

gotchas:
  - "Specific failure mode and how to avoid"

cost_impact: increase | neutral | decrease | unknown

sources:
  - url: https://...
    type: docs | youtube | reddit | github | blog
    author: "Channel/User/Org"
    date: 2025-09-15
    quote: "Short specific phrase that captures the insight (paraphrased)"
  - [additional sources if cross-confirmed]

cross_confirmed: 1 | 2 | 3+
confidence: high | medium | low
recency_flag: fresh | aging | stale | timeless

test_prompt: |
  [A concrete prompt/command you can run in <5 min to validate this technique]

expected_outcome: "What success looks like"
expected_failure: "What it looks like if the technique is wrong"
```

### Type A Extraction Spine

Every Type A niche needs at minimum:

| Slot | What to Extract |
|------|-----------------|
| **Auth/Setup** | API key location, env vars, install commands |
| **Basic call** | Minimum viable working example |
| **Key parameters** | Top 5 parameters that change output quality dramatically |
| **Prompt patterns** | If the API takes natural language, what patterns work |
| **Chaining** | How it composes with adjacent tools |
| **Cost optimization** | Cheap mode vs quality mode tradeoffs |
| **Rate limits** | What breaks at scale |
| **Recent changes** | What shipped in last 90 days |
| **Anti-patterns** | What community has learned not to do |
| **Failure modes** | Error codes, common errors, debugging |

### Type A Example Sources to Mine

- **Official docs** -> parameters, schemas, pricing
- **Context7** -> current SDK/library docs (often fresher than official site)
- **GitHub repos** -> real prompts used at scale
- **Reddit (r/[tool], r/MachineLearning, r/LocalLLaMA, etc.)** -> gotchas, prompt patterns
- **YouTube tutorial channels** (via yt-search skill) -> workflow demos, parameter sweeps
- **Discord public archives / community blogs** -> power user tips

---

## TYPE B: Methodology / Technique

For: prompting frameworks, evaluation methodologies, agentic workflows, design systems, security gates, etc.

### Technique Card Template

```yaml
technique_id: T01
name: [Short memorable name, e.g. "Pain-First Scoring"]
type: principle | pattern | framework | anti_pattern

what:
  one_liner: "The core idea in one sentence"
  longer: "2-3 sentence explanation"

how:
  steps:
    - "Step 1: ..."
    - "Step 2: ..."
  example: |
    [Concrete worked example showing the methodology in action]

when_to_use:
  sweet_spot: "Situations where this clearly wins"
  avoid_when: "Where it breaks down"

mental_model: "The underlying logic -- why it works"

gotchas:
  - "Specific misapplication and how to avoid"

sources:
  - url: https://...
    type: book | paper | talk | post | thread
    author: "Author name"
    date: 2025-03-10
    insight: "What this source contributed (paraphrased)"

cross_confirmed: 1 | 2 | 3+
confidence: high | medium | low

case_studies:
  - "Brief reference to a real application of the technique"

test_prompt: |
  [A concrete scenario/exercise you can run to feel whether the methodology works]

expected_outcome: "What 'this methodology working' looks like"
```

### Type B Extraction Spine

Every Type B niche needs at minimum:

| Slot | What to Extract |
|------|-----------------|
| **Core principle** | The one idea everything else flows from |
| **Mental model** | The underlying logic |
| **Steps/sequence** | Concrete operationalization |
| **Decision criteria** | When to apply, when not to |
| **Anti-patterns** | Common misapplications |
| **Compare/contrast** | How this differs from adjacent methodologies |
| **Case studies** | Real-world applications (sourced) |
| **Failure conditions** | When the methodology breaks |

### Type B Example Sources to Mine

- **Books / long-form posts** by methodology originator
- **Conference talks** (YouTube via yt-search skill)
- **Academic papers** (when applicable)
- **Practitioner blogs** showing real applications
- **Threads/critiques** that surface failure modes
- **Reddit discussions** showing how it's used in the wild

---

## Cross-Type Notes

### When the Niche is Hybrid (Type H)

Some niches are both API + methodology (e.g. "agentic RAG patterns" is methodology + specific tool stacks). In this case:
1. Run BOTH extraction spines
2. Produce separate technique cards
3. Cross-link in the dossier
4. The output SKILL.md has a "Tools" section AND a "Principles" section

### Anti-Pattern Cards

Anti-patterns are first-class citizens. Each anti-pattern gets its own card:

```yaml
anti_pattern_id: AP01
name: "Generic-prompt Slop"
what_people_do: "Concrete description of the wrong move"
why_it_breaks: "The mechanism of failure"
correct_approach: "Pointer to technique T0X"
sources:
  - url: https://reddit.com/...
    quote: "Community evidence this is a real failure mode (paraphrased)"
```

### Contradiction Cards

When sources disagree, capture explicitly:

```yaml
contradiction_id: C01
topic: "Optimal value for parameter X"
positions:
  - claim: "Use Y"
    source: [URL]
    confidence: high
  - claim: "Use Z"
    source: [URL]
    confidence: medium
recommended_test: "Phase 1 test prompt that will resolve this"
```

These flow directly into the test-prompts.md package output.

---

## Distillation Rules

After extracting cards:

1. **Deduplicate**: If two cards describe the same technique, merge with all sources cited
2. **Promote**: Techniques with `cross_confirmed: 2+` AND `confidence: high` go to the SKILL.md core
3. **Dossier-only**: Single-source techniques stay in the dossier as "worth testing" but don't go in the skill until validated
4. **Anti-patterns always promote**: If 2+ sources independently complain about the same failure mode, that's a skill-level anti-pattern
5. **Keep evidence**: The dossier preserves all sources. SKILL.md keeps it tight.

## Output Checklist Per Niche

Before handing off to Phase 1.4 (drafting SKILL.md), confirm:

- [ ] 5-10 technique cards
- [ ] 3+ anti-pattern cards
- [ ] All contradictions surfaced
- [ ] Every card has at least 1 source URL
- [ ] Recency flags applied
- [ ] Test prompts written for each high-confidence technique
- [ ] Sweet spot articulated in one sentence
- [ ] Cost shape documented (Type A) or applicability range documented (Type B)
