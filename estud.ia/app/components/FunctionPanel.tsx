"use client"

import { useState } from "react"
import {
  PanelRight,
  FileText,
  BookOpen,
  HelpCircle,
  MoreVertical,
  StickyNote
} from "lucide-react"

const studioTools = [
  { icon: FileText, label: "Informes", color: "orange" },
  { icon: BookOpen, label: "Tarjetas didácticas", color: "green" },
  { icon: HelpCircle, label: "Cuestionario", color: "purple" },
]

const recentItems = [
  { type: "quiz", title: "Derecho Cuestionario", sources: 1, time: "Hace 13 d" },
  { type: "audio", title: "Arquitectura del Derecho Civil...", sources: 1, time: "Hace 14 d" },
  { type: "flashcards", title: "Derecho Fichas", sources: 1, time: "Hace 14 d" },
]

export default function StudioPanel() {
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
          {studioTools.map((tool, idx) => {
            const Icon = tool.icon
            const colorClasses = {
              purple: "bg-[var(--purple-accent)]/10 text-[var(--purple-accent)]",
              green: "bg-[var(--green-accent)]/10 text-[var(--green-accent)]",
              orange: "bg-[var(--orange-accent)]/10 text-[var(--orange-accent)]",
              gray: "bg-muted/50 text-muted-foreground",
            }[tool.color]

            return (
              <button
                key={idx}
                className={`cursor-pointer flex flex-col w-full gap-2 rounded-lg p-3 text-left transition-colors hover:bg-[var(--hover-bg)] ${colorClasses}`}
              >
                <Icon className="h-4 w-4" />
                <span className={`${ openPanel ? "text-sm font-medium" : "hidden"}`}>{tool.label}</span>
              </button>
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
                  {item.type === "quiz" && <HelpCircle className="h-4 w-4 text-foreground" />}
                  {item.type === "audio" && <FileText className="h-4 w-4 text-foreground" />}
                  {item.type === "flashcards" && <BookOpen className="h-4 w-4 text-foreground" />}
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
        <button className={`text-sm text-black font-semibold w-full flex items-center justify-center gap-2 rounded-full bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] to-[var(--purple-accent)] hover:bg-gradient-to-br hover:from-[var(--sidebar-border)] to-[var(--purple-accent)]  transition-all duration-300 ease-in-out cursor-pointer ${ openPanel ? "py-3 px-6" : "p-3"}`}>
          <StickyNote  className="h-4 w-4" strokeWidth={2.5}/>
          <span className={`${ openPanel ? "" : "hidden" }`}>Agregar nota</span>
        </button>
      </div>
    </div>
  )
}
