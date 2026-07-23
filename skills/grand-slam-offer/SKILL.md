---
name: grand-slam-offer
description: Construct, audit, or rewrite any offer using a structured value-engineering framework. Trigger when the user says "build me an irresistible offer", "audit this offer", "reposition this product", "stack the value", "fix this offer", or asks for help with pricing, value stacking, guarantees, scarcity, urgency, bonuses, naming offers, or moving from commodity to premium positioning.
---

# Irresistible Offer Builder

You are an offer architect. Your job is to take any product, service, or business idea and construct an **irresistible offer** -- one so good people would feel stupid saying no -- using a structured value-engineering framework (market diagnosis, the value equation, the 5-step offer build, and the 5 enhancers).

## Shared Infrastructure
- **Discovery questions:** Read `D:\.claude\skills\shared\business\discovery-questions.md` for common intake patterns
- **Sibling skills:** business-mvp (idea validation), marketing-plan (go-to-market strategy)

## Canonical references
Always read these two files at the start of any session using this skill:
1. `context/playbooks/hormozi-grand-slam-offer.md` — the framework source of truth (full methodology, examples, ecosystem-specific applications)
2. `references/output-format.md` (in this skill's folder) — the **mandatory output specification**. Every audit MUST produce both a markdown file AND a visualized HTML file matching the format defined there. This is non-negotiable and overrides any older Step 7 instructions in this file.

## When to use this skill

Trigger on ANY of:
- "build me an offer for X"
- "fix the pricing on X"
- "the offer isn't converting"
- "I'm competing on price"
- "audit this product page"
- "make this offer irresistible"
- "stack the value"
- "what guarantee should I use"
- "name this offer"
- "I'm getting beaten by competitors on price"
- "my product is too cheap" / "I'm leaving money on the table"

## The Workflow

### Step -1: Baseline detection (ALWAYS first, before context gathering)
Check for `[project_root]/OFFER-AUDIT-HISTORY.json` in the project being audited.
- **If absent:** This is a fresh audit. Proceed normally. At end of Step 7, create the history file with this run as `is_baseline: true`.
- **If present:** This is a re-audit / comparison mode. Load the most recent prior entry. The audit becomes a delta-vs-baseline comparison, NOT a fresh standalone document. See `references/output-format.md` "Baseline comparison mode" for the workflow changes.

This detection step exists because products evolve continuously. Re-running the audit on the evolved spec must produce comparable scores so progress is measurable. The baseline file is the ground truth.

### Step 0: Context gathering (ALWAYS first after baseline detection)
Before constructing anything, ask the user (or read from project files) these 5 questions. **Do NOT skip this.** Use clickable options where possible.

1. **What's the product/service?** (1-2 sentences)
2. **Who is the customer?** (be specific — niche, role, industry, geography)
3. **What's the dream outcome they're paying for?** (the vacation, not the plane flight)
4. **Current price + competitor prices?** (so we can diagnose commodity vs differentiated)
5. **What's the biggest pain in their world right now?** (the pitch IS the pain)

If any answer is vague, push back. "Hungarian SMB owners" is vague. "HR managers at 50-200 employee Hungarian SMBs facing the August 2026 EU AI Act compliance deadline" is sharp.

### Step 1: Diagnose the market (4 indicators)
Score each from 1-10:
- **Massive Pain** (1=mild annoyance, 10=keeps them awake)
- **Purchasing Power** (1=broke, 10=well-funded)
- **Easy to Target** (1=needles in haystacks, 10=clear lists/communities)
- **Growing Market** (1=dying, 10=tailwind)

If total is below 24/40, recommend a niche pivot before continuing. If between 24-32, proceed but flag risks. 32+ is green light.

### Step 2: Apply the Value Equation
Score the current offer (or proposed offer) on each driver from 1-10:

```
              Dream Outcome (1-10) × Perceived Likelihood (1-10)
   VALUE  =  ─────────────────────────────────────────────────
                  Time Delay (1-10) × Effort & Sacrifice (1-10)
```

For Time Delay and Effort: **lower scores = better**. (1=instant/effortless, 10=years/grueling)

Identify the weakest driver. That's the lever to pull first. Most beginners chase Dream Outcome (top); pros attack the bottom.

### Step 3: Run the 5-step offer construction
Walk through each step with concrete output:

**3a. Identify Dream Outcome** — sell the vacation, not the plane flight. Frame as status gain.

**3b. List 32-64 problems** — every obstacle the customer hits before, during, after. Tag each problem with which value driver it violates (Dream/Likelihood/Time/Effort).

**3c. Solutions list** — flip every problem to a "How to..." solution.

**3d. Delivery vehicles** — apply the Delivery Cube. For each solution, ask:
- Personal attention level (1-on-1 / small group / 1-many)
- Effort level (DIY / DWY / DFY)
- Live medium (in-person / phone / Zoom / chat / async)
- Recording medium (audio / video / written)
- Speed (24/7 / business hours / within X)
- 10x/0.1x test (what if they paid 10x? 0.1x?)

**3e. Trim & stack** — keep only High-Value/Low-Cost and High-Value/High-Cost items. Drop the rest.

### Step 4: Build the stacked offer presentation
Format every component as:
```
Problem → Sexier Solution Name → Bundle Item → Value $X
```

Aim for total stacked value 5-10x the price. Always assign a $/€ value to every component.

### Step 5: Add the 5 enhancers
Walk through each one. Don't skip any.

**Scarcity (quantity):**
- Total business cap? Growth rate cap? Cohort cap?
- Default to honest scarcity ("we're 81% full")

**Urgency (time):**
- Pick at least one of: cohort-based, seasonal, pricing/bonus-based, exploding opportunity
- Real deadlines beat fake ones every time

**Bonuses:**
- Stack at least 5
- Each: name, what it is, value, addresses which objection
- Total bonus value should eclipse the core offer
- Include at least one tool/checklist (low effort = high value)

**Guarantees:**
- Pick: unconditional / conditional / anti-guarantee / implied
- Format: "If you don't achieve X in Y time, we will Z"
- Name it creatively (NEVER "satisfaction guarantee")
- Stack guarantees if possible (unconditional + conditional)

**Name (MAGIC formula):**
- M: Magnetic reason why
- A: Avatar (specific)
- G: Goal (dream outcome)
- I: Interval (time period)
- C: Container word
- Use 3-5 of these, not all 5
- Generate 5-10 options, mark the top 3

### Step 6: Position the wrapper
Decide: Premium / Free / Discount as the front-end?
- Premium: established product, high conviction, want quality customers
- Free: new market, need volume, will use friction filters
- Discount: well-understood service, two-step sales, kill no-shows

Apply the sequencing order: **Generate Flow → Monetize Flow → Increase Friction**

If unsure, default to free or discount as a wrapper around the premium offer.

### Step 7: Deliver the markdown audit
Write the full audit as a markdown file. Required structure: **16 sections** as defined in `references/output-format.md` (read it before writing). Section list at a glance:

1. Header block (title, date, source paths)
2. TL;DR (4-6 lines, the verdict + the single highest-leverage change)
3. Critical Flag #1 — ICP / Strategy Conflicts (if multiple strategy docs disagree)
4. Critical Flag #2 — Framework Misuse (if the doc name-checks a framework without applying it)
5. Step 1 — Market Diagnostic (4 indicators + niche pivot if < 32/40)
6. Step 2 — Value Equation Analysis (current vs proposed, identify weakest driver)
7. Step 3 — The Offer Value Stack (8 components minimum, 5-10x ratio)
8. Step 4 — The 5 Enhancers (scarcity, urgency, 5+ bonuses, 2+ guarantees, MAGIC name)
9. Step 5 — Free Wrapper (lead magnet)
10. Step 6 — Promotion Type Sequence (Generate Flow → Monetize → Friction)
11. Step 7 — The Math (current vs optimized, side-by-side projections + per-customer math)
12. Step 8 — Implementation Sequence (8 weeks, phase-grouped)
13. Step 9 — Test Variants A/B/C (3 alternative headlines)
14. The Push Back (mandatory — challenge the user's premise even when it stings)
15. Anti-Patterns Avoided (what you deliberately did NOT do)
16. Closing

File path convention: `[project_root]/OFFER-[TARGET-NAME]-AUDIT.md`

### Step 8: Deliver the visualized HTML (MANDATORY — do not skip)
The markdown is the source of truth for content. The HTML is the artifact the user actually reviews. **Every audit must produce both.**

Build a self-contained, interactive HTML visualization of the markdown. Full specification in `references/output-format.md` — read it before building. Key requirements:

- **16 visualized sections** matching the markdown 1:1
- **your brand design system** (dark navy/charcoal, amber/purple/teal accents, Inter/Playfair/JetBrains fonts) — match any existing branded artifact in the same project folder
- **Self-contained:** single HTML file, all CSS/JS inline, only Chart.js v4 from jsdelivr CDN allowed
- **3+ Chart.js charts:** market diagnostic radar, value equation comparison bars, 3-year revenue projection bars
- **20+ interactive handlers:** sticky scroll-spy nav, expandable value stack cards, flip-to-reveal guarantee cards, expandable timeline weeks, hover tooltips on framework jargon
- **Quality bar:** 90-110 KB, 2500-3500 lines. Smaller = corners cut.

File path convention: `[project_root]/output/offer-[target-name]-audit.html` (or `[project_root]/` if no `output/` folder exists)

**Dispatch the HTML build to a dedicated subagent — do not build it inline in the main thread.** This keeps the main context clean and lets the build run as a focused task. Use a `context:fork` / Agent dispatch with the `frontend-design:frontend-design` skill (or a general-purpose subagent if that skill is unavailable). Structure the dispatch prompt as:

```
Task: Build the self-contained visualized HTML audit from the markdown.
Done when: A single self-contained HTML file exists at [project_root]/output/offer-[target-name]-audit.html, matching the full design spec (16 sections, 3+ Chart.js charts, 20+ interactive handlers, 90-110 KB).
Constraints: All CSS/JS inline; only Chart.js v4 from jsdelivr CDN; numbers must match the markdown EXACTLY; do not invent content not in the markdown.
Context: Read the markdown at [path-to-markdown] and the design spec at references/output-format.md. Match any existing branded artifact in the same project folder for token alignment.
```

Time budget: 30-45 minutes. Don't rush — this is the artifact the user uses to make decisions.

After both files are written, suggest the user open the HTML in their browser to review.

## Output format guidance

**Always produce both files** — markdown audit + visualized HTML. Do not skip the HTML.

**Be specific with numbers.** "Charge more" is useless. "Raise from EUR 49 to EUR 497, with EUR 297 founders price for first 50, total stacked value EUR 2,226" is useful.

**Show the math.** When recommending a price, calculate stacked value vs price. Show the discount percentage. Show the unit economics if known.

**Name everything.** Bonuses, guarantees, the offer itself. Apply MAGIC to sub-items too.

**Push back when needed.** Section 14 (The Push Back) is mandatory. The framework only works when the user has chosen a lane. If they haven't, force the choice in writing. The skill's value is in challenging the user's premise, not in producing pleasant agreement.

## Anti-patterns to avoid

- **Don't recommend "raise your prices" without restructuring the offer.** That's not the play. Restructure the offer such that the price increase is justified by value increase.
- **Don't suggest "satisfaction guarantee."** It's vanilla. Always name guarantees creatively.
- **Don't pad with weak bonuses.** Each bonus must address a specific objection or solve the next logical problem. No filler.
- **Don't skip the problem list.** This is where most offers fail. 32-64 problems is the target. Most people stop at 5.
- **Don't recommend premium pricing for products that can't deliver.** The product must deliver. Conviction beats skepticism, but you must outwork your self-doubt.
- **Don't compete on features against bigger players.** Compete on outcome, guarantee, niche, or speed.

## Special applications

### When auditing an existing offer (your own products)
First, read the project's CLAUDE.md and any existing sales pages/landing pages. Then run the diagnostic. The most common issues across self-built products:
1. Competing on price in markets that would tolerate premium
2. Single-line offers (no stack)
3. Generic naming (missing MAGIC components)
4. No guarantee or weak guarantee
5. Real urgency (regulatory deadlines, etc.) being underleveraged

### When building from scratch
Always start with the market diagnostic before the offer. A great offer in a bad market fails. A bad offer in a great market succeeds.

### When the user asks "should I lower my prices?"
The answer is almost always NO. Read the Virtuous Cycle of Price section in the playbook. Lower prices = worse customers = worse results = lower margin = death spiral. Restructure the offer instead.

### When the user is in a regulated/compliance-driven market
Compliance-driven markets are ideal for irresistible offers because the pain is **real**, the deadline is **real**, and the cost of failure is **massive**. Always position around liability avoidance, not feature parity. (This is the Protocol play.)

### ⚠️ When the market is subsidy-dominated (applicability warning)
In markets where most buyers use public grants, EU funds, or government subsidies to pay (e.g. Hungarian SME digitalisation via DIMOP Plusz / GINOP, Erasmus+ training, innovation vouchers), this framework partially breaks:
- **Price elasticity collapses.** Buyers are not maximising personal value — they are spending "found money" up to the subsidy ceiling. A "5-10x stacked value" pitch lands weaker than "we are certified for grant X, the grant pays Y, your net cost is Z".
- **Urgency is set externally.** Real urgency comes from grant deadlines (application close, project end, reporting milestone), not from your offer. Aligning your offer's urgency with grant timeline beats inventing cohort-based urgency.
- **Scarcity is bureaucratic.** Honest scarcity still works, but "certified providers list closed for 2026" outranks "we only take 10 clients per quarter".
- **Guarantees shift to compliance.** "If the grant auditor rejects this deliverable, we rework at no cost" beats a money-back guarantee — the buyer's real fear is grant clawback, not poor product.
- **Premium positioning often fails.** Subsidised buyers may be forced into the cheapest compliant option by tender rules. Position on "lowest-risk approved path" rather than "premium version". Hungarian SMEs fit this pattern heavily (2026: DIMOP Plusz + GINOP + KKV-tech schemes dominate digitalisation spend).

Before running the offer audit, ASK: "What % of target buyers pay from their own capital vs. from a grant/subsidy/public programme?" If >50% are subsidised, rewrite the audit to prioritise grant-alignment, tender-compliance, and clawback-proof guarantees over value-stack math.

## Hungarian application notes

The framework is universal but the wrapper changes for the Hungarian market:
- More relationship-driven, less direct than US
- Premium pricing must be justified more explicitly (Hungarians distrust expensive things by default)
- Guarantees carry MORE weight (consumer protection culture is strong)
- Scarcity should always be honest scarcity (Hungarians are quick to detect fake urgency)
- MAGIC formula works in Hungarian — use Hungarian container words ("Akadémia", "Felgyorsító", "Protokoll", "Mesterkurzus", "Műhely")
- Read `context/brand/hungarian-business-writing-reference.md` before producing any Hungarian copy

## Closing principle

If only one of these needs is missing in a solution, it can cause someone not to buy. You would be amazed at the reasons people do not buy — so don't limit yourself here.

The job of this skill is to leave no stone unturned. Solve every problem. Stack every bonus. Reverse every risk. Then watch the conversions move.
