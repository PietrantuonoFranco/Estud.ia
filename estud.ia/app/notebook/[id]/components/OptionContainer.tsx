"use client";

import { useOptionContext } from "../contexts/OptionContext";
import { useChatInformationContext } from "../contexts/ChatInformationContext";

import ChatPanel from "./Chat/ChatPanel";
import FlascardContainer from "./Flashcard/FlashcardContainer";
import QuizContainer from "./Quiz/QuizContainer";
import { useEffect } from "react";

export default function OptionContainer() {
  const { option } = useOptionContext();
  const { quizzes } = useChatInformationContext();

  useEffect(() => {
    console.log("Current quizzes in context:", quizzes);
  }, [quizzes]);
  
  return (
    <div className="flex-1 overflow-y-auto">
      {option === "chat" && <ChatPanel/>}
      {option === "flashcards" && <FlascardContainer/>}
      {option === "quiz" && <QuizContainer questions={quizzes[0]?.questions_and_answers || []} />}
    </div>
  )
}