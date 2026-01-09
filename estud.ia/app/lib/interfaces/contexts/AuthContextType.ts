import User from '@/app/lib/interfaces/entities/User';

export default interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string, lastname: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}