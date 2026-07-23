"""
Mode 1: Blueprint Extract
YouTube URL or MP3 -> technical extraction (librosa/madmom) ->
subjective analysis (Gemini 2.5 Pro) -> Suno-ready blueprint
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
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

# Data directory defaults
DATA_DIR = SCRIPT_DIR.parent / "data"
BLUEPRINTS_DIR = DATA_DIR / "blueprints"

# Krumhansl-Schmuckler key profiles
MAJOR_PROFILE = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
MINOR_PROFILE = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Gemini prompt for subjective analysis
SUBJECTIVE_PROMPT = """You are a professional music producer and sound designer analyzing a track.

Listen to this audio carefully and provide a detailed subjective analysis as JSON with these exact fields:

{
  "genre_tags": ["primary genre", "subgenre1", "subgenre2"],
  "mood_tags": ["mood1", "mood2", "mood3"],
  "energy_arc": "Description of how energy flows through the track — where it builds, peaks, drops",
  "vocal_style": "Description of vocal delivery, tone, attitude, language if identifiable",
  "production_style": "Description of production techniques — compression, reverb, layering, mixing approach",
  "instrumentation": ["instrument1", "instrument2", "instrument3"],
  "rhythmic_feel": "Description of groove, swing, syncopation, beat patterns",
  "harmonic_character": "Description of chord progressions, harmonic tension, resolution patterns",
  "sonic_texture": "Description of frequency balance — bass weight, midrange presence, high-end sparkle",
  "reference_artists": ["artist1", "artist2", "artist3"],
  "standout_moments": ["Timestamp or description of the most striking moment", "another moment"],
  "steal_list": [
    "Specific production technique worth stealing",
    "Specific arrangement trick worth stealing",
    "Specific vocal technique worth stealing"
  ],
  "avoid_list": [
    "Something in this track that doesn't work well",
    "Another element to avoid when recreating this style"
  ],
  "suno_style_field": "A Suno-compatible style/genre string that would recreate this track's vibe (max 200 chars, comma-separated tags)",
  "suno_negative_tags": "Tags to exclude in Suno to avoid wrong directions (max 120 chars)"
}

Be specific and actionable. The steal_list should contain techniques a producer could actually implement.
The suno_style_field should be immediately usable in Suno's style field — no vague terms."""


