"""
Voice Recommendation Engine -- suggests vocal approaches based on
genre, blueprint data, and an established house voice catalog.
"""

import random
from typing import Optional


# Default / established house voice profile
HOUSE_VOICE_DEFAULT = {
    "label": "House Standard",
    "register": "low baritone",
    "texture": "gravelly/raspy",
    "delivery": "staccato/percussive",
    "processing": "raw/dry",
    "language": "mixed (EN/HU mid-sentence)",
    "persona": "drill sergeant",
    "choir": "male unison roar",
    "description": (
        "Deep gravelly baritone with Hungarian accent bleeding through English lines. "
        "Percussive delivery, barking short phrases. Raw and unprocessed — sounds like "
        "a man screaming in a concrete room, not a studio. Default mode for power metal, "
        "folk metal, and industrial gym tracks."
    ),
    "suno_field": (
        "Deep gravelly male vocals, aggressive baritone, raw unprocessed, "
        "percussive delivery, Hungarian accent, male choir backing"
    ),
}


# Complete voice dimension catalog
VOICE_DIMENSIONS = {
    "register": {
        "low_baritone": {
            "label": "Low Baritone",
            "suno": "deep baritone male vocals",
            "genres": ["power metal", "doom", "industrial", "folk metal", "spoken word"],
            "energy_range": (0.3, 1.0),
        },
        "mid_tenor": {
            "label": "Mid-Range Tenor",
            "suno": "tenor male vocals",
            "genres": ["pop", "rock", "edm", "country", "blues"],
            "energy_range": (0.2, 0.8),
        },
        "falsetto": {
            "label": "Falsetto",
            "suno": "falsetto male vocals, high-pitched",
            "genres": ["synthwave", "funk", "r&b", "psychedelic", "art rock"],
            "energy_range": (0.1, 0.6),
        },
        "bass": {
            "label": "Bass",
            "suno": "deep bass male vocals, rumbling low",
            "genres": ["doom", "death metal", "dark ambient", "drone", "gothic"],
            "energy_range": (0.4, 1.0),
        },
    },
    "texture": {
        "gravelly": {
            "label": "Gravelly/Raspy",
            "suno": "gravelly raspy vocals",
            "genres": ["metal", "punk", "blues", "industrial", "folk metal"],
            "intensity_min": 0.4,
        },
        "clean": {
            "label": "Clean/Smooth",
            "suno": "clean smooth vocals",
            "genres": ["pop", "r&b", "jazz", "ambient", "synthwave"],
            "intensity_min": 0.0,
        },
        "nasal_punk": {
            "label": "Nasal Punk",
            "suno": "nasal punk vocals, sneering",
            "genres": ["punk", "pop punk", "ska", "garage rock"],
            "intensity_min": 0.3,
        },
        "breathy": {
            "label": "Breathy",
            "suno": "breathy intimate vocals",
            "genres": ["ambient", "shoegaze", "dream pop", "lo-fi", "jazz"],
            "intensity_min": 0.0,
        },
        "operatic": {
            "label": "Operatic",
            "suno": "operatic powerful vocals, classical technique",
            "genres": ["symphonic metal", "power metal", "classical crossover", "gothic"],
            "intensity_min": 0.5,
        },
    },
    "delivery": {
        "staccato": {
            "label": "Staccato/Percussive",
            "suno": "percussive staccato vocal delivery",
            "genres": ["industrial", "metal", "edm", "rap", "punk"],
            "tempo_range": (120, 220),
        },
        "legato": {
            "label": "Legato",
            "suno": "legato flowing vocal delivery",
            "genres": ["ballad", "ambient", "jazz", "r&b", "classical"],
            "tempo_range": (60, 140),
        },
        "monotone": {
            "label": "Monotone Deadpan",
            "suno": "monotone deadpan vocal delivery",
            "genres": ["post-punk", "industrial", "dark wave", "spoken word", "drone"],
            "tempo_range": (80, 160),
        },
        "sprechgesang": {
            "label": "Sprechgesang",
            "suno": "spoken-sung Sprechgesang delivery, half-singing half-speaking",
            "genres": ["art rock", "cabaret", "avant-garde", "industrial", "gothic"],
            "tempo_range": (90, 160),
        },
        "scat": {
            "label": "Scat",
            "suno": "scat vocal improvisation, rhythmic syllables",
            "genres": ["jazz", "bebop", "funk", "experimental"],
            "tempo_range": (100, 200),
        },
    },
    "processing": {
        "raw": {
            "label": "Raw/Dry",
            "suno": "raw dry unprocessed vocals",
            "genres": ["punk", "metal", "folk", "garage", "industrial"],
        },
        "chorus_effect": {
            "label": "Chorus Effect",
            "suno": "chorus-doubled vocals, shimmering",
            "genres": ["shoegaze", "dream pop", "synthwave", "new wave"],
        },
        "vocoder": {
            "label": "Vocoder",
            "suno": "vocoder-processed robotic vocals",
            "genres": ["edm", "synthpop", "electro", "cyberpunk", "industrial"],
        },
        "octave_doubled": {
            "label": "Octave-Doubled",
            "suno": "octave-doubled vocals, harmonic thickness",
            "genres": ["metal", "doom", "power metal", "gothic"],
        },
        "lofi_filter": {
            "label": "Lo-Fi Filter",
            "suno": "lo-fi filtered vocals, vintage degraded",
            "genres": ["lo-fi", "vaporwave", "indie", "garage", "psychedelic"],
        },
    },
    "language": {
        "hungarian": {
            "label": "Hungarian",
            "suno": "Hungarian language vocals",
            "note": "Native-language authenticity, limited Suno pronunciation quality",
        },
        "english": {
            "label": "English",
            "suno": "English vocals",
            "note": "Broadest audience, best Suno TTS quality",
        },
        "german": {
            "label": "German",
            "suno": "German language vocals",
            "note": "Industrial/Rammstein aesthetic, if it fits your voice",
        },
        "mixed": {
            "label": "Mixed Mid-Sentence",
            "suno": "multilingual vocals switching between languages",
            "note": "Signature move — EN base with HU/DE grenades",
        },
    },
    "persona": {
        "drill_sergeant": {
            "label": "Drill Sergeant",
            "suno": "commanding drill sergeant vocals, barking orders",
            "genres": ["industrial", "metal", "power metal", "edm"],
            "energy_floor": 0.6,
        },
        "sad_old_man": {
            "label": "Sad Old Man",
            "suno": "weary aged male vocals, melancholic gravelly",
            "genres": ["folk", "blues", "country", "acoustic", "doom"],
            "energy_floor": 0.1,
        },
        "detached_scientist": {
            "label": "Detached Scientist",
            "suno": "cold clinical vocals, emotionless narration",
            "genres": ["industrial", "dark ambient", "post-punk", "experimental"],
            "energy_floor": 0.2,
        },
        "manic_preacher": {
            "label": "Manic Preacher",
            "suno": "manic evangelical vocals, rising intensity, unhinged sermon",
            "genres": ["industrial", "metal", "punk", "noise", "experimental"],
            "energy_floor": 0.5,
        },
        "tired_boxer": {
            "label": "Tired Boxer",
            "suno": "exhausted breathy male vocals, fighting through fatigue",
            "genres": ["rock", "metal", "folk metal", "blues", "spoken word"],
            "energy_floor": 0.3,
        },
    },
    "choir": {
        "male_unison": {
            "label": "Male Unison Roar",
            "suno": "male choir unison roar, army chant",
            "genres": ["metal", "folk metal", "power metal", "industrial"],
        },
        "gospel": {
            "label": "Gospel Choir",
            "suno": "gospel choir backing vocals, soulful harmonies",
            "genres": ["blues", "soul", "rock", "gospel", "country"],
        },
        "monk_drone": {
            "label": "Monk Drone",
            "suno": "monk drone chant, Gregorian low hum",
            "genres": ["doom", "dark ambient", "gothic", "drone", "medieval"],
        },
        "stadium_crowd": {
            "label": "Stadium Crowd",
            "suno": "stadium crowd chanting, massive crowd vocals",
            "genres": ["rock", "metal", "power metal", "punk", "edm"],
        },
        "childrens_choir": {
            "label": "Children's Choir",
            "suno": "children's choir, innocent ethereal backing vocals",
            "genres": ["ambient", "art rock", "gothic", "horror", "classical"],
        },
        "female_backing": {
            "label": "Female Backing",
            "suno": "female backing vocals, ethereal harmonies",
            "genres": ["symphonic metal", "dream pop", "folk", "gothic", "ambient"],
        },
    },
}


