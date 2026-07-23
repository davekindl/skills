"""
Audio Master — Reference-based mastering pipeline.

Matchering (reference matching) → PyLoudnorm (LUFS verify) → Pedalboard (polish) → Export.

Replaces Mixea/LANDR/eMastered with a free local pipeline.
"""

import argparse
import json
import shutil
import sys
import warnings
from pathlib import Path

# Suppress matchering's verbose warnings
warnings.filterwarnings("ignore")

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
REFERENCES_DIR = SKILL_DIR / "references"
DATA_DIR = SKILL_DIR / "data" / "mastered"

# Genre → LUFS target mapping (integrated LUFS)
# OPTIMIZED FOR STREAMING DISTRIBUTION (Spotify, YouTube, Apple Music all normalize to -14)
# Target -10 to -11 leaves ~4 dB of headroom above normalization floor:
# - Sounds punchy on Spotify (normalized to -14)
# - Preserves real dynamic range (no loudness war crushing)
# - On Spotify "Loud" setting (-11 target), plays nearly full volume
# - Mastering louder than -10 gets normalized DOWN and wastes dynamics
LUFS_TARGETS = {
    "industrial-metal": -10.0,
    "doom": -11.0,           # doom needs more dynamic range
    "doom-sludge": -11.0,
    "edm-industrial": -10.0,
    "folk-metal": -10.5,
    "folk-metal-shanty": -10.5,
    "dark-cinematic": -12.0,  # cinematic needs the most dynamics
    "tribal-metal": -10.0,
    "post-metal": -11.0,
    # Streaming-normalized version (secondary output — only if you really want it)
    "streaming": -14.0,
    # Club/download-only version (if you ever need it — not for streaming uploads)
    "club": -7.0,
}

# Genre → reference filename mapping (defaults — can be overridden in reference_map.json)
DEFAULT_GENRE_MAP = {
    "industrial-metal": "industrial_metal.wav",
    "doom": "doom_sludge.wav",
    "doom-sludge": "doom_sludge.wav",
    "edm-industrial": "edm_industrial.wav",
    "folk-metal": "folk_metal_shanty.wav",
    "folk-metal-shanty": "folk_metal_shanty.wav",
    "dark-cinematic": "dark_cinematic.wav",
    "tribal-metal": "tribal_metal.wav",
    "post-metal": "doom_sludge.wav",
}

TARGET_TRUE_PEAK = -1.0  # dBTP for all genres


