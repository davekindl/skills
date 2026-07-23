#!/usr/bin/env node
// polish-orchestrator v2 — Phase 2 synthesis (deterministic aggregation).
// Ports SKILL.md Phase 2 (L180-192): reads every polish/<mode>-report companion JSON
// (PolishWorkerReport schema, spec §1.4) and writes polish-report.md + polish-log.md.
//
// WHY a script: the Workflow control script has no fs, and synthesis must NOT re-scrape
// "STATUS: COMPLETE" out of transcripts (spec §2.2 — that dead text-scraping is replaced
// by the structured PolishWorkerReport.status field). The synthesizer AGENT shells this to
// produce the human report deterministically, then adds narrative prose around it.
//
// Inputs:  <root>/<project>/polish/<mode>-report.json  (one per completed worker)
//          <root>/<project>/polish/staleness-report.json (optional, wave0)
// Outputs: <root>/<project>/polish-report.md, polish-log.md
//          (and a machine summary printed to stdout for the synthesizer agent)
//
// Usage:
//   node synthesize.mjs --root <projects-root> --project <dir> [--verdict "..."] [--dry]
//   node synthesize.mjs --selftest

import fs from 'node:fs'
import path from 'node:path'
import os from 'node:os'

const SEV_ORDER = ['critical', 'high', 'medium', 'low']
const SEV_ICON = { critical: '\u{1F534}', high: '\u{1F7E0}', medium: '\u{1F7E1}', low: '\u{1F535}' }
const WAVE3 = new Set(['market', 'value', 'copy'])
// mode → wave, for the per-dimension link section ordering
const MODE_WAVE = {
  staleness: 0,
  errors: 1, deps: 1, security: 1, perf: 1, docs: 1, 'api-test': 1, compliance: 1,
  ux: 2, design: 2, journeys: 2, arch: 2, foundation: 2,
  market: 3, value: 3, copy: 3,
}

function parseArgs(argv) {
  const a = {}
  for (let i = 2; i < argv.length; i++) {
    const t = argv[i]
    if (t === '--selftest') a.selftest = true
    else if (t === '--dry') a.dry = true
    else if (t.startsWith('--')) { a[t.slice(2)] = argv[i + 1]; i++ }
  }
  return a
}

function projDir(root, project) {
  if (!project || project === '.') return root
  if (path.isAbsolute(project)) return project
  return path.join(root, project)
}

// Read every *-report.json under polish/. Fail-soft on a malformed file (record it, keep going).
function loadReports(polishDir) {
  const reports = []
  const errors = []
  let names = []
  // staleness-report.json is the Wave-0 companion, synthesized separately — exclude it here.
  try { names = fs.readdirSync(polishDir).filter((n) => /-report\.json$/.test(n) && n !== 'staleness-report.json') } catch { return { reports, errors } }
  for (const n of names.sort()) {
    const full = path.join(polishDir, n)
    try {
      const j = JSON.parse(fs.readFileSync(full, 'utf8'))
      if (!j.mode) j.mode = n.replace(/-report\.json$/, '')
      reports.push(j)
    } catch (e) {
      errors.push(`${n}: ${e.message}`)
    }
  }
  return { reports, errors }
}

// Overall health = mean of per-dimension health_score across COMPLETE reports (1 decimal).
// security/critical findings pull harder: if any critical finding is a recommendation (unfixed),
// cap the score at 6 (a real critical is unshippable). Mirrors the orchestrator's verdict intent.
function computeHealth(reports) {
  const complete = reports.filter((r) => r.status === 'COMPLETE' && typeof r.health_score === 'number')
  if (!complete.length) return { score: null, basis: 0 }
  const mean = complete.reduce((s, r) => s + r.health_score, 0) / complete.length
  let score = Math.round(mean * 10) / 10
  const unfixedCritical = reports.some((r) => (r.findings || []).some((f) => f.severity === 'critical' && f.fix_status !== 'auto-fixed'))
  if (unfixedCritical) score = Math.min(score, 6)
  return { score, basis: complete.length, capped_by_critical: unfixedCritical }
}

function severityCounts(reports) {
  const c = { critical: 0, high: 0, medium: 0, low: 0 }
  for (const r of reports) for (const f of r.findings || []) if (c[f.severity] != null) c[f.severity]++
  return c
}

