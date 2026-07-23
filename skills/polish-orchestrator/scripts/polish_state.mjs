#!/usr/bin/env node
// polish-orchestrator v2 — durable state + resume planner (deterministic prep).
// Ports SKILL.md "Startup Sequence" L10-15, "Dossier Reuse" L18-19, the staleness
// cache short-circuit L123-138, and "Resumability" L203-208 into a real, testable
// Node script — because the Workflow control script has NO fs/child_process/Date.
//
// The Workflow tool's native resume is in-session only (spec §3.2); this script is the
// DURABLE cross-session checkpoint layer on top of it. It reads polish-progress.md
// (schema: polish-progress/v2, spec §1.4 PolishProgress) and reports which phases/modes
// are already done so the orchestrator re-dispatches ONLY the incomplete specialists.
//
// Subcommands:
//   init     --root R --project P [--lock OWNER] [--lean] [--skip-staleness] [--head SHA]
//            mkdir the polish/ tree, decide dossier-reuse + staleness disposition, read or
//            seed polish-progress.md, acquire the lock, and PRINT the resume plan (JSON).
//   phase    --root R --project P --phase NAME [--completed-modes a,b] [--blocked json]
//            [--staleness done|skipped|cached] [--clear-lock]
//            durably advance polish-progress.md after a phase boundary (spec §3.2:
//            "written after every phase"). Idempotent.
//   selftest run the unit gate in a temp dir; exit non-zero on failure.
//
// Writes (under <root>/<project>/): polish/ tree + polish-progress.md (+ the dossier/cache
// are written by the explorer/staleness AGENTS, not here — this script only reads them to
// decide reuse). NEVER writes any *-report.md, polish-report.md, or sibling-engine state.
//
// Forward slashes only (Windows-safe via node:path). No hardcoded roots. No secrets.

import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'

const SCHEMA = 'polish-progress/v2'
const PROGRESS_FILE = 'polish-progress.md'

// The polish/ working tree the orchestrator + workers read/write.
const POLISH_TREE = ['polish']

// Canonical phase order (spec §1.1). explore gates everything; wave0 runs WITH wave1.
const PHASES = ['explore', 'wave1', 'wave2', 'wave3', 'synthesis', 'complete']

// Mode → wave assignment (spec §1.2 / SKILL.md waves). wave0 staleness is tracked separately.
const WAVE_MODES = {
  wave1: ['errors', 'deps', 'security', 'perf', 'docs', 'api-test', 'compliance'],
  wave2: ['ux', 'design', 'journeys', 'arch', 'foundation'],
  wave3: ['market', 'value', 'copy'],
}
const ALL_MODES = [...WAVE_MODES.wave1, ...WAVE_MODES.wave2, ...WAVE_MODES.wave3]

function parseArgs(argv) {
  const a = { _: [] }
  for (let i = 2; i < argv.length; i++) {
    const t = argv[i]
    if (t === '--selftest') a.selftest = true
    else if (t === '--lean') a.lean = true
    else if (t === '--skip-staleness') a.skipStaleness = true
    else if (t === '--clear-lock') a.clearLock = true
    else if (t.startsWith('--')) { a[t.slice(2)] = argv[i + 1]; i++ }
    else a._.push(t)
  }
  return a
}

function projDir(root, project) {
  // project may be "." (root itself), an absolute path, or a name under root.
  if (!project || project === '.') return root
  if (path.isAbsolute(project)) return project
  return path.join(root, project)
}

function mkTree(base) {
  for (const d of POLISH_TREE) fs.mkdirSync(path.join(base, d), { recursive: true })
}

// ---- polish-progress.md (durable checkpoint) read/write ----
// Stored as a fenced JSON block inside markdown so it stays human-readable AND machine-parseable.
function readProgress(base) {
  const p = path.join(base, PROGRESS_FILE)
  try {
    const raw = fs.readFileSync(p, 'utf8')
    const m = raw.match(/```json\s*([\s\S]*?)```/)
    if (m) {
      const obj = JSON.parse(m[1])
      if (obj && obj.schema === SCHEMA) return obj
    }
  } catch { /* missing or unreadable → fresh */ }
  return null
}

function writeProgress(base, obj, nowISO) {
  obj.schema = SCHEMA
  obj.updated_at = nowISO
  const body =
    `# Polish Progress\n\n` +
    `Durable cross-session checkpoint (Workflow native resume is in-session only — spec §3.2).\n` +
    `The orchestrator reads this on startup and re-dispatches ONLY incomplete specialists.\n\n` +
    '```json\n' + JSON.stringify(obj, null, 2) + '\n```\n'
  fs.writeFileSync(path.join(base, PROGRESS_FILE), body)
}

