"""Tests for restriction digest service."""

import pytest
from fastapi import HTTPException

from app.services.restriction_digest_service import digest, resolve_enzymes


def test_resolve_enzymes_case_insensitive_and_canonical():
    assert resolve_enzymes(["ecori", "BAMHI"]) == ["EcoRI", "BamHI"]


def test_resolve_enzymes_deduplicates():
    assert resolve_enzymes(["EcoRI", "ecori", "EcoRI"]) == ["EcoRI"]


def test_resolve_enzymes_unknown_raises_400():
    with pytest.raises(HTTPException) as exc:
        resolve_enzymes(["EcoRI", "NotARealEnzyme"])
    assert exc.value.status_code == 400
    assert "NotARealEnzyme" in exc.value.detail


def test_digest_single_enzyme_produces_fragments():
    # EcoRI (GAATTC) cuts after G at positions 3 and 20 (0-based)
    # Sequence layout:      idx: 012345678901234567890123456
    sequence = "AAGAATTCCCGGATCCTTTGAATTCAA"
    result = digest(sequence, ["EcoRI"])

    assert result["sequence_length"] == len(sequence)
    assert len(result["enzymes"]) == 1
    eco = result["enzymes"][0]
    assert eco["name"] == "EcoRI"
    assert eco["site"] == "GAATTC"
    assert eco["cut_count"] == 2
    assert eco["overhang"] == "5' overhang"
    assert eco["cut_positions"] == [3, 20]

    # Fragments should be: [0..3], [3..20], [20..end]
    fragments = result["fragments"]
    assert len(fragments) == 3
    assert fragments[0]["start"] == 0 and fragments[0]["end"] == 3
    assert fragments[1]["start"] == 3 and fragments[1]["end"] == 20
    assert fragments[2]["start"] == 20 and fragments[2]["end"] == len(sequence)
    # Fragments should concatenate back to the full sequence
    assert "".join(
        sequence[f["start"]:f["end"]] for f in fragments
    ) == sequence


def test_digest_multiple_enzymes_combines_cuts():
    sequence = "AAGAATTCCCGGATCCTTTGAATTCAA"
    result = digest(sequence, ["EcoRI", "BamHI"])
    # BamHI (GGATCC) cuts once in this sequence
    names = [e["name"] for e in result["enzymes"]]
    assert names == ["EcoRI", "BamHI"]
    # Combined cuts → 4 fragments (3 cuts + 1)
    assert len(result["fragments"]) == 4


def test_digest_enzyme_that_does_not_cut_warns():
    # A sequence with no EcoRI site
    sequence = "AAAACCCCGGGGTTTT"
    result = digest(sequence, ["EcoRI"])
    assert result["enzymes"][0]["cut_count"] == 0
    assert any("does not cut" in w for w in result["warnings"])
    # Single uncut fragment covering the whole sequence
    assert len(result["fragments"]) == 1
    assert result["fragments"][0]["length"] == len(sequence)


def test_digest_maps_cut_positions_to_annotation_labels():
    sequence = "AAGAATTCCCGGATCCTTTGAATTCAA"
    annotations = [
        {"type": "promoter", "label": "PromA", "start": 0, "end": 10, "length": 10},
        {"type": "cds", "label": "CDS1", "start": 10, "end": 27, "length": 17},
    ]
    result = digest(sequence, ["EcoRI"], annotations=annotations)
    eco = result["enzymes"][0]
    # EcoRI cuts at positions 3 (inside PromA) and 20 (inside CDS1)
    assert eco["feature_hits"] == ["PromA", "CDS1"]


def test_digest_empty_sequence_raises_400():
    with pytest.raises(HTTPException) as exc:
        digest("", ["EcoRI"])
    assert exc.value.status_code == 400


def test_digest_blunt_cutter_overhang_label():
    # EcoRV (GATATC) is a blunt cutter
    sequence = "AAAGATATCAAA"
    result = digest(sequence, ["EcoRV"])
    assert result["enzymes"][0]["overhang"] == "blunt"


def test_digest_fragment_sequence_preview_truncates_long_fragments():
    # 200bp of A → one fragment since nothing cuts it; preview must be truncated
    sequence = "A" * 200
    result = digest(sequence, ["EcoRI"])
    assert len(result["fragments"][0]["sequence"]) < 200
    assert "..." in result["fragments"][0]["sequence"]
