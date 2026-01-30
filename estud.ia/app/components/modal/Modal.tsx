"use client"

import React from "react"

import { useEffect, useRef } from "react"
import { X } from "lucide-react"
import cn from "@/app/lib/utils/cn"

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  description?: string
  disabed?: boolean
  children: React.ReactNode
  className?: string
}

export function Modal({ isOpen, onClose, title, description, children, className }: ModalProps) {
  const overlayRef = useRef<HTMLDivElement>(null)
  const modalRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose()
    }

    if (isOpen) {
      document.addEventListener("keydown", handleEscape)
      document.body.style.overflow = "hidden"
    }

    return () => {
      document.removeEventListener("keydown", handleEscape)
      document.body.style.overflow = "unset"
    }
  }, [isOpen, onClose])

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === overlayRef.current) {
      onClose()
    }
  }

  if (!isOpen) return null

  return (
    <div
      ref={overlayRef}
      onClick={handleOverlayClick}
      className={cn(
        "fixed inset-0 z-50 flex items-center justify-center",
        "bg-black/60 backdrop-blur-sm",
        "animate-in fade-in duration-200"
      )}
    >
      <div
        ref={modalRef}
        className={cn(
          "relative w-full max-w-lg mx-4",
          "bg-zinc-900 border border-zinc-800",
          "rounded-2xl shadow-2xl shadow-black/50",
          "animate-in zoom-in-95 slide-in-from-bottom-4 duration-300",
          className
        )}
      >
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-zinc-800">
          <div className="space-y-1.5 pr-8">
            {title && (
              <h2 className="text-xl font-semibold text-zinc-100 tracking-tight">
                {title}
              </h2>
            )}
            {description && (
              <p className="text-sm text-zinc-400 leading-relaxed">
                {description}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className={cn(
              "cursor-pointer absolute top-4 right-4",
              "p-2 rounded-xl",
              "text-zinc-400 hover:text-zinc-100",
              "bg-zinc-800/50 hover:bg-zinc-800",
              "transition-all duration-200",
              "focus:outline-none focus:ring-2 focus:ring-zinc-600"
            )}
            aria-label="Cerrar modal"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  )
}

// Componentes adicionales para el modal
export function ModalFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn(
      "flex items-center justify-end gap-3 pt-4 mt-2",
      "border-t border-zinc-800",
      className
    )}>
      {children}
    </div>
  )
}

export function ModalButton({ 
  children, 
  variant = "primary", 
  onClick,
  disabled,
  className 
}: { 
  children: React.ReactNode
  variant?: "primary" | "secondary" | "danger"
  onClick?: () => void
  disabled?: boolean
  className?: string
}) {
  const variants = {
    primary: "bg-white text-zinc-900 hover:bg-zinc-200",
    secondary: "bg-zinc-800 text-zinc-100 hover:bg-zinc-700 border border-zinc-700",
    danger: "bg-red-600 text-white hover:bg-red-700",
  }

  return (
    <button
      onClick={onClick}
      className={cn(
        "cursor-pointer px-4 py-2.5 rounded-xl font-medium text-sm",
        "transition-all duration-200",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-zinc-900",
        variants[variant],
        variant === "primary" && "focus:ring-white",
        variant === "secondary" && "focus:ring-zinc-600",
        variant === "danger" && "focus:ring-red-500",
        className
      )}
    >
      {children}
    </button>
  )
}
