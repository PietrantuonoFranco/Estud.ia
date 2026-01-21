"use client"

import { useState } from "react"
import {
  PanelRight,
  FileText,
  BookOpen,
  HelpCircle,
  MoreVertical,
  StickyNote,
  MessageSquareText
} from "lucide-react"

import { useChatInformationContext } from "../contexts/ChatInformationContext";
import OptionButton from "./OptionButton";
import ShowQuizButton from "./ShowEntityButtons/ShowQuizButton";
import ShowFlashcardsButton from "./ShowEntityButtons/ShowFlashcardsButton";

const studioTools = [
  { optionName: "chat", icon: MessageSquareText, label: "Chat", color: "blue" },
  { optionName: "flashcards", icon: BookOpen, label: "Tarjetas didácticas", color: "green" },
  { optionName: "summary", icon: FileText, label: "Resumen", color: "orange" },
  { optionName: "quiz", icon: HelpCircle, label: "Cuestionario", color: "purple" },
]

export default function StudioPanel() {
  const { quizzes, flashcards } = useChatInformationContext();
  
  const [openPanel, setOpenPanel] = useState(true);

  const recentItems = [
    ...(flashcards && flashcards.length > 0 ? [{
      id: "all-flashcards",
      type: "flashcards",
      title: "Tarjetas didácticas",
      sources: flashcards.length,
      time: "Reciente",
    }] : []),
    ...(quizzes?.map((quiz) => {
      const questionCount = quiz.questions_and_answers?.length || 0;
      console.log(`Quiz "${quiz.title}":`, { questionCount, questions_and_answers: quiz.questions_and_answers });
      return {
        id: quiz.id,
        type: "quiz",
        title: quiz.title,
        sources: questionCount,
        time: "Reciente",
      };
    }) || []),
  ];

  return (
    <div className={`${ openPanel ? "w-90" : "w-18" } flex flex-col border-l border-border bg-[var(--panel-bg)]`}>
      <div className={`flex items-center border-b border-border px-4 py-3 ${ openPanel ? "justify-between" : "justify-center"}`}>
        <h2 className={`${ openPanel ? "" : "hidden" } text-sm font-medium text-foreground`}>Funciones</h2>
        <button
          onClick={() => setOpenPanel(!openPanel)}
          className="cursor-pointer h-8 w-8 p-2 hover:bg-[var(--hover-bg)] hover:rounded-full"
        >
          <PanelRight className="h-4 w-4" />
        </button>
      </div>

      <div className="flex-1">
        <div className={`grid grid-cols-1 ${ openPanel ? "md:grid-cols-2" : ""} p-4 gap-3`}>
          {studioTools.map((tool, idx, index) => {
            const colorClasses = {
              purple: "bg-[var(--purple-accent)]/10 text-[var(--purple-accent)]",
              green: "bg-[var(--green-accent)]/10 text-[var(--green-accent)]",
              orange: "bg-[var(--orange-accent)]/10 text-[var(--orange-accent)]",
              blue: "bg-[var(--blue-accent)]/10 text-[var(--blue-accent)]",
            }[tool.color]

            return (
              <OptionButton
                key={idx.toString()}
                optionName={tool.optionName}
                icon={tool.icon}
                label={tool.label}
                colorClasses={colorClasses}
                openPanel={openPanel}
              />
            )
          })}
        </div>

        {recentItems.length > 0 && (
        <div className="border-t border-border p-4">
          <h3 className={`${ openPanel ? "mb-3 text-sm font-medium text-foreground" : "hidden"}`}>Recientes</h3>
          <div className="space-y-2">
            {recentItems.map((item) => (
              <div key={item.id}>
                {item.type === "flashcards" ? (
                  <ShowFlashcardsButton flashcardsCount={item.sources} openPanel={openPanel} />
                ) : (
                  <ShowQuizButton item={item} openPanel={openPanel} />
                )}
              </div>
            ))}
          </div>
        </div>
        )}
      </div>

      <div className="border-t border-border p-4">
        <button className={`text-sm text-black font-semibold w-full flex items-center justify-center gap-2 bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] hover:from-[var(--purple-accent)] hover:to-[var(--sidebar-border)]/85 hover:shadow-lg transition-all duration-300 ease-in-out cursor-pointer ${ openPanel ? "py-3 px-6  rounded-full" : "p-3  rounded-lg"}`}>
          <StickyNote  className="h-4 w-4" strokeWidth={2.5}/>
          <span className={`${ openPanel ? "" : "hidden" }`}>Agregar nota</span>
        </button>
      </div>
    </div>
  )
}

