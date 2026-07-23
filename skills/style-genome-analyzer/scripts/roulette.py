"""
Mode 3: Style Roulette
Catalog audit -> gap identification -> 5 stretch proposals ->
Suno-ready packages at various stretch levels (1-5)
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Allow imports from sibling modules
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from openrouter_client import generate_text

# Conditional imports for optional sibling modules
try:
    from suno_packager import generate_style_field, format_package, generate_tag_skeleton
    _has_suno_packager = True
except ImportError:
    _has_suno_packager = False

try:
    from voice_engine import recommend_voices, voice_for_genre
    _has_voice_engine = True
except ImportError:
    _has_voice_engine = False

# Data directories
DATA_DIR = SCRIPT_DIR.parent / "data"

# ---- Genre / Style Vocabulary (exhaustive reference for gap detection) ----

ALL_GENRES = [
    # Electronic
    "techno", "house", "deep house", "tech house", "trance", "psytrance",
    "drum and bass", "dubstep", "garage", "uk garage", "breakbeat",
    "electro", "synthwave", "retrowave", "vaporwave", "ambient",
    "downtempo", "chillwave", "lo-fi", "trip-hop", "idm",
    "hardstyle", "hardcore techno", "industrial", "ebm", "darkwave",
    "future bass", "future garage", "uk funky", "grime",
    # Rock / Metal
    "rock", "hard rock", "classic rock", "alternative rock", "indie rock",
    "punk", "post-punk", "grunge", "shoegaze", "dream pop",
    "metal", "heavy metal", "thrash metal", "death metal", "black metal",
    "doom metal", "stoner rock", "progressive rock", "prog metal",
    "nu metal", "metalcore", "post-rock", "math rock", "noise rock",
    # Hip-Hop / R&B
    "hip-hop", "trap", "boom bap", "lo-fi hip-hop", "drill",
    "grime", "phonk", "cloud rap", "mumble rap", "conscious hip-hop",
    "r&b", "neo-soul", "soul", "funk", "g-funk",
    # Pop / Mainstream
    "pop", "indie pop", "synth-pop", "electropop", "k-pop", "j-pop",
    "bubblegum pop", "dance-pop", "art pop", "chamber pop",
    # Jazz / Blues
    "jazz", "bebop", "cool jazz", "free jazz", "acid jazz", "nu jazz",
    "blues", "delta blues", "chicago blues", "blues rock",
    # Classical / Orchestral
    "classical", "orchestral", "cinematic", "neo-classical",
    "baroque", "romantic era", "minimalist", "contemporary classical",
    # World / Regional
    "afrobeat", "afrobeats", "highlife", "amapiano", "kwaito",
    "reggae", "dancehall", "ska", "dub", "reggaeton",
    "latin", "salsa", "bossa nova", "samba", "cumbia", "bachata",
    "flamenco", "fado", "celtic", "folk", "americana",
    "country", "bluegrass", "outlaw country",
    "indian classical", "bollywood", "bhangra",
    "arabic", "turkish", "persian", "rai",
    "japanese traditional", "enka", "city pop",
    "k-hip-hop", "mandopop", "cantopop",
    "balkan", "klezmer", "polka", "sea shanty",
    "mongolian throat singing", "tuvan", "gamelan",
    # Other
    "gospel", "worship", "christian rock",
    "spoken word", "podcast", "asmr",
    "soundtrack", "video game music", "chiptune", "8-bit",
    "new age", "meditation", "binaural",
    "noise", "experimental", "avant-garde", "musique concrete",
]

ALL_TEMPOS = {
    "very slow (40-70 BPM)": (40, 70),
    "slow (70-90 BPM)": (70, 90),
    "moderate (90-110 BPM)": (90, 110),
    "medium (110-130 BPM)": (110, 130),
    "upbeat (130-150 BPM)": (130, 150),
    "fast (150-170 BPM)": (150, 170),
    "very fast (170-200 BPM)": (170, 200),
    "extreme (200+ BPM)": (200, 300),
}

ALL_VOCAL_MODES = [
    "clean male", "clean female", "raspy male", "raspy female",
    "falsetto", "operatic", "whisper", "spoken word", "rap",
    "screaming", "growling", "throat singing", "scat",
    "choir", "call-and-response", "chant", "yodeling",
    "auto-tuned", "vocoder", "talk-singing", "beatboxing",
    "bilingual", "multilingual",
]

ALL_STRUCTURES = [
    "verse-chorus", "verse-chorus-bridge", "AABA", "through-composed",
    "loop-based", "build-drop", "verse-prechorus-chorus",
    "intro-verse-chorus-verse-chorus-bridge-chorus-outro",
    "ambient/textural", "suite/medley", "freestyle/improvised",
    "call-and-response", "rondo", "binary (AB)", "ternary (ABA)",
    "strophic", "12-bar blues",
]

ALL_TIME_SIGNATURES = ["4/4", "3/4", "6/8", "5/4", "7/8", "12/8", "2/4", "5/8", "9/8", "11/8"]

ALL_LANGUAGES = [
    "english", "hungarian", "german", "spanish", "french", "italian",
    "portuguese", "japanese", "korean", "mandarin", "cantonese",
    "arabic", "hindi", "russian", "swedish", "finnish", "turkish",
    "polish", "czech", "dutch", "greek", "hebrew",
    "instrumental",
]

# Gemini prompt for stretch proposals
ROULETTE_PROMPT = """You are an adventurous music producer who pushes artists out of their comfort zones.
You've been given a catalog audit showing what genres, tempos, vocal modes, structures,
and languages an artist has already used — and what they've NEVER tried.

