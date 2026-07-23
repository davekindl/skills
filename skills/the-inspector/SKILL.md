---
name: the-inspector
description: "Product readiness auditor that crawls any codebase, maps what exists, identifies gaps, incomplete code, vulnerabilities, and dead ends, then produces a prioritized remediation plan. Trigger this skill when the user says 'inspect this project', 'audit my code', 'what's broken', 'product readiness check', 'MVP audit', 'ship readiness', 'code health check', 'what did I miss', 'is this ready to ship', 'run the inspector', or any variation of wanting to assess a codebase's completeness and safety before shipping. Also trigger when the user mentions finding bugs, security review, gap analysis on existing code, post-build review, or wants to know what's unfinished in a project. Even casual mentions like 'look at this codebase' or 'what needs fixing' or 'how bad is it' should trigger this skill. When used as a final inspection gate in a multi-phase build pipeline, the pipeline orchestrator invokes this skill after the build completes."
---

# THE INSPECTOR — Product Readiness Auditor

**Version:** 0.2

> "Ship safe, then ship fast."

**Without The Inspector:** You built something overnight, it looks like it works, you ship it, and a week later you discover hardcoded secrets, missing auth on 3 endpoints, and a broken payment flow. **With The Inspector:** In 10-60 minutes you know exactly what's wrong, in what order to fix it, and how long each fix takes.

The Inspector crawls any codebase — language-agnostic, framework-agnostic — and produces a structured audit across three priority layers: Security, Functionality, and Polish. Output is always dual-format: a human-readable Markdown report and a machine-parseable JSON file.

## How to Invoke

The Inspector is a **Claude skill**, not a standalone CLI binary. It runs inside a Claude session (Claude Code or Claude.ai with computer use).

**In Claude Code (primary):**
- Natural language: "inspect this project", "audit my code", "is this ready to ship?"
- Claude reads this SKILL.md, follows the steps, and produces the reports in your project directory

**As a final inspection gate in a build pipeline (automatic):**
- Your build/pipeline orchestrator invokes The Inspector automatically after the build completes
- No user action needed — see the Build-Pipeline Integration section below

**Adam-Powered Mode (OPTIONAL):**
The Inspector can use the ADAM Framework's "Functional Seriousness" model as its analysis engine — an incident-derived scar-tissue corpus, a reputation system with vigilance decay, and security hard gates. If you maintain an ADAM-style knowledge base (see adam-bridge.md for the integration spec), point The Inspector at it at startup: the constitution file, reputation log, and scar-tissue index. If you do not, The Inspector still produces a full audit using the scan-taxonomy.md reference files included in this skill folder.

## Core Principles

1. **Security > Functionality > Polish** — always. A missing feature is a TODO; a missing auth check is a liability.
2. **No silent defaults** — always ask scan depth before running. Never assume.
3. **Language-agnostic** — the scan taxonomy works on any codebase. Language-specific checks are additive layers, not gates. After detecting the project language, activate the appropriate language-specific checks:

   | Generic Check | Python | Node/TS | Go | Rust | Java |
   |---------------|--------|---------|-----|------|------|
   | Secret in source | `grep` for API key patterns | `.env` not in `.gitignore` | hardcoded in `const` | hardcoded in `static` | in `application.properties` |
   | SQL injection | f-strings in queries, raw SQL | string concat in queries | `fmt.Sprintf` in SQL | raw SQL strings | string concat in JDBC |
   | Dependency vulns | `pip-audit` / `safety` | `npm audit` / `snyk` | `govulncheck` | `cargo audit` | `mvn dependency-check` |
   | Auth pattern | `Depends()` decorators | middleware chains | middleware handlers | extractors/guards | `@PreAuthorize` |
   | Test framework | `pytest` | `jest`/`vitest` | `go test` | `cargo test` | `JUnit`/`TestNG` |
   | Async issues | blocking in async loop | unhandled promise rejections | goroutine leaks | `tokio` blocking | thread pool exhaustion |

   The report MUST note which language-specific checks were activated and why.
4. **Honest limits** — when The Inspector can't verify something (runtime behavior, third-party API responses, load performance), it flags it as `NEEDS_HUMAN_VERIFICATION` rather than guessing. These "verification limits" are listed explicitly in every report.
5. **Adam-powered** — The Inspector uses Adam as its analysis engine. Adam's scar tissue corpus provides experience-backed judgment, security hard gates enforce mandatory pass/fail checks, and ceiling markers flag where human judgment is required. Reputation is tracked across both review and inspection modes.

## Gotchas (from production runs)

- **Line counts in reports have been wrong before.** A review pass once caught the Inspector reporting 791 lines when the actual file was 620 lines. Always verify metric claims against the filesystem — never trust a subagent's summary without disk verification.
- **"Research complete" claims need file-existence verification in the same session.** A subagent may claim a deliverable was written when the file doesn't exist.
- **RENDER generated HTML page-by-page before presenting.** Structural checks aren't enough — footer overflow, page breaks, duplicated elements only show up in visual render. Re-render after any find-replace.
- **Single validation can rubber-stamp a wrong stat.** Every client-facing stat/claim needs BOTH validation AND adversarial cross-check. A published figure once read 63% when the real number was 22% — one validation layer accepted it, the adversarial cross-check caught it.
- **First formal evolution has the biggest gains (+58 first run, +6 second).** Don't expect diminishing returns to mean zero returns — the second pass still catches real issues.
- **Code-reviewer subagent after multi-agent runs** — always run one. Multi-agent output has more integration seams than single-agent output.

---

## Step 0: Pre-Flight

When triggered, ALWAYS do these things before scanning:

### 0.1 — Ask Scan Configuration
Do not default. Present TWO choices:

