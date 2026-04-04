"""Tests for construct assembly service."""

from app.schemas.construct import ConstructElementSchema
from app.services.construct_assembly_service import assemble_construct, validate_construct


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
    assert result["full_sequence"] == "AAAAGCCACCATGGATGCCCGGG"
    assert result["element_count"] == 3
    assert len(result["annotations"]) == 3


def test_validate_missing_promoter():
    elements = [
        ConstructElementSchema(
            element_type="cds", label="CDS", sequence="ATGCCC", position=0
        ),
    ]
    warnings = validate_construct(elements)
    assert any("promoter" in w.lower() for w in warnings)
