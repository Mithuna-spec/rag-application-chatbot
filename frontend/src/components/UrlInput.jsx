import React, { useState } from 'react';
import { ingestUrl } from '../services/api';

export default function UrlInput({ onIngestSuccess }) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ type: '', message: '' });

  const handleIngest = async (e) => {
    e.preventDefault();
    if (!url.trim()) return;

    // Basic URL validation
    try {
      new URL(url);
    } catch (_) {
      setStatus({
        type: 'error',
        message: 'Please enter a valid URL (including http:// or https://).',
      });
      return;
    }

    setLoading(true);
    setStatus({ type: 'info', message: 'Processing URL...' });

    try {
      const data = await ingestUrl(url);
      setStatus({
        type: 'success',
        message: data.message || 'URL processed successfully.',
      });
      if (onIngestSuccess) {
        onIngestSuccess({ type: 'url', name: url });
      }
    } catch (err) {
      console.error(err);
      const errMsg = err.response?.data?.detail || 'Unable to process the URL.';
      setStatus({
        type: 'error',
        message: errMsg,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3 className="card-title">Or use a webpage</h3>
      <form onSubmit={handleIngest}>
        <div className="input-group">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            disabled={loading}
            required
            className="input-text"
          />
        </div>
        <button
          type="submit"
          className="btn-secondary"
          disabled={!url.trim() || loading}
        >
          {loading ? 'Processing URL...' : 'Process URL'}
        </button>
      </form>

      {status.message && (
        <div className={`status-message status-${status.type}`}>
          {status.message}
        </div>
      )}
    </div>
  );
}
