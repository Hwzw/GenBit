export interface OrganismSearchResult {
  tax_id: number;
  scientific_name: string;
  common_name?: string;
  lineage?: string;
}

export interface OrganismDetail {
  tax_id: number;
  scientific_name: string;
  common_name?: string;
  lineage?: string;
  gc_content?: number;
}

export interface CodonTable {
  organism_tax_id: number;
  source: string;
  table: Record<string, Record<string, number>>;
}
