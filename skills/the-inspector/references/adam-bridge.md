# Adam Bridge Reference — Live Integration Spec

> This reference maps the ADAM Framework's Functional Seriousness model to The Inspector's audit mission — use it to wire the two together if you run both.

---

## Adam's Architecture Summary (What We're Working With)

Adam is **The Review Agent** — a code review system built on three pillars:

1. **Experience Substrate (Pillar 1):** 55 scar tissue incidents across 6 categories (stability, maintainability, security, business-impact, client-perception, cross-cutting), retrieved via `scar-tissue/index.md` — max 3 loaded per session
2. **Reputation Score (Pillar 2):** Persistent self-evaluation log with confidence/vigilance signals, recency-weighted scoring, vigilance decay after 3 clean reviews
3. **Simulation Ceiling Awareness (Pillar 3):** 5 graduated ceiling markers (PATTERN-BASED → CORPUS MATCH → SIMULATION CEILING → LOW CONFIDENCE → HUMAN GATE) with density guidance (50-70% pattern-based, 15-30% corpus, 5-15% ceiling, 0-5% human gate)

Adam evaluates through **4 decision lenses** (strict priority): Stability & Reliability (40%) → Maintainability (30%) → Business Impact (20%) → Client Perception (10%).

Adam uses **5 severity levels**: BLOCKER → CRITICAL → MAJOR → MINOR → OBSERVATION

Adam always runs on **Opus**. No exceptions. The architecture collapses on smaller models.

---

## Mode Mapping: Adam-as-Reviewer vs Adam-as-Inspector

| Aspect | Adam Standalone (/review) | Adam as Inspector Engine |
|--------|---------------------------|--------------------------|
| **Scope** | One PR, one diff, one codebase review | Entire product audit across 3 layers |
| **Trigger** | /review [path] | "inspect this project" or an automated build gate |
| **Input** | Code diff or full codebase | Full codebase + spec/brief (if available) |
| **Output** | review-verdict.md | inspector-report.md + inspector-report.json |
| **Severity system** | BLOCKER/CRITICAL/MAJOR/MINOR/OBSERVATION | Maps to Inspector's 3-layer system (see below) |
| **Scar tissue** | Max 3 incidents loaded | Same — max 3, matched against entire codebase |
| **Reputation** | Appends to review-reputation.md | Appends to review-reputation.md with Mode: Inspector tag |
| **Ceiling markers** | Inline with findings | Mapped to Inspector's verification limits section |
| **Decision lenses** | Applied to the code | Applied per-layer: Stability maps to Security, Maintainability to Functionality, Business+Client to Polish |

---

## Severity Mapping: Adam → Inspector

Adam's severity system is richer than Inspector's per-layer classifications. Here's the explicit mapping:

### Layer 1: Security Surface
| Adam Severity | Inspector Severity | Notes |
|--------------|-------------------|-------|
| BLOCKER | CRITICAL | Exploitable now — auto-fix if possible |
| CRITICAL | CRITICAL | Exploitable with effort |
| MAJOR | HIGH | Defense-in-depth gap |
| MINOR | MEDIUM | Best practice deviation |
| OBSERVATION | LOW | Noted, not actionable |

### Layer 2: Functionality Completeness
| Adam Severity | Inspector Severity | Notes |
|--------------|-------------------|-------|
| BLOCKER | BROKEN | Feature crashes or produces wrong output |
| CRITICAL | BROKEN or INCOMPLETE | Depends on whether feature exists but fails vs partially works |
| MAJOR | INCOMPLETE or MISSING | Feature partially done or absent |
| MINOR | FRAGILE | Works but edge-case vulnerable |
| OBSERVATION | LOOSELY_COUPLED | May be intentional, needs confirmation |

### Layer 3: Production Polish
| Adam Severity | Inspector Severity | Notes |
|--------------|-------------------|-------|
| BLOCKER | REQUIRED_FOR_SHIP | (rare for polish — only if it blocks deployment) |
| CRITICAL | REQUIRED_FOR_SHIP | Missing README, no error page |
| MAJOR | SHOULD_HAVE | Expected by users |
| MINOR | NICE_TO_HAVE | Would elevate quality |
| OBSERVATION | FUTURE | Worth noting for v2 |

