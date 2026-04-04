import type { ProteinDetail, ProteinSearchResult, ProteinSequence } from "@/types";
import apiClient from "./client";

export async function searchProteins(
  query: string,
  organism?: string
): Promise<ProteinSearchResult[]> {
  const { data } = await apiClient.get("/api/proteins/search", {
    params: { q: query, organism },
  });
  return data;
}

export async function getProtein(accession: string): Promise<ProteinDetail> {
  const { data } = await apiClient.get(`/api/proteins/${accession}`);
  return data;
}

export async function getProteinSequence(accession: string): Promise<ProteinSequence> {
  const { data } = await apiClient.get(`/api/proteins/${accession}/sequence`);
  return data;
}
