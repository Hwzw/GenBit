export interface ProteinSearchResult {
  accession: string;
  name: string;
  organism: string;
  length: number;
  source: "ncbi" | "uniprot";
}

export interface ProteinDetail {
  accession: string;
  name: string;
  full_name?: string;
  organism: string;
  tax_id?: number;
  length: number;
  function?: string;
  gene_name?: string;
  source: string;
}

export interface ProteinSequence {
  accession: string;
  sequence: string;
  length: number;
  source: string;
}
