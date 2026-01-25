import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),
  
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  
  getCurrentUser: () =>
    api.get('/auth/me'),
  // allow passing a token directly for initial verification (won't rely on localStorage)
  getCurrentUserWithToken: (token) =>
    api.get('/auth/me', token ? { headers: { Authorization: `Bearer ${token}` } } : {}),
};

// Puzzles API
export const puzzlesAPI = {
  getAll: () =>
    api.get('/matches/puzzles'),
  
  getById: (id) =>
    api.get(`/matches/puzzles/${id}`),
};

// Matches API
export const matchesAPI = {
  create: (puzzleId, roomCode = null) =>
    api.post('/matches/matches/create', { puzzle_id: puzzleId, room_code: roomCode }),
  
  join: (roomCode = null) =>
    api.post('/matches/matches/join', { room_code: roomCode }),
  
  start: (matchId) =>
    api.post(`/matches/matches/${matchId}/start`),
  
  submitAnswer: (matchId, answer) =>
    api.post(`/matches/matches/${matchId}/submit`, { answer }),
  
  getDetails: (matchId) =>
    api.get(`/matches/matches/${matchId}`),
  
  getHistory: (limit = 50) =>
    api.get(`/matches/matches/user/history?limit=${limit}`),
};

// Stats API
export const statsAPI = {
  getMyStats: () =>
    api.get('/matches/stats/me'),
  
  getLeaderboard: (limit = 100) =>
    api.get(`/matches/leaderboard?limit=${limit}`),
};

// Users API
export const usersAPI = {
  getProfile: (username) =>
    api.get(`/users/${encodeURIComponent(username)}/profile`),
};

// WebSocket connection
export const createWebSocketConnection = (matchId, token) => {
  const WS_URL = API_URL.replace('http', 'ws').replace('/api/v1', '');
  return new WebSocket(`${WS_URL}/api/v1/ws/match/${matchId}?token=${token}`);
};

export default api;
