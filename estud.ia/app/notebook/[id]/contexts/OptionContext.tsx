"use client"

import React, { useState, useContext, useEffect } from "react"

import { useChatInformationContext } from "./ChatInformationContext";

enum OptionEnum {
  CHAT = "chat",
  FLASHCARDS = "flashcards",
  SUMMARY = "summary",
  QUIZ = "quiz"
}

export default interface OptionContextType {
  option: OptionEnum | string;
  setOption: React.Dispatch<React.SetStateAction<OptionEnum | string>>;
  isLoading: boolean;
}

const OptionContext = React.createContext<OptionContextType | null>(null);

export function useOptionContext() {
 const context = useContext(OptionContext);

  if (!context) {
    throw new Error("useOptionContext must be used within a OptionProvider");
  }

  return context;
}


export function OptionContextProvider({ children }: { children: React.ReactNode }) {
  const [option, setOption] = useState<OptionEnum | string>(OptionEnum.CHAT);
  const [isLoading, setIsLoading] = useState(false);

  const { notebook, setNotebook, setFlashcards } = useChatInformationContext();
  
  const API_URL = process.env.API_URL || 'http://localhost:5000';
  
  useEffect(() => {
    const fetchFlashcards = async () => {
      if (!notebook?.id) return;
      
      setIsLoading(true);
      try {
        console.log("Fetching flashcards for notebook ID:", notebook.id);

        const response = await fetch(`${API_URL}/notebooks/${notebook.id}/flashcards`, {
          method: 'POST',
          credentials: 'include',
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch flashcards');
        }

        const data = await response.json();
        
        console.log("Fetched flashcards data:", data);
        setFlashcards(data);
        
        // Update the notebook with the new flashcards
        setNotebook((prev) => {
          if (!prev) return prev;
          return { ...prev, flashcards: data };
        });
      } catch (error) {
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    };

    if (option === "flashcards" && notebook && (!notebook.flashcards || notebook.flashcards.length === 0)) {
      fetchFlashcards();
    }
  }, [option, notebook, API_URL, setFlashcards, setNotebook]);

  return (
    <OptionContext.Provider
      value={{
        option,
        setOption,
        isLoading
      }}
    >
      {children}
    </OptionContext.Provider>
  );
}