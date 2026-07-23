# Package Templates -- Niche Skill Forge

Templates for the artifacts produced alongside SKILL.md.

---

## 1. techniques/_index.md Template

The discovery scan target. One-liner per technique for quick matching.

```markdown
# Technique Index -- [niche-name]

Discovery directory. Used by the skill during discovery step.
Each entry: ID . score . name . [tag] . one-line summary.
Total: [N] techniques across [M] categories.

**Score legend:** 5-star = multi-source verified . 4-star = strong evidence . 3-star = single-source . lower = anecdotal.
**[foundational]** = building-block techniques that recur across categories.

---

## [Category 1]  .  [`library/[category-1].md`]

- **T01** 4-star **[Technique Name]** -- [one-line summary of what it does]
- **T02** 5-star **[Technique Name]** -- [one-line summary]

## [Category 2]  .  [`library/[category-2].md`]

- **T03** 3-star **[Technique Name]** -- [one-line summary]
```

---

## 2. research-dossier.md Template

```markdown
# [Niche Name] -- Research Dossier

**Built:** [YYYY-MM-DD]
**Niche type:** API/Tool | Methodology | Hybrid
**Research effort:** [N tool calls, M sources reviewed]
**Status:** Phase 1 Draft | Phase 2 Finalized

---

## Executive Summary

**Sweet spot:** [One sentence -- when is this niche the clear right answer?]

**Cost shape:** [Type A only -- per-call/per-token/subscription]
**Applicability:** [Type B only -- where does this methodology work?]

**Top 3 techniques** (validated or pending):
1. [Technique name] -- [one-line value]
2. [Technique name] -- [one-line value]
3. [Technique name] -- [one-line value]

**Top 3 anti-patterns:**
1. [Anti-pattern] -- [why it fails]
2. [Anti-pattern] -- [why it fails]
3. [Anti-pattern] -- [why it fails]

**Open contradictions for Phase 1 testing:**
- [Contradiction 1]
- [Contradiction 2]

---

## Technique Cards

[Insert all technique cards from extraction-templates.md format]

---

## Anti-Pattern Cards

[Insert all anti-pattern cards]

---

## Contradictions to Resolve

[Insert contradiction cards]

---

## Sources Inventory

### Official Documentation
- [URL] -- [what was extracted]

### Context7
- [Library ID] -- [topics fetched] -- [what was extracted]

### YouTube (via yt-search)
- [URL] -- [Channel] -- [Date] -- [what was extracted]

### Reddit / Forums
- [URL] -- [Subreddit] -- [Date] -- [what was extracted]

### GitHub
- [URL] -- [Repo] -- [what was extracted]

### Blogs / Other
- [URL] -- [Source] -- [Date] -- [what was extracted]

---

## Phase 1 Test Status (updated in Phase 2)

| Technique | Tested? | Result | Notes |
|-----------|---------|--------|-------|
| T01 | Validated | Works | |
| T02 | Partial | Works only when X | |
| T03 | Failed | Reason | |

---

## Recency Audit

Sources flagged for staleness:
- [Source] -- [Age] -- [Why it matters or doesn't]
```

---

## 3. test-prompts.md Template

```markdown
# [Niche Name] -- Phase 1 Test Prompts

**How to use:** Run each prompt in the appropriate environment (Claude Code, the target API, etc.). Mark each one Pass / Fail / Partial with notes. Return with results to trigger Phase 2.

**Estimated total test time:** [X] minutes

---

## Test 1: [Technique T01 name]

**What we're testing:** [One sentence]

**Environment:** [Claude Code | API directly | Tool UI | etc.]

**Prompt / Command:**
```
[Exact text to paste]
```

**Expected outcome:** [What success looks like]

**Failure signature:** [What it looks like if the technique is wrong]

**Result:**
- [ ] Pass
- [ ] Partial
- [ ] Fail

**Notes:** _______________

---

## Test [N]: Contradiction Resolver -- [Topic]

**What we're testing:** Two sources disagree on [X]. This test determines which is right for your use case.

**Variant A** (sourced from [source]):
```
[Prompt using approach A]
```

**Variant B** (sourced from [source]):
```
[Prompt using approach B]
```

**Compare:** [What to look at when comparing outputs]

**Winner:** _______________
**Why:** _______________

---

## Aggregate Results

When done testing, paste back into chat:

```
PHASE 1 RESULTS -- [niche-name]:

Validated: T01, T03, T07
Partial: T02 (only when X)
Failed: T04, T05
Untested: T06 (needs paid tier)

Contradictions resolved:
- C01: Variant B wins

Anti-patterns confirmed: AP01, AP02
Anti-patterns DIDN'T trigger: AP03 (maybe outdated)

Notes:
- [Anything surprising]
- [Anything missing]
```
```

---

## 4. evolver-config.md Template

```markdown
# [Niche Name] -- Evolver Config

**Use after Phase 2 finalization to harden the skill further.**

Trigger: `evolve [niche-name]`

---

## Target

**Skill file:** your skills library[niche-name]\SKILL.md`

**Mode:** Skill Evolution (modify SKILL.md + technique library, score output)

**Execution mode decision:**
- **Controlled** (you steer): methodology skills, creative tools, subjective quality
- **Autonomous** (agent-driven): API wrappers with measurable output quality

