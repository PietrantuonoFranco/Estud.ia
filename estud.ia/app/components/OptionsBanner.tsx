"use client"

import { Check, LayoutGrid, StretchHorizontal, ChevronDown, Plus } from "lucide-react";
import { useState } from "react"

interface OptionsBannerProps {
  orderBy: "most-recently" | "title";
  setOrderBy: (value: "most-recently" | "title") => void;
  viewMode: "grid" | "list";
  setViewMode: (value: "grid" | "list") => void;
}

export default function OptionsBanner ({ orderBy, setOrderBy, viewMode, setViewMode }: OptionsBannerProps) {
  const [openOrderByMenu, setOpenOrderByMenu] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    
  };

  const handleSubmit = () => {
    
  }
  
  return (
    <div className="w-full flex items-center justify-between">
      <div className="flex items-center gap-2">
        <div className="flex items-center rounded-full">
          <button
            type="button"
            onClick={() => setViewMode("grid")}
            className="cursor-pointer flex items-center gap-2 py-4 px-8 rounded-l-full hover:bg-[var(--hover-bg)] bg-[var(--purple-accent)]/10 text-[var(--purple-accent)]"
          >
            <Check className={`${ viewMode === "grid" ? "h-4 w-4" : "hidden" }`} strokeWidth={2.5}/>
            <LayoutGrid className="h-4 w-4" strokeWidth={2.5}/>
          </button>
          
          <button
            type="button"
            onClick={() => setViewMode("list")}
            className="cursor-pointer flex items-center gap-2 py-4 px-8 rounded-r-full hover:bg-[var(--hover-bg)] bg-[var(--purple-accent)]/10 text-[var(--purple-accent)]"
          >
            <Check className={`${ viewMode === "list" ? "h-4 w-4" : "hidden" }`} strokeWidth={3}/>
            <StretchHorizontal className="h-4 w-4" strokeWidth={2.5}/>
          </button>
        </div>

        <div className="relative">
          <button
            type="button"
            onClick={() => setOpenOrderByMenu(!openOrderByMenu)}
            className="cursor-pointer py-3 px-6 flex items-center gap-2 rounded-full bg-[var(--hover-bg)] hover:bg-[var(--purple-accent)]/10 text-[var(--purple-accent)]"
          >
            <span>Ordenar por</span>
            <ChevronDown className={`h-4 w-4 ${ openOrderByMenu ? "rotate-180" : "rotate-0"} transition-all duration-300`} strokeWidth={3}/>
          </button>

          {openOrderByMenu && (
            <div className="absolute w-full rounded-3xl py-2 flex flex-col items-center gap-2 bg-[var(--hover-bg)] text-[var(--purple-accent)] top-14 left-1/2 -translate-x-1/2 z-10">
              <button
                type="button"
                onClick={() => setOrderBy("most-recently")}
                className="cursor-pointer px-4 py-2 rounded-full hover:bg-[var(--purple-accent)]/10"
              >
                Más reciente
              </button>
              
              <button
                type="button"
                onClick={() => setOrderBy("title")}
                className="cursor-pointer px-4 py-2 rounded-full hover:bg-[var(--purple-accent)]/10"
              >
                Título
              </button>
            </div>
          )}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="text-sm text-black font-semibold flex items-center justify-center gap-2 rounded-full bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] to-[var(--purple-accent)] hover:bg-gradient-to-br hover:from-[var(--sidebar-border)] to-[var(--purple-accent)]  transition-all duration-300 ease-in-out cursor-pointer">
        <input type="file" accept="application/pdf" className="hidden" id="file-upload-banner" onChange={handleFileChange} />
        <label htmlFor="file-upload-banner" className="cursor-pointer rounded-full h-full w-full py-3 px-6 flex items-center justify-center gap-2">
          <Plus className="h-4 w-4" strokeWidth={3}/>
          <span className="font-semibold">Crear cuaderno</span>
        </label>
      </form>
    </div>
  );
}