"use client"

import { Copy, Pencil } from "lucide-react"

export default function UserMessage ({ message }: { message: string }) {
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message);
    } catch (err) {
      console.error('Error al copiar:', err);
    }
  };

  return (
    <div className="group flex justify-end space-x-4 pl-24">
      <div className="opacity-0 group-hover:opacity-100 flex items-center gap-2 transition-opacity duration-300">
        <button
          type="button"
          onClick={handleCopy}
          className="cursor-pointer text-muted-foreground p-2 hover:bg-[var(--hover-bg)] hover:rounded-full hover:shadow-md transition-shadow duration-300"
        >
          <Copy className="h-4 w-4" />
        </button>
        
        <button
          type="button"
          onClick={() => {}}
          className="cursor-pointer text-muted-foreground p-2 hover:bg-[var(--hover-bg)] hover:rounded-full hover:shadow-md transition-shadow duration-300"
        >
          <Pencil className="h-4 w-4" />
        </button>
      </div>

      <div className=" flex items-center justify-center bg-card px-6 py-3 rounded-3xl rounded-br-md">
          <p className="text-right">
            {message}
          </p>
        </div>
    </div>
  );
}