---
name: metapromptify
description: Convert any built tool, product, or consulting methodology into a portable meta-prompt anyone can paste into any LLM to get a fully customized, premium-looking output. Produces self-contained meta-prompts with discovery phases, tool-specific analysis, and 5 beautiful design templates (dark/light). Trigger on "metapromptify this", "turn this into a prompt", "make this portable", "package this as a meta-prompt", "prompt-ify", "extract this as a shareable prompt", "book-ready prompt", or wanting to convert any existing tool into a standalone prompt product. Also trigger when a build pipeline needs a distributable prompt version of a built product, or when packaging tools for books/courses.
allowed-tools: Read, Write, Glob, Grep
---

# Metapromptify — Tool-to-Meta-Prompt Converter

> A meta-prompt is a transferable instance of your tool. The user pastes it into any LLM, runs it on their context, and gets customized output that looks like a premium product — not AI slop.

## What This Skill Does

Takes a tool (via spec card or repo scan) and produces a complete, self-contained meta-prompt document. When a user pastes that document into ChatGPT, Claude, Gemini, or any capable LLM, it runs:

1. **Discovery** — Tool-specific questions tailored to the user's situation + design preference selection
2. **Analysis** — Processes answers through the tool's methodology (scoring, frameworks, research logic)
3. **Generation** — Builds the output artifact using the chosen design template
4. **Render** — Outputs as a beautiful self-contained HTML page or structured Markdown

## Two Input Modes

### Mode A: Tool Spec Card (Primary)

The user writes a structured spec card describing the tool. Read the template at `references/spec-card-template.md`.

**Workflow:**
1. The user provides the spec card (or you help them draft it)
2. Read the spec card
3. Read `references/style-system.md` for the 5 template descriptors
4. Read `references/meta-prompt-skeleton.md` for the output structure
5. Generate the meta-prompt by filling the skeleton with tool-specific logic

### Mode B: Repo Research (Secondary) — run as a context:fork

The user points at an existing tool's codebase. You research it autonomously, then build the meta-prompt.

**Run the repo scan in a forked/isolated context** (`context:fork`): dispatch the codebase research into a sub-context so the raw source files, CLAUDE.md, and progress docs never pollute the main session. The fork returns ONLY the auto-generated spec card; the main context proceeds from that card alone. If a context-fork mechanism is unavailable in the current harness, scan inline but discard the raw file contents from working memory once the spec card is drafted.

**Workflow:**
1. The user specifies the tool directory or repo
2. In the fork — Read: CLAUDE.md, README.md, package.json, key source files, any status/progress docs
3. In the fork — Extract: purpose, inputs, outputs, scoring/analysis logic, edge cases, architecture
4. The fork returns an auto-generated spec card from findings — present to the user for review
5. Once approved, proceed as Mode A

The research goal is to understand what the tool does well enough to build a simplified prompt-only version that captures its core methodology. You're not cloning the codebase — you're extracting the thinking framework.

## Meta-Prompt Architecture

Every generated meta-prompt follows this structure. Read `references/meta-prompt-skeleton.md` for the full template.

```
┌─────────────────────────────────────┐
│ IDENTITY & ROLE                     │  Who the LLM becomes
├─────────────────────────────────────┤
│ METHODOLOGY                         │  The tool's analysis framework, simplified
│  └─ scoring, steps, decision logic  │  for prompt-only execution
├─────────────────────────────────────┤
│ DISCOVERY PHASE                     │  8-15 questions, tool-specific
│  ├─ Business/context questions      │  Generated from spec card capabilities
│  ├─ Scope/depth preferences         │
│  └─ Design template + mode choice   │  5 templates × dark/light
├─────────────────────────────────────┤
│ ANALYSIS PHASE                      │  How to process discovery answers
│  └─ scoring rubrics, frameworks     │  into structured findings
├─────────────────────────────────────┤
│ GENERATION PHASE                    │  Section-by-section output spec
│  └─ what each section contains      │  Mirrors source tool's architecture
├─────────────────────────────────────┤
│ STYLE SYSTEM                        │  5 template descriptors (~150 tokens each)
│  └─ design tokens per template      │  with "beautiful", "polished" vibe words
├─────────────────────────────────────┤
│ RENDER INSTRUCTIONS                 │  How to output HTML or Markdown
│  └─ self-contained, no deps         │  using chosen template + mode
└─────────────────────────────────────┘
```

## Discovery Questions — The Key Differentiator

Generic meta-prompts ask generic questions. Metapromptify generates discovery questions **from the source tool's capabilities.** 

If the tool scores companies on 5 dimensions, the discovery asks about those dimensions. If the tool finds pain points, the discovery asks about the target's industry, competitors, and known frustrations. If the tool generates outreach, the discovery asks about tone, relationship status, and prior interactions.

**How to generate discovery questions:**
1. Read the spec card's "Processing Logic" and "Output Sections"
2. For each output section, ask: "what input does the LLM need to generate this well?"
3. Write 1-2 discovery questions per output section
4. Add 2-3 universal questions: depth preference, industry context, output format
5. Always end with the design template selection (show all 5 with 1-line descriptions + dark/light toggle)

## The 5 Design Templates

Read `references/style-system.md` for complete descriptors with design tokens and vibe words. Summary:

