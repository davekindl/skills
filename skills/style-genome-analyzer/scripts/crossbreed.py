"""
Mode 2: Style DNA Crossbreeder
2-5 blueprints -> common DNA extraction -> 5 unexpected mutations ->
Suno-ready packages for each mutation
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Allow imports from sibling modules
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from openrouter_client import analyze_audio, generate_text

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
BLUEPRINTS_DIR = DATA_DIR / "blueprints"
CROSSBREEDS_DIR = DATA_DIR / "crossbreeds"

# Gemini prompt for crossbreeding
CROSSBREED_PROMPT = """You are a genre-bending music producer who specializes in creating unexpected
style fusions. You have deep knowledge of every genre from Mongolian throat singing to UK garage.

I'm giving you the common DNA and divergent elements extracted from {track_count} tracks.
Your job: create 5 UNEXPECTED genre mutations that combine elements from these tracks
in ways the original artists would never have tried.

COMMON DNA (what all tracks share):
```json
{common_dna}
```

DIVERGENT ELEMENTS (where tracks differ — these are your mutation fuel):
```json
{divergent}
```

{intent_section}

For each mutation, respond with this JSON structure:

{{
  "mutations": [
    {{
      "number": 1,
      "name": "Short evocative name for this mutation",
      "concept": "2-3 sentence description of what this sounds like and why it works",
      "genre_blend": ["genre1", "genre2", "genre3"],
      "borrowed_elements": {{
        "from_common_dna": ["element taken from shared DNA"],
        "from_divergent": ["element borrowed from a specific track's unique quality"]
      }},
      "suno_style_field": "Suno-compatible style string, max 200 chars, comma-separated tags",
      "suno_negative_tags": "Tags to exclude, max 120 chars",
      "bpm_range": "XXX-XXX",
      "key_suggestion": "Key and mode",
      "energy_arc": "How the energy should flow through the track",
      "production_notes": "Specific production techniques to use",
      "vocal_direction": "How vocals should be delivered — tone, style, language",
      "risk_level": "1-5 (1=safe fusion, 5=extremely experimental)",
      "reference_mashup": "If artist X met artist Y in genre Z"
    }},
    // ... 4 more mutations, escalating from safe (1) to unhinged (5)
  ],
  "cross_pollination_insight": "One paragraph about what makes these tracks secretly compatible"
}}

