"""Kozak sequence generation for different organisms.

Kozak consensus varies by species:
- Vertebrates: GCC(A/G)CCAUGG  -> GCCACCATGG (strong) or GCCGCCATGG
- Yeast (S. cerevisiae): (A/Y)A(A/U)A(A/U)AAUGUCU
- Plants: AACAAUGGC
- Drosophila: C/AAAA/CAUGG
"""

# Organism-specific Kozak consensus sequences
KOZAK_CONSENSUS = {
    # Vertebrates
    "vertebrate": {"consensus": "GCCACCATGG", "notes": "Strong Kozak (Kozak, 1987)"},
    9606: {"consensus": "GCCACCATGG", "notes": "Human - strong vertebrate Kozak"},
    10090: {"consensus": "GCCACCATGG", "notes": "Mouse - strong vertebrate Kozak"},
    10116: {"consensus": "GCCACCATGG", "notes": "Rat - strong vertebrate Kozak"},
    9913: {"consensus": "GCCACCATGG", "notes": "Bovine - strong vertebrate Kozak"},
    # Yeast
    4932: {"consensus": "AAAAAUGTCT", "notes": "S. cerevisiae Kozak-like context"},
    # Plants
    3702: {"consensus": "AACAATGGC", "notes": "A. thaliana translation initiation context"},
    # Drosophila
    7227: {"consensus": "CAACATGG", "notes": "D. melanogaster Kozak"},
    # E. coli (uses Shine-Dalgarno, not Kozak)
    562: {"consensus": "AGGAGGATGG", "notes": "E. coli Shine-Dalgarno + start codon"},
}


def generate_kozak(organism_tax_id: int, start_codon: str = "ATG") -> dict:
    """Generate appropriate Kozak/initiation sequence for target organism.

    Returns dict with consensus, sequence, organism info, and notes.
    """
    # Look up by exact tax_id first
    if organism_tax_id in KOZAK_CONSENSUS:
        entry = KOZAK_CONSENSUS[organism_tax_id]
    else:
        # Default to vertebrate Kozak
        entry = KOZAK_CONSENSUS["vertebrate"]

    consensus = entry["consensus"]
    # Replace the ATG in consensus with user-specified start codon if different
    if start_codon != "ATG":
        consensus = consensus.replace("ATG", start_codon)

    return {
        "organism_tax_id": organism_tax_id,
        "consensus": entry["consensus"],
        "sequence": consensus,
        "notes": entry["notes"],
    }
