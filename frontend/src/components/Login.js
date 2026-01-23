import React, { useState } from 'react';
import './Login.css';

function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isRegister) {
        // Register
        const registerRes = await fetch('http://localhost:8000/api/v1/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, email, password })
        });

        if (!registerRes.ok) {
          const data = await registerRes.json();
          throw new Error(data.detail || 'Registration failed');
        }
      }

      // Login
      const loginRes = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (!loginRes.ok) {
        const data = await loginRes.json();
        throw new Error(data.detail || 'Login failed');
      }

      const loginData = await loginRes.json();

      // Get user data
      const userRes = await fetch('http://localhost:8000/api/v1/auth/me', {
        headers: { 'Authorization': `Bearer ${loginData.access_token}` }
      });

      const userData = await userRes.json();
      onLogin(loginData.access_token, userData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="terminal-window">
        <div className="terminal-header">
          <span className="terminal-title">$ CodeArena Terminal v1.0.0</span>
        </div>
        <div className="terminal-body">
          <pre className="ascii-art">{`
   ____          _         _                        
  / ___|___   __| | ___   / \\   _ __ ___ _ __   __ _ 
 | |   / _ \\ / _\` |/ _ \\ / _ \\ | '__/ _ \\ '_ \\ / _\` |
 | |__| (_) | (_| |  __// ___ \\| | |  __/ | | | (_| |
  \\____\\___/ \\__,_|\\___/_/   \\_\\_|  \\___|_| |_|\\__,_|
          `}</pre>

          <p className="welcome-text">
            {isRegister ? '> REGISTER NEW USER' : '> USER AUTHENTICATION REQUIRED'}
          </p>

          {error && <p className="error-text">ERROR: {error}</p>}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label>{'> '} USERNAME:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={loading}
                autoFocus
              />
            </div>

            {isRegister && (
              <div className="form-group">
                <label>{'> '} EMAIL:</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={loading}
                />
              </div>
            )}

            <div className="form-group">
              <label>{'> '} PASSWORD:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <button type="submit" disabled={loading} className="submit-btn">
              {loading ? '> PROCESSING...' : isRegister ? '> REGISTER' : '> LOGIN'}
            </button>
          </form>

          <button
            onClick={() => setIsRegister(!isRegister)}
            className="toggle-btn"
            disabled={loading}
          >
            {isRegister ? '> ALREADY HAVE AN ACCOUNT? LOGIN' : '> NEW USER? REGISTER'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
