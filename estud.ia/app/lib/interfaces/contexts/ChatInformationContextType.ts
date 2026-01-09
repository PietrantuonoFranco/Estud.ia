import React from "react";

import Message from "@/app/lib/interfaces/Message";
import Notebook from "@/app/lib/interfaces/Notebook";
import Summary from "@/app/lib/interfaces/Summary";
import Flashcard from "@/app/lib/interfaces/Flashcard";
import Quiz from "@/app/lib/interfaces/Quiz";

export default interface ChatInformationContextType {
  notebook: Notebook | null;
  setNotebook: React.Dispatch<React.SetStateAction<Notebook | null>>;
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  summaries: Summary[];
  setSummaries: React.Dispatch<React.SetStateAction<Summary[]>>;
  flashcards: Flashcard[];
  setFlashcards: React.Dispatch<React.SetStateAction<Flashcard[]>>;
  quizzes: Quiz[];
  setQuizzes: React.Dispatch<React.SetStateAction<Quiz[]>>;
}