"use client";

import { useOptionContext } from "../contexts/OptionContext";

import ChatPanel from "./Chat/ChatPanel";
import FlascardContainer from "./Flashcard/FlashcardContainer";
import QuizContainer from "./Quiz/QuizContainer";

export default function OptionContainer() {
  const { option } = useOptionContext();

  return (
    <div className="flex-1 overflow-y-auto">
      {option === "chat" && <ChatPanel/>}
      {option === "flashcards" && <FlascardContainer/>}
      {option === "quiz" && <QuizContainer/>}
    </div>
  )
}