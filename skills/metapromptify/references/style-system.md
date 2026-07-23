# Metapromptify Style System — 5 Premium Design Templates

These are the exact style descriptors to embed in every generated meta-prompt. Do NOT shorten, summarize, or rephrase them — copy them as-is into the Style System section of the meta-prompt. The vibe words ("beautiful", "stunning", "polished") are intentional prompt engineering that nudges the target LLM toward higher visual quality.

Each descriptor is ~150 tokens. Total style system cost: ~750 tokens + selection UI ~100 tokens = ~850 tokens.

---

## Template Selection UI

Include this in the Discovery Phase of every meta-prompt:

```
Choose your preferred design template and mode:

1. **Notion Native** — Beautiful clean workspace aesthetic with jewel-toned callout boxes and emoji section markers
2. **Linear** — Stunning developer-tool precision with violet accents and gradient progress gauges
3. **PostHog Analytics** — Gorgeous bold data visualization with thick-bordered cards and multi-color ring gauge
4. **Swiss Modernist** — Architecturally beautiful red-and-black grid with massive typographic score numbers
5. **Glassmorphism** — Breathtaking frosted glass panels on soft gradient mesh backgrounds

Mode: **Light** or **Dark**?
```

---

## Style Descriptor 1: Notion Native

```
STYLE: Notion Native
AESTHETIC: Beautiful, polished workspace. Every element should feel like it belongs in a meticulously designed Notion page crafted by someone with exquisite taste.
LIGHT MODE: White (#ffffff) background. Jewel-toned left-border callout boxes: emerald (#10b981) for positive findings, sapphire (#3b82f6) for informational, amber (#f59e0b) for warnings, ruby (#ef4444) for critical. Property grids with alternating row tints on light gray (#f9fafb). Beautiful gradient rainbow accent bar at top (emerald → sapphire → violet → pink). Tag pills with gorgeous pastel backgrounds. Score as elegant horizontal progress bar with gradient fill. Section headers with emoji markers and subtle underlines. Nested cards with delicate shadows. Pull-quote blocks with purple left border on soft lavender background. Avatar circles with gradient fills. Dividers that fade at edges. Text: primary #1a1a1a, secondary #6b7280.
DARK MODE: Rich dark (#1a1a1f) background, card surfaces (#252528). Same jewel-toned borders glowing subtly against dark. Text in warm off-white (#e0ddd8). Tags with translucent gem-tone backgrounds. Every element maintains its beauty in the darker palette.
TYPOGRAPHY: System sans-serif stack. Headers 700 weight, body 400, labels 600 uppercase with 0.5px letter-spacing. Rounded corners (10px cards, 20px pills, 8px callouts).
```

## Style Descriptor 2: Linear

```
STYLE: Linear
AESTHETIC: Stunning developer-tool precision. Every pixel feels intentional, meticulous, and polished. The kind of interface that makes engineers say "this is beautiful."
DARK MODE (native): Deep charcoal (#111117) background. Violet/purple (#7c3aed, #8b5cf6) as the gorgeous primary accent. Beautiful gradient progress bars (violet → indigo → blue). Polished pill tags with subtle inner glow borders. Cards with elegant thin borders and micro-shadows on rgba(255,255,255,0.02) backgrounds. Section headers with thin violet accent line beneath via ::after pseudo-element. Three-column metric cards with large 800-weight numbers. Status dots with colored box-shadows creating a soft glow. Subtle 1px violet gradient line at top of card. Text: primary #f0eeea, secondary #6b6965.
LIGHT MODE: Crisp white (#ffffff) background. Same violet accent deepened. Cards with beautiful multi-layer shadows (subtle outer + soft spread). Purple-tinted info backgrounds (#f5f3ff). Clean and precise, unmistakably premium.
TYPOGRAPHY: System sans-serif. Titles 700 weight -0.5px tracking. Labels 11px 600 weight uppercase 1px letter-spacing. Tight spacing, no wasted whitespace. Border-radius: 10px cards, 6px tags.
```

## Style Descriptor 3: PostHog Analytics