CATALOG AUDIT:
```json
{catalog_audit}
```

{constraint_section}

Your job: propose 5 stretch experiments, escalating from safe (level 1) to unhinged (level 5).
Each experiment should push the artist into unexplored territory while still being achievable.

Respond with this JSON structure:

{{
  "proposals": [
    {{
      "number": 1,
      "stretch_level": 1,
      "name": "Short evocative name",
      "concept": "2-3 sentence pitch for why this experiment is worth trying",
      "target_genre": "Primary genre to explore",
      "genre_blend": ["genre1", "genre2"],
      "why_stretch": "What makes this outside the artist's comfort zone",
      "connection_to_existing": "How their existing skills make this achievable",
      "suno_style_field": "Suno-compatible style string, max 200 chars",
      "suno_negative_tags": "Tags to exclude, max 120 chars",
      "bpm_suggestion": "XXX BPM or range",
      "key_suggestion": "Key and mode",
      "time_signature": "X/X",
      "structure_suggestion": "Song structure to use",
      "vocal_direction": "Vocal style, delivery, language",
      "production_notes": "Specific production techniques for this genre",
      "energy_arc": "How energy flows through this track",
      "reference_tracks": ["Real track 1 as reference", "Real track 2 as reference"],
      "risk_reward": "What they gain if it works vs. what they learn if it doesn't"
    }},
    // ... 4 more proposals at escalating stretch levels
  ],
  "catalog_personality": "One paragraph characterizing this artist's current musical identity based on the catalog",
  "biggest_blind_spot": "The single biggest gap in their catalog that, if filled, would make them more versatile"
}}

Rules:
- Level 1: Adjacent genre they haven't tried but could easily pull off
- Level 2: Requires learning one new technique but builds on existing strengths
- Level 3: Genuine stretch — different tempo zone, unfamiliar structure, or new vocal approach
- Level 4: Major departure — genre they've never touched, requires research
- Level 5: UNHINGED — the combination sounds absurd but you can articulate why it might work
- Each proposal must reference at least one thing from "never_tried"
- Suno style fields must be immediately usable
- Reference tracks must be real songs that exemplify what you're proposing"""


