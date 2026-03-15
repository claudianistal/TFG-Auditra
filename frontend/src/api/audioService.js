import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const uploadAudioFile = async (formData) => {
  return api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
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

export default api;