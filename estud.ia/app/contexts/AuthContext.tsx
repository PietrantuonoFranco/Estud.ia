'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

import User from '@/app/lib/interfaces/entities/User';
import AuthContextType from '@/app/lib/interfaces/contexts/AuthContextType';
import * as AuthApi from '@/app/lib/api/entities/AuthApi';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Verificar si el usuario está autenticado al montar el componente
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      setIsLoading(true);
      const userData = await AuthApi.getMe();
      setUser(userData);
    } catch (error) {
      console.error('Error verificando autenticación:', error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      await AuthApi.login({ username: email, password });
      
      // Después del login exitoso, obtener datos del usuario
      await checkAuth();
      router.push('/'); // Redirigir a la homepage
    } catch (error) {
      console.error('Error en login:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (email: string, name: string, lastname: string, password: string) => {
    try {
      setIsLoading(true);
      await AuthApi.register({ username: email, name, lastname, password });

      // Después del registro exitoso, obtener datos del usuario
      await checkAuth();
      router.push('/'); // Redirigir a la homepage
    } catch (error) {
      console.error('Error en registro:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      setIsLoading(true);
      await AuthApi.logout();

      setUser(null);
      router.push('/login'); // Redirigir al login
    } catch (error) {
      console.error('Error en logout:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const value: AuthContextType = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Hook para usar el contexto
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
}