def parse_bible(bible_path: str) -> dict:
    """Parse the suno-songwriting-bible.md to extract catalog data.

    This parser is designed to handle a large markdown file with varied formatting:
    code blocks, tables, inline fields, headings, etc.
    """
    path = Path(bible_path)
    if not path.exists():
        raise FileNotFoundError(f"Bible not found: {bible_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    catalog = {
        "genres_used": [],
        "tempos_used": [],
        "keys_used": [],
        "vocal_modes_used": [],
        "languages_used": [],
        "structures_used": [],
        "themes_used": [],
        "style_fields_raw": [],
        "song_count": 0,
    }

    # ---- Extract Style Fields from code blocks ----
    # Style fields appear in ``` blocks, often after a "Style" or "Style Field" heading
    # Pattern: look for lines containing style-like content inside code blocks
    code_blocks = re.findall(r"```[^\n]*\n(.*?)```", content, re.DOTALL)
    for block in code_blocks:
        block_stripped = block.strip()
        # Skip JSON blocks, shell commands, etc.
        if block_stripped.startswith(("{", "[", "$", "#!", "import ", "from ")):
            continue
        # Style fields are typically comma-separated genre/mood descriptors
        # They tend to be 1-5 lines of genre tags
        lines = block_stripped.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # A style field line typically has commas and genre-like words
            if "," in line and len(line) > 10 and len(line) < 300:
                # Check it looks like a style field (has genre-ish words)
                lower = line.lower()
                genre_signals = [
                    "rock", "pop", "metal", "jazz", "blues", "hip", "rap",
                    "techno", "house", "electronic", "ambient", "folk",
                    "punk", "soul", "funk", "reggae", "latin", "classical",
                    "cinematic", "orchestral", "acoustic", "vocal", "beat",
                    "dark", "heavy", "fast", "slow", "aggressive", "calm",
                    "guitar", "synth", "drum", "bass", "piano", "choir",
                    "male", "female", "hungarian", "bilingual", "english",
                    "german", "ballad", "anthem", "power", "epic", "raw",
                    "lo-fi", "trap", "drill", "phonk", "grunge", "indie",
                    "motivational", "gym", "workout", "training",
                ]
                if any(sig in lower for sig in genre_signals):
                    catalog["style_fields_raw"].append(line)

    # ---- Extract BPM values ----
    # Look for BPM mentions: "120 BPM", "BPM: 140", "tempo: 95", etc.
    bpm_patterns = [
        r"(\d{2,3})\s*BPM",
        r"BPM[:\s]+(\d{2,3})",
        r"[Tt]empo[:\s]+(\d{2,3})",
        r"(\d{2,3})\s*bpm",
    ]
    for pattern in bpm_patterns:
        matches = re.findall(pattern, content)
        for m in matches:
            bpm = int(m)
            if 40 <= bpm <= 300:
                catalog["tempos_used"].append(bpm)

    # Also extract BPM from style fields
    for sf in catalog["style_fields_raw"]:
        bpm_match = re.findall(r"(\d{2,3})\s*[Bb][Pp][Mm]", sf)
        for m in bpm_match:
            bpm = int(m)
            if 40 <= bpm <= 300 and bpm not in catalog["tempos_used"]:
                catalog["tempos_used"].append(bpm)

    # ---- Extract genres from style fields ----
    for sf in catalog["style_fields_raw"]:
        # Split by comma and clean
        tags = [t.strip().lower() for t in sf.split(",")]
        for tag in tags:
            # Match against known genres
            for genre in ALL_GENRES:
                if genre in tag or tag in genre:
                    if genre not in catalog["genres_used"]:
                        catalog["genres_used"].append(genre)

    # ---- Extract genres from general content ----
    # Look for genre mentions in headings and body text
    content_lower = content.lower()
    for genre in ALL_GENRES:
        if genre in content_lower and genre not in catalog["genres_used"]:
            # Verify it's used meaningfully (not just mentioned in a list of options)
            # Check proximity to song-like context
            positions = [m.start() for m in re.finditer(re.escape(genre), content_lower)]
            for pos in positions:
                context_window = content_lower[max(0, pos - 200):pos + 200]
                # If near style field markers, song titles, or production notes
                if any(marker in context_window for marker in [
                    "style", "genre", "track", "song", "verse", "chorus",
                    "suno", "prompt", "```", "bpm", "production",
                ]):
                    catalog["genres_used"].append(genre)
                    break

    # ---- Extract keys ----
    key_pattern = r"\b([A-G][#b]?)\s*(major|minor|maj|min|m)\b"
    key_matches = re.findall(key_pattern, content, re.IGNORECASE)
    for key, mode in key_matches:
        mode_clean = "minor" if mode.lower() in ("minor", "min", "m") else "major"
        key_str = f"{key} {mode_clean}"
        if key_str not in catalog["keys_used"]:
            catalog["keys_used"].append(key_str)

    # ---- Extract vocal modes ----
    for mode in ALL_VOCAL_MODES:
        if mode.lower() in content_lower:
            if mode not in catalog["vocal_modes_used"]:
                catalog["vocal_modes_used"].append(mode)

    # ---- Extract languages ----
    for lang in ALL_LANGUAGES:
        if lang.lower() in content_lower:
            if lang not in catalog["languages_used"]:
                catalog["languages_used"].append(lang)

    # ---- Extract structures ----
    for struct in ALL_STRUCTURES:
        if struct.lower() in content_lower:
            if struct not in catalog["structures_used"]:
                catalog["structures_used"].append(struct)

    # ---- Extract themes from headings and content ----
    # Look for thematic keywords near song contexts
    theme_keywords = [
        "motivation", "gym", "workout", "training", "strength", "power",
        "love", "heartbreak", "loss", "grief", "anger", "revenge",
        "party", "celebration", "summer", "night", "darkness", "light",
        "war", "battle", "military", "survival", "resilience",
        "nature", "ocean", "mountain", "space", "cosmos",
        "rebellion", "freedom", "protest", "identity", "growth",
        "nostalgia", "memories", "hometown", "journey", "road",
        "spirituality", "meditation", "transcendence",
        "humor", "satire", "absurdist", "storytelling",
        "technology", "ai", "future", "dystopia", "cyberpunk",
        "romance", "desire", "seduction", "confidence",
    ]
    for theme in theme_keywords:
        if theme in content_lower:
            catalog["themes_used"].append(theme)

    # ---- Count songs ----
    # Heuristic: count style field code blocks as approximate song count
    catalog["song_count"] = max(len(catalog["style_fields_raw"]), 1)

    # ---- Deduplicate ----
    catalog["tempos_used"] = sorted(set(catalog["tempos_used"]))
    catalog["genres_used"] = sorted(set(catalog["genres_used"]))
    catalog["keys_used"] = sorted(set(catalog["keys_used"]))
    catalog["vocal_modes_used"] = sorted(set(catalog["vocal_modes_used"]))
    catalog["languages_used"] = sorted(set(catalog["languages_used"]))
    catalog["structures_used"] = sorted(set(catalog["structures_used"]))
    catalog["themes_used"] = sorted(set(catalog["themes_used"]))

    return catalog


