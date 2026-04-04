from fastapi import APIRouter, Query

from app.schemas.protein import ProteinSearchResult
from app.services import protein_service

router = APIRouter()


@router.get("/search", response_model=list[ProteinSearchResult])
async def search_proteins(
    q: str = Query(..., description="Search query"),
    organism: str | None = Query(None, description="Filter by organism"),
    limit: int = Query(20, ge=1, le=100),
):
    return await protein_service.search_proteins(q, organism=organism, limit=limit)


@router.get("/{accession}")
async def get_protein(accession: str):
    return await protein_service.get_protein(accession)


@router.get("/{accession}/sequence")
async def get_protein_sequence(accession: str):
    return await protein_service.get_protein_sequence(accession)
