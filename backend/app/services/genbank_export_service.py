"""GenBank (.gb) export for constructs.

Builds a BioPython SeqRecord from an assembled construct and serializes it
to the GenBank flat-file format that Benchling imports natively.
"""

from __future__ import annotations

import io
import re
from datetime import datetime, timezone

from Bio.Seq import Seq
from Bio.SeqFeature import FeatureLocation, SeqFeature
from Bio.SeqIO import write as seqio_write
from Bio.SeqRecord import SeqRecord

from app.models.construct import Construct
from app.models.construct_element import ElementType


_FEATURE_KEY_BY_TYPE = {
    ElementType.PROMOTER.value: "promoter",
    ElementType.KOZAK.value: "regulatory",
    ElementType.CDS.value: "CDS",
    ElementType.STOP_CODON.value: "misc_feature",
    ElementType.TERMINATOR.value: "terminator",
    ElementType.TAG.value: "misc_feature",
    ElementType.CUSTOM.value: "misc_feature",
}

_LOCUS_MAX = 16
_FILENAME_MAX = 64


def build_genbank(construct: Construct, assembly: dict) -> str:
    """Render a construct + its assembly output as a GenBank flat-file string.

    `assembly` is the dict returned by
    `construct_assembly_service.assemble_construct`: must contain
    `full_sequence`, `annotations` (list with type/label/start/end), and
    optionally `warnings`.
    """
    sequence = assembly["full_sequence"]
    annotations = assembly.get("annotations", [])
    warnings = assembly.get("warnings", [])

    record = SeqRecord(
        Seq(sequence),
        id=_sanitize_locus(construct.name),
        name=_sanitize_locus(construct.name),
        description=construct.name,
    )
    record.annotations = {
        "molecule_type": "DNA",
        "topology": "linear",
        "date": datetime.now(timezone.utc).strftime("%d-%b-%Y").upper(),
    }
    if warnings:
        record.annotations["comment"] = "GenBit assembly warnings:\n" + "\n".join(warnings)

    source_quals: dict[str, list[str]] = {"mol_type": ["genomic DNA"]}
    if construct.organism_tax_id:
        source_quals["db_xref"] = [f"taxon:{construct.organism_tax_id}"]
    record.features.append(
        SeqFeature(
            FeatureLocation(0, len(sequence), strand=1),
            type="source",
            qualifiers=source_quals,
        )
    )

    first_cds_start = next(
        (a["start"] for a in annotations if a["type"] == ElementType.CDS.value),
        None,
    )

    for annot in annotations:
        record.features.append(
            _build_feature(annot, full_sequence=sequence, first_cds_start=first_cds_start)
        )

    buf = io.StringIO()
    seqio_write(record, buf, "genbank")
    return buf.getvalue()


def sanitize_filename(name: str) -> str:
    """Produce a safe filename stem for a construct (no extension)."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._-")
    if not cleaned:
        cleaned = "construct"
    return cleaned[:_FILENAME_MAX]


def _sanitize_locus(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", name).strip("_")
    if not cleaned:
        cleaned = "CONSTRUCT"
    return cleaned[:_LOCUS_MAX].upper()


def _build_feature(
    annot: dict, *, full_sequence: str, first_cds_start: int | None
) -> SeqFeature:
    element_type = annot["type"]
    label = annot["label"]

    feature_key = _feature_key_for(element_type, annot, first_cds_start)
    qualifiers: dict[str, list[str]] = {
        "label": [label],
        "note": [f"genbit:{element_type}"],
    }

    if element_type == ElementType.KOZAK.value:
        qualifiers["regulatory_class"] = ["other"]
    elif element_type == ElementType.CDS.value:
        qualifiers["gene"] = [label]
        cds_seq = full_sequence[annot["start"]:annot["end"]]
        usable_len = len(cds_seq) - (len(cds_seq) % 3)
        if usable_len >= 3:
            try:
                protein = str(Seq(cds_seq[:usable_len]).translate(table=1, to_stop=False))
                qualifiers["translation"] = [protein.rstrip("*")]
            except Exception:
                pass

    return SeqFeature(
        FeatureLocation(annot["start"], annot["end"], strand=1),
        type=feature_key,
        qualifiers=qualifiers,
    )


def _feature_key_for(
    element_type: str, annot: dict, first_cds_start: int | None
) -> str:
    if element_type == ElementType.UTR.value:
        if first_cds_start is not None and annot["end"] <= first_cds_start:
            return "5'UTR"
        return "3'UTR"
    return _FEATURE_KEY_BY_TYPE.get(element_type, "misc_feature")
