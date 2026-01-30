"use client"

import { useState } from "react"
import { Modal, ModalFooter, ModalButton } from "./Modal"
import { Sparkles, Bell, Settings, Trash2 } from "lucide-react"

export default function Home() {
  const [basicModal, setBasicModal] = useState(false)
  const [confirmModal, setConfirmModal] = useState(false)
  const [formModal, setFormModal] = useState(false)

  return (
    <main className="min-h-screen bg-zinc-950 flex flex-col items-center justify-center p-8">
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-zinc-800/50 border border-zinc-700 mb-6">
          <Sparkles className="w-4 h-4 text-emerald-400" />
          <span className="text-sm text-zinc-300">Modal Moderno</span>
        </div>
        <h1 className="text-4xl font-bold text-white mb-4 tracking-tight">
          Ventana Modal
        </h1>
        <p className="text-zinc-400 max-w-md mx-auto leading-relaxed">
          Componente modal con tema oscuro, animaciones suaves y diseño moderno.
        </p>
      </div>

      {/* Botones de demostración */}
      <div className="flex flex-wrap items-center justify-center gap-4">
        <button
          onClick={() => setBasicModal(true)}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-white text-zinc-900 font-medium hover:bg-zinc-200 transition-all duration-200 shadow-lg shadow-white/10"
        >
          <Bell className="w-4 h-4" />
          Modal Básico
        </button>

        <button
          onClick={() => setConfirmModal(true)}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-zinc-800 text-white font-medium border border-zinc-700 hover:bg-zinc-700 transition-all duration-200"
        >
          <Trash2 className="w-4 h-4" />
          Eliminar
        </button>

        <button
          onClick={() => setFormModal(true)}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-emerald-600 text-white font-medium hover:bg-emerald-500 transition-all duration-200 shadow-lg shadow-emerald-600/20"
        >
          <Settings className="w-4 h-4" />
          Formulario
        </button>
      </div>

      {/* Modal Básico */}
      <Modal
        isOpen={basicModal}
        onClose={() => setBasicModal(false)}
        title="Notificación"
        description="Este es un ejemplo de modal con estilo moderno y tema oscuro."
      >
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-zinc-800/50 border border-zinc-700">
            <p className="text-zinc-300 text-sm leading-relaxed">
              Los modales son componentes esenciales para mostrar información importante,
              solicitar confirmación del usuario o presentar formularios de manera elegante.
            </p>
          </div>
          <ModalFooter>
            <ModalButton variant="secondary" onClick={() => setBasicModal(false)}>
              Cancelar
            </ModalButton>
            <ModalButton variant="primary" onClick={() => setBasicModal(false)}>
              Entendido
            </ModalButton>
          </ModalFooter>
        </div>
      </Modal>

      {/* Modal de Confirmación */}
      <Modal
        isOpen={confirmModal}
        onClose={() => setConfirmModal(false)}
        title="¿Eliminar elemento?"
        description="Esta acción no se puede deshacer. El elemento será eliminado permanentemente."
      >
        <div className="space-y-4">
          <div className="flex items-center gap-4 p-4 rounded-xl bg-red-950/30 border border-red-900/50">
            <div className="p-3 rounded-full bg-red-900/50">
              <Trash2 className="w-5 h-5 text-red-400" />
            </div>
            <div>
              <p className="text-zinc-200 font-medium">documento-importante.pdf</p>
              <p className="text-zinc-500 text-sm">2.4 MB • Modificado hace 3 días</p>
            </div>
          </div>
          <ModalFooter>
            <ModalButton variant="secondary" onClick={() => setConfirmModal(false)}>
              Cancelar
            </ModalButton>
            <ModalButton variant="danger" onClick={() => setConfirmModal(false)}>
              Eliminar
            </ModalButton>
          </ModalFooter>
        </div>
      </Modal>

      {/* Modal de Formulario */}
      <Modal
        isOpen={formModal}
        onClose={() => setFormModal(false)}
        title="Configuración"
        description="Personaliza las opciones de tu cuenta."
      >
        <div className="space-y-5">
          <div className="space-y-2">
            <label className="text-sm font-medium text-zinc-300">Nombre de usuario</label>
            <input
              type="text"
              placeholder="@usuario"
              className="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-zinc-300">Email</label>
            <input
              type="email"
              placeholder="correo@ejemplo.com"
              className="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
            />
          </div>
          <div className="flex items-center justify-between p-4 rounded-xl bg-zinc-800/50 border border-zinc-700">
            <div>
              <p className="text-zinc-200 font-medium text-sm">Notificaciones</p>
              <p className="text-zinc-500 text-xs">Recibir alertas por email</p>
            </div>
            <button className="relative w-12 h-7 rounded-full bg-emerald-600 transition-colors">
              <span className="absolute right-1 top-1 w-5 h-5 rounded-full bg-white shadow-sm transition-transform" />
            </button>
          </div>
          <ModalFooter>
            <ModalButton variant="secondary" onClick={() => setFormModal(false)}>
              Cancelar
            </ModalButton>
            <ModalButton variant="primary" onClick={() => setFormModal(false)}>
              Guardar cambios
            </ModalButton>
          </ModalFooter>
        </div>
      </Modal>
    </main>
  )
}
