"""
Standalone LUFS measurement utility.

Usage:
    python lufs_check.py --input track.wav
    python lufs_check.py --input track.wav --target -8 --fix
"""

import argparse
import json
import sys
from pathlib import Path


def measure(path: Path) -> dict:
    """Measure loudness characteristics of an audio file."""
    import soundfile as sf
    import pyloudnorm as pyln
    import numpy as np

    data, rate = sf.read(str(path))
    meter = pyln.Meter(rate)
    integrated = meter.integrated_loudness(data)

    peak_linear = float(np.max(np.abs(data)))
    true_peak_db = 20 * np.log10(max(peak_linear, 1e-10))

    try:
        lra = meter.loudness_range(data)
    except Exception:
        lra = None

    return {
        "file": str(path),
        "integrated_lufs": round(float(integrated), 2),
        "true_peak_db": round(float(true_peak_db), 2),
        "loudness_range_lu": round(float(lra), 2) if lra is not None else None,
        "sample_rate": int(rate),
        "duration_seconds": round(len(data) / rate, 2),
        "channels": 1 if data.ndim == 1 else data.shape[1],
    }


def fix_lufs(path: Path, target_lufs: float, true_peak_limit: float = -1.0, output: Path | None = None):
    """Apply gain to reach target LUFS. Writes in place unless output is specified."""
    import soundfile as sf
    import pyloudnorm as pyln
    import numpy as np

    data, rate = sf.read(str(path))
    meter = pyln.Meter(rate)
    current_lufs = meter.integrated_loudness(data)

    gain_db = target_lufs - current_lufs
    gain_linear = 10 ** (gain_db / 20)
    adjusted = data * gain_linear

    peak = float(np.max(np.abs(adjusted)))
    peak_db = 20 * np.log10(max(peak, 1e-10))

    if peak_db > true_peak_limit:
        ceiling_linear = 10 ** (true_peak_limit / 20)
        adjusted = adjusted * (ceiling_linear / peak)
        print(f"  peak limited from {peak_db:.2f} to {true_peak_limit:.1f} dBTP")

    target_path = output if output else path
    sf.write(str(target_path), adjusted, rate, subtype="PCM_24")
    print(f"  applied {gain_db:+.2f} dB, written to {target_path}")
    return gain_db


def main():
    parser = argparse.ArgumentParser(description="Measure or correct LUFS of audio files")
    parser.add_argument("--input", required=True, help="Audio file to analyze")
    parser.add_argument("--target", type=float, help="Target LUFS (triggers fix mode)")
    parser.add_argument("--true-peak", type=float, default=-1.0, help="True peak limit (default -1.0)")
    parser.add_argument("--fix", action="store_true", help="Apply gain to hit target")
    parser.add_argument("--output", help="Output path (default: overwrite input)")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    measurements = measure(path)

    if args.json:
        print(json.dumps(measurements, indent=2))
    else:
        print(f"\nFile: {measurements['file']}")
        print(f"  Integrated LUFS: {measurements['integrated_lufs']}")
        print(f"  True Peak:       {measurements['true_peak_db']} dBTP")
        if measurements['loudness_range_lu']:
            print(f"  LRA:             {measurements['loudness_range_lu']} LU")
        print(f"  Duration:        {measurements['duration_seconds']}s")
        print(f"  Sample rate:     {measurements['sample_rate']} Hz")
        print(f"  Channels:        {measurements['channels']}")

    if args.fix and args.target is not None:
        output = Path(args.output) if args.output else None
        fix_lufs(path, args.target, args.true_peak, output)
        # Re-measure
        final = measure(output if output else path)
        print(f"\n  After correction: {final['integrated_lufs']} LUFS, "
              f"peak {final['true_peak_db']} dBTP")


if __name__ == "__main__":
    main()
