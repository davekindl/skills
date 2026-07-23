# Inspector Report — TaskFlow (Example)

**Scan Date:** 2026-03-09T14:30:00Z
**Scan Mode:** Fast Scan
**Verdict:** NOT READY
**Ship-Readiness Score:** 38/100

---

## Executive Summary

TaskFlow is a Next.js task management app with Express backend and SQLite database. The codebase has 2 CRITICAL security findings (hardcoded JWT secret and missing auth on API routes), 3 BROKEN functionality items (incomplete delete flow, crash on empty state, missing error handler), and no deployment configuration. The single most important fix is the hardcoded JWT secret in `backend/auth.js` — this is exploitable immediately. Score: 38/100, NOT READY.

---

## Project Fingerprint

| Attribute | Value |
|-----------|-------|
| Language(s) | JavaScript, TypeScript |
| Framework(s) | Next.js 14, Express 4.18 |
| Package Manager | npm |
| Test Framework | None found |
| Build Tool | Next.js built-in |
| Pipeline-Built | No |
| Lines of Code (est.) | ~2,400 |
| File Count | 34 |
| Dependency Count | 28 |

**Baseline Context:** README states "A simple task manager with user accounts, task CRUD, and team sharing." No brief or spec exists.

---

## Layer 1: Security Surface

### CRITICAL

- **[SEC-001] Hardcoded JWT Secret**
  Location: `backend/auth.js:12`
  Description: JWT signing secret is hardcoded as `"super_secret_key_123"`. Anyone reading the source can forge valid auth tokens and impersonate any user.
  Remediation: Move to environment variable `JWT_SECRET`, generate a cryptographically random 256-bit key, add to `.env.example`.
  Effort: S

- **[SEC-002] Missing Auth Middleware on Task API Routes**
  Location: `backend/routes/tasks.js:1-45`
  Description: The `/api/tasks` endpoints (GET, POST, PUT, DELETE) have no authentication middleware. Any unauthenticated request can read, create, modify, or delete any user's tasks.
  Remediation: Add `requireAuth` middleware to all task routes. The middleware exists in `backend/auth.js` but is only applied to `/api/users/profile`.
  Effort: S

### HIGH

- **[SEC-003] No Rate Limiting on Login Endpoint**
  Location: `backend/routes/auth.js:15`
  Description: The `/api/auth/login` endpoint has no rate limiting. Brute-force attacks are trivial.
  Remediation: Add `express-rate-limit` middleware. Suggested: 5 attempts per IP per 15 minutes on auth endpoints.
  Effort: S

### MEDIUM

- **[SEC-004] Error Messages Leak Stack Traces**
  Location: `backend/app.js:48`
  Description: The global error handler sends `err.stack` in the response body. In production, this exposes internal file paths, dependency versions, and code structure to attackers.
  Remediation: Conditionally include stack trace only when `NODE_ENV !== 'production'`.
  Effort: S

**Layer 1 Summary:** 2 CRITICAL, 1 HIGH, 1 MEDIUM, 0 LOW

---

## Layer 2: Functionality Completeness

### BROKEN

- **[FUNC-001] Task Delete Returns 500**
  Location: `backend/routes/tasks.js:38`
  Description: The DELETE endpoint calls `db.run('DELETE FROM tasks WHERE id = ?', req.params.id)` but doesn't handle the case where `req.params.id` is undefined. Sending `DELETE /api/tasks/undefined` crashes the server.
  Remediation: Add parameter validation. Return 400 if `id` is missing or non-numeric.
  Effort: S

- **[FUNC-002] Empty State Crashes Frontend**
  Location: `frontend/components/TaskList.tsx:22`
  Description: `tasks.map(...)` is called without checking if `tasks` is null/undefined. When the API returns an error or the user has no tasks, the page crashes with "Cannot read properties of undefined."
  Remediation: Add null check: `(tasks ?? []).map(...)` and add an empty state UI component.
  Effort: S

