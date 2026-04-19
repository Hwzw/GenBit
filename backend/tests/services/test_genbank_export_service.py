"""Tests for GenBank export service."""

import io
import uuid
from types import SimpleNamespace

from Bio import SeqIO
from Bio.Seq import Seq

from app.schemas.construct import ConstructElementSchema
from app.services.construct_assembly_service import assemble_construct
from app.services.genbank_export_service import (
    build_genbank,
    sanitize_filename,
)


def _construct(name: str = "Demo Construct", organism_tax_id: int | None = None):
    """Build a lightweight Construct-like stand-in. Only build_genbank's
    attribute access matters here, so a SimpleNamespace is enough."""
    return SimpleNamespace(
        id=uuid.uuid4(),
        name=name,
        organism_tax_id=organism_tax_id,
    )


def _roundtrip(gb: str):
    return SeqIO.read(io.StringIO(gb), "genbank")


def test_build_genbank_roundtrips_sequence_and_features():
    elements = [
        ConstructElementSchema(element_type="promoter", label="CMV", sequence="AAAA", position=0),
        ConstructElementSchema(element_type="kozak", label="Kozak", sequence="GCCACCATGG", position=1),
        ConstructElementSchema(element_type="cds", label="GFP", sequence="ATGCCCGGG", position=2),
        ConstructElementSchema(element_type="terminator", label="bGH", sequence="TTTT", position=3),
    ]
    assembly = assemble_construct(elements)
    gb = build_genbank(_construct(), assembly)
    record = _roundtrip(gb)

    assert str(record.seq) == assembly["full_sequence"]

    types_by_label = {
        f.qualifiers["label"][0]: f.type
        for f in record.features
        if f.type != "source" and "label" in f.qualifiers
    }
    assert types_by_label["CMV"] == "promoter"
    assert types_by_label["Kozak"] == "regulatory"
    assert types_by_label["GFP"] == "CDS"
    assert types_by_label["bGH"] == "terminator"
    assert any(f.type == "misc_feature" for f in record.features)  # injected stop codon


def test_cds_translation_qualifier_matches_biopython():
    elements = [
        ConstructElementSchema(element_type="cds", label="P", sequence="ATGAAACGC", position=0),
    ]
    assembly = assemble_construct(elements)
    gb = build_genbank(_construct(), assembly)
    record = _roundtrip(gb)

    cds = next(f for f in record.features if f.type == "CDS")
    cds_seq = str(record.seq[int(cds.location.start):int(cds.location.end)])
    expected = str(Seq(cds_seq[: len(cds_seq) - len(cds_seq) % 3]).translate(table=1, to_stop=False)).rstrip("*")
    assert cds.qualifiers["translation"][0] == expected
    assert cds.qualifiers["gene"][0] == "P"


def test_utr_before_cds_is_five_prime_after_is_three_prime():
    elements = [
        ConstructElementSchema(element_type="promoter", label="CMV", sequence="AAAA", position=0),
        ConstructElementSchema(element_type="utr", label="5UTR", sequence="GGGG", position=1),
        ConstructElementSchema(element_type="cds", label="CDS1", sequence="ATGCCC", position=2),
        ConstructElementSchema(element_type="utr", label="3UTR", sequence="CCCC", position=3),
    ]
    assembly = assemble_construct(elements)
    gb = build_genbank(_construct(), assembly)
    record = _roundtrip(gb)

    utr_types = {
        f.qualifiers["label"][0]: f.type
        for f in record.features
        if f.qualifiers.get("label", [""])[0] in ("5UTR", "3UTR")
    }
    assert utr_types["5UTR"] == "5'UTR"
    assert utr_types["3UTR"] == "3'UTR"


def test_organism_tax_id_produces_db_xref_on_source():
    elements = [
        ConstructElementSchema(element_type="promoter", label="P", sequence="AAAA", position=0),
    ]
    assembly = assemble_construct(elements)
    gb = build_genbank(_construct(organism_tax_id=9606), assembly)
    record = _roundtrip(gb)

    source = next(f for f in record.features if f.type == "source")
    assert "taxon:9606" in source.qualifiers.get("db_xref", [])


def test_warnings_land_in_comment_block():
    # Force a warning: CDS without ATG start.
    elements = [
        ConstructElementSchema(element_type="promoter", label="P", sequence="AAAA", position=0),
        ConstructElementSchema(element_type="cds", label="C", sequence="CCCGGG", position=1),
    ]
    assembly = assemble_construct(elements)
    assert assembly["warnings"]
    gb = build_genbank(_construct(), assembly)
    assert "GenBit assembly warnings" in gb
    assert "injected" in gb.lower()


def test_kozak_regulatory_class_qualifier():
    elements = [
        ConstructElementSchema(element_type="kozak", label="K", sequence="GCCACC", position=0),
    ]
    assembly = assemble_construct(elements)
    gb = build_genbank(_construct(), assembly)
    record = _roundtrip(gb)

    kozak = next(f for f in record.features if f.type == "regulatory")
    assert kozak.qualifiers["regulatory_class"] == ["other"]


def test_locus_name_sanitization():
    elements = [
        ConstructElementSchema(element_type="promoter", label="P", sequence="AAAA", position=0),
    ]
    assembly = assemble_construct(elements)
    gb = build_genbank(_construct(name="My Construct: v2 / test!"), assembly)
    record = _roundtrip(gb)
    # LOCUS name: alphanumeric + underscores, uppercase, <= 16 chars
    assert record.name.isascii()
    assert len(record.name) <= 16
    assert record.name == record.name.upper()
    assert all(c.isalnum() or c == "_" for c in record.name)


def test_sanitize_filename():
    assert sanitize_filename("my construct") == "my_construct"
    assert sanitize_filename("weird/../name") == "weird_.._name"
    assert sanitize_filename("") == "construct"
    assert sanitize_filename("abc!@#$%^&*()") == "abc"
    assert len(sanitize_filename("x" * 200)) <= 64


def test_feature_count_matches_annotations_plus_source():
    elements = [
        ConstructElementSchema(element_type="promoter", label="P", sequence="AAAA", position=0),
        ConstructElementSchema(element_type="cds", label="C", sequence="ATGCCC", position=1),
        ConstructElementSchema(element_type="terminator", label="T", sequence="TTTT", position=2),
    ]
    assembly = assemble_construct(elements)
    gb = build_genbank(_construct(), assembly)
    record = _roundtrip(gb)

    non_source = [f for f in record.features if f.type != "source"]
    assert len(non_source) == len(assembly["annotations"])
    assert any(f.type == "source" for f in record.features)
