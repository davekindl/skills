#!/usr/bin/env node
// polish-orchestrator v2 — write-scope guard (hard-learned path-scoping).
// MUST-PRESERVE invariant (spec §3.1, polish-worker SKILL.md L199-202): a specialist
// worker's write access is GUARANTEED at the dispatch layer, not honor-system prose.
// This is the structural enforcement: a PreToolUse hook on Write/Edit/NotebookEdit pipes
// the tool-call JSON to this script on stdin; exit 2 BLOCKS the write, exit 0 allows it.
//
// Scope rules (per mode), derived from polish-worker SKILL.md L201-202 + spec §3.1:
//   - A worker may write ONLY: its own polish/<mode>-report.md (+ .json companion) AND
//     project source files (for auto-fix).
//   - market / value are RECOMMENDATIONS-ONLY (polish-worker L148, L154): NO source write,
//     only their own report.
//   - NO worker may write: another mode's polish/*-report.*, polish-progress.md,
//     polish-report.md, polish-log.md, cso-exclusions.json, or any sibling build-orchestrator state file
//     (e.g. an orchestrator progress file, engine state dirs, *-checkpoint.json).
//   - Drive Discipline (root CLAUDE.md): NEVER write the C: drive.
//
// The active worker is identified by the POLISH_MODE env var injected at dispatch
// (the orchestrator sets it per agent). If unset, the guard is permissive about
// report-ownership (can't know whose write it is) but STILL enforces the global denies
// (other-worker reports it can't attribute are allowed; orchestrator/sibling-engine state are not).
//
// Forward slashes only. No hardcoded project root. Testable via --selftest.
//
// Usage (hook): node scope_guard.mjs            # reads PreToolUse JSON on stdin
//   env: POLISH_MODE=security  (the dispatching mode)
// Usage (test): node scope_guard.mjs --selftest

import fs from 'node:fs'
import os from 'node:os'

const ALL_MODES = ['errors', 'deps', 'security', 'perf', 'docs', 'api-test', 'compliance', 'ux', 'design', 'journeys', 'arch', 'foundation', 'market', 'value', 'copy', 'staleness']
const RECO_ONLY = new Set(['market', 'value']) // no source write (polish-worker L148, L154)

