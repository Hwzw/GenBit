from fastapi import APIRouter

from app.schemas.optimization import OptimizationRequest, OptimizationResponse
from app.services import codon_optimization_service

router = APIRouter()


@router.post("/optimize", response_model=OptimizationResponse)
async def optimize_codons(request: OptimizationRequest):
    result = codon_optimization_service.optimize_sequence(
        protein_sequence=request.sequence,
        organism_tax_id=request.organism_tax_id,
        strategy=request.strategy,
        avoid_restriction_sites=request.avoid_restriction_sites,
        target_gc_min=request.target_gc_min,
        target_gc_max=request.target_gc_max,
        avoid_repeats=request.avoid_repeats,
    )
    return OptimizationResponse(
        job_id="00000000-0000-0000-0000-000000000000",  # TODO: async job tracking
        status="completed",
        optimized_sequence=result["optimized_sequence"],
        cai_before=result["cai_before"],
        cai_after=result["cai_after"],
        gc_content=result["gc_content_after"],
    )
