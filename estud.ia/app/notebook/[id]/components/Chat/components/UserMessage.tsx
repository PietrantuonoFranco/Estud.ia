"use client"

import { Copy, SquarePen } from "lucide-react"

export default function UserMessage ({ message }: { message: string }) {
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message);
    } catch (err) {
      console.error('Error al copiar:', err);
    }
  };

  return (
    <div className="flex flex-col items-end space-y-2 pl-24">
      <div className=" flex items-center justify-center bg-[var(--hover-bg)] px-6 py-3 rounded-3xl">
        <p className="text-right">
          {message}
        </p>
      </div>

      <div className="flex items-center gap-4 pt-2">
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
          <SquarePen className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}