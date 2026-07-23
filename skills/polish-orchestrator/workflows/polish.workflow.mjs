export const meta = {
  name: 'polish-orchestrator-v2',
  description: 'THE POLISHER on the Workflow tool — explore → 3 waves of specialist auditors (15 modes) → synthesis, with durable resume and dispatch-layer write-scoping.',
  phases: [
    { title: 'Phase0-Explore', detail: 'deterministic prep (polish_state init) + explorer agent: dossier + mode selection + Swarm injection' },
    { title: 'Phase1-Wave0+Wave1', detail: 'parallel: staleness (wave0) ∥ {errors,deps,security,perf,docs,api-test,compliance}' },
    { title: 'Phase2-Wave2', detail: 'parallel: {ux,design,journeys,arch,foundation} — arch reads staleness-report' },
    { title: 'Phase3-Wave3', detail: 'parallel: {market,value,copy} — strategic, recommendations-mostly' },
    { title: 'Phase4-Synthesis', detail: 'synthesizer agent: synthesize.mjs → polish-report.md + polish-log.md, finalize checkpoint' },
  ],
}

// ============================================================================
// Deterministic wave-DAG orchestration for THE POLISHER.
//
// WHY this shape (vs the spec's illustrative workflow.parallel()/runScript()/checkpoint()):
//  - The Workflow control script has NO fs / child_process / Date / Math.random. So every
//    deterministic step (mkdir polish/, read/write polish-progress.md, compute resume plan,
//    aggregate worker JSON into polish-report.md) runs INSIDE a thin agent that shells the
//    bundled scripts (scripts/polish_state.mjs, scripts/synthesize.mjs). The control script
//    only sequences phases and fans out specialists.
//  - agent(prompt,{schema,model,isolation,label,phase}) is the only dispatch primitive.
//    There are NO per-dispatch tool denies — the MUST-PRESERVE write-scoping
//    (spec §3.1) is enforced by hooks/deny-write-out-of-scope.json (PreToolUse → scope_guard.mjs)
//    and RESTATED in every specialist prompt. Worktree isolation (spec §2.2/§3.1) is the
//    structural backstop: each auto-fixer writes in an isolated checkout, merged at synthesis.
//  - DAG edges: explore → wave1 → wave2 → wave3 → synthesis are SEQUENTIAL phases (gated on
//    prior outputs, mirroring SKILL.md L142/153/162). Wave 0 (staleness) runs in the SAME
//    parallel stage as Wave 1 (SKILL.md L101-103) and feeds ONLY arch (SKILL.md L140).
//  - Durable cross-session resume (spec §3.2): polish_state writes polish-progress.md after
//    every phase; on a cold start the explorer's init reports which modes are already done so
//    we re-dispatch ONLY the pending ones (SKILL.md L203-208).
//
// Inputs (workflow args, all optional): { root, project, lean, skipStaleness, head, lock }
//  - root      : your projects root (default: current directory)
//  - project   : the codebase to polish, relative to root or absolute or "." (default ".")
//  - lean      : --lean → all specialists on sonnet (orchestrator stays opus). SKILL.md L175-176.
//  - skipStaleness : drop Wave 0. SKILL.md L137.
//  - head      : current `git rev-parse HEAD` for the staleness-cache validity check.
//  - lock      : owner string for the polish-progress.md lock (orchestrator lock protocol, SKILL.md L13).
// ============================================================================

const ARGS = (typeof input === 'object' && input) ? input : {}
const ROOT = ARGS.root || '.'
const PROJECT = ARGS.project || '.'
const LEAN = !!ARGS.lean
const SKIP_STALENESS = !!ARGS.skipStaleness
const HEAD = ARGS.head || ''
const LOCK = ARGS.lock || 'polish-v2'

const SKILL = '${CLAUDE_SKILL_DIR}'  // resolved by the runtime to this skill dir; scripts addressed under it
const WORKER_REF = 'polish-worker/SKILL.md' // 16 mode methodologies (the sibling polish-worker skill)

// model tier for a specialist: judgment modes = opus, mechanical = sonnet; --lean forces sonnet.
// security is ALWAYS opus and ALWAYS maximum rigor regardless of --lean's model choice (spec §3.3).
const tier = (base, mode) => (LEAN ? (mode === 'security' ? 'opus' : 'sonnet') : base)

