"use client"

import { Plus, FileText, Check, PanelLeft, Trash2 } from "lucide-react";
import { useState } from "react";

import { useChatInformationContext } from "../contexts/ChatInformationContext";

import Source from "@/app/lib/interfaces/entities/Source";

export default function SourcesPanel() {
  const [openPanel, setOpenPanel] = useState(true);
  const [selectedSources, setSelectedSources] = useState<Source[]>([]);

  const { sources, setSources } = useChatInformationContext();
  
  const API_URL = process.env.API_URL || 'http://localhost:5000';

  const selectSource = (source: Source) => {
    if (selectedSources.includes(source)) {
      setSelectedSources(selectedSources.filter(f => f !== source))
    } else {
      setSelectedSources([...selectedSources, source])
    }
  }
  
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    
  };

  const handleSubmit = () => {
    
  }

  const handleDeleteSources = async () => {
    try {
      const pdf_ids = selectedSources.map(source => parseInt(source.id, 10));

      console.log("Deleting sources with IDs:", pdf_ids);

      const response = await fetch(`${API_URL}/sources/delete-various`, {
        method: "DELETE",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ pdf_ids }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error:", response.status, errorText);
        throw new Error(`Failed to delete sources: ${response.status}`);
      }

      setSelectedSources([]);
      setSources(sources.filter(source => !selectedSources.includes(source)));
    } catch (error) {
      console.error("Error deleting sources:", error);
    }
  }

  const handleDeleteOneSource = async (source: Source) => {
    try {
      const response = await fetch(`${API_URL}/sources/${source.id}`, {
        method: "DELETE",
        credentials: "include",
      });

      if (!response.ok) {
        throw new Error("Failed to delete sources");
      }

      setSelectedSources(selectedSources.filter(s => s !== source));
      setSources(sources.filter(s => s !== source));
    } catch (error) {
      console.error("Error deleting source:", error);
    }
  }

  return (
    <div className={`${ openPanel ? "w-90" : "w-18" } flex flex-col border-r border-border bg-[var(--panel-bg)]`}>
      <div className={`flex items-center border-b border-border px-4 py-3 ${ openPanel ? "justify-between" : "justify-center"}`}>
        <h2 className={`${ openPanel ? "" : "hidden" } text-sm font-medium text-foreground`}>Fuentes</h2>

        <button
          type="button"
          onClick={() => setOpenPanel(!openPanel)}
          className="cursor-pointer h-8 w-8 p-2 hover:bg-[var(--hover-bg)] hover:rounded-full"
        >
          <PanelLeft className="h-4 w-4" />
        </button>
      </div>

      <div className="p-4">
        <form onSubmit={handleSubmit} className={`text-sm text-black font-semibold w-full flex items-center justify-center gap-2 rounded-full bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] to-[var(--purple-accent)] hover:bg-gradient-to-br hover:from-[var(--sidebar-border)] to-[var(--purple-accent)]  transition-all duration-300 ease-in-out cursor-pointer `}>
          <input type="file" accept="application/pdf" className="hidden" id="file-upload" onChange={handleFileChange} />
          <label htmlFor="file-upload" className="cursor-pointer rounded-full h-full w-full py-3 px-6 flex items-center justify-center gap-2">
            <Plus className="h-4 w-4" strokeWidth={3}/>
            <span className={`${ openPanel ? "font-semibold" : "hidden" }`}>Agregar fuentes</span>
          </label>
        </form>
      </div>


      <div className="flex-1 py-2 px-4 border-t border-border bg-[var(--panel-bg)]">
        <div className="h-[calc(100vh-20rem)]">
          <div className="space-y-2">
            <div className={`${ openPanel ? "flex items-center justify-between rounded-lg px-3 py-2 text-sm hover:bg-[var(--hover-bg)] group" : "hidden"}`}>
              <span className="text-muted-foreground font-semibold py-1 px-2">Seleccionar todas las fuentes</span>

              <button
                type="button"
                onClick={() => setSelectedSources(
                  selectedSources.length >= 1 ?
                    []
                  :
                    sources ?? []
                )}
                className={`${ openPanel ? "cursor-pointer h-6 w-6 relative border border-gray-500 rounded-md" : "hidden" }`}
              >
                {selectedSources.length === sources?.length && (
                    <Check className="absolute h-4 w-4 left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 text-[var(--green-accent)]" /> 
                  )}
              </button>
            </div>

            {sources?.map((source, index) => (
              <div key={index} className={`group flex items-center rounded-lg bg-[var(--hover-bg)] text-sm ${ openPanel ? "justify-between px-3 py-2.5" : "justify-center p-3"}`}>
                <div className="group-hover:hidden flex items-center py-1 px-2">
                  <FileText className="h-4 w-4 text-red-500" />
                  <span className={`${ openPanel ? "font-medium text-foreground ml-3" : "hidden" }`}>{source.name}</span>
                </div>

                <button
                  type="button"
                  onClick={() => handleDeleteOneSource(source)}
                  name="delete-source"
                  className={`${ openPanel ? "cursor-pointer hidden group-hover:flex items-center font-medium text-red-500 py-1 px-2 rounded-md hover:bg-red-800/15 hover:shadow-md transition-all duration-200 ease-in-out" : "hidden" }`}
                >
                  <Trash2 className="h-4 w-4 mr-3"/>
                  Eliminar
                </button>

                <button
                  type="button"
                  onClick={() => selectSource(source)}
                  className={`${ openPanel ? "cursor-pointer h-6 w-6 relative border border-gray-500 rounded-md" : "hidden" }`}
                >
                  {selectedSources.includes(source) && (
                    <Check className="absolute h-4 w-4 left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 text-[var(--green-accent)]" /> 
                  )}
                </button>
              </div>
            ))}
          </div>

          {selectedSources.length > 0 && (
            <div className="w-full h-full flex flex-col items-center justify-end py-2">
              <button
                type="button"
                onClick={() => handleDeleteSources()}
                name="delete-selected-sources"
                className={`${ openPanel ? "cursor-pointer w-full flex items-center justify-center font-medium text-red-500 py-3 px-6 rounded-3xl bg-gradient-to-br from-red-800/25 to-red-800/15 hover:to-red-800/25 hover:shadow-md transition-all duration-200 ease-in-out" : "hidden" }`}
              >
                <Trash2 className="h-4 w-4 mr-3"/>
                Eliminar fuentes seleccionadas
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
