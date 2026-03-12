import React, { useState } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8080';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: '40px auto', fontFamily: 'sans-serif', padding: '0 16px' }}>
      <h2>🐳 Docker Model Runner Chatbot</h2>
      <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, minHeight: 300,
                    marginBottom: 16, background: '#fafafa', overflowY: 'auto', maxHeight: 480 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 12, textAlign: m.role === 'user' ? 'right' : 'left' }}>
            <span style={{
              display: 'inline-block', padding: '8px 14px', borderRadius: 16,
              background: m.role === 'user' ? '#0066cc' : '#e8e8e8',
              color: m.role === 'user' ? '#fff' : '#222',
              maxWidth: '80%', wordBreak: 'break-word'
            }}>
              {m.content}
            </span>
          </div>
        ))}
        {loading && <div style={{ color: '#888', fontStyle: 'italic' }}>Thinking…</div>}
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          style={{ flex: 1, padding: '10px 14px', borderRadius: 8, border: '1px solid #ccc', fontSize: 15 }}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
          placeholder="Type a message and press Enter…"
          disabled={loading}
        />
        <button
          style={{ padding: '10px 20px', borderRadius: 8, background: '#0066cc', color: '#fff',
                   border: 'none', cursor: 'pointer', fontSize: 15 }}
          onClick={send}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
