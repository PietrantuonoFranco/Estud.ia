"use client"

import { Plus } from "lucide-react";
import { useState, useMemo, useEffect } from "react"
import { useRouter } from 'next/navigation';

import Notebook from "@/app/lib/interfaces/entities/Notebook";
import { useNotification } from "@/app/contexts/NotificationContext";
import { createNotebook, getAllNotebooks, getNotebooksByUser } from "../../lib/api/entities/NotebooksApi";
import { getPermissionErrorMessage } from "@/app/lib/utils/apiErrorMessage";

import { useAuth } from "../../contexts/AuthContext";
import NotebooksGrid from "./NotebooksGrid";

interface NotebooksContainerProps {
  orderBy: "most-recently" | "title";
  viewMode: "grid" | "list";
  onStartUpload?: () => void;
  onProgressUpdate?: (progress: number) => void;
  onUploadComplete?: () => void;
}

export default function NotebooksContainer ({ orderBy, viewMode, onStartUpload, onProgressUpdate, onUploadComplete }: NotebooksContainerProps) {
  const [notebooks, setNotebooks] = useState<Notebook[]>([]);
  const [userNotebooks, setUserNotebooks] = useState<Notebook[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  const { addNotification } = useNotification();
  const { user } = useAuth();
  
  const router = useRouter();

  // Función para convertir fecha ISO a formato relativo
  

  const sortNotebooks = (data: Notebook[]): Notebook[] => {
    const copy = [...data];

    if (orderBy === "title") {
      return copy.sort((a, b) => a.title.localeCompare(b.title));
    }

    return copy.sort((a, b) => {
      const dateA = new Date(a.created_at ?? 0);
      const dateB = new Date(b.created_at ?? 0);
      return dateB.getTime() - dateA.getTime();
    });
  };

  const sortedUserNotebooks = useMemo(() => {
    return sortNotebooks(userNotebooks);
  }, [orderBy, userNotebooks]);

  const sortedAllNotebooks = useMemo(() => {
    return sortNotebooks(notebooks);
  }, [orderBy, notebooks]);

  const uploadFiles = async (files: FileList) => {
    try {
      onStartUpload?.();

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
      addNotification("Error", permissionMessage ?? "Ocurrió un error al subir el archivo.", "error");
    }
  };

  const handleFilesChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files) return;
    await uploadFiles(files);
    event.target.value = "";
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    if (!isDragging) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = async (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);

    if (!event.dataTransfer?.files?.length) return;
    await uploadFiles(event.dataTransfer.files);
  };

  const fetchUserNotebooks = async () => {
    try {
      if (!user) return;

      const notebooks = await getNotebooksByUser(user?.id);
      
      if (!notebooks) {
        throw new Error("Error al obtener los cuadernos del usuario.");
      }

      setUserNotebooks(notebooks);
    } catch (error) {
      console.error("Error al obtener los cuadernos del usuario:", error);
      addNotification("Error", "Ocurrió un error al obtener los cuadernos del usuario.", "error");
    }
  };

  const fetchNotebooks = async () => {
    try {
      const notebooks = await getAllNotebooks();
      
      if (!notebooks) {
        throw new Error("Error al obtener los cuadernos.");
      }

      setNotebooks(notebooks);
    } catch (error) {
      console.error("Error al obtener los cuadernos del usuario:", error);
      addNotification("Error", "Ocurrió un error al obtener los cuadernos del usuario.", "error");
    }
  };

  useEffect(() => {
    fetchUserNotebooks();
    fetchNotebooks();
  }, []);

  return (
    <>
      <h1 className="text-2xl md:text-4xl font-semibold">Todos los cuadernos</h1>
      <div className={`w-full ${
          viewMode === "grid"
          ? "grid grid-cols-2 md:grid-cols-4 gap-4" 
            : "flex flex-col gap-4"
        }`}
      >
        <NotebooksGrid notebooks={sortedAllNotebooks} viewMode={viewMode} />
      </div>

      <h2 className={`${viewMode === "list" && userNotebooks.length === 0 ? "hidden" : ""} text-2xl md:text-4xl font-semibold`}>Tus cuadernos</h2>
      <div className={`w-full ${
          viewMode === "grid"
            ? "grid grid-cols-2 md:grid-cols-4 gap-4" 
            : "flex flex-col gap-4"
        }`}
      >
        <div
          className={`group cursor-pointer w-full space-y-2 flex justify-center items-center border-2 border-dashed rounded-xl transition-colors duration-300 p-6 ${
            isDragging
              ? "border-primary shadow-lg shadow-primary/20 bg-card/60"
              : "border-border hover:bg-card"
          } ${
            viewMode === "grid" 
              ? "p-8 md:p-0 md:h-48 "
              : "hidden"
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <input type="file" accept="application/pdf" className="hidden" id="file-upload" multiple onChange={handleFilesChange} />

          <label htmlFor="file-upload" className="cursor-pointer h-full w-full flex flex-col items-center justify-center">
            <div className="flex justify-center items-center p-2 rounded-full bg-card group-hover:bg-card/80">
              <Plus className="w-8 h-8" />
            </div>
            <h3 className="mb-2 text-lg text-center font-medium text-foreground">Crear cuaderno</h3>
          </label>
        </div>

        
        <NotebooksGrid notebooks={sortedUserNotebooks} viewMode={viewMode} />
      </div>
    </>
  );
}