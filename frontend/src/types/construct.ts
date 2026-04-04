export enum ElementType {
  PROMOTER = "promoter",
  KOZAK = "kozak",
  CDS = "cds",
  TERMINATOR = "terminator",
  TAG = "tag",
  UTR = "utr",
  CUSTOM = "custom",
}

export interface ConstructElement {
  element_type: ElementType;
  label: string;
  sequence: string;
  position: number;
  metadata_json?: Record<string, unknown>;
}

export interface Construct {
  id: string;
  project_id: string;
  name: string;
  full_sequence?: string;
  organism_tax_id?: number;
  elements: ConstructElement[];
  created_at: string;
  updated_at: string;
}

export interface ConstructCreate {
  project_id: string;
  name: string;
  organism_tax_id?: number;
  elements: ConstructElement[];
}
