import React, { useState } from 'react';

const Dashboard = () => {
  const username = localStorage.getItem('username') || 'User';
  const token = localStorage.getItem('token');

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);

  const logout = () => {
    localStorage.clear();
    window.location.href = '/';
  };

const handleSubmit = async () => {
  if (!input.trim()) return;

  const userMessage = { sender: 'user', text: input };
  setMessages((prev) => [...prev, userMessage]);

  try {
    const response = await fetch('http://localhost:8000/chat/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Remove Authorization if you're not protecting /chat/query
        // Otherwise, make sure backend checks token correctly
      },
      body: JSON.stringify({ question: input }), // ✅ Note: "question" not "query"
    });

    const data = await response.json();
    const botReply = { sender: 'bot', text: data.answer }; // ✅ "answer" not "result"
    setMessages((prev) => [...prev, botReply]);
    setHistory((prev) => [input, ...prev.slice(0, 4)]);
  } catch (error) {
    console.error('Error fetching bot response:', error);
  }

  setInput('');
};


  return (
    <div className="flex h-screen">
      {/* Left Sidebar */}
      <div className="w-1/4 bg-gray-100 p-4 overflow-y-auto">
        <h3 className="text-lg font-semibold mb-4">Last 5 Queries</h3>
        <ul className="space-y-2">
          {history.map((q, i) => (
            <li key={i} className="text-sm text-gray-700 bg-white p-2 rounded shadow-sm">
              {q}
            </li>
          ))}
        </ul>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b shadow">
          <h2 className="text-xl font-bold">Welcome, {username}</h2>
          <div className="relative">
            <div
              className="h-10 w-10 bg-blue-500 text-white rounded-full flex items-center justify-center cursor-pointer"
              onClick={() => setShowDropdown(!showDropdown)}
            >
              {username[0].toUpperCase()}
            </div>
            {showDropdown && (
              <div className="absolute right-0 mt-2 bg-white border rounded shadow z-10">
                <button
                  onClick={logout}
                  className="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100 w-full text-left"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded max-w-xl ${
                msg.sender === 'user'
                  ? 'bg-blue-100 self-end text-right'
                  : 'bg-green-100 self-start text-left'
              }`}
            >
              <p className="text-sm">{msg.text}</p>
            </div>
          ))}
        </div>

        {/* Input Section */}
        <div className="p-4 border-t flex gap-2">
          <input
            type="text"
            className="flex-1 p-2 border rounded"
            placeholder="Ask something..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
          />
          <button
            onClick={handleSubmit}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
