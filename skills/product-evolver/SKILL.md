---
name: product-evolver
description: "Deep autonomous product evolution engine. Goes beyond code quality — 4 rotating lenses (CRAWL/USER/COMPETITIVE/BRAINSTORM), multi-agent architecture (planner/reviewer/reporter/experiment-worker) with SDK-level tool restrictions, git-worktree isolation, per-lens do-not-repeat failure memory, literature-vs-benchmark mode gate, append-only ledger, statistical laps, learned dispositions. Based on Karpathy autoresearch + Burtenshaw multiautoresearch patterns. Trigger when the user says 'evolve this product', 'evolve xyz', 'run product evolver', 'make this product better', 'improve this as a product not just code', 'product evolution', 'deep product review', 'what's missing from this product', 'multi-track product evolve', 'product evolve with tracks', or any variation of wanting holistic product improvement with users/competitors/missing features — not just bug fixes."
---

# PRODUCT EVOLVER — Multi-Track Product Intelligence

> "Don't just fix what's broken. Discover what's missing. Learn what works."

Handles simple and multi-track use equivalently. For straightforward single-lens use, run with `--lens CRAWL` and it operates as a focused single-lens loop with the same safety properties.

Inherits core concepts from the base evolver (tracks, verifiers, laps, rounds, dispositions, failure archive). Reference `the-evolver/references/verifier-types.md` and `the-evolver/references/disposition-schema.md` for shared concepts.

**Architectural lineage:**
- `karpathy/autoresearch` — original single-agent loop
- `uditgoenka/autoresearch` — separate prior art (noted to avoid misbranding)
- `burtenshaw/multiautoresearch` — multi-agent invariants absorbed into this skill: per-role tool surfaces, data plane split, worktree-per-experiment, do-not-repeat memory, literature/benchmark mode gate, append-only submit_result. Credit: Ben Burtenshaw (HF Community Education).

## Architecture

```
4 lenses → multi-track per lens → statistical laps → disposition-informed → keep/revert → rotate → disposition write-back
```

---

## Operational Mode: literature | benchmark (multiautoresearch pattern)

Declared once per run, orthogonal to execution mode (brainless/controlled/hybrid):

### `mode: literature`
- Planner may propose lens hypotheses, edit `research/[lens]/*.md` drafts, read competitor landing pages, reddit complaints, app store reviews via WebFetch/WebSearch, simulate personas on paper
- **Promotion to `live/` is disabled.** Experiment-worker may run experiments but cannot promote.
- Gate: `promoted` column in `experiments.tsv` is hard-locked to `false`.
- Lap verdicts are computed but never trigger promotion.
- Used for: competitive surveys, persona cold-start, disposition seeding, BRAINSTORM idea pool generation before committing build time.

### `mode: benchmark`
- Experiment-worker runs experiments, scores across all tracks per lens, promotes winners to `live/`.
- Gate: **"no win claims without a benchmark run."** `aggregate` score must come from actual verifier output (tests/Inspector/Polisher/count/judge), not planner assertion.
- All tracks must have verifiers validated at run start (validation runs each verifier against baseline once, confirms it returns a score).
- BRAINSTORM and COMPETITIVE lenses especially: require that a literature-mode pass exists for the hypothesis family before a benchmark build is allowed (soft enforcement via reviewer check).

### Invocation
```
product evolve [project] --mode literature    # ideation / survey / disposition seed
product evolve [project] --mode benchmark     # actual multi-track measurement (default)
```

If unspecified: brainless → benchmark, controlled/hybrid → ask.

---

## Subagent Roles & Tool Surfaces (ARCHITECTURAL INVARIANT)

**Invariant:** tool access is a property of role registration, not prompt pleading. Planners cannot accidentally Edit because Edit is not registered in their surface. This is the core multiautoresearch safety property. For product evolution with 4 lenses × multi-track verifiers, the blast radius of a runaway edit is substantial — this invariant is non-negotiable.

### Role: `planner`
- **Job per lens:**
  - CRAWL: Identify weakest track (endpoint_health / error_handling / empty_state_coverage / validation_completeness); emit hypothesis targeting it
  - USER: Pick persona (round-robin), identify weakest track (task_completion / time_to_value / friction_points / accessibility); emit hypothesis
  - COMPETITIVE: Pick next unanalyzed competitor; identify weakest track (feature_parity / differentiation / gap_severity); emit hypothesis
  - BRAINSTORM: Identify weakest track (user_impact / implementation_quality / novelty); emit hypothesis
- Reads results.tsv (per-track trajectory per lens), do-not-repeat.md (lens-scoped), dispositions (per-lens problem classes), archive/[lens]/ for patterns
- **Allowed tools:** `Read`, `Grep`, `Glob`, `WebSearch`, `WebFetch`
- **Forbidden tools:** `Edit`, `Write`, `Bash`, `NotebookEdit`

### Role: `reviewer`
- **Job:** Audit the hypothesis against do-not-repeat (lens-scoped), guardrails, lens boundaries, meta-loop safety gates, operational mode gates.
- **Allowed tools:** `Read`, `Grep`, `Glob`
- **Forbidden tools:** everything else
- Lens-boundary enforcement: misclassified proposals routed to backlog.md with corrected lens tag.

### Role: `reporter`
- **Job:** Compile per-lens reflections, round summaries, lap verdicts, disposition updates, PRODUCT-EVOLUTION-REPORT.md, last-evolution.md, scoring-log.md audit.
- **CRITICAL:** The disposition write-back path from "When Done" step 4 only fires when a role holds Write permission to `context/dispositions/`. The reporter is the **sole writer** to `context/dispositions/`, and disposition write-back is triggered automatically on promoted experiments at round-close.
- **Allowed tools:** `Read`, `Grep`, `Glob`, + **scoped Write to:**
  - `[project]/evolver/reports/`
  - `[project]/last-evolution.md`
  - `[project]/PRODUCT-EVOLUTION-REPORT.md`
  - `[project]/scoring-log.md`
  - `context/learnings.md`
  - `context/dispositions/*.json` (disposition write-back — scoped to this directory only)
