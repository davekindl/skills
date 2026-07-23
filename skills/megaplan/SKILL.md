---
name: megaplan
description: "Canonical deep architectural planning mode. Invoke when the user says 'megaplan', 'deep plan', 'deep think', 'architect this properly', 'think hard about this', 'I need a real architecture', '30 minute plan', or when a build pipeline uses '--megaplan'. Produces production-ready architecture documents by exploring multiple alternatives and deep-diving the best option."
---

# MEGAPLAN -- Deep Think Planning Mode

> "Weeks of coding saves hours of planning. MEGAPLAN takes those hours seriously."

**Progressive disclosure.** The five output-document templates are detailed and live in `references/` so this body stays lean. Load the relevant template only when you reach the layer that writes it:

| Layer / Doc | Template file |
|---|---|
| Layer 1 — `megaplan-progress.md` | `references/template-progress.md` |
| Layer 2 — `megaplan-alternatives.md` | `references/template-alternatives.md` |
| Layer 3 — `megaplan-architecture.md` | `references/template-architecture.md` |
| Layer 4 — `megaplan-validation.md` | `references/template-validation.md` |
| Summary — `MEGAPLAN-RESULT.md` | `references/template-result.md` |

**Announce at start (two-phase):**

1. On invocation: `Entering MEGAPLAN deep-think mode. Reading context... will announce complexity path after scoring.`
2. After complexity gate: `Complexity score: [N]/10. Running [light|standard|heavy] path. Expected runtime: [8-12 | 18-28 | 35-50] min. Headless mode: [on|off]. Gates: [list active gate IDs].`

## Relationship to Other Planning Skills

| Skill | When to Use | Depth | Output |
|-------|-------------|-------|--------|
| `superpowers:brainstorming` | Before any creative work. Explores intent, requirements, design. | Shallow-to-medium. Collaborative dialogue, 1-3 approaches sketched. | Approved design spec for a single feature or component. |
| `superpowers:writing-plans` | When you have a spec and need step-by-step implementation instructions. | Medium. Maps files, tasks, test steps. No alternative exploration. | Bite-sized task list an executing agent can follow blindly. |
| a strategy planner | Strategic business questions, prioritization, revenue modeling. | Medium. Business logic, not technical architecture. | Recommendations with ecosystem context, scenario models. |
| **MEGAPLAN** | Architecture with real trade-offs needing formal comparison. Multi-service systems, migrations, high-blast-radius brownfield work. | Deep. 3 full alternatives with data flows, failure modes, cost models. Then a complete deep-dive on the winner. | 5 documents: progress tracker, alternatives analysis, full architecture spec, validation report, summary with risk register. |

**Rule of thumb:** Use MEGAPLAN when the architecture has genuine trade-offs that need formal side-by-side comparison. If there is one obvious approach and the question is just "how do I implement it step by step," use `writing-plans` instead. If the question is "should I even build this," use a strategy planner. If you need to explore intent and shape requirements, start with `brainstorming` and escalate to MEGAPLAN if the design phase reveals architectural complexity.

**Escalation path:** `brainstorming` -> discovers complexity -> invoke MEGAPLAN. This is a valid and expected flow. MEGAPLAN can consume a brainstorming output as its input.

## When to Use

- **Complex system architecture** -- multi-service, multi-database, event-driven, real-time + batch hybrid
- **Migration planning** -- monolith to microservices, framework upgrades, database migrations, API versioning
- **Brownfield extensions with high blast radius** -- adding a major subsystem to an existing product where wrong choices propagate everywhere
- **Integration architecture** -- connecting 3+ external systems with different protocols, auth models, failure semantics
- **Any architecture where getting it wrong costs weeks of rework** -- if the cost of a bad decision is measured in days, MEGAPLAN is overkill; if it is measured in weeks or months, MEGAPLAN pays for itself
- **Build-pipeline architecture-phase replacement** -- when the `--megaplan` flag is set on a build-pipeline run, this skill replaces the standard architecture-generation phase

## When NOT to Use

- Single-file utilities, config changes, simple CRUD endpoints
- Projects with fewer than 10 source files AND fewer than 5 API endpoints (unless they have genuinely complex data flows)
- Business strategy questions (use a strategy planner)
- When the user says "just build it" -- respect urgency, suggest `writing-plans` instead