Rules:
- Mutation 1 should be a SAFE fusion that clearly works
- Mutation 5 should be UNHINGED — the kind of thing that sounds crazy but might be genius
- Each mutation must borrow at least one element from the common DNA and one from the divergent elements
- Suno style fields must be immediately usable — no vague terms
- Be specific about production techniques, not just genre labels"""


def run_extract(url: str) -> dict:
    """Run extract.py on a YouTube URL and return the blueprint."""
    extract_script = SCRIPT_DIR / "extract.py"
    if not extract_script.exists():
        raise FileNotFoundError(f"extract.py not found at {extract_script}")

    output_dir = BLUEPRINTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[Crossbreed] Running Blueprint Extract on: {url}")
    result = subprocess.run(
        [
            sys.executable, str(extract_script),
            "--url", url,
            "--output", str(output_dir),
            "--save",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[Crossbreed] extract.py stderr:\n{result.stderr}")
        raise RuntimeError(f"Blueprint extract failed for {url}")

    # Find the most recently created blueprint in the output dir
    blueprints = sorted(
        output_dir.glob("*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not blueprints:
        raise RuntimeError(f"No blueprint file found after extracting {url}")

    bp_path = blueprints[0]
    print(f"[Crossbreed] Blueprint ready: {bp_path.name}")
    with open(bp_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_blueprint(path: str) -> dict:
    """Load a blueprint from a JSON file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Blueprint not found: {path}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_common_dna(blueprints: list[dict]) -> dict:
    """Extract common musical DNA across all blueprints."""
    import statistics

    # Collect all BPMs
    bpms = []
    for bp in blueprints:
        bpm = bp.get("technical", {}).get("bpm") or bp.get("summary", {}).get("bpm")
        if bpm and isinstance(bpm, (int, float)):
            bpms.append(float(bpm))

    # Tempo cluster
    tempo_cluster = {}
    if bpms:
        avg_bpm = statistics.mean(bpms)
        min_bpm = min(bpms)
        max_bpm = max(bpms)
        spread = max_bpm - min_bpm

        if spread < 10:
            tempo_desc = f"Tight cluster around {avg_bpm:.0f} BPM"
        elif spread < 30:
            tempo_desc = f"Moderate range {min_bpm:.0f}-{max_bpm:.0f} BPM (avg {avg_bpm:.0f})"
        else:
            tempo_desc = f"Wide range {min_bpm:.0f}-{max_bpm:.0f} BPM — tempo is divergent, not shared"

        tempo_cluster = {
            "average_bpm": round(avg_bpm, 1),
            "min_bpm": round(min_bpm, 1),
            "max_bpm": round(max_bpm, 1),
            "spread": round(spread, 1),
            "description": tempo_desc,
        }

    # Collect keys
    keys = []
    for bp in blueprints:
        key_info = bp.get("technical", {}).get("key", {})
        if isinstance(key_info, dict) and key_info.get("key"):
            keys.append(f"{key_info['key']} {key_info.get('mode', '')}")

    # Collect genres across all tracks
    all_genres = []
    for bp in blueprints:
        genres = (
            bp.get("subjective", {}).get("genre_tags", [])
            or bp.get("summary", {}).get("genres", [])
        )
        all_genres.extend(genres)

    # Find common genres (appearing in more than half the tracks)
    genre_counts = {}
    for g in all_genres:
        g_lower = g.lower().strip()
        genre_counts[g_lower] = genre_counts.get(g_lower, 0) + 1

    threshold = len(blueprints) / 2
    common_genres = [g for g, c in genre_counts.items() if c >= threshold]

    # Collect moods
    all_moods = []
    for bp in blueprints:
        moods = (
            bp.get("subjective", {}).get("mood_tags", [])
            or bp.get("summary", {}).get("moods", [])
        )
        all_moods.extend(moods)

    mood_counts = {}
    for m in all_moods:
        m_lower = m.lower().strip()
        mood_counts[m_lower] = mood_counts.get(m_lower, 0) + 1

    common_moods = [m for m, c in mood_counts.items() if c >= threshold]

    # Vocal patterns
    vocal_styles = []
    for bp in blueprints:
        vs = bp.get("subjective", {}).get("vocal_style", "")
        if vs:
            vocal_styles.append(vs)

    # Energy patterns
    energy_arcs = []
    for bp in blueprints:
        ea = bp.get("subjective", {}).get("energy_arc", "")
        if ea:
            energy_arcs.append(ea)

    # Production styles
    production_styles = []
    for bp in blueprints:
        ps = bp.get("subjective", {}).get("production_style", "")
        if ps:
            production_styles.append(ps)

    # Rhythmic info
    time_sigs = []
    for bp in blueprints:
        ts = bp.get("technical", {}).get("time_signature", {})
        if isinstance(ts, dict):
            time_sigs.append(ts.get("time_signature", "4/4"))
        elif isinstance(ts, str):
            time_sigs.append(ts)

    # Brightness
    brightness_values = []
    for bp in blueprints:
        b = bp.get("technical", {}).get("brightness") or bp.get("summary", {}).get("brightness")
        if b:
            brightness_values.append(b)

    common_dna = {
        "tempo_cluster": tempo_cluster,
        "vocal_pattern": {
            "styles": vocal_styles,
            "common_thread": _find_common_thread(vocal_styles) if vocal_styles else "no vocal data",
        },
        "energy_trick": {
            "arcs": energy_arcs,
            "common_thread": _find_common_thread(energy_arcs) if energy_arcs else "no energy data",
        },
        "rhythmic_shared": {
            "time_signatures": list(set(time_sigs)),
            "dominant_time_sig": max(set(time_sigs), key=time_sigs.count) if time_sigs else "4/4",
        },
        "emotional_core": {
            "common_genres": common_genres,
            "common_moods": common_moods,
            "keys": keys,
            "brightness": brightness_values,
        },
        "production_commonalities": {
            "styles": production_styles,
        },
    }

    return common_dna


def _find_common_thread(descriptions: list[str]) -> str:
    """Find the common thread across multiple text descriptions using simple keyword overlap."""
    if not descriptions:
        return "none"
    if len(descriptions) == 1:
        return descriptions[0]

    # Tokenize and find common words (excluding stopwords)
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "can", "this", "that",
        "these", "those", "it", "its", "very", "quite", "rather", "some",
    }

    word_sets = []
    for desc in descriptions:
        words = set(
            w.lower().strip(".,;:!?\"'()[]")
            for w in desc.split()
            if len(w) > 2 and w.lower() not in stopwords
        )
        word_sets.append(words)

    if not word_sets:
        return "diverse styles"

    # Find words appearing in at least half the descriptions
    all_words = set()
    for ws in word_sets:
        all_words |= ws

    common_words = []
    threshold = len(word_sets) / 2
    for word in all_words:
        count = sum(1 for ws in word_sets if word in ws)
        if count >= threshold:
            common_words.append(word)

    if common_words:
        return f"Shared elements: {', '.join(sorted(common_words)[:10])}"
    return "Diverse approaches — no dominant shared pattern"


