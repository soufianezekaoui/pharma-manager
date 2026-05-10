/**
 * Custom hook for authentication state and actions.
 */
import { useState, useEffect, useCallback } from 'react';
import { login as apiLogin, logout as apiLogout, getMe } from '../api/authApi';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) { setLoading(false); return; }
    getMe()
      .then((res) => setUser(res.data))
      .catch(() => { localStorage.removeItem('access_token'); })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (credentials) => {
    const res = await apiLogin(credentials);
    localStorage.setItem('access_token', res.access);
    localStorage.setItem('refresh_token', res.refresh);
    const me = await getMe();
    setUser(me.data);
    return me.data;
  }, []);

  const logout = useCallback(async () => {
    const refresh = localStorage.getItem('refresh_token');
    try { await apiLogout(refresh); } catch {}
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  }, []);

  return {
    user,
    loading,
    isAuthenticated: !!user,
    isPharmacist: user?.role === 'pharmacist',
    login,
    logout,
  };
}
