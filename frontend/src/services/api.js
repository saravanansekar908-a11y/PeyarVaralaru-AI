import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const res = await apiClient.get('/health');
  return res.data;
};

export const getPlaces = async (searchQuery = '') => {
  const params = searchQuery ? { q: searchQuery } : {};
  const res = await apiClient.get('/places', { params });
  return res.data;
};

export const getPlace = async (id) => {
  const res = await apiClient.get(`/places/${id}`);
  return res.data;
};

export const getTimeline = async (placeId) => {
  const res = await apiClient.get(`/places/${placeId}/timeline`);
  return res.data;
};

export const getPlaceSources = async (placeId) => {
  const res = await apiClient.get(`/places/${placeId}/sources`);
  return res.data;
};

export const getAllSources = async () => {
  const res = await apiClient.get('/sources');
  return res.data;
};

export const getGraphData = async (placeId = 1) => {
  const res = await apiClient.get(`/graph/${placeId}`);
  return res.data;
};

export const askAI = async (question, language = 'ta') => {
  const res = await apiClient.post('/ask', { question, language });
  return res.data;
};

export default apiClient;