function freshProgress(nowISO) {
  return {
    schema: SCHEMA,
    phase: 'explore',
    lock: { owner: null, acquired_at: null },
    dossier_path: 'polish/polish-context.md',
    completed_modes: [],
    blocked_modes: [],
    staleness: 'pending',
    updated_at: nowISO,
  }
}

// ---- dossier-reuse short-circuit (SKILL.md L18-19) ----
function dossierExists(base) {
  return fs.existsSync(path.join(base, 'polish', 'polish-context.md'))
}

// ---- staleness disposition (SKILL.md L134-138): skip if no cache help; cached if valid ----
// Valid cache = exists, <7 days old, AND project_hash matches current HEAD (passed in via --head).
function stalenessDisposition(base, { skipStaleness, currentHead, nowMs }) {
  if (skipStaleness) return { staleness: 'skipped', reason: 'user --skip-staleness' }
  const cachePath = path.join(base, 'polish', 'staleness-cache.json')
  try {
    const c = JSON.parse(fs.readFileSync(cachePath, 'utf8'))
    const ageDays = c.cached_at ? Math.floor((nowMs - Date.parse(c.cached_at)) / 86400000) : 999
    const headMatch = currentHead && c.project_hash && c.project_hash === currentHead
    if (ageDays < 7 && headMatch) return { staleness: 'cached', reason: `valid cache (age ${ageDays}d, HEAD match)` }
    return { staleness: 'run', reason: `cache stale (age ${ageDays}d, headMatch=${!!headMatch})` }
  } catch {
    return { staleness: 'run', reason: 'no cache' }
  }
}

// ---- resume planner (SKILL.md L203-208) ----
// Given current progress, compute which modes still need dispatch per wave, and which
// phase to resume at. Returns the plan the workflow consumes to skip completed work.
function planResume(prog) {
  const done = new Set(prog.completed_modes || [])
  const blocked = new Set((prog.blocked_modes || []).map((b) => b.mode))
  // A mode is "settled" if completed OR blocked (blocked → logged + skipped, SKILL.md L173).
  const settled = (m) => done.has(m) || blocked.has(m)
  const pending = {
    wave1: WAVE_MODES.wave1.filter((m) => !settled(m)),
    wave2: WAVE_MODES.wave2.filter((m) => !settled(m)),
    wave3: WAVE_MODES.wave3.filter((m) => !settled(m)),
  }
  // Resume at the earliest phase that still has pending modes (or the recorded phase).
  let resumePhase = prog.phase
  if (prog.phase !== 'complete') {
    if (prog.phase === 'explore') resumePhase = dossierDone(prog) ? 'wave1' : 'explore'
    if (['explore', 'wave1'].includes(resumePhase) && pending.wave1.length === 0 && dossierDone(prog)) resumePhase = 'wave2'
    if (['explore', 'wave1', 'wave2'].includes(resumePhase) && pending.wave1.length === 0 && pending.wave2.length === 0 && dossierDone(prog)) resumePhase = 'wave3'
    if (pending.wave1.length === 0 && pending.wave2.length === 0 && pending.wave3.length === 0 && dossierDone(prog)) resumePhase = 'synthesis'
  }
  return { resume_phase: resumePhase, pending_modes: pending, completed_modes: [...done], blocked_modes: prog.blocked_modes || [] }
}

function dossierDone(prog) {
  // explore is done once we've advanced past it at least once.
  return PHASES.indexOf(prog.phase) > PHASES.indexOf('explore') || prog.phase === 'complete'
    || (prog.completed_modes && prog.completed_modes.length > 0)
}

// ---- init: the Phase-0 deterministic prep + resume decision ----
function cmdInit(args, { nowMs, nowISO }) {
  const root = args.root || process.cwd()
  const base = projDir(root, args.project)
  mkTree(base)

  let prog = readProgress(base)
  const fresh = !prog
  if (fresh) prog = freshProgress(nowISO)

  // Lock protocol (SKILL.md L13, the orchestrator lock protocol): acquire if free; report contention.
  let lockConflict = null
  if (args.lock) {
    if (prog.lock && prog.lock.owner && prog.lock.owner !== args.lock) {
      lockConflict = prog.lock.owner
    } else {
      prog.lock = { owner: args.lock, acquired_at: nowISO }
    }
  }

  const reuseDossier = !fresh && dossierExists(base) && (prog.completed_modes || []).length === 0 && dossierDone(prog) === false
    ? false // dossier exists but we never progressed — still reuse for mode-selection short-circuit
    : dossierExists(base)
  const stale = stalenessDisposition(base, { skipStaleness: args.skipStaleness, currentHead: args.head, nowMs })
  if (prog.staleness === 'pending') prog.staleness = stale.staleness === 'run' ? 'pending' : stale.staleness

  if (!lockConflict) writeProgress(base, prog, nowISO)

  const plan = planResume(prog)
  const out = {
    engine: 'polish-v2',
    project_dir: base.split(path.sep).join('/'),
    fresh_run: fresh,
    lean: !!args.lean,
    lock_conflict: lockConflict,             // non-null → orchestrator must halt & confirm
    dossier_reuse: dossierExists(base),       // SKILL.md L18-19 short-circuit hint
    dossier_path: 'polish/polish-context.md',
    staleness: { disposition: stale.staleness, reason: stale.reason, skip_wave0: stale.staleness !== 'run' },
    all_modes: ALL_MODES,
    wave_modes: WAVE_MODES,
    resume: plan,
    progress_file: 'polish-progress.md',
  }
  return out
}