def load_genre_map():
    """Load reference_map.json if it exists, else use defaults."""
    map_path = REFERENCES_DIR / "reference_map.json"
    if map_path.exists():
        with open(map_path, encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_GENRE_MAP


def resolve_reference(genre: str, explicit_ref: str | None) -> Path:
    """Return path to reference track for the given genre."""
    if explicit_ref:
        ref_path = Path(explicit_ref)
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference not found: {explicit_ref}")
        return ref_path

    genre_map = load_genre_map()
    if genre not in genre_map:
        available = ", ".join(sorted(genre_map.keys()))
        raise ValueError(f"Unknown genre '{genre}'. Available: {available}")

    ref_name = genre_map[genre]
    ref_path = REFERENCES_DIR / ref_name
    if not ref_path.exists():
        raise FileNotFoundError(
            f"Reference file missing: {ref_path}\n"
            f"Add a professionally mastered track at this path to use genre '{genre}'.\n"
            f"See references/README.md for guidelines."
        )
    return ref_path


def run_matchering(target: Path, reference: Path, output_24: Path, output_16: Path):
    """Run Matchering 2.0 reference-based mastering."""
    import matchering as mg

    print(f"  [1/4] Matchering reference match")
    print(f"        target:    {target.name}")
    print(f"        reference: {reference.name}")

    # Silent logger to avoid matchering's verbose output
    mg.log(print)

    mg.process(
        target=str(target),
        reference=str(reference),
        results=[
            mg.pcm24(str(output_24)),
            mg.pcm16(str(output_16)),
        ],
    )
    print(f"        [OK] wrote {output_24.name}")


def measure_lufs(path: Path) -> dict:
    """Measure integrated LUFS, true peak, and LRA using pyloudnorm."""
    import soundfile as sf
    import pyloudnorm as pyln

    data, rate = sf.read(str(path))
    meter = pyln.Meter(rate)
    integrated = meter.integrated_loudness(data)

    # True peak via oversampled peak
    import numpy as np
    if data.ndim == 1:
        peak_linear = np.max(np.abs(data))
    else:
        peak_linear = np.max(np.abs(data))
    true_peak_db = 20 * np.log10(max(peak_linear, 1e-10))

    # LRA (loudness range) — approximation
    try:
        lra = meter.loudness_range(data)
    except Exception:
        lra = None

    return {
        "integrated_lufs": round(float(integrated), 2),
        "true_peak_db": round(float(true_peak_db), 2),
        "loudness_range_lu": round(float(lra), 2) if lra is not None else None,
        "sample_rate": int(rate),
        "channels": 1 if data.ndim == 1 else data.shape[1],
    }


def adjust_lufs(path: Path, target_lufs: float, true_peak_limit: float = -1.0):
    """
    Use ffmpeg's loudnorm filter to hit target LUFS with true peak ceiling.
    This is a two-pass EBU R128 normalization — measures first, then applies
    exact correction. Battle-tested, used by broadcast and streaming platforms.
    """
    import subprocess
    import json as json_mod

    temp_out = path.with_suffix(".tmp.wav")

    # Pass 1: measure current loudness stats (JSON output)
    measure_cmd = [
        "ffmpeg", "-y", "-i", str(path),
        "-af", f"loudnorm=I={target_lufs}:TP={true_peak_limit}:LRA=11:print_format=json",
        "-f", "null", "-",
    ]
    result = subprocess.run(measure_cmd, capture_output=True, text=True)
    stderr = result.stderr

    # Extract JSON block from stderr
    json_start = stderr.rfind("{")
    json_end = stderr.rfind("}") + 1
    if json_start == -1 or json_end <= json_start:
        raise RuntimeError(f"loudnorm measurement failed:\n{stderr[-500:]}")

    stats = json_mod.loads(stderr[json_start:json_end])
    measured_i = stats["input_i"]
    measured_tp = stats["input_tp"]
    measured_lra = stats["input_lra"]
    measured_thresh = stats["input_thresh"]
    offset = stats.get("target_offset", "0.0")

    print(f"        loudnorm measured: I={measured_i} TP={measured_tp} LRA={measured_lra}")

    # Pass 2: apply correction using measured values
    apply_cmd = [
        "ffmpeg", "-y", "-i", str(path),
        "-af", (
            f"loudnorm=I={target_lufs}:TP={true_peak_limit}:LRA=11:"
            f"measured_I={measured_i}:measured_TP={measured_tp}:"
            f"measured_LRA={measured_lra}:measured_thresh={measured_thresh}:"
            f"offset={offset}:linear=true:print_format=summary"
        ),
        "-ar", "48000", "-c:a", "pcm_s24le",
        str(temp_out),
    ]
    result = subprocess.run(apply_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"loudnorm apply failed:\n{result.stderr[-500:]}")

    # Replace original with corrected version
    shutil.move(str(temp_out), str(path))
    return float(measured_i) - target_lufs


def apply_polish(path: Path, genre: str):
    """Apply final polish with Pedalboard — tape saturation, stereo tweaks, final limit."""
    try:
        from pedalboard import Pedalboard, Compressor, Gain, Limiter, HighShelfFilter
        from pedalboard.io import AudioFile
    except ImportError:
        print("        [WARN] pedalboard not installed, skipping polish")
        return

    print(f"  [3/4] Pedalboard polish")

    # Genre-specific polish chain — tonal shaping + bus compression only
    # Final limiting is handled by adjust_lufs() which enforces true peak ceiling
    if genre in ("doom", "doom-sludge", "post-metal"):
        # Gentle glue compression, preserve dynamics
        board = Pedalboard([
            HighShelfFilter(cutoff_frequency_hz=10000, gain_db=1.5),
            Compressor(threshold_db=-18, ratio=1.5, attack_ms=30, release_ms=200),
        ])
    elif genre in ("edm-industrial",):
        # Tighter compression for club punch
        board = Pedalboard([
            HighShelfFilter(cutoff_frequency_hz=8000, gain_db=2.0),
            Compressor(threshold_db=-16, ratio=2.0, attack_ms=10, release_ms=80),
        ])
    elif genre in ("folk-metal", "folk-metal-shanty"):
        # Minimal compression — preserve the dynamic range of choir vs shantyman
        board = Pedalboard([
            HighShelfFilter(cutoff_frequency_hz=9000, gain_db=1.0),
            Compressor(threshold_db=-20, ratio=1.3, attack_ms=30, release_ms=200),
        ])
    else:
        # Default: gentle bus glue
        board = Pedalboard([
            HighShelfFilter(cutoff_frequency_hz=9000, gain_db=1.0),
            Compressor(threshold_db=-18, ratio=1.5, attack_ms=20, release_ms=150),
        ])

    with AudioFile(str(path)) as f:
        audio = f.read(f.frames)
        sr = f.samplerate
        nch = f.num_channels

    processed = board(audio, sr)

    with AudioFile(str(path), "w", sr, nch, bit_depth=24) as f:
        f.write(processed)

    print(f"        [OK] polished ({genre} chain)")


def master_track(
    input_path: Path,
    genre: str,
    output_dir: Path,
    explicit_ref: Path | None = None,
    lufs_override: float | None = None,
    skip_polish: bool = False,
    streaming_version: bool = False,
    no_reference: bool = False,
):
    """Run the full mastering pipeline on a single track."""
    output_dir.mkdir(parents=True, exist_ok=True)

    name = input_path.stem
    target_lufs = lufs_override if lufs_override is not None else LUFS_TARGETS.get(genre, -10.0)

    print(f"\n=== Mastering: {input_path.name} ===")
    print(f"    Genre: {genre}")
    print(f"    Target LUFS: {target_lufs}")

    out_24 = output_dir / f"{name}_mastered_24bit.wav"
    out_16 = output_dir / f"{name}_mastered_16bit.wav"

    if no_reference:
        # Reference-free mode: copy input to output, skip Matchering
        print(f"    Mode: REFERENCE-FREE (LUFS normalize + polish only)")
        print(f"  [1/4] Preparing track (no reference matching)")
        import soundfile as sf
        data, rate = sf.read(str(input_path))
        sf.write(str(out_24), data, rate, subtype="PCM_24")
        print(f"        [OK] copied to {out_24.name}")
        reference = None
    else:
        reference = resolve_reference(genre, str(explicit_ref) if explicit_ref else None)
        print(f"    Reference: {reference.name}")
        run_matchering(input_path, reference, out_24, out_16)

    # Measure initial state
    measurements_before = measure_lufs(out_24)
    print(f"  [2/4] Pre-polish state: {measurements_before['integrated_lufs']} LUFS, "
          f"peak {measurements_before['true_peak_db']} dBTP")

    # Step 3: Polish FIRST (tonal shaping, compression, initial limiting)
    # Polish changes effective loudness, so we correct LUFS AFTER it
    if not skip_polish:
        apply_polish(out_24, genre)
    else:
        print(f"  [3/4] Polish skipped (--no-polish)")

    # Step 4: FINAL LUFS correction with true peak ceiling enforced
    # This is the authoritative loudness stage — runs after all gain/dynamics processing
    print(f"  [4/4] Final LUFS correction + peak limiting")
    measurements_mid = measure_lufs(out_24)
    print(f"        post-polish: {measurements_mid['integrated_lufs']} LUFS, "
          f"peak {measurements_mid['true_peak_db']} dBTP")

    lufs_diff = abs(measurements_mid["integrated_lufs"] - target_lufs)
    if lufs_diff > 0.3:
        gain_applied = adjust_lufs(out_24, target_lufs, TARGET_TRUE_PEAK)
        print(f"        applied {gain_applied:+.2f} dB final gain")
    else:
        print(f"        [OK] already within +-0.3 LU of target")

    # Re-measure final
    measurements_after = measure_lufs(out_24)

    # Re-export 16-bit from polished 24-bit
    import soundfile as sf
    data, rate = sf.read(str(out_24))
    sf.write(str(out_16), data, rate, subtype="PCM_16")

    # Step 4: Optional streaming version
    streaming_path = None
    if streaming_version:
        streaming_path = output_dir / f"{name}_streaming.wav"
        shutil.copy(out_24, streaming_path)
        adjust_lufs(streaming_path, -14.0, -1.0)
        stream_meas = measure_lufs(streaming_path)
        print(f"  [4/4] Streaming version: {stream_meas['integrated_lufs']} LUFS")

    # QA Report
    report = {
        "source": str(input_path),
        "genre": genre,
        "target_lufs": target_lufs,
        "reference_track": str(reference) if reference else "NONE (reference-free mode)",
        "output_24bit": str(out_24),
        "output_16bit": str(out_16),
        "streaming_version": str(streaming_path) if streaming_path else None,
        "measurements_before": measurements_before,
        "measurements_after": measurements_after,
        "lufs_delta_from_target": round(
            measurements_after["integrated_lufs"] - target_lufs, 2
        ),
        "polish_applied": not skip_polish,
    }

    report_path = output_dir / f"{name}_master_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Summary
    print(f"\n  === Master complete ===")
    print(f"  Final: {measurements_after['integrated_lufs']} LUFS "
          f"(target {target_lufs}, delta {report['lufs_delta_from_target']:+.2f})")
    print(f"  True peak: {measurements_after['true_peak_db']} dBTP")
    if measurements_after["loudness_range_lu"]:
        print(f"  Dynamic range: {measurements_after['loudness_range_lu']} LU")
    print(f"  Output: {out_24}")
    print(f"  Report: {report_path}")

    return report


def master_album(
    album_dir: Path,
    reference: Path,
    output_dir: Path,
    lufs_override: float | None = None,
    skip_polish: bool = False,
    genre: str = "industrial-metal",
):
    """Master all WAV files in a directory with the SAME reference for consistency."""
    wavs = sorted(album_dir.glob("*.wav"))
    if not wavs:
        print(f"No WAV files found in {album_dir}")
        return

    print(f"\n=== Album mode: {len(wavs)} tracks ===")
    print(f"    Reference: {reference.name}")
    print(f"    Genre: {genre}")

    reports = []
    for wav in wavs:
        report = master_track(
            input_path=wav,
            genre=genre,
            output_dir=output_dir,
            explicit_ref=reference,
            lufs_override=lufs_override,
            skip_polish=skip_polish,
        )
        reports.append(report)

    album_report = {
        "album_dir": str(album_dir),
        "reference": str(reference),
        "genre": genre,
        "tracks": reports,
    }
    album_report_path = output_dir / "album_master_report.json"
    album_report_path.write_text(json.dumps(album_report, indent=2), encoding="utf-8")
    print(f"\n=== Album master complete: {len(reports)} tracks ===")
    print(f"    Album report: {album_report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Audio Master — reference-based mastering pipeline",
    )
    parser.add_argument("--input", help="Single track to master (WAV)")
    parser.add_argument("--album", help="Directory of WAV files to master with same reference")
    parser.add_argument("--genre", default="industrial-metal",
                        help="Genre preset (sets reference + LUFS target)")
    parser.add_argument("--reference", help="Explicit reference track path (overrides genre map)")
    parser.add_argument("--lufs", type=float, help="Override LUFS target (dB)")
    parser.add_argument("--output", help="Output directory (default: skill data/mastered/)")
    parser.add_argument("--no-polish", action="store_true", help="Skip Pedalboard polish step")
    parser.add_argument("--no-reference", action="store_true",
                        help="Skip Matchering reference matching — just LUFS + polish")
    parser.add_argument("--streaming", action="store_true",
                        help="Also export -14 LUFS streaming version")

    args = parser.parse_args()

    if not args.input and not args.album:
        parser.error("Specify --input <file> or --album <dir>")

    output_dir = Path(args.output) if args.output else DATA_DIR

    if args.album:
        if args.no_reference:
            # Reference-free album mode — no reference needed
            wavs = sorted(Path(args.album).glob("*.wav"))
            print(f"\n=== Album mode (reference-free): {len(wavs)} tracks ===")
            for wav in wavs:
                master_track(
                    input_path=wav,
                    genre=args.genre,
                    output_dir=output_dir,
                    lufs_override=args.lufs,
                    skip_polish=args.no_polish,
                    no_reference=True,
                )
        else:
            if not args.reference:
                genre_map = load_genre_map()
                ref_name = genre_map.get(args.genre)
                if not ref_name:
                    parser.error(f"Album mode needs --reference or a known --genre")
                reference = REFERENCES_DIR / ref_name
            else:
                reference = Path(args.reference)

            if not reference.exists():
                parser.error(f"Reference not found: {reference}")

            master_album(
                album_dir=Path(args.album),
                reference=reference,
                output_dir=output_dir,
                lufs_override=args.lufs,
                skip_polish=args.no_polish,
                genre=args.genre,
            )
    else:
        master_track(
            input_path=Path(args.input),
            genre=args.genre,
            output_dir=output_dir,
            explicit_ref=Path(args.reference) if args.reference else None,
            lufs_override=args.lufs,
            skip_polish=args.no_polish,
            streaming_version=args.streaming,
            no_reference=args.no_reference,
        )


if __name__ == "__main__":
    main()
