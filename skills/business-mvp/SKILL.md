---
name: business-mvp
description: Use when the user has a business idea and wants to validate it, build a showcase website, and create a business plan. Trigger on phrases like 'business idea', 'startup idea', 'I want to build', 'validate this idea', 'build an MVP', 'create a business', 'side hustle', 'is this viable', 'how would this work as a business', 'build a landing page for this idea', 'üzleti ötlet', or any early-stage concept that needs brainstorming, a showcase site, and a go-to-market plan.
---

# Business MVP Generator

Turn a raw business idea into three deliverables: validated concept, showcase website, and business plan -- all in one session.

## Shared Infrastructure
- **Discovery questions:** Read the discovery-questions reference for common intake patterns
- **Sibling skills:** marketing-plan (go-to-market strategy), grand-slam-offer (Hormozi framework)

## Deliverables

1. **Validated concept** — multi-persona brainstorm confirms (or kills) viability
2. **Showcase website** — standalone HTML landing page with dummy listings/content, ready to share
3. **Business plan** — print-ready HTML document (PDF via Ctrl+P) with financials, outreach templates, target lists, and timeline

## Process

### Phase 1: Discovery

Ask only what you need. Maximum 10 questions. Skip what's obvious from context.

**Core questions (always ask):**
1. Mi az ötlet? (1-2 mondatban)
2. Ki a célcsoport? (Ki fizet, ki használja?)
3. Mi a probléma, amit megold?
4. Van földrajzi fókusz? (Város, régió, ország?)
5. Magyar vagy angol? (Weboldal + terv nyelve)

**Conditional questions (ask if not obvious):**
6. Van hasonló megoldás a piacon? (Versenytársak?)
7. Hogyan keresne pénzt? (Van ötlet a bevételi modellre?)
8. Mennyi idő/pénz áll rendelkezésre? (Hobbi vagy full-time? Budget?)
9. Van már domain/márkanév ötlet?
10. Van célcég/partner, akit már ismer? (Meglévő hálózat?)

Do not ask all 10 if the user already provided context. Adapt. If the idea description is rich enough, you may only need 2-3 clarifying questions.

### Phase 2: Persona Selection + Plan Preview

Select 4-6 brainstorm personas from the pool. Present to user:

```
Ezekből a nézőpontokból gondolom végig az ötletet:

1. **[Persona]** — [mit vizsgál]
2. **[Persona]** — [mit vizsgál]
...

A végeredmény:
- Showcase weboldal (önálló HTML, megosztható)
- Üzleti terv PDF-ben (pénzügyi terv, megkeresési sablonok, célcég lista, ütemterv)

Jól hangzik?
```

Wait for confirmation.

### Persona Pool

| Persona | When to include | Brainstorm focus |
|---------|----------------|------------------|
| **Piactér stratéga** | Marketplace / platform ideas | Üzleti modell, jutalék, bizalmi mechanizmusok, hidegindítás, bevételi előrejelzés |
| **Logisztikai tervező** | Physical goods, delivery, storage | Szállítás, tárolás, lefedett terület, partnerhálózat, szezonalitás |
| **Felhasználói kutatás** | Always | Eladó/vevő/felhasználó perszonák (3+3), UX, minimum életképes felület, bizalmi jelek |
| **Versenytárs-elemző** | Always | Létező megoldások, piaci rések, nemzetközi referenciák, szabályozási háttér |
| **Helyi piaci szakértő** | Regional / local focus | Régió-specifikus kereslet, szezonalitás, partnerek, helyi közösségek |
| **Növekedési taktikus** | Always | Zero-budget indulás, first 30 days playbook, guerrilla taktikák, referral rendszer |
| **Tartalomstratéga** | When brand/content matters | Márkanév javaslatok, szlogen, vizuális irány, social media stratégia |
| **Pénzügyi elemző** | When monetization is complex | Árazási modellek, unit economics, break-even, 3 éves előrejelzés |

