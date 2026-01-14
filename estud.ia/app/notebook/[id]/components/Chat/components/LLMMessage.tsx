"use client"

import { Pin, ThumbsUp, ThumbsDown, Copy } from "lucide-react"

const extractResponse = (message: string | undefined): string => {
  if (!message) return "";

  const responseMatch = message.match(
    /(?:\d+\.\s*)?\*\*Respuesta\b(?:\*\*)?\s*[:\-—]?\s*(?:\*\*\s*)?(.+?)(?=\n\d+\.\s|\s*\d+\.\s*\*\*Justificación|\s*\*\*Justificación(?:\*\*)?|$)/is
  );
  
  if (responseMatch && responseMatch[1]) {
    return responseMatch[1].trim();
  }
  
  // If no match is found, return the original message
  return message.trim();
};

export default function LLMMessage ({ message }: { message: string | undefined}) {

  const response = extractResponse(message);
  const formattedMessage = response.replace(/\n/g, '<br/>');

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(response);
    } catch (err) {
      console.error('Error al copiar:', err);
    }
  };

  return (
    <div className="flex flex-col space-y-2 pr-24">
      <div className="w-fit flex items-center bg-[var(--hover-bg)] px-6 py-3 rounded-3xl rounded-bl-md">
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
          type="button"
          onClick={handleCopy}
          className="cursor-pointer text-muted-foreground"
        >
          <Copy className="h-4 w-4" />
        </button>
        
        <button
          type="button"
          onClick={() => {}}
          className="cursor-pointer text-muted-foreground"
        >
          <ThumbsUp className="h-4 w-4" />
        </button>
        
        <button
          type="button"
          onClick={() => {}}
          className="cursor-pointer text-muted-foreground"
        >
          <ThumbsDown className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}