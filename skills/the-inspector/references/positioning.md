# Positioning Reference

How The Inspector compares to existing code analysis tools. Use this when a user or client asks "why not just use SonarQube / Snyk / CodeClimate?"

---

## The Short Answer

Most tools answer: "Is the code correct?"
The Inspector answers: "Is the *product* ready to ship?"

That's a different question. Code can pass every linter and still be missing a 404 page, a logout flow, error states, deploy config, and a README. The Inspector catches the product-level gaps that code-level tools don't look for.

---

## Comparison Matrix

| Capability | The Inspector | SonarQube | Snyk | CodeClimate | Semgrep |
|-----------|:---:|:---:|:---:|:---:|:---:|
| Security vulnerability patterns | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Dependency CVE scanning | ✅ (checklist) | ⚠️ | ✅ (best) | ⚠️ | ❌ |
| Code quality / smell detection | ⚠️ (high-level) | ✅ (best) | ❌ | ✅ | ⚠️ |
| **Product completeness audit** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **UX/UI gap detection** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Deployment readiness check** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Documentation audit** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Accessibility baseline** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Spec-vs-implementation cross-reference** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Prioritized remediation plan** | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| **Ship/no-ship verdict** | ✅ | ❌ | ❌ | ❌ | ❌ |
| Run without setup/config | ✅ | ❌ | ⚠️ | ❌ | ⚠️ |
| Language-agnostic | ✅ | ⚠️ | ✅ | ⚠️ | ⚠️ |
| Continuous monitoring / CI integration | ❌ | ✅ | ✅ | ✅ | ✅ |
| SAST (runtime analysis) | ❌ | ✅ | ❌ | ❌ | ✅ |
| Historical trend tracking | ❌ | ✅ | ✅ | ✅ | ❌ |

## Where The Inspector Wins

1. **Product-level thinking.** It checks whether your app has a 404 page, empty states, proper error messages, and a working deploy config. No code analysis tool does this.
2. **Spec cross-referencing.** If you have a brief or spec (especially pipeline-built), The Inspector compares what was promised against what was built. This is unique.
3. **Zero setup.** No config files, no CI pipeline, no dashboard. Say "inspect this project" and get a report.
4. **Prioritized action plan.** Not just a list of issues — a sprint-structured remediation plan with effort estimates. Ready to execute.
5. **AI reasoning, not rule matching.** The Inspector can reason about whether auth logic makes sense in context, not just whether a function exists.

## Where Existing Tools Win

1. **Continuous monitoring.** SonarQube/Snyk/CodeClimate run on every commit in CI. The Inspector runs on-demand.
2. **CVE databases.** Snyk has the deepest vulnerability database. The Inspector checks for known patterns but doesn't query live CVE feeds.
3. **SAST precision.** SonarQube and Semgrep can trace data flows through compiled code with high precision. The Inspector reasons about code but can't execute it.
4. **Team dashboards.** Existing tools have web dashboards, trend graphs, team management. The Inspector produces files.

## The Pitch

"SonarQube tells you your code has 47 code smells. The Inspector tells you your product is missing auth on 3 endpoints, has no error handling on the payment flow, ships with debug mode on, has no deploy config, and will take approximately 6 hours to fix — here's the plan, prioritized by security risk."

They complement each other. The Inspector is the pre-ship sanity check; existing tools are the ongoing hygiene layer.

---

## Pricing Context (for client conversations)

The existing tools are SaaS subscriptions: $10-150/dev/month, ongoing. The Inspector is a per-audit engagement (€149-299 suggested) or bundled into managed service retainers. Different model, different value prop.