// ---- phase: durably advance the checkpoint after a phase boundary ----
function cmdPhase(args, { nowISO }) {
  const root = args.root || process.cwd()
  const base = projDir(root, args.project)
  let prog = readProgress(base) || freshProgress(nowISO)
  if (args.phase) {
    if (!PHASES.includes(args.phase)) throw new Error(`unknown phase: ${args.phase}`)
    prog.phase = args.phase
  }
  if (args['completed-modes']) {
    const add = args['completed-modes'].split(',').map((s) => s.trim()).filter(Boolean)
    const set = new Set(prog.completed_modes || [])
    for (const m of add) set.add(m)
    prog.completed_modes = [...set]
  }
  if (args.blocked) {
    try {
      const arr = JSON.parse(args.blocked) // [{mode,reason}]
      const byMode = new Map((prog.blocked_modes || []).map((b) => [b.mode, b]))
      for (const b of arr) if (b && b.mode) byMode.set(b.mode, { mode: b.mode, reason: b.reason || '' })
      prog.blocked_modes = [...byMode.values()]
    } catch (e) { /* fail-soft: ignore malformed blocked arg */ }
  }
  if (args.staleness) prog.staleness = args.staleness
  if (args.clearLock) prog.lock = { owner: null, acquired_at: null }
  writeProgress(base, prog, nowISO)
  return { engine: 'polish-v2', project_dir: base.split(path.sep).join('/'), phase: prog.phase, completed_modes: prog.completed_modes, blocked_modes: prog.blocked_modes, staleness: prog.staleness, lock: prog.lock }
}

