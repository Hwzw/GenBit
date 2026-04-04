"""Protein search and retrieval. Tries UniProt first, falls back to NCBI Protein."""

from app.clients import ncbi_client
from app.clients.uniprot_client import uniprot_client
from app.schemas.protein import ProteinDetail, ProteinSearchResult, ProteinSequence


async def search_proteins(
    query: str, organism: str | None = None, limit: int = 20
) -> list[ProteinSearchResult]:
    """Search UniProt first, then NCBI Protein."""
    results = []

    # Try UniProt
    try:
        uniprot_data = await uniprot_client.search_proteins(query, organism=organism, limit=limit)
        for entry in uniprot_data.get("results", []):
            results.append(
                ProteinSearchResult(
                    accession=entry.get("primaryAccession", ""),
                    name=entry.get("proteinDescription", {})
                    .get("recommendedName", {})
                    .get("fullName", {})
                    .get("value", ""),
                    organism=entry.get("organism", {}).get("scientificName", ""),
                    length=entry.get("sequence", {}).get("length", 0),
                    source="uniprot",
                )
            )
    except Exception:
        pass  # Fall through to NCBI

    # Supplement with NCBI if needed
    if len(results) < limit:
        ncbi_data = await ncbi_client.search_proteins(
            query, organism=organism, limit=limit - len(results)
        )
        for protein_id in ncbi_data.get("IdList", []):
            summary = await ncbi_client.esummary(db="protein", id=protein_id)
            # TODO: parse NCBI protein summary
            _ = summary
    return results


async def get_protein(accession: str) -> ProteinDetail:
    """Fetch protein detail from UniProt or NCBI."""
    # TODO: implement
    raise NotImplementedError


async def get_protein_sequence(accession: str) -> ProteinSequence:
    """Fetch protein amino acid sequence."""
    # TODO: implement
    raise NotImplementedError
