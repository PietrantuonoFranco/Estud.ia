"use client"

import { FormEvent, useState } from "react"
import { SendHorizontal } from "lucide-react"
import { useChatInformationContext } from "../../../contexts/ChatInformationContext";

export default function MessageInbox () {
  const [text, setText] = useState("");

  const { notebook, setMessages } = useChatInformationContext();
  
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!notebook) return;

    const cleanText = text.trim();
    if (!cleanText) return;

    const optimisticMessage = {
      id: Date.now(),
      notebook_id: notebook.id,
      is_user_message: true,
      text: cleanText,
    };

    setMessages((prevMessages) => [...prevMessages, optimisticMessage]);
    setText("");
  }
  
  return (
    <form onSubmit={handleSubmit} className="mx-6 sticky -bottom-6  flex items-center gap-3 rounded-full border border-border bg-card text-sm leading-relaxed text-foreground pl-6 pr-1 py-1">
      <input
        type="text"
        placeholder="Comienza a escribir..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full h-full flex-1 bg-card focus:outline-none focus:ring-none"
      />

      <button
        type="submit"
        disabled={!text.trim()}
        className="cursor-pointer flex items-center justify-center h-10 w-10 shrink-0 rounded-full bg-muted-foreground text-card hover:bg-[var(--hover-bg)] hover:text-foreground transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-muted-foreground"
      >
        <SendHorizontal className="h-5 w-5" />
      </button>
    </form>
  )
}