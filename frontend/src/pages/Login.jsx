import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Login.css';

const Login = () => {
  const [mode, setMode] = useState('login'); // 'login' or 'register'
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login, register, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let result;
      if (mode === 'login') {
        result = await login(username, password);
      } else {
        result = await register(username, email, password);
      }

      if (result.success) {
        // Navigation will happen via useEffect when isAuthenticated becomes true
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <article className="day-desc login-box">
        <h2>--- {mode === 'login' ? 'Sign In' : 'Register'} ---</h2>
        
        <p>
          {mode === 'login' 
            ? 'Welcome back! Enter your credentials to continue your puzzle journey.'
            : 'Join the arena! Create an account to start challenging others.'
          }
        </p>

        {error && (
          <div className="error-message">
            <span className="error-icon">⚠</span> {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
              disabled={loading}
            />
          </div>

          {mode === 'register' && (
            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                disabled={loading}
              />
            </div>
          )}

          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
              disabled={loading}
            />
          </div>

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Processing...' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        <div className="mode-switch">
          {mode === 'login' ? (
            <p>
              Don't have an account?{' '}
              <button 
                onClick={() => setMode('register')}
                className="link-button"
                disabled={loading}
              >
                Register here
              </button>
            </p>
          ) : (
            <p>
              Already have an account?{' '}
              <button 
                onClick={() => setMode('login')}
                className="link-button"
                disabled={loading}
              >
                Sign in
              </button>
            </p>
          )}
        </div>
      </article>
    </div>
  );
};

export default Login;
