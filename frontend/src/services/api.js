import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
});

/**
 * Check backend health status.
 * GET /
 */
export const checkHealth = async () => {
  const response = await api.get('/');
  return response.data;
};

/**
 * Upload a document (PDF, DOCX, TXT).
 * POST /ingest/file
 * @param {File} file
 */
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  // We let Axios and the browser set the Content-Type with the multipart boundary automatically
  const response = await api.post('/ingest/file', formData);
  return response.data;
};

/**
 * Ingest content from a web URL.
 * POST /ingest/url
 * @param {string} url
 */
export const ingestUrl = async (url) => {
  const response = await api.post('/ingest/url', { url });
  return response.data;
};

/**
 * Send a chat question to the assistant.
 * POST /chat/
 * @param {string} sessionId
 * @param {string} question
 */
export const sendMessage = async (sessionId, question) => {
  const response = await api.post('/chat/', {
    session_id: sessionId,
    question: question,
  });
  return response.data;
};