function verdictLine(score, sev, blocked) {
  if (score == null) return 'INCONCLUSIVE — no completed worker reports to synthesize.'
  if (sev.critical > 0) return `NOT SHIP-READY — ${sev.critical} critical finding(s) must be resolved (health ${score}/10).`
  if (score >= 8.5) return `SHIP-READY — health ${score}/10, no criticals. ${blocked.length ? blocked.length + ' mode(s) blocked.' : ''}`.trim()
  if (score >= 7) return `SHIP-READY WITH FOLLOW-UPS — health ${score}/10; address high findings soon.`
  return `NEEDS WORK — health ${score}/10; ${sev.high} high finding(s) before ship.`
}

function buildReport({ project, reports, staleness }, nowISO) {
  const health = computeHealth(reports)
  const sev = severityCounts(reports)
  const complete = reports.filter((r) => r.status === 'COMPLETE')
  const blocked = reports.filter((r) => r.status === 'BLOCKED')
  const autoFixes = reports.flatMap((r) => (r.auto_fixes || []).map((f) => ({ ...f, mode: r.mode })))
  const needsHuman = reports.flatMap((r) => (r.findings || []).filter((f) => f.fix_status !== 'auto-fixed').map((f) => ({ ...f, mode: r.mode })))
  const wave3 = reports.filter((r) => WAVE3.has(r.mode))

  let md = `# Polish Report: ${project}\n\n`
  md += `**Generated:** ${nowISO}  \n`
  md += `**Health Score:** ${health.score == null ? 'N/A' : health.score + '/10'} (mean of ${health.basis} completed dimension${health.basis === 1 ? '' : 's'}${health.capped_by_critical ? ', capped by unresolved critical' : ''})  \n`
  md += `**Verdict:** ${verdictLine(health.score, sev, blocked)}\n\n`

  md += `## Findings by Severity\n\n| Severity | Count |\n|---|---|\n`
  for (const s of SEV_ORDER) md += `| ${SEV_ICON[s]} ${s[0].toUpperCase() + s.slice(1)} | ${sev[s]} |\n`
  md += `\n`

  if (staleness && staleness.findings) {
    const flagged = staleness.findings.filter((f) => f.category && f.category !== 'CURRENT')
    md += `## Dependency Freshness (Wave 0)\n\n`
    md += flagged.length
      ? flagged.map((f) => `- **${f.category}** \`${f.library}\` ${f.api ? '(' + f.api + ')' : ''} — installed ${f.installed_version || '?'} vs latest ${f.latest_stable || '?'}${f.new_name ? ' → use \`' + f.new_name + '\`' : ''} (${f.evidence || 'n/a'})`).join('\n') + '\n\n'
      : `No stale/deprecated APIs in use.\n\n`
  }

  md += `## What Was Auto-Fixed (${autoFixes.length})\n\n`
  if (autoFixes.length) {
    md += `| # | Mode | File | Line | Reason |\n|---|---|---|---|---|\n`
    autoFixes.forEach((f, i) => { md += `| ${i + 1} | ${f.mode} | \`${f.file || '?'}\` | ${f.line ?? ''} | ${oneLine(f.reason)} |\n` })
  } else md += `_No auto-fixes applied._\n`
  md += `\n`

  md += `## What Needs Human Attention (${needsHuman.length})\n\n`
  if (needsHuman.length) {
    const ordered = needsHuman.sort((a, b) => SEV_ORDER.indexOf(a.severity) - SEV_ORDER.indexOf(b.severity))
    for (const f of ordered) md += `- ${SEV_ICON[f.severity] || ''} **[${f.mode}]** ${oneLine(f.title)}${f.location ? ' — `' + f.location + '`' : ''}: ${oneLine(f.impact || f.detail || '')}\n`
  } else md += `_Nothing requires human decision._\n`
  md += `\n`

  if (wave3.length) {
    md += `## Strategic Insights (Wave 3)\n\n`
    for (const r of wave3) {
      const insights = (r.findings || []).map((f) => `- **[${r.mode}]** ${oneLine(f.title)}: ${oneLine(f.impact || f.detail || '')}`)
      md += insights.length ? insights.join('\n') + '\n' : `- **[${r.mode}]** ${oneLine(r.blocked_reason || 'no findings')}\n`
    }
    md += `\n`
  }

  md += `## Per-Dimension Reports\n\n`
  const ordered = reports.slice().sort((a, b) => (MODE_WAVE[a.mode] ?? 9) - (MODE_WAVE[b.mode] ?? 9) || a.mode.localeCompare(b.mode))
  md += `| Mode | Wave | Model | Status | Health | Findings | Report |\n|---|---|---|---|---|---|---|\n`
  for (const r of ordered) {
    const n = (r.findings || []).length
    md += `| ${r.mode} | ${MODE_WAVE[r.mode] ?? '?'} | ${r.model || '?'} | ${r.status} | ${r.health_score ?? ''} | ${n} | [${r.mode}-report.md](polish/${r.mode}-report.md) |\n`
  }
  md += `\n`

  if (blocked.length) {
    md += `## Blocked Modes\n\n`
    for (const r of blocked) md += `- **${r.mode}**: ${oneLine(r.blocked_reason || 'no reason given')}\n`
    md += `\n`
  }

  md += `---\n_Synthesized from ${reports.length} worker report(s): ${complete.length} complete, ${blocked.length} blocked._\n`
  return { md, health, sev, autoFixes, blocked, complete }
}

