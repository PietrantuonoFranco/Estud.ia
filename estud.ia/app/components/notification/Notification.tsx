"use client"

import { useState, useEffect } from "react"
import { CircleCheckBig, CircleAlert, Info, X } from "lucide-react"

import cn from "@/app/lib/utils/cn"
import { Notification as NotificationProps } from "@/app/lib/interfaces/components/Notification"

export default function Notification({ title, message, type, isExiting = false, onClose }: NotificationProps) {
  const handleClose = () => {
    onClose?.()
  }

  return (
    <div
      className={cn(
        "transition-all duration-300 ease-out",
        isExiting ? "animate-slide-out-right" : "animate-slide-in-bottom"
      )}
    >
      <div className="relative rounded-xl bg-card border border-muted px-6 py-4 flex flex-col space-y-2 shadow-lg w-80">
        <div className="flex items-center justify-between">
          <div className="flex items-center text-lg text-left space-x-2">
            { type === 'success' && (
              <CircleCheckBig className="w-5 h-5 text-green-500"/>
            )}
            
            { type === 'error' && (
              <CircleAlert className="w-5 h-5 text-red-500" />
            )}

            { type === 'info' && (
              <Info className="w-5 h-5 text-blue-500"/>
            )}
            <h4 className="font-semibold">{title}</h4>
          </div>

          <button
            type="button"
            onClick={handleClose}
            className="absolute top-2 right-2 cursor-pointer p-1 rounded-full hover:hover:bg-[var(--hover-bg)]"
            aria-label="Cerrar notificación"
          >
            <X className="w-4 h-4 text-muted-foreground"/>
          </button>
        </div>

        <p className="text-sm text-muted-foreground">{message}</p>
        
        {/* Barra de progreso de tiempo */}
        <div className="absolute bottom-0 left-0.75 right-0.75 h-1 bg-muted/30 rounded-b-sm overflow-hidden">
          <div 
            className={cn(
              "h-full",
              type === 'success' && "bg-green-500",
              type === 'error' && "bg-red-500",
              type === 'info' && "bg-blue-500",
              "animate-[shrink_5s_linear_forwards]"
            )}
            style={{
              width: '100%'
            }}
          />
        </div>
      </div>
    </div>
  )
}