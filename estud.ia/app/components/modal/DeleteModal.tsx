"use client"

import Source from "@/app/lib/interfaces/entities/Source"
import { Modal, ModalFooter, ModalButton } from "./Modal"
import { Trash2 } from "lucide-react"
import { useState } from "react"

interface DeleteModalProps {
  isOpen: boolean
  title: string
  items: Source[] // Agregar tipos con un OR según sea necesario
  onClose: () => void
  onDelete: () => void
}

export function DeleteModal({ isOpen, title, items, onClose, onDelete }: DeleteModalProps) {
  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = async () => {
    setIsDeleting(true)

    try {
      await onDelete()
      onClose()
    } catch (error) {
      console.error("Error deleting item:", error)
    } finally {
      setIsDeleting(false)
    }
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      description="Esta acción no se puede deshacer. El elemento será eliminado permanentemente."
    >
      <div className="space-y-4">
        <div className="w-full flex flex-col items-center justify-center space-y-2">
          {items.map((item, index) => (
            <div key={index} className="w-full flex items-center gap-4 px-4 py-2 rounded-xl bg-red-950/30 border border-red-900/50">
              <div className="p-3 rounded-full bg-red-900/50">
                <Trash2 className="w-5 h-5 text-red-400" />
              </div>
    
              <div>
                <p className="text-zinc-200 font-medium">{item.name}</p>
              </div>
            </div>
          ))}
        </div>

        <ModalFooter>
          <ModalButton variant="secondary" onClick={onClose}>
            Cancelar
          </ModalButton>
          <ModalButton variant="danger" onClick={handleDelete} disabled={isDeleting}>
            Eliminar
          </ModalButton>
        </ModalFooter>
      </div>
    </Modal>
  )
}