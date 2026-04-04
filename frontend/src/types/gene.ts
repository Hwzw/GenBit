export interface GeneSearchResult {
  gene_id: string;
  symbol: string;
  description: string;
  organism: string;
  tax_id?: number;
}

export interface GeneDetail {
  gene_id: string;
  symbol: string;
  full_name: string;
  description: string;
  organism: string;
  tax_id: number;
  chromosome?: string;
  map_location?: string;
  aliases: string[];
}

export interface GeneSequence {
  gene_id: string;
  accession: string;
  sequence: string;
  sequence_type: "genomic" | "mrna" | "cds";
  length: number;
}
