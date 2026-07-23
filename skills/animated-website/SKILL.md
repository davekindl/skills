---
name: animated-website
description: "Convert video files (or generate them via Seedance 2.0) into scroll-animated cinematic websites. Two modes: PREMIUM (frame extraction + canvas scroll dwell engine) or RAPID (video background + GSAP ScrollTrigger). Luxury-grade design with ambient particles, film grain, glass morphism, letter-split animations, and parallax galleries. Use when the user says 'animated website', 'scroll animation', 'video to website', 'Apple-style page', 'scroll-driven site', 'frame animation', 'cinematic website', '$10k website', 'Seedance website', 'convert this video to a website', 'make a scroll site from this video', 'luxury website from video', or wants to turn a video clip into an interactive scroll experience."
---

# Animated Website Generator

Convert video files into scroll-animated websites with a luxury, cinematic aesthetic. Two build modes:

- **PREMIUM mode** (default): Extract frames from MP4, optimize to WebP, build a scroll-driven canvas animation with the custom dwell engine. Maximum cinematic control. Best for portfolio showcases, Apple-style product pages, luxury real estate.
- **RAPID mode** (~15 minutes): Use `<video>` as a looping background + GSAP ScrollTrigger for text animations. Faster, simpler, still premium-looking. Best for landing pages, brand sites, quick client deliverables. Inspired by the Jack Roberts "$10k website" workflow.

The design language draws from high-end real estate, product launches, and editorial showcases: warm dark palettes, serif/sans-serif type pairing, ambient particles, film grain texture, glass morphism cards, and scroll pacing that creates natural rhythm through content sections.

---

## Mode Selection

Ask the user which mode they want, or auto-select based on context:

| Signal | Mode |
|--------|------|
| "quick", "fast", "15 minutes", "simple", "$10k website", "GSAP" | RAPID |
| "Apple-style", "frame-by-frame", "dwell", "premium", "canvas" | PREMIUM |
| Short video (<10s), landing page, brand site | RAPID recommended |
| Long video (>10s), portfolio, product showcase, real estate | PREMIUM recommended |
| User has no video yet | Start with Step 0 (video generation), then either mode |

If unclear, default to **RAPID** — it ships faster and can always be upgraded to PREMIUM later.

---

## Step 0: Video Generation (Optional — when user has no MP4)

If the user doesn't have a video yet, generate one using AI video tools. Connect to the `video-prompt-builder` skill for Seedance 2.0 prompts.

### Quick Seedance Prompt Templates

**Abstract/Tech:**
> Close up of an abstract 3D form, made of black iridescent fabric, undulating slowly in a dark, atmospheric environment. Cinematic lighting, dramatic shadows, 4K, photorealistic.

**Nature/Organic:**
> Aerial drone shot of ocean waves crashing against dark volcanic rocks, golden hour light, mist rising, slow motion, cinematic color grade, 4K.

**Product/Luxury:**
> Slow orbit around a matte black luxury watch on a reflective obsidian surface, volumetric light rays, atmospheric haze, extreme close-up, photorealistic, 4K.

**Architecture/Real Estate:**
> Smooth tracking shot through a modern minimalist interior, floor-to-ceiling windows, golden hour sunlight casting long shadows, cinematic depth of field, 4K.

**Data/Digital:**
> Close up of glowing neural network connections forming and dissolving in dark space, electric blue and amber particles, slow motion, cinematic, 4K.

### Process:
1. Match user's concept to a prompt template (or invoke `video-prompt-builder` for custom Seedance prompts)
2. User generates the video in Seedance 2.0 (or Kling, RunwayML, Pika — any AI video tool works)
3. Download the MP4 and proceed to Step 1 (PREMIUM) or Rapid Build

---

## When This Skill Applies

**This skill IS for:**
- Converting an MP4 video into a scroll-driven animated website (PREMIUM or RAPID)
- Luxury showcase pages (real estate, architecture, product, portfolio)
- Apple product page-style frame sequences (scroll to play)
- Quick cinematic landing pages with video backgrounds + GSAP animations
- Any "video → interactive scroll experience" request
- "$10k website" requests (RAPID mode)

**This skill is NOT for:**
- Embedding a video player on a page (just use `<video>`)
- Converting video to GIF or animated WebP
- Building a regular website without video-based scroll animation
- CSS-only scroll animations (use the `frontend-design` skill instead)

**Redirect:** If the user wants a regular animated website WITHOUT a video source, use the `frontend-design` skill.

---

## Input: What You Need From the User

**Required:**
1. **An MP4 video file** — absolute path to the source video
2. **Website concept** — what the site is about (product, brand, property, portfolio, etc.)

