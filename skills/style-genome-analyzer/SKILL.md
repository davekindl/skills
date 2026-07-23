---
name: style-genome-analyzer
description: "Extracts the DNA of any track, crossbreeds styles, and discovers combos the user would never try. Three modes: Blueprint Extract (YouTube/MP3 → style genome), Crossbreeder (2-5 tracks → common DNA → genre mutations), Style Roulette (catalog audit → stretch proposals). Output: Suno-ready packages. Trigger when the user says 'analyze this track', 'blueprint this song', 'extract style', 'crossbreed these', 'style roulette', 'what genre should I try', 'analyze this YouTube', 'style DNA', 'genome', or provides a YouTube URL and wants to know how it's built."
---

# STYLE GENOME ANALYZER

> Extract the DNA of any track, crossbreed styles you love, discover combos you'd never try.
> Output: Suno-ready packages. Always.

## Shared Infrastructure
- **Creative discovery:** Read `D:\.claude\skills\shared\creative\discovery-creative.md` for common intake patterns
- **Sibling skills:** lyric-forge (song scripts), video-prompt-builder (Seedance prompts)

## Prerequisites

```bash
# Audio analysis
pip install librosa soundfile numpy --break-system-packages

# Better beat tracking (optional, graceful fallback)
pip install madmom --break-system-packages

# YouTube download
pip install yt-dlp --break-system-packages
```

**API Key:** `OPENROUTER_API_KEY` env var (for Gemini 2.5 Pro audio analysis, ~$0.05-0.15 per track)

> **Why Gemini, not Claude:** Claude has no audio input, so the subjective audio analysis is routed to Gemini 2.5 Pro (stable GA model `google/gemini-2.5-pro` via OpenRouter). Do not "consolidate to Claude" — the audio step requires a model that can actually hear the track.

## Three Modes

### Mode 1: Blueprint Extract

**Trigger:** User provides a YouTube URL or MP3 path and wants to understand it.

```bash
python3 scripts/extract.py --url "https://youtube.com/watch?v=VIDEO_ID"
python3 scripts/extract.py --file ./reference-track.mp3
python3 scripts/extract.py --url "URL" --intent "Hungarian gym anthem"
```

**What it does:**
1. Downloads audio (if YouTube URL)
2. Technical extraction: BPM, key, time signature, sections, beat grid, energy curve (librosa + madmom)
3. Subjective analysis: vocal DNA, rhythmic hooks, production fingerprint, energy arc, instrument roles, genre genome (Gemini 2.5 Pro)
4. Assembles blueprint with steal_list + avoid_list
5. Generates Suno-ready style field + tag skeleton + voice recommendations

**Output:** `blueprint.json` + `suno-package.md`

### Mode 2: Crossbreeder

**Trigger:** User has multiple tracks they love and wants to find the common thread + new combos.

```bash
python3 scripts/crossbreed.py --blueprints bp1.json bp2.json bp3.json
python3 scripts/crossbreed.py --urls "URL1" "URL2" "URL3"
```

**What it does:**
1. Compares all blueprints for shared DNA (tempo, vocal patterns, energy tricks, emotional core)
2. Identifies divergent surface elements
3. Generates 5 unexpected genre mutations that PRESERVE the shared DNA but sound completely different
4. Each mutation gets a Suno package + voice recommendations

**Output:** `crossbreed-report.md` + `crossbreed-{1-5}.md` + `common-dna.json`

### Mode 3: Style Roulette

**Trigger:** User wants to explore genres they haven't tried yet.

```bash
python3 scripts/roulette.py --bible ./suno-songwriting-bible.md
python3 scripts/roulette.py --bible ./suno-songwriting-bible.md --constraint "gym motivation"
```

**What it does:**
1. Parses your entire song catalog to build a "used" inventory
2. Identifies every genre, tempo, vocal mode, structure, language you've NEVER tried
3. Generates 5 stretch proposals at levels 1-5 (safe bet → unhinged experiment)
4. Each proposal gets 3 voice options + Suno package

**Output:** `roulette-report.md` + `roulette-{1-5}.md` + `catalog-audit.json`

## Voice Recommendation Engine

Every mode includes voice recommendations. The engine knows:
- An established house voice (deep raspy baritone, drill sergeant, whisper-to-scream range)
- 7 voice dimensions to explore (register, texture, delivery, processing, language, persona, choir)
- Genre-specific voice archetypes

## Integration Points

| Tool | How It Connects |
|------|----------------|
| Suno Songwriting Bible | Roulette mode reads it; all modes can extend it |
| lyric-forge skill | Blueprints feed the lyric generation pipeline |
| lyric-video-forge skill | Blueprint energy arcs map to keyframe tiers |
| hungarian-lyrics-masterguide.md | Referenced when any mode generates Hungarian output |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract.py` | Mode 1: Blueprint extraction (librosa + Gemini) |
| `scripts/analyze.py` | Gemini subjective analysis prompt + response parsing |
| `scripts/crossbreed.py` | Mode 2: Common DNA + mutations |
| `scripts/roulette.py` | Mode 3: Catalog audit + stretch proposals |
| `scripts/voice_engine.py` | Voice recommendation logic |
| `scripts/suno_packager.py` | Style field + tag skeleton assembly |
| `scripts/openrouter_client.py` | OpenRouter/Gemini API wrapper |

## Data

| Path | Purpose |
|------|---------|
| `data/blueprints/` | Saved blueprint.json files for crossbreeding |
| `data/crossbreeds/` | Saved crossbreed reports |
| `data/catalog_audit.json` | Latest roulette inventory |
