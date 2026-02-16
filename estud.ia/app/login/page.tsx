"use client"

import { useState } from "react"

import Image from "next/image"
import Link from "next/link"
import { LogIn } from "lucide-react"

import { useAuth } from "../contexts/AuthContext"
import { useNotification } from "../contexts/NotificationContext"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);

  const { login } = useAuth()
  const { addNotification } = useNotification();

  const handleSubmit = async(event: React.FormEvent) => {
    event.preventDefault()
    
    try {
      await login(email, password);
      addNotification("Sesión iniciada", "Has iniciado sesión correctamente.", "success");
    } catch (error) {
      console.error("Error al iniciar sesión:", error);
      addNotification("Error", "Ocurrió un error al iniciar sesión.", "error");
    }
  }
  
  const handleGoogleLogin = () => {
    setIsGoogleLoading(true);

    // Usa la URL del helper de AuthApi
    const { getGoogleLoginUrl } = require("../lib/api/entities/AuthApi");
    window.location.assign(getGoogleLoginUrl());
  };

  return (
    <div className="h-full grid grid-cols-1 lg:grid-cols-2">
      <div className="p-2 sm:p-8 space-y-4 h-full w-full flex flex-col justify-center items-center">
        <Image
          src="/logo_dark.png"
          alt="Estud.ia Logo"
          width={300}
          height={35}
          sizes="(max-width: 640px) 254px, (max-width: 1024px) 284px, 300px"
          className="w-40 sm:w-56 lg:w-72 h-auto"
          priority
        />

        <h2 className="mb-4 text-2xl text-center font-semibold">Iniciar Sesión</h2>

        <form
          onSubmit={handleSubmit}
          className="w-sm sm:w-xl px-6 sm:px-12 shadow-md text-foregroundspace-y-6"
        >
          <div className="mb-4">
            <label
              htmlFor="email"
              className="mb-2 block text-sm font-medium"
            > Correo Electrónico</label>
            <input
              type="email"
              id="email"
              value={email}
              placeholder="jhondoe@example.com"
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-md border-b border-muted-foreground py-3 px-6 shadow-primary/20 focus:shadow-lg focus:border-b-primary focus:outline-none transition-all duration-200"
              required
            />
          </div>
          <div className="mb-6">
            <label
              htmlFor="password"
              className="mb-2 block text-sm font-medium"
            > Contraseña</label>
            <input
              type="password"
              id="password"
              value={password}
              placeholder="****************"
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-md border-b border-muted-foreground py-3 px-6 shadow-primary/20 focus:shadow-lg focus:border-b-primary focus:outline-none transition-all duration-200"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full rounded-md bg-gradient-to-br from-primary-accent to-primary/90 shadow-primary/20 hover:bg-gradient-to-br hover:from-primary-accent hover:to-primary hover:shadow-lg transition-all duration-200 ease-in-out cursor-pointer p-3 text-black font-semibold flex items-center justify-center gap-2"
          >
            <LogIn className="w-4 h-4" strokeWidth={2.5} />
            Iniciar Sesión
          </button>

          <div className="w-full h-[1px] bg-muted-foreground my-4"/>

          <button
            type="submit"
            onClick={handleGoogleLogin}
            className="cursor-pointer w-full flex items-center justify-center gap-2 rounded-lg bg-gradient-to-br from-white to-foreground p-3 text-background hover:to-foreground/80"
          >
            {isGoogleLoading ? (
              <span>Redirigiendo...</span>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" viewBox="0 0 48 48">
                  <path fill="#ffc107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C12.955 4 4 12.955 4 24s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917"></path>
                  <path fill="#ff3d00" d="m6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C16.318 4 9.656 8.337 6.306 14.691"></path>
                  <path fill="#4caf50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.9 11.9 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44"></path>
                  <path fill="#1976d2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002l6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917"></path>
                </svg>
                <span className="font-semibold">Google</span>
              </>
            )}
          </button>
        </form>

        <Link href="/register" className="mt-4 text-sm text-center text-foreground hover:underline">
          ¿No tienes una cuenta? Regístrate
        </Link>
      </div>

      <div style={{backgroundImage: "url(/login.png)"}} className="hidden lg:block h-full w-full bg-cover bg-center"/>
    </div>
  )
}