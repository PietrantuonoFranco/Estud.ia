"use client"

import { Copy, SquarePen } from "lucide-react"

export default function UserMessage ({ message }: { message: string }) {
  return (
    <div className="flex flex-col items-end space-y-2 pl-24">
      <div className=" flex items-center justify-center bg-[var(--hover-bg)] px-4 py-2 rounded-full">
        <p className="text-right">
          {message}
        </p>
      </div>

      <div className="flex items-center gap-4 pt-2">
        <button
          className="cursor-pointer text-muted-foreground"
        >
          <Copy className="h-4 w-4" />
        </button>
        
        <button
          className="cursor-pointer text-muted-foreground"
        >
          <SquarePen className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}