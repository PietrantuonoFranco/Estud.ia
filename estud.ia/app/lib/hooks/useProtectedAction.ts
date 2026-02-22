import { useRouter } from 'next/navigation';
import { useAuth } from '@/app/contexts/AuthContext';

/**
 * Hook que protege acciones que requieren autenticación
 * Si el usuario no está autenticado, redirige al login
 */
export function useProtectedAction() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();

  const protectedAction = (callback: () => void | Promise<void>) => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    return callback();
  };

  return { protectedAction, isAuthenticated };
}
