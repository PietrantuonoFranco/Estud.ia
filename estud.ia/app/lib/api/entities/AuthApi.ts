import api from "../api"

import type User from "../../interfaces/entities/User";

const entity: string = "auth";

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  name: string;
  lastname: string;
  password: string;
}

export interface AuthResponse {
  message: string;
  token_type: string;
}

export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  const response = await api.post<AuthResponse>(`/${entity}/login`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
}

export async function register(data: RegisterData): Promise<AuthResponse> {
  const response = await api.post<AuthResponse>(`/${entity}/register`, data);
  return response.data;
}

export async function logout(): Promise<{ message: string }> {
  const response = await api.post<{ message: string }>(`/${entity}/logout`);
  return response.data;
}

export async function getMe(): Promise<User> {
  const response = await api.get<User>(`/${entity}/me`);
  return response.data;
}

export function getGoogleLoginUrl(): string {
  return `${api.defaults.baseURL}/${entity}/login/google`;
}