def extract_divergent_elements(blueprints: list[dict]) -> list[dict]:
    """Identify where tracks differ from each other."""
    divergent = []

    for i, bp in enumerate(blueprints):
        title = bp.get("meta", {}).get("title", f"Track {i + 1}")
        subjective = bp.get("subjective", {})
        technical = bp.get("technical", {})
        summary = bp.get("summary", {})

        unique = {
            "track": title,
            "unique_genres": subjective.get("genre_tags", summary.get("genres", [])),
            "unique_moods": subjective.get("mood_tags", summary.get("moods", [])),
            "bpm": technical.get("bpm", summary.get("bpm")),
            "key": technical.get("key", {}),
            "vocal_style": subjective.get("vocal_style", ""),
            "production_style": subjective.get("production_style", ""),
            "instrumentation": subjective.get("instrumentation", []),
            "standout_moments": subjective.get("standout_moments", []),
            "steal_list": bp.get("steal_list", subjective.get("steal_list", [])),
            "sonic_texture": subjective.get("sonic_texture", ""),
            "harmonic_character": subjective.get("harmonic_character", ""),
        }
        divergent.append(unique)

    return divergent


def generate_mutations(common_dna: dict, divergent: list[dict], intent: Optional[str] = None) -> dict:
    """Send common DNA + divergent elements to Gemini for mutation generation."""
    intent_section = ""
    if intent:
        intent_section = f"INTENT: The user wants to use these mutations for: {intent}\nWeight your mutations toward this purpose."

    prompt = CROSSBREED_PROMPT.format(
        track_count=len(divergent),
        common_dna=json.dumps(common_dna, indent=2),
        divergent=json.dumps(divergent, indent=2),
        intent_section=intent_section,
    )

    print("[Crossbreed] Sending DNA to Gemini 2.5 Pro for mutation generation...")
    try:
        response_text = generate_text(prompt)
        # Try to parse as JSON
        cleaned = response_text.strip()
        # Strip markdown code blocks if present
        import re
        match = re.match(r"^```(?:json)?\s*\n?(.*?)\n?\s*```$", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
        result = json.loads(cleaned)
        print("[Crossbreed] Received 5 mutations from Gemini")
        return result
    except json.JSONDecodeError as e:
        print(f"[Crossbreed] Warning: Could not parse Gemini response as JSON: {e}")
        return {
            "mutations": [],
            "raw_response": response_text,
            "error": "Failed to parse structured mutations — see raw_response",
        }
    except Exception as e:
        print(f"[Crossbreed] Gemini analysis failed: {e}")
        return {"mutations": [], "error": str(e)}


def generate_mutation_suno_package(mutation: dict) -> str:
    """Generate a Suno-ready package for a single mutation."""
    if _has_suno_packager:
        try:
            style_field = mutation.get("suno_style_field", "")
            tag_skeleton = ""  # Mutations don't have section data
            return format_package(style_field=style_field, tag_skeleton=tag_skeleton)
        except Exception:
            pass

    # Fallback: format inline
    lines = [
        f"# Suno Package: {mutation.get('name', 'Mutation')}",
        "",
        f"## Concept",
        mutation.get("concept", "N/A"),
        "",
        f"## Style Field",
        "```",
        mutation.get("suno_style_field", "N/A"),
        "```",
        "",
        f"## Negative Tags",
        "```",
        mutation.get("suno_negative_tags", "N/A"),
        "```",
        "",
        f"## Technical Parameters",
        f"- **BPM Range:** {mutation.get('bpm_range', 'N/A')}",
        f"- **Key:** {mutation.get('key_suggestion', 'N/A')}",
        f"- **Risk Level:** {mutation.get('risk_level', 'N/A')}/5",
        "",
        f"## Genre Blend",
    ]
    for g in mutation.get("genre_blend", []):
        lines.append(f"- {g}")
    lines.extend([
        "",
        f"## Energy Arc",
        mutation.get("energy_arc", "N/A"),
        "",
        f"## Production Notes",
        mutation.get("production_notes", "N/A"),
        "",
        f"## Vocal Direction",
        mutation.get("vocal_direction", "N/A"),
        "",
        f"## Reference Mashup",
        mutation.get("reference_mashup", "N/A"),
    ])
    return "\n".join(lines)


def generate_mutation_voice_recs(mutation: dict) -> str:
    """Generate voice recommendations for a single mutation."""
    if _has_voice_engine:
        try:
            genre = (mutation.get("genre_blend", ["unknown"]) or ["unknown"])[0]
            mood = "energetic"  # Default for mutations
            bpm_str = mutation.get("bpm_range", "120")
            # Parse BPM from range like "120-140"
            bpm_parts = bpm_str.replace(" ", "").split("-")
            bpm = int(bpm_parts[0]) if bpm_parts[0].isdigit() else 120
            recs = recommend_voices(genre=genre, mood=mood, tempo=bpm)
            lines = [f"## Voice Recommendations", ""]
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

    # Fallback
    vocal = mutation.get("vocal_direction", "No vocal direction specified")
    return f"## Voice Recommendations\n\n**Direction:** {vocal}\n\n(Install voice_engine module for detailed ElevenLabs voice recommendations)"


def build_crossbreed_report(
    blueprints: list[dict],
    common_dna: dict,
    divergent: list[dict],
    mutations_data: dict,
) -> str:
    """Build the main crossbreed report markdown."""
    lines = [
        "# Style DNA Crossbreed Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Input Tracks:** {len(blueprints)}",
        "",
        "## Source Tracks",
        "",
    ]

    for i, bp in enumerate(blueprints):
        meta = bp.get("meta", {})
        summary = bp.get("summary", {})
        title = meta.get("title", f"Track {i + 1}")
        bpm = summary.get("bpm", "?")
        key = summary.get("key", "?")
        genres = ", ".join(summary.get("genres", []))
        lines.append(f"{i + 1}. **{title}** — {bpm} BPM, {key}, [{genres}]")

    lines.extend([
        "",
        "## Common DNA",
        "",
    ])

    # Tempo cluster
    tc = common_dna.get("tempo_cluster", {})
    if tc:
        lines.append(f"### Tempo Cluster")
        lines.append(f"- {tc.get('description', 'N/A')}")
        lines.append("")

    # Emotional core
    ec = common_dna.get("emotional_core", {})
    if ec:
        lines.append("### Emotional Core")
        if ec.get("common_genres"):
            lines.append(f"- **Shared Genres:** {', '.join(ec['common_genres'])}")
        if ec.get("common_moods"):
            lines.append(f"- **Shared Moods:** {', '.join(ec['common_moods'])}")
        lines.append("")

    # Rhythmic
    rs = common_dna.get("rhythmic_shared", {})
    if rs:
        lines.append("### Rhythmic Pattern")
        lines.append(f"- **Dominant Time Sig:** {rs.get('dominant_time_sig', '?')}")
        lines.append("")

    # Vocal
    vp = common_dna.get("vocal_pattern", {})
    if vp:
        lines.append("### Vocal Pattern")
        lines.append(f"- {vp.get('common_thread', 'N/A')}")
        lines.append("")

    # Energy
    et = common_dna.get("energy_trick", {})
    if et:
        lines.append("### Energy Pattern")
        lines.append(f"- {et.get('common_thread', 'N/A')}")
        lines.append("")

    # Divergent elements
    lines.extend([
        "## Divergent Elements",
        "",
    ])
    for div in divergent:
        lines.append(f"### {div.get('track', 'Unknown')}")
        if div.get("unique_genres"):
            lines.append(f"- **Genres:** {', '.join(div['unique_genres'])}")
        if div.get("steal_list"):
            lines.append(f"- **Steal:** {'; '.join(div['steal_list'][:3])}")
        lines.append("")

    # Mutations
    mutations = mutations_data.get("mutations", [])
    if mutations:
        lines.extend([
            "## Mutations",
            "",
        ])
        for mut in mutations:
            num = mut.get("number", "?")
            name = mut.get("name", "Unnamed")
            risk = mut.get("risk_level", "?")
            lines.append(f"### Mutation {num}: {name} (Risk: {risk}/5)")
            lines.append("")
            lines.append(mut.get("concept", ""))
            lines.append("")
            lines.append(f"**Suno Style:** `{mut.get('suno_style_field', '')}`")
            lines.append(f"**BPM:** {mut.get('bpm_range', '?')} | **Key:** {mut.get('key_suggestion', '?')}")
            lines.append(f"**Reference:** {mut.get('reference_mashup', '')}")
            lines.append("")

    # Cross-pollination insight
    insight = mutations_data.get("cross_pollination_insight", "")
    if insight:
        lines.extend([
            "## Cross-Pollination Insight",
            "",
            insight,
            "",
        ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Style Genome Analyzer — Mode 2: Style DNA Crossbreeder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python crossbreed.py --blueprints track1.json track2.json track3.json
  python crossbreed.py --urls "https://youtu.be/abc" "https://youtu.be/def"
  python crossbreed.py --blueprints a.json b.json --intent "dark gym motivation"
        """,
    )
    parser.add_argument(
        "--blueprints", nargs="+", type=str,
        help="Paths to 2-5 blueprint.json files",
    )
    parser.add_argument(
        "--urls", nargs="+", type=str,
        help="YouTube URLs to analyze first (runs extract.py on each)",
    )
    parser.add_argument(
        "--intent", type=str, default=None,
        help="What you plan to use these mutations for",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output directory (default: ./data/crossbreeds/)",
    )

    args = parser.parse_args()

    if not args.blueprints and not args.urls:
        parser.error("Provide --blueprints or --urls (or both)")

    # Validate count
    bp_count = len(args.blueprints or []) + len(args.urls or [])
    if bp_count < 2:
        parser.error("Need at least 2 tracks for crossbreeding")
    if bp_count > 5:
        parser.error("Maximum 5 tracks for crossbreeding")

    output_dir = Path(args.output) if args.output else CROSSBREEDS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Load all blueprints
    blueprints = []

    if args.blueprints:
        for bp_path in args.blueprints:
            print(f"[Crossbreed] Loading blueprint: {bp_path}")
            bp = load_blueprint(bp_path)
            blueprints.append(bp)
            print(f"[Crossbreed] Loaded: {bp.get('meta', {}).get('title', 'Unknown')}")

    if args.urls:
        for url in args.urls:
            bp = run_extract(url)
            blueprints.append(bp)

    print(f"\n[Crossbreed] {len(blueprints)} blueprints loaded. Extracting DNA...")

    # Step 2: Extract common DNA
    common_dna = extract_common_dna(blueprints)

    # Step 3: Identify divergent elements
    divergent = extract_divergent_elements(blueprints)

    # Step 4: Generate mutations via Gemini
    mutations_data = generate_mutations(common_dna, divergent, args.intent)

    # Step 5: Generate Suno packages and voice recs for each mutation
    mutations = mutations_data.get("mutations", [])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, mutation in enumerate(mutations):
        # Suno package
        suno_md = generate_mutation_suno_package(mutation)
        mutation["_suno_package"] = suno_md

        suno_path = output_dir / f"crossbreed-{i + 1}_{timestamp}.md"
        with open(suno_path, "w", encoding="utf-8") as f:
            f.write(suno_md)
            f.write("\n\n---\n\n")
            # Append voice recommendations
            voice_md = generate_mutation_voice_recs(mutation)
            f.write(voice_md)
        print(f"[Output] Mutation {i + 1}: {suno_path}")

    # Step 6: Save common DNA
    dna_path = output_dir / f"common-dna_{timestamp}.json"
    with open(dna_path, "w", encoding="utf-8") as f:
        json.dump({
            "common_dna": common_dna,
            "divergent_elements": divergent,
            "source_tracks": [
                bp.get("meta", {}).get("title", "Unknown") for bp in blueprints
            ],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }, f, indent=2, ensure_ascii=False)
    print(f"[Output] Common DNA: {dna_path}")

    # Build and save the main report
    report = build_crossbreed_report(blueprints, common_dna, divergent, mutations_data)
    report_path = output_dir / f"crossbreed-report_{timestamp}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[Output] Report: {report_path}")

    # Console summary
    print("\n" + "=" * 60)
    print("CROSSBREED COMPLETE")
    print("=" * 60)
    print(f"  Tracks analyzed: {len(blueprints)}")
    print(f"  Mutations generated: {len(mutations)}")

    for mut in mutations:
        risk = mut.get("risk_level", "?")
        name = mut.get("name", "Unnamed")
        style = mut.get("suno_style_field", "")
        print(f"\n  [{risk}/5] {name}")
        print(f"       Style: {style[:80]}{'...' if len(style) > 80 else ''}")

    insight = mutations_data.get("cross_pollination_insight", "")
    if insight:
        print(f"\n  INSIGHT: {insight[:200]}{'...' if len(insight) > 200 else ''}")

    print("=" * 60)


if __name__ == "__main__":
    main()
