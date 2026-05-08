import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const uploadAudioFile = async (formData) => {
  return api.post('/upload', formData);
};

export const deleteAudioFile = async (fileId) => {
  return api.delete(`/upload/${fileId}`);
};

export const getProcessingQueue = async () => {
  return api.get('/queue');
};

export const getAnalysisStatus = async (fileId) => {
  return api.get(`/status/${fileId}`);
};

export const getMetadata = async (fileId) => {
  return api.get(`/metadata/${fileId}`);
};

export const getPatterns = async (fileId, width = 512) => {
  return api.get(`/patterns/${fileId}`, {
    params: { width },
  });
};

export const getAutosimilarity = async (fileId, width = 512) => {
  return api.get(`/patterns/autosimilarity/${fileId}`, {
    params: { width },
  });
};

export const getPadding = async (fileId) => {
  return api.get(`/patterns/padding/${fileId}`);
};

export const getAnalysis = async (fileId) => {
  return api.get(`/analysis/${fileId}`);
};

export const getAudioUrl = async (fileId) => {
  try {
    const response = await api.get(`/audio/${fileId}`, {
      responseType: 'blob',
    });
    return URL.createObjectURL(response.data);
  } catch (error) {
    console.error('Error fetching audio:', error);
    throw error;
  }
};

export default api;