- **Forbidden tools:** Edit outside those specific paths, Bash, WebFetch/Search.

### Role: `experiment-worker`
- **Job:** One experiment end-to-end: implement per lens, run verifiers for ALL tracks of that lens, submit via submit_result.py. Sandboxed to its worktree.
- **Allowed tools:** Full surface (`Read`, `Edit`, `Write`, `Bash`, `Grep`, `Glob`, `NotebookEdit`)
- **Sandbox constraint:** every file operation's path must be under `.runtime/worktrees/[experiment-id]/`. Orchestrator validates the patch path prefix before accepting.

### Enforcement

Prefer SDK-level restriction when dispatching (e.g., Task tool with explicit `allowed_tools`). If unavailable, orchestrator scans subagent transcripts post-hoc and hard-fails the role on forbidden tool invocations. Log enforcement events in `experiments.tsv` comment.

```python
# Dispatch template
dispatch_subagent(
    role="reporter",
    allowed_tools=["Read", "Grep", "Glob", "Write"],
    allowed_write_paths=[
        "[project]/evolver/reports/",
        "[project]/last-evolution.md",
        "[project]/PRODUCT-EVOLUTION-REPORT.md",
        "[project]/scoring-log.md",
        "context/learnings.md",
        "context/dispositions/",  # disposition write-back
    ],
    deny_tools=["Edit", "Bash", "WebFetch", "WebSearch"],
    system_prompt=(
        "You are the reporter. Write access is scoped to the paths listed. "
        "Disposition write-back to context/dispositions/ is a mandatory "
        "round-close responsibility when promoted experiments exist."
    ),
    prompt=reporter_task,
)
```

---

## The Four Lenses (with Multi-Track Evaluation)

### Lens 1: FUNCTIONAL CRAWL
| Track | Type | Verifier |
|-------|------|----------|
| endpoint_health | binary | External tool (curl/httpie) |
| error_handling | 1-10 | LLM judge |
| empty_state_coverage | percentage | Deterministic (count of routes with empty state handling / total routes) |
| validation_completeness | 1-10 | LLM judge |

**Lap size:** 3-5 steps (mechanical fixes, fast feedback). Statistical lap verdicts apply (PROMISING/EXHAUSTED/NOISY).

### Lens 2: USER SIMULATION
| Track | Type | Verifier |
|-------|------|----------|
| task_completion | binary per persona | LLM judge (simulating persona journey) |
| time_to_value | 1-10 | LLM judge |
| friction_points | count (lower better) | LLM judge + deterministic (grep for console.error, missing feedback) |
| accessibility | 1-10 | External tool (axe-core) or LLM judge fallback |

**Lap size:** 2-3 steps (persona simulations are expensive). Statistical lap verdicts apply.

### Lens 3: COMPETITIVE INTELLIGENCE
| Track | Type | Verifier |
|-------|------|----------|
| feature_parity | percentage | Deterministic (features matched / competitor features) |
| differentiation | 1-10 | LLM judge |
| gap_severity | 1-10 per missing feature | LLM judge |

**Lap size:** 1-2 steps (research + implement is heavy)

**Lens constraint:** COMPETITIVE laps produce 1-2 data points — statistical analysis is not applicable. For this lens, fall back to keep/revert binary. Do not compute lap verdicts (PROMISING/EXHAUSTED/NOISY) — the sample size is too small. Record `lap_verdict = "-"` in experiments.tsv for COMPETITIVE rows.

### Lens 4: PRODUCT BRAINSTORM
| Track | Type | Verifier |
|-------|------|----------|
| user_impact | 1-10 | LLM judge (rubric) |
| implementation_quality | 1-10 | External tool (Inspector or Polisher) or LLM judge |
| novelty | 1-10 | LLM judge |

**Lap size:** 1-2 steps (creative ideas need breathing room)

**Lens constraint:** Same as COMPETITIVE — BRAINSTORM laps degrade to keep/revert binary. Statistical verdicts are not meaningful with 1-2 data points. Record `lap_verdict = "-"` for BRAINSTORM rows.

**Verifiers are LOCKED once the run begins.** You cannot change how you measure while measuring. Swapping a verifier mid-run invalidates prior data points. If a verifier misfires, log in experiments.tsv comment and halt the lens.

---

## How to Invoke

- "Multi-track product evolve [project]"
- "Product evolution on [project]"
- "Deep product evolve [project] with tracks"
- "Product evolve with dispositions"

The Product Evolver will ask: "Operational mode — literature or benchmark?" (unless specified). Then it runs.

---

## Execution Modes

### Brainless (default for overnight)
All 4 lenses run autonomously. Full rotation cycles until stopping conditions.

Trigger: "evolve overnight", "brainless", "I'm going to sleep"

### Controlled (interactive)
Pauses after each 4-lens rotation and shows:
- Per-lens, per-track score trajectory
- Lap verdicts for CRAWL and USER (statistical)
- Keep/revert summary for COMPETITIVE and BRAINSTORM (binary)
- Disposition updates and which ones informed hypotheses this round
- Lens efficiency report (after 3+ rotations)
- Meta-loop proposals (if any)
- Options: [Continue] [Focus lens] [I have an idea] [Stop and report]

Trigger: "controlled mode", "evolve with me"

### Hybrid (recommended)
- CRAWL + USER: brainless (mechanical fixes)
- COMPETITIVE: pauses before implementing — shows competitor gap, asks "should I build this?"
- BRAINSTORM: pauses before implementing — shows the idea, asks "worth building?"

Trigger: "hybrid", "auto on fixes, ask me on features"

---

## Step 0: Deep Orient

### 0.1 — Read Shared Context
Same as the base evolver: soul.md, preferences.md, learnings.md, dispositions/, and the per-lens dnr.

| File | Purpose | If missing |
|------|---------|------------|
| `context/soul.md` | Who the operator is, decision style | Use neutral defaults |
| `context/preferences.md` | Output format, what he hates | Default to concise, clean output |
| `context/learnings.md` | Previous evolution runs — don't repeat failed approaches | Treat as first run |
| `context/dispositions/` | Learned priors from past runs — inform per-lens hypothesis generation | Cold start: no priors |
| `[project]/evolver/do-not-repeat.md` | **MANDATORY for planner** — failed hypotheses log with lens column | Create empty with header |

