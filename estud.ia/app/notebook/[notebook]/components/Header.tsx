"use client"

import { Share2, Settings} from "lucide-react"
import Image from "next/image"

export default function Header() {
  const handleShare = async () => {
    try {
      console.log("Compartir")
    } catch (error) {
      console.error(error)
    }
  }

  const handleSettings = async () => {
    try {
      console.log("Ajustes")
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-[var(--panel-bg)] px-6">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg">
          <Image  src="/favicon.png" alt="Estud.IA Logo" width={32} height={32} className="rounded-full" />
        </div>
        <h1 className="text-lg font-medium text-foreground">University Guide to Legislation and Civil Law</h1>
      </div>

      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={handleShare}
          className="cursor-pointer text-muted-foreground rounded-full p-2 bg-card hover:bg-[var(--hover-bg)]"
        >
          <Share2 className="h-4 w-4" />
        </button>

        <button
          type="button"
          onClick={handleSettings}          
          className="cursor-pointer text-muted-foreground rounded-full p-2 bg-card hover:bg-[var(--hover-bg)]"
        >
          <Settings className="h-4 w-4" />
        </button>
        
        <div className="h-8 w-8">
          <Image src="/user-avatar.png" alt="User Avatar" width={32} height={32} className="rounded-full" />
        </div>
        <div className="rounded bg-primary px-2 py-1 text-xs font-medium text-primary-foreground">Jhon Pérez</div>
      </div>
    </header>
  )
}
