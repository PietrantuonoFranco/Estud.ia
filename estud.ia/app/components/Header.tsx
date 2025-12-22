"use client"

import { Settings } from "lucide-react"
import Image from "next/image"
import Link from "next/link"

export default function Header() {

  const handleSettings = async () => {
    try {
      console.log("Ajustes")
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-[var(--panel-bg)] py-3 px-6">
      <Link href="/" className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg">
          <Image  src="/favicon.png" alt="Estud.IA Logo" width={32} height={32} className="rounded-full" />
        </div>
        <h1 className="text-lg font-medium text-foreground">Estud.IA</h1>
      </Link>

      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={handleSettings}          
          className="cursor-pointer flex items-center gap-2 text-muted-foreground rounded-full py-2 px-4 bg-card hover:bg-[var(--hover-bg)]"
        >
          <Settings className="h-4 w-4" />
          <span>Configuración</span>
        </button>
        
        <div className="h-8 w-8">
          <Image src="/user-avatar.png" alt="User Avatar" width={32} height={32} className="rounded-full" />
        </div>
        <div className="rounded bg-primary px-2 py-1 text-xs font-medium text-primary-foreground">Jhon Pérez</div>
      </div>
    </header>
  )
}