### 0.2 — Read Project Context
Read in priority order: CLAUDE.md, README.md, brief.md, progress.md, decisions.md, last-evolution.md, package manifests.

### 0.3 — Cross-Run Continuity
If the project was previously evolved (check for `last-evolution.md` or existing `results.tsv`):
1. Read prior `results.tsv` — identify which lenses/tracks plateaued vs which have headroom
2. Read prior `evolution-assertions.json` — load accumulated assertions
3. Read prior `do-not-repeat.md` — inherit all entries (anti-forgetting across runs, lens-scoped)
4. Read prior `context/dispositions/product_*.json` — inherit priors
5. Start from the prior final state, not from scratch
6. Log: "Continuing from prior evolution: baseline [X], [N] assertions, [M] dnr entries, [K] dispositions inherited"

### 0.4 — Detect Project Type
Scan for project type (WEB_APP, API_SERVICE, LIBRARY, CLI_TOOL, STATIC_SITE, etc.). Adapt lens behavior per type.

### 0.5 — Functional Crawl (Deep)
Map everything the product CAN do. Save as `PRODUCT-MAP.md`.

### 0.6 — Build Personas
From ICP file + target users: define 3-5 personas with name, role, goal, technical comfort.

### 0.7 — Competitor Cache
If `PRODUCT-MAP.md` already has a competitors section from a prior run, **reuse it**. Skip the web search phase for already-analyzed competitors. Only search for NEW competitors if:
- No competitor data exists
- Prior data is >30 days old
- User explicitly requests refresh

This saves significant time on repeat runs.

### 0.8 — Initialize do-not-repeat Memory

Create `[project]/evolver/do-not-repeat.md` if absent:

```markdown
# Do Not Repeat — Failed Hypothesis Log (Product Evolver, multi-track, lens-scoped)

Planner MUST `Read` this file before emitting any new hypothesis.
Reviewer MUST reject any hypothesis whose signature substring-matches a prior entry in the same lens.
Every reverted or archived experiment appends a row.

Schema:
---
date: YYYY-MM-DD
step: <N>
lap: <N>
round: <N>
lens: <CRAWL|USER|COMPETITIVE|BRAINSTORM>
hypothesis: <one-line summary>
signature: <normalized phrase for dedup (lens-scoped)>
failure_reason: <why archived>
tracks_affected: <per-track deltas JSON>
aggregate_delta: <value>
lap_verdict: <PROMISING|EXHAUSTED|NOISY|-   (- for COMPETITIVE/BRAINSTORM binary laps)>
persona: <only filled for USER>
competitor: <only filled for COMPETITIVE>
evidence: <archive/[lens]/[exp-id].md path or commit hash>
---
```

**Planner contract:** Every hypothesis proposal includes a `dnr_check` field: `clear` or `collision: <signature>`. On collision, planner retries (max 3) then escalates to reviewer for alternative track/lens selection.

**Reviewer contract:** Independently re-runs the substring check within the same lens. Disagreement with planner = protocol violation, log and abort.

**Append contract:** Orchestrator (not planner — planner has no Edit) appends a row on every revert, crash, or EXHAUSTED lap verdict that chose not to continue the family.

**Cross-lens signature namespace:** Signatures are lens-scoped — a BRAINSTORM idea can still be tried even if a COMPETITIVE hypothesis touching the same feature area already failed. The `lens:` field makes this explicit.

### 0.9 — Data Plane Layout

```
[project]/
├── evolver/
│   ├── do-not-repeat.md              # append-only, IN git (failure audit per lens)
│   ├── results.tsv                    # append-only ledger (alias: experiments.tsv), OUT of git
│   ├── scoring-log.md                 # IN git, append-only scoring audit
│   ├── backlog.md                     # IN git, misclassified proposals awaiting correct lens
│   ├── live/                          # OUT of git, promoted winners per lens
│   │   └── .gitignore                 # *
│   ├── reports/                       # IN git; reporter writes
│   ├── archive/                       # IN git; reverted experiments organized by lens
│   │   ├── crawl/
│   │   ├── user/
│   │   ├── competitive/
│   │   └── brainstorm/
│   ├── submit_result.py               # IN git; append-only submitter
│   └── meta-loop.md                   # IN git; self-modifying loop definition
├── context/dispositions/              # IN git at WORK root; cross-target learned priors
│                                       # REPORTER writes here (disposition write-back)
├── PRODUCT-MAP.md                     # IN git; updated throughout
├── last-evolution.md                  # IN git; next-session marker
├── PRODUCT-EVOLUTION-REPORT.md        # IN git; end-of-run report
├── evolution-assertions.json          # IN git; cross-run assertion set
└── [project files...]
```

Add `[project]/evolver/live/` and `[project]/evolver/results.tsv` and `[project]/evolver/experiments.tsv` to root `.gitignore`.

**`results.tsv` schema (tab-separated, append-only, multi-track + lens columns):**
```
timestamp	step	lap	round	experiment_id	operator	mode	lens	track_scores_json	aggregate	score_before	score_delta	verdict	verifier_type	disposition_used	signature	hypothesis	promoted	worktree_path	lap_verdict	persona	competitor	comment
```

- `track_scores_json`: JSON object `{"endpoint_health": 1, "error_handling": 7, "empty_state_coverage": 0.6, "validation_completeness": 8}` — one key per track for the current lens
- `aggregate`: normalized weighted average (0-1)
- `verdict`: `win` | `revert` | `crash` | `skip` | `regression` | `reflection`
- `verifier_type`: `tests` | `inspector` | `polisher` | `count` | `llm_judge` | `fallback_build`
- `disposition_used`: name/id of disposition that informed this step, or `-`
- `lap_verdict`: `PROMISING` | `EXHAUSTED` | `NOISY` | `-` (always `-` for COMPETITIVE/BRAINSTORM due to small n)
- `promoted`: `true` only if `mode=benchmark AND verdict=win` (enforced by submit_result.py)
- `persona`: filled only for USER lens rows
- `competitor`: filled only for COMPETITIVE lens rows

