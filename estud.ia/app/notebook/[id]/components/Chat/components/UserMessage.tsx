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
    <div className="group flex flex-col md:flex-row justify-end space-y-2 space-x-4 pl-6 md:pl-24">
      <div className="hidden md:flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
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
          <Pencil className="h-4 w-4" />
        </button>
*/}
      </div>

      <div className="ml-auto md:ml-0 mr-0 w-fit max-w-[80%] inline-flex items-center justify-end bg-card px-6 py-3 rounded-3xl rounded-br-md">
        <p className="text-left">
          {message}
        </p>
      </div>

      <div className="flex md:hidden items-center justify-end gap-2 ">
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
          <Pencil className="h-4 w-4" />
        </button>
*/}
        </div>
    </div>
  );
}