"use client"

import { Pin, ThumbsUp, ThumbsDown, Copy } from "lucide-react"

export default function LLMMessage ({ message }: { message: string | undefined}) {
  return (
    <div className="flex flex-col space-y-2 pr-24">
      <div className="w-fit flex items-center bg-card px-6 py-3 rounded-3xl">
        <p>
          {message}
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