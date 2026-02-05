"use client"

import { FilePlusCorner, FileText, Check, PanelLeft, Trash2 } from "lucide-react";
import { useState } from "react";
import { addSourcesToNotebook } from "@/app/lib/api/entities/NotebooksApi";
import { deleteVariousSourcesByNotebookIdAndSourceIds } from "@/app/lib/api/entities/NotebooksApi";
import { useChatInformationContext } from "../contexts/ChatInformationContext";
import { useNotification } from "@/app/contexts/NotificationContext";
import { DeleteModal } from "@/app/components/modal/DeleteModal";
import Source from "@/app/lib/interfaces/entities/Source";


export default function SourcesPanel() {
  const [openPanel, setOpenPanel] = useState(true);
  const [selectedSources, setSelectedSources] = useState<Source[]>([]);
  const [openDeleteVariousModal,setOpenDeleteVariousModal] = useState(false);
  const [tooltip, setTooltip] = useState<{
    visible: boolean;
    text: string;
    x: number;
    y: number
  }>({
    visible:
    false,
    text: "",
    x: 0,
    y: 0
  });

  const { sources, setSources, notebook } = useChatInformationContext();
  const { addNotification } = useNotification();


  const selectSource = (source: Source) => {
    if (selectedSources.includes(source)) {
      setSelectedSources(selectedSources.filter(f => f !== source))
    } else {
      setSelectedSources([...selectedSources, source])
    }
  }

  const showTooltip = (e: React.MouseEvent<HTMLDivElement>, text: string) => {
    const rect = e.currentTarget.getBoundingClientRect();
    setTooltip({
      visible: true,
      text,
      x: rect.right + 34,
      y: rect.top + rect.height / 2,
    });
  };

  const hideTooltip = () => setTooltip(prev => ({ ...prev, visible: false }));
  
  const handleFilesChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    try {
      const files = event.target.files;
      
      if (!files || files.length === 0) {
        console.error("No se seleccionó ningún archivo");
        return;
      }

      const formData = new FormData();

      for (let i = 0; i < files.length; i++) {
        console.log("Subiendo archivos:", files[i].name);
        formData.append("files", files[i]);
      }
      
      const response = await addSourcesToNotebook(notebook?.id!, Array.from(files));

      if (!response) {
        throw new Error("Error al subir el archivo");
      }
      

      setSources(response.sources);
      addNotification("Éxito", "Archivos subidos exitosamente.", "success");
    } catch (error) {
      console.error("Error al subir el archivo:", error);
      addNotification("Error", "Ocurrió un error al subir los archivos.", "error");
    }
  };

  const handleDeleteSources = async () => {
    try {
      const pdf_ids = selectedSources.map(source => source.id);

      const response = await deleteVariousSourcesByNotebookIdAndSourceIds(notebook?.id!, pdf_ids);

      if (!response) {
        throw new Error(`Failed to delete sources`);
      }

      setSelectedSources([]);
      setSources(sources.filter(source => !selectedSources.includes(source)));
      addNotification("Éxito", "Fuentes eliminadas exitosamente.", "success");
    } catch (error) {
      console.error("Error deleting sources:", error);
      addNotification("Error", "Ocurrió un error al eliminar las fuentes.", "error");
    }
  }

  return (
    <>
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
          <div className={`text-sm text-black font-semibold flex items-center justify-center gap-2 bg-gradient-to-br from-[var(--purple-accent)] to-[var(--sidebar-border)] hover:from-[var(--purple-accent)] hover:to-[var(--sidebar-border)]/85 hover:shadow-lg transition-all duration-300 ease-in-out cursor-pointer ${ openPanel ? "w-full py-3 px-6 rounded-full" : "py-2.75 px-1 rounded-lg" }`}>
            <input type="file" accept="application/pdf" multiple className="hidden" id="file-upload" onChange={handleFilesChange} />
            <label htmlFor="file-upload" className="cursor-pointer rounded-lg h-full w-full flex items-center justify-center gap-2">
              <FilePlusCorner className="h-4 w-4" strokeWidth={2.5}/>
              <span className={`${ openPanel ? "font-semibold" : "hidden" }`}>Agregar fuentes</span>
            </label>
          </div>
        </div>


        <div className="flex-1 py-2 border-t border-border bg-[var(--panel-bg)] flex flex-col">
          <div className="flex-1 overflow-y-auto overflow-x-hidden px-4 ">
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
                  className={`${ openPanel ? "cursor-pointer min-h-6 min-w-6 relative border border-gray-500 rounded-md" : "hidden" }`}
                >
                  {selectedSources.length === sources?.length && (
                      <Check className="absolute h-4 w-4 left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 text-[var(--green-accent)]" /> 
                    )}
                </button>
              </div>

              {sources?.map((source, index) => (
                <div
                  key={index}
                  onMouseEnter={(e) => { if (!openPanel) showTooltip(e, source.name); }}
                  onMouseLeave={() => { if (!openPanel) hideTooltip(); }}
                  className={`group relative flex items-center rounded-lg bg-card hover:bg-[var(--hover-bg)] text-sm ${ openPanel ? "justify-between px-3 py-2.5" : "justify-center p-3"}`}
                >
                  <div
                    className="py-1 px-2 flex items-center"
                  >
                    <FileText className="h-4 w-4 text-red-500" />
                    <span className={`${ openPanel ? "font-medium text-foreground ml-3" : "hidden" }`}>{source.name}</span>
                  </div>

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
          </div>

          {selectedSources.length > 0 && (
            <div className="w-full px-4 pb-2 pt-4 mt-2 border-t border-border">
              <button
                type="button"
                onClick={() => setOpenDeleteVariousModal(true)}
                name="delete-selected-sources"
                className={`${ openPanel ? "cursor-pointer w-full flex items-center justify-center text-sm font-semibold text-red-500 py-3 px-6 rounded-3xl bg-red-800/15 hover:hover:bg-red-800/20 hover:shadow-md transition-all duration-300 ease-in-out" : "hidden" }`}
              >
                <Trash2 className="h-4 w-4 mr-3"/>
                Eliminar seleccionadas
              </button>
            </div>
          )}
        </div>
        {/* Global tooltip overlay using fixed positioning to avoid scrollbars */}
        {!openPanel && tooltip.visible && (
          <div
            className="z-50 bg-card border border-border text-sm shadow-lg rounded-md px-3 py-1.5 whitespace-nowrap text-foreground pointer-events-none"
            style={{ position: "fixed", left: tooltip.x, top: tooltip.y, transform: "translateY(-50%)" }}
          >
            {tooltip.text}
          </div>
        )}
      </div>

      <DeleteModal
        isOpen={openDeleteVariousModal}
        title="Eliminar fuentes seleccionadas"
        items={selectedSources}
        onClose={() => setOpenDeleteVariousModal(false)}
        onDelete={handleDeleteSources}
      />
    </>
  )
}
