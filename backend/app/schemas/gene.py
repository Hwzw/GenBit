from pydantic import BaseModel


class GeneSearchQuery(BaseModel):
    query: str
    organism: str | None = None
    limit: int = 20


class GeneSearchResult(BaseModel):
    gene_id: str
    symbol: str
    description: str
    organism: str
    tax_id: int | None = None


class GeneDetail(BaseModel):
    gene_id: str
    symbol: str
    full_name: str
    description: str
    organism: str
    tax_id: int
    chromosome: str | None = None
    map_location: str | None = None
    aliases: list[str] = []


class GeneSequence(BaseModel):
    gene_id: str
    accession: str
    sequence: str
    sequence_type: str  # "genomic", "mrna", "cds"
    length: int
