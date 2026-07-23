---
name: audio-master
description: "Master tracks to commercial loudness using reference-based mastering (Matchering) + LUFS verification (PyLoudnorm) + optional polish (Pedalboard). Replaces paid services like Mixea, LANDR, eMastered with a free local pipeline. Trigger when the user says 'master this track', 'mix and master', 'make it louder', 'prepare for distrokid', 'mastering', 'LUFS', 'make it radio ready', or provides a raw Suno output and wants the final mastered version."
allowed-tools: Bash, Read, Write, Edit, Glob
---

# AUDIO MASTER

> Suno WAV → Commercially mastered track. Reference-based. Free. Better than Mixea.

## What This Is

A local mastering pipeline that replaces $99/year services. Uses open source tools:

1. **Matchering 2.0** — matches RMS, frequency response, peak amplitude, stereo width to a reference track
2. **PyLoudnorm** — verifies LUFS target is hit (genre-specific)
3. **Pedalboard** (Spotify) — optional final polish (saturation, stereo tweaks)

**Why this beats Mixea:** Mixea has 12 fixed presets and no album consistency. Matchering lets you use ANY reference track and batch-process whole albums with identical treatment. In blind tests, Matchering ranks 3rd out of 12 — behind only 2 professional human engineers.

## Prerequisites

**Python packages:**

```bash
# Windows / macOS / standard venv:
pip install matchering pyloudnorm pedalboard soundfile numpy

# Debian/Ubuntu with an externally-managed Python (PEP 668), add the flag:
pip install matchering pyloudnorm pedalboard soundfile numpy --break-system-packages
```

(Or `pip install -r requirements.txt` from the skill directory.)

**FFmpeg (REQUIRED — hard dependency, not optional):** The LUFS correction + true-peak limiting stage (`adjust_lufs` in `scripts/master.py`) shells out to `ffmpeg`'s two-pass `loudnorm` filter. This stage runs by default on every master, so the pipeline will fail without `ffmpeg` on PATH. Verify with `ffmpeg -version`. On Windows install via `winget install Gyan.FFmpeg` (or grab a build and add it to PATH); it is also already on the system from lyric-video-forge.

## The Pipeline — 4 Steps

```
Raw Suno WAV  →  [1] Match to reference  →  [2] LUFS verify  →  [3] Polish (optional)  →  [4] Export
```

### Step 1: Reference Matching (Matchering)

Takes your raw track + a genre-specific reference track. Matches:
- RMS (loudness)
- Frequency Response (tonal balance)
- Peak amplitude
- Stereo width

Output: 24-bit WAV that sonically mirrors the reference.

### Step 2: LUFS Verification (PyLoudnorm)

**CRITICAL: Tracks distributed via a distributor like DistroKid (Spotify/Apple/Tidal/YouTube Music) + lyric videos on YouTube all land on platforms that normalize to -14 LUFS.**

This means mastering loud (-7 LUFS) is counterproductive — Spotify just turns it down and you lose dynamic range. The correct strategy is **-10 LUFS with -1 dBTP ceiling** — ~4 dB headroom above normalization floor for punch without sacrificing dynamics.

| Genre | Target LUFS | True Peak | Why |
|-------|-------------|-----------|-----|
| Industrial metal | **-10.0** | -1 dBTP | Punchy on Spotify, keeps dynamics |
| EDM industrial | **-10.0** | -1 dBTP | Club-ready impact preserved |
| Doom | **-11.0** | -1 dBTP | Doom NEEDS breathing room |
| Folk metal shanty | **-10.5** | -1 dBTP | Shantyman/choir contrast |
| Dark cinematic | **-12.0** | -1 dBTP | Cinematic needs widest dynamics |
| Tribal metal | **-10.0** | -1 dBTP | Primal impact |
| `--streaming` (secondary) | -14.0 | -1 dBTP | Only if you want a pre-normalized version |
| `--club` (download/DJ only) | -7.0 | -1 dBTP | NEVER upload this version to streaming |

