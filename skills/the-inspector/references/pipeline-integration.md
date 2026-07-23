# Build-Pipeline Integration — Final Inspection Gate

The Inspector can run as the final inspection gate in a multi-phase build pipeline — automatically after the build/launch phase completes. (Pairs with **The Polisher**, a sibling skill in this library; see the bottom of this file.)

---

## Pipeline Position

```
Phase 1: Discovery (Opus)
Phase 2: Architecture (Opus → Sonnet)
Phase 3: Implementation (Sonnet, parallel)
Phase 4: QA & Personas (Opus)
Phase 5: Launch (Mixed)
Phase 6: Inspection (Opus — The Inspector)  ← NEW
```

---

## Trigger Conditions

Phase 6 activates when:
1. Phase 5 is marked complete in `progress.md`
2. the pipeline orchestrator has not been configured to skip inspection (`skip_inspection: true` in CLAUDE.md)

Phase 6 is **optional but recommended**. your pipeline config should include:

```markdown
## Inspection
inspection: true          # Run The Inspector after Phase 5
inspection_gate: strict   # strict = block on CRITICAL/BROKEN, lenient = report only
```

---

## Phase 6 Behavior

### Auto-Configuration
When running as the final inspection gate, The Inspector:
- **Skips depth question** — always runs Deep Audit
- **Reads pipeline context automatically:**
  - `CLAUDE.md` — project constitution, tech stack decisions
  - `brief.md` — original product requirements
  - `progress.md` — what was built, by which agent, in which phase
  - `01-discovery/spec.md` — full product specification
  - `01-discovery/gap-analysis.md` — gaps already identified during discovery
  - `04-qa/issues.md` — issues found during QA phase
  - `04-qa/fix-log.md` — what was fixed during QA
- **Cross-references spec against implementation** — every endpoint, route, and component in `spec.md` should have a corresponding implementation. Missing items are MISSING findings.
- **Avoids duplicate findings** — if `04-qa/issues.md` already identified an issue AND `04-qa/fix-log.md` confirms it was fixed, don't re-flag it.

### Output Location

```
project/
├── 06-inspection/              ← NEW DIRECTORY
│   ├── inspector-report.md     # Full Markdown report
│   ├── inspector-report.json   # Machine-readable report
│   └── gate-verdict.md         # Pass/fail/conditional + summary
├── progress.md                 # Updated with Phase 6 completion
└── ...
```

### Gate Verdict Logic

**`inspection_gate: strict`** (default)
```
IF security CRITICAL > 0 OR functionality BROKEN > 0:
    verdict = FAIL
    action = "Phase 6 FAILED. Blockers listed below. Recommend Phase 4.5 fix sprint."
ELIF security HIGH > 3 OR functionality INCOMPLETE > 5:
    verdict = CONDITIONAL
    action = "Phase 6 CONDITIONAL PASS. Known issues documented. Ship at operator's discretion."
ELSE:
    verdict = PASS
    action = "Phase 6 PASSED. Product is ship-ready."
```

**`inspection_gate: lenient`**
```
# Always passes, but reports everything
verdict = PASS (with findings)
action = "Inspection complete. [N] findings documented. Review recommended before deployment."
```

### Gate Verdict File Format (`gate-verdict.md`)

```markdown
# Phase 6 Gate Verdict

**Verdict:** [PASS | CONDITIONAL | FAIL]
**Score:** [0-100]/100
**Gate Mode:** [strict | lenient]

## Summary
[One paragraph — what was found, what blocks shipping]

## Blockers (if FAIL)
| Finding ID | Title | Layer | Severity |
|-----------|-------|-------|----------|
| SEC-001   | ...   | Security | CRITICAL |

## Action Required
[What to do next — fix sprint, or ship with known issues, or ship clean]
```

### Progress.md Update

After Phase 6 completes, append to `progress.md`:

```markdown
## Phase 6: Inspection — [PASS/CONDITIONAL/FAIL]
- Scan mode: Deep Audit
- Findings: [N] total ([n] CRITICAL, [n] HIGH, [n] BROKEN, [n] INCOMPLETE)
- Score: [0-100]/100
- Full report: `06-inspection/inspector-report.md`
- Gate verdict: `06-inspection/gate-verdict.md`
- Completed: [timestamp]
```

---

## Pipeline Integration — Exact Changes

When integrating The Inspector into a multi-phase build pipeline, apply these changes:

