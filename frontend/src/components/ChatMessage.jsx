import React from 'react';

export default function ChatMessage({ message }) {
  const { role, content, sources } = message;
  const isUser = role === 'user';

  const extractFilename = (source) => {
    if (!source) return '';
    const isUrl = source.startsWith('http://') || source.startsWith('https://');
    if (isUrl) {
      return source;
    }
    const parts = source.split(/[/\\]/);
    return parts[parts.length - 1];
  };

  return (
    <div className={`message-row ${isUser ? 'message-row-user' : 'message-row-assistant'}`}>
      <div className={`message-bubble ${isUser ? 'bubble-user' : 'bubble-assistant'}`}>
        <div className="message-content">{content}</div>
        
        {!isUser && sources && sources.length > 0 && (
          <div className="message-sources">
            <div className="sources-title">Sources</div>
            <ul className="sources-list">
              {sources.map((source, idx) => {
                const name = extractFilename(source);
                const isUrl = source.startsWith('http://') || source.startsWith('https://');
                return (
                  <li key={idx}>
                    {isUrl ? (
                      <a href={source} target="_blank" rel="noopener noreferrer" className="source-link">
                        {name}
                      </a>
                    ) : (
                      <span>{name}</span>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
