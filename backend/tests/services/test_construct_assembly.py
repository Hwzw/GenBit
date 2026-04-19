"""Tests for construct assembly service."""

from app.schemas.construct import ConstructElementSchema
from app.services.construct_assembly_service import assemble_construct, validate_construct

STOP_TANDEM = "TAATAGTGA"  # default ranking when no organism codon table is available


def test_assemble_basic_construct():
    elements = [
        ConstructElementSchema(
            element_type="promoter", label="CMV", sequence="AAAA", position=0
        ),
        ConstructElementSchema(
            element_type="kozak", label="Kozak", sequence="GCCACCATGG", position=1
        ),
        ConstructElementSchema(
            element_type="cds", label="GFP CDS", sequence="ATGCCCGGG", position=2
        ),
    ]
    result = assemble_construct(elements)
    assert result["full_sequence"] == "AAAAGCCACCATGCCCGGG" + STOP_TANDEM
    assert result["element_count"] == 4
    assert len(result["annotations"]) == 4
    assert result["annotations"][-1]["type"] == "stop_codon"


def test_assemble_cds_without_kozak_keeps_atg():
    """CDS not preceded by Kozak should keep its full sequence."""
    elements = [
        ConstructElementSchema(
            element_type="promoter", label="CMV", sequence="AAAA", position=0
        ),
        ConstructElementSchema(
            element_type="cds", label="GFP CDS", sequence="ATGCCCGGG", position=1
        ),
    ]
    result = assemble_construct(elements)
    assert result["full_sequence"] == "AAAAATGCCCGGG" + STOP_TANDEM


def test_assemble_two_cds_injects_single_stop_after_last():
    """Only the final CDS gets a stop element appended; CDS #1 stays clean."""
    elements = [
        ConstructElementSchema(
            element_type="promoter", label="CMV", sequence="AAAA", position=0
        ),
        ConstructElementSchema(
            element_type="cds", label="CDS1", sequence="ATGCCC", position=1
        ),
        ConstructElementSchema(
            element_type="cds", label="CDS2", sequence="ATGGGG", position=2
        ),
    ]
    result = assemble_construct(elements)

    assert result["full_sequence"] == "AAAAATGCCCATGGGG" + STOP_TANDEM
    assert result["element_count"] == 4

    stop_annots = [a for a in result["annotations"] if a["type"] == "stop_codon"]
    assert len(stop_annots) == 1
    assert stop_annots[0]["label"] == "stop-CDS2"

    # CDS1 must immediately precede CDS2, with no stop element wedged between.
    types = [a["type"] for a in result["annotations"]]
    assert types == ["promoter", "cds", "cds", "stop_codon"]


def test_assemble_no_cds_skips_stop_injection():
    elements = [
        ConstructElementSchema(
            element_type="promoter", label="CMV", sequence="AAAA", position=0
        ),
        ConstructElementSchema(
            element_type="terminator", label="T", sequence="TTTT", position=1
        ),
    ]
    result = assemble_construct(elements)
    assert result["full_sequence"] == "AAAATTTT"
    assert result["element_count"] == 2
    assert not any(a["type"] == "stop_codon" for a in result["annotations"])


def test_assemble_injects_atg_when_first_cds_missing_start_codon():
    """CDS without an ATG at its start should get a start codon prepended."""
    elements = [
        ConstructElementSchema(
            element_type="promoter", label="CMV", sequence="AAAA", position=0
        ),
        ConstructElementSchema(
            element_type="cds", label="GFP CDS", sequence="CCCGGG", position=1
        ),
    ]
    result = assemble_construct(elements)
    assert result["full_sequence"] == "AAAAATGCCCGGG" + STOP_TANDEM
    assert any("injected" in w.lower() for w in result["warnings"])
    cds_annot = next(a for a in result["annotations"] if a["type"] == "cds")
    assert cds_annot["length"] == len("ATGCCCGGG")


def test_assemble_no_injection_when_cds_already_starts_with_atg():
    elements = [
        ConstructElementSchema(
            element_type="promoter", label="CMV", sequence="AAAA", position=0
        ),
        ConstructElementSchema(
            element_type="cds", label="GFP CDS", sequence="ATGCCCGGG", position=1
        ),
    ]
    result = assemble_construct(elements)
    assert result["full_sequence"] == "AAAAATGCCCGGG" + STOP_TANDEM
    assert result["warnings"] == []


def test_assemble_no_injection_when_preceding_context_ends_in_atg():
    """If the element before the first CDS already ends in ATG, don't inject."""
    elements = [
        ConstructElementSchema(
            element_type="promoter", label="CMV", sequence="AAAATG", position=0
        ),
        ConstructElementSchema(
            element_type="cds", label="GFP CDS", sequence="CCCGGG", position=1
        ),
    ]
    result = assemble_construct(elements)
    assert result["full_sequence"] == "AAAATGCCCGGG" + STOP_TANDEM
    assert result["warnings"] == []


def test_validate_missing_promoter():
    elements = [
        ConstructElementSchema(
            element_type="cds", label="CDS", sequence="ATGCCC", position=0
        ),
    ]
    warnings = validate_construct(elements)
    assert any("promoter" in w.lower() for w in warnings)
