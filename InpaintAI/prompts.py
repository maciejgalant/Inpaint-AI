ORTHO_BASE_PROMPT_EN = """
You are editing a real high-resolution geospatial orthophoto captured from a near-nadir aerial viewpoint.
Modify only the transparent/masked area. Treat the unmasked surrounding pixels as the primary visual reference.
The result must look as if the edited content had been present during the same aerial survey and captured by the same sensor.

Match the surrounding source imagery as closely as possible in:
- RGB color palette and local color cast,
- brightness, exposure, contrast, saturation and white balance,
- illumination direction, shadow direction, shadow softness and shadow intensity,
- apparent ground sampling resolution, sharpness, blur, noise and compression character,
- surface texture, vegetation character, building materials and road materials,
- object scale, spacing, geometry and spatial pattern.

Maintain a strict top-down/nadir orthophoto appearance. Generated roads, paths, vegetation, buildings and other objects
must connect naturally to existing features at the mask boundary. The boundary transition must be visually seamless.
Do not make the generated region cleaner, sharper, more saturated, more contrasty or more stylized than its surroundings.
Prioritize photorealistic geospatial consistency and seamless integration over artistic appearance.
Preserve all pixels outside the editable mask exactly.
""".strip()

ORTHO_NEGATIVE_BASE_EN = """
Avoid oblique perspective, perspective tilt, illustration, painting, 3D-render appearance, fantasy styling,
oversaturated colors, excessive contrast, mismatched exposure, mismatched sharpness, repeated patterns,
warped roads, impossible geometry, duplicated objects, malformed vehicles, random text, labels, logos and watermarks.
Do not introduce visible seams, halos or abrupt color/texture changes at the mask boundary.
""".strip()

MATCHING_MODES = {
    "strict": {
        "labels": {"pl": "Ścisłe", "en": "Strict"},
        "instruction": (
            "Use STRICT source matching. Reproduce the local color grading, exposure, texture, sharpness, "
            "noise, illumination and spatial character of the surrounding orthophoto as closely as possible. "
            "Seamless visual integration is more important than adding extra detail."
        ),
    },
    "balanced": {
        "labels": {"pl": "Zrównoważone", "en": "Balanced"},
        "instruction": (
            "Use BALANCED source matching. Closely match the surrounding orthophoto while allowing moderate "
            "freedom to reconstruct plausible details inside the mask."
        ),
    },
    "creative": {
        "labels": {"pl": "Kreatywne", "en": "Creative"},
        "instruction": (
            "Use CREATIVE reconstruction while retaining realistic aerial scale, top-down perspective, "
            "photographic appearance and a natural transition to the surrounding orthophoto."
        ),
    },
}

