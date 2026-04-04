"""Tests for sequence utility functions."""

from app.utils.sequence import (
    detect_sequence_type,
    gc_content,
    reverse_complement,
    validate_dna,
    validate_protein,
)


def test_validate_dna_valid():
    assert validate_dna("ATCGATCG") is True


def test_validate_dna_invalid():
    assert validate_dna("ATCGXYZ") is False


def test_validate_protein_valid():
    assert validate_protein("MVLSPADKTNVK") is True


def test_validate_protein_invalid():
    assert validate_protein("MVLS123") is False


def test_reverse_complement():
    assert reverse_complement("ATCG") == "CGAT"
    assert reverse_complement("AAAA") == "TTTT"


def test_gc_content():
    assert gc_content("GGCC") == 1.0
    assert gc_content("AATT") == 0.0
    assert gc_content("ATCG") == 0.5
    assert gc_content("") == 0.0


def test_detect_sequence_type():
    assert detect_sequence_type("ATCGATCG") == "dna"
    assert detect_sequence_type("MVLSPADKTNVK") == "protein"
    assert detect_sequence_type("") == "unknown"