def identify_gaps(catalog: dict) -> dict:
    """Identify what has never been tried based on the catalog."""
    used_genres = set(g.lower() for g in catalog.get("genres_used", []))
    used_tempos = catalog.get("tempos_used", [])
    used_vocal_modes = set(v.lower() for v in catalog.get("vocal_modes_used", []))
    used_structures = set(s.lower() for s in catalog.get("structures_used", []))
    used_languages = set(l.lower() for l in catalog.get("languages_used", []))

    # Genres never tried
    never_genres = [g for g in ALL_GENRES if g.lower() not in used_genres]

    # Tempo ranges never explored
    tempo_coverage = set()
    for bpm in used_tempos:
        for label, (lo, hi) in ALL_TEMPOS.items():
            if lo <= bpm <= hi:
                tempo_coverage.add(label)
    never_tempos = [label for label in ALL_TEMPOS if label not in tempo_coverage]

    # Vocal modes never tried
    never_vocal = [v for v in ALL_VOCAL_MODES if v.lower() not in used_vocal_modes]

    # Structures never tried
    never_structures = [s for s in ALL_STRUCTURES if s.lower() not in used_structures]

    # Time signatures (assume 4/4 is always used, check content for others)
    used_time_sigs = {"4/4"}  # default assumption
    for genre in catalog.get("genres_used", []):
        # Certain genres imply time signatures
        if genre in ("waltz", "3/4"):
            used_time_sigs.add("3/4")
    never_time_sigs = [ts for ts in ALL_TIME_SIGNATURES if ts not in used_time_sigs]

    # Languages never tried
    never_languages = [l for l in ALL_LANGUAGES if l.lower() not in used_languages]

    return {
        "never_tried_genres": never_genres,
        "never_tried_tempos": never_tempos,
        "never_tried_vocal_modes": never_vocal,
        "never_tried_structures": never_structures,
        "never_tried_time_signatures": never_time_sigs,
        "never_tried_languages": never_languages,
        "genre_gap_count": len(never_genres),
        "total_genre_vocabulary": len(ALL_GENRES),
        "genre_coverage_pct": round(
            100 * (1 - len(never_genres) / max(len(ALL_GENRES), 1)), 1
        ),
    }


