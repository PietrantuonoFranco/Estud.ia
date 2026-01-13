"use client"

import { MoreVertical, Plus } from "lucide-react";
import { useState, useMemo, useEffect } from "react"
import { useRouter } from 'next/navigation';
import Link from "next/link";

import Notebook from "@/app/lib/interfaces/entities/Notebook";

interface NotebooksContainerProps {
  orderBy: "most-recently" | "title";
  viewMode: "grid" | "list";
}

export default function NotebooksContainer ({ orderBy, viewMode }: NotebooksContainerProps) {
  const [notebooks, setNotebooks] = useState<Notebook[]>([]);
  const router = useRouter();

  const API_URL = process.env.API_URL || 'http://localhost:5000';

  // Función para convertir fecha ISO a formato relativo
  const formatRelativeDate = (dateStr: string): string => {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffMonths = Math.floor(diffDays / 30);
    const diffYears = Math.floor(diffMonths / 12);

    if (diffDays === 0) {
      return "Hoy";
    } else if (diffDays === 1) {
      return "Hace 1 día";
    } else if (diffDays < 30) {
      return `Hace ${diffDays} días`;
    } else if (diffMonths === 1) {
      return "Hace 1 mes";
    } else if (diffMonths < 12) {
      return `Hace ${diffMonths} meses`;
    } else if (diffYears === 1) {
      return "Hace 1 año";
    } else {
      return `Hace ${diffYears} años`;
    }
  };

  // Ordenar notebooks según el criterio seleccionado
  const sortedNotebooks = useMemo(() => {
    const data = [...notebooks];
    
    if (orderBy === "title") {
      return data.sort((a, b) => a.title.localeCompare(b.title));
    } else {
      return data.sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return dateB.getTime() - dateA.getTime();
      });
    }
  }, [orderBy, notebooks]);

  const handleFilesChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    try {
      const files = event.target.files;
      
      if (!files || files.length === 0) {
        console.error("No se seleccionó ningún archivo");
        return;
      }

      const formData = new FormData();

      for (let i = 0; i < files.length; i++) {
        console.log("Subiendo archivo:", files[i].name);
        formData.append("files", files[i]);
      }
      
      const response = await fetch(`${API_URL}/notebooks/`, {
        method: "POST",
        body: formData,
        credentials: 'include', // Enviar cookies
      });

      if (!response.ok) {
        throw new Error("Error al subir el archivo");
      } else {
        alert("Archivo subido exitosamente");
      }

      const result = await response.json();
      const notebookId = result.id;

      router.push(`/notebook/${notebookId}`);
    } catch (error) {
      console.error("Error al subir el archivo:", error);
    }
  };

  const fetchUserNotebooks = async () => {
    try {
      const response = await fetch(`${API_URL}/notebooks/`, {
        method: "GET",
        credentials: 'include', // Enviar cookies
      });
      
      if (!response.ok) {
        throw new Error("Error al obtener los cuadernos del usuario");
      }

      const data = await response.json();
      
      setNotebooks(data);
    } catch (error) {
      console.error("Error al obtener los cuadernos del usuario:", error);
    }
  };

  useEffect(() => {
    fetchUserNotebooks();
  }, []);

  return (
    <>
    <h1 className="text-4xl font-semibold">Tus cuadernos</h1>
    <div className={`w-full ${
        viewMode === "grid" 
          ? "grid grid-cols-4 gap-4" 
          : "flex flex-col gap-4"
      }`}
    >
      <div className={`group cursor-pointer w-full space-y-2 flex justify-center items-center border-2 border-dashed border-border rounded-xl hover:bg-card transition-colors duration-300 p-6 ${
        viewMode === "grid" 
          ? "h-48 "
          : "hidden"
          }
        `}>
        <input type="file" accept="application/pdf" className="hidden" id="file-upload" multiple onChange={handleFilesChange} />

        <label htmlFor="file-upload" className="cursor-pointer h-full w-full flex flex-col items-center justify-center">
          <div className="flex justify-center items-center p-2 rounded-full bg-card group-hover:bg-card/80">
            <Plus className="w-8 h-8" />
          </div>
          <h3 className="mb-2 text-lg font-medium text-foreground">Crear cuaderno</h3>
        </label>
      </div>

      {sortedNotebooks.map((notebook, index) => (
        <Link
          href={`/notebook/${notebook.id}`}
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
            <div className={`flex items-center justify-center rounded-lg bg-muted text-2xl ${
              viewMode === "grid" 
                ? "h-10 w-10"
                : "h-14 w-14"
            }`}>
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
              {notebook.sources.length === 1 ? "1 fuente" : `${notebook.sources.length} fuentes`} · {formatRelativeDate(notebook.date)}
            </p>
          </div>
        </Link>
      ))}
    </div>
    </>
  );
}