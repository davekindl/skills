# davekindl / skills

**A public library of 30 AI skills — free to take, use, and adapt.**

Reusable, self-contained operational skills for AI coding agents. Grab any one,
run it, adapt it to your work. Built for **Claude Code**, usable by any capable
agent.

---

## What's a "skill"?

A skill is a reusable instruction set an AI assistant follows — a recipe for a
specific task, encoded as a `SKILL.md` (plus any scripts and references it needs).
The `SKILL.md` files are plain instructions any agent can load.

## Install

**Claude Code** — copy a skill folder into your skills directory:

```bash
# global (all projects)
cp -r skills/<name> ~/.claude/skills/<name>
# or project-scoped
cp -r skills/<name> <your-project>/.claude/skills/<name>
```

It's live next session. **Any other agent** — load `skills/<name>/SKILL.md` as
instructions when the task comes up.

**Want your AI to do the whole setup for you?** Point it at this repo and say
*"read AI-START-HERE.md and integrate these."* It will install them, tell you
which ones need customizing, and interview you to configure them. See
[`AI-START-HERE.md`](AI-START-HERE.md).

## The skills (30)

Grouped by what they do. Each is self-contained.

### Web & design
- `animated-website` — turn a video into a scroll-driven cinematic website (2 modes)

### Content & writing
- `content-atomizer` — one long piece → ten platform-native derivatives
- `course-creator` — turn expertise into a structured, assessment-backed course
- `seo-content-engine` — search-first content with schema/SEO built in
- `lyric-forge` — songwriting / lyric structuring

### Media production
- `gpt-image-2-techniques` — 117-technique catalog for branded image generation
- `video-prompt-builder` — cinematic AI-video prompts (Seedance & co.)
- `line-tapper` — precise lyric/subtitle timing
- `lyric-video-forge` — automated lyric videos (auto-timed)
- `lyric-video-studio` — manual-precision lyric videos (real footage)
- `audio-master` — reference-based audio mastering
- `style-genome-analyzer` — reverse-engineer any track's style DNA
- `pod-shirt-designer` — print-on-demand shirt design pipeline

### Business & consulting
- `business-mvp` — idea → validated concept + landing page + business plan
- `business-evolution-audit` — crawl + benchmark + gap-analysis audit *(needs setup)*
- `grand-slam-offer` — offer construction (value-stacking methodology)
- `marketing-plan` — structured marketing plan generation
- `legal-toolkit` — GDPR/EU-AI-Act checklists + contract clause templates
- `metapromptify` — turn a tool/methodology into a portable meta-prompt
- `niche-skill-forge` — research-to-production skill generator

### Code & quality
- `the-inspector` — product-readiness auditor (security → functionality → polish)
- `deep-interrogation` — 20-question idea/product pre-build validation
- `polish-orchestrator` — parallel multi-mode quality gate (wave DAG) *(needs setup)*
- `polish-worker` — the 15 audit-mode methodologies the orchestrator runs
- `close` — end-of-session ritual (durable state + checkpoint commit)
- `open` — start-of-session ritual (resume from durable state)

### Automation & planning
- `product-evolver` — 4-lens autonomous product improvement loop *(needs setup)*
- `octopus` — nightly multi-arm autonomous operations *(needs setup)*
- `megaplan` — deep architectural planning (alternatives + decision docs)
- `firecrawl` — web scraping/crawling toolkit *(needs API key)*

*"Needs setup"* skills interview you (or scan your repos) before first use —
`AI-START-HERE.md` walks your agent through it. Skills that call paid APIs read
keys from **your** environment — never hardcode or commit them.

## Using these

Take them, run them, adapt them to your work. If you build something good on top
of them, that's the point. Attribution appreciated, not required.

— davekindl · NOTREPLACED
