# Irresistible Offer — Output Format Specification

This file is the **source of truth** for what an offer audit produces. Every audit MUST produce BOTH files described below. Reference this file when running Step 7 of the skill.

---

## Naming convention

For an audit of an existing product:
- Markdown: `[project_root]/OFFER-[TARGET-NAME]-AUDIT.md`
- HTML: `[project_root]/output/offer-[target-name]-audit.html`

For a greenfield irresistible-offer build:
- Markdown: `[project_root]/OFFER-[OFFER-NAME]-OFFER.md`
- HTML: `[project_root]/output/offer-[offer-name]-offer.html`

If `output/` does not exist in the project root, use `[project_root]/` for both files. Place the HTML next to any existing business plan, sales page, or related artifact so they live together.

---

## FILE 1: Markdown audit (16 sections)

The markdown is the source of truth for the audit content. The HTML visualizes what's in the markdown — never invent content in the HTML that isn't in the markdown.

### Required structure

Every section below is mandatory unless explicitly marked optional. Section ordering matters — it builds the argument from diagnosis to action.

**1. Header block**
- Title: "Irresistible Offer Audit — [Target Name]"
- Audited date (ISO)
- Source artifact path (the document or product being audited)
- Framework reference path (`context/playbooks/hormozi-grand-slam-offer.md`)
- Auditor identity (skill name, session)

**2. TL;DR (4-6 lines)**
- The one-paragraph verdict
- Market score / value equation score / revenue ceiling comparison
- The single highest-leverage change in plain language
- The "before applying any tactic, X must be true" gate condition

**3. CRITICAL FLAG #1: ICP / Strategy Conflicts** (only if conflicts exist)
- If there are multiple strategy documents in the same project pointing different directions, surface them in a 3-column comparison table: ICP / Price / Channel / Promise
- Force the user to pick a lane

**4. CRITICAL FLAG #2: Framework Misuse Patterns** (only if applicable)
- If the target document already references an offer or value framework but doesn't actually apply it, quote the offending passage
- Counter-quote with the customer's actual objections from the same document
- Show the gap between "stated" and "reality"

**5. Step 1: Market Diagnostic (4 indicators)**
Score each 1-10 with concrete rationale:
- Massive Pain
- Purchasing Power
- Easy to Target
- Growing Market

Total /40 with threshold interpretation:
- < 24 = niche pivot before continuing
- 24-32 = proceed but flag risks
- 32+ = green light

If the market scores below 32, present **3 sharper niche candidates** with their re-scored 4-indicator totals. The niche pivot is mandatory output if the original market is below the threshold.

**6. Step 2: Value Equation Analysis**
Present the formula visually:
```
              Dream × Likelihood
   VALUE  =  ─────────────────────
              Time Delay × Effort
```

Score current state on each driver (1-10, lower is better for Time/Effort). Calculate the current value score.

Then score the proposed (optimized) state. Calculate the proposed value score. Show the multiplier.

**Identify the weakest current driver explicitly.** That's the lever to attack first. State this in one sentence.

