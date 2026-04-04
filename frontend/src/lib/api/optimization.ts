import type { OptimizationRequest, OptimizationResult } from "@/types";
import apiClient from "./client";

export async function optimizeCodons(request: OptimizationRequest): Promise<OptimizationResult> {
  const { data } = await apiClient.post("/api/optimization/optimize", request);
  return data;
}

export async function getCodonTable(organismTaxId: number) {
  const { data } = await apiClient.get(`/api/organisms/${organismTaxId}/codon-table`);
  return data;
}
