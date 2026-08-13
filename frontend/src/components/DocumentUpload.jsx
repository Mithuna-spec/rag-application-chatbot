import React, { useState } from 'react';
import { uploadFile } from '../services/api';

export default function DocumentUpload({ onIngestSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ type: '', message: '', chunks: null });

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    const allowed = ['.pdf', '.docx', '.txt'];

    if (!allowed.includes(extension)) {
      setStatus({
        type: 'error',
        message: 'Only PDF, DOCX and TXT files are supported.',
        chunks: null,
      });
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    setStatus({ type: '', message: '', chunks: null });
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setStatus({ type: 'info', message: 'Processing document...', chunks: null });

    try {
      const data = await uploadFile(selectedFile);
      setStatus({
        type: 'success',
        message: data.message || 'Document processed successfully.',
        chunks: data.chunks,
      });
      if (onIngestSuccess) {
        onIngestSuccess({ type: 'file', name: selectedFile.name });
      }
    } catch (err) {
      console.error(err);
      const errMsg = err.response?.data?.detail || 'Unable to process the document.';
      setStatus({
        type: 'error',
        message: errMsg,
        chunks: null,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3 className="card-title">Upload a document</h3>
      <p className="card-subtitle">Supported formats: PDF, DOCX, TXT</p>
      
      <div className="file-upload-container">
        <label className={`file-input-label ${loading ? 'disabled' : ''}`}>
          Choose File
          <input 
            type="file" 
            accept=".pdf,.docx,.txt" 
            onChange={handleFileChange} 
            disabled={loading}
            style={{ display: 'none' }}
          />
        </label>
        {selectedFile && (
          <div className="selected-filename">
            Selected: <strong>{selectedFile.name}</strong>
          </div>
        )}
      </div>

      <button
        className="btn-primary"
        onClick={handleUpload}
        disabled={!selectedFile || loading}
      >
        {loading ? 'Processing document...' : 'Process Document'}
      </button>

      {status.message && (
        <div className={`status-message status-${status.type}`}>
          <div>{status.message}</div>
          {status.type === 'success' && status.chunks !== undefined && status.chunks !== null && (
            <div className="chunks-info">
              Chunks: <strong>{status.chunks}</strong>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
