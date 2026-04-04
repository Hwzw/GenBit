from fastapi import APIRouter, Query

from app.schemas.organism import CodonTableResponse, OrganismSearchResult
from app.services import organism_service

router = APIRouter()


@router.get("/search", response_model=list[OrganismSearchResult])
async def search_organisms(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100),
):
    return await organism_service.search_organisms(q, limit=limit)


@router.get("/{tax_id}")
async def get_organism(tax_id: int):
    return await organism_service.get_organism(tax_id)


@router.get("/{tax_id}/codon-table", response_model=CodonTableResponse)
async def get_codon_table(tax_id: int):
    return organism_service.get_codon_table(tax_id)
