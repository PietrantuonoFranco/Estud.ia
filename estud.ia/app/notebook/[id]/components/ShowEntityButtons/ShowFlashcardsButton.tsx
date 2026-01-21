"use client"

import { BookOpen } from "lucide-react"

import { useOptionContext } from "../../contexts/OptionContext";

interface ShowFlashcardsButtonProps {
  flashcardsCount: number;
  openPanel: boolean;
}

export default function ShowFlashcardsButton({ flashcardsCount, openPanel }: ShowFlashcardsButtonProps) {
  const { setOption } = useOptionContext();

  const handleClick = () => {
    setOption("flashcards");
  };

  return (
    <div 
      onClick={handleClick}
      className="cursor-pointer group flex items-center gap-3 rounded-lg bg-card p-3 hover:bg-[var(--hover-bg)]"
    >
      <div className={`${openPanel ? "h-10 w-10" : ""} flex items-center justify-center rounded bg-muted`}>
        <BookOpen className="h-4 w-4 text-[var(--green-accent)]" />
      </div>
      
      <div className={`${openPanel ? "flex-1 min-w-0" : "hidden"}`}>
        <p className="text-sm font-medium text-foreground truncate">Tarjetas didácticas</p>
        <p className="text-xs text-muted-foreground">
          {flashcardsCount} tarjeta{flashcardsCount > 1 ? "s" : ""}
        </p>
      </div>
    </div>
  )
}
