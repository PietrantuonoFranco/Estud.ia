"use client"

import {
  FileText,
  BookOpen,
  HelpCircle,
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
  // { optionName: "summary", icon: FileText, label: "Resumen", color: "orange" },
  { optionName: "quiz", icon: HelpCircle, label: "Cuestionario", color: "purple" },
]

interface StudioPanelProps {
  openPanel: boolean;
}

export default function StudioPanel({ openPanel }: StudioPanelProps) {
  const { quizzes, flashcards } = useChatInformationContext();

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
    <div className={`${ openPanel ? "w-90 opacity-100" : "w-0 md:w-18 opacity-0 md:opacity-100 pointer-events-none md:pointer-events-auto" } flex h-full flex-col overflow-hidden border-l border-border bg-[var(--panel-bg)] transition-[width,opacity] duration-400 ease-in-out`}>
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

{/*
      <div className="w-full border-t border-border p-4">
        <button className={`text-sm text-black font-semibold w-full flex items-center justify-center gap-2 rounded-md bg-gradient-to-br from-primary-accent to-primary/90 shadow-primary/20 hover:bg-gradient-to-br hover:from-primary-accent hover:to-primary hover:shadow-lg transition-all duration-200 ease-in-out cursor-pointer ${ openPanel ? "py-3 px-6" : "p-3"}`}>
          <StickyNote  className="h-4 w-4" strokeWidth={2.5}/>
          <span className={`${ openPanel ? "" : "hidden" }`}>Agregar nota</span>
        </button>
      </div>
*/}
    </div>
  )
}

