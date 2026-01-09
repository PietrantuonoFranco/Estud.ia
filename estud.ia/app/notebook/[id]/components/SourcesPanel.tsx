"use client"

import { Plus, FileText, Check, PanelLeft } from "lucide-react";
import fonts from "./mocks/fonts.json";
import { useState } from "react";

import { useChatInformationContext } from "../contexts/ChatInformationContext";

interface Font  {
  name: string
}

export default function SourcesPanel() {
  const [openPanel, setOpenPanel] = useState(true);
  const [selectedFonts, setSelectedFonts] = useState<Font[]>([]);

  const { notebook } = useChatInformationContext();

  const selectFont = (font: Font) => {
    if (selectedFonts.includes(font)) {
      setSelectedFonts(selectedFonts.filter(f => f !== font))
    } else {
      setSelectedFonts([...selectedFonts, font])
    }
  }
  
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    
  };

  const handleSubmit = () => {
    
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


      <div className="flex-1 px-4">
        <div className="h-[calc(100vh-20rem)]">
          <div className="space-y-2">
            <div className={`${ openPanel ? "flex items-center justify-between rounded-lg px-3 py-2 text-sm hover:bg-[var(--hover-bg)]" : "hidden"}`}>
              <span className="text-muted-foreground font-semibold">Seleccionar todas las fuentes</span>
              
              <button
                type="button"
                onClick={() => setSelectedFonts(
                  selectedFonts.length >= 1 ?
                    []
                  :
                    fonts
                )}
                className={`${ openPanel ? "cursor-pointer h-6 w-6 relative border border-gray-500 rounded-md" : "hidden" }`}
              >
                {selectedFonts.length === fonts.length && (
                    <Check className="absolute h-4 w-4 left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 text-[var(--green-accent)]" /> 
                  )}
              </button>
            </div>

            {fonts.map((font, index) => (
              <div key={index} className={`flex items-center rounded-lg bg-[var(--hover-bg)] text-sm ${ openPanel ? "justify-between px-3 py-2.5" : "justify-center p-3"}`}>
                <div className="flex items-center">
                  <FileText className="h-4 w-4 text-red-500" />
                  <span className={`${ openPanel ? "font-medium text-foreground ml-3" : "hidden" }`}>{font.name}</span>
                </div>

                <button
                  type="button"
                  onClick={() => selectFont(font)}
                  className={`${ openPanel ? "cursor-pointer h-6 w-6 relative border border-gray-500 rounded-md" : "hidden" }`}
                >
                  {selectedFonts.includes(font) && (
                    <Check className="absolute h-4 w-4 left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 text-[var(--green-accent)]" /> 
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
