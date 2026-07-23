---
name: content-atomizer
description: "Take ONE long-form content piece and produce 10 platform-specific derivatives. Input: blog post, video transcript, podcast, book chapter (URL, file, or paste). Output: LinkedIn post, X thread, newsletter section, Instagram carousel script, quote graphics text, short-form video script, podcast show notes, email sequence, infographic outline, blog summary with SEO. Trigger on: 'atomize this', 'repurpose this content', 'content atomizer', 'turn this into social posts', '1 to 10', 'repurpose for LinkedIn', 'make a thread from this', 'create social content from', 'atomize [url]', 'content repurposing'. Also triggers when you share a blog post, article, or transcript and wants it distributed across platforms."
allowed-tools: Read, Write, Glob, Grep, WebFetch
---

# CONTENT ATOMIZER

> One piece in, ten pieces out. Platform-native, not copy-pasted. Quality-gated.

## Platform Specs (hard constraints per format)

| # | Format | Length | Structure Rule | Engagement Driver |
|---|--------|--------|---------------|-------------------|
| 1 | **LinkedIn** | 1,300-1,900 chars sweet spot | Hook in first 140 chars (mobile). Short paragraphs. End with question. | Dwell time + comment depth |
| 2 | **X Thread** | 280/tweet, 6-8 tweets | Tweet 1 = hook. Each tweet = one idea. Final = CTA + link in reply. | Saves + follows. 6-9 tweets = 3.1x saves |
| 3 | **Newsletter** | 300-600 words | Headline + 2-3 para summary + key takeaway bullet + CTA | Click-through rate |
| 4 | **IG Carousel** | 8-10 slides, <30 words/slide | Slide 1 = hook (<10 words). 1080x1350 portrait. Last = "save this" CTA | Swipe-through + saves |
| 5 | **Quote Graphics** | <150 chars/graphic | 1080x1080 square. Text <20% of area. High contrast. Attribution. | Saves + shares |
| 6 | **Video Script** | 15-30 sec (75 words for 30s) | Hook 2-3 sec. Hook > Problem > Solution > CTA. 9:16 vertical. | Completion rate |
| 7 | **Podcast Notes** | 300-600 words | Title with keyword. Summary. Numbered takeaways. Timestamps. Resources. | SEO discovery |
| 8 | **Email Sequence** | 3-5 emails, 200-400 words each | E1: hook. E2: evidence. E3: framework. E4: proof. E5: CTA. | Open rate + clicks |
| 9 | **Infographic** | 6-8 sections | Title > Problem stat > Key findings > Framework > Data > CTA. 1080px wide. | Saves + backlinks |
| 10 | **Blog Summary** | 150-160 chars meta, 1,000-1,500 words post | H2 every 200-300 words. TL;DR at top. Bullets. Internal links. | Organic search |

## 3-Pass Extraction Pipeline

### Pass 1: Skeleton Extraction
Parse source into argument map: thesis, supporting claims (3-7), evidence per claim, counterarguments, conclusion/CTA.

### Pass 2: Moment Mining
Scan for 6 types of scroll-stopping content:
1. **Contrarian takes** -- challenges conventional wisdom
2. **Data points** -- specific numbers, percentages, findings
3. **Frameworks** -- step-by-step processes, matrices, models
4. **Stories** -- anecdotes, case studies, transformations
5. **Quotable lines** -- standalone sentences (<150 chars)
6. **Questions** -- rhetorical or provocative

### Pass 3: Platform Routing
Map moments to highest-impact output:
- Contrarian → LinkedIn hook, X thread opener
- Data points → Quote graphic, infographic, newsletter stat
- Frameworks → Carousel (1 step/slide), blog, email sequence
- Stories → Video script, podcast notes
- Quotable lines → Quote graphics, standalone tweet
- Questions → LinkedIn CTA, email subject lines

## Quality Gate (before generation)

Source must contain 3+ of the 6 moment types. If fewer:
```
"This source lacks sufficient atomic content for 10-format repurposing.
Found: [list what exists]. Missing: [list gaps].
Recommendation: [strengthen the source | atomize to fewer formats]"
```

Reject weak sources. Don't multiply mediocrity.

## Workflow

```
INPUT:
├── URL provided?    → fetch article text with best AVAILABLE web tool
│                       (prefer firecrawl-scrape skill — handles JS/SPA;
│                        fall back to WebFetch if firecrawl unavailable)
├── YouTube URL?     → yt-search skill for transcript
├── File path?       → Read tool
└── Raw paste?       → Accept directly

EXTRACT:
├── Pass 1: Skeleton (thesis, claims, evidence)
├── Pass 2: Moment mining (6 types)
└── Pass 3: Quality gate (3+ types required)

GENERATE (sequential, each format gets platform spec constraints):
├── For each of 10 formats:
│   1. Load platform spec
│   2. Select relevant moments
│   3. Generate in platform-native tone
│   4. Validate against char limits
│   5. Insert [REVIEW] markers for personal voice
└── Done

OUTPUT:
├── content-atoms/{slug}/index.md          (extraction summary)
├── content-atoms/{slug}/linkedin.md
├── content-atoms/{slug}/x-thread.md
├── content-atoms/{slug}/newsletter.md
├── content-atoms/{slug}/carousel.md
├── content-atoms/{slug}/quotes.md
├── content-atoms/{slug}/video-script.md
├── content-atoms/{slug}/show-notes.md
├── content-atoms/{slug}/email-sequence.md
├── content-atoms/{slug}/infographic.md
├── content-atoms/{slug}/blog-summary.md
└── content-atoms/{slug}/calendar.md       (2-week distribution schedule)
```

## Distribution Calendar (auto-generated)

Staggered to prevent self-cannibalization:
- Day 1: LinkedIn post
- Day 2: X thread
- Day 3: Newsletter section
- Day 4-5: Carousel + quote graphics
- Week 2: Video script, email sequence, blog summary

## Tone Modifiers (per platform)

| Platform | Tone | Register |
|----------|------|----------|
| LinkedIn | Authoritative peer | Professional, thought-leader |
| X/Twitter | Sharp conversationalist | Concise, opinionated |
| Instagram | Visual teacher | Accessible, aspirational |
| Newsletter | Trusted advisor | Warm, personal, exclusive |
| Email | Direct consultant | Problem-solution, clear CTA |

## Anti-Patterns
1. **Copy-paste across platforms:** Algorithms detect cross-posts. Rewrite from the argument, not the text.
2. **"In my latest blog post...":** Nobody cares. Lead with the insight.
3. **Uniform tone:** LinkedIn voice on TikTok is cringe. Apply tone modifiers.
4. **Atomizing weak sources:** Quality gate rejects <3 moment types.
5. **Simultaneous publishing:** Stagger across 2 weeks per the calendar.
6. **Wrong formatting:** Enforce platform specs as hard constraints. Fail if violated.
7. **No editorial pass:** Insert `[REVIEW: add personal angle]` markers. AI drafts, human authenticates.

## Tool Integration

| Tool | Usage |
|------|-------|
| firecrawl-scrape skill | Preferred web fetcher — handles JS/SPA pages. Use if available. |
| WebFetch | Fallback web fetcher when firecrawl is unavailable (e.g. published users without firecrawl) |
| yt-search skill | YouTube transcript extraction |
| Read | Load local files |
| Write | Save all 10 output files + calendar |
| Glob | Check for existing atomized content (prevent re-atomizing) |
| Grep | Search existing outputs for thematic overlap |