### 0.10 — Setup
- `git checkout -b product-evolution/[project]-[date]`
- Run baseline metric (per lens, per track) via experiment-worker, record as step 0 per lens
- Load dispositions from `context/dispositions/product_[type].json` and `context/dispositions/cross_domain.json`
- Write `submit_result.py` into `[project]/evolver/`
- Validate ALL track verifiers respond: run each once against baseline, confirm it returns a score

### 0.11 — Initialize Assertion Layer
1. Check if `evolution-assertions.json` exists from a previous run
   - If yes: load, run immediately, report drift
   - If no: create empty `[]`
2. Locate assertion runner: `tools/assertions/runner.py` from WORK root
3. Validate: `python runner.py --test` — if fails, warn and continue without assertions

---

## Worktree-per-Experiment

Each step runs in an isolated git worktree:

```bash
EXP_ID="exp-$(date +%s)-$RANDOM-$LENS"
git worktree add .runtime/worktrees/$EXP_ID HEAD
# Dispatch experiment-worker with cwd=.runtime/worktrees/$EXP_ID
# Worker's Edit/Write/Bash is effectively path-sandboxed
# Worker runs ALL track verifiers for the current lens within the worktree
# Worker calls submit_result.py (which appends to ../../evolver/results.tsv)
cd .runtime/worktrees/$EXP_ID
git diff HEAD > ../../patches/$EXP_ID.patch
# Orchestrator validates patch paths, applies or archives
git worktree remove .runtime/worktrees/$EXP_ID --force
```

**Non-git fallback:** `cp -r` + `diff -r` + `rm -rf`. Log in results.tsv comment: `"worktree: filesystem-copy (no git)"`.

**Why worktrees matter for product evolution:** multi-track verifiers compound side-effect risk — tests leave junit artifacts, Inspector leaves Markdown reports, Polisher leaves SARIF files, axe-core leaves a11y reports. Without isolation, concurrent or failed experiments leak state into the evolution branch. Worktrees prevent this. Also, parallel lens experiments (e.g., CRAWL and USER on independent modules) can run in separate worktrees — the orchestrator serializes patch application but parallelizes implementation.

---

## Step 1: The Rotation Loop

Rotate: CRAWL → USER → COMPETITIVE → BRAINSTORM → repeat.

### Pre-Flight (before each lens)
Run all accumulated assertions. Regression → revert or pause.

### Lens Boundaries (prevent overlap)
| Lens | DOES | DOES NOT |
|------|------|----------|
| CRAWL | Technical correctness: error handling, validation, dead code | Judge UX, add features |
| USER | Experience quality: friction, confusion, missing feedback | Fix code bugs (log for CRAWL) |
| COMPETITIVE | Feature gaps vs market | Fix bugs, improve existing UX |
| BRAINSTORM | Novel value: cross-module connections, surprise features | Fix existing issues |

Misclassification → redirect to `backlog.md` with corrected lens tag.

### Statistical Laps (CRAWL and USER only)

CRAWL and USER lenses use full statistical laps:
- Run N steps (3-5 for CRAWL, 2-3 for USER) in the same parameter family
- Compute distribution of aggregate scores across the lap
- Verdict: PROMISING (continue) / EXHAUSTED (switch) / NOISY (extend)

### Binary Laps (COMPETITIVE and BRAINSTORM)

COMPETITIVE and BRAINSTORM produce 1-2 data points per lap:
- Statistical analysis degrades — not applicable
- Use keep/revert binary decision
- No lap verdicts computed (`lap_verdict = "-"` in results.tsv)
- Still record for disposition learning

### Per-Step Flow (detailed)

```
0. PRE-FLIGHT: Run all accumulated assertions from evolution-assertions.json
   - All pass → proceed
   - Any fail → REGRESSION DETECTED
     a. Log which assertion(s) failed
     b. In brainless: revert to last safe commit, log as REGRESSION in results.tsv
     c. In controlled/hybrid: pause, offer [Revert] [Accept] [Investigate]

1. DISPATCH planner (Read/Grep/Glob/WebSearch/WebFetch only). Planner:
   - Reads results.tsv (current per-lens, per-track trajectory)
   - Reads do-not-repeat.md (to avoid lens-scoped collisions)
   - Reads dispositions for (problem_class, action_intent) matching the current lens
   - Reads archive/[lens]/ for patterns (every complexity addition in BRAINSTORM failed → try simplification)
   - Identifies weakest track in current lens (lowest normalized score)
   - Emits: { hypothesis, signature, lens, dnr_check, target_track, disposition_used }

2. DISPATCH reviewer (Read/Grep/Glob only). Reviewer:
   - Re-checks dnr signature match (lens-scoped)
   - Checks lens boundaries (is this actually the right lens?)
   - Checks guardrails
   - Checks operational mode gate (literature → no promotion allowed)
   - Returns approve | reject | redirect-to-backlog
   If rejected, loop to planner (max 3 retries before escalating/skipping lens)

3. ORCHESTRATOR creates worktree:
   EXP_ID="exp-$(date +%s)-$RANDOM-$LENS"
   git worktree add .runtime/worktrees/$EXP_ID HEAD

4. DISPATCH experiment-worker (full surface, sandboxed to worktree). Worker:
   - Implements hypothesis per lens
   - Runs EACH track's verifier for the current lens inside worktree
   - Collects track_scores, computes aggregate
   - Calls submit_result.py with all track scores + lens + verifier_type + mandatory comment
   - Emits patch: git diff HEAD > patches/$EXP_ID.patch

5. ORCHESTRATOR validates patch paths ⊆ worktree, then decides:
   IF aggregate_score > previous_aggregate by >= 0.01 (normalized):
     - Apply patch to evolution branch
     - git commit -m "step $STEP [$LENS]: $HYPOTHESIS — aggregate $BEFORE → $AFTER"
     - (benchmark mode only) Promote to live/
     - Update PRODUCT-MAP.md if new features/endpoints/pages
     - Generate 1-3 assertions (specificity + revert-check gates)
   ELSE:
     - Drop patch
     - Write archive/[lens]/$EXP_ID.md with reasoning + per-track deltas + lesson
     - APPEND row to do-not-repeat.md (with lens tag)

6. CLEANUP worktree: git worktree remove .runtime/worktrees/$EXP_ID --force
```

