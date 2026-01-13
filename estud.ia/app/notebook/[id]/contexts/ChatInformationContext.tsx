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
  

  const API_URL = process.env.API_URL || 'http://localhost:5000';
  const isSending = useRef(false);
  
    useEffect(() => {
      if (id) {
        // Fetch notebook data when id is available
        const fetchNotebook = async () => {
          try {
            const response = await fetch(`${API_URL}/notebooks/${id}`); // Adjust the API endpoint as needed
  
            if (!response.ok) {
              throw new Error('Failed to fetch notebook');
            }
        
            const data: Notebook & { messages?: Message[], sources?: Source[] } = await response.json();

            console.log("Fetched notebook data:", data);
            setNotebook(data);
            setMessages(data.messages ?? []);
            setSources(data.sources ?? []);
            
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

      const controller = new AbortController();
      isSending.current = true;
    
      const send = async () => {
        try {
          // 1. Create the user message in the DB
          const userMessageRes = await fetch(`${API_URL}/messages/user`, {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              text: last.text,
              notebook_id: notebook.id,
            }),
            signal: controller.signal,
          });
    
          if (!userMessageRes.ok) throw new Error("Could not create user message");
    
          const userMessageData = await userMessageRes.json();
          const createdUserMessage = userMessageData;

          // Replace the optimistic message with the one from the server
          setMessages((prev) => 
            prev.map((msg) => msg.id === last.id ? createdUserMessage : msg)
          );

          // 2. Now send the request to the LLM
          const llmRes = await fetch(`${API_URL}/messages/llm`, {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              text: last.text,
              notebook_id: notebook.id,
            }),
            signal: controller.signal,
          });
    
          if (!llmRes.ok) throw new Error("Could not get LLM response");
    
          const llmData = await llmRes.json();
          setMessages((prev) => [...prev, llmData]);
        } catch (err) {
          console.error(err);
        } finally {
          isSending.current = false;
        }
      };
    
      send();
      return () => {
        // Evitar abortar la petición del LLM por cambios en el estado.
        // Mantener la petición en curso hasta completar o desmontar el componente.
        isSending.current = false;
      };
    }, [messages, notebook, API_URL, setMessages]);

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