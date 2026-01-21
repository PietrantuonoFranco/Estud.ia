import api from "../api"

import type Message from "../../interfaces/entities/Message";

const entity: string = "messages";

export async function createMessage(message: { text: string; notebook_id: number }): Promise<Message> {
  const response = await api.post<Message>(`/${entity}`, message);
  return response.data;
}

export async function createUserMessage(message: { text: string; notebook_id: number }): Promise<Message> {
  const response = await api.post<Message>(`/${entity}/user`, message);
  return response.data;
}

export async function createLLMMessage(message: { text: string; notebook_id: number }): Promise<Message> {
  const response = await api.post<Message>(`/${entity}/llm`, message);
  return response.data;
}

export async function getAllMessages(skip: number = 0, limit: number = 10): Promise<Message[]> {
  const response = await api.get<Message[]>(`/${entity}`, {
    params: { skip, limit },
  });
  return response.data;
}

export async function getMessage(messageId: number): Promise<Message> {
  const response = await api.get<Message>(`/${entity}/${messageId}`);
  return response.data;
}

export async function deleteMessage(messageId: number): Promise<void> {
  await api.delete<void>(`/${entity}/${messageId}`);
}

export async function getMessagesByNotebook(notebookId: number): Promise<Message[]> {
  const response = await api.get<Message[]>(`/${entity}/notebook/${notebookId}`);
  return response.data;
}

export async function getMessagesByUser(userId: number): Promise<Message[]> {
  const response = await api.get<Message[]>(`/${entity}/user/${userId}`);
  return response.data;
}