**Optional (skill handles defaults if not provided):**
- Target frame count (default: auto-calculated from video duration)
- Brand colors (default: warm-dark luxury palette)
- Section copy (headlines, body text, CTAs)
- Brand name and tagline

If the user gives just a video path and a vague concept, ask ONE clarifying question about the content direction, then proceed.

---

## Process

### Step 1: Analyze the Video

Probe the video to understand what you're working with:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams "/path/to/video.mp4"
```

Parse and present:

```
VIDEO ANALYSIS:
Duration:    12.4s
Resolution:  3840x2160 (4K)
Frame Rate:  30fps
Total Frames: 372
Codec:       H.264
```

Then recommend frame count:

| Video Duration | Recommended Frames | Scroll Height |
|---------------|-------------------|---------------|
| 0-5s          | 60-90             | 400vh         |
| 5-15s         | 100-150           | 650vh         |
| 15-30s        | 150-200           | 800vh         |
| 30s+          | Cap at 200        | 900vh         |

**Get user confirmation before extracting.** Say: "I recommend extracting {N} frames. Sound good, or want to adjust?"

### Step 2: Extract and Optimize Frames

Run the extraction script. Invoke it from the skill directory using `${CLAUDE_SKILL_DIR}` (the env var Claude Code sets to this skill's path) so it works regardless of where the repo lives:

```bash
# macOS / Linux (python3); Windows: use `python` and `^` line continuations or a single line
python3 "${CLAUDE_SKILL_DIR}/scripts/extract_frames.py" \
  --input "/path/to/video.mp4" \
  --output "workspace/{today}/animated-sites/{slug}/frames" \
  --frames {N} \
  --quality 80
```

```powershell
# Windows (PowerShell) — python (not python3), backtick line continuation
python "$env:CLAUDE_SKILL_DIR/scripts/extract_frames.py" `
  --input "C:/path/to/video.mp4" `
  --output "workspace/{today}/animated-sites/{slug}/frames" `
  --frames {N} `
  --quality 80
```

> Requires `ffmpeg`/`ffprobe` and Pillow on PATH. Install ffmpeg with `choco install ffmpeg` (Windows), `brew install ffmpeg` (macOS), or `apt install ffmpeg` (Linux); install Pillow with `python -m pip install Pillow`.

The script produces:
- `frames/desktop/` — 1920x1080 WebP frames
- `frames/mobile/` — 960x540 WebP frames
- `frames/manifest.json` — metadata (counts, sizes, scroll height)

Show the manifest summary to the user. If payload exceeds budget (>10MB desktop, >5MB mobile), recommend `--quality 60` or fewer frames.

### Step 3: Gather Content

Based on the user's concept, prepare content for 6 scroll-text sections. These overlay the video at different scroll positions, creating a narrative experience. The sections are:

1. **Hero** — Property/product name, tagline, key stats
2. **Vision** — A quote or aspirational statement about the subject
3. **Details** — Key specifications or features (with icon list)
4. **Grid** — 4-6 amenities/features in a glass grid layout
5. **Context** — Location, availability, or background info
6. **CTA** — Call to action with buttons and contact info

If the user provides copy, use it. If not, generate content that fits the concept. The content should feel editorial and refined — short sentences, evocative language.

### Step 4: Build the Website

Generate a complete single-file HTML page using the design system below. Save to: `workspace/{today}/animated-sites/{slug}/index.html`

**Adapt the content and branding to the concept** — the design patterns stay consistent but the palette, copy, and section content should fit the subject matter. A tech product might use cooler blues, a restaurant warmer golds, a real estate listing the warm-neutral default.

### Step 5: Serve and Preview

The site must be served over HTTP (frame loading + `createImageBitmap` fail on `file://` due to CORS). Start a static server from the output directory in the background:

```bash
# macOS / Linux
python3 -m http.server 8080 --directory "workspace/{today}/animated-sites/{slug}"
```
```powershell
# Windows (PowerShell) — use `python`, run in the output dir
python -m http.server 8080 --directory "workspace/{today}/animated-sites/{slug}"
```

Then verify with the **Playwright MCP** tools (do NOT write Bash screenshot scripts or hand-paste JS into a DevTools console):

1. `browser_navigate` → `http://localhost:8080/index.html`
2. `browser_console_messages` → check for 404s (wrong frame paths), CORS errors, or JS errors
3. `browser_snapshot` → confirm structure (canvas, 6 scroll-text sections, gallery) without spending tokens on pixels
4. `browser_evaluate` → run the structural audit from `references/quality-checklist.md` (returns a PASS/FAIL array in the transcript)
5. `browser_take_screenshot` only when visual appearance matters — scroll first with `browser_evaluate` (`() => window.scrollTo(0, document.body.scrollHeight * 0.3)`) to capture different scroll positions