```
STYLE: PostHog Analytics
AESTHETIC: Gorgeous bold data visualization that commands attention. Every metric should feel important. Confident, playful, and information-rich — beautiful density without clutter.
LIGHT MODE (native): White (#ffffff) background. Stunning thick-bordered cards (2.5px solid #1d1f27). Multi-color conic-gradient ring gauge for scores (green #10b981 → amber #f59e0b → red #ef4444 zones). Horizontal bar charts with beautiful gradient fills per dimension. Numbered finding cards with severity badges (CRITICAL in red, WARNING in amber, OK in green — each with colored backgrounds and borders). Multi-color rainbow accent bar at top. Heavy confident typography (800 weight headers). Info grid with 2-column layout. Strategy cards with green accent borders. Person panels with gradient avatar circles. Text: primary #1d1f27, secondary #6b7280.
DARK MODE: Rich dark (#1d1f27) background. Borders become bright against dark (#3a3d48). Ring gauge and bar charts glow with vivid color. Finding numbers switch to orange (#f97316) on dark. Severity badges with translucent colored backgrounds. Same bold beautiful energy, stunning in dark.
TYPOGRAPHY: System sans-serif. Headers 800 weight. Section titles 16px 800. Labels 10px 700 uppercase 0.8px tracking. Bold everywhere — this template is not shy.
```

## Style Descriptor 4: Swiss Modernist

```
STYLE: Swiss Modernist
AESTHETIC: Architecturally beautiful. Every element placed with the precision of a Swiss watchmaker. Red and black — nothing else needed. Structure IS the decoration. Feels like Josef Müller-Brockmann designed your data.
LIGHT MODE (native): Pristine white (#ffffff) background. Red (#dc2626) and black (#0a0a0a) only — no other colors except traffic-light status dots. Massive ghosted section numbers (56-72px, 0.3-0.45 opacity) positioned behind content as architectural landmarks. Score displayed as devastating 120px 900-weight red numeral. Gorgeous gradient rule lines (black → red 15% → black). Diamond (◆) markers centered on thin dividers. Oversized red quotation marks on pull-quotes. Three-column key-value grids with 10px uppercase labels. Red numbered item markers (20px 900 weight). Red circle avatar with white initials. Text: primary #0a0a0a, secondary #555, labels #999.
DARK MODE: Near-black (#0a0a0a) background. Red stays vivid (#ef4444). White text, rules in subtle gray (#222). Ghost section numbers in dark gray (#1a1a1a). Same grid discipline — Swiss design transcends color mode.
TYPOGRAPHY: Segoe UI/Helvetica/Arial stack. Section titles 14px 700 uppercase 1.5px letter-spacing. Body 13px. Extreme alignment discipline. Border-radius: 4px only (sharp, architectural). Padding: generous (48-52px).
```

## Style Descriptor 5: Glassmorphism

```
STYLE: Glassmorphism
AESTHETIC: Breathtakingly beautiful. Dreamy, luminous, modern. Every panel floats on a soft gradient like frosted glass in a premium SaaS app's most polished dashboard. The kind of design that makes people pause and stare.
LIGHT MODE (native): Soft mesh gradient background (lavender #e8d5f5 → blue #c7d9f7 → pink #f5d5e0 → mint #d4f0e4 → purple #e0d7f7 at 135deg). Frosted glass panels: rgba(255,255,255,0.7) background, backdrop-filter blur(20px), 1px rgba(255,255,255,0.6) border, delicate multi-layer shadows. Nested glass-inner cards at rgba(255,255,255,0.5). Beautiful conic-gradient score ring with gradient stroke. Glowing status dots with colored box-shadows. Rounded tag pills with translucent gem-tone backgrounds. Subtle SVG noise texture overlay at 0.03 opacity. Insight boxes with purple-tinted glass. Text: primary #2d2b3d, secondary #7c7a8e.
DARK MODE: Deep stunning gradient (indigo #1a1040 → navy #0d1a3a → plum #2a0a2e → dark teal #0a1a2a → deep violet #1a0d30). Frosted panels at rgba(255,255,255,0.06) with rgba(255,255,255,0.1) borders. Score ring glows brighter. Toggle knob in luminous purple (#a78bfa) with glow shadow. Same dreamy glass aesthetic, night mode. Absolutely gorgeous.
TYPOGRAPHY: System sans-serif. Headers 700 weight. Labels 10px 700 uppercase. Border-radius: 16px glass panels, 12px inner cards, 20px pills. Everything rounded, nothing sharp.
```

---

## Usage Notes

- These descriptors go into the meta-prompt's STYLE SYSTEM section verbatim
- The target LLM reads these and applies them when generating HTML output
- The vibe words are load-bearing — they measurably improve output quality across all major LLMs
- For Markdown output, the style system is not needed (skip it in the render instructions)
- The dark/light toggle is a small JS snippet (~15 lines) that swaps a CSS class on the output container
