# Reference Tracks

Place professionally mastered commercial tracks here. These are the sonic targets your tracks will be matched to.

## Required Files (by genre key in reference_map.json)

| Genre Key | Filename | Suggested Reference |
|-----------|----------|---------------------|
| `industrial-metal` | `industrial_metal.wav` | Rammstein "Mein Herz Brennt" or "Links 2-3-4" |
| `doom` / `doom-sludge` | `doom_sludge.wav` | Electric Wizard "Dopethrone" or Conan "Horseback Battle Hammer" |
| `edm-industrial` | `edm_industrial.wav` | Angerfist "Incoming" or Perturbator "Sentinel" |
| `folk-metal-shanty` | `folk_metal_shanty.wav` | Wind Rose "Diggy Diggy Hole" or Alestorm "Drink" |
| `dark-cinematic` | `dark_cinematic.wav` | Two Steps from Hell "Victory" or Thomas Bergersen "Starchild" |
| `tribal-metal` | `tribal_metal.wav` | Sepultura "Roots Bloody Roots" or Gojira "L'Enfant Sauvage" |

## Rules for Good Reference Tracks

1. **Professionally mastered commercial release.** Not a demo, not a YouTube rip with weird EQ, not a Bandcamp upload of questionable quality.
2. **Same general energy as your target.** A 145 BPM industrial banger reference will not work for a 65 BPM shanty — the dynamics are completely different.
3. **Clean WAV format.** Convert MP3 → WAV if needed (lossy source introduces artifacts). Ideally 24-bit, 44.1 or 48 kHz.
4. **Full track, not a snippet.** Matchering needs at least 30 seconds to analyze properly.
5. **Mixed in the range you want to hit.** If you want -8 LUFS, use a reference at -8 LUFS. Don't use a -14 LUFS streaming master as reference for a club banger.

## Legal Note

You are not distributing these reference tracks, you are using them as sonic targets for your own music. This is fair use for personal production purposes. Do NOT commit these files to any public repo or share them.

## Where to Get References

- **Buy FLAC/WAV from Bandcamp** (best source — artist gets paid, you get a proper file)
- **Rip from your own CDs** (cleanest possible source)
- **Qobuz/Tidal hi-res downloads** (if you have a subscription)
- **Never use YouTube rips** — the compression artifacts will confuse Matchering

## Testing a New Reference

Before using a new reference in production, test it:

```bash
python scripts/master.py --input test_track.wav --reference references/new_reference.wav --output ./test_output/
```

Check the master report — if LUFS is on target and the A/B sounds good, the reference is usable.
