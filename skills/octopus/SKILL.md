---
name: octopus
description: >
  An overnight autonomous-operations orchestrator. You define a set of independent "arms"
  (self-contained tasks), and the system dispatches them in parallel across a few phases,
  then hands you one visual morning report. Run it, walk away, read the summary. Trigger when
  you want a repeatable nightly batch that evolves your projects, audits, gathers data, and
  drafts work while you sleep — without babysitting it.
---

# Octopus — Autonomous Nightly Operations

> Point it at your projects, define the arms, let it run overnight. Read the report over coffee.

Octopus is a **pattern for unattended parallel operations**: a small orchestrator that fans a
batch of independent tasks ("arms") out across a few ordered phases, runs them concurrently,
collects the results, and prints a single morning briefing. It turns "things I keep meaning to
do" into "things that happen every night."

This is a **template you configure**, not a fixed program. The value is the architecture —
phases, parallel arms, a durable ledger, and a report — which you fill with the arms that matter
for *your* projects.

## The architecture

```
PHASE 1 — SENSE      (read state, gather signals)      arms run in parallel
PHASE 2 — ACT        (evolve, build, draft, audit)     arms run in parallel
PHASE 3 — GROW       (data, benchmarks, research)      arms run in parallel
PHASE 4 — REPORT     (reconcile ledgers, build report) single arm
```

Each **arm** is a self-contained task with a clear goal, its own inputs, and a written result.
Arms in the same phase have no dependencies on each other, so they run concurrently (via parallel
agent dispatch). Later phases can read what earlier phases wrote.

## Configuring your arms (examples — pick what fits your projects)

| Arm type | What it does overnight |
|---|---|
| Product evolution | Run an improvement pass on one project; write a change proposal for you to review |
| Security/quality audit | Scan a codebase or product for defects, write a prioritized findings list |
| Data growth | Pull fresh signals (market, competitor, keyword) into a local knowledge store |
| Content drafting | Draft the next posts/emails from your existing material for morning review |
| Outreach prep | Assemble a shortlist + first-draft messages for you to send by hand |
| Benchmarking | Re-run your metrics/tests and flag regressions vs the last accepted run |
| Housekeeping | Reconcile your notes/queues so nothing rots (a task ledger, a backlog file) |
| Reporting | Compose the visual morning briefing from every arm's result |

Keep each arm's prompt in the same shape: **Task / Done-when / Constraints / Context.** Give every
arm a measurable "done when," and tell each one to write its result to a file the report arm reads.

## How to run

1. Define your arms in a config (one entry per arm: phase, goal, inputs, output file).
2. Kick off the run — the orchestrator dispatches phase by phase.
3. In the morning, open the generated report (an HTML dashboard: what changed, what was found,
   what's queued for your decision).
4. Act on the decisions it surfaces — the system proposes; you approve.

## Dependencies

- Parallel agent dispatch (an "agent teams"-style runner) — arms are subagents run concurrently.
- A durable ledger file per run (signals / proposals / actions) so results survive the session.
- A report renderer (any HTML + chart approach) for the morning briefing.
- Nothing cloud-specific: it runs wherever your agent runner runs.

## Use cases

- **BAU:** a standing nightly batch — evolve one project, audit another, refresh data, draft content.
- **Special:** a one-off "big sweep" before a launch (audit everything, benchmark everything, draft
  the launch kit) by loading a heavier arm set for a single run.

## Guardrails

- **Arms are READ-ONLY on shared state unless explicitly told otherwise** — an arm that mutates
  shared files can clobber a parallel arm. Give writers their own output files.
- **The orchestrator proposes; you dispose.** Nightly runs should produce *drafts and proposals*,
  not irreversible actions. Keep anything destructive or outbound behind your morning approval.
- **Cap concurrency** to what your machine/runner can handle; queue the rest.
- **Verify before trusting** — an arm's self-report is a claim; the report arm (or you) should
  confirm against the actual artifacts before acting.
