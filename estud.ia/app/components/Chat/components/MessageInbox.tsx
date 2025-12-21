"use client"

import { useState } from "react"
import { Send } from "lucide-react"

export default function MessageInbox () {
  const [message, setMessage] = useState("");

  const handleSubmit = async () => {
    try {

    } catch (error) {
      console.error(error);
    }
  } 
  return (
    <form onSubmit={handleSubmit} className="sticky -bottom-8 w-full flex items-center gap-3 rounded-lg border border-border bg-card text-sm leading-relaxed text-foreground px-4 py-2">
      <input
        type="text"
        placeholder="Comienza a escribir..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="w-full h-full flex-1 bg-card focus:outline-none focus:ring-none"
      />

      <button
        type="submit"
        className="flex items-center justify-center h-8 w-8 shrink-0 rounded-md bg-muted-foreground"
      >
        <Send className="h-4 w-4" />
      </button>
    </form>
  )
}