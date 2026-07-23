# EVALUATE — Three-Leg Site Assessment (Firecrawl edition)

> **Default crawler:** Firecrawl is the DEFAULT crawler for EVALUATE — it renders JS, defeats most anti-bot, and returns markdown + html + links + metadata + a screenshot in one call. **Playwright MCP is fallback-only** (login-gated / interaction-heavy flows).
> **Promoted into the live skill on 2026-05-29.** The original Playwright spec is preserved at `skills/evaluate-legacy-playwright.md` (the revert target if needed).
> **Output schema is unchanged.** Every field downstream steps (BENCHMARK → PLAN → … → REPORT) read out of `reports/site_health.json` is produced exactly as before. Only the *acquisition method* for Leg 1 changed.

---

## Purpose

Assess a target website/business from three independent data sources. Each leg can succeed or fail independently — the audit continues with whatever data is available.

- **LEG 1: Direct Crawl** — now **Firecrawl `/v1/scrape` + `/v1/map`** (was Playwright MCP).
- **LEG 2: Sentiment Mining** — **unchanged** (`WebSearch` + `WebFetch`).
- **LEG 3: Technical Audit** — **unchanged in substance**; keeps the **curl** direct fetches for `robots.txt` / `sitemap.xml` / `llms.txt` / `security.txt` plus `WebSearch`.

Read API keys from your own environment/config. Never commit keys. **Never hardcode the key** in the skill, agent prompts, or committed files. The examples below use the placeholder `$FIRECRAWL_KEY`.

```bash
# All curl examples below assume:
FIRECRAWL_KEY="fc-..."   # read from your own env/config, do NOT commit
BASE="https://api.firecrawl.dev"
```

---

## Three Legs (run in parallel)

### LEG 1: Direct Crawl — Firecrawl

**Endpoints:** `POST /v1/scrape` (per-page extraction + screenshot) and `POST /v1/map` (URL inventory). One scrape per page; one map per domain.

#### Sequence

1. **Map the domain** (`/v1/map`) → get the full URL inventory and the information-architecture signal (replaces Playwright nav-tree walking).
2. **Scrape the homepage** (`/v1/scrape`) with `formats: ["markdown","html","links","screenshot","summary"]`. The single response carries the content, the rendered HTML (for DOM-level checks), the link graph, a real screenshot, and `metadata` (status, title, og:*, viewport, generator, etc.).
3. **Scrape 2–5 key pages** identified from the map (pricing, contact/booking, product/service, about, signup) — same `formats`. These are the conversion-path pages.
4. **Run the DATA-QUALITY GATE** (below) on every scrape *before* using it. Reject non-200 / tiny / CMS-error pages.
5. **Derive the assessments** (nav depth, CTA inventory, form complexity, mobile responsiveness, JS/resource health, visual quality) from the scraped markdown + html + metadata + screenshot.

> **Multi-viewport is replaced, not lost.** Playwright's 1440/768/375 snapshots are replaced by: (a) Firecrawl's rendered **screenshot** (full-page render of the live, JS-executed page), plus (b) **responsive metadata** parsed from the returned HTML/metadata — the `<meta name="viewport">` value, presence of `@media` queries / responsive `<picture>`/`srcset`, fixed-width layout containers, and touch-target hints. This is the same responsiveness signal the bulk scorer's `mobile` dimension already derives from Firecrawl (`viewport_present`, `device_width`, `initial_scale`, `no_fixed_width`, `media_queries`, `touch_friendly`). For a true second render, optionally re-scrape once with `"mobile": true` (Firecrawl renders with a mobile viewport) and diff the two screenshots/HTML.

#### `/v1/scrape` — homepage (real curl)

```bash
curl -sS -X POST "$BASE/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ingatlan.com",
    "formats": ["markdown", "html", "links", "summary", {"type": "screenshot", "fullPage": true}],
    "onlyMainContent": false,
    "waitFor": 2500,
    "timeout": 45000,
    "blockAds": false,
    "removeBase64Images": true,
    "skipTlsVerification": false,
    "location": { "country": "HU", "languages": ["hu"] }
  }'
```

