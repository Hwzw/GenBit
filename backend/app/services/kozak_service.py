"""Kozak sequence generation for different organisms.

Loads organism-specific Kozak consensus sequences from CSV data file.
"""

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

# Load Kozak data from CSV at import time
_KOZAK_DATA: list[dict] = []


def _load_kozak_data() -> list[dict]:
    global _KOZAK_DATA
    if _KOZAK_DATA:
        return _KOZAK_DATA

    csv_path = DATA_DIR / "kozak_sequences.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Collect non-empty combinations
            combinations = []
            for i in range(1, 9):
                val = row.get(f"Combination {i}", "").strip()
                if val and not val.startswith("Lots of"):
                    combinations.append(val.upper())

            _KOZAK_DATA.append({
                "organism": row["Organism"].strip(),
                "clade": row.get("Clade/Group", "").strip(),
                "organism_type": row.get("Organism Type", "").strip(),
                "consensus": row.get("Kozak Consensus", "").strip(),
                "combinations": combinations,
            })

    return _KOZAK_DATA


# Map short clade aliases (typed by the user) to CSV organism names.
# `None` means the alias resolves to a non-Kozak system (Shine-Dalgarno).
_CLADE_ALIASES: dict[str, str | None] = {
    "vertebrate": "Vertebrate",
    "vertebrates": "Vertebrate",
    "mammal": "Vertebrate",
    "mammals": "Vertebrate",
    "human": "Vertebrate",
    "mouse": "Vertebrate",
    "rat": "Vertebrate",
    "fish": "Vertebrate",
    "zebrafish": "Vertebrate",
    "bird": "Vertebrate",
    "chicken": "Vertebrate",
    "fly": "Fruit fly",
    "flies": "Fruit fly",
    "drosophila": "Fruit fly",
    "insect": "Fruit fly",
    "yeast": "Budding yeast",
    "scerevisiae": "Budding yeast",
    "cerevisiae": "Budding yeast",
    "klactis": "Budding yeast",
    "fungus": "Budding yeast",
    "fungi": "Budding yeast",
    "plant": "Terrestrial plants",
    "plants": "Terrestrial plants",
    "arabidopsis": "Terrestrial plants",
    "maize": "Terrestrial plants",
    "rice": "Terrestrial plants",
    "wheat": "Terrestrial plants",
    "embryophyte": "Terrestrial plants",
    "algae": "Microalga",
    "alga": "Microalga",
    "chlamydomonas": "Microalga",
    "greenalgae": "Microalga",
    "slimemold": "Slime mold",
    "dictyostelium": "Slime mold",
    "ciliate": "Ciliate",
    "paramecium": "Ciliate",
    "tetrahymena": "Ciliate",
    "malaria": "Malarial",
    "malarial": "Malarial",
    "plasmodium": "Malarial",
    "toxoplasma": "Toxoplasma",
    "trypanosome": "Trypanosomatidae",
    "trypanosoma": "Trypanosomatidae",
    "leishmania": "Trypanosomatidae",
    "kinetoplastid": "Trypanosomatidae",
    # Prokaryotes use Shine-Dalgarno, not a Kozak sequence.
    "ecoli": None,
    "bacteria": None,
    "bacterium": None,
    "prokaryote": None,
    "prokaryotic": None,
}


def _normalize_clade(name: str) -> str:
    return "".join(c for c in name.lower() if c.isalnum())


# Map common tax IDs to CSV organism names for lookup
_TAX_ID_MAP = {
    # Vertebrates
    9606: "Vertebrate",
    10090: "Vertebrate",
    10116: "Vertebrate",
    9913: "Vertebrate",
    9031: "Vertebrate",
    7955: "Vertebrate",
    # Drosophila
    7227: "Fruit fly",
    # Yeast
    4932: "Budding yeast",
    28985: "Budding yeast",  # K. lactis — similar Kozak to S. cerevisiae
    # Plants
    3702: "Terrestrial plants",
    4577: "Terrestrial plants",  # Zea mays
    4530: "Terrestrial plants",  # Oryza sativa
    # Green algae
    3055: "Microalga",  # Chlamydomonas
    # Slime mold
    44689: "Slime mold",
    # Plasmodium
    5833: "Malarial",
    36329: "Malarial",
    # Toxoplasma
    5811: "Toxoplasma",
    # Ciliates
    5888: "Ciliate",  # Paramecium
    5911: "Ciliate",  # Tetrahymena
    # Trypanosomatidae
    5691: "Trypanosomatidae",  # Trypanosoma
    5660: "Trypanosomatidae",  # Leishmania
    # Prokaryotes — use Shine-Dalgarno, not Kozak
    562: None,       # E. coli
    83333: None,     # E. coli K-12 (strain-level)
    1423: None,      # Bacillus subtilis
    287: None,       # Pseudomonas aeruginosa
    1358: None,      # Lactococcus lactis
    1773: None,      # Mycobacterium tuberculosis
    1902: None,      # Streptomyces coelicolor
    1718: None,      # Corynebacterium glutamicum
    1148: None,      # Synechocystis sp. PCC 6803
    # Archaea — use SD-like ribosome binding; SD consensus is a reasonable approximation
    2190: None,      # Methanocaldococcus jannaschii
    2287: None,      # Saccharolobus solfataricus
    2246: None,      # Haloferax volcanii
    64091: None,     # Halobacterium salinarum NRC-1
}