**Scope:** Full Scan (all 3 layers) or Targeted Scan (pick layers)?
- If Targeted: let the user select which layers to run. Security always runs first if selected alongside other layers.
- If only one layer is selected, skip the others entirely but still produce a full report for that layer.

**Depth:** Fast Scan or Deep Audit?
Do not default. Present the choice:

**Fast Scan** (~5-10 min)
- Directory structure mapping
- Security surface (hardcoded secrets, auth patterns, input validation)
- Critical functionality gaps (dead routes, orphan files, TODO/FIXME/HACK count)
- Dependency health (outdated, vulnerable, unused)
- Quick production readiness (missing README, no error handling patterns, no tests directory)

**Deep Audit** (~30-60 min)
- Everything in Fast, plus:
- File-by-file analysis of all source files
- Complete UX/product gaps (empty states, loading states, error states, 404, responsive)
- Full security surface (OWASP Top 10 mapping, auth flow tracing, data flow analysis)
- Code hygiene (dead code, unused imports, inconsistent patterns, type safety)
- Dependency chain analysis (transitive vulnerabilities, license conflicts)
- Architecture assessment (separation of concerns, coupling, scalability indicators)
- Production infrastructure (CI/CD, logging, monitoring, health checks, env validation)
- Accessibility baseline (semantic HTML, ARIA, keyboard navigation, contrast indicators)

**xhigh Audit** (~60-120 min, Opus / maximum-reasoning runs only)
- Everything in Deep Audit, plus:
- Invoke with `thinking: {type: "adaptive"}` at Opus's maximum reasoning allocation
- Compound-chain analysis: trace how 3+ individually-minor findings combine into a single BLOCKER (e.g., weak auth + verbose errors + unpatched dep → full chain)
- Adversarial framing: for each BLOCKER, enumerate at least 2 attacker personas (external exploiter, insider, AI-using script kiddie) and how each would exploit it
- Root-cause clustering: group findings by shared root cause (e.g., "10 findings all trace to missing input validation layer")
- Migration-path audit: if target uses Claude SDK, run current-model capability-diff checks — flag retired model IDs, deprecated `temperature`/`top_p` combinations, manual prefill where structured output is now preferred, and hand-rolled thinking-budget knobs that the adaptive-thinking models manage automatically. (If a versioned capability-diff doc is available on the host, ground the check against it; otherwise apply these checks from first principles.)
- Used by: an automated final-gate step when the build spec flags `ship_readiness: xhigh` OR when ADAM `/deep-review --xhigh` is invoked. Also recommended for pre-grant-submission audits, pre-compliance-deadline audits (e.g. EU AI Act), and any audit where a missed finding triggers legal/financial liability.

**Default when unspecified:** Fast Scan. Never auto-escalate to Deep or xhigh without explicit scope/depth selection.

### 0.2 — Detect Project Type
Before scanning, run a project fingerprint:
1. Read the root directory structure (2 levels deep)
2. Check for: `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, `Gemfile`, `composer.json`, `*.csproj`, `mix.exs`, `pubspec.yaml`, `CLAUDE.md`, `progress.md`
3. Identify: language(s), framework(s), package manager(s), test framework(s), build tool(s)
4. Check for build-pipeline signatures: phase directories (e.g. `01-discovery/`, `02-architecture/`), a `brief.md`-style spec, a `progress.md` log
5. Log the fingerprint — it informs which language-specific checks to activate

### 0.3 — Establish Baseline Context
Read (if they exist):
- `README.md` — stated purpose, setup instructions
- `CLAUDE.md` — project constitution (especially if pipeline-built)
- `brief.md` — original product brief
- `progress.md` — what was supposed to be built vs what was built
- `.env.example` or `.env.template` — expected configuration
- `package.json` / `requirements.txt` etc. — declared dependencies

**False Positive Suppression Protocol:**

After reading context files, build an **Acknowledged Scope** list:

1. **Out-of-scope features** — If `brief.md` or `CLAUDE.md` explicitly lists features as "out of scope", "not for MVP", "v2", or "deferred", do NOT flag their absence as MISSING. Instead, mark them `ACKNOWLEDGED_OUT_OF_SCOPE` in the report with a reference to the source document.

2. **Intentional architecture choices** — If `CLAUDE.md` documents a decision (e.g., "no tests for prototypes", "SQLite for dev only"), do not flag it as a gap. Note it as `ACKNOWLEDGED_BY_DESIGN` with the rationale.

3. **Known issues** — If `progress.md` lists known bugs or incomplete items, still report them but cross-reference: "Also tracked in progress.md" to avoid treating them as newly discovered.

4. **Stage-appropriate expectations** — If the project is explicitly labeled as "prototype", "hackathon", "internal tool", or "MVP", adjust severity for polish items: `REQUIRED_FOR_SHIP` may become `SHOULD_HAVE` for a prototype. Security findings are NEVER downgraded regardless of project stage.

5. **When no context files exist** — Note in the report: "No brief.md, CLAUDE.md, or progress.md found. All findings are reported without scope filtering. Some may be intentional omissions." This prevents silent false positive assumptions.

### 0.4 — Assess Codebase Size & Plan Scan Strategy

After fingerprinting, count source files (excluding `node_modules`, `vendor`, `__pycache__`, `.git`, build output).

| Tier | Source Files | Strategy | Estimated Time (Deep) |
|------|-------------|----------|----------------------|
| **Small** | < 50 | Single-pass: read all files, analyze holistically | 15-30 min |
| **Medium** | 50-200 | Chunked by directory: analyze per-module, then synthesize | 30-60 min |
| **Large** | 200-500 | Sampling: full scan on critical paths (auth, API, entry points), statistical sampling on the rest. Flag `SAMPLING_USED` in report. | 60-90 min |
| **Massive** | 500+ | Flag to user: "This codebase exceeds single-session analysis. Recommend splitting into subsystems or focusing on specific modules." Offer to run targeted scan on a subset. | Variable |

For Fast Scan, all tiers can be processed in a single pass since Fast only checks high-signal items.

---

## Step 0.5: Deterministic Pre-Scan (Phase A.5 -- runs BEFORE the LLM judgment phase)

**Why this step exists:** The Inspector's LLM phase used to burn context re-deriving facts that a `grep`/AST pass could establish in 50ms. The pre-scan script `run-prescan.py` is a Python-stdlib-only deterministic scanner that fires 35 rules across 5 layers (SEC, ARCH, TEST, AI, PROMPT). The LLM phase MUST consume its output instead of re-deriving findings.

This step is mandatory for **every** Inspector run except `--skip-prescan` (rare; only when the script is unavailable on the host machine). When skipped, log it explicitly in Scan Health under `Pre-Scan: SKIPPED ([reason])` so the report's provenance stays honest.

### 0.5.1 -- Locate the script

The pre-scan script is `run-prescan.py`. To find it:

1. Check for a local pre-scan script: `$INSPECTOR_HOME/scripts/run-prescan.py` (env var) or `the-inspector/scripts/run-prescan.py` in your own tooling checkout
3. If not found, log `Pre-Scan: SKIPPED (script not found at expected paths)` in Scan Health and continue with the LLM-only fallback. Do NOT abort -- the Inspector still produces a report; it just loses the deterministic layer.

### 0.5.2 -- Run the script

Invoke from the target codebase root (not from your tooling directory):

```bash
python <ADAM>/the-inspector/scripts/run-prescan.py <target-root> \
    --output <target-root>/inspector-prescan-findings.json \
    --rules SEC,ARCH,TEST,AI,PROMPT
