"use client";

import { useOptionContext } from "../contexts/OptionContext";
import { useChatInformationContext } from "../contexts/ChatInformationContext";

import ChatPanel from "./Chat/ChatPanel";
import FlashcardContainer from "./Flashcard/FlashcardContainer";
import QuizContainer from "./Quiz/QuizContainer";
export default function OptionContainer() {
  const { option, selectedQuizId, isLoading } = useOptionContext();
  const { quizzes } = useChatInformationContext();

  const selectedQuiz = quizzes.find((quiz) => quiz.id === selectedQuizId);
  

  if (isLoading) {
    return (
      <div className="min-h-[100dvh] flex-1 flex flex-col items-center justify-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" width="34px" height="34px" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3c4.97 0 9 4.03 9 9"><animateTransform attributeName="transform" dur="1.5s" repeatCount="indefinite" type="rotate" values="0 12 12;360 12 12"></animateTransform></path></svg>
        <p className="w-full text-center">
          Generando contenido...
        </p>
      </div>
    );
  }
  return (
    <div className="h-full flex-1 overflow-y-auto flex flex-col">
      {option === "chat" && <ChatPanel/>}
      {option === "flashcards" && <FlashcardContainer/>}
      {option === "quiz" && <QuizContainer questions={selectedQuiz?.questions_and_answers || []} />}
    </div>
  )
}