def download_youtube_audio(url: str, output_dir: str) -> tuple[str, str]:
    """Download audio from YouTube URL using yt-dlp.

    Returns (audio_path, title).
    """
    print(f"[Download] Fetching audio from: {url}")

    # Check yt-dlp is available
    try:
        subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "yt-dlp is not installed. Install with: pip install yt-dlp"
        )

    # Get title first
    title_result = subprocess.run(
        ["yt-dlp", "--get-title", "--no-warnings", url],
        capture_output=True,
        text=True,
    )
    title = title_result.stdout.strip() or "unknown_track"
    # Sanitize title for filename
    safe_title = re.sub(r'[^\w\s\-]', '', title)[:80].strip()
    safe_title = re.sub(r'\s+', '_', safe_title)

    output_template = os.path.join(output_dir, f"{safe_title}.%(ext)s")

    result = subprocess.run(
        [
            "yt-dlp",
            "-x",                          # extract audio
            "--audio-format", "mp3",       # convert to mp3
            "--audio-quality", "0",        # best quality
            "--no-playlist",               # single video only
            "--no-warnings",
            "-o", output_template,
            url,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"yt-dlp failed (exit {result.returncode}):\n{result.stderr}"
        )

    # Find the output file
    mp3_path = os.path.join(output_dir, f"{safe_title}.mp3")
    if os.path.exists(mp3_path):
        print(f"[Download] Saved: {mp3_path}")
        return mp3_path, title

    # Fallback: look for any audio file in the output dir
    for f in os.listdir(output_dir):
        if f.endswith((".mp3", ".m4a", ".wav", ".opus", ".webm")):
            found_path = os.path.join(output_dir, f)
            print(f"[Download] Saved: {found_path}")
            return found_path, title

    raise RuntimeError(
        f"yt-dlp completed but no audio file found in {output_dir}"
    )


def detect_key(y, sr) -> dict:
    """Detect musical key using chroma features + Krumhansl-Schmuckler algorithm."""
    import numpy as np

    try:
        import librosa
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    except Exception as e:
        return {"key": "unknown", "mode": "unknown", "confidence": 0, "error": str(e)}

    # Average chroma energy per pitch class
    chroma_mean = np.mean(chroma, axis=1)

    best_corr = -2
    best_key = "C"
    best_mode = "major"

    for shift in range(12):
        # Rotate profile to test each key
        major_rotated = np.roll(MAJOR_PROFILE, shift)
        minor_rotated = np.roll(MINOR_PROFILE, shift)

        corr_major = np.corrcoef(chroma_mean, major_rotated)[0, 1]
        corr_minor = np.corrcoef(chroma_mean, minor_rotated)[0, 1]

        if corr_major > best_corr:
            best_corr = corr_major
            best_key = PITCH_CLASSES[shift]
            best_mode = "major"

        if corr_minor > best_corr:
            best_corr = corr_minor
            best_key = PITCH_CLASSES[shift]
            best_mode = "minor"

    return {
        "key": best_key,
        "mode": best_mode,
        "confidence": round(float(best_corr), 4),
    }


def estimate_time_signature(y, sr) -> dict:
    """Estimate time signature from beat emphasis patterns."""
    import numpy as np

    try:
        import librosa
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    except Exception as e:
        return {"time_signature": "4/4", "confidence": 0, "error": str(e)}

    if len(beats) < 8:
        return {"time_signature": "4/4", "confidence": 0.3, "note": "too few beats detected"}

    # Get onset strengths at beat positions
    beat_strengths = onset_env[beats[beats < len(onset_env)]]
    if len(beat_strengths) < 4:
        return {"time_signature": "4/4", "confidence": 0.3}

    # Test groupings of 3 and 4
    # For 4/4: every 4th beat should be strongest
    # For 3/4: every 3rd beat should be strongest
    scores = {}
    for grouping in [3, 4]:
        if len(beat_strengths) < grouping * 2:
            continue
        # Trim to even multiple
        trim_len = (len(beat_strengths) // grouping) * grouping
        grouped = beat_strengths[:trim_len].reshape(-1, grouping)
        # Check if first beat of each group is stronger
        first_beat_strength = np.mean(grouped[:, 0])
        other_mean = np.mean(grouped[:, 1:])
        scores[grouping] = first_beat_strength / (other_mean + 1e-10)

    if not scores:
        return {"time_signature": "4/4", "confidence": 0.3}

    best_grouping = max(scores, key=scores.get)
    confidence = min(1.0, scores[best_grouping] / 2.0)

    return {
        "time_signature": f"{best_grouping}/4",
        "confidence": round(float(confidence), 4),
    }


def extract_sections(y, sr) -> list:
    """Extract section boundaries using structural segmentation."""
    import numpy as np

    try:
        import librosa

        # Compute a self-similarity matrix from MFCCs
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        # Use recurrence matrix for structure
        rec = librosa.segment.recurrence_matrix(
            mfcc, mode="affinity", sym=True
        )
        # Agglomerative clustering for section boundaries
        bound_frames = librosa.segment.agglomerative(mfcc, k=None)
        bound_times = librosa.frames_to_time(bound_frames, sr=sr)

        # Filter out sections shorter than 5 seconds
        filtered = [0.0]
        for t in bound_times:
            if t - filtered[-1] >= 5.0:
                filtered.append(round(float(t), 2))

        sections = []
        for i in range(len(filtered)):
            start = filtered[i]
            end = filtered[i + 1] if i + 1 < len(filtered) else round(float(len(y) / sr), 2)
            sections.append({
                "start": start,
                "end": end,
                "duration": round(end - start, 2),
            })

        return sections

    except Exception as e:
        duration = float(len(y) / sr)
        return [{
            "start": 0.0,
            "end": round(duration, 2),
            "duration": round(duration, 2),
            "error": str(e),
        }]


def extract_energy_curve(y, sr, n_points: int = 20) -> list:
    """Extract RMS energy curve sampled at n_points across the track."""
    import numpy as np

    try:
        import librosa
        rms = librosa.feature.rms(y=y)[0]
        # Resample to n_points
        indices = np.linspace(0, len(rms) - 1, n_points, dtype=int)
        sampled = rms[indices]
        # Normalize to 0-1
        max_val = sampled.max()
        if max_val > 0:
            sampled = sampled / max_val
        duration = float(len(y) / sr)
        times = np.linspace(0, duration, n_points)
        return [
            {"time": round(float(t), 2), "energy": round(float(e), 4)}
            for t, e in zip(times, sampled)
        ]
    except Exception:
        return []


def extract_technical(audio_path: str) -> dict:
    """Run full technical extraction with librosa (+ madmom fallback for downbeats)."""
    import numpy as np

    try:
        import librosa
    except ImportError:
        raise RuntimeError(
            "librosa is required. Install with: pip install librosa"
        )

    print("[Technical] Loading audio with librosa...")
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    duration = float(len(y) / sr)
    print(f"[Technical] Loaded: {duration:.1f}s at {sr}Hz")

    technical = {
        "duration_seconds": round(duration, 2),
        "sample_rate": sr,
    }

    # BPM detection
    print("[Technical] Detecting tempo...")
    try:
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        # Handle both scalar and array returns from different librosa versions
        bpm = float(tempo) if not hasattr(tempo, '__len__') else float(tempo[0])
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        technical["bpm"] = round(bpm, 2)
        technical["beat_count"] = len(beat_times)
        technical["beat_positions"] = [round(float(t), 3) for t in beat_times[:50]]  # first 50
        # Confidence: std of inter-beat intervals (lower = more confident)
        if len(beat_times) > 1:
            ibis = np.diff(beat_times)
            ibi_std = float(np.std(ibis))
            ibi_mean = float(np.mean(ibis))
            technical["tempo_confidence"] = round(1.0 - min(1.0, ibi_std / (ibi_mean + 1e-10)), 4)
        print(f"[Technical] BPM: {technical['bpm']} (confidence: {technical.get('tempo_confidence', 'N/A')})")
    except Exception as e:
        technical["bpm"] = None
        technical["bpm_error"] = str(e)
        print(f"[Technical] BPM detection failed: {e}")

    # Key detection
    print("[Technical] Detecting key...")
    key_info = detect_key(y, sr)
    technical["key"] = key_info
    print(f"[Technical] Key: {key_info['key']} {key_info['mode']} (confidence: {key_info.get('confidence', 'N/A')})")

    # Time signature
    print("[Technical] Estimating time signature...")
    time_sig = estimate_time_signature(y, sr)
    technical["time_signature"] = time_sig
    print(f"[Technical] Time sig: {time_sig['time_signature']}")

    # Spectral centroid (brightness)
    print("[Technical] Computing spectral features...")
    try:
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        technical["spectral_centroid_mean"] = round(float(np.mean(centroid)), 2)
        technical["spectral_centroid_std"] = round(float(np.std(centroid)), 2)
        technical["brightness"] = "bright" if technical["spectral_centroid_mean"] > 3000 else "warm" if technical["spectral_centroid_mean"] > 1500 else "dark"
    except Exception as e:
        technical["spectral_centroid_error"] = str(e)

    # Energy curve
    print("[Technical] Extracting energy arc...")
    technical["energy_curve"] = extract_energy_curve(y, sr, n_points=20)

    # Section segmentation
    print("[Technical] Segmenting structure...")
    technical["sections"] = extract_sections(y, sr)
    print(f"[Technical] Found {len(technical['sections'])} sections")

    # Madmom downbeat tracking (optional, better than librosa for this)
    try:
        import madmom
        print("[Technical] Running madmom downbeat detection...")
        proc = madmom.features.downbeats.DBNDownBeatTrackingProcessor(
            beats_per_bar=[3, 4], fps=100
        )
        act = madmom.features.downbeats.RNNDownBeatProcessor()(audio_path)
        downbeats_raw = proc(act)
        downbeat_times = [
            round(float(row[0]), 3)
            for row in downbeats_raw
            if int(row[1]) == 1
        ]
        technical["downbeats_madmom"] = downbeat_times[:50]
        technical["madmom_available"] = True
        print(f"[Technical] Madmom found {len(downbeat_times)} downbeats")
    except ImportError:
        technical["madmom_available"] = False
        print("[Technical] madmom not installed — skipping downbeat tracking (pip install madmom)")
    except Exception as e:
        technical["madmom_available"] = True
        technical["madmom_error"] = str(e)
        print(f"[Technical] madmom downbeat detection failed: {e}")

    return technical


def run_subjective_analysis(audio_path: str, technical: dict) -> dict:
    """Send audio + technical data to Gemini 2.5 Pro for subjective analysis."""
    print("[Subjective] Sending to Gemini 2.5 Pro via OpenRouter...")
    try:
        result = analyze_audio(
            audio_path=audio_path,
            prompt=SUBJECTIVE_PROMPT,
            technical_data=technical,
        )
        print("[Subjective] Analysis complete")
        return result
    except Exception as e:
        print(f"[Subjective] Gemini analysis failed: {e}")
        return {"error": str(e), "note": "Subjective analysis unavailable — technical-only blueprint"}


def build_blueprint(
    source: str,
    title: str,
    audio_path: str,
    technical: dict,
    subjective: dict,
    intent: Optional[str] = None,
) -> dict:
    """Assemble the complete blueprint from technical + subjective data."""
    blueprint = {
        "meta": {
            "version": "1.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "title": title,
            "audio_file": str(audio_path),
            "intent": intent,
        },
        "technical": technical,
        "subjective": subjective,
    }

    # Pull steal_list and avoid_list to top level for easy access
    blueprint["steal_list"] = subjective.get("steal_list", [])
    blueprint["avoid_list"] = subjective.get("avoid_list", [])

    # Composite summary fields
    bpm = technical.get("bpm")
    key_info = technical.get("key", {})
    key_str = f"{key_info.get('key', '?')} {key_info.get('mode', '?')}"
    genre_tags = subjective.get("genre_tags", [])
    mood_tags = subjective.get("mood_tags", [])

    blueprint["summary"] = {
        "bpm": bpm,
        "key": key_str,
        "genres": genre_tags,
        "moods": mood_tags,
        "brightness": technical.get("brightness", "unknown"),
        "duration": technical.get("duration_seconds"),
        "sections_count": len(technical.get("sections", [])),
        "suno_style_field": subjective.get("suno_style_field", ""),
        "suno_negative_tags": subjective.get("suno_negative_tags", ""),
    }

    return blueprint


def generate_suno_output(blueprint: dict) -> Optional[str]:
    """Generate Suno package markdown from blueprint."""
    if _has_suno_packager:
        try:
            style_field = generate_style_field(blueprint)
            sections = blueprint.get("technical", {}).get("sections", [])
            tag_skeleton = generate_tag_skeleton(sections) if sections else ""
            return format_package(style_field=style_field, tag_skeleton=tag_skeleton)
        except Exception as e:
            print(f"[Suno] Packager failed, using fallback: {e}")

    # Fallback: generate a basic package inline
    summary = blueprint.get("summary", {})
    subjective = blueprint.get("subjective", {})

    lines = [
        "# Suno Package",
        "",
        f"## Style Field",
        f"```",
        f"{summary.get('suno_style_field', 'N/A')}",
        f"```",
        "",
        f"## Negative Tags",
        f"```",
        f"{summary.get('suno_negative_tags', 'N/A')}",
        f"```",
        "",
        f"## Technical Reference",
        f"- **BPM:** {summary.get('bpm', 'N/A')}",
        f"- **Key:** {summary.get('key', 'N/A')}",
        f"- **Brightness:** {summary.get('brightness', 'N/A')}",
        "",
        f"## Instrumentation",
    ]
    for inst in subjective.get("instrumentation", []):
        lines.append(f"- {inst}")
    lines.extend([
        "",
        "## Production Notes",
        subjective.get("production_style", "N/A"),
        "",
        "## Energy Arc",
        subjective.get("energy_arc", "N/A"),
    ])
    return "\n".join(lines)


def generate_voice_output(blueprint: dict) -> Optional[str]:
    """Generate voice recommendations from blueprint."""
    if _has_voice_engine:
        try:
            subjective = blueprint.get("subjective", {})
            summary = blueprint.get("summary", {})
            genre = (subjective.get("genre_tags", summary.get("genres", ["unknown"])) or ["unknown"])[0]
            mood = (subjective.get("mood_tags", summary.get("moods", ["neutral"])) or ["neutral"])[0]
            bpm = blueprint.get("technical", {}).get("bpm") or summary.get("bpm") or 120
            recs = recommend_voices(genre=genre, mood=mood, tempo=int(bpm))
            lines = ["## Voice Recommendations", ""]
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
        except Exception as e:
            print(f"[Voice] Engine failed, using fallback: {e}")

    # Fallback: basic recommendations from subjective data
    subjective = blueprint.get("subjective", {})
    vocal_style = subjective.get("vocal_style", "No vocal analysis available")
    return f"## Voice Recommendations\n\n**Detected Vocal Style:** {vocal_style}\n\n(Install voice_engine module for detailed ElevenLabs recommendations)"


def print_summary(blueprint: dict):
    """Print a console-friendly summary of the blueprint."""
    summary = blueprint.get("summary", {})
    meta = blueprint.get("meta", {})
    subjective = blueprint.get("subjective", {})

    print("\n" + "=" * 60)
    print("BLUEPRINT EXTRACT COMPLETE")
    print("=" * 60)
    print(f"  Title:      {meta.get('title', 'Unknown')}")
    print(f"  Source:     {meta.get('source', 'Unknown')}")
    print(f"  Duration:   {summary.get('duration', '?')}s")
    print(f"  BPM:        {summary.get('bpm', '?')}")
    print(f"  Key:        {summary.get('key', '?')}")
    print(f"  Brightness: {summary.get('brightness', '?')}")
    print(f"  Genres:     {', '.join(summary.get('genres', []))}")
    print(f"  Moods:      {', '.join(summary.get('moods', []))}")
    print(f"  Sections:   {summary.get('sections_count', '?')}")
    print()

    steal_list = blueprint.get("steal_list", [])
    if steal_list:
        print("  STEAL LIST:")
        for item in steal_list:
            print(f"    + {item}")

    avoid_list = blueprint.get("avoid_list", [])
    if avoid_list:
        print("  AVOID LIST:")
        for item in avoid_list:
            print(f"    - {item}")

    suno_style = summary.get("suno_style_field", "")
    if suno_style:
        print(f"\n  SUNO STYLE FIELD:")
        print(f"    {suno_style}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Style Genome Analyzer — Mode 1: Blueprint Extract",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract.py --url "https://youtube.com/watch?v=..."
  python extract.py --file track.mp3 --save --intent "gym motivation"
  python extract.py --url "https://youtu.be/..." --output ./my_blueprints/ --save
        """,
    )
    parser.add_argument("--url", type=str, help="YouTube URL to analyze")
    parser.add_argument("--file", type=str, help="Path to local audio file (mp3, wav, flac, etc.)")
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output directory (default: ./data/blueprints/)",
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save blueprint to the shared library for crossbreeding",
    )
    parser.add_argument(
        "--intent", type=str, default=None,
        help="What you plan to use this analysis for (e.g., 'gym track', 'lo-fi study')",
    )

    args = parser.parse_args()

    if not args.url and not args.file:
        parser.error("Either --url or --file is required")

    if args.url and args.file:
        parser.error("Provide either --url or --file, not both")

    output_dir = Path(args.output) if args.output else BLUEPRINTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = None
    audio_path = None
    title = "unknown_track"
    source = ""

    try:
        # Step 1: Get audio file
        if args.url:
            source = args.url
            temp_dir = tempfile.mkdtemp(prefix="sga_")
            audio_path, title = download_youtube_audio(args.url, temp_dir)
        else:
            audio_path = os.path.abspath(args.file)
            if not os.path.exists(audio_path):
                print(f"[Error] File not found: {audio_path}")
                sys.exit(1)
            source = audio_path
            title = Path(audio_path).stem

        # Step 2-3: Technical extraction
        print(f"\n[Extract] Analyzing: {title}")
        technical = extract_technical(audio_path)

        # Step 4: Subjective analysis via Gemini
        subjective = run_subjective_analysis(audio_path, technical)

        # Step 5: Build blueprint
        blueprint = build_blueprint(
            source=source,
            title=title,
            audio_path=audio_path,
            technical=technical,
            subjective=subjective,
            intent=args.intent,
        )

        # Step 6: Generate Suno package
        suno_md = generate_suno_output(blueprint)
        blueprint["suno_package"] = suno_md

        # Step 7: Generate voice recommendations
        voice_md = generate_voice_output(blueprint)
        blueprint["voice_recommendations"] = voice_md

        # Step 8: Save outputs
        safe_title = re.sub(r'[^\w\s\-]', '', title)[:60].strip()
        safe_title = re.sub(r'\s+', '_', safe_title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        blueprint_filename = f"{safe_title}_{timestamp}.json"
        blueprint_path = output_dir / blueprint_filename
        with open(blueprint_path, "w", encoding="utf-8") as f:
            # Remove non-serializable fields before saving
            save_data = {k: v for k, v in blueprint.items()}
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        print(f"\n[Output] Blueprint saved: {blueprint_path}")

        # Save Suno package markdown
        if suno_md:
            suno_path = output_dir / f"{safe_title}_{timestamp}_suno.md"
            with open(suno_path, "w", encoding="utf-8") as f:
                f.write(suno_md)
            print(f"[Output] Suno package: {suno_path}")

        # Save voice recommendations
        if voice_md:
            voice_path = output_dir / f"{safe_title}_{timestamp}_voice.md"
            with open(voice_path, "w", encoding="utf-8") as f:
                f.write(voice_md)
            print(f"[Output] Voice recs: {voice_path}")

        # If --save, copy to shared library
        if args.save:
            shared_path = BLUEPRINTS_DIR / blueprint_filename
            if str(shared_path.resolve()) != str(blueprint_path.resolve()):
                BLUEPRINTS_DIR.mkdir(parents=True, exist_ok=True)
                with open(shared_path, "w", encoding="utf-8") as f:
                    json.dump(save_data, f, indent=2, ensure_ascii=False)
                print(f"[Output] Saved to shared library: {shared_path}")

        # Print summary
        print_summary(blueprint)

    finally:
        # Clean up temp download directory
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