---

## Decision Lens → Inspector Layer Mapping

Adam's 4 lenses map naturally to The Inspector's 3 layers:

| Adam Lens | Weight | Inspector Layer | How It Applies |
|-----------|--------|----------------|---------------|
| Stability & Reliability (40%) | Primary | **Layer 1: Security** + **Layer 2: Functionality** | "Will this break?" drives security analysis and error handling checks |
| Maintainability (30%) | Secondary | **Layer 2: Functionality** | Code completeness, dead code, architecture assessment |
| Business Impact (20%) | Tertiary | **Layer 3: Polish** + **Layer 2: Functionality** | Deployment readiness, vendor lock-in, technical debt |
| Client Perception (10%) | Quaternary | **Layer 3: Polish** | UX, accessibility, documentation, professional appearance |

When Adam runs as Inspector engine, it applies all 4 lenses but routes findings to the appropriate Inspector layer based on this mapping.

---

## Scar Tissue → Scan Taxonomy Wiring

Each scar tissue category maps to specific scan-taxonomy.md sections. When Adam loads incidents, findings that match get the `adam_scar_tissue_match` field populated in JSON output.

| Scar Tissue Category | Files | Maps to Scan Taxonomy Sections |
|---------------------|-------|-------------------------------|
| **stability/** | 28 incidents | 1.3 (input validation), 2.1 (structural integrity), 2.3 (error handling), 2.4 (state management), 2.6 (data layer) |
| **maintainability/** | 11 incidents | 2.1 (structural integrity), 2.2 (code completeness), 2.7 (test coverage), 3.5 (developer experience) |
| **security/** | 6 incidents | 1.1 (secrets), 1.2 (auth), 1.3 (input validation), 1.4 (HTTP security), 1.5 (data exposure) |
| **business-impact/** | 5 incidents | 1.6 (dependencies), 3.6 (deployment readiness), 3.7 (legal/compliance) |
| **client-perception/** | 0 incidents (empty) | 3.2 (UX), 3.3 (accessibility), 3.4 (performance) |
| **cross-cutting/** | 5 incidents | Applies across all layers — organizational and process patterns |

### Security Hard Gates (from Adam's Scar Tissue + Vibe Coding Findings)

These are vulnerability patterns that Adam flags as automatic CRITICAL/BLOCKER. When Adam is the engine, these run as **mandatory pass/fail pre-checks** in Layer 1 before the regular scan taxonomy:

| Hard Gate | Adam Severity | Scan Taxonomy Item | Source |
|-----------|--------------|--------------------|--------------------|
| Hardcoded JWT secret | BLOCKER | ★ 1.1 JWT secrets | security/ incidents |
| SHA256 for password hashing | BLOCKER | ★ 1.2 Password hashing | security/ incidents |
| Non-expiring tokens | CRITICAL | ★ 1.2 Token expiration | security/ incidents |
| Missing rate limiting on auth | CRITICAL | 1.4 Rate limiting | security/ incidents |
| Missing cookie flags (HttpOnly, Secure, SameSite) | CRITICAL | 1.4 Cookie flags | security/ incidents |
| SQL string concatenation | BLOCKER | ★ 1.3 SQL parameterization | security/ incidents |
| Hardcoded API keys in source | BLOCKER | ★ 1.1 Hardcoded API keys | security/ incidents |

A hard gate failure is always **P1 priority** — it cannot be downgraded by context. These represent patterns Adam has "seen go wrong" (via scar tissue) and refuses to let pass.

---

## Ceiling Markers → Verification Limits Mapping

Adam's ceiling markers translate directly to The Inspector's verification limits section:

| Adam Marker | Inspector Equivalent | Report Behavior |
|-------------|---------------------|-----------------|
| PATTERN-BASED | Finding confidence: HIGH | Standard finding — no special note needed |
| CORPUS MATCH | Finding confidence: HIGH + `adam_scar_tissue_match` populated | Finding references specific incident in JSON |
| SIMULATION CEILING | Verification Limit entry | Listed in "Verification Limits" section with context |
| LOW CONFIDENCE | Finding confidence: LOW | Finding still listed but flagged with lower confidence |
| HUMAN GATE | Verification Limit entry (priority) | Listed with "HUMAN DECISION REQUIRED" emphasis |

### Density Check

After Adam completes analysis, before synthesis, check the marker distribution:
- If SIMULATION CEILING + HUMAN GATE exceeds 30% of total findings → Adam recalibrates before finalizing (per Adam's constitution)
- This prevents the report from being a "list of things I can't decide" — the human came for answers, not more questions

---

## Reputation Tracking in Inspector Mode

When Adam runs as Inspector engine, it still maintains its reputation log. Append format:

```markdown
---
### Review #[N] — [Project Name] (Inspector Mode) — [YYYY-MM-DD HH:MM]
**Mode:** Inspector [Fast Scan | Deep Audit]
**Verdict:** [SHIP_READY | CONDITIONAL | NOT_READY]
**Ship-Readiness Score:** [0-100]
**Self-Score:** [1-100]
**Confidence Signal:** [HIGH | MEDIUM | LOW] — [why]
**Vigilance Signal:** [HIGH | MEDIUM | LOW] — [areas of extra scrutiny]
**Key Uncertainty:** [what you weren't sure about]
**What You'd Improve:** [specific, not generic]
**Corpus Incidents Used:** [list with IDs or "none — pattern-based"]
**Human Feedback:** [leave blank — operator fills this in later]
---
```

Reputation is unified across both review and inspection modes. A miss in inspection mode raises vigilance for future reviews (and vice versa). There is one Adam, not a reviewer-Adam and an inspector-Adam.

---

## Integration Checklist

To fully activate Adam as The Inspector's engine:

- [ ] Verify scar-tissue/index.md exists and is populated with all 55 incidents
- [ ] Test index-based retrieval — give Adam a sample codebase, confirm it reads index first, selects 1-3 incidents, then reads only those files
- [ ] Test severity mapping — run Adam on a known-vulnerable codebase, verify BLOCKER→CRITICAL and MAJOR→HIGH mappings produce correct Inspector output
- [ ] Test hard gate enforcement — inject a hardcoded JWT secret, confirm it's always CRITICAL regardless of other context
- [ ] Test density check — review a codebase where most findings are novel (no corpus match), confirm Adam doesn't over-use SIMULATION CEILING
- [ ] Test report generation — confirm Adam's output is reformatted into Inspector's Markdown + JSON templates correctly
- [ ] Test reputation continuity — run two inspections, confirm the second loads reputation from the first
- [ ] Test the build-pipeline gate flow — run through a full pipeline, confirm the gate invokes Adam correctly and writes gate-verdict.md

---

## What Changes When Adam Is Active

| Component | Without Adam | With Adam |
|-----------|-------------|-----------|
| Analysis engine | Scan taxonomy checklists | Adam's 4-lens + scar tissue reasoning |
| Finding confidence | Checklist-based (binary: checked/not checked) | Graduated (pattern-based → corpus match → ceiling → human gate) |
| Security checks | Taxonomy items 1.1-1.7 | Hard gates (mandatory) + taxonomy (supplementary) |
| Report personality | Neutral, structured | Adam's tone: "direct, opinionated, respectful" |
| Self-evaluation | None | Appended to review-reputation.md every run |
| Severity reasoning | Rule-based mapping | Context-sensitive (Adam can elevate MEDIUM to CRITICAL when combined patterns warrant it) |
| "What's Good" section | Not included | Mandatory — Adam always calls out strong patterns and good decisions |

The biggest change: **Adam brings judgment where the checklist brings compliance.** Two MEDIUM findings that together create a CRITICAL exposure — the checklist can't see that. Adam can, because the scar tissue teaches cross-cutting pattern recognition.
