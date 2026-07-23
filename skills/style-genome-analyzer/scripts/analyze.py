"""
Subjective Audio Analysis — Gemini 2.5 Pro prompt for musical DNA extraction.

Takes librosa technical data + audio file, sends to Gemini via OpenRouter,
returns structured subjective analysis (vocal DNA, rhythmic hooks, production
fingerprint, energy arc, instrument roles, genre genome).
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from openrouter_client import analyze_audio


ANALYSIS_PROMPT = """You are a music producer analyzing a reference track for style replication in Suno.ai. I've already extracted technical data (provided below). Now I need the SUBJECTIVE analysis — the things that make this track feel like itself.

Technical data: {technical_data}

Analyze the audio and return a JSON object with these fields:

1. "vocal_dna": For each section you can identify, describe:
   - delivery: whispered/spoken/sung/belted/screamed/chanted
   - texture: clean/raspy/gravelly/nasal/breathy/guttural
   - mic_feel: close-mic-intimate / room-reverb / cathedral-huge
   - layering: solo/doubled/choir/call-response
   - pitch_range: low-baritone/mid/tenor/high
   - intensity: 1-5

2. "rhythmic_hook": What makes the main hook physically engaging?
   - syllable_pattern: stressed/unstressed per line
   - chantability_score: 1-10 (could a crowd yell this?)
   - rhythmic_trick: what makes it stick (e.g., "pause before the word that hits", "triplet feel in a 4/4 context")

3. "production_fingerprint": 5 specific production choices that make this track sound like ITSELF, not a generic version of its genre. Be precise and Suno-translatable.

4. "energy_arc": Describe the emotional journey as a curve. Note deliberate DROPS in energy — these matter more than peaks.

5. "instrument_roles": For each instrument detected:
   - role: bed/hook/accent/fill/transition
   - when_active: which sections
   - when_deliberately_absent: which sections (absence = choice)

6. "genre_genome": The 2-3 genre tags that would best reproduce this feel in Suno. Not the obvious genre — the EFFECTIVE genre. (e.g., a folk metal track might be effectively a "work song with distortion" rather than "folk metal")

7. "voice_recommendations": 3 alternative vocal approaches that would work with this instrumental bed but create a different feel. Describe each in Suno style field language.

Return ONLY valid JSON, no markdown, no preamble."""


def run_subjective_analysis(audio_path: str, technical_data: dict) -> dict:
    """
    Send audio + technical data to Gemini 2.5 Pro for subjective analysis.

    Returns parsed JSON dict with vocal_dna, rhythmic_hook, production_fingerprint,
    energy_arc, instrument_roles, genre_genome, voice_recommendations.
    """
    prompt = ANALYSIS_PROMPT.format(
        technical_data=json.dumps(technical_data, indent=2)
    )

    result = analyze_audio(audio_path, prompt, technical_data)
    return result


def build_steal_list(subjective: dict) -> list[str]:
    """
    Extract actionable 'steal' items from subjective analysis.
    These are specific production choices translatable to Suno style fields.
    """
    steals = []

    # From production fingerprint
    fingerprints = subjective.get("production_fingerprint", [])
    if isinstance(fingerprints, list):
        for fp in fingerprints:
            if isinstance(fp, str):
                steals.append(fp)
            elif isinstance(fp, dict):
                steals.append(fp.get("description", str(fp)))

    # From rhythmic hook
    hook = subjective.get("rhythmic_hook", {})
    if isinstance(hook, dict):
        trick = hook.get("rhythmic_trick", "")
        if trick:
            steals.append(f"Rhythmic trick: {trick}")

    # From energy arc
    arc = subjective.get("energy_arc", "")
    if isinstance(arc, str) and arc:
        steals.append(f"Energy arc: {arc}")
    elif isinstance(arc, dict):
        desc = arc.get("description", arc.get("curve", ""))
        if desc:
            steals.append(f"Energy arc: {desc}")

    return steals


def build_avoid_list(subjective: dict, source_title: str = "") -> list[str]:
    """
    Generate 'avoid' items — things specific to the source track
    that shouldn't be replicated (artist-specific vocal timbre, gimmicks, etc.)
    """
    avoids = []

    # Warn about artist-specific vocal timbre
    vocal = subjective.get("vocal_dna", {})
    if isinstance(vocal, dict):
        texture = vocal.get("texture", "")
        if texture:
            avoids.append(
                f"The specific vocal timbre is unique to the source artist — "
                f"don't replicate '{texture}' directly, use your own gravelly baritone instead"
            )
    elif isinstance(vocal, list) and vocal:
        first = vocal[0] if isinstance(vocal[0], dict) else {}
        texture = first.get("texture", "")
        if texture:
            avoids.append(
                f"Source vocal texture '{texture}' is artist-specific — "
                f"adapt the delivery style, not the timbre"
            )

    # Generic avoids
    avoids.append(
        "Sound effects or vocal tricks that are gimmicky — "
        "replace with genre-appropriate equivalents"
    )

    return avoids


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run subjective audio analysis via Gemini")
    parser.add_argument("--audio", required=True, help="Path to audio file")
    parser.add_argument("--technical", required=True, help="Path to technical data JSON")
    parser.add_argument("--output", default="./subjective_analysis.json")
    args = parser.parse_args()

    tech = json.loads(Path(args.technical).read_text())
    result = run_subjective_analysis(args.audio, tech)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2))

    print(f"\nSubjective analysis saved to {args.output}")
    print(f"  Genre genome: {result.get('genre_genome', 'N/A')}")
    print(f"  Production fingerprints: {len(result.get('production_fingerprint', []))}")
    print(f"  Voice recommendations: {len(result.get('voice_recommendations', []))}")
