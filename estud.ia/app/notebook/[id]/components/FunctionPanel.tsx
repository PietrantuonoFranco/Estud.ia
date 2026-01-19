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

const studioTools = [
  { optionName: "chat", icon: MessageSquareText, label: "Chat", color: "blue" },
  { optionName: "flashcards", icon: BookOpen, label: "Tarjetas didácticas", color: "green" },
  { optionName: "summary", icon: FileText, label: "Resumen", color: "orange" },
  { optionName: "quiz", icon: HelpCircle, label: "Cuestionario", color: "purple" },
]

const recentItems = [
  { id: 1, type: "quiz", title: "Derecho Cuestionario", sources: 1, time: "Hace 13 d" },
  { id: 1, type: "audio", title: "Arquitectura del Derecho Civil...", sources: 1, time: "Hace 14 d" },
  { id: 1, type: "flashcards", title: "Derecho Fichas", sources: 1, time: "Hace 14 d" },
]

export default function StudioPanel() {
  const { notebook, quizzes, flashcards } = useChatInformationContext();
  
  const [openPanel, setOpenPanel] = useState(true);

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

        <div className="border-t border-border p-4">
          <h3 className={`${ openPanel ? "mb-3 text-sm font-medium text-foreground" : "hidden"}`}>Recientes</h3>
          <div className="space-y-2">
            {recentItems.map((item, idx) => (
              <div
                key={idx}
                className="cursor-pointer group flex items-center gap-3 rounded-lg bg-card p-3 hover:bg-[var(--hover-bg)]"
              >
                <div className={`${ openPanel ? "h-10 w-10" : ""} flex items-center justify-center rounded bg-muted`}>
                  {item.type === "quiz" && <HelpCircle className="h-4 w-4 text-[var(--purple-accent)]" />}
                  {item.type === "audio" && <FileText className="h-4 w-4 text-[var(--orange-accent)]" />}
                  {item.type === "flashcards" && <BookOpen className="h-4 w-4 text-[var(--green-accent)]" />}
                </div>
                <div className={`${ openPanel ? "flex-1 min-w-0" : "hidden"}`}>
                  <p className="text-sm font-medium text-foreground truncate">{item.title}</p>
                  <p className="text-xs text-muted-foreground">
                    {item.sources} fuente · {item.time}
                  </p>
                </div>
                <div className={ openPanel ? "flex items-center gap-1" : "hidden"}>
                  <button className="cursor-pointer h-8 w-8 opacity-0 group-hover:opacity-100">
                    <MoreVertical className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
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