# Genre-to-voice presets: genres you have used, with opinionated defaults
GENRE_PRESETS = {
    # --- Genres you have used ---
    "power metal": {
        "register": "low_baritone",
        "texture": "gravelly",
        "delivery": "staccato",
        "processing": "octave_doubled",
        "language": "english",
        "persona": "drill_sergeant",
        "choir": "male_unison",
        "fit_note": "House-voice home turf. Full aggression, male choir call-and-response.",
    },
    "folk metal": {
        "register": "low_baritone",
        "texture": "gravelly",
        "delivery": "legato",
        "processing": "raw",
        "language": "mixed",
        "persona": "tired_boxer",
        "choir": "male_unison",
        "fit_note": "Legato delivery for folk melody lines, gravelly for battle cries. HU/EN switching.",
    },
    "edm industrial": {
        "register": "low_baritone",
        "texture": "gravelly",
        "delivery": "staccato",
        "processing": "vocoder",
        "language": "english",
        "persona": "manic_preacher",
        "choir": "stadium_crowd",
        "fit_note": "Vocoder processing for drops, raw for breakdowns. Manic energy builds.",
    },
    "doom": {
        "register": "bass",
        "texture": "gravelly",
        "delivery": "legato",
        "processing": "raw",
        "language": "english",
        "persona": "sad_old_man",
        "choir": "monk_drone",
        "fit_note": "Slowest, heaviest. Monk drone choir adds ceremonial weight. Weary delivery.",
    },
    "spoken word": {
        "register": "low_baritone",
        "texture": "clean",
        "delivery": "monotone",
        "processing": "raw",
        "language": "hungarian",
        "persona": "detached_scientist",
        "choir": None,
        "fit_note": "Clean delivery, no choir. Hungarian language for maximum authenticity.",
    },
    "industrial": {
        "register": "low_baritone",
        "texture": "gravelly",
        "delivery": "staccato",
        "processing": "vocoder",
        "language": "german",
        "persona": "drill_sergeant",
        "choir": "male_unison",
        "fit_note": "Rammstein DNA. German language, vocoder processing, military precision.",
    },
    # --- Genres you haven't used (creative stretch recommendations) ---
    "jazz": {
        "register": "mid_tenor",
        "texture": "clean",
        "delivery": "scat",
        "processing": "raw",
        "language": "english",
        "persona": "sad_old_man",
        "choir": None,
        "fit_note": "STRETCH: Clean tenor with scat delivery. Keep the melancholic persona for depth.",
    },
    "blues": {
        "register": "low_baritone",
        "texture": "gravelly",
        "delivery": "legato",
        "processing": "lofi_filter",
        "language": "english",
        "persona": "tired_boxer",
        "choir": "gospel",
        "fit_note": "Natural fit: the gravelly house voice is built for blues. Gospel choir elevates it.",
    },
    "ambient": {
        "register": "falsetto",
        "texture": "breathy",
        "delivery": "legato",
        "processing": "chorus_effect",
        "language": "hungarian",
        "persona": "detached_scientist",
        "choir": "monk_drone",
        "fit_note": "STRETCH: Falsetto is new territory. Hungarian whispered over monk drones.",
    },
    "country": {
        "register": "mid_tenor",
        "texture": "clean",
        "delivery": "legato",
        "processing": "raw",
        "language": "english",
        "persona": "tired_boxer",
        "choir": "gospel",
        "fit_note": "STRETCH: Clean tenor, storytelling delivery. Gospel choir for Americana feel.",
    },
    "synthwave": {
        "register": "mid_tenor",
        "texture": "clean",
        "delivery": "legato",
        "processing": "chorus_effect",
        "language": "english",
        "persona": "detached_scientist",
        "choir": "female_backing",
        "fit_note": "STRETCH: Clean 80s tenor with chorus shimmer. Female backing for retro vibes.",
    },
    "punk": {
        "register": "mid_tenor",
        "texture": "nasal_punk",
        "delivery": "staccato",
        "processing": "raw",
        "language": "english",
        "persona": "manic_preacher",
        "choir": "stadium_crowd",
        "fit_note": "Nasal sneer, raw energy. Stadium crowd for singalong anthems.",
    },
    "gothic": {
        "register": "bass",
        "texture": "operatic",
        "delivery": "sprechgesang",
        "processing": "chorus_effect",
        "language": "german",
        "persona": "detached_scientist",
        "choir": "childrens_choir",
        "fit_note": "STRETCH: Operatic bass with Sprechgesang. Children's choir for contrast-horror.",
    },
    "hip hop": {
        "register": "low_baritone",
        "texture": "gravelly",
        "delivery": "staccato",
        "processing": "raw",
        "language": "mixed",
        "persona": "drill_sergeant",
        "choir": "stadium_crowd",
        "fit_note": "The house voice's percussive delivery maps well to hip hop flow. Mixed language bars.",
    },
    "shoegaze": {
        "register": "falsetto",
        "texture": "breathy",
        "delivery": "legato",
        "processing": "chorus_effect",
        "language": "english",
        "persona": "sad_old_man",
        "choir": "female_backing",
        "fit_note": "STRETCH: Total departure. Breathy falsetto buried in reverb. Voice as texture.",
    },
    "ska": {
        "register": "mid_tenor",
        "texture": "nasal_punk",
        "delivery": "staccato",
        "processing": "raw",
        "language": "english",
        "persona": "manic_preacher",
        "choir": "male_unison",
        "fit_note": "STRETCH: Nasal punk delivery over upstrokes. Male choir for brass-section energy.",
    },
}