PRESETS = {
    "custom": {
        "labels": {"pl": "Własny prompt", "en": "Custom prompt"},
        "suggestions": {"pl": "", "en": ""},
        "instruction": "",
        "avoid": "",
    },
    "single_family": {
        "labels": {"pl": "Zabudowa jednorodzinna", "en": "Single-family housing"},
        "suggestions": {
            "pl": "Stwórz realistyczną zabudowę jednorodzinną dopasowaną do otoczenia.",
            "en": "Create realistic single-family housing matching the surroundings.",
        },
        "instruction": (
            "Create plausible low-density residential development with detached houses, varied roofs, gardens, "
            "driveways, fences, trees and local access roads. Match the surrounding parcel pattern and density."
        ),
        "avoid": "Avoid apartment towers, oversized buildings and industrial compounds.",
    },
    "multi_family": {
        "labels": {"pl": "Zabudowa wielorodzinna", "en": "Multi-family housing"},
        "suggestions": {
            "pl": "Stwórz realistyczną zabudowę wielorodzinną z drogami, parkingami i zielenią.",
            "en": "Create realistic multi-family housing with roads, parking and greenery.",
        },
        "instruction": (
            "Create realistic medium-density residential development with apartment buildings, internal roads, "
            "parking, sidewalks, courtyards and landscaped greenery."
        ),
        "avoid": "Avoid detached rural farmsteads and heavy industrial facilities.",
    },
    "urban_dense": {
        "labels": {"pl": "Zabudowa miejska", "en": "Dense urban development"},
        "suggestions": {
            "pl": "Stwórz realistyczną zwartą zabudowę miejską zgodną z układem otoczenia.",
            "en": "Create realistic dense urban development consistent with the surroundings.",
        },
        "instruction": (
            "Create realistic dense urban fabric with buildings, courtyards, streets, sidewalks, service access, "
            "parking and urban vegetation. Follow the surrounding block geometry and street pattern."
        ),
        "avoid": "Avoid rural field patterns and isolated suburban houses.",
    },
    "industrial": {
        "labels": {"pl": "Zabudowa przemysłowa / magazynowa", "en": "Industrial / warehouse"},
        "suggestions": {
            "pl": "Stwórz realistyczny obszar przemysłowy lub magazynowy dopasowany do otoczenia.",
            "en": "Create a realistic industrial or warehouse area matching the surroundings.",
        },
        "instruction": (
            "Create plausible industrial or warehouse development with large roofed buildings, service yards, "
            "access roads, loading areas and parking at a scale consistent with the surroundings."
        ),
        "avoid": "Avoid residential gardens and dense historic urban fabric.",
    },
    "parking": {
        "labels": {"pl": "Parking", "en": "Parking area"},
        "suggestions": {
            "pl": "Stwórz realistyczny parking z miejscami postojowymi i drogą dojazdową.",
            "en": "Create a realistic parking area with parking spaces and an access road.",
        },
        "instruction": (
            "Create a realistic parking area naturally connected to nearby roads. Use plausible lane widths, "
            "parking-space geometry, pavement texture, markings where appropriate, a realistic number of vehicles "
            "and drainage/green edges consistent with the local context."
        ),
        "avoid": "Avoid oversized vehicles, repetitive car cloning and implausible parking geometry.",
    },
    "road": {
        "labels": {"pl": "Droga / ulica asfaltowa", "en": "Paved road / street"},
        "suggestions": {
            "pl": "Stwórz realistyczną drogę asfaltową naturalnie połączoną z istniejącą siecią.",
            "en": "Create a realistic paved road naturally connected to the existing network.",
        },
        "instruction": (
            "Create a realistic paved road or street connected naturally to existing roads. Match local width, "
            "surface, markings, shoulders, curbs, sidewalks and intersection geometry where applicable."
        ),
        "avoid": "Avoid disconnected road ends, warped lanes and implausible curvature.",
    },
    "dirt_road": {
        "labels": {"pl": "Droga gruntowa", "en": "Dirt road"},
        "suggestions": {
            "pl": "Stwórz realistyczną drogę gruntową dopasowaną do terenu.",
            "en": "Create a realistic dirt road matching the terrain.",
        },
        "instruction": (
            "Create a realistic unpaved dirt or gravel road with wheel tracks, natural edges and vegetation transitions "
            "matching local terrain and usage intensity."
        ),
        "avoid": "Avoid clean asphalt markings and urban curbs unless present in the surroundings.",
    },
    "square": {
        "labels": {"pl": "Plac / powierzchnia utwardzona", "en": "Paved square / hardscape"},
        "suggestions": {
            "pl": "Stwórz realistyczny plac lub powierzchnię utwardzoną dopasowaną do otoczenia.",
            "en": "Create a realistic paved square or hardscape matching the surroundings.",
        },
        "instruction": (
            "Create a plausible paved or hard-surface area with local material character, access paths, edge details "
            "and subtle wear consistent with nearby surfaces."
        ),
        "avoid": "Avoid overly clean synthetic textures and decorative patterns not supported by the context.",
    },
    "sports": {
        "labels": {"pl": "Obiekt sportowy", "en": "Sports facility"},
        "suggestions": {
            "pl": "Stwórz realistyczny obiekt sportowy dopasowany skalą i kolorystyką do ortofotomapy.",
            "en": "Create a realistic sports facility matching the orthophoto in scale and color.",
        },
        "instruction": (
            "Create a realistic sports facility such as a field, court or small recreation complex, with plausible "
            "surface materials, boundaries, access paths, fencing and surrounding greenery."
        ),
        "avoid": "Avoid oversized stadium architecture unless the user explicitly requests it.",
    },
    "playground": {
        "labels": {"pl": "Plac zabaw", "en": "Playground"},
        "suggestions": {
            "pl": "Stwórz realistyczny plac zabaw z dojściem i zielenią.",
            "en": "Create a realistic playground with pedestrian access and greenery.",
        },
        "instruction": (
            "Create a realistic playground visible from aerial imagery, with safety-surface areas, compact play structures, "
            "paths, seating zones and surrounding greenery at plausible scale."
        ),
        "avoid": "Avoid oversized toy-like objects and bright artificial colors inconsistent with the source image.",
    },
    "urban_green": {
        "labels": {"pl": "Zieleń miejska", "en": "Urban greenery"},
        "suggestions": {
            "pl": "Stwórz realistyczny teren zieleni miejskiej z trawą, drzewami i ścieżkami.",
            "en": "Create realistic urban green space with grass, trees and paths.",
        },
        "instruction": (
            "Create realistic urban green space with lawns, tree groups, shrubs and paths matching nearby vegetation "
            "species character, canopy scale and maintenance level."
        ),
        "avoid": "Avoid tropical vegetation or uniformly repeated tree crowns unless supported by the surroundings.",
    },
    "forest": {
        "labels": {"pl": "Las / zadrzewienie", "en": "Forest / woodland"},
        "suggestions": {
            "pl": "Odtwórz realistyczny las lub zadrzewienie zgodne z otaczającą roślinnością.",
            "en": "Create realistic forest or woodland matching surrounding vegetation.",
        },
        "instruction": (
            "Create realistic forest or woodland matching nearby canopy density, crown sizes, species character, "
            "gaps, understory visibility, shadowing and edge structure."
        ),
        "avoid": "Avoid repeated cloned tree crowns and vegetation types absent from the local context.",
    },
    "meadow": {
        "labels": {"pl": "Łąka / trawa", "en": "Meadow / grass"},
        "suggestions": {
            "pl": "Odtwórz realistyczną łąkę lub teren trawiasty zgodny z otoczeniem.",
            "en": "Create realistic meadow or grassland matching the surroundings.",
        },
        "instruction": (
            "Create natural meadow or grassland with subtle tonal variation, mowing/use patterns and vegetation texture "
            "consistent with adjacent areas."
        ),
        "avoid": "Avoid uniform synthetic green fills and decorative lawn patterns.",
    },
    "farmland": {
        "labels": {"pl": "Pole uprawne", "en": "Farmland"},
        "suggestions": {
            "pl": "Stwórz realistyczne pole uprawne zgodne z układem sąsiednich pól.",
            "en": "Create realistic farmland consistent with neighboring fields.",
        },
        "instruction": (
            "Create realistic agricultural land following nearby field boundaries, crop-row direction, cultivation texture, "
            "seasonal color and tractor-track patterns."
        ),
        "avoid": "Avoid urban objects and crop patterns inconsistent with adjacent fields.",
    },
    "bare_ground": {
        "labels": {"pl": "Grunt / ziemia", "en": "Bare ground / soil"},
        "suggestions": {
            "pl": "Odtwórz realistyczny grunt lub odsłoniętą ziemię zgodną z terenem.",
            "en": "Create realistic bare ground or exposed soil matching the terrain.",
        },
        "instruction": (
            "Create realistic bare soil, disturbed ground or natural earth matching local moisture, color, track patterns, "
            "vegetation transitions and surface roughness."
        ),
        "avoid": "Avoid perfectly smooth uniform fills.",
    },
    "water": {
        "labels": {"pl": "Woda / zbiornik", "en": "Water / pond"},
        "suggestions": {
            "pl": "Stwórz realistyczną powierzchnię wody lub niewielki zbiornik dopasowany do terenu.",
            "en": "Create realistic water or a small pond matching the terrain.",
        },
        "instruction": (
            "Create realistic water or a small water body with shoreline geometry, tone, reflectance and surrounding wet-edge "
            "vegetation consistent with nearby terrain and lighting."
        ),
        "avoid": "Avoid tropical blue water, dramatic reflections and perspective effects not present in the orthophoto.",
    },
    "remove_restore": {
        "labels": {"pl": "Usuń obiekt i odtwórz teren", "en": "Remove object and restore ground"},
        "suggestions": {
            "pl": "Usuń zaznaczony obiekt i odtwórz najbardziej prawdopodobne podłoże na podstawie otoczenia.",
            "en": "Remove the selected object and reconstruct the most plausible ground from its surroundings.",
        },
        "instruction": (
            "Remove the existing object inside the mask and reconstruct the most plausible underlying land cover or surface "
            "by extending patterns, geometry, vegetation, pavement or soil visible around the mask."
        ),
        "avoid": "Do not invent a new unrelated object. Prioritize continuation of surrounding land cover.",
    },
}


