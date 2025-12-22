"use client"

import { MoreVertical, Plus } from "lucide-react";
import { useState } from "react"

import notebooksData from "./mocks/notebooksData.json"

interface Notebook {
  id: number
  title: string
  source: string
  icon: string
  date: Date
  sourcesCount: number
}


export default function NotebooksContainer () {
  const [notebooks, setNotebooks] = useState<Notebook[]>([]);

  const handleSubmit = () => {
    
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    
  };

  return (
    <div className="w-full grid grid-cols-4 gap-4">
      <form onSubmit={handleSubmit} className="group cursor-pointer w-full h-48 space-y-2 flex flex-col justify-center items-center border-2 border-dashed border-border rounded-xl hover:bg-card transition-colors duration-300">
        <input type="file" accept="application/pdf" className="hidden" id="file-upload" onChange={handleFileChange} />

        <label htmlFor="file-upload" className="cursor-pointer h-full w-full flex flex-col items-center justify-center">
          <div className="flex justify-center items-center p-2 rounded-full bg-card group-hover:bg-card/80">
            <Plus className="w-8 h-8" />
          </div>
          <h3 className="mb-2 text-lg font-medium text-foreground">Crear cuaderno</h3>
        </label>
      </form>

      {notebooksData.map((notebook, index) => (
        <div
          key={notebook.id}
          className="group relative flex h-48 cursor-pointer flex-col justify-between rounded-xl p-4 bg-gradient-to-bl from-transparent to-purple-700/15 transition-colors hover:bg-card/80"
        >
          <div className="flex items-start justify-between">
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-muted text-2xl">
              {notebook.icon}
            </div>
            <button
              type="button"
              className="h-8 w-8 opacity-0 transition-opacity group-hover:opacity-100"
            >
              <MoreVertical className="h-4 w-4" />
            </button>
          </div>
          <div>
            <h3 className="mb-2 text-lg font-medium text-foreground">{notebook.title}</h3>
            <p className="text-sm text-foreground">
              {notebook.sourcesCount} fuente · {notebook.date}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}