### Phase 3: Parallel Research + Brainstorms

Launch in parallel:

**Research agents (if applicable):**
- Competitor/market research — search for existing solutions, market size, regulations
- Target company/partner research — find real companies to partner with or sell to
- Social/online audit of competitors

**Brainstorm agents:**
- Each selected persona gets the full brief + discovery answers
- Each brainstorms independently
- Language instruction included

All agents run in parallel. Do not chain.

### Phase 4: Build Showcase Website

Create a standalone single-file HTML landing page. No external dependencies except Google Fonts CDN.

**Website must include:**
- Navigation bar with logo/brand name
- Hero section with value proposition + CTA
- Trust bar (3-4 trust signals)
- "How it works" section (3 steps)
- Sample listings / products / services (6+ dummy items with realistic details — real brand names, real locations, realistic pricing with discount badges)
- Categories grid (if applicable)
- "Why us" / differentiator section
- Region / coverage section (if local business)
- CTA section with pricing model explanation
- Footer

**Design principles:**
- Modern, clean, light theme (not dark luxury — this is a marketplace/service site)
- Mobile responsive
- Inter + DM Serif Display from Google Fonts
- Warm accent color that fits the brand
- Dummy product images as colored gradient placeholders with unicode icons (no external images needed)
- If KIE.AI API key is available in CLAUDE.md, optionally generate 2-3 hero/product images

**Save as:** `[slug]-standalone.html` in working directory. Must open directly in browser with zero dependencies.

### Phase 5: Build Business Plan

Create a print-optimized HTML document covering:

**Always include:**
- Borítólap (cover page with brand, title, author, date)
- Tartalomjegyzék
- Vezetői összefoglaló (executive summary with key stats)
- A probléma (pain points for both sides of the market)
- Piacelemzés és versenytársak (with real competitor data from research)
- Üzleti modell és bevételi források (table: revenue stream, model, pricing, timeline)
- Célcsoportok és perszonák (from UX researcher brainstorm)
- Pénzügyi terv (startup costs, 3-year revenue forecast)
- Azonnali teendők (first week / first month / decision checkpoints)
- Kockázatok és mitigáció

**Include if applicable:**
- Logisztika és működés (for physical goods/services)
- Marketing és ügyfélszerzés (channels, campaigns, seasonal calendar)
- Hideg megkeresés sablonok (3 email templates: general, premium, partner)
- Célcégek listája (real companies from research, with contact info)
- Ütemterv — első 12 hónap (visual timeline)
- Jogi és szabályozási környezet

**Design:** Same print-ready A4 HTML as marketing-plan skill (Inter + DM Serif Display, @page CSS, callout boxes, styled tables, email template boxes, page breaks).

**Save as:** `[slug]-uzleti-terv.html` (or `business-plan.html` if English)

### Phase 6: Deliver

Present both files to the user:

```
Kész! Két fájl:

1. **[slug]-standalone.html** — Showcase weboldal ([X] KB, önálló, böngészőben megnyitható)
2. **[slug]-uzleti-terv.html** — Üzleti terv (Ctrl+P → PDF mentés)

[Ha fut szerver:] Előnézet: http://localhost:XXXX/[filename]
```

## Language Handling

Same as marketing-plan skill:
- Hungarian: natural language, no forced translations. LinkedIn/SEO/B2B/MVP stay as-is.
- English: standard business English.
- Website and business plan must be in the same language (whichever user chose).

## Quality Checklist

Before delivering, verify:
- [ ] Showcase HTML opens in browser with no errors, no external dependencies except Google Fonts
- [ ] All dummy listings have realistic details (real brands, real locations, real pricing)
- [ ] Business plan has real competitor data (not placeholder)
- [ ] Business plan has real target companies with contact info (if B2B)
- [ ] Email templates are copy-paste ready in the correct language
- [ ] Financial projections are internally consistent
- [ ] Both files are in the working directory