# Mood-to-dimension biases
MOOD_BIASES = {
    "aggressive": {"texture": "gravelly", "delivery": "staccato", "persona": "drill_sergeant"},
    "dark": {"register": "bass", "texture": "gravelly", "persona": "sad_old_man"},
    "epic": {"register": "low_baritone", "texture": "operatic", "choir": "male_unison"},
    "melancholic": {"texture": "clean", "delivery": "legato", "persona": "sad_old_man"},
    "manic": {"delivery": "staccato", "persona": "manic_preacher", "choir": "stadium_crowd"},
    "calm": {"texture": "breathy", "delivery": "legato", "processing": "chorus_effect"},
    "triumphant": {"register": "low_baritone", "texture": "operatic", "choir": "male_unison"},
    "raw": {"texture": "gravelly", "processing": "raw", "choir": None},
    "psychedelic": {"texture": "breathy", "processing": "chorus_effect", "register": "falsetto"},
    "industrial": {"processing": "vocoder", "delivery": "staccato", "persona": "detached_scientist"},
    "haunting": {"register": "falsetto", "texture": "breathy", "choir": "childrens_choir"},
    "anthemic": {"choir": "stadium_crowd", "delivery": "legato", "register": "mid_tenor"},
    "primal": {"texture": "gravelly", "delivery": "staccato", "persona": "drill_sergeant", "choir": "male_unison"},
    "hypnotic": {"delivery": "monotone", "processing": "chorus_effect", "persona": "detached_scientist"},
}