```

Add `--include-build` ONLY when the audit explicitly covers `dist/`/`build/`/`out/`/`.next/` (required for ARCH-PR-007 -- hardcoded localhost in deployable artifacts). Default: skip those dirs (faster, fewer false positives on minified code).

**Exit codes:**
- `0` -- scan completed (any finding count is fine; findings live in the JSON)
- `2` -- hard error (target is not a directory, malformed args). On exit-2, log `Pre-Scan: FAILED (exit 2)` and proceed with LLM-only fallback.

### 0.5.3 -- Load and parse the output

Read `inspector-prescan-findings.json` from the target root. Schema (full spec in `the-inspector/references/deterministic-prescan-rules.md`):

```json
{
  "schema_version": "1.0",
  "spec_version": "1.0",
  "script_version": "1.0.0",
  "scan_root": "<absolute path>",
  "layers_run": ["AI", "ARCH", "PROMPT", "SEC", "TEST"],
  "include_build": false,
  "files_scanned": 47,
  "findings_count": 12,
  "findings_by_severity": {"BLOCKER": 2, "CRITICAL": 4, "MAJOR": 5, "MINOR": 1},
  "findings_by_rule": {"SEC-PR-001": 1, "ARCH-PR-005": 3, "...": "..."},
  "findings": [
    {
      "rule_id": "SEC-PR-001",
      "file": "src/api/openai.py",
      "line": 42,
      "matched_text": "API_KEY = 'sk-proj-aBc...redacted-sha8:1f2e3d4c'",
      "severity": "BLOCKER",
      "scar_tissue_refs": ["SCAR-SEC-001", "SCAR-SEC-019"],
      "auto_fixable": false,
      "human_gate": false,
      "notes": "Hardcoded API key. Rotate the secret AND wire a secret store."
    }
  ],
  "llm_phase_instructions": "Add the findings VERBATIM..."
}
```

**Validation before consuming:**
1. `schema_version` MUST start with `"1."` -- incompatible-major versions abort with `Pre-Scan: SCHEMA_MISMATCH (got X, want 1.x)`
2. `findings` MUST be a list (defensive -- empty is fine, missing means corruption)
3. Each finding MUST have `rule_id`, `file`, `line`, `severity`. Skip findings missing any of these and log under Scan Health (`Pre-Scan: 1 malformed finding skipped`).

If validation fails, fall back to LLM-only mode and log it. Do NOT crash the Inspector.

### 0.5.4 -- Convert pre-scan findings to Inspector finding IDs

Pre-scan rule severities map to Inspector severities:

| Pre-scan severity | Inspector severity | Notes |
|---|---|---|
| `BLOCKER` | `CRITICAL` | Maps to `inspector-report.json` severity field |
| `CRITICAL` | `HIGH` | |
| `MAJOR` | `MEDIUM` | |
| `MINOR` | `LOW` | |
| `ESCALATE_TO_HUMAN_GATE` | `HIGH` + `human_gate: true` flag | Per CLAUDE.md crypto rule (SEC-PR-007). Never auto-fix. |

Pre-scan rule layers map to Inspector layers:

| Pre-scan layer | Inspector layer |
|---|---|
| `SEC` | `security` |
| `ARCH`, `AI` | `functionality` |
| `TEST` | `functionality` |
| `PROMPT` | `security` (prompt injection IS a security category per OWASP A03) |

Inspector finding IDs follow the existing convention: `SEC-001`, `FUNC-001`, `POL-001` (zero-padded, sequential per layer). Pre-scan findings get IDs first (they're confirmed by regex/AST), then LLM findings extend the sequence.

**Auto-fix policy for pre-scan findings:**
- `auto_fixable: true` AND severity <= MAJOR AND no human_gate flag -> eligible for auto-fix in CONDITIONAL_PASS mode
- `human_gate: true` -> NEVER auto-fix; flag `HUMAN GATE` per ADAM CLAUDE.md
- All others -> flag-only

### 0.5.5 -- Emit the verbatim block in the report

After Step 4.1 generates the Markdown report, the **first** Findings section MUST be:

```markdown
## Pre-Scan Findings (deterministic)