Common iteration requests:
- "Slower scroll" → increase animation-section height (650vh → 900vh)
- "Faster scroll" → decrease height (650vh → 400vh)
- "Smoother animation" → decrease LERP_FACTOR (0.09 → 0.05)
- "More responsive" → increase LERP_FACTOR (0.09 → 0.15)
- "Change text" → edit the scroll-text overlay content
- "Different colors" → update CSS custom properties in `:root`

---

## RAPID Mode — Video Background + GSAP (~15 minutes)

Use this mode when speed matters more than frame-level control. Instead of extracting frames, the video plays as a looping `<video>` background while GSAP ScrollTrigger handles text animations.

### When to Use RAPID Instead of PREMIUM

- Client needs it fast ("can you have something by tomorrow?")
- Short videos (<10s) where frame-by-frame adds no value over a loop
- Landing pages and brand sites (not portfolios or product showcases)
- Quick prototypes to validate a concept before investing in PREMIUM

### Rapid Build Process

**Step R1: Video Prep**
Place the MP4 in the project folder. If the user doesn't have a video, use Step 0 (Seedance prompt templates) to generate one.

**Step R2: Scaffold with a Single Prompt**
Generate the entire site structure from one high-level prompt. The prompt should describe:
- Brand name and tagline
- Desired aesthetic (dark, cinematic, premium)
- Font choice (default: Inter from Google Fonts)
- Number of content sections (3-6)
- Color accent

Example founding prompt:
> "Build a cinematic landing page for '{Brand}'. Dark theme, Inter font, centered hero heading + subheading. Clean, modern, high-end. Single index.html + style.css."

**Step R3: Integrate Video Background**
Add the video as a fixed, full-viewport background:

```html
<div class="video-background">
  <video autoplay muted loop playsinline>
    <source src="background.mp4" type="video/mp4">
  </video>
</div>
```

```css
.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.video-background video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Dark overlay for text readability */
.video-background::after {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.5);
}
```

**Step R4: Add GSAP ScrollTrigger Animations**
Load GSAP from CDN and create scroll-driven animations:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
```

```javascript
gsap.registerPlugin(ScrollTrigger);

// Hero text fades out on scroll
let tl = gsap.timeline({
  scrollTrigger: {
    trigger: "main",
    start: "top top",
    end: "bottom top",
    scrub: true
  }
});

tl.to("h1", { y: -50, opacity: 0 });
tl.to("p", { y: -30, opacity: 0 }, "<");

