import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

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

export const researchPlace = async (placeName, district = null, language = 'ta') => {
  const res = await apiClient.post('/history/research', {
    place_name: placeName,
    district,
    language,
  });
  return res.data;
};

export const askAI = async (question, language = 'ta', district = null) => {
  const res = await apiClient.post('/ask', { question, language, district });
  return res.data;
};

export const getDocuments = async () => {
  const res = await apiClient.get('/documents');
  return res.data;
};

export const getDocumentPassages = async (documentId) => {
  const res = await apiClient.get(`/documents/${documentId}/passages`);
  return res.data;
};

export const searchPassages = async (query, district = null) => {
  const params = { q: query };
  if (district) params.district = district;
  const res = await apiClient.get('/documents/search/passages', { params });
  return res.data;
};

export const getDistricts = async (query = '', region = '') => {
  const params = {};
  if (query) params.q = query;
  if (region && region !== 'all') params.region = region;
  const res = await apiClient.get('/districts', { params });
  return res.data;
};

export const getDistrict = async (identifier) => {
  const res = await apiClient.get(`/districts/${encodeURIComponent(identifier)}`);
  return res.data;
};

export const ingestDocument = async (payload) => {
  const res = await apiClient.post('/documents/ingest', payload);
  return res.data;
};

// --- Historical Maps & Comparison Observations ---
export const getHistoricalMaps = async (params = {}) => {
  const res = await apiClient.get('/maps', { params });
  return res.data;
};

export const getHistoricalMap = async (id) => {
  const res = await apiClient.get(`/maps/${id}`);
  return res.data;
};

export const getMapPeriods = async () => {
  const res = await apiClient.get('/maps/periods');
  return res.data;
};

export const getMapPlaces = async () => {
  const res = await apiClient.get('/maps/places');
  return res.data;
};

export const getMapObservationCategories = async () => {
  const res = await apiClient.get('/maps/observations/categories');
  return res.data;
};

export const searchMapObservations = async (params = {}) => {
  const res = await apiClient.get('/maps/observations/search', { params });
  return res.data;
};

export const getMapObservations = async (mapId, category = null) => {
  const params = category ? { category } : {};
  const res = await apiClient.get(`/maps/${mapId}/observations`, { params });
  return res.data;
};

export default apiClient;
