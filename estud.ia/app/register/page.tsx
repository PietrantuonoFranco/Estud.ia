"use client"

import { useState } from "react"

import Image from "next/image"
import Link from "next/link"

export default function RegisterPage() {
  const [email, setEmail] = useState("")
  const [name, setName] = useState("")
  const [lastName, setLastName] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")



  const handleSubmit = async(event: React.FormEvent) => {
    event.preventDefault()

    try {
      // Aquí iría la lógica para manejar el registro, como llamar a una API
      console.log("Registrando usuario:", { email, name, lastName, password, confirmPassword })

      if (password !== confirmPassword) {
        alert("Las contraseñas no coinciden")
        return
      }

      const formData = {
        email,
        name,
        lastname: lastName,
        password,
      }

      const response = await fetch('http://localhost:5000/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (response.ok) {
        alert("Usuario registrado exitosamente")
        // Aquí podrías redirigir al usuario a otra página, como la de login
      } else {
        const errorData = await response.json()
        alert("Error al registrar el usuario: " + (errorData.detail || 'Error desconocido'))
      }

    } catch (error) {
      console.error("Error al registrar el usuario:", error)
    }
  }


  return (
    <div className="h-full p-8">
      <div className="h-full w-full flex flex-col justify-center items-center space-y-4">
        <Image
          src="/logo_dark.png"
          alt="Estud.ia Logo"
          width={350}
          height={50}
          className="mb-10 mx-auto"
        />

        <h2 className="mb-4 text-2xl text-center font-semibold">Registra tu cuenta</h2>

        <form
          onSubmit={handleSubmit}
          className="w-xl rounded-lg px-12 shadow-md text-foregroundspace-y-6"
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
              className="w-full rounded-full border border-gray-300 py-3 px-6 focus:border-blue-500 focus:outline-none"
              required
            />
          </div>

          <div className="grid grid-cols-2 w-full gap-4">
            <div className="mb-4">
              <label
                htmlFor="name"
                className="mb-2 block text-sm font-medium"
              > Nombre</label>
              <input
                type="text"
                id="name"
                value={name}
                placeholder="Jhon"
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-full border border-gray-300 py-3 px-6 focus:border-blue-500 focus:outline-none"
                required
              />
            </div>

            <div className="mb-4">
              <label
                htmlFor="lastName"
                className="mb-2 block text-sm font-medium"
              > Apellido</label>
              <input
                type="text"
                id="lastName"
                value={lastName}
                placeholder="Doe"
                onChange={(e) => setLastName(e.target.value)}
                className="w-full rounded-full border border-gray-300 py-3 px-6 focus:border-blue-500 focus:outline-none"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 w-full gap-4">
            <div className="mb-4">
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
                className="w-full rounded-full border border-gray-300 py-3 px-6 focus:border-blue-500 focus:outline-none"
                required
              />
            </div>

            <div className="mb-6">
              <label
                htmlFor="confirmPassword"
                className="mb-2 block text-sm font-medium"
              > Confirmar Contraseña</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                placeholder="****************"
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full rounded-full border border-gray-300 py-3 px-6 focus:border-blue-500 focus:outline-none"
                required
              />
            </div>
          </div>
          
          <button
            type="submit"
            className="cursor-pointer font-semibold w-full rounded-full bg-gradient-to-br from-purple-600 to-blue-500 p-3 text-white hover:to-blue-600"
          >
            Registrarme
          </button>

          <div className="w-full h-[1px] bg-foreground my-4"/>

          <button
            type="submit"
            className="cursor-pointer w-full flex items-center justify-center gap-2 rounded-full bg-gradient-to-br from-white to-foreground p-3 text-background hover:to-foreground/80"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" viewBox="0 0 48 48">
              <path fill="#ffc107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8c-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C12.955 4 4 12.955 4 24s8.955 20 20 20s20-8.955 20-20c0-1.341-.138-2.65-.389-3.917"></path>
              <path fill="#ff3d00" d="m6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4C16.318 4 9.656 8.337 6.306 14.691"></path>
              <path fill="#4caf50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.9 11.9 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44"></path>
              <path fill="#1976d2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002l6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917"></path>
            </svg>
            <span className="font-semibold">Google</span>
          </button>
        </form>

        <Link href="/login" className="mt-4 text-sm text-center text-foreground hover:underline">
          ¿Ya tienes una cuenta? Inicia sesión
        </Link>
      </div>
    </div>
  )
}