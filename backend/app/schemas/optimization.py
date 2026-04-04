import uuid
from enum import StrEnum

from pydantic import BaseModel


class OptimizationStrategy(StrEnum):
    FREQUENCY = "frequency"
    HARMONIZED = "harmonized"
    BALANCED = "balanced"


class OptimizationRequest(BaseModel):
    sequence: str  # protein sequence
    organism_tax_id: int
    strategy: OptimizationStrategy = OptimizationStrategy.FREQUENCY
    avoid_restriction_sites: list[str] = []
    target_gc_min: float | None = None
    target_gc_max: float | None = None
    avoid_repeats: bool = True


class OptimizationResponse(BaseModel):
    job_id: uuid.UUID
    status: str
    optimized_sequence: str | None = None
    cai_before: float | None = None
    cai_after: float | None = None
    gc_content: float | None = None
    changes_summary: dict | None = None