function buildLog({ project, autoFixes }, nowISO) {
  let md = `# Polish Log: ${project}\n\n**Generated:** ${nowISO}\n\nConsolidated auto-fix changes across all specialist workers.\n\n`
  if (!autoFixes.length) { md += `_No automated changes were applied this run._\n`; return md }
  const byFile = new Map()
  for (const f of autoFixes) { const k = f.file || '(unknown)'; if (!byFile.has(k)) byFile.set(k, []); byFile.get(k).push(f) }
  for (const [file, fixes] of [...byFile.entries()].sort()) {
    md += `### \`${file}\`\n\n`
    for (const f of fixes) {
      md += `- **[${f.mode}]** line ${f.line ?? '?'} — ${oneLine(f.reason)}\n`
      if (f.before || f.after) md += `  - \`${oneLine(f.before || '')}\` → \`${oneLine(f.after || '')}\`\n`
    }
    md += `\n`
  }
  md += `---\n_${autoFixes.length} change(s) across ${byFile.size} file(s)._\n`
  return md
}

const oneLine = (s) => String(s == null ? '' : s).replace(/\s+/g, ' ').replace(/\|/g, '\\|').trim().slice(0, 300)

function run({ root, project, verdict, dry }, nowISO) {
  const base = projDir(root, project)
  const polishDir = path.join(base, 'polish')
  const { reports, errors } = loadReports(polishDir)
  let staleness = null
  try { staleness = JSON.parse(fs.readFileSync(path.join(polishDir, 'staleness-report.json'), 'utf8')) } catch { /* optional */ }

  const built = buildReport({ project: project || path.basename(base), reports, staleness }, nowISO)
  if (verdict) built.md = built.md.replace(/\*\*Verdict:\*\* .*/, `**Verdict:** ${verdict}`)
  const log = buildLog({ project: project || path.basename(base), autoFixes: built.autoFixes }, nowISO)

  if (!dry) {
    fs.writeFileSync(path.join(base, 'polish-report.md'), built.md)
    fs.writeFileSync(path.join(base, 'polish-log.md'), log)
  }
  return {
    engine: 'polish-v2',
    project_dir: base.split(path.sep).join('/'),
    reports_loaded: reports.length,
    complete: built.complete.length,
    blocked: built.blocked.map((b) => b.mode),
    health_score: built.health.score,
    severity: built.sev,
    auto_fixes: built.autoFixes.length,
    load_errors: errors,
    wrote: dry ? [] : ['polish-report.md', 'polish-log.md'],
  }
}

