import api from "../api"

import type User from "../../interfaces/entities/User";

const entity: string = "users";

export async function createUser(user: { email: string; password: string }): Promise<User> {
  const response = await api.post<User>(`/${entity}`, user);
  return response.data;
}

export async function getUser(userId: number): Promise<User> {
  const response = await api.get<User>(`/${entity}/${userId}`);
  return response.data;
}

export async function getAllUsers(skip: number = 0, limit: number = 10): Promise<User[]> {
  const response = await api.get<User[]>(`/${entity}`, {
    params: { skip, limit },
  });
  return response.data;
}

export async function getUserByEmail(email: string): Promise<User> {
  const response = await api.get<User>(`/${entity}/by_email`, {
    params: { email },
  });
  return response.data;
}
