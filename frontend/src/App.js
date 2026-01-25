import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components';
import { AuthProvider, useAuth } from './context/AuthContext';
import Calendar from './pages/Calendar';
import PuzzleDetail from './pages/PuzzleDetail';
import PuzzleMatch from './pages/PuzzleMatch';
import Leaderboard from './pages/Leaderboard';
import Login from './pages/Login';
import './App.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <Layout year="2026">
        <article className="day-desc">
          <h2>Loading...</h2>
        </article>
      </Layout>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Main App Component
function AppContent() {
  const { user, logout } = useAuth();

  const navigate = (path) => {
    window.location.href = path;
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navLinks = {
    global: [
      { href: '/', label: 'Calendar' },
      { href: '/leaderboard', label: 'Leaderboard' },
    ],
    event: user ? [
      { href: '#', label: user.username },
      { href: '#', label: 'Logout', onClick: handleLogout },
    ] : [
      { href: '/login', label: 'Login' }
    ]
  };

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout year="2026" navLinks={navLinks}>
                <Calendar />
              </Layout>
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/puzzle/:puzzleId"
          element={
            <ProtectedRoute>
              <Layout year="2026" navLinks={navLinks}>
                <PuzzleDetail />
              </Layout>
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/match"
          element={
            <ProtectedRoute>
              <Layout year="2026" navLinks={navLinks}>
                <PuzzleMatch />
              </Layout>
            </ProtectedRoute>
          }
        />
        
        <Route
          path="/leaderboard"
          element={
            <ProtectedRoute>
              <Layout year="2026" navLinks={navLinks}>
                <Leaderboard />
              </Layout>
            </ProtectedRoute>
          }
        />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;