// Content sections fade in as they enter viewport
gsap.utils.toArray('.content-section').forEach(section => {
  gsap.from(section, {
    scrollTrigger: {
      trigger: section,
      start: "top 80%",
      end: "top 30%",
      scrub: true
    },
    y: 60,
    opacity: 0,
    filter: "blur(4px)"
  });
});
```

**Step R5: Add Ambient Effects (Optional)**
For premium feel even in RAPID mode, add from the PREMIUM design system:
- Film grain overlay (SVG feTurbulence, 3.5% opacity)
- Vignette (radial gradient)
- Custom cursor (desktop only, mix-blend-mode: difference)

These are lightweight and dramatically increase perceived quality.

**Step R6: Serve and Verify**
Serve over HTTP, then verify with the Playwright MCP tools (see Step 5 above — `browser_navigate` → `browser_console_messages` → `browser_snapshot`):
```bash
# macOS / Linux
python3 -m http.server 8080
```
```powershell
# Windows (PowerShell)
python -m http.server 8080
```

### RAPID Mode File Structure
```
project/
├── index.html      (structure + inline CSS + inline JS)
├── style.css       (optional, can be inline)
├── background.mp4  (the video)
└── app.js          (optional, can be inline)
```

### RAPID vs PREMIUM Comparison

| Dimension | RAPID | PREMIUM |
|-----------|-------|---------|
| Build time | ~15 minutes | 1-2 hours |
| Video handling | `<video>` loop | Frame extraction → canvas |
| Scroll animation | GSAP ScrollTrigger | Custom dwell engine |
| File size | Small (video + HTML) | Large (100+ WebP frames) |
| Frame control | None (video plays independently) | Exact (scroll position = frame) |
| Ambient effects | Optional subset | Full (grain, particles, vignette, tint, cursor) |
| Gallery section | Not included | Parallax masonry grid |
| Mobile payload | Small | Can be large (mobile frames) |
| Best for | Landing pages, quick client work | Portfolios, Apple-style showcases |
| Perceived value | $5K-$10K | $10K-$25K |

### Upgrading RAPID to PREMIUM
If the client loves the RAPID prototype and wants the full treatment:
1. Extract frames from the same video (Step 1-2 of PREMIUM)
2. Replace `<video>` with canvas animation
3. Add scroll dwell engine
4. Add full ambient effects + gallery
5. Replace GSAP with custom scroll-text overlays

---

## Design System (Both Modes)

The visual language is warm, dark, and cinematic. Every element serves the animation — surrounding effects (grain, particles, vignette) add depth without competing with the video frames. RAPID mode uses a subset; PREMIUM uses everything.

**DESIGN.md References:** Before building, check the `frontend-design-references` skill's `design-systems/` directory for matching design systems. For cinematic websites: `spacex-DESIGN.md` (dark cinematic), `tesla-DESIGN.md` (minimal premium), `ferrari-DESIGN.md` (luxury). Adapt accent colors from the matching reference.

**Full spec → [`references/design-system.md`](references/design-system.md).** It contains the complete:
- Color palette (CSS custom properties), spacing scale, border radii, typography table, glass morphism values
- z-index layer stack and ambient effects (film grain, vignette, particles, dynamic tint, custom cursor)
- **Scroll Dwell Engine** — the math, the ASCII remap curve, tunable parameters, and the copy-pasteable `buildRemapLUT()` / `remapProgress()` implementation
- The six **Scroll Text Overlays** (Hero, Vision, Details, Grid, Context, CTA) with `data-show-at`/`data-hide-at` positions, content rules, and anti-patterns
- Glass cards, chapter markers, gallery section, branded loader, and footer

The core invariants: keep `--ink`, `--charcoal`, `--warm-white` constant across every brand (they make the frames pop); adapt the `--accent-blue` family per concept.

---

## Code Architecture

The entire site is a single HTML file. The complete annotated **HTML skeleton** (8 structural blocks + the 15-step JS execution order) and the four copy-pasteable **Key JavaScript Patterns** (frame loading with WebP→JPEG fallback + progressive batching, DPR-safe cover-fit canvas drawing, the dwell-remap scroll loop, and the IntersectionObserver stat counter) live in **[`references/code-architecture.md`](references/code-architecture.md)**. Use those implementations exactly — do not simplify or improvise.

---

## Adapting for Different Concepts

The warm-dark base (`--ink`, `--charcoal`, `--warm-white`) and all ambient effects stay the SAME for every domain — only the accent colors and content change, and the 6-section structure is universal. **[`references/concept-adaptations.md`](references/concept-adaptations.md)** has per-domain content tables and accent overrides for Real Estate (default), Tech Product, Portfolio/Creative, Restaurant/Hospitality, and Automotive, plus the universal adaptation rules and a fully worked tech-product example.

---

## Progressive Enhancement & Robustness

The generated site MUST degrade gracefully across real-world constraints. **[`references/progressive-enhancement.md`](references/progressive-enhancement.md)** specifies ALL required behaviors: reduced-motion handling, WebP→JPEG fallback, the iOS `100dvh` viewport fix, connection-aware loading, the desktop/mobile performance budget + responsive breakpoints, memory management, the `<noscript>` fallback, and the `@media print` stylesheet. Implement every item.

---

## Quality Checklist

Before showing the site to the user, verify ALL categories in **[`references/quality-checklist.md`](references/quality-checklist.md)** (Core Animation, Visual Effects, Content & Layout, Performance & Payload, Progressive Enhancement, Accessibility, SEO & Meta, Cross-Browser). Any unchecked item is a ship-blocker. That file also includes the structural audit to run via Playwright MCP `browser_evaluate` (returns a PASS/FAIL array in the transcript — no DevTools console paste).

---

## Output Format

```
workspace/{today}/animated-sites/{slug}/
├── frames/
│   ├── desktop/              # 1920x1080 WebP
│   │   ├── frame-0001.webp
│   │   └── ...
│   ├── mobile/               # 960x540 WebP
│   │   ├── frame-0001.webp
│   │   └── ...
│   └── manifest.json         # Frame metadata
└── index.html                # Complete luxury scroll site
```

To view: serve the output directory over HTTP (`python3 -m http.server 8080` on macOS/Linux, `python -m http.server 8080` on Windows), then verify with the Playwright MCP tools per Step 5.

---

## Troubleshooting

Full issue → cause → fix tables (Setup & Extraction, Animation & Rendering, Mobile & iOS, Visual Effects, Network & Loading, Accessibility) plus the step-by-step **Debugging Workflow** live in **[`references/troubleshooting.md`](references/troubleshooting.md)**. The debugging workflow drives the browser with the Playwright MCP tools (`browser_console_messages` for 404/CORS/JS errors, `browser_evaluate` for the frame-loading and scroll-progress audits) rather than hand-pasting into a DevTools console. The setup install commands cover Windows (`choco`/`python`), macOS (`brew`/`python3`), and Linux (`apt`).