def preset_ids():
    return list(PRESETS.keys())


def preset_label(preset_id, lang="pl"):
    data = PRESETS.get(preset_id, PRESETS["custom"])
    return data["labels"].get(lang, data["labels"]["en"])


def preset_suggestion(preset_id, lang="pl"):
    data = PRESETS.get(preset_id, PRESETS["custom"])
    return data["suggestions"].get(lang, data["suggestions"]["en"])


def matching_label(mode_id, lang="pl"):
    data = MATCHING_MODES.get(mode_id, MATCHING_MODES["strict"])
    return data["labels"].get(lang, data["labels"]["en"])


def build_edit_prompt(preset_id, user_instruction, matching_mode="strict", extra_constraints=""):
    preset = PRESETS.get(preset_id, PRESETS["custom"])
    matching = MATCHING_MODES.get(matching_mode, MATCHING_MODES["strict"])

    parts = [
        ORTHO_BASE_PROMPT_EN,
        "\nSOURCE MATCHING MODE:\n" + matching["instruction"],
    ]

    if preset.get("instruction"):
        parts.append("\nPRESET-SPECIFIC GUIDANCE:\n" + preset["instruction"])

    if user_instruction and user_instruction.strip():
        parts.append("\nUSER REQUEST:\n" + user_instruction.strip())

    constraints = [ORTHO_NEGATIVE_BASE_EN]
    if preset.get("avoid"):
        constraints.append(preset["avoid"])
    if extra_constraints and extra_constraints.strip():
        constraints.append(extra_constraints.strip())

    parts.append("\nCONSTRAINTS / AVOID:\n" + "\n".join(constraints))
    return "\n".join(parts).strip()
