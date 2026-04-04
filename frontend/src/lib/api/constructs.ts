import type { Construct, ConstructCreate } from "@/types";
import apiClient from "./client";

export async function createConstruct(data: ConstructCreate): Promise<Construct> {
  const { data: result } = await apiClient.post("/api/constructs", data);
  return result;
}

export async function getConstruct(id: string): Promise<Construct> {
  const { data } = await apiClient.get(`/api/constructs/${id}`);
  return data;
}

export async function updateConstruct(id: string, data: Partial<ConstructCreate>): Promise<Construct> {
  const { data: result } = await apiClient.put(`/api/constructs/${id}`, data);
  return result;
}

export async function deleteConstruct(id: string): Promise<void> {
  await apiClient.delete(`/api/constructs/${id}`);
}

export async function assembleConstruct(id: string): Promise<{ full_sequence: string; length: number }> {
  const { data } = await apiClient.post(`/api/constructs/${id}/assemble`);
  return data;
}
