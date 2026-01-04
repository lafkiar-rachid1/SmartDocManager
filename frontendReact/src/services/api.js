/**
 * Service API pour communiquer avec le backend FastAPI
 * Centralise toutes les requêtes HTTP
 */

import axios from 'axios';

// Configuration de base Axios
const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token à chaque requête
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ========== Upload de documents ==========

/**
 * Téléverse un document vers le backend
 * @param {File} file - Fichier à téléverser
 * @returns {Promise} Réponse de l'API
 */
export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const token = localStorage.getItem('token');
  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${token}`
    },
  });
  
  return response.data;
};

/**
 * Récupère tous les documents
 * @param {number} skip - Nombre de documents à ignorer
 * @param {number} limit - Nombre maximum de documents
 * @returns {Promise} Liste de documents
 */
export const getDocuments = async (skip = 0, limit = 100) => {
  const response = await api.get(`/documents?skip=${skip}&limit=${limit}`);
  return response.data;
};

/**
 * Récupère un document spécifique
 * @param {number} documentId - ID du document
 * @returns {Promise} Détails du document
 */
export const getDocument = async (documentId) => {
  const response = await api.get(`/documents/${documentId}`);
  return response.data;
};

/**
 * Supprime un document
 * @param {number} documentId - ID du document à supprimer
 * @returns {Promise} Confirmation de suppression
 */
export const deleteDocument = async (documentId) => {
  const response = await api.delete(`/documents/${documentId}`);
  return response.data;
};

// ========== OCR ==========

/**
 * Effectue l'OCR sur un document
 * @param {number} documentId - ID du document
 * @returns {Promise} Texte extrait
 */
export const performOCR = async (documentId) => {
  const response = await api.post('/ocr', { document_id: documentId });
  return response.data;
};

/**
 * Récupère les langues supportées pour l'OCR
 * @returns {Promise} Liste des langues
 */
export const getSupportedLanguages = async () => {
  const response = await api.get('/ocr/languages');
  return response.data;
};

// ========== Classification ==========

/**
 * Classifie un document
 * @param {number} documentId - ID du document
 * @returns {Promise} Catégorie et confiance
 */
export const classifyDocument = async (documentId) => {
  const response = await api.post('/classify', { document_id: documentId });
  return response.data;
};

/**
 * Classifie plusieurs documents
 * @param {Array<number>} documentIds - Liste des IDs
 * @returns {Promise} Résultats de classification
 */
export const classifyBatch = async (documentIds) => {
  const response = await api.post('/classify/batch', documentIds);
  return response.data;
};

/**
 * Récupère les catégories disponibles
 * @returns {Promise} Liste des catégories
 */
export const getCategories = async () => {
  const response = await api.get('/classify/categories');
  return response.data;
};

// ========== Statistiques ==========

/**
 * Récupère les statistiques globales
 * @returns {Promise} Statistiques du système
 */
export const getStatistics = async () => {
  const response = await api.get('/stats');
  return response.data;
};

/**
 * Récupère les statistiques par catégorie
 * @returns {Promise} Stats détaillées par catégorie
 */
export const getCategoryStats = async () => {
  const response = await api.get('/stats/categories');
  return response.data;
};

/**
 * Récupère l'évolution temporelle
 * @param {number} days - Nombre de jours à analyser
 * @returns {Promise} Timeline
 */
export const getTimelineStats = async (days = 30) => {
  const response = await api.get(`/stats/timeline?days=${days}`);
  return response.data;
};

// ========== Export ==========

/**
 * Exporte les documents en CSV
 * @returns {Promise} Fichier CSV
 */
export const exportToCSV = async () => {
  const response = await axios.get(`${API_BASE_URL}/export/csv`, {
    responseType: 'blob',
  });
  
  // Créer un lien de téléchargement
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `documents_export_${new Date().getTime()}.csv`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};

/**
 * Exporte les documents en JSON
 * @returns {Promise} Données JSON
 */
export const exportToJSON = async () => {
  const response = await api.get('/export/json');
  return response.data;
};

export default api;