def _score_dimension_fit(dimension: str, key: str, genre: str, mood: str, tempo: int) -> float:
    """Score how well a specific dimension choice fits the target parameters."""
    dim_data = VOICE_DIMENSIONS.get(dimension, {}).get(key, {})
    if not dim_data:
        return 5.0  # neutral

    score = 5.0
    genre_lower = genre.lower()

    # Genre match
    genres = dim_data.get("genres", [])
    if genres:
        for g in genres:
            if g in genre_lower or genre_lower in g:
                score += 3.0
                break
        else:
            # Partial match on genre words
            genre_words = set(genre_lower.split())
            for g in genres:
                if genre_words & set(g.split()):
                    score += 1.5
                    break

    # Tempo range match
    tempo_range = dim_data.get("tempo_range")
    if tempo_range and tempo:
        low, high = tempo_range
        if low <= tempo <= high:
            score += 1.5
        elif abs(tempo - low) < 20 or abs(tempo - high) < 20:
            score += 0.5

    # Energy range match (using tempo as rough proxy)
    energy_range = dim_data.get("energy_range")
    if energy_range and tempo:
        normalized_energy = min(1.0, max(0.0, (tempo - 60) / 160))
        low, high = energy_range
        if low <= normalized_energy <= high:
            score += 1.0

    return min(10.0, score)


