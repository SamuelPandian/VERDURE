"""Shared label helpers.

PlantVillage class folders are named like:
    Tomato___Late_blight
    Apple___healthy
    Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot

Indian medicinal dataset folders look like:
    Mango diseased (P0b)
    Mango healthy (P0a)
    Alstonia Scholaris diseased (P2a)

Zenodo rice dataset folders (after remapping from numeric):
    Rice___Bacterial_Leaf_Blight
    Rice___Normal

so a single N-way classifier already encodes BOTH the species and the
health condition. We just split the folder name on '___' or parse the
Indian format to get clean (species, condition, is_healthy) tuples.
"""

import re

SEP = "___"
BACKGROUND_CLASS = "__background__"

# Indian medicinal: "Species diseased/healthy (Pxx)"
_INDIAN_RE = re.compile(
    r"^(.+?)\s+(diseased|healthy)\s*\(P\w+\)$", re.IGNORECASE
)

# Conditions that mean "healthy" even without the word "healthy"
_HEALTHY_CONDITIONS = {"normal", "healthy"}


def _tidy(s: str) -> str:
    s = s.replace("_", " ").strip()
    s = " ".join(s.split())
    return s


def species_name(class_name: str) -> str:
    """Pretty-print a bare species folder name.

    Leafsnap uses botanical snake_case: 'abies_concolor' -> 'Abies concolor'
    (genus capitalised, species epithet lower, as binomial nomenclature wants).
    """
    s = _tidy(class_name)
    if not s:
        return class_name
    parts = s.split()
    return " ".join([parts[0].capitalize()] + [p.lower() for p in parts[1:]])


def parse_label(class_name: str):
    """Parse any class name into (species, condition, is_healthy).

    Handles:
      'Tomato___Late_blight'            -> ('Tomato', 'Late blight', False)
      'Apple___healthy'                 -> ('Apple', 'Healthy', True)
      'abies_concolor'                  -> ('Abies concolor', 'unknown', False)
      '__background__'                  -> ('Background', 'unknown', False)
      'Mango diseased (P0b)'            -> ('Mango', 'Diseased', False)
      'Mango healthy (P0a)'             -> ('Mango', 'Healthy', True)
      'Alstonia Scholaris diseased (P2a)' -> ('Alstonia Scholaris', 'Diseased', False)
      'Rice___Bacterial_Leaf_Blight'    -> ('Rice', 'Bacterial Leaf Blight', False)
      'Rice___Normal'                   -> ('Rice', 'Normal', True)
      'Rice___Tungro'                   -> ('Rice', 'Tungro', False)

    Returns (species: str, condition: str, is_healthy: bool).
    """
    if class_name == "__background__":
        return "Background", "unknown", False

    # Indian medicinal dataset: "Mango diseased (P0b)" / "Mango healthy (P0a)"
    m = _INDIAN_RE.match(class_name)
    if m:
        species = m.group(1).strip()
        cond_raw = m.group(2).strip().lower()
        is_healthy = cond_raw == "healthy"
        condition = "Healthy" if is_healthy else "Diseased"
        return species, condition, is_healthy

    # PlantVillage / Zenodo rice: "Species___Condition"
    if SEP in class_name:
        species, condition = class_name.split(SEP, 1)
        species = _tidy(species)
        condition = _tidy(condition)
    else:
        # Leafsnap bare species name
        species = species_name(class_name)
        condition = "unknown"

    is_healthy = condition.lower() in _HEALTHY_CONDITIONS
    if condition.lower() == "healthy":
        condition = "Healthy"
    elif condition.lower() == "normal":
        condition = "Normal"  # keep the domain-specific term

    return species, condition, is_healthy


def pretty(class_name: str) -> str:
    """Human-readable label: 'Rice - Bacterial Leaf Blight'."""
    species, condition, _ = parse_label(class_name)
    return f"{species} - {condition}"


if __name__ == "__main__":
    tests = [
        "Tomato___Late_blight",
        "Apple___healthy",
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Orange___Haunglongbing_(Citrus_greening)",
        "abies_concolor",
        "quercus_rubra",
        "__background__",
        "Mango diseased (P0b)",
        "Mango healthy (P0a)",
        "Alstonia Scholaris diseased (P2a)",
        "Pongamia Pinnata healthy (P7a)",
        "Rice___Bacterial_Leaf_Blight",
        "Rice___Normal",
        "Rice___Tungro",
        "Rice___Blast",
    ]
    for c in tests:
        sp, cond, healthy = parse_label(c)
        print(f"{c:55s} -> {pretty(c):35s}  (healthy={healthy})")
