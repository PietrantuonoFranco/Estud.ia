"use client"

import { CircleCheckBig, CircleAlert, Info } from "lucide-react"

import cn from "@/app/lib/utils/cn"
import { Notification as NotificationProps } from "@/app/lib/interfaces/components/Notification"

export default function Notification({ title, message, type }: NotificationProps) {
  return (
    <div
      className={cn(
        "inset-0",
        "bg-gradient-to-br from-transparent to-black/60 backdrop-blur-sm",
        "animate-in fade-in duration-200"
      )}
    >
      <div className="rounded-xl bg-card border border-muted px-8 py-4 flex flex-col space-y-2 shadow-lg w-80">
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

        <p className="text-sm text-muted-foreground">{message}</p>
      </div>
    </div>
  )
}