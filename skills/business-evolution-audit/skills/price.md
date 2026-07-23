# PRICE -- Consultation Pricing Proposal

## Purpose
Generate a pricing proposal calibrated to the target company's size, industry, and the audit's scope.

## Inputs Required
- `roadmap.json` (from plan)
- Industry classification
- Target company size estimate (from benchmark research)

## Tier Structure

| Tier | Name | Price (EUR) | What They Get | Delivery |
|------|------|-------------|---------------|----------|
| 0 | **Teaser** | Free | 3-page preview + email | Immediate (automated) |
| 1 | **Snapshot Report** | €299-499 | 10-page focused audit: Site Health + SEO/GEO + Top 10 Gaps with revenue estimates | 48 hours |
| 2 | **Full Evolution Audit** | €1,499-2,499 | 30-page report + 12-month roadmap + revenue model + implementation specs | 1 week |
| 3 | **Advisory Retainer** | €499-999/month | Monthly check-ins, roadmap progress reviews, vendor evaluation support, priority access | Ongoing |
| 4 | **Implementation Partner** | €2,500-5,000/month | Hands-on: manage improvement projects, coordinate vendors, weekly syncs | Ongoing |

## Tier Selection Logic

**Company size estimation (from public data):**
- WebSearch: "[company] employees" or "[company] revenue"
- Check LinkedIn company page (employee count range)
- Check company registry (public filings if available)

**Pricing calibration:**

| Company Size | Snapshot | Full Audit | Advisory |
|-------------|----------|-----------|----------|
| Small (1-10 employees) | €299 | €1,499 | €499/mo |
| Medium (11-100) | €399 | €1,999 | €749/mo |
| Large (100+) | €499 | €2,499 | €999/mo |

## Value Justification

The proposal must justify pricing against:

1. **Alternative cost:** "A traditional consulting firm charges €5,000-15,000 for a comparable audit. Ours is AI-augmented, delivered faster, at a fraction of the cost."
2. **ROI framing:** "The audit identified €[X] in annual revenue opportunity. At €[price], the audit pays for itself if just ONE recommendation is implemented."
3. **Opportunity cost:** "Every month without [highest-impact gap] costs an estimated €[monthly_impact]. The audit cost is recovered in [days] of implementing the first Quick Win."

Apply grand-slam-offer value stacking:
- Core: the audit report itself
- Bonus 1: GEO/AI visibility audit (normally a separate service)
- Bonus 2: Competitor Feature Matrix (proprietary research)
- Bonus 3: Revenue projection model with three scenarios
- Bonus 4: Priority email support for 30 days post-delivery

## Guarantee

"If the audit doesn't identify at least 5 actionable improvements with measurable revenue impact, we'll refund the full amount. No questions."

This is low-risk because the methodology virtually guarantees findings -- every business has gaps.

## Currency and Tax

- Default currency: EUR
- For Hungarian targets: show HUF equivalent at current MNB rate
- VAT handling: reverse charge for B2B EU, 27% Hungarian VAT for domestic
- Reference: your own invoicing configuration for local tax and entity details

## Output

```json
{
  "target": "ingatlan.com",
  "company_size_estimate": "large",
  "recommended_tier": "full-audit",
  "pricing": {
    "snapshot": 499,
    "full_audit": 2499,
    "advisory_monthly": 999,
    "partner_monthly": 5000
  },
  "value_justification": {
    "alternative_cost": "€10,000-15,000 from traditional consultancies",
    "roi_payback_days": 12,
    "opportunity_cost_monthly": 175000
  },
  "currency": "EUR",
  "vat_treatment": "reverse_charge"
}
```

Save to `evolution-audits/{slug}/reports/pricing.json`.
