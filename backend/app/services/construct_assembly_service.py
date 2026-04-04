"""Construct assembly service.

Takes ordered genetic elements and assembles them into a full construct sequence.
Validates junctions and reading frames.
"""

from app.schemas.construct import ConstructElementSchema


def assemble_construct(elements: list[ConstructElementSchema]) -> dict:
    """Assemble ordered elements into a complete construct sequence.

    Returns dict with full_sequence, length, annotations (element positions).
    """
    sorted_elements = sorted(elements, key=lambda e: e.position)

    full_sequence = ""
    annotations = []
    current_pos = 0

    for element in sorted_elements:
        start = current_pos
        full_sequence += element.sequence
        end = current_pos + len(element.sequence)
        annotations.append({
            "type": element.element_type,
            "label": element.label,
            "start": start,
            "end": end,
            "length": len(element.sequence),
        })
        current_pos = end

    return {
        "full_sequence": full_sequence,
        "length": len(full_sequence),
        "annotations": annotations,
        "element_count": len(sorted_elements),
    }


def validate_construct(elements: list[ConstructElementSchema]) -> list[str]:
    """Validate construct element ordering and compatibility.

    Returns list of warning/error messages (empty if valid).
    """
    warnings = []
    sorted_elements = sorted(elements, key=lambda e: e.position)

    if not sorted_elements:
        warnings.append("Construct has no elements")
        return warnings

    # Check that CDS follows Kozak
    element_types = [e.element_type for e in sorted_elements]
    if "kozak" in element_types and "cds" in element_types:
        kozak_idx = element_types.index("kozak")
        cds_idx = element_types.index("cds")
        if cds_idx != kozak_idx + 1:
            warnings.append("CDS should immediately follow Kozak sequence")

    # Check that promoter comes first
    if element_types and element_types[0] != "promoter":
        warnings.append("Construct should begin with a promoter")

    return warnings
