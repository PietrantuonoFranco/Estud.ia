"use client"

import React, { useState, useContext, useEffect } from "react"
import { useParams } from "next/navigation";

import ChatInformationContextType from "@/app/lib/interfaces/contexts/ChatInformationContextType";
import Notebook from "@/app/lib/interfaces/entities/Notebook";
import Message from "@/app/lib/interfaces/entities/Message";
import Summary from "@/app/lib/interfaces/entities/Summary";
import Flashcard from "@/app/lib/interfaces/entities/Flashcard";
import Quiz from "@/app/lib/interfaces/entities/Quiz";


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

  const params = useParams();
  const id = params.id as string; // Extract the id from the route parameters
  

  const API_URL = process.env.API_URL || 'http://localhost:5000';
  
    useEffect(() => {
      if (id) {
        // Fetch notebook data when id is available
        const fetchNotebook = async () => {
          try {
            const response = await fetch(`${API_URL}/notebooks/${id}`); // Adjust the API endpoint as needed
  
            if (!response.ok) {
              throw new Error('Failed to fetch notebook');
            }
        
            const data: Notebook = await response.json();
              setNotebook(data);
            } catch (error) {
              console.error(error);
          }
          };
  
          fetchNotebook();
      }
    }, [id]);

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
      }}
    >
      {children}
    </ChatInformationContext.Provider>
  );
}