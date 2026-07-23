"""
Suno Package Generator -- takes blueprint/genome data and outputs
paste-ready Suno style fields and tag skeletons.
"""

from typing import Optional


# Suno tag mapping: internal section labels -> Suno structure tags
SUNO_TAG_MAP = {
    # Standard sections
    "intro": "[Intro]",
    "verse": "[Verse]",
    "verse1": "[Verse 1]",
    "verse2": "[Verse 2]",
    "verse3": "[Verse 3]",
    "verse4": "[Verse 4]",
    "chorus": "[Chorus]",
    "prechorus": "[Pre-Chorus]",
    "pre-chorus": "[Pre-Chorus]",
    "bridge": "[Bridge]",
    "outro": "[Outro]",
    "hook": "[Hook]",
    "refrain": "[Refrain]",
    # Breakdowns and builds
    "breakdown": "[Breakdown]",
    "buildup": "[Build]",
    "build": "[Build]",
    "drop": "[Drop]",
    # Instrumental / spoken
    "instrumental": "[Instrumental]",
    "solo": "[Instrumental Solo]",
    "guitar_solo": "[Guitar Solo]",
    "interlude": "[Interlude]",
    "spoken": "[Spoken Word]",
    "spoken_word": "[Spoken Word]",
    "rap": "[Rap]",
    "chant": "[Chant]",
    # Structural markers
    "silence": "[Silence]",
    "break": "[Break]",
    "fade_out": "[Fade Out]",
    "fade_in": "[Fade In]",
    "end": "[End]",
}

# Priority order for style field descriptors (most to least important for trimming)
DESCRIPTOR_PRIORITY = [
    "genre",
    "tempo",
    "key",
    "vocals",
    "instruments",
    "mood",
    "production",
    "dynamics",
    "texture",
    "negatives",
]

# Energy level thresholds (RMS dB ranges)
ENERGY_THRESHOLDS = {
    "low": (-40, -24),
    "medium": (-24, -14),
    "high": (-14, -8),
    "maximum": (-8, 0),
}


def _classify_energy(rms_db: float) -> str:
    """Classify an RMS dB value into an energy level."""
    if rms_db <= -24:
        return "Low"
    elif rms_db <= -14:
        return "Medium"
    elif rms_db <= -8:
        return "High"
    else:
        return "Maximum"


def _classify_energy_label(label: str) -> str:
    """Normalize an energy label string."""
    normalized = label.strip().lower()
    mapping = {
        "low": "Low",
        "quiet": "Low",
        "soft": "Low",
        "medium": "Medium",
        "mid": "Medium",
        "moderate": "Medium",
        "high": "High",
        "loud": "High",
        "intense": "High",
        "maximum": "Maximum",
        "max": "Maximum",
        "peak": "Maximum",
        "extreme": "Maximum",
    }
    return mapping.get(normalized, "Medium")


def _build_descriptor_parts(genome: dict) -> dict[str, str]:
    """Extract and format descriptor parts from genome data."""
    parts = {}

    # Genre
    genres = genome.get("genre") or genome.get("genres") or genome.get("style")
    if genres:
        if isinstance(genres, list):
            parts["genre"] = ", ".join(str(g) for g in genres)
        else:
            parts["genre"] = str(genres)

    # Tempo
    tempo = genome.get("tempo") or genome.get("bpm")
    if tempo:
        if isinstance(tempo, (int, float)):
            parts["tempo"] = f"{int(tempo)} BPM"
        else:
            parts["tempo"] = str(tempo)

    # Key
    key = genome.get("key") or genome.get("musical_key")
    if key:
        parts["key"] = f"Key of {key}"

    # Vocals
    vocals = genome.get("vocals") or genome.get("vocal_style") or genome.get("voice")
    if vocals:
        if isinstance(vocals, list):
            parts["vocals"] = ", ".join(str(v) for v in vocals)
        elif isinstance(vocals, dict):
            vocal_parts = []
            for k, v in vocals.items():
                vocal_parts.append(f"{v}" if isinstance(v, str) else f"{k}: {v}")
            parts["vocals"] = ", ".join(vocal_parts)
        else:
            parts["vocals"] = str(vocals)

    # Instruments
    instruments = genome.get("instruments") or genome.get("instrumentation")
    if instruments:
        if isinstance(instruments, list):
            parts["instruments"] = ", ".join(str(i) for i in instruments)
        else:
            parts["instruments"] = str(instruments)

    # Mood
    mood = genome.get("mood") or genome.get("moods") or genome.get("emotion")
    if mood:
        if isinstance(mood, list):
            parts["mood"] = ", ".join(str(m) for m in mood)
        else:
            parts["mood"] = str(mood)

    # Production
    production = genome.get("production") or genome.get("production_style")
    if production:
        if isinstance(production, list):
            parts["production"] = ", ".join(str(p) for p in production)
        else:
            parts["production"] = str(production)

    # Dynamics
    dynamics = genome.get("dynamics") or genome.get("dynamic_range")
    if dynamics:
        parts["dynamics"] = str(dynamics)

    # Texture
    texture = genome.get("texture") or genome.get("sonic_texture")
    if texture:
        parts["texture"] = str(texture)

    # Negatives (what to avoid)
    negatives = genome.get("negatives") or genome.get("negative_tags") or genome.get("avoid")
    if negatives:
        if isinstance(negatives, list):
            parts["negatives"] = "NOT " + ", NOT ".join(str(n) for n in negatives)
        else:
            parts["negatives"] = f"NOT {negatives}"

    return parts