def generate_stretch_proposals(catalog: dict, gaps: dict, constraint: Optional[str] = None) -> dict:
    """Send catalog audit + gaps to Gemini for stretch proposals."""
    catalog_audit = {
        "what_they_use": {
            "genres": catalog.get("genres_used", []),
            "tempos": catalog.get("tempos_used", []),
            "keys": catalog.get("keys_used", []),
            "vocal_modes": catalog.get("vocal_modes_used", []),
            "languages": catalog.get("languages_used", []),
            "structures": catalog.get("structures_used", []),
            "themes": catalog.get("themes_used", []),
            "song_count": catalog.get("song_count", 0),
        },
        "never_tried": {
            "genres": gaps.get("never_tried_genres", [])[:40],  # Cap to avoid prompt overflow
            "tempos": gaps.get("never_tried_tempos", []),
            "vocal_modes": gaps.get("never_tried_vocal_modes", []),
            "structures": gaps.get("never_tried_structures", []),
            "time_signatures": gaps.get("never_tried_time_signatures", []),
            "languages": gaps.get("never_tried_languages", [])[:20],
        },
        "coverage": {
            "genre_coverage_pct": gaps.get("genre_coverage_pct", 0),
            "genre_gap_count": gaps.get("genre_gap_count", 0),
        },
    }

    constraint_section = ""
    if constraint and constraint.lower() != "no constraints":
        constraint_section = (
            f"CONSTRAINT: The artist wants these experiments to relate to: {constraint}\n"
            "Weight your proposals toward this constraint, but don't let it prevent truly wild ideas at level 5."
        )

    prompt = ROULETTE_PROMPT.format(
        catalog_audit=json.dumps(catalog_audit, indent=2),
        constraint_section=constraint_section,
    )

    print("[Roulette] Sending catalog audit to Gemini 2.5 Pro...")
    try:
        response_text = generate_text(prompt)
        cleaned = response_text.strip()
        match = re.match(r"^```(?:json)?\s*\n?(.*?)\n?\s*```$", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
        result = json.loads(cleaned)
        print("[Roulette] Received 5 stretch proposals from Gemini")
        return result
    except json.JSONDecodeError as e:
        print(f"[Roulette] Warning: Could not parse Gemini response as JSON: {e}")
        return {
            "proposals": [],
            "raw_response": response_text,
            "error": "Failed to parse structured proposals — see raw_response",
        }
    except Exception as e:
        print(f"[Roulette] Gemini analysis failed: {e}")
        return {"proposals": [], "error": str(e)}


def generate_proposal_suno_package(proposal: dict) -> str:
    """Generate a Suno-ready package for a single proposal."""
    if _has_suno_packager:
        try:
            style_field = proposal.get("suno_style_field", "")
            tag_skeleton = ""  # Proposals don't have section data
            return format_package(style_field=style_field, tag_skeleton=tag_skeleton)
        except Exception:
            pass

    # Fallback: format inline
    lines = [
        f"# Suno Package: {proposal.get('name', 'Stretch Experiment')}",
        f"**Stretch Level: {proposal.get('stretch_level', '?')}/5**",
        "",
        f"## Concept",
        proposal.get("concept", "N/A"),
        "",
        f"## Style Field",
        "```",
        proposal.get("suno_style_field", "N/A"),
        "```",
        "",
        f"## Negative Tags",
        "```",
        proposal.get("suno_negative_tags", "N/A"),
        "```",
        "",
        f"## Technical Parameters",
        f"- **BPM:** {proposal.get('bpm_suggestion', 'N/A')}",
        f"- **Key:** {proposal.get('key_suggestion', 'N/A')}",
        f"- **Time Signature:** {proposal.get('time_signature', '4/4')}",
        f"- **Structure:** {proposal.get('structure_suggestion', 'N/A')}",
        "",
        f"## Genre Target",
        f"- **Primary:** {proposal.get('target_genre', 'N/A')}",
        f"- **Blend:** {', '.join(proposal.get('genre_blend', []))}",
        "",
        f"## Why This Is a Stretch",
        proposal.get("why_stretch", "N/A"),
        "",
        f"## Connection to Existing Work",
        proposal.get("connection_to_existing", "N/A"),
        "",
        f"## Energy Arc",
        proposal.get("energy_arc", "N/A"),
        "",
        f"## Production Notes",
        proposal.get("production_notes", "N/A"),
        "",
        f"## Vocal Direction",
        proposal.get("vocal_direction", "N/A"),
        "",
        f"## Reference Tracks",
    ]
    for ref in proposal.get("reference_tracks", []):
        lines.append(f"- {ref}")
    lines.extend([
        "",
        f"## Risk/Reward",
        proposal.get("risk_reward", "N/A"),
    ])
    return "\n".join(lines)


def generate_proposal_voice_recs(proposal: dict) -> str:
    """Generate voice recommendations for a proposal."""
    if _has_voice_engine:
        try:
            genre = proposal.get("target_genre", "rock")
            mood = "energetic"
            bpm_str = str(proposal.get("bpm_suggestion", "120"))
            # Parse BPM from string like "120 BPM" or "120-140"
            bpm_digits = re.findall(r"\d+", bpm_str)
            bpm = int(bpm_digits[0]) if bpm_digits else 120
            recs = recommend_voices(genre=genre, mood=mood, tempo=bpm)
            lines = [f"## Voice Recommendations for: {proposal.get('name', 'Stretch Experiment')}", ""]
            for i, rec in enumerate(recs):
                label = rec.get("label", rec.get("register", f"Option {i + 1}"))
                suno_field = rec.get("suno_field", "")
                desc = rec.get("description", "")
                lines.append(f"### {i + 1}. {label}")
                if desc:
                    lines.append(desc)
                if suno_field:
                    lines.append(f"\n**Suno vocal tag:** `{suno_field}`")
                lines.append("")
            return "\n".join(lines)
        except Exception:
            pass

    # Fallback: 3 basic recommendations based on vocal direction
    vocal = proposal.get("vocal_direction", "")
    genre = proposal.get("target_genre", "")

    lines = [
        f"## Voice Recommendations for: {proposal.get('name', 'Stretch Experiment')}",
        "",
        f"**Vocal Direction:** {vocal}",
        "",
        "### Recommendation 1 — Safe Match",
        f"Find a voice that naturally fits {genre}. Look for voices tagged with this genre on ElevenLabs voice library.",
        "",
        "### Recommendation 2 — Contrasting Voice",
        f"Try a voice from a completely different genre layered over {genre} production — the contrast creates novelty.",
        "",
        "### Recommendation 3 — Processed/Effected",
        f"Use a clean voice but apply genre-appropriate processing (reverb, distortion, pitch shift) to fit the {genre} aesthetic.",
        "",
        "(Install voice_engine module for detailed ElevenLabs voice ID recommendations)",
    ]
    return "\n".join(lines)


def build_roulette_report(catalog: dict, gaps: dict, proposals_data: dict) -> str:
    """Build the main roulette report markdown."""
    lines = [
        "# Style Roulette Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Catalog Audit",
        "",
        f"**Songs in catalog:** ~{catalog.get('song_count', '?')}",
        f"**Genre coverage:** {gaps.get('genre_coverage_pct', '?')}% "
        f"({len(catalog.get('genres_used', []))} of {gaps.get('total_genre_vocabulary', '?')} genres)",
        "",
        "### What You Use",
        "",
    ]

    # Genres
    genres = catalog.get("genres_used", [])
    if genres:
        lines.append(f"**Genres ({len(genres)}):** {', '.join(genres)}")
    else:
        lines.append("**Genres:** None detected")
    lines.append("")

    # Tempos
    tempos = catalog.get("tempos_used", [])
    if tempos:
        lines.append(f"**Tempo range:** {min(tempos)}-{max(tempos)} BPM")
        tempo_counts = Counter()
        for bpm in tempos:
            for label, (lo, hi) in ALL_TEMPOS.items():
                if lo <= bpm <= hi:
                    tempo_counts[label] += 1
        lines.append(f"**Tempo zones:** {', '.join(f'{k} ({v}x)' for k, v in tempo_counts.most_common())}")
    else:
        lines.append("**Tempos:** None detected")
    lines.append("")

    # Keys
    keys = catalog.get("keys_used", [])
    if keys:
        lines.append(f"**Keys ({len(keys)}):** {', '.join(keys)}")
    lines.append("")

    # Vocal modes
    vocals = catalog.get("vocal_modes_used", [])
    if vocals:
        lines.append(f"**Vocal modes ({len(vocals)}):** {', '.join(vocals)}")
    lines.append("")

    # Languages
    langs = catalog.get("languages_used", [])
    if langs:
        lines.append(f"**Languages ({len(langs)}):** {', '.join(langs)}")
    lines.append("")

    # Structures
    structs = catalog.get("structures_used", [])
    if structs:
        lines.append(f"**Structures ({len(structs)}):** {', '.join(structs)}")
    lines.append("")

    # Themes
    themes = catalog.get("themes_used", [])
    if themes:
        lines.append(f"**Themes ({len(themes)}):** {', '.join(themes)}")
    lines.append("")

    # Gaps
    lines.extend([
        "### What You've Never Tried",
        "",
    ])

    never_tempos = gaps.get("never_tried_tempos", [])
    if never_tempos:
        lines.append(f"**Unexplored tempo zones:** {', '.join(never_tempos)}")
    lines.append("")

    never_vocal = gaps.get("never_tried_vocal_modes", [])
    if never_vocal:
        lines.append(f"**Untried vocal modes ({len(never_vocal)}):** {', '.join(never_vocal)}")
    lines.append("")

    never_structs = gaps.get("never_tried_structures", [])
    if never_structs:
        lines.append(f"**Untried structures ({len(never_structs)}):** {', '.join(never_structs)}")
    lines.append("")

    never_ts = gaps.get("never_tried_time_signatures", [])
    if never_ts:
        lines.append(f"**Untried time signatures:** {', '.join(never_ts)}")
    lines.append("")

    never_langs = gaps.get("never_tried_languages", [])
    if never_langs:
        lines.append(f"**Untried languages ({len(never_langs)}):** {', '.join(never_langs[:15])}{'...' if len(never_langs) > 15 else ''}")
    lines.append("")

    genre_gap = gaps.get("genre_gap_count", 0)
    lines.append(f"**Genre gaps:** {genre_gap} unexplored genres")
    lines.append("")

    # Catalog personality
    personality = proposals_data.get("catalog_personality", "")
    if personality:
        lines.extend([
            "## Your Musical Identity",
            "",
            personality,
            "",
        ])

    # Biggest blind spot
    blind_spot = proposals_data.get("biggest_blind_spot", "")
    if blind_spot:
        lines.extend([
            "## Biggest Blind Spot",
            "",
            blind_spot,
            "",
        ])

    # Proposals
    proposals = proposals_data.get("proposals", [])
    if proposals:
        lines.extend([
            "## Stretch Proposals",
            "",
        ])
        for prop in proposals:
            level = prop.get("stretch_level", "?")
            name = prop.get("name", "Unnamed")
            genre = prop.get("target_genre", "?")
            lines.append(f"### Level {level}: {name}")
            lines.append(f"**Target Genre:** {genre}")
            lines.append("")
            lines.append(prop.get("concept", ""))
            lines.append("")
            lines.append(f"**Suno Style:** `{prop.get('suno_style_field', '')}`")
            bpm = prop.get("bpm_suggestion", "?")
            key = prop.get("key_suggestion", "?")
            lines.append(f"**BPM:** {bpm} | **Key:** {key} | **Structure:** {prop.get('structure_suggestion', '?')}")
            lines.append("")
            refs = prop.get("reference_tracks", [])
            if refs:
                lines.append(f"**References:** {', '.join(refs)}")
                lines.append("")
            lines.append(f"**Risk/Reward:** {prop.get('risk_reward', '')}")
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Style Genome Analyzer — Mode 3: Style Roulette",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python roulette.py --bible suno-songwriting-bible.md
  python roulette.py --bible bible.md --constraint "gym motivation"
  python roulette.py --bible bible.md --constraint "no constraints" --output ./my_roulette/
        """,
    )
    parser.add_argument(
        "--bible", type=str, required=True,
        help="Path to suno-songwriting-bible.md",
    )
    parser.add_argument(
        "--constraint", type=str, default=None,
        help="Optional constraint (e.g., 'gym motivation', 'no constraints')",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output directory (default: ./data/)",
    )

    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else DATA_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Step 1: Parse the bible
    print(f"[Roulette] Parsing bible: {args.bible}")
    catalog = parse_bible(args.bible)
    print(f"[Roulette] Found ~{catalog['song_count']} songs, "
          f"{len(catalog['genres_used'])} genres, "
          f"{len(catalog['tempos_used'])} tempo values, "
          f"{len(catalog['vocal_modes_used'])} vocal modes")

    # Step 2: Identify gaps
    gaps = identify_gaps(catalog)
    print(f"[Roulette] Genre coverage: {gaps['genre_coverage_pct']}% "
          f"({gaps['genre_gap_count']} genres never tried)")

    # Save catalog audit
    audit_path = output_dir / f"catalog-audit_{timestamp}.json"
    with open(audit_path, "w", encoding="utf-8") as f:
        json.dump({
            "catalog": catalog,
            "gaps": gaps,
            "bible_path": str(args.bible),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2, ensure_ascii=False, default=str)
    print(f"[Output] Catalog audit: {audit_path}")

    # Step 3: Generate stretch proposals via Gemini
    proposals_data = generate_stretch_proposals(catalog, gaps, args.constraint)

    # Step 4: Generate Suno packages and voice recs for each proposal
    proposals = proposals_data.get("proposals", [])
    for i, proposal in enumerate(proposals):
        # Suno package
        suno_md = generate_proposal_suno_package(proposal)
        proposal["_suno_package"] = suno_md

        # Voice recommendations
        voice_md = generate_proposal_voice_recs(proposal)
        proposal["_voice_recs"] = voice_md

        # Save individual file
        individual_path = output_dir / f"roulette-{i + 1}_{timestamp}.md"
        with open(individual_path, "w", encoding="utf-8") as f:
            f.write(suno_md)
            f.write("\n\n---\n\n")
            f.write(voice_md)
        print(f"[Output] Proposal {i + 1}: {individual_path}")

    # Build and save the main report
    report = build_roulette_report(catalog, gaps, proposals_data)
    report_path = output_dir / f"roulette-report_{timestamp}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[Output] Report: {report_path}")

    # Console summary
    print("\n" + "=" * 60)
    print("STYLE ROULETTE COMPLETE")
    print("=" * 60)
    print(f"  Songs in catalog: ~{catalog['song_count']}")
    print(f"  Genres used: {len(catalog['genres_used'])}")
    print(f"  Genre coverage: {gaps['genre_coverage_pct']}%")
    print(f"  Tempo range: {min(catalog['tempos_used'])}-{max(catalog['tempos_used'])} BPM" if catalog["tempos_used"] else "  Tempos: none detected")
    print(f"  Languages: {', '.join(catalog['languages_used'])}" if catalog["languages_used"] else "  Languages: none detected")

    if proposals:
        print("\n  STRETCH PROPOSALS:")
        for prop in proposals:
            level = prop.get("stretch_level", "?")
            name = prop.get("name", "Unnamed")
            genre = prop.get("target_genre", "?")
            print(f"    [{level}/5] {name} — {genre}")

    personality = proposals_data.get("catalog_personality", "")
    if personality:
        print(f"\n  IDENTITY: {personality[:200]}{'...' if len(personality) > 200 else ''}")

    blind_spot = proposals_data.get("biggest_blind_spot", "")
    if blind_spot:
        print(f"\n  BLIND SPOT: {blind_spot[:200]}{'...' if len(blind_spot) > 200 else ''}")

    print("=" * 60)


if __name__ == "__main__":
    main()
