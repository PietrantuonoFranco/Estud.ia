import api from "../api"

import type Flashcard from "../../interfaces/entities/Flashcard";

const entity: string = "flashcards";

export async function getFlashcards(notebookId: number): Promise<Flashcard[]> {
  const response = await api.get<Flashcard[]>(`/${entity}/notebook/${notebookId}`);
  return response.data;
}

export async function createFlashcard(notebookId: number, question: string, answer: string): Promise<Flashcard> {
  const response = await api.post<Flashcard>(`/${entity}`, {
    notebook_id: notebookId,
    question,
    answer,
  });
  return response.data;
}

export async function deleteFlashcard(flashcardId: number): Promise<void> {
  await api.delete<void>(`/${entity}/${flashcardId}`);
}

export async function updateFlashcard(flashcardId: number, question: string, answer: string): Promise<Flashcard> {
  const response = await api.put<Flashcard>(`/${entity}/${flashcardId}`, {
    question,
    answer,
  });
  return response.data;
}

export async function deleteFlashcardsByNotebook(notebookId: number): Promise<void> {
  await api.delete<void>(`/${entity}/notebook/${notebookId}`);
}