// ---- self-test (spec §5.2 gates 2 & 4: DAG resume + durable checkpoint) ----
function selftest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'polish-state-'))
  const assert = (c, m) => { if (!c) { console.error('FAIL:', m); process.exit(1) } }
  const proj = 'proj'
  const base = path.join(tmp, proj)
  const env = (overrideMs) => ({ nowMs: overrideMs ?? Date.now(), nowISO: new Date(overrideMs ?? Date.now()).toISOString() })

  // 1. fresh init: creates polish/ tree + polish-progress.md, resumes at explore, lock acquired.
  const i1 = cmdInit({ root: tmp, project: proj, lock: 'run-A' }, env())
  assert(fs.existsSync(path.join(base, 'polish')), 'polish/ tree created')
  assert(fs.existsSync(path.join(base, PROGRESS_FILE)), 'polish-progress.md written')
  assert(i1.fresh_run === true, 'fresh run flagged')
  assert(i1.resume.resume_phase === 'explore', 'fresh resumes at explore')
  assert(i1.lock_conflict === null, 'lock acquired (no conflict)')
  assert(i1.staleness.skip_wave0 === false && i1.staleness.disposition === 'run', 'no cache → staleness runs')

  // 2. lock contention: a different owner must be reported as conflict, progress NOT overwritten.
  const i2 = cmdInit({ root: tmp, project: proj, lock: 'run-B' }, env())
  assert(i2.lock_conflict === 'run-A', 'different owner reported as lock conflict')

  // 3. advance explore → wave1 done (errors, deps, security complete), checkpoint persists across "sessions".
  cmdPhase({ root: tmp, project: proj, phase: 'wave1', 'completed-modes': 'errors,deps,security' }, env())
  const after1 = readProgress(base)
  assert(after1.phase === 'wave1', 'phase advanced to wave1 on disk')
  assert(after1.completed_modes.length === 3, '3 wave1 modes recorded')

  // 4. fresh init in a "new session" reads the checkpoint and re-plans: wave1 has 4 pending, NOT 7.
  const i3 = cmdInit({ root: tmp, project: proj, lock: 'run-A' }, env())
  assert(i3.fresh_run === false, 'second init is NOT fresh (checkpoint read)')
  assert(i3.resume.pending_modes.wave1.length === 4, 'only 4 wave1 modes pending after resume (7-3)')
  assert(!i3.resume.pending_modes.wave1.includes('errors'), 'completed errors mode not re-dispatched')
  assert(i3.dossier_reuse === false, 'no dossier file yet → no reuse')

  // 5. blocked mode is settled (skipped, not re-dispatched). SKILL.md L173.
  cmdPhase({ root: tmp, project: proj, phase: 'wave1', blocked: JSON.stringify([{ mode: 'perf', reason: 'no runtime' }]) }, env())
  const i4 = cmdInit({ root: tmp, project: proj }, env())
  assert(!i4.resume.pending_modes.wave1.includes('perf'), 'blocked perf mode not re-dispatched')
  assert(i4.resume.blocked_modes.some((b) => b.mode === 'perf'), 'blocked perf recorded in plan')

  // 6. dossier-reuse short-circuit: once polish-context.md exists, dossier_reuse flips true.
  fs.mkdirSync(path.join(base, 'polish'), { recursive: true })
  fs.writeFileSync(path.join(base, 'polish', 'polish-context.md'), '# dossier')
  const i5 = cmdInit({ root: tmp, project: proj }, env())
  assert(i5.dossier_reuse === true, 'dossier-reuse detected when polish-context.md exists')

  // 7. staleness cache: valid (<7d + HEAD match) → cached; stale HEAD → run.
  const now = Date.now()
  fs.writeFileSync(path.join(base, 'polish', 'staleness-cache.json'), JSON.stringify({ cached_at: new Date(now - 2 * 86400000).toISOString(), project_hash: 'abc123', findings: [] }))
  const cValid = cmdInit({ root: tmp, project: proj, head: 'abc123' }, env(now))
  assert(cValid.staleness.disposition === 'cached' && cValid.staleness.skip_wave0 === true, 'valid cache + HEAD match → wave0 skipped')
  const cStaleHead = cmdInit({ root: tmp, project: proj, head: 'DIFFERENT' }, env(now))
  assert(cStaleHead.staleness.disposition === 'run', 'HEAD mismatch → staleness runs')
  const cOld = (() => { fs.writeFileSync(path.join(base, 'polish', 'staleness-cache.json'), JSON.stringify({ cached_at: new Date(now - 30 * 86400000).toISOString(), project_hash: 'abc123', findings: [] })); return cmdInit({ root: tmp, project: proj, head: 'abc123' }, env(now)) })()
  assert(cOld.staleness.disposition === 'run', '>7d cache → staleness runs (even with HEAD match)')

  // 8. --skip-staleness forces skipped regardless of cache.
  const cSkip = cmdInit({ root: tmp, project: proj, skipStaleness: true, head: 'abc123' }, env(now))
  assert(cSkip.staleness.disposition === 'skipped' && cSkip.staleness.skip_wave0 === true, '--skip-staleness → wave0 dropped')

  // 9. synthesis resume: all modes complete → resume at synthesis.
  cmdPhase({ root: tmp, project: proj, phase: 'wave3', 'completed-modes': ALL_MODES.filter((m) => m !== 'perf').join(',') }, env())
  const i6 = cmdInit({ root: tmp, project: proj }, env())
  assert(i6.resume.resume_phase === 'synthesis', 'all modes settled → resume at synthesis')

  // 10. complete + clear lock.
  cmdPhase({ root: tmp, project: proj, phase: 'complete', clearLock: true }, env())
  const done = readProgress(base)
  assert(done.phase === 'complete' && done.lock.owner === null, 'complete + lock cleared')

  // 11. project "." resolves to root itself (no subdir).
  const i7 = cmdInit({ root: tmp, project: '.' }, env())
  assert(fs.existsSync(path.join(tmp, 'polish')), 'project "." writes polish/ at root')
  assert(i7.project_dir === tmp.split(path.sep).join('/'), 'project_dir forward-slashed root')

  fs.rmSync(tmp, { recursive: true, force: true })
  console.log('polish_state selftest: PASS (tree, durable checkpoint, lock, resume-skip, blocked-settle, dossier-reuse, staleness cache/skip, synthesis-resume)')
}

// ---- main ----
const args = parseArgs(process.argv)
if (args.selftest) {
  selftest()
} else {
  const cmd = args._[0]
  const ctx = { nowMs: Date.now(), nowISO: new Date().toISOString() }
  try {
    let out
    if (cmd === 'init') out = cmdInit(args, ctx)
    else if (cmd === 'phase') out = cmdPhase(args, ctx)
    else { console.error('usage: polish_state.mjs <init|phase|--selftest> [...]'); process.exit(2) }
    console.log(JSON.stringify(out, null, 2))
  } catch (e) {
    console.error('polish_state error:', e.message)
    process.exit(1)
  }
}
