"use client";

import { MessageSquareText, BookOpen, HelpCircle, FileText } from "lucide-react";

import { useOptionContext } from "../contexts/OptionContext";

export default function OptionHeader() {
  const { option } = useOptionContext();


  return (
    <div className="sticky top-0 z-10 bg-background flex items-center space-x-2 border-b border-border px-6 py-4.5">
      {option === "chat" && (
        <>
          <MessageSquareText className="h-4 w-4 text-[var(--blue-accent)]" />
          <h2 className="text-sm font-medium text-foreground">Chat</h2>
        </>
      )}
      {option === "flashcards" && (
        <>
          <BookOpen className="h-4 w-4 text-[var(--green-accent)]" />
          <h2 className="text-sm font-medium text-foreground">Tarjetas Didácticas</h2>
        </>
      )}
      {option === "quiz" && (
        <>
          <HelpCircle className="h-4 w-4 text-[var(--purple-accent)]" />
          <h2 className="text-sm font-medium text-foreground">Quiz</h2>
        </>
      )}
      {option === "summary" && (
        <>
          <FileText className="h-4 w-4 text-[var(--orange-accent)]" />
          <h2 className="text-sm font-medium text-foreground">Resumen</h2>
        </>
      )}
    </div>
  )
}