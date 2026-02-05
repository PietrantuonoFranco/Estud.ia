import api from "../api"

import type Notebook from "../../interfaces/entities/Notebook";
import type Source from "../../interfaces/entities/Source";

const entity: string = "notebooks";

export async function createNotebook(files: File[]): Promise<Notebook> {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  
  const response = await api.post<Notebook>(`/${entity}`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function getNotebook(notebookId: number): Promise<Notebook> {
  const response = await api.get<Notebook>(`/${entity}/${notebookId}`);
  return response.data;
}

export async function getAllNotebooks(skip: number = 0, limit: number = 10): Promise<Notebook[]> {
  const response = await api.get<Notebook[]>(`/${entity}`, {
    params: { skip, limit },
  });
  return response.data;
}

export async function getNotebooksByUser(userId: number): Promise<Notebook[]> {
  const response = await api.get<Notebook[]>(`/${entity}/user/${userId}`);
  return response.data;
}

export async function deleteNotebook(notebookId: number): Promise<Notebook> {
  const response = await api.delete<Notebook>(`/${entity}/${notebookId}`);
  return response.data;
}

export async function generateFlashcards(notebookId: number): Promise<Notebook> {
  const response = await api.post<Notebook>(`/${entity}/${notebookId}/flashcards`);
  return response.data;
}

export async function generateSummary(notebookId: number): Promise<Notebook> {
  const response = await api.post<Notebook>(`/${entity}/${notebookId}/summary`);
  return response.data;
}

export async function generateQuiz(notebookId: number): Promise<Notebook> {
  const response = await api.post<Notebook>(`/${entity}/${notebookId}/quiz`);
  return response.data;
}

export async function getSourcesByNotebook(notebookId: number): Promise<any[]> {
  const response = await api.get<any[]>(`/${entity}/${notebookId}/sources`);
  return response.data;
}

export async function deleteVariousSourcesByNotebookIdAndSourceIds(notebookId: number, sourceIds: number[]): Promise<Source[]> {
  const response = await api.delete<Source[]>(`/${entity}/${notebookId}/sources/delete-various`, {
    data: { pdf_ids: sourceIds }
  });

  if (!response.data) {
    throw new Error("Failed to delete sources");
  }

  return response.data
}