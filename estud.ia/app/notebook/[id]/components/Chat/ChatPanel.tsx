"use client"

import MessageInbox from "./components/MessageInbox"
import LLMMessage from "./components/LLMMessage"
import UserMessage from "./components/UserMessage"

import { useChatInformationContext } from "../../contexts/ChatInformationContext";

export default function ChatPanel() {
  const { notebook, messages, sources } = useChatInformationContext();

  return (
    <div className="flex flex-1 flex-col bg-background">
      <div className="flex items-center justify-between border-b border-border px-6 py-4.5">
        <h2 className="text-sm font-medium text-foreground">Chat</h2>
      </div>

      <div className="flex-1 overflow-y-auto flex-col items-center space-y-2 px-6 py-8">
        <div className="relative mx-auto max-w-3xl space-y-4">
          <div className="flex flex-col items-center gap-6 text-center">
            <div className="flex text-4xl h-16 w-16 items-center justify-center rounded-full bg-[var(--hover-bg)]">
              {notebook?.icon}
            </div>

            <h1 className="text-4xl font-semibold text-foreground">{notebook?.title}</h1>
            <p className="text-sm text-muted-foreground">
              {sources.length === 1 
                ?
                  "1 fuente"
                :
                  sources.length + " fuentes"
              }
            </p>
          </div>

          <div className="p-6 space-y-6 text-sm leading-relaxed text-foreground">
            <LLMMessage message={notebook?.description}/>

            {messages?.map((message, index) => (
              message.is_user_message ? 
                <UserMessage key={index} message={message.text} />
              :
                <LLMMessage key={index} message={message.text} />
            ))}
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