### Lap Verdict (CRAWL and USER only, after N steps in same parameter family)

Analyze the distribution of aggregate scores across the lap:
- **PROMISING:** Scores trending up, variance decreasing → continue this family
- **EXHAUSTED:** No improvement across the distribution → switch parameter family, mark family signature in do-not-repeat
- **NOISY:** High variance, no clear trend → extend lap by 3 to determine signal

Append a lap-close row to results.tsv with `verdict=reflection`, `lap_verdict` filled in.

### Lens Efficiency Tracking

After 3 full rotations, compute per-lens efficiency:
- `kept_ratio = kept_changes / total_experiments` per lens
- Report which lens has the best ratio
- Suggest skipping lenses with <10% kept ratio ("COMPETITIVE lens appears exhausted — 1/12 changes kept. Consider skipping.")
- Never auto-skip — only suggest. User confirms in controlled/hybrid. In brainless mode, skip after 3 consecutive rotations of 0% kept ratio for that lens.

### Round Reflection (after all laps across all 4 lenses)

1. Which lenses improved? Which plateaued?
2. Which parameter families were PROMISING vs EXHAUSTED (CRAWL/USER)?
3. Which personas benefited most (USER)?
4. Which competitors contributed kept features (COMPETITIVE)?
5. Which BRAINSTORM angles landed (cross-module, unused data, etc.)?
6. **Dispatch reporter to update dispositions** (disposition write-back — see next section)
7. If a meta-loop proposal is warranted, generate it (see Meta-Loop below)
8. Reporter writes `reports/round-[N].md` summary
9. Log reflection in results.tsv as a REFLECTION row

---

## Disposition Integration (WITH WRITE-BACK)

**Why this matters:** The disposition write-back path is only effective when a role holds Write permission to `context/dispositions/`. If no role has that access — for example, if the planner reads dispositions but no writer is registered — the directory stays empty and learned priors never accumulate across runs.

**Design:** Reporter is the **sole writer** to `context/dispositions/`. Disposition write-back is triggered automatically at round-close (step 6 in Round Reflection, above) on any round with at least one promoted experiment.

### Reading Dispositions (planner, at step start)

```
Before each hypothesis, planner runs this checklist:

0. Read do-not-repeat.md — enumerate signatures to skip (lens-scoped)
1. Read results.tsv — what's been tried (full per-lens ledger)
2. Identify weakest track in current lens (lowest normalized score)
3. Check dispositions for (problem_class, action_intent) matching this lens + track:
   - For CRAWL: problem_class examples: "product_web/endpoint_health", "product_api/error_handling"
   - For USER: problem_class examples: "product_web/persona_friction", "product_web/onboarding_gap"
   - For COMPETITIVE: problem_class examples: "product_web/competitive_gap", "product_api/feature_parity"
   - For BRAINSTORM: problem_class examples: "product_web/cross_module", "product_web/unused_data"
   - Prior > 0.6 AND confidence > 0.7 → try this first
   - Prior < 0.3 AND confidence > 0.7 → skip
   - No matching disposition → neutral prior, try and learn
4. Check archive/[lens]/ — don't repeat experiments that already failed (belt + suspenders)
5. Emit ONE specific change targeting the weakest track in current lens
6. Emit signature normalized from hypothesis (lowercase, strip articles, hash key nouns)
7. Run dnr_check locally: substring-match signature against do-not-repeat.md entries (same lens)
   - clear → return hypothesis
   - collision → retry (max 3, then escalate to reviewer for alternative track/lens selection)
```

### Writing Dispositions (reporter, at round-close)

At round-close, reporter performs disposition write-back for every promoted experiment in the round:

```python
# Pseudocode — reporter subagent logic at round-close
for exp in round_experiments where promoted == True:
    lens = exp.lens
    problem_class = f"product_{project_type}/{exp.target_track}"
    action_intent = extract_action_intent(exp.hypothesis)  # e.g., "add_empty_state_handler"

    disp_file = f"context/dispositions/product_{project_type}.json"
    load_or_create(disp_file)

    existing = find_disposition(disp_file, problem_class, action_intent)
    if existing:
        existing.times_applied += 1
        existing.times_succeeded += 1 if exp.verdict == "win" else 0
        existing.prior = existing.times_succeeded / existing.times_applied
        existing.confidence = min(existing.times_applied / 20, 1.0)
        existing.evidence.append({
            "run": f"{project}-{date}",
            "target": project_path,
            "lens": lens,
            "outcome": f"improved_by_{delta}",
            "tracks_affected": list(exp.track_scores.keys()),
            "timestamp": now_iso(),
        })
        existing.last_updated = now_iso()
    else:
        create_disposition({
            "id": f"disp-{timestamp}",
            "problem_class": problem_class,
            "action_intent": action_intent,
            "prior": 1.0 if exp.verdict == "win" else 0.0,
            "confidence": 0.05,  # cold-start, grows with evidence
            "evidence": [...],
            "notes": f"[{lens}] {exp.hypothesis[:80]}",
            "created": now_iso(),
            "last_updated": now_iso(),
            "times_applied": 1,
            "times_succeeded": 1 if exp.verdict == "win" else 0,
        })

    save(disp_file)
```

Also write reverted experiments (`verdict=revert`) — they lower the prior for (problem_class, action_intent) pairs and inform future rounds not to repeat.

### Disposition Cold-Start

With <20 evidence entries across all dispositions in a domain, frame dispositions as "notes from past runs" — not statistical priors. Log: "Disposition cold-start: [N] evidence entries, treating as hints."

### Safety: Meta-Loop Disposition Validation

Before applying any disposition, validate:
- **Auto-reject** any disposition with positive prior on security-weakening patterns:
  - `action_intent` contains: "remove_validation", "skip_auth", "disable_error_handling", "remove_tests", "weaken_security"
  - Log: "DISPOSITION-REJECTED: [id] — unsafe action_intent [action_intent]"
