"use client"

import { useState } from "react"
import { Menu, X, Settings, LogOut, LogIn, UserRoundPlus } from "lucide-react"
import Image from "next/image"
import Link from "next/link"

import { useAuth } from "../../contexts/AuthContext"
import { useNotification } from "../../contexts/NotificationContext"

export default function Header() {
  const [open, setOpen] = useState(false);

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
    <header className="relative flex h-16 items-center justify-between border-b border-border bg-[var(--panel-bg)] py-3 px-6 lg:px-42 z-2000">
      <Link href="/" className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg">
          <Image  src="/favicon.png" alt="Estud.IA Logo" width={32} height={32} className="rounded-full" />
        </div>
        <h1 className="hidden md:inline text-lg font-medium text-foreground pt-1">Estud<span className="text-primary">.IA</span></h1>
      </Link>

      <div className="w-full flex sm:hidden items-center justify-end">
        <button
          type="button"
          onClick={() => setOpen(!open)}
          className="cursor-pointer"
        >
          {!open ? <Menu className="h-6 w-6" /> : <X className="h-6 w-6" />}
        </button>
      </div>

      <div className="w-full hidden sm:flex items-center justify-end">
        {user && (
          <div className="flex items-center gap-1">
            <div className="ml-6 h-10 w-10">
              {user.profile_image_url !== null ? (
                <Image src={user.profile_image_url || "/user-avatar.png"} alt="User Avatar" width={32} height={32} className="rounded-full" />
              ) : (
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary-accent/10 text-sm text-primary font-semibold">
                  {user.name.charAt(0).toUpperCase()}{user.lastname.charAt(0).toUpperCase()}
                </div>
              )}
            </div>
    
            <div className="text-foreground text-sm font-semibold mr-2">{user.name} {user.lastname}</div>

            <button
              type="button"
              onClick={handleSettings}          
              className="cursor-pointer flex items-center gap-2 p-1.5 rounded-full hover:bg-[var(--hover-bg)] bg-card text-foreground"
            >
              <Settings className="h-4 w-4" />
            </button>
            <button
              type="button"
              onClick={handleLogout}
                className="cursor-pointer p-1.5 rounded-full hover:bg-hover-bg bg-primary-accent/10 text-primary"
              >
              <LogOut className="h-4 w-4" strokeWidth={2.5}/>
            </button>
          </div>
          )}

        {!user && (
          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="cursor-pointer flex items-center gap-2 text-muted-foreground rounded-lg py-2 px-4 bg-card hover:bg-[var(--hover-bg)]"
            >
              <LogIn  className="h-4 w-4" />
              <span>Iniciar sesión</span>
            </Link>
            <Link
              href="/register"
              className="cursor-pointer flex items-center gap-2 text-muted-foreground rounded-lg py-2 px-4 bg-card hover:bg-[var(--hover-bg)]"
            >
              <UserRoundPlus className="h-4 w-4" />
              <span>Registrarse</span>
            </Link>
          </div>
          )}
      </div>

      <div className={`absolute top-full right-2 mt-2 w-42 rounded-lg bg-card shadow-lg border border-border bg-[var(--panel-bg)] z-2000 ${open ? "block" : "hidden"}`}>
          {user ? (
            <div className="">
              <div className="px-4 py-2 mb-2 w-full flex items-center gap-2 bg-[var(--hover-bg)] rounded-t-lg">
                <div className="">
                  {user.profile_image_url !== null ? (
                    <Image src={user.profile_image_url || "/user-avatar.png"} alt="User Avatar" width={40} height={40} className="rounded-full" />
                  ) : (
                    <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary-accent/10 text-sm text-primary font-semibold">
                      {user.name.charAt(0).toUpperCase()}{user.lastname.charAt(0).toUpperCase()}
                    </div>
                  )}
                </div>
        
                <div className="text-muted-foreground text-sm rounded-full">{user.name} {user.lastname}</div>
              </div>

              <div className="pb-4 flex flex-col items-center gap-2">
                <button
                  onClick={handleSettings}
                  className="cursor-pointer text-left px-4 py-2 text-sm text-muted-foreground hover:bg-[var(--hover-bg)] hover:rounded-md flex items-center gap-2"
                >
                  <Settings className="h-4 w-4" />
                  Configuración
                </button>
                <button
                  onClick={handleLogout}
                  className="cursor-pointer text-left px-4 py-2 text-sm text-muted-foreground hover:bg-[var(--hover-bg)] hover:rounded-md flex items-center gap-2"
                >
                  <LogOut className="h-4 w-4" strokeWidth={2.5}/>
                  Cerrar sesión
                </button>
              </div>
            </div>
          ) : (
            <div className="py-1">
              <Link
                href="/login"
                className="block px-4 py-2 text-sm text-muted-foreground hover:bg-[var(--hover-bg)] flex items-center gap-2"
              >
                <LogIn className="h-4 w-4" />
                Iniciar sesión
              </Link>
              <Link
                href="/register"
                className="block px-4 py-2 text-sm text-muted-foreground hover:bg-[var(--hover-bg)] flex items-center gap-2"
              >
                <UserRoundPlus className="h-4 w-4" />
                Registrarse
              </Link>
            </div>
          )}
      </div>
    </header>
  )
}