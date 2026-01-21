import api from "../api"

import type Quiz from "../../interfaces/entities/Quiz";
import type QuestionsAndAnswers from "../../interfaces/entities/QuestionsAndAnswers";

const entity: string = "quizzes";

export async function getQuiz(quizId: number): Promise<Quiz> {
  const response = await api.get<Quiz>(`/${entity}/${quizId}`);
  return response.data;
}

export async function getQuizzes(skip: number = 0, limit: number = 10): Promise<Quiz[]> {
  const response = await api.get<Quiz[]>(`/${entity}`, {
    params: { skip, limit },
  });
  return response.data;
}

export async function getQuizzesByNotebook(notebookId: number): Promise<Quiz[]> {
  const response = await api.get<Quiz[]>(`/${entity}/notebook/${notebookId}`);
  return response.data;
}

export async function getQuizzesByUser(userId: number): Promise<Quiz[]> {
  const response = await api.get<Quiz[]>(`/${entity}/user/${userId}`);
  return response.data;
}

export async function createQuiz(quiz: { notebook_id: number; notebook_users_id: number; title?: string; questions?: any[] }): Promise<Quiz> {
  const response = await api.post<Quiz>(`/${entity}`, quiz);
  return response.data;
}

export async function deleteQuiz(quizId: number): Promise<Quiz> {
  const response = await api.delete<Quiz>(`/${entity}/${quizId}`);
  return response.data;
}

export async function getQuestionsByQuiz(quizId: number): Promise<QuestionsAndAnswers[]> {
  const response = await api.get<QuestionsAndAnswers[]>(`/${entity}/${quizId}/questions`);
  return response.data;
}

export async function createQuestion(question: { question: string; answer: string; incorrect_answer_1: string; incorrect_answer_2: string; incorrect_answer_3: string; quiz_id: number }): Promise<QuestionsAndAnswers> {
  const response = await api.post<QuestionsAndAnswers>(`/${entity}/questions`, question);
  return response.data;
}

export async function getQuestion(questionId: number): Promise<QuestionsAndAnswers> {
  const response = await api.get<QuestionsAndAnswers>(`/${entity}/questions/${questionId}`);
  return response.data;
}

export async function deleteQuestion(questionId: number): Promise<QuestionsAndAnswers> {
  const response = await api.delete<QuestionsAndAnswers>(`/${entity}/questions/${questionId}`);
  return response.data;
}