def _build_voice_dict(
    register: str,
    texture: str,
    delivery: str,
    processing: str,
    language: str,
    persona: str,
    choir: Optional[str],
    fit_note: str = "",
) -> dict:
    """Build a complete voice recommendation dict from dimension keys."""
    reg = VOICE_DIMENSIONS["register"].get(register, {})
    tex = VOICE_DIMENSIONS["texture"].get(texture, {})
    deliv = VOICE_DIMENSIONS["delivery"].get(delivery, {})
    proc = VOICE_DIMENSIONS["processing"].get(processing, {})
    lang = VOICE_DIMENSIONS["language"].get(language, {})
    pers = VOICE_DIMENSIONS["persona"].get(persona, {})
    ch = VOICE_DIMENSIONS["choir"].get(choir, {}) if choir else {}

    # Build suno field from components
    suno_parts = [
        reg.get("suno", ""),
        tex.get("suno", ""),
        deliv.get("suno", ""),
        proc.get("suno", ""),
    ]
    if pers:
        suno_parts.append(pers.get("suno", ""))
    if ch:
        suno_parts.append(ch.get("suno", ""))

    suno_field = ", ".join(p for p in suno_parts if p)

    # Build human description
    desc_parts = [
        reg.get("label", register),
        tex.get("label", texture),
        f"with {deliv.get('label', delivery)} delivery",
    ]
    if proc.get("label"):
        desc_parts.append(f"({proc['label']} processing)")
    if lang.get("label"):
        desc_parts.append(f"in {lang['label']}")
    if pers.get("label"):
        desc_parts.append(f"channeling {pers['label']}")
    if ch.get("label"):
        desc_parts.append(f"backed by {ch['label']}")

    description = " ".join(desc_parts) + "."

    return {
        "register": register,
        "texture": texture,
        "delivery": delivery,
        "processing": processing,
        "language": language,
        "persona": persona,
        "choir": choir,
        "label": f"{pers.get('label', persona)} {reg.get('label', register)}",
        "description": description,
        "suno_field": suno_field,
        "note": fit_note,
    }


def get_default_voice() -> dict:
    """Return the established default house voice profile."""
    return dict(HOUSE_VOICE_DEFAULT)


def voice_for_genre(genre: str) -> dict:
    """
    Return the most suitable voice for a specific genre.

    Checks presets first, then builds a best-guess from dimension scoring.

    Args:
        genre: Genre string (e.g., "power metal", "jazz", "ambient")

    Returns:
        Voice recommendation dict with all dimensions + suno_field
    """
    genre_lower = genre.strip().lower()

    # Check presets
    if genre_lower in GENRE_PRESETS:
        preset = GENRE_PRESETS[genre_lower]
        voice = _build_voice_dict(
            register=preset["register"],
            texture=preset["texture"],
            delivery=preset["delivery"],
            processing=preset["processing"],
            language=preset["language"],
            persona=preset["persona"],
            choir=preset.get("choir"),
            fit_note=preset.get("fit_note", ""),
        )
        voice["fit_score"] = 8
        return voice

    # No preset: build from dimension scoring with default tempo
    return _recommend_single(genre_lower, "aggressive", 140)


def _recommend_single(genre: str, mood: str, tempo: int) -> dict:
    """Build a single voice recommendation by scoring all dimensions."""
    best = {}

    for dimension in ["register", "texture", "delivery", "processing"]:
        best_key = None
        best_score = -1
        for key in VOICE_DIMENSIONS[dimension]:
            score = _score_dimension_fit(dimension, key, genre, mood, tempo)
            if score > best_score:
                best_score = score
                best_key = key
        best[dimension] = best_key

    # Apply mood biases
    mood_lower = mood.strip().lower()
    if mood_lower in MOOD_BIASES:
        for dim, val in MOOD_BIASES[mood_lower].items():
            if dim in best and val is not None:
                best[dim] = val

    # Language: default to English unless mood/genre suggests otherwise
    best["language"] = "english"
    genre_lower = genre.lower()
    if "hungarian" in genre_lower or "magyar" in genre_lower:
        best["language"] = "hungarian"
    elif any(g in genre_lower for g in ["industrial", "neue deutsche", "rammstein"]):
        best["language"] = "german"
    elif "folk" in genre_lower and "metal" in genre_lower:
        best["language"] = "mixed"

    # Persona: pick best from scoring
    best_persona = "drill_sergeant"
    best_p_score = -1
    for key, data in VOICE_DIMENSIONS["persona"].items():
        score = 5.0
        for g in data.get("genres", []):
            if g in genre_lower or genre_lower in g:
                score += 3.0
                break
        if mood_lower in MOOD_BIASES:
            bias_persona = MOOD_BIASES[mood_lower].get("persona")
            if bias_persona == key:
                score += 2.0
        if score > best_p_score:
            best_p_score = score
            best_persona = key
    best["persona"] = best_persona

    # Choir: pick best from scoring
    best_choir = None
    best_c_score = -1
    for key, data in VOICE_DIMENSIONS["choir"].items():
        score = 5.0
        for g in data.get("genres", []):
            if g in genre_lower or genre_lower in g:
                score += 3.0
                break
        if mood_lower in MOOD_BIASES:
            bias_choir = MOOD_BIASES[mood_lower].get("choir")
            if bias_choir == key:
                score += 2.0
            elif bias_choir is None:
                score -= 2.0  # mood says no choir
        if score > best_c_score:
            best_c_score = score
            best_choir = key
    # If mood explicitly suppresses choir
    if mood_lower in MOOD_BIASES and MOOD_BIASES[mood_lower].get("choir") is None:
        best_choir = None
    best["choir"] = best_choir

    voice = _build_voice_dict(**best)
    voice["fit_score"] = 6  # generic recommendation
    return voice