// --- shared specialist preamble (calibration table + write-scope contract, ported verbatim intent) ---
const CALIBRATION =
  'Calibrate standards to the dossier ambition level: Prototype = structural risks only (ignore polish); ' +
  'MVP = real problems, no over-engineering (flag cosmetics, don\'t fix); Production = full rigor; ' +
  'Enterprise = max rigor + compliance. (polish-worker calibration table.)'

const WRITE_SCOPE = (mode, recoOnly) =>
  `WRITE-SCOPE (ENFORCED at the dispatch layer by a PreToolUse hook — NOT honor-system): ` +
  `you may write ONLY polish/${mode}-report.md (+ polish/${mode}-report.json companion)` +
  (recoOnly ? ` — you are RECOMMENDATIONS-ONLY: do NOT modify any project source file.` : ` AND project source files (for auto-fixes).`) +
  ` You may NOT write any other mode's polish/*-report.*, nor polish-progress.md / polish-report.md / polish-log.md / cso-exclusions.json, ` +
  `nor any sibling build-orchestrator/engine state file. NEVER write outside the target project directory. Attempts are blocked.`

// Each specialist's prompt = read dossier + your briefing notes + your mode methodology (from polish-worker)
// + calibration + write-scope, then emit BOTH the markdown report AND the §1.4 PolishWorkerReport JSON.
const specialistPrompt = (mode, extra) =>
  `You are a POLISHER worker, world-class specialist in the \`${mode}\` quality dimension. ` +
  `Read FIRST: ${PROJECT}/polish/polish-context.md (the orchestrator's dossier) — find your "For \`${mode}\` worker" briefing section and follow it closely. ` +
  `Read your mode methodology verbatim from ${WORKER_REF} (the \`${mode}\` section) and execute it exhaustively (don't sample). ` +
  `${extra || ''} ${CALIBRATION} ` +
  `Auto-fix what you are confident about (match existing style; mark fixes with a brief // Polisher: comment); document risky changes as recommendations. ` +
  `Write your human report to ${PROJECT}/polish/${mode}-report.md (template: polish-worker report format) AND a machine companion ${PROJECT}/polish/${mode}-report.json ` +
  `matching the PolishWorkerReport schema (mode, model, status COMPLETE|BLOCKED, blocked_reason, health_score 1-10, findings[{severity,title,location,impact,fix_status,detail}], auto_fixes[{file,line,before,after,reason}]). ` +
  `Be honest, not nice — find real problems, but do NOT invent findings. ` +
  `${WRITE_SCOPE(mode, mode === 'market' || mode === 'value')} ` +
  `Return the PolishWorkerReport object.`

const REPORT_SCHEMA = {
  type: 'object', additionalProperties: true,
  required: ['mode', 'status'],
  properties: {
    mode: { type: 'string' },
    model: { type: 'string' },
    status: { type: 'string', enum: ['COMPLETE', 'BLOCKED'] },
    blocked_reason: { type: ['string', 'null'] },
    health_score: { type: ['number', 'null'] },
    findings: { type: 'array', items: { type: 'object', additionalProperties: true } },
    auto_fixes: { type: 'array', items: { type: 'object', additionalProperties: true } },
  },
}

