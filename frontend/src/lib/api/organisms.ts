import type { OrganismDetail, OrganismSearchResult } from "@/types";
import apiClient from "./client";

export async function searchOrganisms(query: string): Promise<OrganismSearchResult[]> {
  const { data } = await apiClient.get("/api/organisms/search", { params: { q: query } });
  return data;
}

export async function getOrganism(taxId: number): Promise<OrganismDetail> {
  const { data } = await apiClient.get(`/api/organisms/${taxId}`);
  return data;
}
