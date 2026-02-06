"use client";

import { MessageSquareText, BookOpen, HelpCircle, FileText, PanelLeft, PanelRight } from "lucide-react";

import { useOptionContext } from "../contexts/OptionContext";

interface OptionHeaderProps {
  isSourcesOpen: boolean;
  isStudioOpen: boolean;
  onToggleSources: () => void;
  onToggleStudio: () => void;
}

export default function OptionHeader({
  isSourcesOpen,
  isStudioOpen,
  onToggleSources,
  onToggleStudio,
}: OptionHeaderProps) {
  const { option } = useOptionContext();

  return (
    <div className="sticky top-0 z-10 bg-background border-b border-border py-2.5">
      <div className="flex items-center justify-between">
        <div className="w-18 flex items-center justify-center">
          <button
            type="button"
            onClick={onToggleSources}
            aria-label={isSourcesOpen ? "Cerrar panel de fuentes" : "Abrir panel de fuentes"}
            className="cursor-pointer h-8 w-8 p-2 hover:bg-[var(--hover-bg)] hover:rounded-full"
          >
            <PanelLeft className="h-4 w-4" />
          </button>
        </div>

        <div className="flex items-center space-x-2">
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

        <div className="w-18 flex items-center justify-center">
          <button
            type="button"
            onClick={onToggleStudio}
            aria-label={isStudioOpen ? "Cerrar panel de funciones" : "Abrir panel de funciones"}
            className="cursor-pointer h-8 w-8 p-2 hover:bg-[var(--hover-bg)] hover:rounded-full"
          >
            <PanelRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  )
}