def generate_style_field(genome: dict, target_chars: int = 995) -> str:
    """
    Build a Suno style field from genome/blueprint data.

    Assembles descriptors in priority order: genre -> tempo -> key -> vocals ->
    instruments -> mood -> production -> dynamics -> texture -> negatives.

    Args:
        genome: Dict with style data (genre, tempo, key, vocals, instruments, etc.)
        target_chars: Target character count (Suno max is 999, default 995 for safety)

    Returns:
        Style field string, guaranteed <= target_chars
    """
    parts = _build_descriptor_parts(genome)

    # Build in priority order
    ordered_values = []
    for key in DESCRIPTOR_PRIORITY:
        if key in parts:
            ordered_values.append(parts[key])

    # Add any keys not in the priority list
    for key, value in parts.items():
        if key not in DESCRIPTOR_PRIORITY:
            ordered_values.append(value)

    field = ", ".join(ordered_values)

    # Trim if needed
    if len(field) > target_chars:
        field = trim_style_field(field, target_chars)

    return field


def trim_style_field(field: str, max_chars: int = 998) -> str:
    """
    Intelligently trim a style field to fit within character limit.

    Removes least important descriptors first (from the end, which is
    lowest priority based on assembly order). If still too long, truncates
    individual descriptors by removing trailing adjectives.

    Args:
        field: The style field string to trim
        max_chars: Maximum allowed characters

    Returns:
        Trimmed string, guaranteed len() <= max_chars
    """
    if len(field) <= max_chars:
        return field

    # Split into comma-separated parts
    parts = [p.strip() for p in field.split(",")]

    # Remove parts from the end (lowest priority) until it fits
    while len(", ".join(parts)) > max_chars and len(parts) > 1:
        parts.pop()

    result = ", ".join(parts)

    # If a single remaining part is still too long, hard truncate
    if len(result) > max_chars:
        result = result[: max_chars - 3].rstrip(", ") + "..."

    return result


def _resolve_suno_tag(label: str) -> str:
    """Map a section label to its Suno tag."""
    normalized = label.strip().lower().replace(" ", "_").replace("-", "_")
    return SUNO_TAG_MAP.get(normalized, f"[{label.strip().title()}]")


def generate_tag_skeleton(
    sections: list,
    vocal_modes: Optional[dict] = None,
) -> str:
    """
    Build a Suno lyrics structure from section data.

    Args:
        sections: List of section dicts, each with at minimum:
            - label (str): Section name (verse, chorus, etc.)
            Optional fields:
            - lyrics (str): Actual lyrics for this section
            - energy (float or str): RMS energy in dB, or label like "high"
            - notes (str): Production/performance notes
        vocal_modes: Optional dict mapping section labels to vocal mode strings
            e.g. {"chorus": "Belting, Powerful", "verse": "Whispered, Intimate"}

    Returns:
        Formatted tag skeleton string ready to paste into Suno
    """
    lines = []

    for section in sections:
        label = section.get("label", section.get("name", section.get("type", "verse")))
        suno_tag = _resolve_suno_tag(label)

        # Energy annotation
        energy = section.get("energy")
        energy_str = ""
        if energy is not None:
            if isinstance(energy, (int, float)):
                energy_str = f" [Energy: {_classify_energy(energy)}]"
            elif isinstance(energy, str):
                energy_str = f" [Energy: {_classify_energy_label(energy)}]"

        # Vocal mode from explicit map or section data
        vocal_mode = ""
        normalized_label = label.strip().lower().replace(" ", "_").replace("-", "_")
        if vocal_modes and normalized_label in vocal_modes:
            vocal_mode = f" ({vocal_modes[normalized_label]})"
        elif section.get("vocal_mode"):
            vocal_mode = f" ({section['vocal_mode']})"

        # Build section header
        header = f"{suno_tag}{energy_str}{vocal_mode}"
        lines.append(header)

        # Add lyrics if present
        lyrics = section.get("lyrics", "")
        if lyrics:
            for lyric_line in lyrics.strip().split("\n"):
                lines.append(lyric_line)
        else:
            # Placeholder
            lines.append(f"(lyrics for {label})")

        # Notes as comments
        notes = section.get("notes", "")
        if notes:
            lines.append(f"// {notes}")

        lines.append("")  # Blank line between sections

    return "\n".join(lines).rstrip("\n")


