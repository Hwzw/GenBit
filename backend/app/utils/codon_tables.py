"""Helpers for codon usage table loading and CAI calculation."""

import math

import python_codon_tables as pct


def get_available_organisms() -> list[str]:
    """List all organisms with available codon usage tables."""
    return pct.get_all_available_codons_tables()


def load_codon_table(organism_name: str) -> dict:
    """Load a codon usage table by organism name."""
    return pct.get_codons_table(organism_name)


def calculate_relative_adaptiveness(codon_table: dict) -> dict[str, float]:
    """Calculate relative adaptiveness (w) for each codon.

    w(codon) = frequency(codon) / max_frequency(synonymous codons)
    """
    w_values = {}
    for _aa, codons in codon_table.items():
        max_freq = max(codons.values()) if codons else 1.0
        for codon, freq in codons.items():
            w_values[codon] = freq / max_freq if max_freq > 0 else 0.0
    return w_values


def calculate_cai(dna_sequence: str, codon_table: dict) -> float:
    """Calculate Codon Adaptation Index for a DNA sequence.

    CAI = geometric mean of relative adaptiveness values for all codons.
    """
    w_values = calculate_relative_adaptiveness(codon_table)

    codons = [dna_sequence[i : i + 3].upper() for i in range(0, len(dna_sequence) - 2, 3)]
    codons = [c for c in codons if len(c) == 3]

    if not codons:
        return 0.0

    log_sum = 0.0
    valid_count = 0
    for codon in codons:
        w = w_values.get(codon, 0.0)
        if w > 0:
            log_sum += math.log(w)
            valid_count += 1

    if valid_count == 0:
        return 0.0

    return math.exp(log_sum / valid_count)