- **[FUNC-003] Team Sharing Not Implemented**
  Location: `frontend/pages/share.tsx`
  Description: The share page exists but contains only `<p>Coming soon</p>`. The README claims "team sharing" as a feature. This is a broken promise — the feature is advertised but not built.
  Remediation: Either implement team sharing or remove it from README and navigation.
  Effort: L (if implementing) / S (if removing)

### INCOMPLETE

- **[FUNC-004] User Registration Missing Email Verification**
  Location: `backend/routes/auth.js:28`
  Description: Users can register with any email without verification. No confirmation email is sent. This allows fake account creation and makes password reset unreliable.
  Remediation: Add email verification flow or at minimum validate email format server-side.
  Effort: M

**Layer 2 Summary:** 3 BROKEN, 1 INCOMPLETE, 0 MISSING, 0 ORPHAN, 0 FRAGILE

**TODO/FIXME/HACK Inventory:**
| Marker | Count | Most Critical Location |
|--------|-------|----------------------|
| TODO   | 7     | `backend/routes/tasks.js:30` — "TODO: add pagination" |
| FIXME  | 2     | `frontend/components/TaskForm.tsx:15` — "FIXME: date picker broken on Safari" |
| HACK   | 1     | `backend/db.js:8` — "HACK: hardcoded DB path" |

---

## Layer 3: Production Polish

*Layer 3 skipped in Fast Scan mode — Security and Functionality findings are sufficient to determine NOT READY verdict.*

---

## Remediation Plan

### Sprint 1: Blockers (Estimated: 2 hours)

| # | Finding ID | Title | Layer | Severity | Effort |
|---|-----------|-------|-------|----------|--------|
| 1 | SEC-001 | Hardcoded JWT secret | Security | CRITICAL | S |
| 2 | SEC-002 | Missing auth on task routes | Security | CRITICAL | S |
| 3 | FUNC-001 | Task delete crashes | Functionality | BROKEN | S |
| 4 | FUNC-002 | Empty state crashes frontend | Functionality | BROKEN | S |
| 5 | FUNC-003 | Team sharing not implemented | Functionality | BROKEN | S-L |

### Sprint 2: High Priority (Estimated: 1.5 hours)

| # | Finding ID | Title | Layer | Severity | Effort |
|---|-----------|-------|-------|----------|--------|
| 6 | SEC-003 | No rate limiting on login | Security | HIGH | S |
| 7 | SEC-004 | Stack traces in error responses | Security | MEDIUM | S |
| 8 | FUNC-004 | No email verification | Functionality | INCOMPLETE | M |

---

## Verification Limits

- [ ] [LIMIT-001] Cannot verify SQLite database integrity or query performance — would need runtime testing with realistic data volumes
- [ ] [LIMIT-002] Cannot verify Next.js SSR behavior — client/server rendering split may produce hydration mismatches not visible in source
- [ ] [LIMIT-003] Cannot verify email delivery — if email verification is implemented, SMTP configuration needs manual testing

---

## Metrics Summary

| Metric | Value |
|--------|-------|
| Total Findings | 8 |
| Security: CRITICAL | 2 |
| Security: HIGH | 1 |
| Functionality: BROKEN | 3 |
| Functionality: INCOMPLETE | 1 |
| Polish: REQUIRED_FOR_SHIP | (not scanned — Fast mode) |
| Estimated Total Remediation | 3.5 hours |
| Ship-Readiness Score | 38/100 |
| Verdict | NOT READY |

---

*Generated by The Inspector v0.2 — 2026-03-09T14:30:00Z*
*Analysis Engine: Checklist-only | Scan workers: Sonnet*

---

> **Note:** This is a fictional example report included for calibration purposes. It demonstrates the expected tone (direct, specific, actionable), detail level (file:line locations, concrete remediation steps), and structure for Inspector reports.
