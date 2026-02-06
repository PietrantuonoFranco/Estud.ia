"use client"

import { useRef, useEffect } from "react"
import { MessageSquareText } from "lucide-react"

import MessageInbox from "./components/MessageInbox"
import LLMMessage from "./components/LLMMessage"
import UserMessage from "./components/UserMessage"

import { useChatInformationContext } from "../../contexts/ChatInformationContext";

export default function ChatPanel() {
  const { notebook, messages, sources } = useChatInformationContext();
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="flex flex-1 flex-col bg-background">
      <div className="flex-1 overflow-y-auto flex-col items-center space-y-2 px-6 pt-8" ref={scrollContainerRef}>
        <div className="mx-auto max-w-3xl space-y-6 pb-6">
          <div className="flex flex-col items-center gap-3 md:gap-6 text-center">
            <div className="flex text-3xl md:text-4xl h-12 w-12 md:h-16 md:w-16 items-center justify-center rounded-full bg-[var(--hover-bg)]">
              {notebook?.icon}
            </div>

            <h1 className="text-3xl md:text-4xl font-semibold text-foreground">{notebook?.title}</h1>
            <p className="text-sm text-muted-foreground">
              {sources.length === 1 
                ?
                  "1 fuente"
                :
                  sources.length + " fuentes"
              }
            </p>
          </div>

          <div className="px-3 md:px-6 space-y-3 text-sm leading-relaxed text-foreground">
            <LLMMessage message={notebook?.description}/>

            {messages?.map((message, index) => (
              message.is_user_message ? 
                <UserMessage key={index} message={message.text} />
              :
                <LLMMessage key={index} message={message.text} isLoading={message.isLoading} />
            ))}
          </div>
        </div>
      </div>

      <div className="sticky bottom-0 w-full flex flex-col items-center space-y-4">
        <div className="flex items-center justify-center w-full px-6 md:px-12">
          <MessageInbox />
        </div>
        <div className="border-t border-border p-2 bg-background w-full">
          <div className="mx-auto max-w-3xl">
            <div className="flex items-center justify-center text-xs text-center text-muted-foreground">
              <span>Es posible que Estud.IA muestre información imprecisa. Verifica las respuestas.</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
