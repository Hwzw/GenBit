"""Organism search and codon table retrieval."""

import python_codon_tables as pct

from app.clients import ncbi_client
from app.schemas.organism import CodonTableResponse, OrganismDetail, OrganismSearchResult


async def search_organisms(query: str, limit: int = 20) -> list[OrganismSearchResult]:
    results = await ncbi_client.search_taxonomy(query, limit=limit)
    tax_ids = results.get("IdList", [])

    organisms = []
    for tax_id in tax_ids:
        detail = await ncbi_client.fetch_taxonomy(tax_id)
        if detail:
            taxon = detail[0] if isinstance(detail, list) else detail
            organisms.append(
                OrganismSearchResult(
                    tax_id=int(tax_id),
                    scientific_name=taxon.get("ScientificName", ""),
                    common_name=taxon.get("CommonName"),
                    lineage=taxon.get("Lineage"),
                )
            )
    return organisms


async def get_organism(tax_id: int) -> OrganismDetail:
    """Fetch organism details from NCBI Taxonomy."""
    # TODO: implement with caching
    raise NotImplementedError


def get_codon_table(tax_id: int) -> CodonTableResponse:
    """Get codon usage table. Tries python-codon-tables first."""
    available = pct.get_all_available_codons_tables()
    table_name = None
    for name in available:
        if str(tax_id) in name:
            table_name = name
            break

    if table_name:
        table = pct.get_codons_table(table_name)
    else:
        # Default to E. coli if organism not found
        table = pct.get_codons_table("e_coli_316407")

    return CodonTableResponse(
        organism_tax_id=tax_id,
        source="python-codon-tables",
        table=table,
    )
