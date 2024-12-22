import React, { useState } from 'react';
import './App.css';

function App() {
  const [content, setContent] = useState('');
  const [qrCode, setQrCode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateQRCode = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(process.env.REACT_APP_API_ENDPOINT + '/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': process.env.REACT_APP_API_KEY
        },
        body: JSON.stringify({ content })
      });

      if (!response.ok) {
        throw new Error('Failed to generate QR code');
      }

      const data = await response.json();
      setQrCode(data.url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>QR Code Generator</h1>
        <div className="input-container">
          <input
            type="text"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Enter text or URL"
          />
          <button 
            onClick={generateQRCode}
            disabled={loading || !content}
          >
            {loading ? 'Generating...' : 'Generate QR Code'}
          </button>
        </div>
        {error && <p className="error">{error}</p>}
        {qrCode && (
          <div className="qr-container">
            <img src={qrCode} alt="Generated QR Code" />
            <a href={qrCode} download>Download QR Code</a>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
