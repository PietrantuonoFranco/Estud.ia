import React from "react";

import Message from "@/app/lib/interfaces/entities/Message";
import Notebook from "@/app/lib/interfaces/entities/Notebook";
import Summary from "@/app/lib/interfaces/entities/Summary";
import Flashcard from "@/app/lib/interfaces/entities/Flashcard";
import Quiz from "@/app/lib/interfaces/entities/Quiz";

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