// Orchestrator-owned / shared state files no worker may write (spec §3.1).
const ORCH_OWNED = [
  /(^|\/)polish-progress\.md$/i,
  /(^|\/)polish-report\.md$/i,
  /(^|\/)polish-log\.md$/i,
  /(^|\/)polish[/\\]cso-exclusions\.json$/i,
]
// Sibling build-orchestrator / engine state no worker may touch (spec §3.1).
const ENGINE_OWNED = [
  /(^|\/)orchestrator-progress\.md$/i,
  /(^|\/)engine[/\\]state[/\\]/i,
  /(^|\/)\.engine[/\\]/i,
  /(^|\/)OCTOPUS-LOG\.md$/i,
  /(^|\/)octopus[/\\]state[/\\]/i,
  /[/\\][a-z0-9-]*-checkpoint\.json$/i,
]
// C: drive (Drive Discipline).
const C_DRIVE = [/^[cC]:[\\/]/, /^\/c\//i, /^\/mnt\/c\//i]

function norm(p) { return String(p || '').split('\\').join('/') }

// Is this path a polish/<mode>-report.{md,json} and if so for which mode?
function reportMode(p) {
  const m = norm(p).match(/(?:^|\/)polish\/([a-z0-9-]+)-report\.(?:md|json)$/i)
  return m ? m[1].toLowerCase() : null
}

// Decide allow/deny for a write to `filePath` by worker `mode`.
// Returns { allow:boolean, reason:string }.
function decide(filePath, mode) {
  const p = norm(filePath)

  // 1. C: drive — always denied, EXCEPT the two harness-managed locations the Claude Code
  // platform itself writes to (persistent auto-memory + session scratchpad). Added
  // 2026-07-10 when this guard was wired globally; mirrors deny_push_and_c_write.cjs.
  if (C_DRIVE.some((re) => re.test(p))) {
    const harnessManaged =
      /^(?:[cC]:|\/+(?:mnt\/+)?c)\/+Users\/+[^/]+\/+\.claude\/+projects\//i.test(p) ||
      /^(?:[cC]:|\/+(?:mnt\/+)?c)\/+Users\/+[^/]+\/+AppData\/+Local\/+Temp\/+claude\//i.test(p)
    if (!harnessManaged) return { allow: false, reason: 'C: drive write forbidden (Drive Discipline) — D: is canonical' }
  }

  // 2. Sibling build-orchestrator / engine state — always denied.
  if (ENGINE_OWNED.some((re) => re.test(p))) return { allow: false, reason: 'sibling build-orchestrator/engine state file is off-limits to polish workers (spec §3.1)' }

  // 3. Orchestrator-owned shared state — always denied (workers never write these).
  if (ORCH_OWNED.some((re) => re.test(p))) return { allow: false, reason: 'orchestrator-owned state (polish-progress/report/log/cso-exclusions) — workers may not write it (spec §3.1)' }

  // 4. A polish/<x>-report.* path: allowed ONLY if x === this worker's own mode.
  const rm = reportMode(p)
  if (rm) {
    if (mode && rm === mode) return { allow: true, reason: `own report (${mode})` }
    if (mode && rm !== mode) return { allow: false, reason: `cross-worker write: ${mode} may not write ${rm}'s report (path-scoping)` }
    // mode unknown: can't attribute — but a *-report write to a known mode that isn't us is still
    // suspicious; without POLISH_MODE we cannot prove violation, so allow (fail-open only for unattributable).
    return { allow: true, reason: 'report write, POLISH_MODE unset (unattributable — allowed)' }
  }

  // 5. Any other path = project source. Allowed for fixer modes; DENIED for recommendation-only modes.
  if (mode && RECO_ONLY.has(mode)) return { allow: false, reason: `${mode} is recommendations-only — no source writes (polish-worker L148/L154)` }
  return { allow: true, reason: 'project source write (auto-fix) allowed' }
}

function extractPath(input) {
  // PreToolUse payload shape: { tool_name, tool_input: { file_path, ... } }
  const ti = input && input.tool_input
  if (!ti) return null
  return ti.file_path || ti.path || (ti.edits && ti.edits[0] && ti.edits[0].file_path) || null
}

function runHook() {
  let s = ''
  process.stdin.on('data', (d) => (s += d)).on('end', () => {
    let input = {}
    try { input = JSON.parse(s) } catch { process.exit(0) } // not our shape → don't block
    const fp = extractPath(input)
    if (!fp) process.exit(0)
    const mode = (process.env.POLISH_MODE || '').toLowerCase() || null
    const { allow, reason } = decide(fp, mode)
    if (!allow) {
      console.error(`[polish deny] ${reason} :: ${norm(fp)}`)
      process.exit(2)
    }
    process.exit(0)
  })
}

// ---- self-test (spec §5.2 gate 3: write-scope enforcement) ----
function selftest() {
  const assert = (c, m) => { if (!c) { console.error('FAIL:', m); process.exit(1) } }
  const root = '/path/to/your/project'

  // security worker:
  assert(decide(`${root}/polish/security-report.md`, 'security').allow, 'security CAN write own report')
  assert(decide(`${root}/polish/security-report.json`, 'security').allow, 'security CAN write own report JSON')
  assert(decide(`${root}/src/api/login.ts`, 'security').allow, 'security CAN write source (auto-fix)')
  assert(!decide(`${root}/polish/errors-report.md`, 'security').allow, 'security CANNOT write errors report (cross-worker)')
  assert(!decide(`${root}/polish-progress.md`, 'security').allow, 'security CANNOT write polish-progress.md')
  assert(!decide(`${root}/polish-report.md`, 'security').allow, 'security CANNOT write polish-report.md')
  assert(!decide(`${root}/polish-log.md`, 'security').allow, 'security CANNOT write polish-log.md')
  assert(!decide(`${root}/orchestrator-progress.md`, 'security').allow, 'security CANNOT write sibling-engine state')
  assert(!decide(`${root}/octopus/state/x.json`, 'security').allow, 'security CANNOT write octopus state')
  assert(!decide(`${root}/polish/cso-exclusions.json`, 'security').allow, 'security CANNOT write shared cso-exclusions')

  // market worker (recommendations-only):
  assert(decide(`${root}/polish/market-report.md`, 'market').allow, 'market CAN write own report')
  assert(!decide(`${root}/src/Landing.tsx`, 'market').allow, 'market CANNOT write source (recommendations-only)')
  assert(!decide(`${root}/polish/value-report.md`, 'market').allow, 'market CANNOT write value report (cross-worker)')

  // value worker (recommendations-only):
  assert(!decide(`${root}/src/Hero.tsx`, 'value').allow, 'value CANNOT write source')
  assert(decide(`${root}/polish/value-report.md`, 'value').allow, 'value CAN write own report')

  // errors worker (fixer):
  assert(decide(`${root}/src/util.ts`, 'errors').allow, 'errors CAN write source')
  assert(!decide(`${root}/polish/security-report.md`, 'errors').allow, 'errors CANNOT write security report')

  // C: drive denied for everyone:
  assert(!decide('C:/Users/kindl/x.ts', 'errors').allow, 'C: drive denied (backslash-normalized)')
  assert(!decide('C:\\Users\\kindl\\x.ts', 'security').allow, 'C: drive denied (literal backslash)')
  assert(!decide('/mnt/c/x', 'errors').allow, 'WSL /mnt/c denied')

  // checkpoint files denied regardless of name prefix:
  assert(!decide(`${root}/polish-v2-checkpoint.json`, 'errors').allow, 'any *-checkpoint.json denied')

  // POLISH_MODE unset: global denies still hold; unattributable report allowed.
  assert(!decide(`${root}/polish-progress.md`, null).allow, 'progress denied even without mode')
  assert(!decide('C:/x.ts', null).allow, 'C: denied even without mode')
  assert(decide(`${root}/polish/errors-report.md`, null).allow, 'unattributable report write allowed when POLISH_MODE unset')
  assert(decide(`${root}/src/x.ts`, null).allow, 'source allowed when mode unknown (can\'t prove reco-only)')

  // extractPath handles the real PreToolUse shape + Edit edits[].
  assert(extractPath({ tool_input: { file_path: '/a/b.ts' } }) === '/a/b.ts', 'extractPath file_path')
  assert(extractPath({ tool_input: { edits: [{ file_path: '/c/d.ts' }] } }) === '/c/d.ts', 'extractPath edits[0]')
  assert(extractPath({}) === null, 'extractPath empty → null')

  // reportMode parsing
  assert(reportMode('x/polish/arch-report.md') === 'arch', 'reportMode md')
  assert(reportMode('x/polish/api-test-report.json') === 'api-test', 'reportMode hyphenated json')
  assert(reportMode('x/src/foo.ts') === null, 'non-report → null')

  console.log('scope_guard selftest: PASS (own-report-only, cross-worker-deny, reco-only-no-source, orch/engine deny, mode-unset global denies)')
}

const isSelftest = process.argv.includes('--selftest')
if (isSelftest) selftest()
else runHook()

// Export-equivalent for potential reuse / clarity (ESM): the decision fn is the unit.
export { decide, reportMode, extractPath, RECO_ONLY, ALL_MODES }
