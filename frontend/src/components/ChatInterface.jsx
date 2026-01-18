import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message to chat
    setMessages((prev) => [...prev, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat/`, {
        question: userMessage,
      });

      // Add bot response to chat
      setMessages((prev) => [
        ...prev,
        { 
          type: 'bot', 
          content: response.data.answer,
          sources: response.data.source_documents 
        },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          type: 'error',
          content: error.response?.data?.error || 'Failed to get response from server. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearHistory = async () => {
    try {
      await axios.post(`${API_BASE_URL}/clear-history/`);
      setMessages([]);
    } catch (error) {
      console.error('Error clearing history:', error);
      alert('Failed to clear history');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <h3>👋 Welcome to the RAG Chatbot!</h3>
            <p>Start a conversation by asking a question.</p>
            <p>I'll use my knowledge base to provide accurate answers.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-label">
                {message.type === 'user' ? '👤 You' : message.type === 'bot' ? '🤖 Bot' : '⚠️ Error'}
              </div>
              <div className="message-content">{message.content}</div>
              {message.sources && message.sources.length > 0 && (
                <div className="message-sources" style={{ marginTop: '0.5rem', fontSize: '0.85rem', opacity: 0.8 }}>
                  <details>
                    <summary style={{ cursor: 'pointer' }}>📚 Sources ({message.sources.length})</summary>
                    {message.sources.map((source, idx) => (
                      <div key={idx} style={{ marginTop: '0.25rem', paddingLeft: '1rem' }}>
                        {source.metadata?.source && <small>• {source.metadata.source}</small>}
                      </div>
                    ))}
                  </details>
                </div>
              )}
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot loading-message">
            <span>Bot is thinking</span>
            <div className="loading-dots">
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
              <div className="loading-dot"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-container" onSubmit={handleSendMessage}>
        <input
          type="text"
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
          disabled={isLoading}
        />
        <button type="submit" className="chat-button" disabled={isLoading || !input.trim()}>
          Send
        </button>
        {messages.length > 0 && (
          <button
            type="button"
            className="chat-button clear-button"
            onClick={handleClearHistory}
            disabled={isLoading}
          >
            Clear
          </button>
        )}
      </form>
    </div>
  );
}

export default ChatInterface;
