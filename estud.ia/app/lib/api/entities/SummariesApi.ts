import api from "../api"

import type Summary from "../../interfaces/entities/Summary";

const entity: string = "summaries";

export async function createSummary(summary: { notebook_id: number; notebook_users_id: number; summary_text: string }): Promise<Summary> {
  const response = await api.post<Summary>(`/${entity}`, summary);
  return response.data;
}

export async function getSummary(summaryId: number): Promise<Summary> {
  const response = await api.get<Summary>(`/${entity}/${summaryId}`);
  return response.data;
}

export async function getAllSummaries(skip: number = 0, limit: number = 10): Promise<Summary[]> {
  const response = await api.get<Summary[]>(`/${entity}`, {
    params: { skip, limit },
  });
  return response.data;
}

export async function deleteSummary(summaryId: number): Promise<Summary> {
  const response = await api.delete<Summary>(`/${entity}/${summaryId}`);
  return response.data;
}

export async function getSummariesByNotebook(notebookId: number): Promise<Summary[]> {
  const response = await api.get<Summary[]>(`/${entity}/notebook/${notebookId}`);
  return response.data;
}

export async function getSummariesByUser(userId: number): Promise<Summary[]> {
  const response = await api.get<Summary[]>(`/${entity}/user/${userId}`);
  return response.data;
}