- Prevents disposition poisoning where a series of bad runs could teach the Evolver to weaken security.

---

## Scoring

Normalization (binary=0/1, percentage=value/100, 1-10=(value-1)/9).

**Primary metric** (pick best available):
1. Test suite → pass rate %
2. Inspector → ship-readiness score
3. Polisher → health score
4. Fallback → builds(25) + starts(25) + healthcheck(25) + no-errors(25)

**Product quality overlay:**
- User Impact (1-10): rubric
- Implementation Quality (1-10): rubric
- Combined: `(primary × 0.6) + (user_impact × 4 × 0.2) + (impl_quality × 4 × 0.2)`

**No win claims without a benchmark run (mode gate):** In benchmark mode, aggregate score must come from verifier output (tests/Inspector/Polisher/count/judge). Planner-asserted scores are rejected by submit_result.py.

**Score audit trail (scoring-log.md, IN git, append-only):**
Reporter writes one entry per step:
```
## Step [N] — Lap [M] Round [K] — Lens [LENS]
- Verifier type: [tests|inspector|polisher|count|llm_judge|fallback_build]
- Per-track scores: { track_name: value, ... } (all tracks for this lens)
- Aggregate (normalized): [0-1]
- Score before: [0-1]
- Delta: [signed]
- Disposition used: [id or -]
- Decision: KEEP / REVERT / REFLECTION
- Lap verdict (if close): [PROMISING|EXHAUSTED|NOISY|-]
- Patch: [path to patches/$EXP_ID.patch]
```

---

## Failure Archive

Reverted experiments are archived per lens rather than forgotten:

```
[project]/evolver/archive/
├── crawl/
│   └── exp-007-added-retry-logic.md
│       reason: aggregate gained on error_handling but lost on empty_state_coverage
│       tracks_affected: {error_handling: +2, empty_state_coverage: -0.1}
│       lesson: retry logic should not block empty-state paths
├── user/
├── competitive/
│   └── exp-012-copied-dashboard.md
│       reason: differentiation dropped (looked too similar to ServiceNow)
│       tracks_affected: {feature_parity: +0.2, differentiation: -3, gap_severity: 0}
│       lesson: feature parity with competitor ≠ value — differentiation matters more
└── brainstorm/
    └── exp-015-cross-module-alert.md
        reason: novelty was high but implementation_quality was low
        tracks_affected: {novelty: +3, implementation_quality: -2, user_impact: +0.5}
        lesson: novel features need a spike first; don't land novelty in one step
```

`archive/[lens]/` entries are long-form reasoning; `do-not-repeat.md` is the lens-scoped fast-lookup index.

---

## Self-Modifying Meta-Loop

The evolution loop itself is defined in `[project]/evolver/meta-loop.md`. The Evolver can propose modifications to its own loop:

Examples:
- "Lap size of 5 for CRAWL is too large for this project — reduce to 3"
- "LLM judge on user_impact disagrees with Inspector on implementation_quality — investigate alignment"
- "Competitor X's feature parity shouldn't be pursued — users prefer simplicity per rounds 1-3"

**Safety gates:**
- In controlled/hybrid mode: meta-loop modifications require HUMAN GATE
- In brainless mode: meta-modifications are logged but NOT applied (conservative default)
- **In literature mode: meta-loop modifications are proposal-only, never applied** (mode gate)
- **Auto-reject rule 1:** Any meta-loop modification that would weaken security-related tracks (validation_completeness, error_handling, auth checks) is auto-rejected: "META-REJECTED: [proposal] — would weaken security track [track_name]"
- **Auto-reject rule 2:** Any meta-loop modification that would violate the tool-surface invariants (planner/reviewer/reporter getting expanded surface, experiment-worker escaping worktree) is auto-rejected: "META-REJECTED: [proposal] — would violate multiautoresearch tool-surface invariant"
- **Auto-reject rule 3:** Any meta-loop modification that would revert the disposition write-back design (removing Write permission to `context/dispositions/` from reporter, or moving the responsibility to a non-writing role) is auto-rejected: "META-REJECTED: [proposal] — would re-introduce the disposition-empty bug"

---

## submit_result.py

Each project gets `[project]/evolver/submit_result.py`. Append-only, mandatory comment, lens-required, promoted-flag enforced.