**The math:** Spotify normalizes everything to -14 LUFS. If you master at -10, Spotify plays it at -14 with a 4 dB gain reduction applied. If you master at -7, Spotify applies 7 dB reduction — same final volume, but your -7 master had to sacrifice 3 more dB of dynamic range to get there. **Less dynamic range = worse perceived sound at the same loudness.**

If outside target ±0.5 LU, script applies gain correction.

### Step 3: Pedalboard Polish (Optional)

Apply final touches:
- Tape saturation (warmth)
- Stereo widening (for EDM/industrial)
- High-shelf boost (air, presence)
- Final brickwall limiter backup

### Step 4: Export

Outputs:
- `{name}_mastered_24bit.wav` — hi-res for DistroKid
- `{name}_mastered_16bit.wav` — CD/streaming standard
- `{name}_master_report.json` — LUFS, true peak, dynamic range measurements
- `{name}_streaming.wav` — secondary version at -14 LUFS for Spotify/YouTube (optional)

## Reference Track Setup

The skill needs genre-specific reference tracks. Place them in `references/`:

```
references/
├── reference_map.json          # Genre → filename mapping
├── industrial_metal.wav         # e.g. Rammstein "Mein Herz Brennt"
├── edm_industrial.wav           # e.g. Angerfist or Perturbator
├── doom_sludge.wav              # e.g. Electric Wizard "Dopethrone"
├── folk_metal_shanty.wav        # e.g. Wind Rose "Diggy Diggy Hole"
├── dark_cinematic.wav           # e.g. Two Steps from Hell
└── tribal_metal.wav             # e.g. Sepultura "Roots"
```

**Rule:** Reference tracks should be professionally mastered, commercially released, same key/tempo zone as your target (ideally), and match the energy you want.

## CLI Usage

```bash
# Auto-detect genre from filename or flag
python scripts/master.py --input plateau.wav --genre doom

# Explicit reference
python scripts/master.py --input evek.wav --reference references/edm_industrial.wav

# Album mode — master multiple tracks with SAME reference for consistency
python scripts/master.py --album ./tracks/ --reference references/industrial_metal.wav --output ./mastered/

# Override LUFS target
python scripts/master.py --input track.wav --genre doom --lufs -8

# Include streaming version (-14 LUFS secondary output)
python scripts/master.py --input track.wav --genre doom --streaming

# Skip polish step (Matchering only)
python scripts/master.py --input track.wav --genre doom --no-polish
```

## Pipeline Integration

This skill fits between lyric-forge (song writing) and lyric-video-forge (video):

```
┌─────────────┐    ┌────────┐    ┌──────────────────┐    ┌──────────────────┐
│ lyric-forge │───▶│ Suno   │───▶│ audio-master     │───▶│ lyric-video-forge│
│ (script)    │    │ (raw)  │    │ (mastered WAV)   │    │ (MP4 with audio) │
└─────────────┘    └────────┘    └──────────────────┘    └──────────────────┘
                                          │
                                          ▼
                                   DistroKid / Spotify
```

## Scripts

| File | Purpose |
|------|---------|
| `scripts/master.py` | Main CLI pipeline (Matchering → LUFS → Pedalboard → export) |
| `scripts/lufs_check.py` | Standalone LUFS measurement + correction |
| `scripts/reference_map.py` | Genre → reference track resolution logic |

## Quality Gate

Before delivering a master, verify:
- [ ] LUFS within ±1 of target for the genre
- [ ] True peak ≤ -1 dBTP (no clipping)
- [ ] Dynamic range (LRA) ≥ 4 LU for doom/industrial, ≥ 6 LU for shanty
- [ ] No audible artifacts introduced by limiter
- [ ] A/B compared against original Suno output (should sound tonally closer to reference, but not completely different)