| # | Template | Character |
|---|----------|-----------|
| 1 | Notion Native | Beautiful workspace aesthetic, jewel-toned callouts, emoji markers, polished property grids |
| 2 | Linear | Stunning developer-tool precision, violet accents, gradient gauges, meticulous pill tags |
| 3 | PostHog Analytics | Gorgeous bold data visualization, thick-bordered cards, multi-color ring gauge, confident typography |
| 4 | Swiss Modernist | Architecturally beautiful, red+black, massive typographic scores, oversized ghost section numbers |
| 5 | Glassmorphism | Breathtaking frosted glass panels, soft gradient mesh backgrounds, luminous score rings |

Each template has both light and dark mode. The style descriptors include words like "beautiful", "stunning", "polished", "gorgeous", "meticulous" — these nudge any LLM to produce higher-quality visual output at near-zero token cost.

## Output Quality Rules

The meta-prompt must instruct the target LLM to:

1. **Generate self-contained HTML** — all CSS inline, no external dependencies, opens in any browser
2. **Include the dark/light toggle** as a small JS-powered button
3. **Use CSS transitions** (0.5s) on all color properties for smooth mode switching
4. **Apply the full design system** — not just colors, but shadows, borders, gradients, typography hierarchy, score visualizations, card depth, decorative dividers, avatar circles, status indicators
5. **Make every element beautiful** — the meta-prompt should explicitly tell the LLM that visual quality matters and every shadow, gradient, and border radius should feel considered and polished
6. **INTERACTIVE, NOT STATIC** — this is a general rule for ALL metapromptified outputs. HTML must include vanilla JS interactivity. Never output a flat scroll of content. Minimum interactive elements:
   - **Collapsible/expandable cards** — show summary by default, click to expand full detail
   - **Filter controls** — pill buttons or dropdowns to filter by key dimensions (tier, classification, score range, etc.)
   - **Sort controls** — clickable column headers or buttons to re-sort the data
   - **Sticky navigation** — summary bar or tab nav that stays visible while scrolling
   - **Search/filter input** — for outputs with many items, a text filter
   - All interactive JS must be vanilla (no frameworks), inline in the HTML, and compact
7. **Markdown fallback** — if the user chose Markdown, produce structured output with clear headers, bullet formatting, bold key metrics, and blockquote callouts. Still looks premium, just in text.

## Evolution & Next Steps Section (MANDATORY)

Every metapromptified output — HTML or Markdown — must end with a "What's Next" section. This is NOT optional. It transforms a one-shot output into a growth path. Include:

1. **Iterate** — "To add more [items/prospects/data], paste this prompt again with updated answers. Your previous output serves as context."
2. **Deepen** — Tool-specific advice on how to populate the research further (e.g., "Validate these pain signals with LinkedIn research", "Cross-check scores against real financials")
3. **Upgrade to terminal** — "For real-time web research, API access, and file I/O: run this prompt in Claude Code (terminal) or Claude Desktop. This unlocks live data that chat-only mode can't access."
4. **Build the real thing** — "Want a full interactive app with a database, API, and real frontend? Use this Markdown output as a build brief — it already contains your requirements, scoring logic, and architecture. Paste it into a new session with: 'Build this as a production app.'"
5. **Export as a build brief** — The Markdown output from discovery answers + the prompt's methodology section = a ready-made project specification. The meta-prompt should explicitly tell the user this.

The tone should be helpful and exciting, not salesy. The user just got a powerful free tool — now show them the ladder.

## Generating the Meta-Prompt

When you have the spec card and understand the tool:

1. Read `references/meta-prompt-skeleton.md` — this is your template
2. Fill in each section:
   - **Identity**: derived from the tool's purpose
   - **Methodology**: simplified version of the tool's processing logic
   - **Discovery questions**: generated from the tool's capabilities (see algorithm above)
   - **Analysis phase**: how to score/evaluate based on the tool's rubrics
   - **Generation phase**: section specs matching the tool's output structure
   - **Style system**: copy the 5 descriptors from `references/style-system.md` (do NOT shorten them)
   - **Render instructions**: standard HTML/Markdown rendering rules
3. Output the complete meta-prompt as a single Markdown file in the output folder: `<output-dir>/{tool-name}-meta-prompt.md`
4. Also output just the raw prompt text (no wrapping, ready to paste) at: `<output-dir>/{tool-name}-paste-ready.txt`

   `<output-dir>` resolution order: (a) a path the user/caller passes in, else (b) a `./prompts/` folder relative to the current working directory. If `./prompts/` does not exist, create it. Never hardcode an absolute or machine-specific path.

## Quality Checklist

Before delivering, verify:
- [ ] Discovery questions are tool-specific, not generic
- [ ] Methodology section captures the tool's real analysis logic
- [ ] All 5 templates are included with full descriptors (not shortened)
- [ ] Both HTML and Markdown output paths are specified
- [ ] The meta-prompt works when pasted raw into any LLM (no Claude-specific syntax)
- [ ] Dark/light toggle instructions are included
- [ ] **HTML is interactive** — collapsible cards, filters, sort, sticky nav (NOT a flat scroll)
- [ ] **"What's Next" section** is present with iterate/deepen/terminal/build-brief bridge
- [ ] Output sections match the source tool's architecture
- [ ] Vibe words ("beautiful", "polished", "stunning") are present in style instructions
- [ ] The prompt is self-contained (no references to external files or APIs)
- [ ] Total prompt length is reasonable (target 3500-6500 tokens — interactivity adds ~500 tokens)

## Build-Pipeline Integration

When invoked as a phase of a larger build pipeline, this skill runs after the product is built. The pipeline should provide the tool's directory path. Use Mode B (repo research) to auto-generate the spec card, then proceed to meta-prompt generation.

Deliver the meta-prompt alongside the built product as a distributable artifact.
