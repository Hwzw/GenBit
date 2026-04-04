from fastapi import APIRouter, Query

from app.schemas.gene import GeneSearchResult
from app.services import gene_service

router = APIRouter()


@router.get("/search", response_model=list[GeneSearchResult])
async def search_genes(
    q: str = Query(..., description="Search query"),
    organism: str | None = Query(None, description="Filter by organism"),
    limit: int = Query(20, ge=1, le=100),
):
    return await gene_service.search_genes(q, organism=organism, limit=limit)


@router.get("/{gene_id}")
async def get_gene(gene_id: str):
    return await gene_service.get_gene(gene_id)


@router.get("/{gene_id}/sequence")
async def get_gene_sequence(gene_id: str, seq_type: str = Query("cds")):
    return await gene_service.get_gene_sequence(gene_id, seq_type=seq_type)
