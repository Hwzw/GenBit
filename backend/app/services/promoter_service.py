"""Promoter search and selection service. Queries EPD and JASPAR."""

from app.clients.epd_client import epd_client
from app.schemas.regulatory import PromoterInfo, PromoterSearchResult

# Common synthetic promoters (not from EPD)
SYNTHETIC_PROMOTERS = {
    "mammalian": [
        PromoterInfo(
            id="syn_cmv", name="CMV", organism="mammalian", sequence="", length=0,
            description="Cytomegalovirus immediate-early promoter", strength="strong",
        ),
        PromoterInfo(
            id="syn_ef1a", name="EF1a", organism="mammalian", sequence="", length=0,
            description="Elongation factor 1-alpha promoter", strength="strong",
        ),
        PromoterInfo(
            id="syn_cag", name="CAG", organism="mammalian", sequence="", length=0,
            description="CMV early enhancer/chicken beta-actin promoter", strength="strong",
        ),
        PromoterInfo(
            id="syn_pgk", name="PGK", organism="mammalian", sequence="", length=0,
            description="Phosphoglycerate kinase promoter", strength="moderate",
        ),
    ],
    "yeast": [
        PromoterInfo(
            id="syn_gal1", name="GAL1", organism="yeast", sequence="", length=0,
            description="Galactose-inducible promoter", strength="strong",
        ),
        PromoterInfo(
            id="syn_tef1", name="TEF1", organism="yeast", sequence="", length=0,
            description="Translation elongation factor promoter", strength="strong",
        ),
    ],
    "plant": [
        PromoterInfo(
            id="syn_camv35s", name="CaMV 35S", organism="plant", sequence="", length=0,
            description="Cauliflower mosaic virus 35S promoter", strength="strong",
        ),
    ],
}


async def search_promoters(
    organism: str, gene: str | None = None, limit: int = 20
) -> PromoterSearchResult:
    """Search EPD for promoters, supplemented with synthetic promoter catalog."""
    promoters: list[PromoterInfo] = []

    # Try EPD first
    try:
        epd_data = await epd_client.search_promoters(organism, gene=gene, limit=limit)
        # TODO: parse EPD response into PromoterInfo objects
        _ = epd_data
    except Exception:
        pass

    # Supplement with synthetic promoters
    for category, synth_list in SYNTHETIC_PROMOTERS.items():
        if category in organism.lower():
            promoters.extend(synth_list)

    return PromoterSearchResult(promoters=promoters[:limit], total=len(promoters))


async def get_promoter(promoter_id: str) -> PromoterInfo:
    """Fetch a specific promoter by ID."""
    # TODO: implement
    raise NotImplementedError
