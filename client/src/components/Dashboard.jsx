import React, { useState } from 'react';
import '../styles/dashboard.css';

const Dashboard = () => {
  const username = localStorage.getItem('username') || 'User';
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  const logout = () => {
    localStorage.clear();
    window.location.href = '/';
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput(''); // Clear input immediately

    try {
      const response = await fetch('http://localhost:8000/chat/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input }),
      });

      const data = await response.json();
      const botReply = { sender: 'bot', text: data.answer };
      setMessages((prev) => [...prev, botReply]);
    } catch (error) {
      console.error('Error fetching bot response:', error);
    }
  };

  return (
    <div className="flex h-screen font-sans">
      {/* Sidebar */}
      <div className="sidebar">
        <div>
          <h2 className="sidebar-header">Welcome, {username}</h2>
        </div>
        <button onClick={logout} className="logout-btn">
          Logout
        </button>
      </div>

      {/* Chat Area */}
      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={msg.sender === 'user' ? 'user-msg' : 'bot-msg'}>
              <p className="text-sm">{msg.text}</p>
            </div>
          ))}
        </div>

        {/* Input Section */}
        <div className="input-section">
          <input
            type="text"
            className="input-box"
            placeholder="Ask something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
          />
          <button onClick={handleSubmit} className="send-btn">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
