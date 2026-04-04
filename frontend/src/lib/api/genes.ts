import type { GeneDetail, GeneSearchResult, GeneSequence } from "@/types";
import apiClient from "./client";

export async function searchGenes(query: string, organism?: string): Promise<GeneSearchResult[]> {
  const { data } = await apiClient.get("/api/genes/search", {
    params: { q: query, organism },
  });
  return data;
}

export async function getGene(geneId: string): Promise<GeneDetail> {
  const { data } = await apiClient.get(`/api/genes/${geneId}`);
  return data;
}

export async function getGeneSequence(geneId: string, seqType = "cds"): Promise<GeneSequence> {
  const { data } = await apiClient.get(`/api/genes/${geneId}/sequence`, {
    params: { seq_type: seqType },
  });
  return data;
}