Notes on the options (all chosen to match what EVALUATE needs):
- `formats` — request everything in **one** call. `markdown` for content/readability + LLM-citation signal; `html` (rendered, post-JS) for DOM-level checks (heading hierarchy, alt-text ratio, JSON-LD, viewport tag, fixed widths, inline-style bloat); `links` for the link graph + broken-link candidates; `summary` for a fast content gist; `screenshot` (full-page) replaces the visual snapshot.
  - Newer Firecrawl takes screenshot as an object `{"type":"screenshot","fullPage":true}`. If your account is on the older string form, use `"screenshot@fullPage"` in the array instead (see fallback below).
- `onlyMainContent: false` — we want headers/footers/nav/CTAs, **not** just the article body (EVALUATE inventories nav + CTAs + footer).
- `waitFor: 2500` — let JS-rendered carousels / consent dialogs / lazy content settle (e.g. the ingatlan.com lazy-load skeletons, Cookiebot overlay).
- `timeout: 45000` — heavy portals need headroom.
- `removeBase64Images: true` — keeps the returned HTML measurable (the bulk scorer checks `no_large_base64`); we don't want inlined image bytes inflating `html_size`.
- `location: { country, languages }` — geo/locale the request (HU sites served Hungarian, correct regional CDN behavior).
- `blockAds: false` — we deliberately **keep** ads so the ad-density UX finding is observable (ingatlan.com's Adverticum interstitials are a real High pain point). Flip to `true` only if ads break rendering.

Older-account fallback (string formats, no object form):
```bash
curl -sS -X POST "$BASE/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ingatlan.com",
    "formats": ["markdown", "html", "links", "screenshot@fullPage"],
    "onlyMainContent": false,
    "waitFor": 2500,
    "timeout": 45000
  }'
```

#### `/v1/scrape` — optional second render for the mobile signal

```bash
curl -sS -X POST "$BASE/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ingatlan.com",
    "formats": [{"type": "screenshot", "fullPage": true}, "html"],
    "mobile": true,
    "waitFor": 2500,
    "timeout": 45000
  }'
```
Diff the desktop vs. `"mobile": true` screenshots/HTML to confirm responsive adaptation (hamburger nav, stacked forms, condensed footer) — this reproduces the cross-viewport check the old `browser_resize` loop did, in two calls instead of three snapshots.

#### `/v1/scrape` — a key conversion page (pricing example)

```bash
curl -sS -X POST "$BASE/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ingatlan.com/szolgaltatasok/arak",
    "formats": ["markdown", "html", "links"],
    "onlyMainContent": false,
    "waitFor": 2000,
    "timeout": 45000
  }'
```

#### `/v1/map` — URL inventory + IA (real curl)

```bash
curl -sS -X POST "$BASE/v1/map" \
  -H "Authorization: Bearer $FIRECRAWL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ingatlan.com",
    "search": "ar pricing kapcsolat contact hirdetes regisztracio",
    "includeSubdomains": true,
    "limit": 500
  }'
```
- The returned `links[]` array is the site's URL inventory → derive **navigation depth**, **information architecture**, and **subdomains_detected** (the old Playwright nav-tree walk). `includeSubdomains: true` surfaces the subdomain spread (e.g. `partner.`, `tudastar.`, `my-money.` for ingatlan.com).
- `search` (optional) ranks the map toward conversion-relevant pages so you know which 2–5 pages to scrape in step 3.

#### Async variant (large/slow sites)

For very large portals where a synchronous scrape may time out, kick off async and poll:
```bash
# Start
JOB=$(curl -sS -X POST "$BASE/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_KEY" -H "Content-Type: application/json" \
  -d '{"url":"https://ingatlan.com","formats":["markdown","html","links",{"type":"screenshot","fullPage":true}],"waitFor":2500}' \
  | sed -n 's/.*"id":"\([^"]*\)".*/\1/p')

# Poll until status == "completed"
curl -sS "$BASE/v1/scrape/$JOB" -H "Authorization: Bearer $FIRECRAWL_KEY"
```
(For per-page EVALUATE the synchronous call is normally enough; prefer it for simplicity.)

#### What Firecrawl returns (response envelope — this is the real shape)

A successful `/v1/scrape` returns (fields confirmed against `scores-v2/*/score.json` `metadata` blocks produced by the live scorer):

```json
{
  "success": true,
  "data": {
    "markdown": "....",
    "html": "<!doctype html>...rendered, post-JS...",
    "links": ["https://...", "..."],
    "summary": "One-paragraph gist of the page.",
    "screenshot": "https://service.firecrawl.dev/storage/.../screenshot.png",
    "metadata": {
      "title": "....",
      "description": "....",
      "language": "hu-HU",
      "og:title": "....", "og:description": "....", "og:image": "....", "og:url": "....", "og:site_name": "....", "og:type": "website",
      "twitter:card": "summary_large_image",
      "viewport": ["width=device-width, initial-scale=1"],
      "robots": "max-image-preview:large",
      "generator": ["WordPress 6.x", "All in One SEO ..."],
      "favicon": "https://.../favicon.ico",
      "canonical": "https://.../",
      "sourceURL": "https://www.ingatlan.com",
      "url": "https://ingatlan.com/",
      "statusCode": 200,
      "contentType": "text/html; charset=UTF-8",
      "scrapeId": "019e4f3a-....",
      "proxyUsed": "basic",
      "cacheState": "miss",
      "creditsUsed": 1
    }
  }
}
```

**Map of Firecrawl fields → EVALUATE outputs (this is how the old Playwright signals are reconstructed):**

| Old Playwright signal | Firecrawl source |
|---|---|
| `browser_navigate` reached page | `data.metadata.statusCode == 200` + non-empty `markdown` |
| Visual snapshot at 3 viewports | `data.screenshot` (full-page render) + optional `"mobile": true` re-scrape |
| Nav structure / IA depth | `/v1/map` `links[]` + in-page `data.links` + nav blocks in `data.html` |
| Subdomains detected | `/v1/map` with `includeSubdomains: true` |
| CTA inventory | anchors/buttons in `data.html` + `data.markdown` link text |
| Form complexity | `<form>`/`<input>`/`<label>` count + types in `data.html` |
| Mobile responsiveness | `metadata.viewport` + `@media`/`srcset`/fixed-width scan of `data.html` (+ mobile re-scrape) |
| JavaScript errors / broken resources | broken/4xx links from `data.links`; rendered-vs-source gaps; Firecrawl `warning`/`statusCode` per page (note: Firecrawl does **not** expose the JS console — see Known Differences) |
| Visual design quality | `data.screenshot` + structural read of `data.html` (heading hierarchy, density, ad blocks) |
| Tech stack (`confirmed_via_crawl`) | `metadata.generator`, og/twitter tags, framework fingerprints + script src hosts in `data.html`, CDN hints from Leg 3 headers |

#### Extract (unchanged deliverables — same fields the old spec extracted)
- Navigation depth and information architecture
- CTA inventory (what they want users to do)
- Form complexity (how hard is it to convert)
- Mobile responsiveness quality
- JavaScript errors and broken resources (best-effort — see Known Differences)
- Visual design quality assessment

#### Anti-bot handling (Firecrawl-aware)

Firecrawl handles most anti-bot transparently (rotating proxies, JS rendering). Escalate **only on failure**, in this order — never circumvent beyond Firecrawl's own options:

1. Default scrape (`proxy: "basic"` implied).
2. If blocked (403 / challenge HTML / empty body), retry once with `"proxy": "stealth"` and a longer `"waitFor": 5000`:
   ```bash
   curl -sS -X POST "$BASE/v1/scrape" \
     -H "Authorization: Bearer $FIRECRAWL_KEY" -H "Content-Type: application/json" \
     -d '{"url":"https://target.example","formats":["markdown","html","links",{"type":"screenshot","fullPage":true}],"proxy":"stealth","waitFor":5000,"timeout":60000}'
   ```
3. If still blocked after the stealth retry:
   - Log: `"Direct crawl blocked by [Cloudflare challenge / 403 / bot wall] even with Firecrawl stealth proxy. Leg 1 data unavailable."`
   - Do **NOT** attempt any other circumvention.
   - **Set `legs_completed` to exclude `"crawl"`** and continue on Legs 2+3 (they always succeed).
   - Flag in the report exactly as before: `"Site Health score based on Legs 2+3 only (direct crawl blocked)"`.
   - **Never fabricate** crawl-derived metrics. If a page wasn't measured, say so — never guess a number (skill operating rule).

---

### LEG 2: Sentiment Mining (WebSearch) — UNCHANGED

**Tools:** `WebSearch`, `WebFetch`.

**Search queries (adapt `[target]` to the actual site/company name):**
```
"[target] reviews"
"[target] vélemények" (Hungarian)
"[target] complaints"
"[target] panasz"
"[target] site:reddit.com"
"[target] site:trustpilot.com"
"[target] Google reviews"
"[target] Árukereső vélemények"
"[target] app store reviews"
"[target] vs [competitor]" (users comparing)
"[target] alternative" (users looking to leave)
"[target] frustrating OR annoying OR terrible OR slow"
```

**Extract and categorize:**
- **Pain points:** what users complain about most (ranked by frequency)
- **Praise points:** what users love (don't ignore strengths)
- **Feature requests:** what users wish the site had
- **Competitor comparisons users make:** "I switched to X because…"
- **Churn signals:** "looking for alternative to [target]"
- **NPS proxy:** ratio of positive to negative sentiment across sources

**Scoring:**
- 5+ independent complaints about the same issue = Critical pain point
- 3-4 = High pain point
- 1-2 = Noted pain point
- User-initiated competitor comparisons are the highest-value data for the teaser.

**This leg ALWAYS succeeds** (public data, no anti-bot risk).

---

### LEG 3: Technical Audit (curl + WebSearch) — UNCHANGED (keeps curl)

**Tools:** `curl` (direct public-endpoint fetches), `WebSearch`. (`WebFetch` also works; **curl is kept** because these endpoints are plain text, anti-bot-free, and curl gives us raw bytes + response headers for the security/tech-stack checks.)

**Direct fetches (public endpoints, no anti-bot risk) — real curl:**
```bash
# robots.txt — crawler access + AI-bot rules + disallowed paths
curl -sSL -A "Mozilla/5.0 (compatible; BizAudit/1.0)" "https://ingatlan.com/robots.txt"

# sitemap.xml — page count, update frequency, structure (follow redirects; many sites use sitemap_index.xml)
curl -sSL -A "Mozilla/5.0 (compatible; BizAudit/1.0)" "https://ingatlan.com/sitemap.xml"

# llms.txt — AI-readiness signal (presence = forward-thinking)
curl -sSL -A "Mozilla/5.0 (compatible; BizAudit/1.0)" "https://ingatlan.com/llms.txt"

# security.txt — modern security disclosure standard
curl -sSL -A "Mozilla/5.0 (compatible; BizAudit/1.0)" "https://ingatlan.com/.well-known/security.txt"

# Response headers — HSTS, CSP, server, CDN, cache, compression (for technical + tech_stack)
curl -sSI -A "Mozilla/5.0 (compatible; BizAudit/1.0)" "https://ingatlan.com/"
```
> Capture the **HTTP status** of each (a `200` vs `404` is itself the signal recorded in `llms_txt_present` / `sitemap_xml_present` / `security_txt_present`). For robots/sitemap a `404` is recorded as "present: false", not an error.

**Search-based checks:**
```
WebSearch: "[target] site speed PageSpeed"
WebSearch: "[target] technology stack built with"
WebSearch: "[target] SEO audit"
WebSearch: "site:[target] inurl:api" (public API presence)
```

**Extract:**
- robots.txt: which crawlers are allowed/blocked (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot, AhrefsBot, etc.)
- Sitemap: page count, update frequency, structure
- llms.txt: AI-readiness signal (presence = forward-thinking)
- Technology stack: frameworks, CDN, analytics, A/B testing, CRM integrations (cross-reference Leg 1 `metadata.generator` + script hosts with Leg 3 response headers)
- Page speed data (from public tools / cached results)
- SSL certificate validity + security headers (from `curl -I`)

**This leg ALWAYS succeeds** (public endpoints only).

---

## DATA-QUALITY GATE (NEW — applies to every Leg 1 Firecrawl result)

Run this gate on **each** scraped page **before** any score or finding is derived from it. Its job is to stop a blocked/empty/error page from being scored as if it were the real site. If a page fails the gate, it is excluded from Leg 1 analysis (and if the **homepage** fails, Leg 1 is marked unavailable per the anti-bot ladder above).

A scrape **PASSES** only if ALL of the following hold:

1. **HTTP success:** `data.metadata.statusCode` is `200`–`299`. Reject `3xx`-final / `4xx` / `5xx`.
2. **Non-trivial body:** rendered `data.html` length **> 5,000 bytes** AND `data.markdown` length **> 300 chars**. (Reject near-empty shells. For reference, real pages in this corpus run ~100 KB of HTML, e.g. dhdentaleurope ≈ 103 KB.)
3. **Real content, not a wall:** `data.markdown` is not dominated by challenge/consent text. Reject if the body is essentially one of:
   - Cloudflare / anti-bot interstitial — markers: `"Checking your browser"`, `"Just a moment"`, `"cf-chl"`, `"Attention Required! | Cloudflare"`, `"Please enable JavaScript and cookies"`, `"Request unsuccessful. Incapsula"`, `"Access denied"`.
   - **CMS / framework error page** — markers: `"Error establishing a database connection"`, `"503 Service Temporarily Unavailable"`, `"This site can’t be reached"`, `"There has been a critical error on this website"` (WP), `"Whitebox/Whoops" / Laravel stack trace`, `"NextJS"`/`"Application error: a client-side exception"`, `"500 Internal Server Error"`, `"account has been suspended"`, default `"Index of /"` listing, parked-domain text (`"buy this domain"`, `"domain is for sale"`).
4. **Title present & not an error title:** `data.metadata.title` is non-empty and is not one of `["403 Forbidden","404 Not Found","Access Denied","Just a moment...","Attention Required!"]`.
5. **Right host:** `data.metadata.url` resolves to the target domain (or a known subdomain). Reject if it redirected off-domain to a parking/registrar/marketplace host.

**On gate FAIL:**
- Record the reason in a `data_quality` block (see schema addition below) — e.g. `"homepage rejected: statusCode 403 + Cloudflare challenge body"`.
- For a **non-home** key page: skip that page, keep the others, note the skip.
- For the **homepage**: trigger the anti-bot ladder (stealth retry → if still failing, drop `"crawl"` from `legs_completed`, score on Legs 2+3, flag in report). **Never** let a failed page contribute a fabricated number.

> The gate is the Firecrawl-era equivalent of the old "anti-bot handling" + "no failed network requests" sanity check, made explicit so a JS-rendered error page can't masquerade as a healthy site.

---

## Output

Combine all three legs into **the same structured JSON as before** — schema is **backward-compatible**. Downstream steps read these keys unchanged. The headline contract:

```json
{
  "target": "ingatlan.com",
  "timestamp": "2026-05-29T...",
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
  "critical_pain_points": [],
  "praise_points": [],
  "user_feature_requests": [],
  "user_competitor_comparisons": [],
  "tech_stack": [],
  "crawler_access": { "GPTBot": "blocked", "ClaudeBot": "allowed" },
  "llms_txt_present": false
}
```

**All richer keys the live pipeline already emits remain identical and required** (see `ingatlan-com/reports/site_health.json` for the canonical full shape): `scoring_methodology`, `high_pain_points`, `noted_pain_points`, `churn_signals`, `tech_stack` (as the object form `{confirmed_via_crawl, confirmed_via_search, inferred}` when known), `robots_txt_disallowed_paths`, `security_txt_present`, `sitemap_xml_present`, `sitemap_pages`, `navigation_structure`, `cta_inventory`, `console_errors`, `network_issues`, `mobile_assessment`, `visual_design_assessment`, `traffic_data`, `company_info`, `notable_features`, `regulatory_history`, `opportunities_for_disruption`.

**Field-population notes under Firecrawl (so the same keys stay populated):**
- `console_errors` — Firecrawl does not expose the browser JS console. Populate from (a) Firecrawl per-page `warning`/non-200 signals, (b) WebSearch findings, and (c) rendered-HTML red flags (deprecated SDK snippets, FedCM/GSI markers, mixed content). If genuinely unobservable, emit `[]` and add one `network_issues` note: `"JS console not captured (Firecrawl renders headless without console export); errors inferred from HTML + search only."` — **do not invent console lines.**
- `network_issues` — derive from broken/4xx entries in `data.links`, redirect chains, and Leg 3 header anomalies, instead of Playwright's `browser_network_requests`.
- `mobile_assessment` / `visual_design_assessment` — written from the Firecrawl screenshot(s) + rendered HTML structure (and the optional `"mobile": true` re-scrape), same prose depth as before.
- `tech_stack.confirmed_via_crawl` — from `metadata.generator`, og/twitter tags, framework/script fingerprints in `data.html`, plus CDN/server from Leg 3 headers.

**Schema ADDITION (additive only — does not break consumers):**
```json
"data_quality": {
  "gate_passed_pages": ["https://ingatlan.com/", "https://ingatlan.com/.../arak"],
  "gate_failed_pages": [
    { "url": "https://...", "reason": "statusCode 403 + Cloudflare challenge body" }
  ],
  "fetch_method": "firecrawl",
  "homepage_status": 200,
  "screenshot_url": "https://service.firecrawl.dev/storage/.../screenshot.png"
}
```
This mirrors the bulk scorer's provenance fields (`method`, `fetch_method`, `statusCode`, `creditsUsed`) and is purely additional — existing readers ignore unknown keys.

Save to `evolution-audits/{slug}/reports/site_health.json` (path unchanged).

---

## Known Differences vs. the Playwright spec (carry-forward caveats)

- **No JS console.** Playwright's `browser_console_messages` gave literal console errors/warnings (the ingatlan.com FedCM/GSI/Turbo lines). Firecrawl renders headless without exporting the console, so `console_errors` is now best-effort/inferred (see note above). This is the one genuine fidelity loss; everything else is parity or better.
- **No live network waterfall.** `browser_network_requests` is replaced by link-graph + header inspection. Double-fired analytics calls (the GA4 double `page_view` finding) won't be directly visible; capture such issues from HTML tags / search if surfaced.
- **Viewport renders.** Three discrete viewport snapshots → one full-page desktop screenshot + responsive-metadata parse, optionally a second `"mobile": true` render. Equivalent coverage of the responsiveness question in ≤2 calls.

---

## Quick reference — minimal happy-path EVALUATE call sequence

```bash
FIRECRAWL_KEY="fc-..."           # from your own env/config
BASE="https://api.firecrawl.dev"
T="https://ingatlan.com"

# Leg 1a: map the site
curl -sS -X POST "$BASE/v1/map" -H "Authorization: Bearer $FIRECRAWL_KEY" -H "Content-Type: application/json" \
  -d "{\"url\":\"$T\",\"includeSubdomains\":true,\"limit\":500}"

# Leg 1b: scrape homepage (content + html + links + screenshot + metadata)
curl -sS -X POST "$BASE/v1/scrape" -H "Authorization: Bearer $FIRECRAWL_KEY" -H "Content-Type: application/json" \
  -d "{\"url\":\"$T\",\"formats\":[\"markdown\",\"html\",\"links\",\"summary\",{\"type\":\"screenshot\",\"fullPage\":true}],\"onlyMainContent\":false,\"waitFor\":2500,\"timeout\":45000,\"removeBase64Images\":true,\"location\":{\"country\":\"HU\",\"languages\":[\"hu\"]}}"
# → RUN DATA-QUALITY GATE on the result before using it.

# Leg 1c: scrape 2-5 key pages from the map (repeat per page)
# Leg 1d (optional): mobile re-render for the responsive diff (..."mobile":true...)

# Leg 3: technical (curl) — robots / sitemap / llms / security / headers
curl -sSL "$T/robots.txt"
curl -sSL "$T/sitemap.xml"
curl -sSL "$T/llms.txt"
curl -sSL "$T/.well-known/security.txt"
curl -sSI "$T/"

# Leg 2: sentiment via WebSearch/WebFetch (queries above) — always succeeds.
```