**7. Step 3: The Offer — Value Stack**
8 components minimum. Each row: Problem (in customer's own words from their feedback) → Sexier Solution Name → Delivery Mechanism → Value (€).

Total stacked value. Recommended price. Stack-to-price ratio (must be 5-10x per the value-stack rule).

**8. Step 4: The 5 Enhancers**
Each enhancer gets its own subsection:

- **Scarcity (quantity):** specific cohort/seat/business cap with reason-why
- **Urgency (time):** specific deadline mechanism (cohort/seasonal/bonus-based/exploding)
- **Bonuses:** at least 5 named bonuses, each with name + value + objection it addresses. Total bonus value must eclipse the core offer price by 3x+
- **Guarantees:** at least 2, layered. Format: "If [condition X], we [consequence Z]". Always named creatively, NEVER "satisfaction guarantee"
- **MAGIC Naming:** Letter-by-letter breakdown (Magnet/Avatar/Goal/Interval/Container) plus 5-10 candidate names with top 3 highlighted

**9. Step 5: Free Wrapper (Lead Generation)**
Specific lead magnet recommendation that flows into the paid offer. Include distribution strategy in 3-5 bullet points.

**10. Step 6: Promotion Type Sequence**
The sequencing order: Generate Flow → Monetize Flow → Increase Friction.
Map to Months 1-3 / 4-6 / 7-12 with concrete actions.

**11. Step 7: The Math — Current vs Optimized**
Side-by-side projection table for at least 3 years:
- Volume metrics (top of funnel)
- Conversion rates
- Paying customer counts
- Revenue per year

Per-customer math comparison: AOV, breakeven ad spend, LTV, conversion required for profitable paid acquisition.

**One brutal sentence at the end:** what is the difference in business model viability — side-hustle vs business?

**12. Step 8: Implementation Sequence (8 weeks)**
Concrete week-by-week task list. Group weeks into phases (Lock Offer / Build / Sales Page / Launch / Iterate).

**13. Step 9: Test Variants (A/B/C)**
3 alternative homepage headlines, each with:
- Headline (MAGIC-applied)
- Subhead
- CTA copy
- Niche assumption
- Estimated test budget

The test variants serve as the "if you can't commit, run this experiment instead" path.

**14. The Push Back** (mandatory, even when it stings)
This is the section where you challenge the user's premise. Pull-quote treatment.

Pattern: "[Target document] is a well-executed answer to the wrong question. The question it asks is [X]. The question it should ask is [Y]."

Then the conditional answers — if the user picks ICP A, do this; if B, do that; if C, do the other thing.

End with: "If you can't answer [the commitment question] in writing, [stop and do something else]."

The push-back exists because the framework only works when the user has chosen a lane. This section forces the choice.

**15. Anti-Patterns Avoided**
List the offer anti-patterns you deliberately did NOT do:
- Did not recommend "raise your prices" without restructuring
- Did not suggest "satisfaction guarantee"
- Did not pad with weak bonuses
- Did not skip the problem list
- Did not recommend premium pricing for products that can't deliver

5 items, each with strikethrough/checkmark formatting.

**16. Closing**
1-2 paragraphs. The framework is ready and standing. The bottleneck is not the offer — it's the commitment.

---

## FILE 2: Visualized HTML

The HTML is a beautiful, interactive, self-contained single-file visualization of the markdown. It is not a markdown-to-HTML conversion. It is a designed deliverable.

### Self-contained constraints
- Single HTML file
- All CSS inline
- All JS inline (vanilla, no frameworks)
- One external dependency allowed: Chart.js v4 from `https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js`
- No other CDNs, no other external scripts

### Design system (your brand)

If a `business-plan-2026.html` or similar branded artifact already exists in the same project, peek at lines 1-200 to extract its exact tokens and match them. The audit and the source artifact must read as the same product line.

Default tokens (use exactly):
```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #111111;
  --bg-card: #141414;
  --bg-tertiary: #1a1a1a;
  --text-primary: #f0f0f0;
  --text-secondary: #a3a3a3;
  --text-muted: #737373;
  --accent: #f59e0b;          /* amber — primary */
  --accent-hover: #d97706;
  --accent-secondary: #8b5cf6; /* purple */
  --success: #22c55e;
  --danger: #ef4444;
  --info: #38bdf8;             /* teal */
  --border: #262626;
  --border-focus: #404040;
  --font-body: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  --font-display: 'Playfair Display', Georgia, serif;
}
```

Load fonts from Google Fonts inline:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Playfair+Display:wght@400;600;700;800&display=swap" rel="stylesheet">
```

### Color usage rules
- **Amber (`--accent`):** primary CTAs, section numbers, highlights
- **Purple (`--accent-secondary`):** secondary highlights, alternative tracks
- **Red (`--danger`):** warnings, current-state values, anti-patterns
- **Green (`--success`):** optimized state values, recommendations, positive deltas
- **Teal (`--info`):** neutral data, definitions, niche candidates
- All text on dark backgrounds, never inverse

### Layout
- Max-width container: 1100px
- Section padding: 64px vertical
- Card padding: 24px
- Grid: 2 columns desktop, 1 column < 880px
- Sticky top nav with scroll-spy
- Hero section is full viewport height with centered content

### Sections to render (16 — match the markdown 1:1)

Each section gets a visual treatment, not just rendered text. Specific treatments:

**1. Hero / Cover**
- Big display title (Playfair, 3.5rem)
- Subtitle with date
- Stat grid (4 prominent numbers): Market /40, Value Eq score, Year 3 ceiling current, Year 3 ceiling optimized
- Pull-quote with the verdict

**2. TL;DR card** — single prominent card with 4-6 bullets

**3. Critical Flag #1 — ICP Conflict** (if applicable)
- 3 cards side-by-side, each ICP doc as a card
- Visual "vs" connector showing conflict
- Each card expandable on click

**4. Critical Flag #2 — Framework Misuse** (if applicable)
- Quote box with offending passage
- Counter-quote box with customer objections
- Visual "stated vs reality" treatment

**5. Market Diagnostic**
- **Chart.js radar chart** (REQUIRED): 4 axes, single dataset, threshold zones marked
- 4 indicator cards below the chart with rationale text

**6. Niche Pivot** (if market scored < 32)
- 3 candidate cards with score badges
- Bar visualization or gauge for each score
- Each card expandable for the rationale

**7. Value Equation**
- Visual formula display (numerator over denominator)
- Side-by-side current state vs proposed state
- **Chart.js grouped bar chart** (REQUIRED): each driver compared current vs proposed
- Multiplier callout (e.g., "8.9x")

**8. The 8-Component Value Stack**
- 8 cards in a 2-column grid (1 column mobile)
- Each card: Problem → Solution Name → Delivery → Value (€)
- **Each card expandable on click** to reveal full delivery detail
- Total at bottom with strikethrough math: ~~€ stacked value~~ → € price
- Stack-to-price ratio badge (must be 5-10x)

**9. The 5 Enhancers** (one section each)
- **Scarcity:** cohort cap visualization, "honest scarcity" callout
- **Urgency:** timeline visual showing the deadline mechanism
- **Bonuses:** 5 bonus cards with values, total bonus value vs price callout
- **Guarantees:** 2+ "shield" cards. **Click to flip** and reveal customer-facing copy
- **MAGIC Naming:** letter-by-letter breakdown table + 5-10 candidate names with top 3 highlighted

**10. Free Wrapper**
- Card explaining the lead magnet
- Visual: current state vs proposed state
- Distribution strategy as 3-5 icon bullets

**11. Promotion Type Sequence**
- 3-phase visual: Months 1-3 / 4-6 / 7-12
- Each phase with its own card

**12. The Math — Current vs Optimized**
- **Chart.js grouped bar chart** (REQUIRED): 3-year revenue projection, current vs optimized
- Per-customer math comparison table with color coding (red current, green optimized)
- Big callout with the brutal one-sentence verdict

**13. Implementation Timeline**
- 8-week visual stepper / horizontal timeline
- Color-coded by phase
- **Each week clickable** — loads task list into a detail panel below

**14. Test Variants A/B/C**
- 3 mockup cards showing alternative homepage headlines
- Visually distinct (different border accents) so they feel like real test variants
- Each shows: headline + subhead + CTA + niche + estimated test cost

**15. The Push Back**
- Big pull-quote treatment for the verdict sentence
- Question reframe (from X to Y)
- 4 conditional answers as expandable cards

**16. Anti-Patterns Avoided**
- 5 items with strikethrough on the anti-pattern, checkmark on what was done instead
- Each expandable for rationale

**17. Footer**
- Generation metadata
- "Read alongside" link to the source artifact

### Charts (3 minimum, all Chart.js v4)

1. **Market Diagnostic Radar** — 4 axes (Pain/Power/Target/Growth), single dataset, threshold zones
2. **Value Equation Comparison** — grouped bars, current vs optimized for each driver
3. **3-Year Revenue Projection** — grouped bars by year, current vs optimized

Optional:
4. Niche scoring bar chart
5. Stacked value horizontal bar showing each component's contribution

Chart styling: dark background, grid lines in `--border`, dataset colors using `--accent` and `--success`/`--danger` for comparisons.

### Interactivity (20+ handlers minimum)

User explicitly asks for "everything clickable for more info." Implement:

- **Sticky top nav** with scroll-spy active state highlighting
- **All 8 value stack cards expandable** to show delivery detail
- **All 5 bonus cards expandable** to show full bonus rationale
- **All 2+ guarantee cards flip** on click to reveal customer copy
- **All 3 niche cards expandable** to show scoring rationale
- **All 8 timeline week cards clickable** — loads tasks into a detail panel
- **All 5 anti-pattern items expandable** for rationale
- **Hover tooltips on framework jargon** (Perceived Likelihood, MAGIC, Value Equation, etc.) — small hover boxes with one-sentence definitions
- **Smooth scroll** on nav clicks
- **CSS transitions** on every interactive element (no jarring jumps)

### Responsiveness
- Breakpoint at 880px: 2-col grids → 1-col
- Hero adjusts font size on mobile
- Nav becomes hamburger or wraps on narrow viewports
- Charts resize responsively
- Print-friendly: `@page` CSS, `page-break-after` on major sections

### Voice & accuracy
- Quote the markdown verbatim where the markdown quotes things
- Numbers must match the markdown EXACTLY
- Don't add new content in the HTML — visualize what's in the markdown
- Preserve the markdown's bluntness and push-back tone in the visual treatment
- Use red/amber for warnings, green for recommendations

---

## Workflow checklist

When running the skill:

1. Run Steps 0-6 of the SKILL.md workflow (context gathering through enhancers)
2. Write the markdown file (Step 7 in SKILL.md, format above)
3. **Build the HTML visualization** (new Step 8) by:
   - Reading the markdown you just wrote
   - Reading any existing branded artifact in the same folder for token alignment
   - Producing the self-contained HTML matching the spec above
4. Verify both files exist
5. Print the final report including both file paths
6. Suggest the user open the HTML to review

The HTML build should take 30-45 minutes with quality. Don't rush it. The HTML is the artifact the user will use to make decisions — it must look like a premium consulting deliverable.

---

## Quality bar

A passing audit produces:
- Markdown: 400-700 lines, 16 sections, all required
- HTML: 90-110 KB, 2500-3500 lines, 16 sections, 3+ charts, 20+ interactive handlers

If your output is significantly smaller, you've cut corners. Re-read the spec and complete the missing sections.

---

## Baseline comparison mode (re-audits)

When the user re-audits a project after evolving the spec or product, the audit MUST become a comparison instead of a fresh standalone document. This is non-negotiable for evolved-product audits — it lets the user measure spec evolution against a frozen baseline.

### Detection
At the start of every audit, **check for** `[project_root]/OFFER-AUDIT-HISTORY.json`:
- If absent → fresh audit, create the history file at the end of Step 7 with this run as baseline
- If present → comparison mode is ACTIVE for the rest of the workflow

### Snapshot file format
`OFFER-AUDIT-HISTORY.json` is append-only. Each audit appends one entry to the `audits` array. Required fields per entry:

```json
{
  "audit_id": "YYYY-MM-DD-[label]",
  "audited_at": "ISO timestamp",
  "source_artifact": "path/to/the/spec/being/audited",
  "audit_target": "human readable name",
  "auditor": "skill name + session context",
  "is_baseline": false,
  "deliverables": {"markdown": "...", "html": "..."},
  "current_positioning": "one-line ICP statement",
  "market_diagnostic": {
    "pain": N, "purchasing_power": N, "easy_to_target": N, "growing_market": N,
    "total": N, "interpretation": "...",
    "rationale": {"pain": "...", "purchasing_power": "...", "easy_to_target": "...", "growing_market": "..."}
  },
  "value_equation": {
    "current": {"dream": N, "perceived_likelihood": N, "time_delay": N, "effort_sacrifice": N, "score": N, "weakest_driver": "...", "weakest_driver_reason": "..."},
    "proposed_optimized": {"dream": N, "perceived_likelihood": N, "time_delay": N, "effort_sacrifice": N, "score": N, "multiplier_vs_current": N}
  },
  "value_stack": {
    "components_count": N,
    "components": [{"name": "...", "value_eur": N}],
    "total_stacked_value_eur": N,
    "recommended_price_founders_eur": N,
    "recommended_price_regular_eur": N,
    "stack_to_price_ratio_at_founders": N
  },
  "enhancers": {
    "scarcity": "...", "urgency": "...",
    "bonuses_count": N, "bonuses_total_value_eur": N, "bonuses_eclipse_price_ratio": N,
    "guarantees_count": N, "guarantee_names": ["..."],
    "magic_name_top_3": ["..."]
  },
  "niche_candidates": [{"name": "...", "score": N, "rationale": "..."}],
  "revenue_projection": {
    "current_plan": {"year_1_eur": N, "year_2_eur": N, "year_3_eur": N, "weighted_aov_eur": N},
    "optimized_plan": {"year_1_eur": N, "year_2_eur": N, "year_3_eur": N, "weighted_aov_eur": N, "year_3_multiplier": N}
  },
  "icp_conflicts": {"count": N, "documents": [{"path": "...", "icp": "...", "price_range": "..."}], "verdict": "..."},
  "verdict_one_line": "...",
  "primary_recommendation": "...",
  "decision_required": "..."
}
```

### Comparison-mode workflow changes

When prior audits exist:

**Step 7 markdown additions:**
- Insert a new section between #2 (TL;DR) and #3 (Critical Flag #1): **"Section 2.5 — Evolution Since Last Audit"**
- This section shows a delta table comparing the most recent prior audit to the current one
- Column headers: Metric / Baseline / Current / Delta / Direction
- Rows: market score total, each of the 4 indicators, current value equation score, weakest driver name, stack-to-price ratio, year 3 optimized revenue, ICP conflicts count
- Color/symbol coding: ↑ green for improvements, ↓ red for regressions, → grey for unchanged
- Add a one-paragraph narrative below the table: "What changed since [baseline date]:" with the user's spec changes summarized

**Step 8 HTML additions:**
- Insert a new visualized section after the Hero: **"Evolution Since Last Audit"**
- Required visualizations:
  - **Side-by-side market diagnostic radars** (one per audit, overlaid or paired)
  - **Delta bar chart** showing change in each of the 4 market indicators
  - **Big delta number cards** for: market total, value equation score, year 3 revenue ceiling
  - **Score evolution timeline** (line chart) if 3+ audits exist
- Visual treatment: green for improvements, red for regressions, neutral grey for unchanged
- Add a "Changes Since [baseline date]" narrative card

### Snapshot saving rules
- **Append, never overwrite.** Every audit adds a new entry to the array.
- **Mark the first audit `is_baseline: true`.** All subsequent audits are `is_baseline: false`.
- **Audit IDs must be unique** — if user re-audits same day, append `-v2`, `-v3`, etc.
- **Never delete prior entries** — historical comparability is the point. If a prior entry has wrong data, add a new corrected entry, do not edit.

### When the comparison narrative writes itself
The most powerful sentence in a re-audit is: "Since [baseline], market score went from X to Y, value equation from A to B, and the weakest driver shifted from [old weakness] to [new weakness] — meaning your spec changes addressed [thing] and revealed [new thing]."

That sentence belongs at the top of Section 2.5 in the markdown and as the hero subhead in the HTML.

### Failure modes to avoid
- **Don't re-explain the framework on a re-audit.** The user knows it. Cut the playbook context, jump straight to the deltas.
- **Don't pretend a re-audit is a fresh audit.** The whole point is the comparison. If you produce a clean fresh audit on a re-audit run, you've broken the contract.
- **Don't lose the verdict-stinging tone on a re-audit.** Even if scores improved, keep the bluntness — "improved from terrible to mediocre" is more useful than "great progress."
