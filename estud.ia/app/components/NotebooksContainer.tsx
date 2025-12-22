"use client"

import { MoreVertical, Plus } from "lucide-react";
import { useState, useMemo } from "react"

import notebooksData from "./mocks/notebooksData.json"

interface Notebook {
  id: number
  title: string
  source: string
  icon: string
  date: string
  sourcesCount: number
}

interface NotebooksContainerProps {
  orderBy: "most-recently" | "title";
  viewMode: "grid" | "list";
}

export default function NotebooksContainer ({ orderBy, viewMode }: NotebooksContainerProps) {
  const [notebooks, setNotebooks] = useState<Notebook[]>([]);

  // Función para parsear fechas en español
  const parseDate = (dateStr: string): Date => {
    if (dateStr.includes("Hace")) {
      const days = parseInt(dateStr.match(/\d+/)?.[0] || "0");
      const date = new Date();
      date.setDate(date.getDate() - days);
      return date;
    }
    
    const months: { [key: string]: number } = {
      'ene': 0, 'feb': 1, 'mar': 2, 'abr': 3, 'may': 4, 'jun': 5,
      'jul': 6, 'ago': 7, 'sept': 8, 'oct': 9, 'nov': 10, 'dic': 11
    };
    
    const parts = dateStr.split(' ');
    if (parts.length === 3) {
      const day = parseInt(parts[0]);
      const month = months[parts[1]];
      const year = parseInt(parts[2]);
      return new Date(year, month, day);
    }
    
    return new Date();
  };

  // Ordenar notebooks según el criterio seleccionado
  const sortedNotebooks = useMemo(() => {
    const data = [...notebooksData];
    
    if (orderBy === "title") {
      return data.sort((a, b) => a.title.localeCompare(b.title));
    } else {
      return data.sort((a, b) => {
        const dateA = parseDate(a.date);
        const dateB = parseDate(b.date);
        return dateB.getTime() - dateA.getTime();
      });
    }
  }, [orderBy]);

  const handleSubmit = () => {
    
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    
  };

  return (
    <>
    <h1 className="text-4xl font-semibold">Tus cuadernos</h1>
    <div className={`w-full ${
        viewMode === "grid" 
          ? "grid grid-cols-4 gap-4" 
          : "flex flex-col gap-4"
      }`}
    >
      <form onSubmit={handleSubmit} className={`group cursor-pointer w-full space-y-2 flex justify-center items-center border-2 border-dashed border-border rounded-xl hover:bg-card transition-colors duration-300 p-6 ${
        viewMode === "grid" 
          ? "h-48 "
          : "hidden"
          }
        `}>
        <input type="file" accept="application/pdf" className="hidden" id="file-upload" onChange={handleFileChange} />

        <label htmlFor="file-upload" className="cursor-pointer h-full w-full flex flex-col items-center justify-center">
          <div className="flex justify-center items-center p-2 rounded-full bg-card group-hover:bg-card/80">
            <Plus className="w-8 h-8" />
          </div>
          <h3 className="mb-2 text-lg font-medium text-foreground">Crear cuaderno</h3>
        </label>
      </form>

      {sortedNotebooks.map((notebook, index) => (
        <div
          key={notebook.id}
          className={`
            group relative flex cursor-pointer flex-col rounded-xl p-4 ${
              viewMode === "grid" 
                ? "justify-between h-48 bg-gradient-to-bl" 
                : "flex-row items-center gap-4 bg-gradient-to-l"
            }
            from-transparent to-purple-700/15 transition-colors hover:bg-card/80 duration-300
          `}
        >
          <div className={`flex items-start ${
            viewMode === "grid" 
              ? "justify-between"
              : "gap-4"
          }`}>
            <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-muted text-2xl">
              {notebook.icon}
            </div>
            <button
              type="button"
              className={`cursor-pointer absolute p-2 rounded-full bg-card hover:bg-card/80 opacity-0 group-hover:opacity-100 transition-opacity duration-300 right-4 ${
                viewMode === "grid" 
                  ? "top-4"
                  : "top-1/2 -translate-y-1/2"
              }`}
            >
              <MoreVertical className="h-4 w-4" />
            </button>
          </div>
          <div>
            <h3 className={`text-lg font-medium text-foreground ${viewMode === "grid" ? "mb-2" : "mb-1"}`}>{notebook.title}</h3>
            <p className="text-sm text-foreground">
              {notebook.sourcesCount} fuente · {notebook.date}
            </p>
          </div>
        </div>
      ))}
    </div>
    </>
  );
}