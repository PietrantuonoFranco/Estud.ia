"use client"

import { HelpCircle, FileText, BookOpen, MoreVertical } from "lucide-react"

import { useOptionContext } from "../../contexts/OptionContext";

interface ShowQuizButtonProps {
  item: {
    id: string | number;
    type: string;
    title: string;
    sources: number;
    time: string;
  };
  openPanel: boolean;
}

export default function ShowQuizButton ({ item, openPanel }: ShowQuizButtonProps) {
  const { setOption, setSelectedQuizId } = useOptionContext();

  const handleClick = () => {
    if (item.type === "quiz" && typeof item.id === "number") {
      setSelectedQuizId(item.id);
      setOption("quiz");
    }
  };

  return (
    <div
      onClick={handleClick}
      className="cursor-pointer group flex items-center gap-3 rounded-lg bg-card p-3 hover:bg-[var(--hover-bg)]"
    >
      <div className={`${ openPanel ? "h-10 w-10" : ""} flex items-center justify-center rounded bg-muted`}>
        {item.type === "quiz" && <HelpCircle className="h-4 w-4 text-[var(--purple-accent)]" />}
        {item.type === "audio" && <FileText className="h-4 w-4 text-[var(--orange-accent)]" />}
        {item.type === "flashcards" && <BookOpen className="h-4 w-4 text-[var(--green-accent)]" />}
      </div>
      
      <div className={`${ openPanel ? "flex-1 min-w-0" : "hidden"}`}>
        <p className="text-sm font-medium text-foreground truncate">{item.title ? item.title : "Cuestionario"}</p>
        <p className="text-xs text-muted-foreground">
          {item.type === "flashcards" && `${item.sources} tarjeta${item.sources > 1 ? "s" : ""}` }

          {item.type === "quiz" && `${item.sources} pregunta${item.sources > 1 ? "s" : ""}` }
        </p>
      </div>
{/*
      <div className={ openPanel ? "flex items-center gap-1" : "hidden"}>
        <button className="cursor-pointer h-8 w-8 opacity-0 group-hover:opacity-100">
          <MoreVertical className="h-4 w-4" />
         </button>
      </div>
*/}
    </div>
  )
}