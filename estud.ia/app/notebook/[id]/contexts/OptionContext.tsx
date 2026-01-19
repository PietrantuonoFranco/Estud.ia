"use client"

import React, { useState, useContext, useEffect, useRef } from "react"

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

  const { notebook, setNotebook, setFlashcards, setQuizzes } = useChatInformationContext();
  
  const API_URL = process.env.API_URL || 'http://localhost:5000';
  const fetchedExistingQuizRef = useRef<boolean>(false);
  const createdQuizRef = useRef<boolean>(false);
  const lastNotebookIdRef = useRef<number | null>(null);

  const normalizeQuiz = (raw: any) => {
    if (!raw) return raw;
    // If the backend returns an array directly, wrap it
    if (Array.isArray(raw)) {
      return { id: Date.now(), notebook_id: notebook?.id ?? 0, questions_and_answers: raw };
    }

    const copy: any = { ...raw };
    if (!copy.questions_and_answers) {
      if (copy.questions) copy.questions_and_answers = copy.questions;
      else if (copy.question_and_answers) copy.questions_and_answers = copy.question_and_answers;
      else if (copy.questionAndAnswers) copy.questions_and_answers = copy.questionAndAnswers;
      else copy.questions_and_answers = [];
    }

    return copy;
  };

  const fetchQuestionsForQuiz = async (quizId: number) => {
    try {
      const resp = await fetch(`${API_URL}/quizzes/${quizId}/questions`, {
        method: 'GET',
        credentials: 'include',
      });
      if (!resp.ok) return [];
      const questions = await resp.json();
      return questions;
    } catch (err) {
      console.error('Failed to fetch questions for quiz', err);
      return [];
    }
  };

  useEffect(() => {
    // reset guards when switching notebooks
    if (notebook?.id && lastNotebookIdRef.current !== notebook.id) {
      fetchedExistingQuizRef.current = false;
      createdQuizRef.current = false;
      lastNotebookIdRef.current = notebook.id;
    }

    const createFlashcard = async () => {
      if (!notebook?.id) return;
      
      setIsLoading(true);
      try {
        const response = await fetch(`${API_URL}/notebooks/${notebook.id}/flashcards`, {
          method: 'POST',
          credentials: 'include',
        });
        
        if (!response.ok) {
          throw new Error('Failed to create flashcards');
        }

        const data = await response.json();
        
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

    const createQuiz = async () => {
      if (!notebook?.id) return;
      if (createdQuizRef.current) return;
      setIsLoading(true);
      try {
        const response = await fetch(`${API_URL}/notebooks/${notebook.id}/quiz`, {
          method: 'POST',
          credentials: 'include',
        });
        
        if (!response.ok) {
          throw new Error('Failed to create quiz');
        }

        const raw = await response.json();
        const data = normalizeQuiz(raw);
        // If backend returned no questions, try fetching them separately
        if (data && data.id && Array.isArray(data.questions_and_answers) && data.questions_and_answers.length === 0) {
          const fetched = await fetchQuestionsForQuiz(data.id);
          data.questions_and_answers = fetched;
        }

        setQuizzes(prev => [...prev, data]);
        createdQuizRef.current = true;

        // Update the notebook with the new quizzes
        setNotebook((prev) => {
          if (!prev) return prev;
          return { ...prev, quizzes: [...(prev.quizzes || []), data] };
        });
      } catch (error) {
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    };

    if (option === "flashcards" && notebook && (!notebook.flashcards || notebook.flashcards.length === 0)) {
      createFlashcard();
    }

    if (option === "quiz" && notebook) {
      if (!notebook.quizzes || notebook.quizzes.length === 0) {
        createQuiz();
      } else {
        // If quizzes already exist, fetch from external endpoint and display
        const fetchExistingQuiz = async () => {
          if (fetchedExistingQuizRef.current) return;
          setIsLoading(true);
          try {
            const quizId = notebook.quizzes && notebook.quizzes[0] ? notebook.quizzes[0].id : null;
            if (!quizId) throw new Error('No quiz id available');
            const resp = await fetch(`${API_URL}/quizzes/${quizId}`, {
              method: 'GET',
              credentials: 'include',
            });

            if (!resp.ok) throw new Error('Failed to fetch existing quiz');

            const raw = await resp.json();
            const data = normalizeQuiz(raw);

            // If quiz has no questions, try fetching them
            if (data && data.id && Array.isArray(data.questions_and_answers) && data.questions_and_answers.length === 0) {
              const fetched = await fetchQuestionsForQuiz(data.id);
              data.questions_and_answers = fetched;
            }

            console.log("Fetched existing quiz data:", data);
            
            setQuizzes(prev => [...prev, data]);

            setNotebook((prev) => {
              if (!prev) return prev;
              return { ...prev, quizzes: [...(prev.quizzes || []), data] };
            });
            fetchedExistingQuizRef.current = true;
          } catch (err) {
            console.error(err);
          } finally {
            setIsLoading(false);
          }
        };

        fetchExistingQuiz();
      }
    } 
  }, [option, notebook, API_URL, setFlashcards, setNotebook, setQuizzes]);

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