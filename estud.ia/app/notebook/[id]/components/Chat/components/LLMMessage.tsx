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

export default function LLMMessage ({ message, isLoading }: { message: string | undefined, isLoading?: boolean}) {

  const response = extractResponse(message);
  const formattedMessage = response.replace(/\n/g, '<br/>');

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(response);
    } catch (err) {
      console.error('Error al copiar:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col space-y-2 pr-6 md:pr-24">
        <div className="w-fit flex items-center bg-[var(--hover-bg)] px-6 py-3 rounded-3xl rounded-bl-md">
          <svg xmlns="http://www.w3.org/2000/svg" width="34px" height="34px" viewBox="0 0 24 24"><circle cx={18} cy={12} r={0} fill="currentColor"><animate attributeName="r" begin={0.67} calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx={12} cy={12} r={0} fill="currentColor"><animate attributeName="r" begin={0.33} calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx={6} cy={12} r={0} fill="currentColor"><animate attributeName="r" begin={0} calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col space-y-2 pr-6 md:pr-24">
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

      <div className="flex items-center gap-2">
{/*
        <button
          className="cursor-pointer flex items-center gap-2 text-muted-foreground p-1.5 md:px-3 rounded-full border border-border  hover:bg-card/50 hover:shadow-md transition-shadow duration-300"
        >
          <Pin className="h-4 w-4" />
          <span className="hidden md:inline whitespace-pre-wrap">Guardar en las notas</span>
        </button>
*/}
        <button
          type="button"
          onClick={handleCopy}
          className="cursor-pointer text-muted-foreground p-2 hover:bg-[var(--hover-bg)] hover:rounded-full hover:shadow-md transition-shadow duration-300"
        >
          <Copy className="h-4 w-4" />
        </button>
{/*
        <button
          type="button"
          onClick={() => {}}
          className="cursor-pointer text-muted-foreground p-2 hover:bg-[var(--hover-bg)] hover:rounded-full hover:shadow-md transition-shadow duration-300"
        >
          <ThumbsUp className="h-4 w-4" />
        </button>
        
        <button
          type="button"
          onClick={() => {}}
          className="cursor-pointer text-muted-foreground p-2 hover:bg-[var(--hover-bg)] hover:rounded-full hover:shadow-md transition-shadow duration-300"
        >
          <ThumbsDown className="h-4 w-4" />
        </button>
*/}
      </div>
    </div>
  );
}