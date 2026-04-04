export enum OptimizationStrategy {
  FREQUENCY = "frequency",
  HARMONIZED = "harmonized",
  BALANCED = "balanced",
}

export interface OptimizationRequest {
  sequence: string;
  organism_tax_id: number;
  strategy: OptimizationStrategy;
  avoid_restriction_sites: string[];
  target_gc_min?: number;
  target_gc_max?: number;
  avoid_repeats: boolean;
}

export interface OptimizationResult {
  job_id: string;
  status: string;
  optimized_sequence?: string;
  cai_before?: number;
  cai_after?: number;
  gc_content?: number;
  changes_summary?: Record<string, unknown>;
}
