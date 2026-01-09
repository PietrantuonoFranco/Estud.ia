"use client"

import { Pin, ThumbsUp, ThumbsDown, Copy } from "lucide-react"

const extractResponse = (message: string | undefined): string => {
  if (!message) return "";
  
  // Buscar el patrón de respuesta entre "**Respuesta:**" y "2. **Justificación"
  const responseMatch = message.match(/\*\*Respuesta:\*\*\s*(.+?)(?=\s*2\.\s*\*\*Justificación|$)/s);
  
  if (responseMatch && responseMatch[1]) {
    return responseMatch[1].trim();
  }
  
  // Si no encuentra el patrón, devuelve el mensaje original sin etiquetas
  return message.replace(/^<|>$/g, "").trim();
};

export default function LLMMessage ({ message }: { message: string | undefined}) {

  const response = extractResponse(message);
  const formattedMessage = response.replace(/\n/g, '<br/>');

  return (
    <div className="flex flex-col space-y-2 pr-24">
      <div className="w-fit flex items-center bg-card px-6 py-3 rounded-3xl">
        <p>
          {formattedMessage ? (
            <span
              className="whitespace-pre-wrap" dangerouslySetInnerHTML={{ __html: formattedMessage }} />
          ) : (
            <></>
          )}
        </p>
      </div>

      <div className="flex items-center gap-4 pt-2">
        <button
          className="cursor-pointer flex items-center gap-2 text-muted-foreground px-3 py-1.5 rounded-full border border-border"
        >
          <Pin className="h-4 w-4" />
          Guardar en las notas
        </button>

        <button
          className="cursor-pointer text-muted-foreground"
        >
          <Copy className="h-4 w-4" />
        </button>
        
        <button
          className="cursor-pointer text-muted-foreground"
        >
          <ThumbsUp className="h-4 w-4" />
        </button>
        
        <button
          className="cursor-pointer text-muted-foreground"
        >
          <ThumbsDown className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}