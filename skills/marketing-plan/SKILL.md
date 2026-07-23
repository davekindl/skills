---
name: marketing-plan
description: Use when the user needs a marketing plan, go-to-market strategy, outreach plan, lead generation strategy, or any structured business growth document. Trigger on phrases like 'marketing plan', 'outreach strategy', 'how do we get clients', 'lead generation', 'B2B strategy', 'growth plan', 'help me sell this', 'attract customers', or any request that requires multi-perspective strategic thinking about customer acquisition.
---

# Marketing Plan Generator

Orchestrate parallel expert brainstorms into a unified, actionable marketing plan delivered as a print-ready HTML document (save as PDF from browser).

## Shared Infrastructure
- **Discovery questions:** Read `D:\.claude\skills\shared\business\discovery-questions.md` for common intake patterns
- **Sibling skills:** business-mvp (idea validation), grand-slam-offer (Hormozi framework)

## Process

### Phase 1: Discovery (ask the user)

Before doing anything, ask these questions in a single message. Do not proceed until answered.

```
A tervhez szükségem van néhány alapinfóra:

1. **Mi a termék/szolgáltatás?** (Röviden: mit árul, mit kínál?)
2. **Ki a célcsoport?** (Cégek? Magánszemélyek? Melyik iparág/régió?)
3. **Mi a fő probléma?** (Miért nem jönnek az ügyfelek? Mi nem működik most?)
4. **Van már online jelenlét?** (Weboldal, social media — ha igen, URL-eket kérek)
5. **Költségkeret?** (Van marketing büdzsé, vagy nulla forintból indulunk?)
6. **Magyar vagy angol?** (A terv és a sablonok nyelve)
7. **Van más, amit tudnom kell?** (Szezonalitás, versenytársak, korábbi próbálkozások)
```

If the user already provided most of this context in their message, only ask what's missing. Don't re-ask what's obvious.

### Phase 2: Persona Selection

Based on the discovery answers, select 4-6 expert personas from the pool below. Not every persona applies to every case — pick what fits.

**Present the selection to the user for verification before proceeding.** Format:

```
Az alábbi szakértői nézőpontokból dolgozom ki a tervet:

1. **[Persona name]** — [1 sentence: what angle they cover]
2. **[Persona name]** — [1 sentence]
...

A végeredmény: [1-2 sentence description of the plan type — e.g., "B2B megkeresési stratégia email sablonokkal, célcég listával, és éves kampánynaptárral"]

Jól hangzik, vagy módosítanál?
```

Wait for confirmation. If the user adjusts, adapt.

### Persona Pool

| Persona | When to include | What they cover |
|---------|----------------|-----------------|
| **Értékesítési stratéga** | Always for B2B | Email sorozatok, LinkedIn megkeresés, mérőszámok, listaépítés, tárgysorok |
| **Márkaépítő** | When positioning is unclear or competition is strong | Pozicionálás, üzenetrendszer, csomagnevek, versenyelőny érvek |
| **HR / Döntéshozó belső nézőpont** | When selling to corporations (team building, SaaS, enterprise) | Büdzsé-ciklusok, jóváhagyási folyamat, fájdalompontok, döntési kritériumok |
| **Gyors növekedési taktikus** | Always | Zero-budget azonnali lépések, guerrilla taktikák, automatizáció, referral rendszer |
| **Iparági szakértő** | When the industry has agencies, platforms, or partnership ecosystems | Partnerügynökségek, platformok, árazási benchmark, szezonalitás, trendek |
| **Tartalomstratéga** | When content/social media is a key channel | Tartalomnaptár, videó/fotó terv, közösségi média stratégia |
| **Közösségépítő** | When community, local presence, or word-of-mouth matters | Facebook csoportok, helyi partnerek, események, ajánlási rendszer |
| **Digitális hirdetési szakértő** | When paid ads are part of the strategy | Google Ads, Facebook/Instagram hirdetések, retargeting, költségoptimalizálás |

### Phase 3: Research (if URLs provided)

If the user provided website or social media URLs, dispatch a research agent FIRST:

- Audit the website (structure, messaging, pricing visibility, SEO)
- Audit social media (followers, posting frequency, content types, engagement, gaps)
- Check Google reviews / ratings
- Search for the brand name + relevant keywords
- Compile into a structured findings summary

This becomes input for all persona brainstorms.

### Phase 4: Parallel Brainstorms

Dispatch each selected persona as a **parallel Agent**. Each gets:

1. The full discovery brief (client info, problem, target audience)
2. Research findings (if Phase 3 ran)
3. Language instruction (Hungarian or English)
4. Specific brainstorm mandate (see persona descriptions above)

**Critical:** Each agent brainstorms INDEPENDENTLY. Do not chain them. Launch all in parallel.

Each agent prompt must end with: "Output everything in [Hungarian/English]. Be specific, actionable, and practical. Include copy-paste-ready templates where applicable."

### Phase 5: Compile

Once all persona agents return, synthesize into a single unified plan:

1. **Deduplicate** — remove redundant ideas across personas
2. **Prioritize** — rank by impact and feasibility
3. **Structure** into the output template (see below)
4. **Preserve** copy-paste-ready templates (emails, LinkedIn messages, post scripts)
5. **Add** the research audit as a final section (if Phase 3 ran)

### Phase 6: Generate HTML Document

Create a single print-optimized HTML file with:

- Professional A4 layout with `@page` CSS
- Google Fonts (Inter + DM Serif Display)
- Cover page with client name, document type, date, author
- Table of contents
- Part I: Raw persona brainstorms (labeled, brief)
- Part II: Unified deduplicated plan (the actionable output)
- Styled tables, callout boxes, email template boxes
- Page breaks between major sections
- Print stylesheet

Save to the working directory as `[client-slug]-marketing-terv.html`.

Tell the user: "Nyisd meg böngészőben, majd Ctrl+P → Mentés PDF-ként."

## Output Template (sections to include — adapt per case)

Not every section applies to every plan. Include what's relevant.

| Section | When to include |
|---------|----------------|
| Vezetői összefoglaló | Always |
| Célcsoport és döntéshozók | Always |
| Pozicionálás és csomagok | When selling services/products |
| Megkeresési stratégia + email sablonok | B2B |
| Listaépítés módszertan | B2B |
| Partnerségi csatornák | When ecosystem exists |
| Tartalomterv és referenciák | When content is a channel |
| Azonnali teendők (ezen a héten) | Always |
| Éves kampány naptár | When seasonality matters |
| Online jelenlét audit | When URLs were provided |
| Árazási benchmark | When pricing is unclear |
| Kockázatok | Always |

## Language Handling

- If Hungarian: all section headers, body text, email templates, and UI copy in Hungarian. Use natural Hungarian — avoid forced translations of common terms (LinkedIn, SEO, B2B stay as-is). Replace unnecessary English jargon: "pipeline" → "értékesítési tölcsér", "quick wins" → "azonnali teendők", "content" → "tartalom", "social proof" → "referenciák".
- If English: standard business English throughout.
