"use client"

import { Settings, LogOut, LogIn, UserRoundPlus } from "lucide-react"
import Image from "next/image"
import Link from "next/link"

import { useAuth } from "../contexts/AuthContext"
import { useNotification } from "../contexts/NotificationContext"

export default function Header() {
  const { user, logout } = useAuth();
  const { addNotification } = useNotification();

  const handleSettings = async () => {
    try {
      console.log("Ajustes");
    } catch (error) {
      console.error(error);
    }
  }

  const handleLogout = async () => {
    try {
      await logout();
      addNotification("Sesión cerrada", "Has cerrado sesión correctamente.", "success");
    } catch (error) {
      console.error("Error al cerrar sesión:", error);
      addNotification("Error", "Ocurrió un error al cerrar sesión.", "error");
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

      
      {user && (
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleSettings}          
            className="cursor-pointer flex items-center gap-2 py-1.5 px-3 rounded-full hover:bg-[var(--hover-bg)] bg-[var(--purple-accent)]/10 text-[var(--purple-accent)]"
          >
            <Settings className="h-4 w-4" />
            <span>Configuración</span>
          </button>

          <div className="h-100 m-3 w-px bg-[var(--hover-bg)]"></div>
        
          <div className="h-8 w-8">
            <Image src={user.profile_image_url || "/user-avatar.png"} alt="User Avatar" width={32} height={32} className="rounded-full" />
          </div>
  
          <div className="text-muted-foreground rounded-full py-1.5 px-3 bg-card">{user.name} {user.lastname}</div>

          <button
            type="button"
            onClick={handleLogout}
              className="cursor-pointer text-muted-foreground hover:text-[var(--purple-accent)]"
            >
            <LogOut className="h-4 w-4" strokeWidth={2.5}/>
          </button>
        </div>
        )}

      {!user && (
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="cursor-pointer flex items-center gap-2 text-muted-foreground rounded-full py-2 px-4 bg-card hover:bg-[var(--hover-bg)]"
          >
            <LogIn  className="h-4 w-4" />
            <span>Iniciar sesión</span>
          </Link>
          <Link
            href="/register"
            className="cursor-pointer flex items-center gap-2 text-muted-foreground rounded-full py-2 px-4 bg-card hover:bg-[var(--hover-bg)]"
          >
            <UserRoundPlus className="h-4 w-4" />
            <span>Registrarse</span>
          </Link>
        </div>
        )}
    </header>
  )
}