These findings come from `inspector-prescan-findings.json` produced by
`run-prescan.py` v<script_version> against spec v<spec_version>. They are
confirmed by regex/AST -- no LLM judgment required. Confidence: HIGH (the rule
either matched or it didn't; no false-confidence risk).

**Coverage:** <files_scanned> files scanned, <findings_count> findings, layers
run: <layers_run>, include_build: <include_build>.

| ID | Rule | Severity | File:Line | Matched | Scar Tissue | Auto-fixable | Human Gate |
|---|---|---|---|---|---|---|---|
| SEC-001 | SEC-PR-001 (Hardcoded API key) | CRITICAL | src/api/openai.py:42 | `API_KEY = 'sk-proj-aBc...'` | SCAR-SEC-001, SCAR-SEC-019 | no | no |
| ... | ... | ... | ... | ... | ... | ... | ... |

**LLM phase instruction (do not delete):** These findings are pre-confirmed.
Do NOT re-derive them in the judgment phase. Spend LLM context on the
AMBIGUOUS layer that pre-scan can't catch -- design intent, business context,
integration risk -- and on HUMAN GATE escalations (especially SEC-PR-007
crypto code).
```

### 0.5.6 -- Confidence calibration

Tag pre-scan findings with `DETERMINISTIC` (a sixth ceiling marker, distinct from `PATTERN-BASED`). The distinction matters in self-evaluation: a `DETERMINISTIC` finding cannot be wrong about whether the pattern is present (only about whether the pattern is harmful in this codebase). LLM-only findings retain `PATTERN-BASED` / `CORPUS MATCH`.

### 0.5.7 -- Update Scan Health

Add a `Pre-Scan` line to the Scan Health block (Section 4):

```
- Pre-Scan: COMPLETE (script v1.0.0, spec v1.0, 35 rules, <X> fired)
- Pre-Scan Layers: SEC=<n>, ARCH=<n>, TEST=<n>, AI=<n>, PROMPT=<n>
- Pre-Scan Coverage: <files_scanned> source files, <findings_count> findings
```

If the pre-scan was skipped or failed, replace `COMPLETE` with `SKIPPED ([reason])` or `FAILED (exit <N>: [reason])`. Inspector readers (auditors, compliance reviewers) need to see this line to trust the report's provenance.

---

## Resilience & Error Recovery

The Inspector must handle real-world scanning failures gracefully.

**Context window pressure:** If the analysis is approaching context limits, stop the current layer, write a partial report with findings so far, mark remaining items as `NOT_SCANNED`, and note the reason. A partial report is always better than no report.

**Unreadable files:** Binary files, encoded files, minified bundles, and files with permission errors should be skipped and logged in the report's verification limits section. Never crash on a file read failure.

**Partial failure recovery:** If a layer completes but the next layer fails, the completed layer's findings are still valid and should be included in the final report. Each layer is independent — a Layer 2 failure doesn't invalidate Layer 1 findings.

**State tracking:** For Deep Audits on Medium+ codebases, write a lightweight `inspector-progress.md` tracking which directories/files have been scanned. If the session is interrupted, a resumed scan can pick up where it left off rather than starting from scratch.

**Mandatory Scan Health section in every report:** The report MUST always include a "Scan Health" section immediately after the Executive Summary, showing:

```
SCAN HEALTH
- Status: COMPLETE | PARTIAL (with reason) | ABORTED (with reason)
- Files Scanned: [n] / [total] ([percentage]%)
- Files Skipped: [n] — [reasons: binary, permission_denied, too_large, encoding_error]
- Directories Scanned: [list]
- Context Window Pressure: [yes/no] — if yes: [which layer was interrupted, findings captured before interruption]
- Scan Strategy: [single-pass / chunked / sampling] — [tier reasoning]
- Recovery State: FRESH_SCAN | RESUMED_FROM [inspector-progress.md timestamp]
- Layer Completion: L1-Security [COMPLETE/PARTIAL] | L2-Functionality [COMPLETE/PARTIAL] | L3-Polish [COMPLETE/PARTIAL]
```

This section MUST appear even when everything is nominal (all files scanned, no pressure, no skips). A clean scan health report IS the evidence that resilience was tested and passed.

---

## Step 1: Security Surface (Layer 1 — Always First)

Read `references/scan-taxonomy.md` → Section 1 for the complete checklist.

**Priority:** CRITICAL and HIGH findings here block all other layers from producing a "ship-ready" verdict.

Key areas (mapped to OWASP Top 10 2021):
- **A01 Broken Access Control** — missing auth on endpoints, IDOR, CORS misconfiguration, privilege escalation
- **A02 Cryptographic Failures** — hardcoded secrets, weak hashing, missing encryption at rest/transit
- **A03 Injection** — SQL injection, command injection, XSS, SSRF, template injection
- **A04 Insecure Design** — missing rate limiting, no abuse-case controls, missing anti-automation
- **A05 Security Misconfiguration** — default secrets, debug mode in prod, overly permissive headers
- **A06 Vulnerable Components** — outdated dependencies, known CVEs, unpinned versions
- **A07 Auth Failures** — weak password policy, credential stuffing surface, session fixation
- **A08 Data Integrity Failures** — unsigned updates, missing webhook signature verification, CI/CD gaps
- **A09 Logging Failures** — missing audit logs, no security event tracking, insufficient monitoring
- **A10 SSRF** — unvalidated URLs in server-side requests, redirect manipulation

*(OWASP Top 10:2025 is now final — A02 is Security Misconfiguration, new categories: Software Supply Chain Failures, Mishandling of Exceptional Conditions; mapping update pending.)*

The report MUST include an **OWASP Coverage Matrix** showing which OWASP categories have findings, which are clear, and which couldn't be assessed:
```
| OWASP Category | Status | Finding IDs |
|A01 Broken Access Control | FINDINGS | SEC-002, SEC-003 |
|A02 Cryptographic Failures | FINDINGS | SEC-001 |
|A03 Injection | FINDINGS | SEC-004 |
|A04 Insecure Design | FINDINGS | SEC-006 |
|A05 Security Misconfiguration | FINDINGS | SEC-005, SEC-007 |
|A06 Vulnerable Components | FINDINGS | SEC-013, SEC-014 |
|A07 Auth Failures | FINDINGS | SEC-008 |
|A08 Data Integrity Failures | NOT_ASSESSED | (requires runtime verification) |
|A09 Logging Failures | FINDINGS | POL-005 |
|A10 SSRF | CLEAR | No SSRF vectors detected |
```

**[ADAM INTEGRATION POINT]**: Adam's scar tissue corpus contains real-world vulnerability patterns from vibe-coded projects. When Adam is wired in, this layer uses his security hard gates as mandatory pass/fail checks. Until then, use the checklist in scan-taxonomy.md.

### BaaS Security (Firebase / Supabase / Appwrite)

**Firebase:**
- Check `firebase.json` and `firestore.rules` for `allow read, write: if true;`
- Check Realtime Database rules for `".read": true, ".write": true`
- Verify auth is required for all write operations
- Check for `firebaseConfig` exposed in client-side code without server-side enforcement
- Severity: BLOCKER if public read/write rules detected

**Supabase:**
- Check for `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` on all tables
- Verify RLS policies exist for all tables with user data
- Check for `.rpc()` calls that bypass RLS
- Verify `anon` key usage has RLS enforced
- Severity: BLOCKER if RLS disabled on user-data tables

### MCP / Agent Tool Security

- Check for auto-approval of tool calls without user confirmation
- Verify tool descriptions don't contain injection payloads (tool poisoning -- 84.2% success rate)
- Check for ToolPoison patterns: tool descriptions that instruct the LLM to ignore user instructions
- Verify MCP server inputs are validated (30+ CVEs in first 60 days of 2026)
- Check for SSRF vectors in any tool that accepts URLs
- Severity: BLOCKER if auto-approval + external tool access detected

### Dependency Health

- Run `npm audit` / `pip audit` / equivalent and parse output
- Flag packages with <1000 weekly downloads (slopsquatting risk)
- Flag packages with names similar to popular packages (typosquatting)
- Check for hallucinated package names (package exists in import but not in package.json/requirements.txt)
- Severity: CRITICAL for known CVEs, MAJOR for low-download packages

### Severity Classification (Calibration Rubric)

Use this decision tree — if ANY condition in a severity level matches, classify at that level:

**CRITICAL** — Exploitable now, data loss or unauthorized access possible
- Hardcoded secrets/API keys in source (not .env)
- SQL injection, command injection, or SSRF with user-controlled input
- Authentication bypass (endpoints with no auth that should have it)
- Unvalidated file upload allowing arbitrary file types to be saved/executed
- Default/weak credentials that ship in production config
- *Test: "Can an attacker exploit this in under 1 hour with no insider knowledge?"* → If yes, CRITICAL

**HIGH** — Exploitable with moderate effort, or exposes significant attack surface
- Missing rate limiting on auth endpoints (brute force possible)
- Wildcard CORS on apps handling sensitive data (payments, PII)
- Weak random number generation for security tokens (`random` instead of `secrets`)
- Sensitive data in error responses (stack traces, DB schemas in production)
- Missing authorization on non-critical endpoints (data exposure without financial impact)
- *Test: "Does this require specific conditions or multi-step exploitation?"* → If yes and impact is significant, HIGH

**MEDIUM** — Defense-in-depth gap, not immediately exploitable alone
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Unpinned dependencies (supply chain risk, not an active exploit)
- Missing CSRF protection (when JWT-based auth partially mitigates)
- Overly permissive cloud resource ACLs (S3 public-read on private data)
- No dependency vulnerability scanning configured
- *Test: "Is this a missing layer of defense rather than a direct vulnerability?"* → If yes, MEDIUM

**LOW** — Best practice deviation, no direct threat
- Missing security-related linting rules
- No signed commits or branch protection
- Verbose logging that could theoretically leak info but doesn't in current config
- *Test: "Would a security auditor note this but not flag it as a finding?"* → If yes, LOW

### Finding Confidence Level

Every finding MUST include a confidence indicator:

- **HIGH** — The Inspector directly observed the issue in source code (e.g., saw the hardcoded key, read the f-string SQL query, confirmed the missing auth decorator). Specific file:line references provided.
- **MEDIUM** — The Inspector inferred the issue from patterns but couldn't fully confirm (e.g., "this pattern suggests X but the actual behavior depends on runtime configuration"). May require human verification.
- **LOW** — The Inspector suspects the issue based on absence of evidence (e.g., "no rate limiting middleware detected" — but it might be handled by an API gateway or reverse proxy not visible in the codebase). These findings MUST include a `NEEDS_VERIFICATION` tag.

In the report output, format as: `Confidence: HIGH — observed directly in source`

In the JSON, add: `"confidence": "HIGH|MEDIUM|LOW"` and `"confidence_reason": "explanation"`

This prevents false positives by making uncertainty visible. A finding with LOW confidence is a flag for human review, not a definitive judgment.

### Ship-Readiness Score Formula

The ship-readiness score (0-100) MUST be computed using this formula, not guessed:

```
risk_weight = { CRITICAL: 15, HIGH: 8, MEDIUM: 3, LOW: 1 }
confidence_multiplier = { HIGH: 1.0, MEDIUM: 0.7, LOW: 0.4 }

total_risk = sum(risk_weight[f.severity] * confidence_multiplier[f.confidence] for f in findings)

# Absolute scale: each risk point reduces ship-readiness
# Calibration: a typical NO-SHIP project scores 25-40, a clean project scores 85-100
ship_readiness = max(0, round(100 - total_risk * 0.42))
```

Include the formula breakdown in the Metrics section so the score is auditable.

In the JSON, add: `"risk_score": number` per finding (= risk_weight × confidence_multiplier) and `"ship_readiness_formula": { "total_risk": N, "max_risk": N, "score": N }`

---

## Step 2: Functionality Completeness (Layer 2)

Read `references/scan-taxonomy.md` → Section 2.

This layer maps what the codebase claims to do vs what it actually does.

Key areas:
- Route/endpoint mapping — declared vs implemented
- Dead code and orphan files (exists but unreachable)
- TODO/FIXME/HACK inventory with context
- Error handling coverage (try/catch, error boundaries, fallback UI)
- State management completeness (loading, error, empty, success states)
- API contract fulfillment (if spec exists: do endpoints match?)
- Database schema vs actual queries (unused columns, missing indexes)
- Test coverage assessment (existence and basic quality, not line-by-line)
- Build/run verification (does `npm start` / `python main.py` / etc. actually work?)

### Gap Classification
- **BROKEN**: Feature exists but crashes or produces wrong output
- **INCOMPLETE**: Feature partially implemented, dead ends
- **MISSING**: Expected feature absent entirely
- **ORPHAN**: Code exists with zero references anywhere in the project — no imports, no dynamic references, no test coverage
- **LOOSELY_COUPLED**: Code exists but not reachable from the main entry point — may be a secondary entry point, utility, optional module, or test helper. Confidence: MEDIUM (needs human confirmation)
- **FRAGILE**: Works but will break under edge cases

### Browser QA Mode (when available)

If the project has a running dev server or the user provides a URL:

1. **Detect dev server**: check `package.json` scripts for `start`/`dev`, or `docker-compose.yml` services
2. **Start the dev server** if not already running
3. **Register handlers first**: set up a dialog handler (`browser_handle_dialog`) before any navigation to auto-dismiss alerts/confirms and log them — unhandled dialogs block the entire QA pass
4. **Navigate every route** and for each page:
   - Use `browser_snapshot` (accessibility tree) as the **primary observation** — it's deterministic, token-efficient, and reveals semantic issues (missing labels, broken ARIA roles, unnamed buttons). Use `browser_take_screenshot` as visual supplement, not primary.
   - After page load, call `browser_console_messages` — flag any errors or unhandled promise rejections
   - After page load, call `browser_network_requests` — flag any 4xx/5xx responses, mixed content, or CORS failures
   - Interactive elements respond to clicks
   - Navigation between pages works
   - No broken images or missing assets (check both snapshot and network requests for failed resource loads)
   - Test hover states on navigation menus and elements with `title` attributes using `browser_hover` — dropdowns, tooltips, and hover cards are invisible without this
   - After link clicks, check `browser_tabs` for unexpected new tabs — flag `target="_blank"` links that break navigation flow
5. **Form validation depth** — for each form found, test three scenarios:
   - (a) Submit empty — verify required-field validation appears
   - (b) Submit with valid data — verify success feedback
   - (c) Submit with one boundary input (max-length string or special characters) — verify no crash
6. **Responsive viewport sweep**: resize the browser and re-check each key page at 3 breakpoints:
   - Mobile: 375x667
   - Tablet: 768x1024
   - Desktop: 1280x800 (or default)
   - Check for: layout breakage, horizontal overflow/scrollbar issues, unreachable interactive elements, text truncation
   - Screenshot each breakpoint (save to `inspector-screenshots/`)
7. **Screenshot archive**: save all screenshots (per-page + per-breakpoint) to `inspector-screenshots/`
8. **Generate regression test stubs** in Playwright format:
   ```typescript
   // Generated by Inspector Browser QA
   test('[page-name] loads clean', async ({ page }) => {
     const errors: string[] = [];
     const failedRequests: string[] = [];
     page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
     page.on('requestfailed', req => failedRequests.push(`${req.method()} ${req.url()}`));

     await page.goto('[url]');
     await page.waitForLoadState('networkidle');

     expect(errors).toHaveLength(0);
     expect(failedRequests).toHaveLength(0);
   });

   test('[page-name] responsive — mobile', async ({ page }) => {
     await page.setViewportSize({ width: 375, height: 667 });
     await page.goto('[url]');
     await expect(page.locator('body')).toBeVisible();
     // No horizontal overflow
     const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
     const clientWidth = await page.evaluate(() => document.documentElement.clientWidth);
     expect(scrollWidth).toBeLessThanOrEqual(clientWidth + 5);
   });
   ```

**Playwright availability check:** Before attempting browser QA, check for the Playwright MCP tools (e.g., `browser_navigate`, `browser_snapshot`). If using CLI mode, run:
```bash
npx playwright --version 2>/dev/null
```
If Playwright is not available in either form, emit this in the Inspector report:
```
[BROWSER_QA_SKIPPED: no browser tooling detected — install Playwright for automated visual testing]
```
Do NOT silently omit browser QA. The skip must be visible in the report.

Browser QA is **additive** — the existing scan-based audit always runs first. Browser QA runs after if tooling is available. Default to headless mode for speed; use headed mode only when the user requests visual observation.

---

## Step 3: Production Polish (Layer 3)

Read `references/scan-taxonomy.md` → Section 3.

This layer only matters if Layers 1 and 2 are passing. It's the "would a user trust this product?" layer.

Key areas:
- Documentation quality (README, API docs, inline comments)
- UX completeness (404 page, favicon, meta tags, responsive, empty states)
- Accessibility baseline (semantic HTML, alt text, keyboard nav, ARIA)
- Performance indicators (bundle size, image optimization, lazy loading, caching headers)
- Developer experience (setup instructions, env.example, linting config, git hygiene)
- Deployment readiness (Dockerfile, CI/CD config, health check endpoint, env validation)
- Internationalization readiness (hardcoded strings, locale handling)
- Legal/compliance (LICENSE file, cookie consent if web, privacy policy link)

### Polish Classification
- **REQUIRED_FOR_SHIP**: Blocks professional deployment (no README, no error page)
- **SHOULD_HAVE**: Expected by users/devs but not blocking
- **NICE_TO_HAVE**: Would elevate quality but fine without for MVP
- **FUTURE**: Worth noting for v2, not relevant now

---

## Step 3.5: Production Gap Analysis (NEW -- vibecoding research finding)

After completing the 3-layer scan, calculate the Production Gap Score. This measures what's MISSING for production readiness, not what exists.

**22-Item Production Gap Checklist:**

| # | Item | Category | Check |
|---|------|----------|-------|
| 1 | Environment variables for all hosts/ports/URLs | Deployment | No hardcoded localhost |
| 2 | Error handling on all external calls | Stability | try/catch or .catch() |
| 3 | Input validation on all user inputs | Security | Zod/Joi/manual validation |
| 4 | Authentication on all protected routes | Security | Middleware or guards |
| 5 | CSRF protection | Security | Token or SameSite cookies |
| 6 | Security headers (CSP, X-Frame, HSTS) | Security | Helmet or manual |
| 7 | Rate limiting | Security | Per-route or global |
| 8 | CORS configuration (not wildcard) | Security | Specific origins only |
| 9 | Logging (structured, not console.log) | Operations | Pino/Winston/structured |
| 10 | Error tracking (Sentry or equivalent) | Operations | Wired and reporting |
| 11 | Health check endpoint | Operations | GET /health or /api/health |
| 12 | 404 page | UX | Custom, not framework default |
| 13 | Loading states for async operations | UX | Skeleton/spinner/placeholder |
| 14 | Error states for failed requests | UX | User-facing error messages |
| 15 | Empty states for zero-data views | UX | Not blank, not broken |
| 16 | Responsive design (mobile) | UX | Viewport meta + breakpoints |
| 17 | Tests exist (any framework) | Quality | At least 1 test file |
| 18 | Build succeeds (no errors) | Quality | npm run build exits 0 |
| 19 | No secrets in source code | Security | No API keys, passwords |
| 20 | Dependencies up to date (no critical CVEs) | Security | npm audit / pip audit |
| 21 | README with setup instructions | Documentation | Can a stranger run this? |
| 22 | Deployment configuration exists | Deployment | Dockerfile/wrangler.toml/vercel.json |

**Scoring:**
- Count items present -> Production Gap Score = (items_present / 22) x 100%
- Include in Inspector report as: `Production Gap: XX% (N/22 items present)`
- Items 1-8 (Security) missing -> auto-escalate to CRITICAL finding
- Score < 50% -> flag `WARNING -- SIMULATION CEILING: "This project has significant production gaps. Shipping in this state will expose users to preventable risks."`

**Output format:**
```
Production Readiness: 45% (10/22)
Missing: error handling (3), deployment config (2), monitoring (2), rate limiting (2), CI/CD (2), edge cases (1)
```

This score appears in both the Markdown report summary and the JSON output under `production_gap_score`.

---

## Step 4: Synthesis & Report Generation

After all layers complete, generate both output files.

### 4.1 — Markdown Report
Read `references/output-templates.md` → Markdown Template for the exact structure.

Key sections:
1. **Executive Summary** — one paragraph, ship/no-ship verdict, critical count
2. **Project Fingerprint** — language, framework, detected patterns, baseline context
3. **Pre-Scan Findings (deterministic)** — emitted from `inspector-prescan-findings.json` per Step 0.5.5. Comes BEFORE the layer findings so readers see the high-confidence regex/AST matches first. Tag every entry with `DETERMINISTIC`. If pre-scan was skipped, omit this section but log `Pre-Scan: SKIPPED` in Scan Health.
4. **Findings by Layer** — Security → Functionality → Polish, each with severity-sorted items. For CRITICAL and HIGH severity findings, include a **before/after code example** showing the vulnerable pattern and the fixed version. Keep examples concise (3-8 lines each). Example:
   ```
   # BEFORE (vulnerable):
   query = f"SELECT * FROM invoices WHERE status = '{user_input}'"

   # AFTER (fixed):
   query = text("SELECT * FROM invoices WHERE status = :status")
   result = session.execute(query, {"status": user_input})
   ```
4. **Cross-Cutting Concerns** — After findings, before remediation. Identify 3-5 systemic patterns that span multiple findings and layers:
   - Example: "Input validation is missing systemically — affects SEC-003 (file upload), SEC-004 (SQL), FUNC-006 (status transitions), POL-003 (error responses)"
   - Example: "Observability gap — SEC-009 (error details), POL-005 (no logging), POL-009 (no monitoring) create a blind spot where exploits and failures are invisible"
   - For each pattern: describe the systemic risk and the single architectural fix that addresses multiple findings
5. **Remediation Plan** — prioritized list with effort estimates (S/M/L), grouped into sprints
6. **Verification Limits** — things The Inspector can't verify (needs human/runtime testing)
7. **Metrics** — total findings by severity, estimated remediation time, ship-readiness score (computed by formula)

### 4.2 — JSON Report

The JSON report MUST include ALL findings — never truncate. Every finding from the Markdown report must appear in the JSON `findings` array. Use this schema:

```json
{
  "inspector_version": "string",
  "scan_date": "ISO-8601",
  "scan_mode": "fast | deep",
  "scan_scope": "full | targeted",
  "layers_scanned": ["security", "functionality", "polish"],
  "project": {
    "name": "string",
    "language": "string",
    "framework": "string",
    "source_files": "number",
    "test_files": "number",
    "test_coverage_pct": "number",
    "codebase_tier": "small | medium | large | massive"
  },
  "verdict": "SHIP | NO_SHIP | CONDITIONAL",
  "ship_readiness_score": "0-100",
  "gate": {
    "result": "PASS | FAIL | CONDITIONAL_PASS",
    "blockers": ["finding IDs that block shipping"],
    "conditions": ["finding IDs that are known issues if CONDITIONAL"]
  },
  "findings_summary": {
    "total": "number",
    "by_severity": { "CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0 },
    "by_layer": { "security": 0, "functionality": 0, "polish": 0 }
  },
  "findings": [
    {
      "id": "SEC-001",
      "layer": "security | functionality | polish",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "classification": "e.g. BROKEN | INCOMPLETE | ORPHAN | REQUIRED_FOR_SHIP",
      "title": "string",
      "location": "file:line or 'Global'",
      "finding": "description",
      "impact": "what goes wrong",
      "fix": "how to fix it",
      "effort": "S | M | L",
      "effort_hours": "estimated range"
    }
  ],
  "remediation_sprints": [
    {
      "name": "Sprint 1: Security Critical",
      "days": "1-2",
      "finding_ids": ["SEC-001", "SEC-004"]
    }
  ],
  "verification_limits": [
    {
      "item": "string",
      "reason": "why it can't be verified statically",
      "recommendation": "what to do instead"
    }
  ],
  "scan_metadata": {
    "files_scanned": "number",
    "files_skipped": "number",
    "skipped_reasons": ["binary", "permission_denied", "too_large"],
    "context_pressure": "boolean",
    "partial_scan": "boolean"
  },
  "prescan": {
    "status": "COMPLETE | SKIPPED | FAILED",
    "script_version": "string (e.g. 1.0.0)",
    "spec_version": "string (e.g. 1.0)",
    "files_scanned": "number",
    "findings_count": "number",
    "findings_by_severity": {"BLOCKER": 0, "CRITICAL": 0, "MAJOR": 0, "MINOR": 0, "ESCALATE_TO_HUMAN_GATE": 0},
    "findings_by_rule": {"SEC-PR-001": 0, "...": 0},
    "rule_ids_fired": ["SEC-PR-001", "..."],
    "skipped_reason": "string | null",
    "include_build": "boolean"
  }
}
```

This JSON is the data contract for trend tracking across audits and automated build-gate logic. The `gate` object enables automated pass/fail decisions. The `prescan` object captures deterministic-pass provenance -- `status: SKIPPED` is honest signal, not a defect.

### 4.3 — Save Outputs
- Save to project root: `inspector-report.md` and `inspector-report.json`
- If running as a build-pipeline gate: save to `06-inspection/` directory
- Always present both files to the user via `SendUserFile`

**⚠️ Report Handling Warning:** After generating the report, always remind the user:
> "This report contains security-sensitive findings including vulnerability locations and attack surface details. Do not commit to public repositories or share on unencrypted channels. Consider adding `inspector-report.*` to your `.gitignore`."

---

## Build-Pipeline Integration

When invoked by a build pipeline after the build completes:

1. **Auto-detect build-pipeline context** — read `progress.md`, `brief.md`, `CLAUDE.md` if present
2. **Skip the depth question** — the automated gate always runs Deep Audit
3. **Cross-reference the spec** — compare `01-discovery/spec.md` against implementation
4. **Gate logic:**
   - 0 CRITICAL security findings AND 0 BROKEN functionality → **PASS** (ship-ready)
   - Any CRITICAL or BROKEN → **FAIL** (list blockers, suggest Phase 4.5 fix sprint)
   - Only HIGH/MEDIUM → **CONDITIONAL PASS** (ship with known issues documented)
5. **Write Phase 6 completion** to `progress.md` with verdict and summary
6. **Output to `06-inspection/`** — both report files plus a `gate-verdict.md`

---

## Model Routing

- **Opus** for: security analysis, architecture assessment, gap reasoning, synthesis, severity classification, remediation prioritization
- **Sonnet** for: file scanning, dependency checking, pattern matching, TODO counting, structure mapping, dead code detection

When Adam is integrated, Adam runs on Opus and IS the analysis engine. The Inspector skill becomes the orchestration wrapper.

---

## Reference Files

| File | Read When |
|------|-----------|
| `references/scan-taxonomy.md` | Always — during Steps 1, 2, and 3 |
| `references/output-templates.md` | During Step 4 — report generation |
| `references/example-report.md` | First time running The Inspector — calibrates tone, detail, and finding quality |
| `references/pipeline-integration.md` | When running as a build-pipeline gate |
| `references/known-limitations.md` | When setting expectations — what The Inspector fundamentally cannot do |
| `references/positioning.md` | When explaining The Inspector's value vs existing tools (SonarQube, Snyk, etc.) |
| `references/adam-bridge.md` | When Adam is wired in — maps Adam's constitution to Inspector's mission. Severity mapping, hard gates, ceiling markers, reputation tracking. |
| `run-prescan.py` (optional local tooling — `the-inspector/scripts/`) | The actual pre-scan executable. Invoked at Step 0.5.2. Self-test via `--self-test`. |

---

## What The Inspector Is NOT

- **Not a linter** — it doesn't enforce style rules. It finds product-level problems.
- **Not a test runner** — it doesn't execute tests. It checks if tests exist and if coverage is reasonable.
- **Not a deployment tool** — it checks if deployment is possible, not performs it.
- **Not a replacement for change-level review** — the ADAM Framework (Part Two of the Code Review Bible) reviews code changes (PRs, commits). The Inspector audits entire products. Same brain, different scope.
