"use client"

import { Scale, ThumbsUp, ThumbsDown, Copy, Send } from "lucide-react"

import fonts from "../mocks/fonts.json"
import message from "./components/mocks/message.json"

import MessageInbox from "./components/MessageInbox"
import LLMMessage from "./components/LLMMessage"
import UserMessage from "./components/UserMessage"


export default function ChatPanel() {
  return (
    <div className="flex flex-1 flex-col bg-background">
      <div className="flex items-center justify-between border-b border-border px-6 py-4.5">
        <h2 className="text-sm font-medium text-foreground">Chat</h2>
      </div>

      <div className="flex-1 overflow-y-auto flex-col items-center space-y-2 px-6 py-8">
        <div className="relative mx-auto max-w-3xl space-y-4">
          <div className="flex flex-col items-center gap-6 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--orange-accent)]/20">
              <Scale className="h-8 w-8 text-[var(--orange-accent)]" />
            </div>

            <h1 className="text-4xl font-semibold text-foreground">University Guide to Legislation and Civil Law</h1>

            <p className="text-sm text-muted-foreground">
              {fonts.length === 1 
                ?
                  "1 fuente"
                :
                  fonts.length + " fuentes"
              }
            </p>
          </div>

          <div className="p-6 space-y-6 text-sm leading-relaxed text-foreground">
            <LLMMessage message={message.message}/>
            <UserMessage message={`De la legislación de qué país?`}/>
            <LLMMessage message={`De la República Argentina`}/>
          </div>
          <MessageInbox />
        </div>
      </div>

      <div className="border-t border-border p-2">
        <div className="mx-auto max-w-3xl">
          <div className="flex items-center justify-center text-xs text-muted-foreground">
            <span>Es posible que Estud.IA muestre información imprecisa. Verifica las respuestas.</span>
          </div>
        </div>
      </div>
    </div>
  )
}
