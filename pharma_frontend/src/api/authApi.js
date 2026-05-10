/**
 * Authentication API calls.
 */
import axiosInstance from './axiosConfig';

export const login = async (credentials) => {
  const res = await axiosInstance.post('/auth/login/', credentials);
  return res.data;
};

export const register = async (data) => {
  const res = await axiosInstance.post('/auth/register/', data);
  return res.data;
};

export const logout = async (refresh) => {
  const res = await axiosInstance.post('/auth/logout/', { refresh });
  return res.data;
};

export const getMe = async () => {
  const res = await axiosInstance.get('/auth/me/');
  return res.data;
};