// Wave configs (model per spec §1.2 table). isolation:"worktree" on every fixer so auto-fixes
// land in an isolated checkout (spec §2.2/§3.1); recommendations-only modes need no worktree.
const WAVE1 = [
  { mode: 'errors', model: 'sonnet', iso: true, extra: 'Hunt unhandled exceptions, null/undefined access, off-by-one, async races, missing UI error/loading/empty states, broken imports, circular deps, dead code, type mismatches.' },
  { mode: 'deps', model: 'sonnet', iso: true, extra: 'Audit manifests + lockfiles. Flag CVEs, unused deps, license incompatibility, lockfile drift. Update patch versions; flag major bumps. Use Swarm dep-audit evidence if present.' },
  { mode: 'security', model: 'opus', iso: true, extra: 'CSO Mode: OWASP Top 10 + STRIDE. Zero-noise — honor polish/cso-exclusions.json, 8/10+ confidence gate, independent verification. Each finding needs a concrete exploit scenario, not just a category. ALWAYS maximum rigor — no prototype exception, and --lean does NOT lower your rigor. Use Swarm-confirmed vulns if present (verify fix status; do not re-discover).' },
  { mode: 'perf', model: 'sonnet', iso: true, extra: 'N+1, missing indexes, unoptimized images, missing caching, needless re-renders, sync-should-be-async, bundle bloat, missing pagination/debounce. Add caching/lazy-loading/debounce where safe.' },
  { mode: 'docs', model: 'sonnet', iso: true, extra: 'Generate/update README (desc, setup, usage, env vars, deploy), API docs from routes, component docs, deployment guide. Enhance existing docs, never overwrite.' },
  { mode: 'api-test', model: 'sonnet', iso: true, extra: 'Map every endpoint (method+path+expected shapes). Generate contract tests: correct→expected status/shape, wrong method→405, no auth→401, bad input→400. Use Swarm endpoint map if present.' },
  { mode: 'compliance', model: 'sonnet', iso: true, extra: 'GDPR/CCPA basics: PII-without-consent, missing privacy policy / cookie consent / ToS, copyleft (GPL) in proprietary, tracking without opt-out, missing deletion path, GDPR Art 13/14. Use Swarm secrets-scan if present.' },
]
const WAVE2 = [
  { mode: 'ux', model: 'opus', iso: true, extra: 'Define 3-5 personas from the dossier; simulate first-visit, core action, edge cases (bad input, back, refresh), return visit. Document every friction point. Fix clear UX bugs.' },
  { mode: 'design', model: 'opus', iso: true, extra: 'WCAG 2.1 AA (contrast, alt text, keyboard nav, focus), responsive breakpoints, spacing/font/color consistency, component patterns. Fix a11y violations + alt text + contrast + responsive.' },
  { mode: 'journeys', model: 'opus', iso: true, extra: 'Map all entry points → forward paths; find dead ends, circular flows, orphan pages, missing error/empty/first-run states. Add missing states; fix dead-end nav. Include a journey map.' },
  { mode: 'arch', model: 'opus', iso: true, extra: 'READ polish/staleness-report.md (Wave 0) and fold dependency-freshness into the architecture assessment. Map module deps; find circular deps, god files (>500 LOC), tight coupling, leaky abstractions; assess scale match + tech debt. Include an arch health score. Use Swarm architecture scan if present.' },
  { mode: 'foundation', model: 'opus', iso: true, extra: 'Design-system coherence: ad-hoc spacing vs a scale, inconsistent type hierarchy, non-token colors, inconsistent breakpoints, pattern violations, missing dark-mode tokens. Extract tokens; normalize spacing.' },
]
const WAVE3 = [
  { mode: 'market', model: 'opus', iso: false, extra: 'Value prop AS BUILT (not as intended). What users compare this to; competitive gaps + unique advantages; would the target user choose this? Recommendations only — no source writes.' },
  { mode: 'value', model: 'opus', iso: false, extra: 'Skeptical first-time customer: is value clear in 30s? clear CTA? when does the aha-moment arrive? #1 bounce reason? Recommendations only — no source writes.' },
  { mode: 'copy', model: 'opus', iso: true, extra: 'Audience/tone match, jargon, vague CTAs, missing microcopy, grammar/spelling, placeholder text in production, multilingual inconsistencies. Fix grammar/spelling/placeholders/vague CTAs; flag tone changes.' },
]

const dispatch = (w, ph) => agent(specialistPrompt(w.mode, w.extra), {
  model: tier(w.model, w.mode),
  isolation: w.iso ? 'worktree' : undefined,
  schema: REPORT_SCHEMA,
  label: `polish:${w.mode}`,
  phase: ph,
})

// ============================================================================
// RUN
// ============================================================================

phase('Phase0-Explore')
log(`THE POLISHER v2 — project=${PROJECT} lean=${LEAN} skipStaleness=${SKIP_STALENESS}`)

