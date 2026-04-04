from pydantic import BaseModel


class ProteinSearchQuery(BaseModel):
    query: str
    organism: str | None = None
    limit: int = 20


class ProteinSearchResult(BaseModel):
    accession: str
    name: str
    organism: str
    length: int
    source: str  # "ncbi" or "uniprot"


class ProteinDetail(BaseModel):
    accession: str
    name: str
    full_name: str | None = None
    organism: str
    tax_id: int | None = None
    length: int
    function: str | None = None
    gene_name: str | None = None
    source: str


class ProteinSequence(BaseModel):
    accession: str
    sequence: str
    length: int
    source: str