// ---- self-test (spec §5.2 gate 7: output parity / synthesis fields) ----
function selftest() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'polish-synth-'))
  const assert = (c, m) => { if (!c) { console.error('FAIL:', m); process.exit(1) } }
  const base = path.join(tmp, 'proj')
  const polish = path.join(base, 'polish')
  fs.mkdirSync(polish, { recursive: true })

  // security: COMPLETE with one critical recommendation (unfixed) → must cap health at 6.
  fs.writeFileSync(path.join(polish, 'security-report.json'), JSON.stringify({
    mode: 'security', model: 'opus', status: 'COMPLETE', health_score: 9,
    findings: [{ severity: 'critical', title: 'SQLi in /login', location: 'api/login.ts:42', impact: 'auth bypass', fix_status: 'recommendation', detail: 'param interpolation' }],
    auto_fixes: [],
  }))
  // errors: COMPLETE, one high auto-fixed.
  fs.writeFileSync(path.join(polish, 'errors-report.json'), JSON.stringify({
    mode: 'errors', model: 'sonnet', status: 'COMPLETE', health_score: 8,
    findings: [{ severity: 'high', title: 'null deref', location: 'x.ts:5', impact: 'crash', fix_status: 'auto-fixed', detail: '' }],
    auto_fixes: [{ file: 'x.ts', line: 5, before: 'if(u)', after: 'if(u?.id)', reason: 'null guard' }],
  }))
  // market: Wave 3, COMPLETE, recommendation-only.
  fs.writeFileSync(path.join(polish, 'market-report.json'), JSON.stringify({
    mode: 'market', model: 'opus', status: 'COMPLETE', health_score: 7,
    findings: [{ severity: 'medium', title: 'weak differentiation', location: null, impact: 'hard to choose vs X', fix_status: 'recommendation', detail: '' }],
    auto_fixes: [],
  }))
  // deps: BLOCKED.
  fs.writeFileSync(path.join(polish, 'deps-report.json'), JSON.stringify({ mode: 'deps', model: 'sonnet', status: 'BLOCKED', blocked_reason: 'no lockfile', health_score: null, findings: [], auto_fixes: [] }))
  // malformed file → must fail-soft.
  fs.writeFileSync(path.join(polish, 'bad-report.json'), '{not json')
  // staleness optional companion.
  fs.writeFileSync(path.join(polish, 'staleness-report.json'), JSON.stringify({ findings: [{ library: 'react-router', installed_version: '5.0.0', latest_stable: '6.22.0', category: 'RENAMED', api: 'useHistory', new_name: 'useNavigate', used_in_code: true, evidence: 'App.tsx:12' }] }))

  const r = run({ root: tmp, project: 'proj' }, '2026-05-30T00:00:00Z')
  assert(r.reports_loaded === 4, 'loaded 4 valid reports (bad one fail-soft)')
  assert(r.load_errors.length === 1 && /bad-report/.test(r.load_errors[0]), 'malformed report recorded, not fatal')
  assert(r.complete === 3 && r.blocked.length === 1 && r.blocked[0] === 'deps', '3 complete, deps blocked')
  assert(r.health_score === 6, `health capped at 6 by unresolved critical (got ${r.health_score})`)
  assert(r.severity.critical === 1 && r.severity.high === 1 && r.severity.medium === 1, 'severity tally correct')
  assert(r.auto_fixes === 1, '1 auto-fix consolidated')

  const report = fs.readFileSync(path.join(base, 'polish-report.md'), 'utf8')
  assert(/NOT SHIP-READY/.test(report), 'verdict reflects critical → NOT SHIP-READY')
  assert(/Strategic Insights \(Wave 3\)/.test(report) && /weak differentiation/.test(report), 'wave3 strategic insights present')
  assert(/Dependency Freshness/.test(report) && /useNavigate/.test(report), 'staleness section + RENAMED finding rendered')
  assert(/\[security-report.md\]\(polish\/security-report.md\)/.test(report), 'per-dimension link present')
  assert(/Blocked Modes/.test(report) && /no lockfile/.test(report), 'blocked mode listed')
  const log = fs.readFileSync(path.join(base, 'polish-log.md'), 'utf8')
  assert(/`x.ts`/.test(log) && /null guard/.test(log), 'auto-fix log groups by file')

  // dry run does not write.
  fs.rmSync(path.join(base, 'polish-report.md'))
  const r2 = run({ root: tmp, project: 'proj', dry: true }, '2026-05-30T00:00:00Z')
  assert(!fs.existsSync(path.join(base, 'polish-report.md')) && r2.wrote.length === 0, '--dry writes nothing')

  // empty project → INCONCLUSIVE, no crash.
  const empty = path.join(tmp, 'empty'); fs.mkdirSync(path.join(empty, 'polish'), { recursive: true })
  const r3 = run({ root: tmp, project: 'empty' }, '2026-05-30T00:00:00Z')
  assert(r3.health_score === null && r3.reports_loaded === 0, 'empty project → null health, no crash')
  assert(/INCONCLUSIVE/.test(fs.readFileSync(path.join(empty, 'polish-report.md'), 'utf8')), 'empty → INCONCLUSIVE verdict')

  fs.rmSync(tmp, { recursive: true, force: true })
  console.log('synthesize selftest: PASS (aggregate, critical-cap, fail-soft, wave3, staleness, blocked, log-by-file, dry, empty)')
}

const args = parseArgs(process.argv)
if (args.selftest) {
  selftest()
} else {
  const root = args.root || process.cwd()
  if (!args.project) { console.error('need --project (or --selftest)'); process.exit(2) }
  const out = run({ root, project: args.project, verdict: args.verdict, dry: args.dry }, new Date().toISOString())
  console.log(JSON.stringify(out, null, 2))
}
