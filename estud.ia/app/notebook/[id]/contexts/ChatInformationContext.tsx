"use client"

import React, { useState, useContext, useEffect, useRef } from "react"
import { useParams } from "next/navigation";

import ChatInformationContextType from "@/app/lib/interfaces/contexts/ChatInformationContextType";
import Notebook from "@/app/lib/interfaces/entities/Notebook";
import Message from "@/app/lib/interfaces/entities/Message";
import Summary from "@/app/lib/interfaces/entities/Summary";
import Flashcard from "@/app/lib/interfaces/entities/Flashcard";
import Quiz from "@/app/lib/interfaces/entities/Quiz";
import Source from "@/app/lib/interfaces/entities/Source";

import { NotebooksApi, QuizzesApi, MessagesApi } from "@/app/lib/api/entities";

const ChatInformationContext = React.createContext<ChatInformationContextType | null>(null);

export function useChatInformationContext() {
 const context = useContext(ChatInformationContext);

  if (!context) {
    throw new Error("useChatInformationContext must be used within a ChatInformationProvider");
  }

  return context;
}

export function ChatInformationProvider({ children }: { children: React.ReactNode }) {
  const [notebook, setNotebook] = useState<Notebook | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [summaries, setSummaries] = useState<Summary[]>([]);
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [sources, setSources] = useState<Source[]>([]);

  const params = useParams();
  const id = params.id as string; // Extract the id from the route parameters
  
  const isSending = useRef(false);

  const fetchQuestionsForQuiz = async (quizId: number) => {
    try {
      const questions = await QuizzesApi.getQuestionsByQuiz(quizId);
      return questions;
    } catch (err) {
      console.error('Failed to fetch questions for quiz', err);
      return [];
    }
  };
  
  useEffect(() => {
    if (id) {
      // Fetch notebook data when id is available
      const fetchNotebook = async () => {
        try {
          const notebookId = parseInt(id);
          const data = await NotebooksApi.getNotebook(notebookId);

          console.log("Fetched notebook data:", data);
          setNotebook(data);
          setMessages(data.messages ?? []);
          setSources(data.sources ?? []);
          setFlashcards(data.flashcards ?? []);

          // Fetch detailed quiz data for each quiz
          if (data.quizzes && data.quizzes.length > 0) {
            const quizPromises = data.quizzes.map(async (quiz) => {
              const quizData = await QuizzesApi.getQuiz(quiz.id);
              
              // If quiz has no questions_and_answers, fetch them separately
              if (!quizData.questions_and_answers || quizData.questions_and_answers.length === 0) {
                const questions = await fetchQuestionsForQuiz(quiz.id);
                quizData.questions_and_answers = questions;
              }
              
              return quizData;
            });

            const quizzesData = await Promise.all(quizPromises);

            console.log("Fetched quizzes data:", quizzesData);
            quizzesData.forEach(quiz => {
              console.log(`Quiz ${quiz.id} - ${quiz.title}:`, {
                has_questions_and_answers: !!quiz.questions_and_answers,
                count: quiz.questions_and_answers?.length || 0,
                data: quiz.questions_and_answers
              });
            });
            
            setQuizzes(quizzesData);
          } else {
            setQuizzes([]);
          }
        } catch (error) {
          console.error(error);
        }
      };

      fetchNotebook();
    }
  }, [id]);

    useEffect(() => {
      if (!notebook || messages.length === 0) return;
    
      const last = messages[messages.length - 1];
      if (!last.is_user_message || isSending.current) return;

      // Si el mensaje tiene un ID temporal (Date.now()), aún no ha sido creado en la BD
      const isOptimistic = typeof last.id === 'number' && last.id > 1000000000000;
      if (!isOptimistic) return;

      isSending.current = true;
    
      const send = async () => {
        try {
          // 1. Create the user message in the DB
          const createdUserMessage = await MessagesApi.createUserMessage({
            text: last.text,
            notebook_id: notebook.id,
          });

          // Replace the optimistic message with the one from the server
          setMessages((prev) => 
            prev.map((msg) => msg.id === last.id ? createdUserMessage : msg)
          );

          // 2. Add a loading message for the LLM response
          const loadingMessage: Message = {
            id: Date.now() + 1,
            notebook_id: notebook.id,
            is_user_message: false,
            text: "",
            isLoading: true,
          };
          setMessages((prev) => [...prev, loadingMessage]);

          // 3. Now send the request to the LLM
          const llmData = await MessagesApi.createLLMMessage({
            text: last.text,
            notebook_id: notebook.id,
          });

          setMessages((prev) => 
            prev.map((msg) => msg.id === loadingMessage.id ? llmData : msg)
          );
        } catch (err) {
          console.error(err);
        } finally {
          isSending.current = false;
        }
      };
    
      send();
    }, [messages, notebook, setMessages]);

  return (
    <ChatInformationContext.Provider
      value={{
        notebook,
        setNotebook,
        messages,
        setMessages,
        summaries,
        setSummaries,
        flashcards,
        setFlashcards,
        quizzes,
        setQuizzes,
        sources,
        setSources,
      }}
    >
      {children}
    </ChatInformationContext.Provider>
  );
}