### 1. `setup.sh` — Add to directory scaffolding

Find the `mkdir -p` block that creates the phase directories. Add after `05-launch/`:

```bash
# Add this line after the 05-launch directories:
mkdir -p 06-inspection
```

### 2. `references/templates.md` → CLAUDE.md Template

Find the CLAUDE.md template section. Add this block after the existing configuration:

```markdown
## Inspection
inspection: true          # Run The Inspector after Phase 5
inspection_gate: strict   # strict = block on CRITICAL/BROKEN, lenient = report only
```

### 3. `references/phase-details.md` — Add Phase 6

Add this section after Phase 5:

```markdown
---

## Phase 6: Inspection (Opus — The Inspector)

**Goal:** Verify the shipped product is safe, complete, and ready for deployment.

**Task 6.1 — Invoke The Inspector [Opus]:** Auto-detect pipeline context, run Deep Audit across all 3 layers (Security, Functionality, Polish), cross-reference `01-discovery/spec.md` against implementation. → `06-inspection/inspector-report.md`, `06-inspection/inspector-report.json`

**Task 6.2 — Gate Verdict [Opus]:** Apply gate logic based on `inspection_gate` setting in CLAUDE.md. Write verdict. → `06-inspection/gate-verdict.md`

**Task 6.3 — Update Progress [Opus]:** Append Phase 6 completion to `progress.md` with verdict, score, and finding counts.

**Acceptance Criteria:**
- Both report files exist in `06-inspection/`
- Gate verdict file exists with PASS/CONDITIONAL/FAIL
- progress.md updated with Phase 6 entry
- If gate = strict and verdict = FAIL: pipeline stops, blockers listed
```

### 4. Your pipeline orchestrator config — Update the pipeline overview

Find "## Step 3: The 5-Phase Pipeline (Overview)". Change heading to "The 6-Phase Pipeline" and add after Phase 5:

```markdown
**Phase 6 — Inspection (Opus — The Inspector):** Product readiness audit. Security surface scan, functionality completeness check, production polish assessment. Produces ship/no-ship verdict with prioritized remediation plan. Configurable gate: strict blocks on critical findings, lenient reports only.
```

### 5. `references/state-files.md` — Add gate-verdict.md format

Add this format definition:

```markdown
## gate-verdict.md

Location: `06-inspection/gate-verdict.md`
Written by: The Inspector (Phase 6)

### Format:
- **Verdict line**: `**Verdict:** PASS | CONDITIONAL | FAIL`
- **Score line**: `**Score:** [0-100]/100`
- **Gate Mode line**: `**Gate Mode:** strict | lenient`
- **Summary section**: One paragraph explaining what was found
- **Blockers table** (if FAIL): Finding ID, Title, Layer, Severity
- **Action Required section**: What to do next

### Behavior:
- Written once at Phase 6 completion
- Never modified after creation
- Read by the pipeline orchestrator to determine pipeline outcome
```

### Parallelization Map Update

Update the existing parallelization map to include Phase 6:

```
Phase 1: 1.1 → 1.2 → 1.3 → 1.4 → [1.5 ∥ 1.6] → 1.7
Phase 2: 2.1 → 2.2 → [2.3 ∥ 2.4 ∥ 2.5] → 2.6
Phase 3: [A ∥ B ∥ C ∥ D] → Integration
Phase 4: 4.1 → [4.2 ∥ 4.3] → 4.4 → 4.5 → 4.6
Phase 5: [5.1 ∥ 5.2 ∥ 5.3] → 5.4
Phase 6: 6.1 → 6.2 → 6.3
```

---

## Interaction with The Polisher

The Inspector and The Polisher serve different purposes:

| | The Polisher | The Inspector |
|---|---|---|
| **Scope** | Code quality across 12 dimensions | Product readiness across 3 layers |
| **Timing** | During development (after any build phase) | After all phases complete |
| **Focus** | "Is the code good?" | "Is the product shippable?" |
| **Output** | Polish report + health score | Remediation plan + ship verdict |
| **Workers** | 12 specialist agents in 3 waves | Single audit engine (Adam) |
| **Gate** | No formal gate — advisory | Formal pass/fail gate |

They can run in sequence: Polisher during Phase 4 (QA), Inspector as Phase 6 (final gate). The Inspector will detect if a Polisher report exists (`polish-report.md`) and factor its findings into the audit to avoid duplication.
