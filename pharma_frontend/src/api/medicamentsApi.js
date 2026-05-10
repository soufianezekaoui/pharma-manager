/**
 * Medicaments API calls.
 * @param {Object} params - Filtering params (search, categorie, page)
 */
import axiosInstance from './axiosConfig';

export const fetchMedicaments = async (params = {}) => {
  const res = await axiosInstance.get('/medicaments/', { params });
  return res.data;
};

export const fetchMedicament = async (id) => {
  const res = await axiosInstance.get(`/medicaments/${id}/`);
  return res.data;
};

export const createMedicament = async (data) => {
  const res = await axiosInstance.post('/medicaments/', data);
  return res.data;
};

export const updateMedicament = async (id, data) => {
  const res = await axiosInstance.patch(`/medicaments/${id}/`, data);
  return res.data;
};

export const deleteMedicament = async (id) => {
  const res = await axiosInstance.delete(`/medicaments/${id}/`);
  return res.data;
};

export const restockMedicament = async (id, quantite) => {
  const res = await axiosInstance.post(`/medicaments/${id}/restock/`, { quantite });
  return res.data;
};

export const fetchAlertesStock = async () => {
  const res = await axiosInstance.get('/medicaments/alertes-stock/');
  return res.data;
};

export const fetchCategories = async () => {
  const res = await axiosInstance.get('/categories/');
  return res.data;
};
