---
name: polish-orchestrator
description: "THE POLISHER orchestrator on the Workflow tool — intelligent quality gate that explores any codebase, builds a risk-weighted dossier, then dispatches parallel specialist auditors (15 modes across 3 waves) that audit and auto-fix, and synthesizes a health-scored report. Deterministic DAG, durable cross-session resume, dispatch-layer write-scoping. Activates on /polish, /polish-all, /polish-status, /polish-report. Heavy and side-effecting; writes only the target project's polish/ tree + source auto-fixes, commits locally, never pushes."
disable-model-invocation: true
user-invocable: true
triggers:
  - "/polish"
  - "/polish-all"
  - "/polish-status"
  - "/polish-report"
---

# Polish Orchestrator v2 — Parallel Quality Gate (Workflow tool)

THE POLISHER: a Senior QA Architect that walks into a codebase cold, rapidly understands what someone tried to build, then deploys specialist reviewers with surgical precision and synthesizes one health-scored verdict. v2 runs the wave DAG on the **Workflow tool** (deterministic control flow, intermediate state held out of context, resumable, ≤16 concurrent). Mode methodologies are the source of truth in `polish-worker/SKILL.md` (16 sections); this skill defines orchestration only.

## How to run

Invoke the Workflow tool with this skill's orchestration script:

```
Workflow({
  scriptPath: "${CLAUDE_SKILL_DIR}/workflows/polish.workflow.mjs",
  input: { root: "<your-projects-root, or . >", project: "<dir-or-.>", lean: false, skipStaleness: false, head: "<git HEAD>", lock: "polish-v2" }
})
```

Pipeline: **explore → (wave0 ∥ wave1) → wave2 → wave3 → synthesis**. Each phase gates on the prior phase's outputs. The script writes a durable checkpoint (`<project>/polish-progress.md`) after every phase, so a cold start (new session / `/compact` / reboot) resumes only the **pending** modes — Workflow-native resume handles in-session pause; the checkpoint handles cross-session.

- `lean: true` → every specialist runs on sonnet (orchestrator stays opus); `security` stays opus regardless.
- `skipStaleness: true` → drops Wave 0; also auto-skipped when Context7 is unavailable, there are no external deps, or a valid <7-day cache matches the current HEAD.

## Waves & modes (15)

| Wave | Phase | Modes | Model |
|---|---|---|---|
| 0 | Phase1 (∥ wave1) | `staleness` | sonnet |
| 1 | Phase1 | `errors` `deps` `perf` `docs` `api-test` `compliance` / **`security`** | sonnet / **opus** |
| 2 | Phase2 | `ux` `design` `journeys` `arch` `foundation` | opus |
| 3 | Phase3 | `market` `value` `copy` | opus |

Wave 0 runs **concurrently with** Wave 1 and feeds **only** the Wave-2 `arch` worker (`polish/staleness-report.md`). Phase 0 prep and Phase-4 synthesis run via bundled scripts (`scripts/polish_state.mjs`, `scripts/synthesize.mjs`) inside their phase agents (the control script has no fs).

## Invariants (enforced, not just stated)

- **Write-scoping (MUST-PRESERVE — hard-learned path-scoping):** each specialist may write ONLY its own `polish/<mode>-report.{md,json}` + project source (for auto-fix). `market`/`value` are recommendations-only (no source write). No worker may write another mode's report, `polish-progress.md` / `polish-report.md` / `polish-log.md` / `cso-exclusions.json`, or any sibling build-orchestrator/engine state. Enforced by `hooks/deny-write-out-of-scope.json` (PreToolUse → `scripts/scope_guard.mjs`, exit 2 blocks), backstopped by `isolation: worktree` on every fixer, and restated in each agent prompt.
- **Never push / never auto-send:** `hooks/deny-push-send.json` (PreToolUse deny on `git push`, `gh pr/issue create`, `git send-email`). The Polisher commits locally only; you review and push.
- **Durable cross-session resume:** `polish-progress.md` (schema `polish-progress/v2`) is written after every phase; the lock field follows the orchestrator lock protocol; sibling-engine state files are never modified.
- **Staleness via Context7 `get-library-docs`** (the obsolete `query-docs` defect is fixed): `resolve-library-id` → `get-library-docs` (topic "breaking changes, migration guide, deprecated APIs", ~30K cap). Missing Context7 emits `[STALENESS_SKIPPED: Context7 MCP not available]` without failing the run.
- **security is always opus + maximum rigor** regardless of project state, and `--lean` does not lower its rigor expectations.
- **No transcript scraping:** synthesis consumes structured `PolishWorkerReport.status`, not `STATUS: COMPLETE` text.

## Notes
- **Models are tier aliases** (`'opus'` | `'sonnet'` | `'haiku'` in `agent()` calls) resolved live by the harness — never pinned dated IDs. Current lineup (2026-07-10): Opus 4.8 (judgment/security), Sonnet 5 (mechanical modes), Haiku 4.5 (thin checkpoint relays).
- No API keys in scripts — keep secrets in your own config, never in the skill. Asset paths resolve under `${CLAUDE_SKILL_DIR}` (fallback: the script's own dir). No hardcoded project root — `root`/`project` are inputs.
- Wire `hooks/*.json` into your project's `.claude/settings.json` and point the scope-guard hook command at this skill's `scripts/scope_guard.mjs` (absolute path — settings files do not resolve skill variables). The scope-guard needs `POLISH_MODE` set per dispatch (the workflow's agent prompts carry the mode).