// 0a. Deterministic prep + resume decision (shells polish_state init — control script has no fs).
const planText = await agent(
  `Run the Phase-0 prep script and return its printed JSON VERBATIM (no prose). Execute exactly: ` +
  `\`node ${SKILL}/scripts/polish_state.mjs init --root ${ROOT} --project ${PROJECT} --lock ${LOCK}` +
  `${LEAN ? ' --lean' : ''}${SKIP_STALENESS ? ' --skip-staleness' : ''}${HEAD ? ' --head ' + HEAD : ''}\` ` +
  `(resolve ${SKILL} to this skill's directory). It mkdirs the polish/ tree, reads/seeds polish-progress.md (the durable ` +
  `cross-session checkpoint), acquires the lock, decides dossier-reuse + the Wave-0 staleness disposition, and prints a resume plan. ` +
  `Return that JSON object.`,
  { schema: { type: 'object', additionalProperties: true, required: ['engine', 'resume'] }, label: 'polish:init', phase: 'Phase0-Explore' }
)
const plan = parsePlan(planText)
if (plan.lock_conflict) return { halted: `polish run already in progress (lock owner: ${plan.lock_conflict}) — confirm with the operator before forcing` }

const pending = (plan.resume && plan.resume.pending_modes) || { wave1: WAVE1.map((w) => w.mode), wave2: WAVE2.map((w) => w.mode), wave3: WAVE3.map((w) => w.mode) }
const resumePhase = (plan.resume && plan.resume.resume_phase) || 'explore'
const runStaleness = !SKIP_STALENESS && !(plan.staleness && plan.staleness.skip_wave0)
log(`Resume at: ${resumePhase} | pending w1=${pending.wave1.length} w2=${pending.wave2.length} w3=${pending.wave3.length} | wave0 staleness=${runStaleness ? 'run' : (plan.staleness && plan.staleness.disposition)}`)

// 0b. Explorer — Phase 0 dossier (only if we're actually at explore; on resume past explore we reuse the dossier).
let dossier = null
if (resumePhase === 'explore') {
  dossier = await agent(
    `You are THE POLISHER orchestrator — a Senior QA Architect. Build the project dossier for ${PROJECT} (under ${ROOT}). ` +
    `Steps (port of SKILL.md Phase 0): (0.0) if ${PROJECT}/polish/polish-context.md already exists and the project is unchanged, REUSE it and skip to mode selection (dossier-reuse short-circuit). ` +
    `(0.1) Understand intent: read CLAUDE.md, brief.md, README.md, package manifests, main entry file (first 20 lines). ` +
    `(0.2) Rapid triage with Glob/Grep (NOT raw find/grep/cat): count source files, total LOC, git log depth, test files, TODO/FIXME/HACK/XXX markers. ` +
    `(0.3) Structural x-ray: entry points, data flow, auth boundary, external deps, build chain. ` +
    `(0.4) Risk mapping by project state (prototype/MVP/production/legacy/pipeline-fresh/landing/API — priority order per state). ` +
    `(0.5) Write the dossier to ${PROJECT}/polish/polish-context.md: project identity, tech fingerprint, maturity assessment, structural map, risk profile, recommended modes, and a "For \`<mode>\` worker" briefing-notes section for EACH selected mode. ` +
    `(0.6) Swarm-evidence injection: IF ${PROJECT}/swarm-output/ exists, APPEND tool-scan + attack evidence to the relevant per-worker briefing notes (security←attack-reports + sast; deps←dep-audit; api-test←health-check endpoints; perf←timing; compliance←secrets; arch←architecture scan). APPEND ONLY — never replace your own analysis; your analysis takes priority. If swarm-output/ is absent, skip 0.6 entirely. ` +
    `Constraints: read-only on project source in this phase (you only write polish/polish-context.md). NEVER write the C: drive. ` +
    `Return {arm:"explorer", status:"completed", selected_modes:[...], maturity:"...", summary:"..."}.`,
    { model: 'opus', schema: { type: 'object', additionalProperties: true, required: ['status'] }, label: 'polish:explorer', phase: 'Phase0-Explore' }
  )
  await checkpoint('explore', { phase: 'explore' })
} else {
  log('Dossier already exists (resume) — reusing polish/polish-context.md, skipping explorer.')
}