## How to Invoke

Direct triggers (any of these activate MEGAPLAN):
- "megaplan this architecture"
- "deep plan a service extension"
- "think hard about how to add real-time to an existing service"
- "architect this properly"
- "I need a real architecture for this"
- "30 minute plan"
- "deep think this"

Build-pipeline integration:
- `--megaplan` flag on the pipeline's architecture phase triggers this skill instead of standard architecture generation

## Complexity Gate (Testable Classifier)

Before starting Layer 2, compute a Complexity Score. **The gate is deterministic; no handwaves.**

### Score formula

Add 1 point for each condition that is true:

1. Codebase has 10+ source files (count files matching `*.py|*.js|*.ts|*.tsx|*.jsx|*.go|*.rs|*.java` under project src/)
2. Design requires 5+ API endpoints (endpoints enumerated in brief or existing code)
3. 2+ data stores OR 1 store + blob storage
4. 3+ external system integrations
5. Brownfield with existing production users (not fresh greenfield)
6. Migration required (framework bump, DB change, monolith-to-microservices, API versioning)
7. Real-time requirements (WebSocket, SSE, push, sub-second latency)
8. Event-driven components (queues, streams, pub/sub)
9. Multi-tenant or compliance scope (RBAC, PII, HIPAA, GDPR data rules)
10. Hot-path SLO exists (latency or availability budget in brief)

### Mapping

| Score | Mode | Layer 2 alternatives | Layer 3 sections |
|-------|------|---------------------|------------------|
| 0-2 | **Light path** | skip (single path) | minimum set (see Layer 3 minimum gate) |
| 3-5 | **Standard path** | 3 alternatives | full set |
| 6+ | **Heavy path** | 4 alternatives (1 "black swan" outlier required) | full set + supply-chain + DR sub-sections |

### Announce

Emit one line: `Complexity gate: score=[N]/10, path=[light|standard|heavy]. Scoring factors: [list true conditions].`

If the user explicitly asked for a specific mode ("simple", "light", "full", "heavy"), honour that override and log: `Gate overridden by user: [mode].`

**No "ask the user" ambiguity.** If critical input is missing (no brief AND no codebase to count), STOP — this is different from mode uncertainty. Score is always computable when context exists.

## Execution

### Output Directory

All MEGAPLAN outputs go into the project's architecture directory:
- Standalone: `./megaplan/` in the current working directory
- Architecture phase: `./02-architecture/` alongside standard pipeline outputs

### Input Requirements (Agentic-OS Aware)

Before starting Layer 1, read and internalize ALL of the following that exist. MEGAPLAN reads ecosystem-level sources that prevent re-deciding already-parked questions.

**Project-local context:**

| Source | What to Extract |
|--------|----------------|
| Project brief / requirements doc | Core problem, constraints, success criteria, non-functional requirements |
| Existing codebase (if brownfield) | Current architecture, tech stack, conventions, pain points, technical debt |
| Project CLAUDE.md | Identity, guardrails, architecture notes, known decisions |
| `lib-docs/` or Context7 | Current documentation for libraries/frameworks in play |
| `decisions.md` (if exists) | Prior architectural decisions and their rationale |
| `docs/` directory | Any existing architecture docs, API specs, diagrams |

**Agentic-OS shared context (read from WORK root):**

| Source | What to Extract |
|--------|----------------|
| `context/soul.md` | Decision style, risk tolerance |
| `context/preferences.md` | Tech preferences, output expectations |
| your lessons log | Past architectural mistakes |
| your backlog file | **Previously parked items with gate conditions.** Previously-parked items with gate conditions are pre-analyzed alternatives waiting for trigger events. If the current megaplan would re-examine a parked item, quote the parked entry in Layer 1 and honor the parked decision unless the gate has fired. |
| `megaplan/*/MEGAPLAN-RESULT.md` (all past workspaces) | Decisions already made in this or related projects. Prevents rediscovering the same alternative. If a past megaplan decided against an approach, note it and don't regenerate it unless the context has changed. |
| `context/a signal scanner/YYYY-MM-DD-suggestions.json` (latest) | Recent signals from scans that might contradict or support the plan. If a scan flagged the domain, surface the signal in Layer 1. |
| `context/brand/positioning.md`, `context/brand/icp.md` | Strategic positioning and customer context. For product/commerce projects only — shape non-functional requirements. |
| Project `progress.md` + `history.md` (if exist) | Recent session context — what was tried and what failed. Avoid re-proposing recently-failed approaches. |