def format_package(
    style_field: str,
    tag_skeleton: str,
    voice_recs: Optional[list] = None,
    notes: str = "",
) -> str:
    """
    Format a complete Suno-ready package as a paste-ready markdown document.

    Args:
        style_field: The generated style field
        tag_skeleton: The generated tag skeleton
        voice_recs: Optional list of voice recommendation dicts
        notes: Optional additional production notes

    Returns:
        Formatted markdown string
    """
    char_count = len(style_field)
    char_status = "OK" if char_count <= 999 else "OVER LIMIT"

    doc_parts = [
        "# Suno Generation Package",
        "",
        "## Style Field",
        f"Characters: {char_count}/999 ({char_status})",
        "",
        "```",
        style_field,
        "```",
        "",
        "## Lyrics / Structure Tags",
        "",
        "```",
        tag_skeleton,
        "```",
    ]

    if voice_recs:
        doc_parts.extend([
            "",
            "## Voice Recommendations",
            "",
        ])
        for i, rec in enumerate(voice_recs, 1):
            label = rec.get("label", f"Option {i}")
            score = rec.get("fit_score", "?")
            desc = rec.get("description", "")
            suno = rec.get("suno_field", "")
            note = rec.get("note", "")

            doc_parts.append(f"### {i}. {label} (fit: {score}/10)")
            if desc:
                doc_parts.append(f"{desc}")
            if suno:
                doc_parts.extend(["", "Suno vocal field:", f"```", suno, "```"])
            if note:
                doc_parts.append(f"*{note}*")
            doc_parts.append("")

    if notes:
        doc_parts.extend([
            "",
            "## Production Notes",
            "",
            notes,
        ])

    doc_parts.extend([
        "",
        "---",
        f"Generated by Style Genome Analyzer | Style field: {char_count} chars",
    ])

    return "\n".join(doc_parts)


if __name__ == "__main__":
    # Self-test with example data
    print("Suno Packager — self-test\n")

    test_genome = {
        "genre": ["Power Metal", "Folk Metal"],
        "tempo": 165,
        "key": "E minor",
        "vocals": "Aggressive male vocals, guttural lows, soaring highs",
        "instruments": ["Distorted guitar", "Double bass drums", "Orchestral strings", "War horns"],
        "mood": ["Epic", "Aggressive", "Triumphant"],
        "production": "Wall of sound, heavy compression, wide stereo",
        "negatives": ["Lo-fi", "Acoustic", "Jazz", "Calm"],
    }

    style = generate_style_field(test_genome)
    print(f"Style field ({len(style)} chars):")
    print(style)
    print()

    test_sections = [
        {"label": "intro", "energy": -30, "notes": "War drums building"},
        {"label": "verse1", "lyrics": "Through fire and steel we march\nNo retreat, no surrender", "energy": "medium"},
        {"label": "prechorus", "lyrics": "The battle cry rises\nFrom deep within", "energy": "high"},
        {"label": "chorus", "lyrics": "STAND AND FIGHT\nWE NEVER DIE\nFORGED IN FLAME\nWE TOUCH THE SKY", "energy": -6},
        {"label": "verse2", "lyrics": "Shields locked, swords drawn\nDarkness falls at dawn", "energy": "medium"},
        {"label": "bridge", "lyrics": "One final charge...", "energy": "high"},
        {"label": "chorus", "lyrics": "STAND AND FIGHT\nWE NEVER DIE", "energy": "maximum"},
        {"label": "outro", "energy": -28, "notes": "Fade with distant horns"},
    ]

    vocal_modes = {
        "chorus": "Belting, Full Power",
        "verse1": "Controlled Growl",
        "verse2": "Controlled Growl",
        "bridge": "Building Intensity",
    }

    skeleton = generate_tag_skeleton(test_sections, vocal_modes)
    print("Tag skeleton:")
    print(skeleton)
    print()

    package = format_package(style, skeleton, notes="Test version — verify vocal fit before full gen")
    print("Full package:")
    print(package)
