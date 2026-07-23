# EVALUATE -- Three-Leg Site Assessment

## Purpose
Assess a target website/business from three independent data sources. Each leg can succeed or fail independently -- the audit continues with whatever data is available.

## Three Legs (run in parallel)

### LEG 1: Direct Crawl (Playwright MCP)

**Tools:** `browser_navigate`, `browser_snapshot`, `browser_resize`, `browser_console_messages`, `browser_network_requests`

**Sequence:**
1. Navigate to target URL
2. Snapshot at 3 viewports: 1440px (desktop), 768px (tablet), 375px (mobile)
3. Map navigation structure (all top-level and second-level nav items)
4. Identify conversion paths (CTAs, forms, pricing pages, signup flows)
5. Check console for errors/warnings
6. Check network for failed requests, slow responses

**Extract:**
- Navigation depth and information architecture
- CTA inventory (what they want users to do)
- Form complexity (how hard is it to convert)
- Mobile responsiveness quality
- JavaScript errors and broken resources
- Visual design quality assessment

**Anti-bot handling:**
If Cloudflare, reCAPTCHA, or other anti-bot blocks the crawl:
- Log: "Direct crawl blocked by [mechanism]. Leg 1 data unavailable."
- Do NOT retry with circumvention techniques
- The other two legs provide sufficient data to continue
- Flag in report: "Site Health score based on Legs 2+3 only (direct crawl blocked)"

### LEG 2: Sentiment Mining (WebSearch)

**Tools:** `WebSearch`, `WebFetch`

**Search queries (adapt [target] to the actual site/company name):**

```
"[target] reviews"
"[target] vélemények" (Hungarian)
"[target] complaints"
"[target] panasz"
"[target] site:reddit.com"
"[target] site:trustpilot.com"
"[target] Google reviews"
"[target] Árukeresó vélemények"
"[target] app store reviews"
"[target] vs [competitor]" (users comparing)
"[target] alternative" (users looking to leave)
"[target] frustrating OR annoying OR terrible OR slow"
```

**Extract and categorize:**
- **Pain points:** what users complain about most (ranked by frequency)
- **Praise points:** what users love (don't ignore strengths)
- **Feature requests:** what users wish the site had
- **Competitor comparisons users make:** "I switched to X because..."
- **Churn signals:** "looking for alternative to [target]"
- **NPS proxy:** ratio of positive to negative sentiment across sources

**Scoring:**
- 5+ independent complaints about the same issue = Critical pain point
- 3-4 = High pain point
- 1-2 = Noted pain point
- User-initiated competitor comparisons are the highest-value data for the teaser

**This leg ALWAYS succeeds** (public data, no anti-bot risk).

### LEG 3: Technical Audit (WebSearch + WebFetch)

**Tools:** `WebSearch`, `WebFetch`

**Direct fetches (public endpoints, no anti-bot risk):**
```
WebFetch: [target]/robots.txt
WebFetch: [target]/sitemap.xml
WebFetch: [target]/llms.txt (check if exists)
WebFetch: [target]/.well-known/security.txt
```

**Search-based checks:**
```
WebSearch: "[target] site speed PageSpeed"
WebSearch: "[target] technology stack built with"
WebSearch: "[target] SEO audit"
WebSearch: "site:[target] inurl:api" (public API presence)
```

**Extract:**
- robots.txt: which crawlers are allowed/blocked (GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
- Sitemap: page count, update frequency, structure
- llms.txt: AI-readiness signal (presence = forward-thinking)
- Technology stack: frameworks, CDN, analytics, A/B testing, CRM integrations
- Page speed data (from public tools/cached results)
- SSL certificate validity
- Security headers (via security.txt)

**This leg ALWAYS succeeds** (public endpoints only).

## Output

Combine all three legs into structured JSON:

```json
{
  "target": "ingatlan.com",
  "timestamp": "2026-05-19T...",
  "legs_completed": ["crawl", "sentiment", "technical"],
  "site_health_score": 62,
  "sub_scores": {
    "ux": 55,
    "performance": 70,
    "content": 65,
    "technical": 72,
    "mobile": 48,
    "accessibility": 60,
    "sentiment_nps_proxy": 3.2
  },
  "critical_pain_points": [...],
  "praise_points": [...],
  "user_feature_requests": [...],
  "user_competitor_comparisons": [...],
  "tech_stack": [...],
  "crawler_access": {"GPTBot": "blocked", "ClaudeBot": "allowed", ...},
  "llms_txt_present": false
}
```

Save to `evolution-audits/{slug}/reports/site_health.json`.