**Context-read protocol:**
1. Read each source above that exists. If a source is load-bearing but missing, log it as a gap in `megaplan-progress.md` — do NOT fail (adapt: neutral defaults).
2. Build a Context Summary at the top of Layer 1 output listing: which sources were read, which were missing (and what default was used), and which your backlog file items or past MEGAPLAN-RESULT files are load-bearing for this plan.
3. FAIL condition: Layer 1 output does not acknowledge a your backlog file item that matches the project scope keyword-wise. Do a quick grep of your backlog file for the project name / keywords before marking Layer 1 complete.

If critical context is missing (no brief AND no codebase AND no CLAUDE.md), STOP and ask. Do not plan in the dark.

---

### Layer 1 -- Deep Absorption

**Goal:** Build a complete mental model of the problem space before proposing any solutions.

**Process:**
1. Read every input source listed above. Do not skim -- read fully.
2. Extract and organize:
   - **Entities:** What are the nouns in this system? Users, accounts, pipelines, reports, events...
   - **Data flows:** How does data enter, transform, and exit? What are the critical paths?
   - **Failure points:** Where can things go wrong? Network, disk, auth, concurrency, data consistency...
   - **Dependencies:** External services, libraries, APIs, infrastructure, human processes
   - **User journeys:** End-to-end flows from user intent to system response
   - **Constraints:** Performance budgets, compliance, existing contracts, team skill, timeline, cost
   - **Non-functional requirements:** Latency, throughput, availability, security, observability, maintainability
3. Identify the 3-5 hardest architectural decisions this system faces. These become the focus of Layer 2.
4. Identify unknowns and assumptions. Flag each clearly.

**Output:** Create `megaplan-progress.md` using the template at `references/template-progress.md` (layer-status checklist, mental-model summary, entities, data flows, failure points, hard decisions, assumptions, unknowns).

**Write this file to disk before proceeding.** This is your crash recovery checkpoint.

---

### Layer 2 -- Alternative Exploration (Parallel Divergent Generation)

**Goal:** Generate 3 (or 4 on heavy path) genuinely different architectural approaches — not variations of the same idea.