**This skill:** [Controlled | Autonomous] -- [1-sentence justification]

---

## Scoring Rubric (1-10)

[Tailor per niche. Example for an image generation skill:]

| Score | Description |
|-------|-------------|
| 10 | Publication-ready, hits brief perfectly, no artifacts |
| 8-9 | Strong output, minor tweaks needed |
| 6-7 | Good direction, needs another pass |
| 4-5 | Mediocre, missing key qualities |
| 1-3 | Broken -- triggers known anti-patterns |

Auto-fail conditions:
- Output triggers a known anti-pattern from the dossier
- Output violates a hard constraint

---

## Evaluation Set

**Inputs:** [N] test prompts representing common use cases
[List them]

**For each input:** run skill -> score 1-10 -> log

---

## Hypotheses to Explore

Based on research, the following changes are worth trying:
- [Hypothesis 1]
- [Hypothesis 2]
- [Hypothesis 3]

---

## Stopping Conditions

- 5 consecutive non-improvements
- Score >= 9 sustained for 3 runs
- 50 experiments total
- you say stop

---

## Cross-System Links

- Updates flow to: `last-evolution.md` in skill dir
- Findings flow to: your lessons log
```

---

## 5. crystal-ball-entries.md Template

**Conditional:** Only generate if your project folder exists. If not, skip with a note.

```markdown
# [Niche Name] -- Crystal Ball Evidence Entries

**Append to:** your flagship product evidence pipeline
**Status:** [Generated | Deferred -- your flagship product not found]

---

## [ID]: [Niche] Released / Updated [Capability]

- **Source:** [Org/Author] ([URL])
- **Date:** [YYYY-MM-DD]
- **Domain:** [matching project domain]
- **Confidence:** [high | medium | low]
- **Tags:** [niche-name], [capability-area], [recency]

### Summary
[2-4 sentences. What shipped, what changed, why it matters.]

### Key Data Points
- [Specific capability with numbers/specs]
- [Pricing/cost shape]
- [Competitive positioning]

### Relevance
- Connects to: [prediction IDs if known]
- Implications: [1-2 sentences on what this enables or threatens]
```

### Tag Discipline

Before generating tags:
1. Read existing tag vocabulary from the evidence database (if accessible)
2. Reuse existing tags where applicable
3. Flag any new tags being introduced
4. Keep tags lowercase-hyphenated

---

## 6. CHANGELOG.md Template

```markdown
# [niche-name] Changelog

## v1.0.0 -- [YYYY-MM-DD] -- Initial Build (Phase 1 Draft)
- Built via niche-skill-forge
- [N] techniques extracted from [M] sources across [K] source types
- [J] anti-patterns documented
- [C] contradictions flagged for testing
- Status: DRAFT -- awaiting manual validation

## v1.1.0 -- [YYYY-MM-DD] -- Phase 2 Validation
- Validated: [list technique IDs]
- Failed: [list technique IDs] -- moved to anti-patterns
- Partial: [list technique IDs] -- caveats documented
- Status: PRODUCTION

## v1.2.0 -- [YYYY-MM-DD] -- Evolution Run [N]
- Evolver branch: [branch name]
- Score: [baseline] -> [final]
- Changes: [summary of what improved]
```

---

## 7. [niche]_client.py Template (Type A only)

For API/Tool niches, generate a reusable Python client:

```python
"""
[niche-name] API Client
Generated by niche-skill-forge on [YYYY-MM-DD]

Usage:
    from [niche]_client import [MainClass]
    client = [MainClass](api_key="...")
    result = client.[primary_method](...)
"""

import os
import time
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class [NicheClient]:
    """Minimal client for [niche] API. No external dependencies."""

    def __init__(self, api_key: str | None = None, base_url: str = "[API_BASE]"):
        self.api_key = api_key or os.environ.get("[NICHE]_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        if not self.api_key:
            raise ValueError("[NICHE]_API_KEY not set")

    def _request(self, method: str, path: str, body: dict | None = None,
                 timeout: int = 30) -> dict:
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = json.dumps(body).encode() if body else None
        req = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            raise RuntimeError(
                f"[niche] API {e.code}: {error_body}"
            ) from e

    # -- Core methods (customize per niche) --

    def [primary_method](self, **kwargs) -> dict:
        """[What the primary operation does]"""
        return self._request("POST", "/[endpoint]", body=kwargs)

    def poll(self, task_id: str, interval: float = 5.0,
             max_wait: float = 300.0) -> dict:
        """Poll async task until complete or timeout."""
        elapsed = 0.0
        while elapsed < max_wait:
            result = self._request("GET", f"/[status-endpoint]?taskId={task_id}")
            status = result.get("data", {}).get("status", "")
            if status in ("completed", "success", "done"):
                return result
            if status in ("failed", "error"):
                raise RuntimeError(f"Task {task_id} failed: {result}")
            time.sleep(interval)
            elapsed += interval
        raise TimeoutError(f"Task {task_id} timed out after {max_wait}s")

    @staticmethod
    def estimate_cost(**kwargs) -> str:
        """Rough cost estimate for an operation."""
        # Customize per niche pricing model
        return "[cost estimate logic]"
```
