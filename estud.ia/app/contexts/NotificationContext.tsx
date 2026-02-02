// context/NotificationContext.tsx
"use client";
import React, { createContext, useContext, useState, useCallback } from 'react';

import Notification from '@/app/components/notification/Notification';
import { Notification as NotificationInterface, NotificationType } from '@/app/lib/interfaces/components/Notification';

interface NotificationContextType {
  addNotification: (title: string, message: string, type: NotificationType) => void;
}

const NotificationContext = createContext<NotificationContextType | undefined>(undefined);

export const NotificationProvider = ({ children }: { children: React.ReactNode }) => {
  const [notifications, setNotifications] = useState<NotificationInterface[]>([]);

  const removeNotification = useCallback((id: number) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  }, []);

  const addNotification = useCallback((title: string, message: string, type: NotificationType) => {
    const id = Date.now();
    setNotifications((prev) => [...prev, { id, title, message, type }]);

    // Auto-eliminar después de 5 segundos
    setTimeout(() => {
      removeNotification(id);
    }, 5000);
  }, [removeNotification]);

  return (
    <NotificationContext.Provider value={{ addNotification }}>
      {children}

      {/* Contenedor de Toasts */}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        {notifications.map((n) => (
          <Notification key={n.id} {...n} onClose={() => removeNotification(n.id)} />
        ))}
      </div>
    </NotificationContext.Provider>
  );
};

// Hook personalizado para usarlo fácilmente
export const useNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) throw new Error("useNotification debe usarse dentro de NotificationProvider");
  return context;
};