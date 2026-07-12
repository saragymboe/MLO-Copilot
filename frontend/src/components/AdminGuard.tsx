import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

export function AdminGuard() {
  const { user, loading } = useAuth();
  if (loading) return null;
  return user?.groups?.includes('Admins') ? <Outlet /> : <Navigate to="/dashboard" replace />;
}
