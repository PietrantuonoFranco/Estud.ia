import { MoreVertical, FileText, Clock3 } from "lucide-react";
import Link from "next/link";

import Notebook from "@/app/lib/interfaces/entities/Notebook";
import formatRelativeDate from "@/app/lib/utils/formatRelativeDate";

interface NotebooksGridProps {
  notebooks: Notebook[];
  viewMode: "grid" | "list";
}

export default function NotebooksGrid({ notebooks, viewMode }: NotebooksGridProps) {
  return (
    <>
      {notebooks.map((notebook) => (
        <Link
          href={`/notebook/${notebook.id}`}
          key={notebook.id}
          className={`
            group relative flex cursor-pointer flex-col rounded-xl p-4 ${
              viewMode === "grid" 
                ? "justify-between md:h-48 bg-gradient-to-bl" 
                : "flex-row md:items-center gap-4 bg-gradient-to-l"
            }
            from-primary/1 to-primary/4 border border-0.5 border-primary/10 transition-colors hover:bg-card/80 duration-300
          `}
        >
          <div className={`flex items-start ${
            viewMode === "grid" 
              ? "justify-between"
              : "gap-4"
          }`}>
            <div className={`flex items-center justify-center rounded-lg bg-muted text-lg md:text-2xl ${
              viewMode === "grid" 
                ? "h-6 w-6 md:h-10 md:w-10"
                : "h-10 w-10 md:h-14 md:w-14"
            }`}>
              {notebook.icon}
            </div>
{/*
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
*/}
          </div>
          <div>
            <h3 className={`text-sm xl:text-lg font-medium text-foreground ${viewMode === "grid" ? "mb-2" : "mb-1"}`}>{notebook.title}</h3>
            <p className="flex flex-col sm:flex-row sm:items-center gap-1 text-xs xl:text-sm text-foreground">
              <div className="flex items-center gap-1">
                <FileText className="h-3 w-3" />
                {notebook.sources.length === 1 ? "1 fuente" : `${notebook.sources.length} fuentes`}
              </div>
              
              <span className="hidden sm:inline sm:mx-1">-</span> 
              
              <div className="flex items-center gap-1">
                <Clock3 className="h-3 w-3" />
                {formatRelativeDate(notebook.created_at ?? new Date().toISOString())}
              </div>
            </p>
          </div>
        </Link>
      ))}
    </>
  )
}