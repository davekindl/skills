# Schema Templates — JSON-LD (Phase 7)

The three schema types every article ships with (Phase 7, deliverable 3). Fill the `[...]` placeholders from the approved brief and the final article. Validate before delivery: every URL absolute, dates in ISO 8601, no empty fields left as placeholders.

## 1. Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[meta title — max 60 characters, matches the title tag]",
  "description": "[meta description — 140-160 characters]",
  "author": {
    "@type": "Person",
    "name": "[named author — required by the GEO core checks]",
    "url": "[author bio or about page URL]",
    "jobTitle": "[credential that supports E-E-A-T]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[site or brand name]",
    "url": "[site root URL]"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD — keep fresh; update on every content refresh]",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "[canonical article URL]"
  }
}
```

Notes: `dateModified` is the field the refresh schedule (Phase 7, deliverable 5) exists to keep honest — bump it only when the content actually changes. AI engines favor fresh pages, so a stale `dateModified` costs citations.

## 2. FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[question exactly as it appears in the article's FAQ section]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[the brief, extractable answer — answer-first, no preamble]"
      }
    },
    {
      "@type": "Question",
      "name": "[next question]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[next answer]"
      }
    }
  ]
}
```

Notes: one `Question` object per Q&A pair from the article's FAQ section (Phase 5 requires 5-10 pairs). The `name` and `text` must match the on-page FAQ verbatim — mismatched schema is worse than no schema.

## 3. BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "[site root URL]"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[section or topic-cluster pillar name]",
      "item": "[pillar page URL]"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[article title]",
      "item": "[canonical article URL]"
    }
  ]
}
```

Notes: mirror the topic-cluster map from Phase 2 — the middle crumb should be the pillar page the article satellites around. This doubles as one of the article's required internal links.

## Delivery

Embed each block in the article HTML as `<script type="application/ld+json">...</script>`, or hand off as separate snippets if the CMS injects schema itself. All three blocks can also be combined into a single `@graph` array under one `@context` if the target platform prefers a single script tag.
