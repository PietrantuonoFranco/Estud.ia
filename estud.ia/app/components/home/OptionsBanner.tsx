"use client"

import { Check, LayoutGrid, StretchHorizontal, ArrowUpDown, ChevronDown, Plus } from "lucide-react";
import { useState } from "react"
import { useRouter } from 'next/navigation';

import { useNotification } from "@/app/contexts/NotificationContext";
import { createNotebook } from "../../lib/api/entities/NotebooksApi";
import { getPermissionErrorMessage } from "@/app/lib/utils/apiErrorMessage";
import { getOrderByLabel } from "@/app/lib/utils/orderByLabel";
import { useProtectedAction } from "@/app/lib/hooks/useProtectedAction";
import { useProtectedActionWithNotification } from "@/app/lib/hooks/useProtectedActionWithNotification";

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
  const { protectedAction: protectedActionBasic } = useProtectedAction();
  const { protectedAction } = useProtectedActionWithNotification();
  
  const handleFilesChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    protectedAction(async () => {
      try {
        onStartUpload?.();
        const files = event.target.files;
        
        if (!files || files.length === 0) {
          console.error("No se seleccionó ningún archivo");
          return;
        }

        // Validar que el tamaño total no exceda 2MB
        const totalSize = Array.from(files).reduce((acc, file) => acc + file.size, 0);
        const maxSize = 2 * 1024 * 1024; // 2MB en bytes
        
        if (totalSize > maxSize) {
          onUploadComplete?.();
          addNotification("Error", "El tamaño total de los archivos no puede exceder 2MB.", "error");
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
        const permissionMessage = getPermissionErrorMessage(error);
        addNotification("Error", permissionMessage ?? "Ocurrió un error al crear el cuaderno.", "error");
      }
    }, 'crear un cuaderno');
  };
  
  return (
    <div className="mt-2 w-full flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div className="flex items-center gap-2">
        <div className="flex items-center rounded-lg bg-card p-1 gap-2 border border-muted">
          <button
            type="button"
            onClick={() => setViewMode("grid")}
            className={`${
              viewMode === "grid" ?
                "bg-[var(--primary-accent)]/10 text-[var(--primary)]"
              :
                "text-secondary-foreground"
              } cursor-pointer flex items-center p-2.5 rounded-md hover:bg-[var(--hover-bg)]`}
          >
            <LayoutGrid className="h-4 w-4" strokeWidth={2}/>
          </button>
          
          <button
            type="button"
            onClick={() => setViewMode("list")}
            className={`${
              viewMode === "list" ?
                "bg-[var(--primary-accent)]/10 text-[var(--primary)]"
              :
                "text-secondary-foreground" 
            } cursor-pointer flex items-center p-2.5 rounded-md hover:bg-[var(--hover-bg)]`}
          >
            <StretchHorizontal className="h-4 w-4" strokeWidth={2}/>
          </button>
        </div>

        <div className="relative w-1/2">
          <button
            type="button"
            onClick={() => setOpenOrderByMenu(!openOrderByMenu)}
            className="flex justify-between items-center cursor-pointer border border-muted py-2.5 px-4 gap-2 rounded-lg bg-card hover:bg-hover-bg text-[var(--primary)]"
          >
            <div className="flex items-center gap-2">
              <ArrowUpDown className="h-4 w-4"/>
              <span className="whitespace-nowrap min-w-0">{getOrderByLabel(orderBy)}</span>
            </div>
            <ChevronDown className={`h-3 w-3 ${ openOrderByMenu ? "rotate-180" : "rotate-0"} transition-all duration-300`} strokeWidth={3}/>
          </button>

          {openOrderByMenu && (
            <div className="absolute w-full md:w-auto rounded-lg p-2 flex flex-col items-center gap-2 border border-muted bg-card text-secondary-foreground top-14 left-0 z-10">
              <button
                type="button"
                onClick={() => setOrderBy("most-recently")}
                className="cursor-pointer whitespace-nowrap w-full p-2 rounded-md hover:bg-hover-bg"
              >
                Más reciente
              </button>
              
              <button
                type="button"
                onClick={() => setOrderBy("title")}
                className="cursor-pointer w-full py-2 rounded-md hover:bg-hover-bg"
              >
                Título
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="text-sm text-black font-semibold flex items-center justify-center rounded-md bg-gradient-to-br from-primary-accent to-primary/90 shadow-primary/20 hover:bg-gradient-to-br hover:from-primary-accent hover:to-primary hover:shadow-lg transition-all duration-200 ease-in-out cursor-pointer">
        <input type="file" multiple accept="application/pdf" className="hidden" id="file-upload-banner" onChange={handleFilesChange} />
        <label htmlFor="file-upload-banner" className="cursor-pointer rounded-full h-full w-full py-3 px-4 text-sm flex items-center justify-center gap-2">
          <Plus className="h-4 w-4" strokeWidth={3}/>
          <span className="font-semibold">Crear cuaderno</span>
        </label>
      </div>
    </div>
  );
}