import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import Terminal from './components/Terminal';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  console.log('App rendering - API_URL:', API_URL, 'Token exists:', !!token, 'User:', user);

  useEffect(() => {
    if (token) {
      // Verify token and get user
      fetch(`${API_URL}/api/v1/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => {
          if (!res.ok) {
            throw new Error('Token validation failed');
          }
          return res.json();
        })
        .then(data => {
          if (data.username) {
            setUser(data);
          } else {
            // Invalid token
            localStorage.removeItem('token');
            setToken(null);
          }
        })
        .catch((error) => {
          console.error('Token verification error:', error);
          localStorage.removeItem('token');
          setToken(null);
        });
    }
  }, [token]);

  const handleLogin = (newToken, userData) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  if (!token || !user) {
    return <Login onLogin={handleLogin} />;
  }

  return <Terminal user={user} onLogout={handleLogout} token={token} />;
}

export default App;