// --- Phase 1: Wave 0 (staleness) ∥ Wave 1 (independent specialists) ---
let wave1Results = []
if (['explore', 'wave1'].includes(resumePhase)) {
  phase('Phase1-Wave0+Wave1')
  const thunks = []
  // Wave 0 staleness lives in the SAME parallel stage as Wave 1 (spec §1.1) and feeds ONLY arch.
  if (runStaleness) {
    thunks.push(() => agent(
      `You are the POLISHER Wave-0 staleness auditor for ${PROJECT}. Compare actual code usage against CURRENT library docs via the Context7 MCP. ` +
      `Process: scan manifests for deps+versions; for the top ~10 critical deps (skip dev-only): (1) Context7 \`resolve-library-id\` with the library name (pass the manifest version); ` +
      `(2) Context7 \`get-library-docs\` with topic "breaking changes, migration guide, deprecated APIs" (cap ~30K tokens) — NOTE: the method is get-library-docs, NOT the obsolete "query-docs"; ` +
      `(3) Grep the codebase for actual usage of each flagged API and ONLY report a finding if the deprecated/renamed API is actually used (eliminates false positives). ` +
      `Categorize: DEPRECATED | RENAMED (give new name) | OUTDATED_PATTERN | VERSION_MISMATCH | CURRENT. ` +
      `Write polish/staleness-report.md (per-dependency findings) AND polish/staleness-report.json (array of {library,installed_version,latest_stable,category,api,used_in_code,new_name,evidence}). ` +
      `Also write/update polish/staleness-cache.json = {cached_at:<ISO>, project_hash:<git rev-parse HEAD>, findings:[...]} for the 7-day reuse cache. ` +
      `IF the Context7 MCP is unavailable, do NOT fail — write polish/staleness-report.md containing exactly "[STALENESS_SKIPPED: Context7 MCP not available]" and return status "BLOCKED". ` +
      `WRITE-SCOPE: only polish/staleness-report.{md,json} + polish/staleness-cache.json. NEVER write C:. Return the PolishWorkerReport (mode:"staleness").`,
      { model: tier('sonnet', 'staleness'), schema: REPORT_SCHEMA, label: 'polish:staleness', phase: 'Phase1-Wave0+Wave1' }
    ))
  } else {
    log(`Wave 0 skipped (${plan.staleness && plan.staleness.disposition}) — arch will read any existing staleness-report.md.`)
  }
  const w1 = WAVE1.filter((w) => pending.wave1.includes(w.mode))
  for (const w of w1) thunks.push(() => dispatch(w, 'Phase1-Wave0+Wave1'))
  wave1Results = await parallel(thunks)
  await checkpoint('wave1', { phase: 'wave1', completedModes: completedFrom(w1, wave1Results, runStaleness), blocked: blockedFrom(wave1Results) })
} else {
  log(`Skipping Wave 1 (resume at ${resumePhase}; all Wave-1 modes already settled).`)
}

// --- Phase 2: Wave 2 (context-enhanced; arch consumes staleness-report) ---
let wave2Results = []
if (['explore', 'wave1', 'wave2'].includes(resumePhase)) {
  phase('Phase2-Wave2')
  const w2 = WAVE2.filter((w) => pending.wave2.includes(w.mode))
  wave2Results = await parallel(w2.map((w) => () => dispatch(w, 'Phase2-Wave2')))
  await checkpoint('wave2', { phase: 'wave2', completedModes: completedFrom(w2, wave2Results, false), blocked: blockedFrom(wave2Results) })
} else {
  log(`Skipping Wave 2 (resume at ${resumePhase}).`)
}

// --- Phase 3: Wave 3 (strategic; reads all prior reports) ---
let wave3Results = []
if (resumePhase !== 'synthesis' && resumePhase !== 'complete') {
  phase('Phase3-Wave3')
  const w3 = WAVE3.filter((w) => pending.wave3.includes(w.mode))
  wave3Results = await parallel(w3.map((w) => () => dispatch(w, 'Phase3-Wave3')))
  await checkpoint('wave3', { phase: 'wave3', completedModes: completedFrom(w3, wave3Results, false), blocked: blockedFrom(wave3Results) })
} else {
  log(`Skipping Wave 3 (resume at ${resumePhase}).`)
}