def _find_kozak_entry(organism_tax_id: int) -> dict | None:
    """Find the best matching Kozak entry for a given tax ID."""
    data = _load_kozak_data()

    # Check tax ID map first
    search_term = _TAX_ID_MAP.get(organism_tax_id)
    if search_term is None and organism_tax_id in _TAX_ID_MAP:
        # Explicitly mapped to None (e.g., E. coli)
        return None

    if search_term:
        for entry in data:
            if search_term.lower() in entry["organism"].lower():
                return entry

    # No match found — return None so caller can warn about defaulting
    return None


# Shine-Dalgarno for prokaryotes
_SHINE_DALGARNO = {
    "consensus": "AGGAGGATGG",
    "notes": "E. coli Shine-Dalgarno + start codon",
    "organism": "E. coli",
}


def _shine_dalgarno_result(start_codon: str, organism_tax_id: int | None = None) -> dict:
    sequence = _SHINE_DALGARNO["consensus"]
    if start_codon != "ATG":
        idx = sequence.rfind("ATG")
        if idx >= 0:
            sequence = sequence[:idx] + start_codon + sequence[idx + 3:]
    return {
        "organism_tax_id": organism_tax_id,
        "organism": _SHINE_DALGARNO["organism"],
        "consensus": _SHINE_DALGARNO["consensus"],
        "sequence": sequence,
        "notes": _SHINE_DALGARNO["notes"],
    }


def list_clades() -> list[str]:
    """Return the canonical clade aliases users can pass to `generate_kozak`."""
    return [
        "vertebrate", "fly", "yeast", "plant", "algae",
        "slimemold", "ciliate", "malaria", "toxoplasma",
        "trypanosome", "ecoli",
    ]


def generate_kozak(
    organism_tax_id: int | None = None,
    start_codon: str = "ATG",
    clade: str | None = None,
) -> dict:
    """Generate appropriate Kozak/initiation sequence for target organism.

    Accepts either an NCBI tax ID or a clade alias (e.g. "plant", "vertebrate").
    Returns dict with consensus, sequence, organism info, and notes.
    """
    if clade:
        key = _normalize_clade(clade)
        if key not in _CLADE_ALIASES:
            valid = ", ".join(list_clades())
            raise ValueError(f"Unknown clade '{clade}'. Try one of: {valid}")

        search_term = _CLADE_ALIASES[key]
        if search_term is None:
            return _shine_dalgarno_result(start_codon)

        entry = next(
            (e for e in _load_kozak_data() if search_term.lower() in e["organism"].lower()),
            None,
        )
        if entry is None:
            raise ValueError(f"Clade '{clade}' has no Kozak entry in the database")
        return _build_result(entry, start_codon, organism_tax_id=None)

    if organism_tax_id is None:
        raise ValueError("Must provide either organism_tax_id or clade")

    # Prokaryotes (bacteria + archaea) use Shine-Dalgarno
    if organism_tax_id in _TAX_ID_MAP and _TAX_ID_MAP[organism_tax_id] is None:
        return _shine_dalgarno_result(start_codon, organism_tax_id=organism_tax_id)

    entry = _find_kozak_entry(organism_tax_id)
    if not entry:
        # Fallback to vertebrate consensus
        return {
            "organism_tax_id": organism_tax_id,
            "organism": "Unknown (defaulting to vertebrate)",
            "consensus": "GCCACCATGG",
            "sequence": "GCCACCATGG" if start_codon == "ATG" else "GCCACC" + start_codon + "G",
            "notes": "Default vertebrate Kozak — pass a clade (e.g. 'kozak plant') to override",
        }

    return _build_result(entry, start_codon, organism_tax_id=organism_tax_id)


def _build_result(entry: dict, start_codon: str, organism_tax_id: int | None) -> dict:
    consensus = entry["consensus"]
    # Use the first concrete combination as the sequence
    if entry["combinations"]:
        sequence = entry["combinations"][0]
    else:
        sequence = consensus.upper()

    # Replace only the start codon (last ATG in Kozak context)
    if start_codon != "ATG":
        idx = sequence.upper().rfind("ATG")
        if idx >= 0:
            sequence = sequence[:idx] + start_codon + sequence[idx + 3:]

    organism_name = entry["organism"]
    return {
        "organism_tax_id": organism_tax_id,
        "organism": organism_name,
        "consensus": consensus,
        "sequence": sequence,
        "notes": f"{organism_name} Kozak consensus from {entry['clade']}",
        "combinations": entry["combinations"],
    }
