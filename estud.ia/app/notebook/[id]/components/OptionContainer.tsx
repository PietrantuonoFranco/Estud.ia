"use client";

import { useOptionContext } from "../contexts/OptionContext";
import { useChatInformationContext } from "../contexts/ChatInformationContext";

import ChatPanel from "./Chat/ChatPanel";
import FlashcardContainer from "./Flashcard/FlashcardContainer";
import QuizContainer from "./Quiz/QuizContainer";
import OptionHeader from "./OptionHeader";

export default function OptionContainer() {
  const { option, selectedQuizId } = useOptionContext();
  const { quizzes } = useChatInformationContext();

  const selectedQuiz = quizzes.find((quiz) => quiz.id === selectedQuizId);
  
  return (
    <div className="flex-1 overflow-y-auto min-h-[100dvh]">
      <OptionHeader />
      {option === "chat" && <ChatPanel/>}
      {option === "flashcards" && <FlashcardContainer/>}
      {option === "quiz" && <QuizContainer questions={selectedQuiz?.questions_and_answers || []} />}
    </div>
  )
}