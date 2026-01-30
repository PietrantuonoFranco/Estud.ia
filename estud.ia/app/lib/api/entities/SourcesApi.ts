import api from "../api"

import type Source from "../../interfaces/entities/Source";

const entity: string = "sources";

export async function createSource(source: { url: string; notebook_id: number }): Promise<Source> {
  const response = await api.post<Source>(`/${entity}`, source);
  return response.data;
}

export async function getSource(sourceId: number): Promise<Source> {
  const response = await api.get<Source>(`/${entity}/${sourceId}`);
  return response.data;
}

export async function getAllSources(skip: number = 0, limit: number = 10): Promise<Source[]> {
  const response = await api.get<Source[]>(`/${entity}`, {
    params: { skip, limit },
  });
  return response.data;
}

export async function deleteSource(sourceId: number): Promise<Source> {
  const response = await api.delete<Source>(`/${entity}/${sourceId}`);

  if (!response.data) {
    throw new Error("Failed to delete sources");
  }
  
  return response.data;
}

export async function deleteVariousSources(sourceIds: number[]): Promise<Source[]> {
  const response = await api.delete<Source[]>(`/${entity}/delete-various`, {
    data: { pdf_ids: sourceIds }
  });

  if (!response.data) {
    throw new Error("Failed to delete sources");
  }

  return response.data
}

export async function getNotebookBySource(sourceId: number): Promise<any> {
  const response = await api.get<any>(`/${entity}/${sourceId}/notebook`);
  return response.data;
}

export async function getSourcesByNotebook(notebookId: number): Promise<Source[]> {
  const response = await api.get<Source[]>(`/${entity}/notebook/${notebookId}`);
  return response.data;
}

export async function getSourcesByUser(userId: number): Promise<Source[]> {
  const response = await api.get<Source[]>(`/${entity}/user/${userId}`);
  return response.data;
}
