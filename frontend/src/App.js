import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import Terminal from './components/Terminal';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (token) {
      // Verify token and get user
      fetch('http://localhost:8000/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => res.json())
        .then(data => {
          if (data.username) {
            setUser(data);
          } else {
            // Invalid token
            localStorage.removeItem('token');
            setToken(null);
          }
        })
        .catch(() => {
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
