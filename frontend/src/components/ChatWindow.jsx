import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';

export default function ChatWindow({ messages, onSendMessage, loading }) {
  const [question, setQuestion] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    onSendMessage(question.trim());
    setQuestion('');
  };

  return (
    <div className="chat-window card">
      <div className="chat-messages-container">
        {messages.length === 0 ? (
          <div className="chat-empty-state">
            Upload a document or provide a URL to start chatting.
          </div>
        ) : (
          <div className="chat-messages-list">
            {messages.map((msg, index) => (
              <ChatMessage key={index} message={msg} />
            ))}
            
            {loading && (
              <div className="message-row message-row-assistant">
                <div className="message-bubble bubble-assistant bubble-thinking">
                  <span className="thinking-text">Thinking...</span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask something about your document..."
          disabled={loading}
          required
          className="chat-input"
        />
        <button
          type="submit"
          className="btn-primary btn-send"
          disabled={!question.trim() || loading}
        >
          Send
        </button>
      </form>
    </div>
  );
}
