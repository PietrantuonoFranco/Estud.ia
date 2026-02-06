"use client"

import { Check, LayoutGrid, StretchHorizontal, ChevronDown, Plus } from "lucide-react";
import { useState } from "react"
import { useRouter } from 'next/navigation';

import { useNotification } from "@/app/contexts/NotificationContext";
import { createNotebook } from "../../lib/api/entities/NotebooksApi";

interface OptionsBannerProps {
  orderBy: "most-recently" | "title";
  setOrderBy: (value: "most-recently" | "title") => void;
  viewMode: "grid" | "list";
  setViewMode: (value: "grid" | "list") => void;
  onStartUpload?: () => void;
  onProgressUpdate?: (progress: number) => void;
  onUploadComplete?: () => void;
}

export default function OptionsBanner ({ orderBy, setOrderBy, viewMode, setViewMode, onStartUpload, onProgressUpdate, onUploadComplete }: OptionsBannerProps) {
  const [openOrderByMenu, setOpenOrderByMenu] = useState(false);
  const router = useRouter();
  const { addNotification } = useNotification(); 
  
  const handleFilesChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    try {
      onStartUpload?.();
      const files = event.target.files;
      
      if (!files || files.length === 0) {
        console.error("No se seleccionó ningún archivo");
        return;
      }
      
      onProgressUpdate?.(30);
      
      const notebook = await createNotebook(files as unknown as File[]);

      onProgressUpdate?.(70);

      if (!notebook) {
        throw new Error("Error al subir el archivo");
      }

      const notebookId = notebook.id;

      onProgressUpdate?.(90);
      
      addNotification("Éxito", "El cuaderno se creó exitosamente.", "success");
      
      setTimeout(() => {
        onUploadComplete?.();
        router.push(`/notebook/${notebookId}`);
      }, 100);
    } catch (error) {
      console.error("Error al subir el archivo:", error);
      onUploadComplete?.();
      addNotification("Error", "Ocurrió un error al crear el cuaderno.", "error");
    }
  };
  
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

      <div className="text-sm text-black font-semibold flex items-center justify-center gap-2 rounded-full bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] to-[var(--purple-accent)] hover:bg-gradient-to-br hover:from-[var(--sidebar-border)] to-[var(--purple-accent)]  transition-all duration-300 ease-in-out cursor-pointer">
        <input type="file" multiple accept="application/pdf" className="hidden" id="file-upload-banner" onChange={handleFilesChange} />
        <label htmlFor="file-upload-banner" className="cursor-pointer rounded-full h-full w-full py-3 px-6 flex items-center justify-center gap-2">
          <Plus className="h-4 w-4" strokeWidth={3}/>
          <span className="font-semibold">Crear cuaderno</span>
        </label>
      </div>
    </div>
  );
}