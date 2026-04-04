import type { Project, ProjectCreate } from "@/types";
import apiClient from "./client";

export async function listProjects(): Promise<Project[]> {
  const { data } = await apiClient.get("/api/projects");
  return data;
}

export async function getProject(id: string): Promise<Project> {
  const { data } = await apiClient.get(`/api/projects/${id}`);
  return data;
}

export async function createProject(data: ProjectCreate): Promise<Project> {
  const { data: result } = await apiClient.post("/api/projects", data);
  return result;
}

export async function deleteProject(id: string): Promise<void> {
  await apiClient.delete(`/api/projects/${id}`);
}
