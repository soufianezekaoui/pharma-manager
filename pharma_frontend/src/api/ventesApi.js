/**
 * Ventes API calls.
 */
import axiosInstance from './axiosConfig';

export const fetchVentes = async (params = {}) => {
  const res = await axiosInstance.get('/ventes/', { params });
  return res.data;
};

export const fetchVente = async (id) => {
  const res = await axiosInstance.get(`/ventes/${id}/`);
  return res.data;
};

export const createVente = async (data) => {
  const res = await axiosInstance.post('/ventes/', data);
  return res.data;
};

export const updateVenteStatut = async (id, statut) => {
  const res = await axiosInstance.patch(`/ventes/${id}/statut/`, { statut });
  return res.data;
};

export const cancelVente = async (id) => {
  const res = await axiosInstance.delete(`/ventes/${id}/`);
  return res.data;
};
