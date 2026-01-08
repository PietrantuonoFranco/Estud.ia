"use client"

import { useState } from "react"
import { SendHorizontal } from "lucide-react"

export default function MessageInbox () {
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    try {

    } catch (error) {
      console.error(error);
    }
  } 
  return (
    <form onSubmit={handleSubmit} className="mx-6 sticky -bottom-6  flex items-center gap-3 rounded-full border border-border bg-card text-sm leading-relaxed text-foreground pl-6 pr-1 py-1">
      <input
        type="text"
        placeholder="Comienza a escribir..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="w-full h-full flex-1 bg-card focus:outline-none focus:ring-none"
      />

      <button
        type="submit"
        className="cursor-pointer flex items-center justify-center h-10 w-10 shrink-0 rounded-full bg-muted-foreground text-card hover:bg-[var(--hover-bg)] hover:text-foreground transition-colors duration-300"
      >
        <SendHorizontal className="h-5 w-5" />
      </button>
    </form>
  )
}