**The Divergence Problem.** Naive sequential generation with one reasoning thread produces variations (A, A', A'') more often than genuine divergence (A, B, C). MEGAPLAN solves this by forcing each alternative to optimize a DIFFERENT top-level objective, generating them in parallel mentally, then checking a divergence matrix.

**Mandatory pre-generation step — assign distinct optimization targets.**

Before writing any alternative, pick targets from this menu (at least one per alternative; no target repeats across alts):

| Target | Philosophy |
|---|---|
| `velocity-first` | Ship the leanest thing that works. Refactor later. |
| `cost-first` | Minimize infra and ongoing operational cost. |
| `reversibility-first` | Make every piece swappable. No lock-in. |
| `compliance-first` | GDPR/PII/audit requirements drive the shape. |
| `correctness-first` | Formal state machines, strong consistency, type-safe everywhere. |
| `scale-first` | Design for 100x from day 1. |
| `vendor-leverage-first` | Lean into one platform's managed services (Cloudflare/AWS/GCP/Supabase). |
| `portability-first` | Runs anywhere — self-host, public cloud, air-gapped. |
| `observability-first` | Every event traceable, every mutation auditable. |
| `simplicity-first` | Fewest moving parts even at the cost of flexibility. |
| `brownfield-minimal-diff` | Minimize changes to existing code — additive only. |
| `greenfield-clean-slate` | Use the "nothing to preserve" freedom to pick ideal shape. |

**Selection rule.**
- Standard path (3 alternatives) — pick 3 targets relevant to the project. At least one must be the "obvious" target you would pick; the other two must be deliberately contrasting.
- Heavy path (4 alternatives) — pick 3 targets + 1 "black swan" target chosen using Inversion (pick the target that seems least applicable; the alt that wins against it often has hidden merit).

**Generation mental model.** Generate all alternatives' one-line philosophy + component inventory first (in parallel, treating each as if a separate agent owned it), THEN fill in the 10 detail fields for each. This prevents the first alt from anchoring the others.

**Rules (with FAIL conditions):**
- Each alternative must make a fundamentally different trade-off on at least one of the hard decisions from Layer 1.
- FAIL: two alternatives share the same optimization target.
- FAIL: two alternatives share >80% of their component inventory (they're variations, not alts).
- No strawmen. Every alt must be defensible — a real architect could argue for any of them. Record the "strongest case" sentence for each.
- If 3 genuinely different approaches don't emerge after divergence-matrix check, the problem is simpler than it appears. Log the attempt in `megaplan-alternatives.md` as "attempted divergence targets [X, Y, Z] — converged to [A]; dropping back to simplified single-path mode per gate." Then proceed to Layer 3 with the single alt.

**Divergence self-check (end of Layer 2 before writing file):**

Build this matrix internally:

| | Alt A | Alt B | Alt C |
|---|---|---|---|
| Optimization target | `velocity-first` | `correctness-first` | `cost-first` |
| Hard Decision 1 answer | X | Y | X |
| Hard Decision 2 answer | X | X | Y |
| Hard Decision 3 answer | X | Y | Z |
| Primary data store | Postgres | Postgres | SQLite |
| Sync/async split | sync-heavy | sync-heavy | async-heavy |

Row-by-row, count distinct answers. If any row has only 1 distinct answer across all alts, AND that row is a load-bearing decision, generation is not divergent enough → rework.

**For EACH alternative, produce the 11 detail fields** (name + philosophy, ASCII data-flow diagram, component inventory, failure-mode analysis, scale implications, migration path, cost model, implementation effort, risk assessment, recommendation score, and the implementation-simulation with a 1-10 friction score). The selected alt should have LOW friction (≤4) AND high recommendation (≥7); if these conflict, document and let the user decide.

**Output:** Create `megaplan-alternatives.md` using the template at `references/template-alternatives.md` — it holds the full 11-field spec and the comparison-matrix structure. Document all alternatives (3 standard / 4 heavy) plus the comparison matrix and a 2-3 sentence recommendation. Headings must produce clean kebab-case anchors (no emoji/punctuation) because your backlog file and downstream agents cite by anchor.

**Update `megaplan-progress.md`** to mark Layer 2 complete.

**CHECKPOINT G2 — Alternative Selection (headless-safe).**

Present the comparison matrix + recommendation. Behavior depends on run mode:

| Mode | Behavior at G2 |
|---|---|
| `interactive` (default; human is present) | Ask: "I recommend Alternative [X]. Proceed / switch to [Y or Z] / discuss?" Wait for reply. |
| `headless` (no human, e.g. an overnight pipeline `--megaplan` run) | Auto-select the recommended alternative. Log to `megaplan-progress.md`: `G2 auto-selected Alt [X] at [timestamp]. No human reply configured.` |
| `hybrid` | If recommendation score gap between top-2 alts is ≥2 points: auto-select. If gap <2: pause and ask (genuine coin-flip). |

**Multi-gate model.** MEGAPLAN inserts additional gates throughout the run, each with the same headless-safe behavior:

| Gate | When | Auto-default in headless |
|---|---|---|
| G1 — complexity path confirmation | After complexity gate scoring | Use the scored path; no pause needed |
| G2 — alternative selection | After Layer 2 comparison matrix | Select highest-recommendation-score alt |
| G3 — Layer 3 section applicability | Light path only, after applicability classification | Use applicability table defaults |
| G4 — validation issue triage | After Layer 4 finds issues | CRITICAL: auto-fix in architecture.md and re-validate. HIGH: auto-fix if fix is mechanical (e.g., add missing auth row), otherwise flag OPEN. MEDIUM/LOW: flag OPEN, continue. |
| G5 — rejected-alt parking | After Layer 2 if rejected alts have defensibility | Auto-append to your backlog file with inferred gate conditions |

For interactive mode, each gate is a chance for the operator to steer. For headless, each gate has a documented default. FAIL condition: a gate fires in headless mode with no documented default — protocol violation, log and continue with conservative choice.

---

### Layer 3 -- Deep Dive Best Option

**Goal:** Produce architecture documentation detailed enough that a Sonnet-class worker agent can implement every component without asking a single clarifying question.

**This is the core of MEGAPLAN.** Do not rush this layer. Every ambiguity left here becomes a bug or a blocked worker later.

#### Sub-section checkpointing

Write `megaplan-architecture.md` incrementally — one sub-section at a time. After each sub-section:
1. Append that sub-section to `megaplan-architecture.md` (not buffered in memory).
2. Update `megaplan-progress.md` with: `- [x] 3.1 API Specification` etc.
3. Append a 1-line note to the Layer 3 progress trail in `megaplan-progress.md`: `[ISO timestamp] Sub-section 3.X completed, [N] bytes written.`

FAIL condition (durability): more than one sub-section's worth of content held in memory without writing to disk. A crash between sub-sections should lose ≤1 sub-section of work.

#### Section applicability (light-path only)

On **light path** (complexity score 0-2), mark applicability before generating. Only sections with any APPLICABLE row produce output:

| Sub-section | Applicability test | Default on light path |
|---|---|---|
| 3.1 API Specification | ≥1 HTTP endpoint | APPLICABLE if any |
| 3.2 Database Schema | ≥1 data store | APPLICABLE if any |
| 3.3 State Machines | ≥1 entity with multi-state lifecycle | SKIP unless flagged |
| 3.4 Integration Points | ≥1 external service | APPLICABLE if any |
| 3.5 Error Handling Strategy | always | APPLICABLE |
| 3.6 Event Architecture | async/queue/pub-sub present | SKIP unless flagged |
| 3.7 Security Model | auth required OR PII present | APPLICABLE if any |
| 3.8 Observability | production deploy OR SLOs | light: 1-paragraph minimum; heavy: full |
| 3.9 Directory Structure | always | APPLICABLE |

For each skipped sub-section, write: `### 3.X [Name] — NOT APPLICABLE (light path; trigger would be: [X])`. Don't silently drop.

On **standard or heavy path**, all sub-sections are mandatory unless test truly shows zero applicable items.

#### Minimum-detail gates per sub-section

Each sub-section must clear a minimum-detail threshold before being marked complete:

| Sub-section | Minimum detail gate |
|---|---|
| 3.1 API | Every endpoint has method + path + auth + 1 success + ≥2 error responses + 1 side-effect line |
| 3.2 DB | Every table has ≥3 columns with types + PK + ≥1 index + estimated row count |
| 3.3 State | Every state machine has ≥2 states + ≥1 transition with guard + initial + terminal |
| 3.4 Integration | Every integration has protocol + auth + ≥1 operation row with timeout + retry |
| 3.5 Error handling | Retry policy count ≥ number of distinct transient error classes; fallback defined for every external call |
| 3.6 Event | Every event has producer + ≥1 consumer + schema + ordering + delivery + idempotency key |
| 3.7 Security | Auth flow numbered steps ≥3 + authz model named + encryption at rest & in transit explicit |
| 3.8 Observability | ≥3 metrics + ≥1 dashboard pointer + ≥1 alert rule + structured-log format |
| 3.9 Directory | Every top-level folder annotated with 1-sentence purpose |

FAIL condition: sub-section written but gate not met. Do not mark complete. Expand until gate passes.

**Produce sub-sections 3.1 through 3.9** (subject to the light-path applicability table above):

- **3.1 API Specification** — every endpoint: method, path, auth, rate limit, request/response schemas, error table, side effects, idempotency
- **3.2 Database Schema** — every table: purpose, row counts, columns/types/constraints, indexes, migrations, relationships
- **3.3 State Machines** — every entity with lifecycle: states, initial/terminal, transition table with guards + side effects
- **3.4 Integration Points** — every external system: protocol, auth, operations table (timeout/retry/circuit breaker), error handling, data mapping
- **3.5 Error Handling Strategy** — classification, retry policies, circuit breakers, fallbacks, reporting, user-facing messages
- **3.6 Event Architecture** (if applicable) — every event: producer, consumers, schema, ordering, delivery, idempotency key, DLQ policy
- **3.7 Security Model** — auth flow, authz model, encryption (rest + transit), secrets, input validation, CORS, rate limiting
- **3.8 Observability** — logging format, metrics/SLIs/SLOs, tracing, alerting
- **3.9 Directory Structure** — full tree with a 1-sentence purpose annotation per top-level folder

The full per-section markdown templates are in `references/template-architecture.md`. Use them while writing each sub-section; each must clear its minimum-detail gate above before being marked complete.

**Output:** Create `megaplan-architecture.md` with all applicable sections above.

**Update `megaplan-progress.md`** to mark Layer 3 complete.

---

### Layer 4 -- Validation and Handoff

**Goal:** Cross-reference everything to catch gaps, contradictions, and missing pieces before any code is written.

**Validation checklist:**

1. **Frontend-Backend contract check:**
   - Every UI page/component has a data source mapped to an API endpoint
   - Every form submission has a corresponding POST/PUT/PATCH endpoint
   - Every loading state has error and empty states defined
   - WebSocket/SSE subscriptions (if any) have reconnection logic specified

2. **API-Database consistency:**
   - Every API endpoint that reads data has a corresponding query pattern with an index to support it
   - Every API endpoint that writes data has the target table and constraint behavior documented
   - No endpoint returns data that requires a table that does not exist in the schema

3. **Auth consistency:**
   - Every endpoint has an auth requirement specified
   - Auth middleware is documented with exact behavior for each endpoint type
   - Token refresh, session expiry, and revocation flows are complete

4. **Error path completeness:**
   - Every API endpoint has error responses for all plausible failure modes
   - External integration failures have fallback behavior defined
   - Database constraint violations (unique, FK, check) map to user-facing error messages

5. **Migration executability:**
   - Migration steps are ordered and each step is independently deployable
   - Rollback is defined for each migration step
   - No step requires downtime unless explicitly called out

6. **Event flow completeness:**
   - Every emitted event has at least one consumer
   - Every consumer has idempotency handling
   - Dead letter handling is defined for every queue

7. **Dependency resolution:**
   - All external dependencies (libraries, services, APIs) are listed with versions
   - No circular dependencies between services/modules
   - Build order is clear

8. **Scale sanity:**
   - Hot paths identified and optimization notes attached
   - No unbounded queries (pagination on all list endpoints)
   - Cache invalidation strategy documented for every cached resource

**Output:** Create `megaplan-validation.md` using the template at `references/template-validation.md` (validation summary, per-issue blocks with CRITICAL/HIGH/MEDIUM/LOW severity + status, cross-reference matrix, and the 7-quality architecture-fitness scorecard).

If CRITICAL issues are found, go back and fix them in `megaplan-architecture.md` before proceeding. Update the validation report to show them as RESOLVED.

**Update `megaplan-progress.md`** to mark Layer 4 complete.

---

### Summary Document — The Only Doc The Operator Is Guaranteed To Read

`MEGAPLAN-RESULT.md` is opened 100% of the time; the other four docs are opened on demand (alternatives by anchor from downstream agents, architecture/validation by builders, progress only on crash recovery).

**Design rule:** MEGAPLAN-RESULT.md must be complete enough that you can (a) make a build-or-defer decision in <5 minutes of reading, (b) quote decision rationale in your backlog file without re-opening other docs, (c) hand off to a builder agent with one file reference.

**Output:** Create `MEGAPLAN-RESULT.md` using the template at `references/template-result.md`. Mandatory sections in this order: machine-readable HTML-comment header → TL;DR → Decision → Builder Handoff (with Phase-1 first task + definition of done) → Trade-offs Accepted/Avoided → Implementation Order → Risk Register → Dependencies → Post-Launch Gates (if applicable) → Files Produced → How To Cite. The template also restates the kebab-case anchor rule and the citation conventions.

**Anchor rule (load-bearing).** Every heading inside `megaplan-alternatives.md` and `megaplan-architecture.md` must render a kebab-case anchor matching the header text (`## Alternative A: Threshold Compactor` → `#alternative-a-threshold-compactor`). Downstream agents depend on these anchors. No emoji or anchor-breaking punctuation in those headings.

**Update `megaplan-progress.md`** to mark all layers complete.

---

## Dry-Run Mode

Invoke with `megaplan --dry-run` or when the user says "dry-run megaplan". Produces only:
1. Complexity gate scoring output (score, path, factors)
2. Context read summary (which files existed/missing)
3. Estimated runtime bracket
4. List of hard decisions that would be explored in Layer 2
5. List of optimization targets that would be picked for alternatives
6. The file paths that would be written (not their content)

**No layer documents are written in dry-run.** Useful for:
- Sanity-checking the scope before committing 15-50 min of Opus time
- Pre-flighting a build-pipeline `--megaplan` run before scheduling it
- Verifying that context inputs are complete before plane takes off

FAIL condition: dry-run writes any content file beyond a single `megaplan-dryrun-report.md` in the output directory.

---

## Crash Recovery

MEGAPLAN writes partial results to disk after each layer. If the session crashes or context fills:

1. Check for `megaplan-progress.md` in the output directory
2. Read the layer status to determine where execution stopped
3. Read the completed layer outputs to rebuild context
4. Resume from the next incomplete layer

This is why each layer writes to disk before proceeding. The documents ARE the crash recovery mechanism.

If resuming after a crash:
- Announce: "Resuming MEGAPLAN from Layer [N]. Previous layers loaded from disk."
- Re-read all completed layer outputs before continuing
- Do not re-run completed layers unless the user explicitly asks

## Integration with a Build Pipeline

When invoked as a build-pipeline architecture-phase replacement (via `--megaplan` flag): read all `01-discovery/` outputs, run all 4 layers, then produce the standard architecture files **by observed consumer demand** (not all 10 unconditionally) plus the MEGAPLAN-specific outputs in `02-architecture/`, and write a `phase2-manifest.json` so the downstream build orchestrator can skip absent files.

When run as a build-pipeline architecture phase, produce the standard architecture files by observed consumer demand plus the MEGAPLAN outputs in `02-architecture/`, and write a `phase2-manifest.json` for the downstream build orchestrator.

## Integration with Agentic OS

MEGAPLAN is a full participant in your shared context layer. Read inputs at start (see Input Requirements above). At the end, write three outputs using the exact formats in `references/agentic-os-writeback.md`:

1. **Append to your lessons log** — architecture decision, trade-offs, top-3 risks, principles discovered ([KEEP]-tagged if they generalize), what worked/didn't this session.
2. **Park rejected alternatives → your backlog file** — if Layer 2 produced 3-4 alts and only one was selected, append each rejected-but-defensible alt as a GATED entry citing `megaplan-alternatives.md#alternative-X` with trigger conditions.
3. **Optionally append a `megaplan-completed` entry to your own project-tracking file** (if you keep one) so your dashboard surfaces the newly-planned project.

**FAIL conditions:**
- Heavy-path or standard-path megaplan with rejected alternatives, but nothing appended to your backlog file → fail. Rejected alts with any defensibility must be parked.
- your lessons log not updated within this session → fail.

## Model Routing (Tiered, informed by 2026 SOTA planning workflows)

The Aider architect/editor split and Cline plan/act separation both show that pairing a heavy reasoner with a cheap codifier produces SOTA results on planning benchmarks. MEGAPLAN adopts a tiered routing policy while preserving "Opus does the hard thinking."

| Layer / Task | Recommended Tier | Rationale |
|---|---|---|
| Layer 1 — Deep Absorption | Opus | Context synthesis is core reasoning. |
| Layer 2 — Alternative Exploration | Opus | Divergence cannot be cheap — this is why MEGAPLAN exists. |
| Layer 3 — Deep Dive (hard sections: API spec, state machines, event arch, security) | Opus | Specification is load-bearing for workers. |
| Layer 3 — Deep Dive (mechanical sections: directory tree, observability boilerplate, env vars) | Sonnet acceptable | Repetitive, pattern-based. |
| Layer 4 — Validation | Opus | Cross-referencing needs full-context reasoning. |
| MEGAPLAN-RESULT.md summary synthesis | Opus | Final decision synthesis. |
| Architecture-phase output derivation (extracting sub-files from architecture.md) | Sonnet | Extraction, not reasoning. |

**Non-Opus invocation.** If the current model is Sonnet-class or smaller, announce: `Model [X] detected. MEGAPLAN recommends Opus for Layers 1, 2, 4 and the hard-section half of Layer 3. Proceeding may produce weaker alternative divergence and shallower spec depth. Continue anyway? [Y/N in controlled mode, autoYES with warning logged in headless mode]`.

**Cheap exploration tier (light path only).** For light-path projects (score 0-2), Sonnet can run the entire flow. Announce: `Light path on Sonnet — this is acceptable because alternative exploration is disabled and spec depth required is lower.`

## Planner / Architect / Builder Separation (Cline + Aider inspired)

MEGAPLAN explicitly enforces a three-role contract:

1. **Planner (this skill)** — read-only during Layer 1-4. Produces docs, never touches source. Mirrors Cline's Plan mode.
2. **Architect handoff (MEGAPLAN-RESULT.md Builder Handoff section)** — is the "edit instructions" the architect passes to the builder. Mirrors Aider architect→editor split.
3. **Builder (a separate session or your build phase)** — reads MEGAPLAN-RESULT.md + the specific architecture anchors, produces code.

**Enforcement:**
- During MEGAPLAN execution, the skill MUST NOT create or modify source files outside `megaplan/` (or `02-architecture/` in build-pipeline mode). FAIL condition: any Write or Edit to files under `src/`, `app/`, `backend/`, etc.
- The Builder Handoff section must be complete enough that the builder session does NOT need to open `megaplan-alternatives.md` or `megaplan-progress.md` — only architecture.md.

## Constraints (Testable)

Every constraint below has a FAIL condition. If a FAIL condition is detected during self-check at end of each layer, the layer is incomplete — repeat it until no FAILs remain.

1. **Divergence requirement (Layer 2).** Each alternative must differ from every other alternative on at least one hard decision from Layer 1.
   - FAIL: two alternatives share the same answer on every hard decision.
   - FAIL: alternative names differ only in degree ("async A", "async A with retries", "async A with caching") — this is variation, not divergence.
   - Self-check: enumerate the hard decisions, plot alternatives × decisions as a matrix. Every row must have ≥2 distinct values.

2. **No-handwave rule (Layer 3).** No section may contain the string pattern "handle X appropriately", "proper error handling", "standard best practice", "as needed", "if applicable" (unless immediately followed by an enumerated list), "TBD", "TODO" (unless tagged `[BY-WORKER]`).
   - FAIL: grep of the section returns any of the above patterns without enumeration.
   - Pass condition: every error, retry, timeout, auth rule has an explicit value or a citation to another spec section.

3. **Context floor.** If project brief AND existing codebase summary are both missing, STOP.
   - FAIL: Layer 1 output contains >3 entries in Unknowns section that are load-bearing (would change the recommendation).
   - On FAIL, pause and emit: "Context insufficient. Need: [specific list]. Options: (a) answer these, (b) proceed with stated assumptions flagged."

4. **MEGAPLAN does NOT write code.** FAIL: any new non-megaplan file is created outside `megaplan/` or the pipeline's `02-architecture/`. Exception: appendix code stubs inside the architecture doc's fenced blocks are fine — they are documentation, not source.

5. **Durability.** Write partial results to disk AT sub-section granularity, not layer granularity. See Layer 3 checkpointing section.
   - FAIL: if current layer ran >5 minutes of wall clock without a disk write, crash recovery is compromised. Emit warning.

6. **Complexity gate compliance.** Mode from gate must match actual execution. FAIL: gate scored 1/10 but a full 4-alternative Layer 2 was produced.

7. **Time budget transparency.** Announce expected runtime based on path:
   - Light: 8-12 min
   - Standard: 18-28 min
   - Heavy: 35-50 min
   - FAIL to announce = protocol violation. Log it.

8. **Library fidelity.** When specifying integrations or library features, the skill MUST either (a) cite a Context7 doc version/section, (b) cite an official doc URL, or (c) tag `[VERIFY: <what to verify>]`.
   - FAIL: any integration section with a method name or API shape but no citation and no `[VERIFY]` tag.
   - `[VERIFY]` tags are legitimate when Context7 unreachable; they become worker tasks.
