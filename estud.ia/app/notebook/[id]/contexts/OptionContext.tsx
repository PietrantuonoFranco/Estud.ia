"use client"

import React, { useState, useContext } from "react"

import { useChatInformationContext } from "./ChatInformationContext";
import { generateFlashcards, generateQuiz } from "@/app/lib/api/entities/NotebooksApi";
import { getQuestionsByQuiz } from "@/app/lib/api/entities/QuizzesApi";

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
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
  selectedQuizId: number | null;
  setSelectedQuizId: React.Dispatch<React.SetStateAction<number | null>>;
  createFlashcard: () => Promise<void>;
  createQuiz: () => Promise<void>;
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
  const [selectedQuizId, setSelectedQuizId] = useState<number | null>(null);

  const { notebook, setNotebook, setFlashcards, setQuizzes } = useChatInformationContext();
  


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
      const quizQuestions = await getQuestionsByQuiz(quizId);

      if (!quizQuestions) return [];
      
      return quizQuestions;
    } catch (err) {
      console.error('Failed to fetch questions for quiz', err);
      return [];
    }
  };

  const createFlashcard = async () => {
    if (!notebook?.id) return;
    
    setIsLoading(true);
    try {
      const newFlashcards = await generateFlashcards(notebook.id);
      
      if (!newFlashcards || newFlashcards.length === 0) {
        throw new Error('Failed to create flashcards');
      }

      // Add new flashcards to existing ones
      setFlashcards(prev => [...prev, ...newFlashcards]);
      
      // Update the notebook with the new flashcards
      setNotebook((prev) => {
        if (!prev) return prev;
        return { ...prev, flashcards: [...(prev.flashcards || []), ...newFlashcards] };
      });
    } catch (error) {
      console.error(error);
      setIsLoading(false);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const createQuiz = async () => {
    if (!notebook?.id) return;
    setIsLoading(true);
    try {
      const newQuiz = await generateQuiz(notebook.id);
      
      if (!newQuiz) {
        throw new Error('Failed to create quiz');
      }

      const data = normalizeQuiz(newQuiz);
      // If backend returned no questions, try fetching them separately
      if (data && data.id && Array.isArray(data.questions_and_answers) && data.questions_and_answers.length === 0) {
        const fetched = await fetchQuestionsForQuiz(data.id);
        data.questions_and_answers = fetched;
      }

      setQuizzes(prev => [...prev, data]);
      setSelectedQuizId(data.id); // Auto-select the newly created quiz

      // Update the notebook with the new quizzes
      setNotebook((prev) => {
        if (!prev) return prev;
        return { ...prev, quizzes: [...(prev.quizzes || []), data] };
      });
    } catch (error) {
      console.error(error);
      setIsLoading(false);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <OptionContext.Provider
      value={{
        option,
        setOption,
        isLoading,
        setIsLoading,
        selectedQuizId,
        setSelectedQuizId,
        createFlashcard,
        createQuiz,
      }}
    >
      {children}
    </OptionContext.Provider>
  );
}