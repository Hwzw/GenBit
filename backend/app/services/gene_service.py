"""Gene search and retrieval service. Orchestrates NCBI client calls with Redis caching."""

from app.clients import ncbi_client
from app.schemas.gene import GeneDetail, GeneSearchResult, GeneSequence


async def search_genes(
    query: str, organism: str | None = None, limit: int = 20
) -> list[GeneSearchResult]:
    results = await ncbi_client.search_genes(query, organism=organism, limit=limit)
    gene_ids = results.get("IdList", [])

    search_results = []
    for gene_id in gene_ids:
        summary = await ncbi_client.esummary(db="gene", id=gene_id)
        # Parse summary into GeneSearchResult
        # TODO: implement full parsing of NCBI summary response
        doc_sums = summary.get("DocumentSummarySet", {}).get("DocumentSummary", [])
        if doc_sums:
            doc = doc_sums[0]
            search_results.append(
                GeneSearchResult(
                    gene_id=gene_id,
                    symbol=doc.get("Name", ""),
                    description=doc.get("Description", ""),
                    organism=doc.get("Organism", {}).get("ScientificName", ""),
                    tax_id=doc.get("Organism", {}).get("TaxID"),
                )
            )
    return search_results


async def get_gene(gene_id: str) -> GeneDetail:
    """Fetch detailed gene information from NCBI."""
    # TODO: implement full gene detail retrieval
    raise NotImplementedError


async def get_gene_sequence(gene_id: str, seq_type: str = "cds") -> GeneSequence:
    """Fetch gene coding sequence from NCBI Nucleotide."""
    # TODO: implement sequence retrieval
    raise NotImplementedError