```python
#!/usr/bin/env python3
"""
submit_result.py — Product Evolver multi-track, 4-lens append-only submitter.

Usage:
    python submit_result.py \\
        --step 42 --lap 3 --round 2 \\
        --experiment-id exp-042-CRAWL \\
        --lens CRAWL \\
        --hypothesis "Added empty-state handler for /api/reports when no data" \\
        --signature "empty_state_handler_reports" \\
        --mode benchmark \\
        --operator experiment-worker \\
        --verdict win \\
        --verifier-type tests \\
        --track-scores '{"endpoint_health": 1, "error_handling": 7, "empty_state_coverage": 0.85, "validation_completeness": 8}' \\
        --aggregate 0.79 \\
        --score-before 0.72 \\
        --disposition-used "simplification-beats-complexity" \\
        --worktree-path .runtime/worktrees/exp-042-CRAWL \\
        --lap-verdict "-" \\
        --persona "-" \\
        --competitor "-" \\
        --comment "REQUIRED — explain hypothesis + observed per-track deltas"

Invariants:
- Appends ONE row to evolver/results.tsv. Never edits prior rows.
- --comment MANDATORY.
- --lens MANDATORY.
- Timestamp auto-generated.
- score_delta computed here.
- promoted=true REQUIRES mode=benchmark AND verdict=win (enforced, not trusted).
- track-scores must parse as JSON.
- For COMPETITIVE/BRAINSTORM lenses, lap_verdict is auto-set to "-" (binary laps, no statistical verdict).
"""

import argparse
import csv
import datetime as dt
import json
import pathlib
import sys

LEDGER = pathlib.Path(__file__).parent / "results.tsv"
HEADER = [
    "timestamp", "step", "lap", "round", "experiment_id", "operator", "mode",
    "lens", "track_scores_json", "aggregate", "score_before", "score_delta",
    "verdict", "verifier_type", "disposition_used", "signature", "hypothesis",
    "promoted", "worktree_path", "lap_verdict", "persona", "competitor", "comment",
]


def main() -> int:
    p = argparse.ArgumentParser(description="Append a row to Product Evolver results.tsv.")
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--lap", type=int, required=True)
    p.add_argument("--round", type=int, required=True)
    p.add_argument("--experiment-id", required=True)
    p.add_argument("--lens", required=True,
                   choices=["CRAWL", "USER", "COMPETITIVE", "BRAINSTORM"])
    p.add_argument("--hypothesis", required=True)
    p.add_argument("--signature", required=True,
                   help="Normalized dedup key for do-not-repeat matching (lens-scoped).")
    p.add_argument("--mode", required=True, choices=["literature", "benchmark"])
    p.add_argument("--operator", required=True,
                   choices=["planner", "reviewer", "reporter",
                            "experiment-worker", "orchestrator"])
    p.add_argument("--verdict", required=True,
                   choices=["win", "revert", "crash", "skip",
                            "regression", "reflection"])
    p.add_argument("--verifier-type", required=True,
                   choices=["tests", "inspector", "polisher", "count",
                            "llm_judge", "fallback_build"])
    p.add_argument("--track-scores", required=True,
                   help="JSON: {track_name: score, ...}")
    p.add_argument("--aggregate", type=float, required=True)
    p.add_argument("--score-before", type=float, required=True)
    p.add_argument("--disposition-used", default="-")
    p.add_argument("--worktree-path", default="-")
    p.add_argument("--lap-verdict", default="-",
                   choices=["-", "PROMISING", "EXHAUSTED", "NOISY"])
    p.add_argument("--persona", default="-",
                   help="Required for USER lens; '-' for others.")
    p.add_argument("--competitor", default="-",
                   help="Required for COMPETITIVE lens; '-' for others.")
    p.add_argument("--comment", required=True,
                   help="MANDATORY — mechanical append with no context is forbidden.")
    args = p.parse_args()

    if not args.comment.strip():
        print("ERROR: --comment may not be empty.", file=sys.stderr)
        return 2

    # Parse track scores
    try:
        tracks = json.loads(args.track_scores)
        if not isinstance(tracks, dict):
            raise ValueError("track-scores must be a JSON object")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"ERROR: --track-scores invalid JSON: {e}", file=sys.stderr)
        return 2

    # Lens-specific validation
    if args.lens == "USER" and args.persona == "-":
        print("WARNING: USER lens without --persona — recording anyway but recommend filling.",
              file=sys.stderr)
    if args.lens == "COMPETITIVE" and args.competitor == "-":
        print("WARNING: COMPETITIVE lens without --competitor — recommend filling.",
              file=sys.stderr)

    # Binary lap enforcement: COMPETITIVE and BRAINSTORM cannot have statistical verdicts
    lap_verdict = args.lap_verdict
    if args.lens in ("COMPETITIVE", "BRAINSTORM") and lap_verdict != "-":
        print(f"NOTE: {args.lens} uses binary laps — forcing lap-verdict to '-'.",
              file=sys.stderr)
        lap_verdict = "-"

    # Invariant: promoted only in benchmark mode on a win
    promoted = args.mode == "benchmark" and args.verdict == "win"
    delta = round(args.aggregate - args.score_before, 4)

    if not LEDGER.exists():
        with LEDGER.open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh, delimiter="\t").writerow(HEADER)

    row = [
        dt.datetime.now(dt.timezone.utc).isoformat(),
        args.step, args.lap, args.round, args.experiment_id,
        args.operator, args.mode, args.lens,
        json.dumps(tracks, separators=(",", ":")),
        args.aggregate, args.score_before, delta,
        args.verdict, args.verifier_type,
        args.disposition_used, args.signature, args.hypothesis,
        str(promoted).lower(), args.worktree_path, lap_verdict,
        args.persona, args.competitor, args.comment,
    ]
    with LEDGER.open("a", newline="", encoding="utf-8") as fh:
        csv.writer(fh, delimiter="\t").writerow(row)
    print(f"Appended: step={args.step} lap={args.lap} round={args.round} "
          f"[{args.lens}] {args.verdict} Δ={delta} promoted={promoted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Writer contract: every append call MUST come from this script. Direct writes to results.tsv are a protocol violation. Orchestrator may `tail` the file but not `edit` it.

---

## Stopping Conditions

- 3 consecutive ROUNDS with no improvement across all lenses/tracks
- Budget exhausted (default: 50 steps or user-specified)
- All tracks at ceiling (normalized aggregate > 0.95 per lens)
- User says stop
- Going in circles (do-not-repeat catches this — same signature proposed + reverted 3+ times)
- 5 consecutive experiments across ALL lenses fail to improve
- All 4 lenses cycled 3+ times with 0% kept ratio (lens-efficiency auto-skip in brainless)

---

## Guardrails

**Before starting, verify:**
- No uncommitted changes on current branch (stash or commit first)
- Not on main/master/production branch
- No active deploy or CI pipeline running
- Database migrations: NEVER auto-apply. Generate files, log them, let the operator review.

**During evolution, NEVER:**
- Delete .env files, credentials, or secrets
- Modify CI/CD pipeline configuration
- Change authentication/authorization logic without explicit approval (project mode)
- Remove existing tests
- Downgrade dependencies
- Make changes outside the project directory
- **Write outside the experiment-worker's worktree** (sandbox invariant)
- **Promote to `live/` in literature mode** (operational mode gate)
- **Emit a hypothesis whose signature substring-matches do-not-repeat.md within the same lens** (lens-scoped dnr invariant)
- **Allow a subagent role to invoke a tool outside its registered surface** (tool-surface invariant)
- **Let any role other than reporter write to `context/dispositions/`** (disposition write-back invariant)

**If something breaks badly:**
1. `git stash` the current experiment (or remove the worktree)
2. Log the failure in results.tsv with aggregate 0, verdict=crash
3. Append to do-not-repeat.md + archive/[lens]/
4. Move on to next hypothesis

---

## Output Discipline

- **Redirect all output to files.** Never flood context.
- **Read only the metric.** grep for score/pass rate.
- **results.tsv is your real memory.** Append-only via submit_result.py, never committed (in `.gitignore`), never deleted.
- **Git branch is curated memory.** Only wins. do-not-repeat.md + archive/ + scoring-log.md + backlog.md IS in git as the audit trail.

**Assertion decay — every 10 steps:**
Run assertion maintenance:
1. Update metadata: increment `survived` count, promote confidence tiers
2. If >50 assertions: prune "new" that never caught regression (oldest first)
3. Log pruning in results.tsv comment

**Compaction protocol — every 5 steps:**
```
PRODUCT EVOLUTION STATE — DO NOT LOSE:
- Project: [name and path]
- Branch: [branch name]
- Operational mode: [literature|benchmark]
- Step: [N] of max 50, Lap: [N], Round: [N]
- Current lens: [CRAWL|USER|COMPETITIVE|BRAINSTORM]
- Next lens: [which one]
- Per-lens track scores (latest): [lens: {track: score, ...}]
- Per-lens aggregate trajectory: [lens: [0.64, 0.71, 0.76, 0.80]]
- Weakest lens/track: [lens] / [track] at [normalized score]
- Current lap verdict: [PROMISING|EXHAUSTED|NOISY|-]
- PRODUCT-MAP.md: [path] — DO NOT re-crawl
- results.tsv: [path] — append-only via submit_result.py (NOT in git)
- do-not-repeat.md: [path] — [N] entries, lens-scoped
- backlog.md: [path] — misclassified proposals waiting for correct lens
- Competitors cached: [list or "not yet"]
- Personas: [count] in PRODUCT-MAP.md
- Lens efficiency: [lens: kept/total ratio]
- Dispositions loaded: [N] from [domains]
- Dispositions updated this session: [N] (disposition write-back confirmed active)
- Assertions: [N] total ([M] new, [O] established, [P] high confidence)
- Archive entries: [N] failed experiments documented per lens
- Active worktrees: [list] — MUST be cleaned up before compaction
- Key insight: [one line]
```

---

## When Done — Agentic OS Integration

### 1. Update PRODUCT-MAP.md (orchestrator + reporter)
Final version reflecting all additions.

### 2. Update Project CLAUDE.md (reporter)
Current State: "product-evolved [N] steps, [L] lenses, aggregate [X→Y], dispositions updated"

### 3. Write Evolution Marker (reporter)
```markdown
## Last Evolution Run
- Date: [timestamp]
- Engine: product-evolver (multi-track, 4-lens)
- Operational mode: [literature|benchmark]
- Branch: product-evolution/[project]-[date]
- Steps: [N] total, [M] kept, [K] archived, [J] in do-not-repeat
- Lenses: CRAWL [N kept/total], USER [N], COMPETITIVE [N], BRAINSTORM [N]
- Aggregate: [X] → [Y] overall; per-lens finals: {lens: aggregate}
- Rounds: [N], Laps: [N]
- Lens efficiency: [best lens and ratio]
- Dispositions: [N] loaded, [M] updated, [K] new (write-back fired successfully)
- Competitors analyzed: [list]
- Mode: [brainless/controlled/hybrid]
```

### 4. Update context/learnings.md (reporter)
Per-lens What Worked / What Didn't, reference disposition write-back status.

### 5. Update Dispositions (reporter)
Reporter writes updated/new dispositions to `context/dispositions/product_[type].json`. Confirm write succeeded — log "DISPOSITIONS WRITTEN: [N] updated, [M] new, file size before/after" in scoring-log.md.

**Verification step (mandatory):** After writing, Read the disposition file back. If it's still empty or the count didn't change, log "DISPOSITION WRITE-BACK FAILED — investigate write permissions" and surface it to the operator. This is the write-back canary.

### 6. Write Product Evolution Report (reporter)
`PRODUCT-EVOLUTION-REPORT.md` with:
- Per-lens breakdown (kept/reverted, best find, track trajectory chart)
- Disposition summary (read count, write count, new vs updated)
- Competitor analysis
- Persona impact summary
- BRAINSTORM ideas landed vs reverted
- do-not-repeat.md contributions this run (per lens)
- Archive highlights (top 3 lessons learned)
- Recommendations for next run

### 7. Preserve Assertions
Commit `evolution-assertions.json` on evolution branch.

### 8. Final Commit
`"product-evolution complete: [project] — [N] steps, aggregate [X→Y], [M] dispositions updated, dnr + archive + learnings written"`

Commits include: `do-not-repeat.md`, `archive/[lens]/`, `reports/`, `submit_result.py`, `meta-loop.md`, `scoring-log.md`, `backlog.md`, `PRODUCT-MAP.md`, `evolution-assertions.json`, and `context/dispositions/*.json`. Commits do NOT include: `results.tsv`, `experiments.tsv`, `live/`.

### 9. Merge or Present
- Brainless: leave on branch for user review
- Controlled/hybrid: ask "Merge to main?"

---

## Reference Files

| File | Read When |
|------|-----------|
| `the-evolver/references/verifier-types.md` | Setting up tracks |
| `the-evolver/references/disposition-schema.md` | Reading/writing dispositions |
| `context/soul.md` | Every run |
| `context/preferences.md` | Every run |
| `context/learnings.md` | Every run |
| `context/dispositions/` | Every run (planner reads; reporter writes at round-close) |
| `context/brand/icp.md` | Building personas |
| `context/brand/positioning.md` | Competitive context |
| `PRODUCT-MAP.md` | Created during orient, updated throughout |
| `[project]/evolver/do-not-repeat.md` | **Every hypothesis** — mandatory planner/reviewer read (lens-scoped) |
| `[project]/evolver/results.tsv` | Every hypothesis — current per-lens ledger |
| `[project]/evolver/archive/[lens]/` | Adjudicating borderline hypotheses — long-form reasoning per lens |
| `[project]/evolver/backlog.md` | Each lens start — misclassified proposals waiting for correct lens |
