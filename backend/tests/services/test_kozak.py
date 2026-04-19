"""Tests for Kozak sequence generation."""

import pytest

from app.services.kozak_service import generate_kozak


def test_human_kozak():
    result = generate_kozak(organism_tax_id=9606)
    assert result["consensus"] == "gccRccATGG"
    assert "ATG" in result["sequence"].upper()


def test_yeast_kozak():
    result = generate_kozak(organism_tax_id=4932)
    assert "ATG" in result["sequence"]
    assert result["organism_tax_id"] == 4932


def test_unknown_organism_defaults_to_vertebrate():
    result = generate_kozak(organism_tax_id=99999)
    assert result["consensus"] == "GCCACCATGG"


def test_plant_clade_alias_uses_terrestrial_plants():
    """Regression: arabidopsis tax_id 3701 wasn't mapped, so users couldn't easily
    get the plant Kozak. The `plant` clade alias bypasses tax_id lookup entirely."""
    result = generate_kozak(clade="plant")
    assert "Terrestrial plants" in result["organism"]
    assert "ATG" in result["sequence"].upper()


def test_vertebrate_clade_alias():
    result = generate_kozak(clade="vertebrate")
    assert result["consensus"] == "gccRccATGG"


def test_clade_alias_is_case_and_punctuation_insensitive():
    a = generate_kozak(clade="Plant")
    b = generate_kozak(clade="plants")
    assert a["consensus"] == b["consensus"]


def test_ecoli_clade_returns_shine_dalgarno():
    result = generate_kozak(clade="ecoli")
    assert result["organism"] == "E. coli"
    assert "Shine-Dalgarno" in result["notes"]


def test_bsubtilis_tax_id_returns_shine_dalgarno():
    result = generate_kozak(organism_tax_id=1423)
    assert result["organism"] == "E. coli"
    assert "Shine-Dalgarno" in result["notes"]


def test_archaeal_tax_id_returns_shine_dalgarno():
    result = generate_kozak(organism_tax_id=2190)
    assert result["organism"] == "E. coli"
    assert "Shine-Dalgarno" in result["notes"]


def test_unknown_clade_raises():
    with pytest.raises(ValueError, match="Unknown clade"):
        generate_kozak(clade="martian")


def test_missing_both_args_raises():
    with pytest.raises(ValueError, match="Must provide"):
        generate_kozak()
