"""Promoter search and selection service.

Loads promoter data from CSV, supplemented by EPD API queries.
"""

import csv
from pathlib import Path

from fastapi import HTTPException

from app.clients.epd_client import epd_client
from app.schemas.regulatory import PromoterInfo, PromoterSearchResult

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

# Loaded once at first access
_PROMOTER_DATA: list[PromoterInfo] = []


def _load_promoters() -> list[PromoterInfo]:
    global _PROMOTER_DATA
    if _PROMOTER_DATA:
        return _PROMOTER_DATA

    csv_path = DATA_DIR / "promoters.csv"
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("Name") or "").strip()
            organism = (row.get("Organism") or "").strip()
            if not name or not organism:
                continue
            sequence = (row.get("Sequence") or "").strip()
            ptype = (row.get("Type") or "").strip()
            inducer = (row.get("Inducer_Tissue_Trigger") or "").strip()
            score = (row.get("Expression_Score") or "").strip()
            usable_in = (row.get("Usable_In") or "").strip()

            # Build description from type + inducer/trigger info
            desc_parts = [ptype] if ptype else []
            if inducer:
                desc_parts.append(inducer)
            if usable_in:
                desc_parts.append(f"Usable in: {usable_in}")
            description = ". ".join(desc_parts) if desc_parts else None

            # Map expression score to strength
            strength = None
            if score:
                try:
                    s = int(score)
                    if s >= 80:
                        strength = "strong"
                    elif s >= 40:
                        strength = "moderate"
                    else:
                        strength = "weak"
                except ValueError:
                    pass

            # Generate a stable ID from the name
            promoter_id = "csv_" + name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")

            _PROMOTER_DATA.append(PromoterInfo(
                id=promoter_id,
                name=name,
                organism=organism,
                sequence=sequence,
                length=len(sequence),
                description=description,
                strength=strength,
            ))

    return _PROMOTER_DATA


def _match_organism(promoter: PromoterInfo, query: str) -> bool:
    """Check if a promoter matches an organism search query."""
    q = query.lower()
    fields = [
        promoter.organism.lower(),
        promoter.name.lower(),
        (promoter.description or "").lower(),
    ]
    return any(q in f for f in fields)


async def search_promoters(
    organism: str, gene: str | None = None, limit: int = 20
) -> PromoterSearchResult:
    """Search for promoters by organism, supplemented with EPD results."""
    promoters: list[PromoterInfo] = []

    # Search CSV data first
    all_promoters = _load_promoters()
    for p in all_promoters:
        if _match_organism(p, organism):
            promoters.append(p)

    # Supplement with EPD API
    try:
        epd_data = await epd_client.search_promoters(organism, gene=gene, limit=limit)
        for entry in epd_data.get("results", []):
            promoters.append(
                PromoterInfo(
                    id=entry.get("id", ""),
                    name=entry.get("gene", ""),
                    organism=entry.get("organism", organism),
                    sequence=entry.get("sequence", ""),
                    length=len(entry.get("sequence", "")),
                    description=entry.get("description"),
                    strength=None,
                )
            )
    except Exception:
        pass

    return PromoterSearchResult(promoters=promoters[:limit], total=len(promoters))


async def get_promoter(promoter_id: str) -> PromoterInfo:
    """Fetch a specific promoter by ID."""
    # Check CSV promoters first
    all_promoters = _load_promoters()
    for p in all_promoters:
        if p.id == promoter_id:
            return p

    # Try EPD
    try:
        epd_data = await epd_client.get_promoter_sequence(promoter_id)
        return PromoterInfo(
            id=promoter_id,
            name=epd_data.get("gene", promoter_id),
            organism=epd_data.get("organism", ""),
            sequence=epd_data.get("sequence", ""),
            length=len(epd_data.get("sequence", "")),
            description=epd_data.get("description"),
            strength=None,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail=f"Promoter {promoter_id} not found"
        ) from exc