def recommend_voices(
    genre: str,
    mood: str,
    tempo: int,
    energy_profile: Optional[str] = None,
) -> list[dict]:
    """
    Generate 3 ranked voice recommendations for a given genre/mood/tempo.

    Returns diverse options: (1) best fit, (2) creative alternative, (3) wild card.

    Args:
        genre: Target genre (e.g., "power metal", "jazz fusion")
        mood: Dominant mood (e.g., "aggressive", "melancholic", "epic")
        tempo: BPM as integer
        energy_profile: Optional energy descriptor ("building", "sustained", "explosive")

    Returns:
        List of 3 voice recommendation dicts, each with:
        - label, description, suno_field, fit_score (1-10), note
        - Plus all dimension keys (register, texture, delivery, etc.)
    """
    genre_lower = genre.strip().lower()
    mood_lower = mood.strip().lower()
    results = []

    # --- RECOMMENDATION 1: Best Fit ---
    # Try preset first
    if genre_lower in GENRE_PRESETS:
        preset = GENRE_PRESETS[genre_lower]
        voice = _build_voice_dict(
            register=preset["register"],
            texture=preset["texture"],
            delivery=preset["delivery"],
            processing=preset["processing"],
            language=preset["language"],
            persona=preset["persona"],
            choir=preset.get("choir"),
            fit_note=preset.get("fit_note", f"Optimized preset for {genre}."),
        )
        voice["fit_score"] = 9
        # Apply mood overrides
        if mood_lower in MOOD_BIASES:
            bias = MOOD_BIASES[mood_lower]
            for dim, val in bias.items():
                if dim in voice and val is not None and voice.get(dim) != val:
                    voice["note"] += f" Mood-adjusted {dim} toward {val}."
        results.append(voice)
    else:
        voice = _recommend_single(genre_lower, mood_lower, tempo)
        voice["fit_score"] = 7
        voice["note"] = f"Computed best fit for {genre} / {mood}."
        results.append(voice)

    # --- RECOMMENDATION 2: Creative Alternative ---
    # Flip one or two dimensions from the best fit for contrast
    alt = dict(results[0])  # shallow copy of dimensions
    alt_dims = {}
    for dim in ["register", "texture", "delivery", "processing", "persona", "choir"]:
        alt_dims[dim] = alt.get(dim)

    # Pick 2 dimensions to vary
    vary_dims = random.sample(
        ["texture", "delivery", "processing", "persona", "choir"], 2
    )

    for dim in vary_dims:
        current = alt_dims.get(dim)
        options = list(VOICE_DIMENSIONS.get(dim, {}).keys())
        if current in options:
            options.remove(current)
        if options:
            # Score remaining options and pick the best non-default
            scored = []
            for opt in options:
                s = _score_dimension_fit(dim, opt, genre_lower, mood_lower, tempo)
                scored.append((opt, s))
            scored.sort(key=lambda x: x[1], reverse=True)
            alt_dims[dim] = scored[0][0]

    alt_voice = _build_voice_dict(
        register=alt_dims.get("register", "low_baritone"),
        texture=alt_dims.get("texture", "gravelly"),
        delivery=alt_dims.get("delivery", "staccato"),
        processing=alt_dims.get("processing", "raw"),
        language=alt_dims.get("language", alt.get("language", "english")),
        persona=alt_dims.get("persona", "drill_sergeant"),
        choir=alt_dims.get("choir"),
        fit_note=f"Creative alternative: varied {', '.join(vary_dims)} from best fit.",
    )
    alt_voice["fit_score"] = 6
    results.append(alt_voice)

    # --- RECOMMENDATION 3: Wild Card ---
    # Intentionally pick unexpected dimensions for creative discovery
    wild_dims = {}

    # Pick register that's unusual for this genre
    reg_options = list(VOICE_DIMENSIONS["register"].keys())
    used_reg = results[0].get("register")
    if used_reg in reg_options:
        reg_options.remove(used_reg)
    wild_dims["register"] = random.choice(reg_options) if reg_options else "mid_tenor"

    # Pick contrasting texture
    tex_options = list(VOICE_DIMENSIONS["texture"].keys())
    used_tex = results[0].get("texture")
    if used_tex in tex_options:
        tex_options.remove(used_tex)
    wild_dims["texture"] = random.choice(tex_options) if tex_options else "clean"

    # Pick delivery style from a different genre family
    del_options = list(VOICE_DIMENSIONS["delivery"].keys())
    wild_dims["delivery"] = random.choice(del_options)

    # Processing: always different from best fit
    proc_options = list(VOICE_DIMENSIONS["processing"].keys())
    used_proc = results[0].get("processing")
    if used_proc in proc_options:
        proc_options.remove(used_proc)
    wild_dims["processing"] = random.choice(proc_options) if proc_options else "lofi_filter"

    # Persona: random
    wild_dims["persona"] = random.choice(list(VOICE_DIMENSIONS["persona"].keys()))

    # Choir: random (including None option)
    choir_options = list(VOICE_DIMENSIONS["choir"].keys()) + [None]
    wild_dims["choir"] = random.choice(choir_options)

    # Language: keep accessible
    wild_dims["language"] = random.choice(["english", "mixed", "hungarian"])

    wild_voice = _build_voice_dict(
        register=wild_dims["register"],
        texture=wild_dims["texture"],
        delivery=wild_dims["delivery"],
        processing=wild_dims["processing"],
        language=wild_dims["language"],
        persona=wild_dims["persona"],
        choir=wild_dims["choir"],
        fit_note="WILD CARD: Intentionally unexpected combination. May reveal something new.",
    )
    wild_voice["fit_score"] = 4
    results.append(wild_voice)

    # Apply energy profile annotations
    if energy_profile:
        ep = energy_profile.strip().lower()
        for r in results:
            if ep == "building":
                r["note"] += " Energy builds: start restrained, end explosive."
            elif ep == "sustained":
                r["note"] += " Sustained energy: maintain intensity throughout."
            elif ep == "explosive":
                r["note"] += " Explosive: immediate full intensity from bar one."
            elif ep == "decaying":
                r["note"] += " Decaying energy: start strong, fade to whisper."

    return results


if __name__ == "__main__":
    print("Voice Engine — self-test\n")
    print("=" * 60)

    # Test default voice
    default = get_default_voice()
    print(f"Default voice: {default['label']}")
    print(f"Suno field: {default['suno_field']}")
    print()

    # Test genre presets
    for genre in ["power metal", "doom", "jazz", "ambient", "gothic"]:
        voice = voice_for_genre(genre)
        print(f"Genre: {genre}")
        print(f"  Voice: {voice['label']}")
        print(f"  Suno: {voice['suno_field'][:80]}...")
        print(f"  Note: {voice.get('note', 'N/A')}")
        print()

    # Test full recommendations
    print("=" * 60)
    print("Full recommendations for: EDM Industrial, aggressive, 145 BPM\n")
    recs = recommend_voices("EDM Industrial", "aggressive", 145, energy_profile="building")
    for i, rec in enumerate(recs, 1):
        print(f"--- Recommendation {i} (fit: {rec['fit_score']}/10) ---")
        print(f"Label: {rec['label']}")
        print(f"Description: {rec['description']}")
        print(f"Suno: {rec['suno_field']}")
        print(f"Note: {rec['note']}")
        print()
