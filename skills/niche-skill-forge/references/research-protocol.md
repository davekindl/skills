# Research Protocol -- Niche Skill Forge

This is the playbook for Phase 1, Step 1.2. Read before researching a new niche.

## Source Hierarchy (by signal-to-noise)

| Tier | Source | Signal | When to skip |
|------|--------|--------|--------------|
| 1 | your existing context (project files, uploaded docs, conversation) | Highest | Never skip -- read first |
| 1.5 | Context7 library docs | High | Skip if niche is not an SDK/library |
| 2 | Official docs | High | Skip only if docs are sparse/outdated |
| 3 | GitHub repos (real code) | High | Skip if niche is non-code |
| 4 | YouTube transcripts (via yt-search skill) | High for visual/audio niches | Skip for pure dev tools |
| 5 | Reddit / forums | High for gotchas, anti-patterns | Skip if niche is enterprise-only |
| 6 | Web blogs / Medium articles | Mixed -- often SEO slop | Skip aggregators |
| 7 | Vendor marketing pages | Low signal | Skip unless looking for pricing |

## Phase 1.2 Execution Order

### Step A: Read Existing Context (Free Tokens)
- Use `Grep` to search for the niche keyword across the current project
- Check the working directory for relevant .md files, notes, or prior research
- Read any files you explicitly mentioned or uploaded

### Step A.5: Context7 Documentation Check
If the niche is a library/SDK with likely Context7 coverage:
1. `resolve-library-id` for the niche name (pass version from package.json if available)
2. `get-library-docs` for key topics: auth, core API, error handling, recent changes
3. Context7 docs are often more current than official docs pages
4. If Context7 is unreachable, flag with `[DOCS GAP]` and continue to Step B

### Step B: Official Docs Pass
```
1. WebSearch: "[niche] official documentation"
2. WebFetch the canonical URL
3. Save full content to ./research-[niche]/docs.md (using Write tool)
4. Extract: capabilities, parameters, pricing, rate limits, recent changes
```

### Step C: Web Search Pass (Spread Wide)

Run these query patterns using WebSearch:
- `"[niche]" best practices 2025`
- `"[niche]" techniques`
- `"[niche]" prompt engineering` (if relevant)
- `"[niche]" common mistakes`
- `"[niche]" vs [closest competitor]`
- `"[niche]" cost optimization`
- `"[niche]" advanced workflow`

Cap at 5-7 searches. Don't repeat near-duplicate queries.

### Step D: YouTube Pass (via yt-search skill)

Use the `yt-search` skill for structured results with engagement data:
1. Search: `[niche] tutorial` -- get top 5 by engagement
2. Search: `[niche] tips tricks` -- get top 3
3. For high-engagement results (>50K views): request transcript if available
4. Extract techniques from transcripts using the technique card template

Look for: channel authority (subscriber count, recency), demo quality, specific parameter advice.

### Step E: Reddit / Forums Pass

Use WebSearch:
- `site:reddit.com "[niche]"`
- `site:reddit.com "[niche]" tips`
- `site:reddit.com "[niche]" not working`
- `"[niche]" discord` (find community hubs even if can't access)

Reddit gold:
- "I finally figured out..." threads
- "Why does X keep doing Y" threads
- Megathreads with pinned tips
- Specific prompt-sharing threads

### Step F: GitHub Pass

Use WebSearch:
- `site:github.com "[niche]" examples`
- `awesome-[niche]`
- WebFetch top repos' README
- Look at: prompt patterns in actual code, parameter defaults used in production, common imports/dependencies

### Step G: Recency Check
Any technique sourced from material older than 12 months for a fast-moving API gets flagged.
- For LLM/AI APIs: 12 months
- For frameworks: 24 months
- For methodologies: no recency cutoff (timeless principles welcome)

## Token Discipline

**Hard rules:**
- Total tool calls capped at ~20 (Type A API skill) or ~15 (Type B methodology skill)
- Every fetched page -> saved to `./research-[niche]/*.md` using Write tool -> extract -> move on
- Never let raw page content sit in context after extraction
- Use Grep to search large scratch files for specific keywords

**Soft rules:**
- If 3 searches return the same top 3 results, you're saturated -- stop searching that angle
- If you've extracted 7+ techniques, stop searching -- you have enough for a v1 skill

**Context pressure checkpoints:**
- After completing all research steps: write findings to disk, run /compact
- After extraction: write technique cards to disk, run /compact if needed
- The disk files ARE your memory -- context is expendable

## Contradiction Surfacing

When two sources disagree, do NOT pick a winner. Record both:

```yaml
contradiction:
  topic: optimal_temperature
  source_A:
    claim: "use 0.7 for creative output"
    url: docs.anthropic.com/...
    confidence: high
  source_B:
    claim: "use 1.2 for creative output"
    url: reddit.com/r/.../comments/...
    confidence: medium
  resolution: "FLAG FOR PHASE 1 TESTING -- you validate which works"
```

Phase 1 testing is the only valid resolution mechanism for contradictions.

## Recency Flagging

For every technique, include:
```yaml
recency: 2025-09
recency_flag: fresh | aging | stale | timeless
```

- `fresh` = source <6mo
- `aging` = 6-12mo, still likely valid
- `stale` = >12mo for fast-moving API (verify before encoding)
- `timeless` = methodology or principle, no expiry

Stale techniques get included in the dossier with a flag but are NOT auto-promoted to the SKILL.md core techniques without Phase 1 validation.

## What to Always Extract

Per niche, regardless of type:
1. **Core capability** -- what it does in one sentence
2. **Sweet spot use case** -- what it's clearly the best tool for
3. **Edge case use cases** -- what surprised the community
4. **Anti-patterns** -- what people try that doesn't work
5. **Cost shape** -- per-call, per-token, per-second, subscription tier
6. **Recent changes** -- anything shipped in the last 90 days
7. **Composable patterns** -- how it chains with other tools
8. **Failure modes** -- what breaks and why

These 8 form the spine of every extraction.

## What to Ignore

- Marketing pages from competitors comparing themselves to the niche
- Sponsored content / affiliate review sites
- AI-generated SEO content (smell test: generic headings, no specifics, no real examples)
- Pre-release speculation about future features
- Twitter hot takes without code or specifics

## When Research Is Done

You're done with Phase 1.2 when:
1. You have 5-10 distinct techniques with sources
2. You have at least 2 contradictions or open questions surfaced
3. You have 3+ anti-patterns from forum/community sources
4. You can articulate the niche's sweet spot in one sentence
5. You know the cost shape (if applicable)

If any of these are missing, do one more targeted research pass before extraction.
