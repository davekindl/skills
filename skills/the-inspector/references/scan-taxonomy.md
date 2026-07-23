# Scan Taxonomy Reference

Complete checklist for each analysis layer. Items marked [FAST] run in Fast Scan mode. All items run in Deep Audit mode.

Items marked with ★ are **highest-signal checks** — if time or context is constrained, prioritize these within each section. They catch the most common and most damaging issues.

---

## Section 1: Security Surface

### 1.1 Secrets & Credentials [FAST]
- [ ] ★ Hardcoded API keys, tokens, passwords in source files
- [ ] ★ `.env` files committed to source (check `.gitignore`)
- [ ] Private keys in repository
- [ ] ★ Database connection strings with credentials in source
- [ ] Third-party service credentials (Stripe, AWS, Firebase, etc.)
- [ ] ★ JWT secrets hardcoded (not from environment)
- [ ] Base64-encoded secrets (obfuscated but not secured)

**Detection method:** Regex scan for patterns: `key=`, `token=`, `password=`, `secret=`, `API_KEY`, `Bearer `, base64 strings > 20 chars adjacent to auth contexts. Check `.env*` files in git history if git is available.

### 1.2 Authentication & Authorization [FAST]
- [ ] ★ Auth implementation exists (or project doesn't need it — check brief)
- [ ] ★ Password hashing uses bcrypt/scrypt/argon2 (NOT MD5, SHA256, plaintext)
- [ ] Session tokens are cryptographically random
- [ ] ★ Token expiration is implemented (no eternal tokens)
- [ ] ★ Authorization checks on every protected route (not just frontend hiding)
- [ ] Role-based access is enforced server-side
- [ ] Password reset flow doesn't leak user existence
- [ ] OAuth state parameter used (if OAuth implemented)

**[ADAM SCAR TISSUE LINK]:** Vibe-coded projects commonly use SHA256 for passwords and non-expiring JWTs. These are CRITICAL findings.

### 1.3 Input Validation [FAST]
- [ ] ★ All user inputs validated server-side (not just client-side)
- [ ] ★ SQL queries parameterized (no string concatenation)
- [ ] ★ HTML output escaped (XSS prevention)
- [ ] File uploads validated (type, size, content inspection)
- [ ] URL parameters sanitized
- [ ] JSON payloads validated against schema
- [ ] Path traversal prevention on file operations

### 1.4 HTTP Security [DEEP ONLY]
- [ ] HTTPS enforced (or localhost-only appropriate for dev)
- [ ] Security headers present: `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Strict-Transport-Security`
- [ ] CORS configured restrictively (not `*` in production)
- [ ] Cookie flags: `HttpOnly`, `Secure`, `SameSite`
- [ ] CSRF tokens on state-changing requests
- [ ] Rate limiting on auth endpoints
- [ ] Rate limiting on API endpoints

**[ADAM SCAR TISSUE LINK]:** Missing cookie flags and absent rate limiting are top vibe-coding vulnerabilities.

### 1.5 Data Exposure [FAST]
- [ ] Error messages don't leak stack traces, DB schemas, or internal paths
- [ ] API responses don't include unneeded sensitive fields (password hashes, internal IDs)
- [ ] Logs don't contain passwords, tokens, or PII
- [ ] Debug mode is off in production config
- [ ] Source maps not shipped in production build

### 1.6 Dependencies [FAST]
- [ ] No known CVEs in direct dependencies (check `npm audit` / `pip audit` / `cargo audit` equivalent)
- [ ] Lock file exists and is committed (`package-lock.json`, `poetry.lock`, `Cargo.lock`)
- [ ] No wildcard version ranges in dependency specs
- [ ] Dependencies from trusted sources (no typosquatting indicators)

### 1.7 Advanced Security [DEEP ONLY]
- [ ] OWASP Top 10 mapping — which items are addressed, which are open
- [ ] Data flow analysis — where does user input travel? Does it ever reach unsafe sinks?
- [ ] Auth flow tracing — complete path from login to protected resource
- [ ] Cryptographic practices — proper key lengths, no deprecated algorithms
- [ ] Third-party script audit — what external scripts are loaded, what do they have access to?
- [ ] Supply chain indicators — are build scripts doing anything unexpected?

---

## Section 2: Functionality Completeness

### 2.1 Structural Integrity [FAST]
- [ ] ★ Every declared route has an implementation
- [ ] ★ Every import/require resolves to an existing file
- [ ] No orphan files (exist in tree but unreachable from entry points)
- [ ] ★ Entry point(s) exist and are correct (`main`, `index`, `app`, etc.)
- [ ] ★ Build succeeds without errors (if build tooling exists)
- [ ] No circular dependencies causing runtime issues

**Detection method:** Map declared routes (router config, file-based routing) against existing handler files. Trace import tree from entry point, flag unreached files. Differentiate between ORPHAN (zero references anywhere) and LOOSELY_COUPLED (not reachable from main entry but referenced elsewhere — secondary entry points, test helpers, optional modules).

### 2.2 Code Completeness [FAST]
- [ ] TODO/FIXME/HACK/XXX inventory (count, location, context)
- [ ] `console.log` / `print` / debug statements inventory
- [ ] Empty function bodies or placeholder returns
- [ ] Commented-out code blocks (what was disabled and why?)
- [ ] Hardcoded values that should be configurable (URLs, ports, limits)
- [ ] `throw new Error('not implemented')` or equivalent

### 2.3 Error Handling [FAST]
- [ ] ★ Global error handler exists (catch-all for unhandled exceptions)
- [ ] ★ API endpoints return proper error responses (not 500 for everything)
- [ ] ★ Frontend has error boundaries or equivalent
- [ ] Network failures handled gracefully (timeout, retry, fallback)
- [ ] Database operation errors caught and handled
- [ ] User-facing error messages are helpful (not raw stack traces)

### 2.4 State Management [DEEP ONLY]
- [ ] Loading states exist for async operations
- [ ] Error states exist for failed operations
- [ ] Empty states exist for zero-data scenarios
- [ ] Success/confirmation states for user actions
- [ ] Optimistic updates handled correctly (if used)
- [ ] State persistence across page refreshes (if needed)
- [ ] Race conditions in async flows identified

### 2.5 API Contract Fulfillment [DEEP ONLY]
- [ ] If API spec exists (OpenAPI, GraphQL schema): implementation matches spec
- [ ] Request validation matches documented schemas
- [ ] Response shapes match documented schemas
- [ ] Error codes match documentation
- [ ] Pagination implemented where documented
- [ ] Versioning consistent

### 2.6 Data Layer [DEEP ONLY]
- [ ] Schema migrations exist and are sequential
- [ ] Indexes on frequently queried columns
- [ ] Foreign key constraints defined
- [ ] No unused tables/columns (if schema documented in spec)
- [ ] Seed data exists for development
- [ ] Database queries are efficient (no N+1 patterns in obvious loops)
- [ ] Transactions used for multi-step writes

### 2.7 Test Coverage [FAST for existence, DEEP for quality]
- [ ] Test directory exists
- [ ] At least one test runs and passes
- [ ] Critical paths have tests (auth, core business logic, payment if applicable)
- [ ] [DEEP] Test quality — tests assert behavior, not just "doesn't crash"
- [ ] [DEEP] Edge cases covered in tests
- [ ] [DEEP] Test fixtures/mocks don't mask real bugs

---

## Section 3: Production Polish

### 3.1 Documentation [FAST]
- [ ] README exists with: purpose, setup instructions, usage
- [ ] API documentation exists (if API project)
- [ ] Environment variable documentation (`.env.example` or equivalent)
- [ ] Architecture decision records or design docs (for complex projects)
- [ ] [DEEP] Inline comments on non-obvious logic
- [ ] [DEEP] Changelog or release notes

### 3.2 UX Completeness [DEEP ONLY]
- [ ] Custom 404 page
- [ ] Favicon exists
- [ ] Meta tags (title, description, Open Graph)
- [ ] Responsive design (mobile breakpoints)
- [ ] Form validation feedback (inline errors, not just alerts)
- [ ] Navigation is consistent and complete
- [ ] Dark/light mode (if designed for it)
- [ ] Print stylesheet (if content-heavy)

### 3.3 Accessibility [DEEP ONLY]
- [ ] Semantic HTML elements used (`nav`, `main`, `section`, `article`, not div-soup)
- [ ] Images have alt text
- [ ] Form inputs have labels
- [ ] Keyboard navigation works for critical flows
- [ ] ARIA attributes on custom interactive elements
- [ ] Focus indicators visible
- [ ] Color is not the only information carrier
- [ ] Sufficient color contrast (check against WCAG AA)

### 3.4 Performance [DEEP ONLY]
- [ ] Images optimized (not raw 5MB PNGs)
- [ ] Lazy loading for below-fold content
- [ ] Bundle size reasonable (no entire lodash for one function)
- [ ] Caching headers configured
- [ ] Database queries have appropriate limits
- [ ] No memory leaks in obvious patterns (event listeners not cleaned up, intervals not cleared)
- [ ] Static assets served efficiently (CDN, compression)

### 3.5 Developer Experience [FAST]
- [ ] Setup instructions work (clone → install → run in < 5 min)
- [ ] `.env.example` exists with all required variables
- [ ] Linting configured (ESLint, Ruff, Clippy, etc.)
- [ ] Formatting configured (Prettier, Black, rustfmt, etc.)
- [ ] `.gitignore` covers common artifacts (node_modules, __pycache__, .env, build output)
- [ ] No committed build artifacts

### 3.6 Deployment Readiness [DEEP ONLY]
- [ ] Deployment config exists (Dockerfile, Vercel config, serverless.yml, etc.)
- [ ] Health check endpoint (if backend)
- [ ] Environment variable validation at startup (fail fast on missing config)
- [ ] Graceful shutdown handling
- [ ] CI/CD pipeline config exists
- [ ] Production build differs from development (minification, source maps, debug mode)
- [ ] Database migration strategy for production

### 3.7 Legal & Compliance [DEEP ONLY]
- [ ] LICENSE file present
- [ ] Third-party license compatibility checked
- [ ] Cookie consent (if web app in EU scope)
- [ ] Privacy policy link (if collects user data)
- [ ] Data deletion capability (if stores user data, GDPR relevant)
- [ ] Terms of service (if commercial product)

---

## Language-Specific Addons

These checks activate based on project fingerprint detection. They supplement, not replace, the core taxonomy.

### JavaScript / TypeScript
- [ ] TypeScript strict mode (if TS project) — or JSDoc types
- [ ] `package.json` has `engines` field
- [ ] Scripts defined: `start`, `build`, `test`, `lint`
- [ ] No `eval()` usage
- [ ] Proper `async/await` error handling (no unhandled promise rejections)

### Python
- [ ] Virtual environment documented/configured
- [ ] Type hints on public functions (if Python 3.6+)
- [ ] No `exec()` or `eval()` on user input
- [ ] WSGI/ASGI server configured (not `flask run` in production)
- [ ] `__init__.py` files present where needed

### Rust
- [ ] `unsafe` blocks documented with safety invariants
- [ ] `clippy` warnings addressed
- [ ] Error types defined (not just `unwrap()` everywhere)
- [ ] `Cargo.lock` committed (for binaries)

### Go
- [ ] Error returns checked (no `_ = someFunc()` on error returns)
- [ ] Context propagation for cancellation
- [ ] Goroutine leaks checked
- [ ] `go vet` clean

### General Backend
- [ ] Environment-based config (not hardcoded dev/prod URLs)
- [ ] Request logging middleware
- [ ] Graceful error responses (JSON, not HTML stack traces)
- [ ] Connection pooling for database
- [ ] Timeout configuration for external calls