// --- Phase 4: Synthesis (deterministic aggregation via synthesize.mjs, then narrative) ---
phase('Phase4-Synthesis')
const synthesis = await agent(
  `You are THE POLISHER synthesizer for ${PROJECT}. First run the deterministic aggregator and return its result, then finalize. Execute exactly: ` +
  `\`node ${SKILL}/scripts/synthesize.mjs --root ${ROOT} --project ${PROJECT}\` (resolve ${SKILL} to this skill dir). ` +
  `It reads every ${PROJECT}/polish/<mode>-report.json (PolishWorkerReport companions — NOT transcript scraping) plus the optional staleness-report.json, ` +
  `computes the overall health score (mean of completed dimensions, capped at 6 if any critical is unresolved), and writes ${PROJECT}/polish-report.md ` +
  `(Health Score, Verdict, severity table, what-was-auto-fixed, what-needs-human, Wave-3 strategic insights, per-dimension report links) and ${PROJECT}/polish-log.md (consolidated changes). ` +
  `If isolation worktrees were used by fixers, ensure their changes are merged into the working tree before/at this step with NO cross-worker file clobber. ` +
  `Then run \`node ${SKILL}/scripts/polish_state.mjs phase --root ${ROOT} --project ${PROJECT} --phase complete --clear-lock\` to mark the durable checkpoint complete and release the lock. ` +
  `WRITE-SCOPE: you (synthesizer) own polish-report.md / polish-log.md / polish-progress.md (the scope-guard allows the synthesizer; specialists never write these). NEVER write C:. NEVER git push. ` +
  `Return {arm:"synthesizer", status:"completed", health_score:<n>, verdict:"<one line>", summary:"..."}.`,
  { model: 'opus', schema: { type: 'object', additionalProperties: true, required: ['status'] }, label: 'polish:synthesizer', phase: 'Phase4-Synthesis' }
)

return {
  project: PROJECT,
  lean: LEAN,
  resumed_at: resumePhase,
  dossier: dossier ? summ(dossier) : 'reused',
  wave1: wave1Results.filter(Boolean).map(summ),
  wave2: wave2Results.filter(Boolean).map(summ),
  wave3: wave3Results.filter(Boolean).map(summ),
  synthesis: summ(synthesis),
}

// ============================================================================
// helpers (plain JS — no Date/fs/Math.random)
// ============================================================================
function parsePlan(text) {
  if (text && typeof text === 'object') return text
  try { return JSON.parse(String(text)) } catch {}
  try { const s = String(text); return JSON.parse(s.slice(s.indexOf('{'), s.lastIndexOf('}') + 1)) } catch {}
  return { engine: 'polish-v2', resume: {}, staleness: {} }
}
function summ(e) {
  if (!e || typeof e !== 'object') return { status: 'failed', summary: 'no result returned' }
  return { mode: e.mode || e.arm, status: e.status, health_score: e.health_score, summary: e.summary || e.verdict, findings: (e.findings || []).length }
}
// Which modes completed COMPLETE in this stage (for the durable checkpoint). staleness tracked via flag.
function completedFrom(configs, results, includeStaleness) {
  const out = []
  if (includeStaleness) {
    // staleness is the first result when runStaleness was true; mark separately, not as a "mode".
  }
  for (let i = 0; i < results.length; i++) {
    const r = results[i]
    if (r && typeof r === 'object' && r.status === 'COMPLETE' && r.mode && r.mode !== 'staleness') out.push(r.mode)
  }
  return out
}
function blockedFrom(results) {
  const out = []
  for (const r of results) if (r && typeof r === 'object' && r.status === 'BLOCKED' && r.mode) out.push({ mode: r.mode, reason: r.blocked_reason || 'blocked' })
  return out
}
// Durable cross-session checkpoint (spec §3.2): a thin agent shells polish_state phase (control script has no fs).
async function checkpoint(phaseTag, { phase: ph, completedModes, blocked, staleness }) {
  const parts = [`--phase ${phaseTag === 'wave1' ? 'wave1' : phaseTag === 'wave2' ? 'wave2' : phaseTag === 'wave3' ? 'wave3' : 'explore'}`]
  if (completedModes && completedModes.length) parts.push(`--completed-modes ${completedModes.join(',')}`)
  if (blocked && blocked.length) parts.push(`--blocked '${JSON.stringify(blocked)}'`)
  if (staleness) parts.push(`--staleness ${staleness}`)
  await agent(
    `Durably advance the polish checkpoint (cross-session resume layer — spec §3.2). Execute exactly: ` +
    `\`node ${SKILL}/scripts/polish_state.mjs phase --root ${ROOT} --project ${PROJECT} ${parts.join(' ')}\` ` +
    `(resolve ${SKILL} to this skill dir). This overwrites polish-progress.md (not a ledger). Return {arm:"checkpoint", status:"completed", summary:"${phaseTag}"}.`,
    { model: 'haiku', schema: { type: 'object', additionalProperties: true, required: ['status'] }, label: `polish:checkpoint:${phaseTag}` }
  )
}
