# Known Limitations

What The Inspector fundamentally cannot do. Be transparent about these with users to prevent over-trust in the verdict.

---

## Cannot Execute Code

The Inspector reads and reasons about source code — it does not compile, run, or execute anything. This means:
- It cannot verify that a build actually succeeds (only checks if build config exists)
- It cannot run tests (only checks if tests exist and if they look meaningful)
- It cannot confirm runtime behavior (a function may parse correctly but crash at runtime)
- It cannot detect bugs that only manifest under specific runtime conditions (race conditions, memory leaks under load, timezone-dependent logic)

**Mitigation:** Flag these as verification limits in every report.

## Cannot Test External Integrations

If a project calls a third-party API (Stripe, AWS, Firebase, etc.), The Inspector can check if the integration code looks correct but cannot verify:
- That API keys are valid
- That the API is responding
- That request/response shapes match the actual API (not just local types)
- That webhook handlers work end-to-end

**Mitigation:** Flag as "NEEDS_HUMAN_VERIFICATION: external integration" for each detected third-party dependency.

## Cannot Assess Actual Performance

The Inspector identifies performance *indicators* (bundle size, N+1 queries, missing indexes, no lazy loading) but cannot measure:
- Actual page load times
- API response latency
- Database query execution time
- Memory usage under load
- Concurrent user capacity

**Mitigation:** Report performance findings as "indicators" not "measurements." Recommend profiling tools.

## Cannot Review Binary Files

Images, compiled binaries, encrypted files, minified bundles (without source maps), and proprietary file formats are opaque. The Inspector skips them and logs the skip.

## Cannot Verify Authorization Logic Correctness

The Inspector can check that authorization checks exist on protected routes, but cannot verify that the logic is *correct*. Example: a route might check `if (user.role)` instead of `if (user.role === 'admin')` — The Inspector sees an auth check exists but can't reason about whether it's the right check for the right resource.

**Mitigation:** Flag auth logic as "EXISTS but correctness unverified" rather than "PASS."

## Cannot Detect Business Logic Bugs

If the specification says "discount should be 10% for orders over $100" and the code applies 10% for orders over $1000, The Inspector is unlikely to catch this unless the spec is machine-readable and the code is simple enough to trace. Business logic correctness generally requires human review or automated tests.

## Cannot Replace a Human Security Audit

The Inspector catches common vulnerability patterns (OWASP Top 10, hardcoded secrets, missing headers). It does NOT perform:
- Penetration testing
- Dynamic Application Security Testing (DAST)
- Threat modeling
- Social engineering assessment
- Infrastructure security review (server config, network, firewall)

For production systems handling sensitive data or financial transactions, a human security audit is still necessary.

## Context Window Constraints

For very large codebases (500+ source files), The Inspector uses sampling strategies and may not examine every file. The report will mark these cases with `SAMPLING_USED` and indicate which areas were not fully covered.

---

*When in doubt, The Inspector should flag something as a verification limit rather than silently assume it's fine. False negatives (missed real issues) are worse than false positives (flagged non-issues) for a safety-first tool.*
