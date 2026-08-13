import React, { useState, useEffect } from 'react';
import { checkHealth, sendMessage } from './services/api';
import DocumentUpload from './components/DocumentUpload';
import UrlInput from './components/UrlInput';
import ChatWindow from './components/ChatWindow';

export default function App() {
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [activeSource, setActiveSource] = useState(null); // { type: 'file' | 'url', name: string }
  const [backendStatus, setBackendStatus] = useState('checking'); // 'checking' | 'connected' | 'disconnected'
  const [globalError, setGlobalError] = useState('');

  // 1. Initialize sessionId and verify backend health on mount
  useEffect(() => {
    // Generate one sessionId for the application session
    const id = crypto.randomUUID();
    setSessionId(id);

    const verifyBackend = async () => {
      try {
        await checkHealth();
        setBackendStatus('connected');
      } catch (err) {
        console.error('Backend health check failed:', err);
        setBackendStatus('disconnected');
      }
    };

    verifyBackend();
  }, []);

  // 2. Handle successful document/URL ingestion
  const handleIngestSuccess = (source) => {
    setActiveSource(source);
    setGlobalError('');
  };

  // 3. Send chat message to backend
  const handleSendMessage = async (question) => {
    if (!question.trim()) return;

    // Append user's query to chat messages state
    const newUserMessage = { role: 'user', content: question };
    setMessages((prev) => [...prev, newUserMessage]);
    setChatLoading(true);
    setGlobalError('');

    try {
      const response = await sendMessage(sessionId, question);
      
      // Append assistant's answer and sources to chat messages state
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources || [],
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat request failed:', err);
      
      // Map error responses to readable error messages
      let errorMessage = 'Unable to get an answer. Please try again.';
      
      if (err.response) {
        const detail = err.response.data?.detail;
        
        // Handle 404 or specific load failures (e.g. database not initialized)
        if (err.response.status === 404) {
          errorMessage = detail || 'No document has been processed yet. Upload a document or provide a URL first.';
        } else if (err.response.status === 500) {
          if (detail && detail.includes('Knowledge base could not be loaded')) {
            errorMessage = 'No document has been processed yet. Upload a document or provide a URL first.';
          } else {
            errorMessage = detail || 'The assistant encountered an error. Please try again.';
          }
        } else {
          errorMessage = detail || errorMessage;
        }
      } else {
        errorMessage = 'Unable to connect to the assistant server. Verify that the backend is running.';
      }

      setGlobalError(errorMessage);
      
      // Display the error directly inside the chat so the user is aware of what went wrong
      const errorSystemMessage = {
        role: 'assistant',
        content: errorMessage,
        sources: [],
      };
      setMessages((prev) => [...prev, errorSystemMessage]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">RAG Knowledge Assistant</h1>
        <p className="app-subtitle">Ask questions about your documents and web content.</p>
        
        <div className={`backend-badge ${backendStatus === 'disconnected' ? 'disconnected' : ''}`}>
          <span className="badge-dot"></span>
          {backendStatus === 'checking' && 'Checking backend status...'}
          {backendStatus === 'connected' && 'Connected to backend'}
          {backendStatus === 'disconnected' && 'Disconnected from backend'}
        </div>
      </header>

      {globalError && (
        <div className="status-message status-error">
          <strong>Error:</strong> {globalError}
        </div>
      )}

      <main className="app-layout">
        {/* Left Column - Ingestion Controls & State */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <DocumentUpload onIngestSuccess={handleIngestSuccess} />
          
          <UrlInput onIngestSuccess={handleIngestSuccess} />

          {activeSource && (
            <div className="card active-source-card">
              <div className="active-source-header">Active Source</div>
              <div className="active-source-name">
                {activeSource.type === 'file' ? '📄 ' : '🔗 '}
                {activeSource.name}
              </div>
            </div>
          )}
        </div>

        {/* Right Column - Chat Area */}
        <ChatWindow 
          messages={messages} 
          onSendMessage={handleSendMessage} 
          loading={chatLoading} 
        />
      </main>

      <footer className="app-footer">
        RAG Knowledge Assistant • Minimal Clean UI
      </footer>
    </div>
  );
}
