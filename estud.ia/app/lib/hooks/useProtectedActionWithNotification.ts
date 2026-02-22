'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';
import { useNotification } from '@/app/contexts/NotificationContext';

/**
 * Hook avanzado que protege acciones y muestra notificaciones
 * Si el usuario no está autenticado, muestra una notificación y redirige al login
 */
export function useProtectedActionWithNotification() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const { addNotification } = useNotification();

  const protectedAction = (
    callback: () => void | Promise<void>,
    actionName: string = 'esta acción'
  ) => {
    if (!isAuthenticated) {
      addNotification(
        'Debes iniciar sesión',
        `Inicia sesión para ${actionName}.`,
        'error'
      );
      setTimeout(() => {
        router.push('/login');
      }, 1000);
      return;
    }
    return callback();
  };

  return { protectedAction, isAuthenticated };
}
