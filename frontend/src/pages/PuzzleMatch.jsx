import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { puzzlesAPI, matchesAPI, createWebSocketConnection } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './PuzzleMatch.css';

const PuzzleMatch = () => {
  const { puzzleId } = useParams();
  const navigate = useNavigate();
  const { user, token } = useAuth();
  
  const [puzzle, setPuzzle] = useState(null);
  const [match, setMatch] = useState(null);
  const [matchId, setMatchId] = useState(null);
  const [inputData, setInputData] = useState('');
  const [answer, setAnswer] = useState('');
  const [roomCode, setRoomCode] = useState('');
  const [mode, setMode] = useState('select'); // select, waiting, active, completed
  const [feedback, setFeedback] = useState(null);
  const [opponentStatus, setOpponentStatus] = useState(null);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [loading, setLoading] = useState(false);
  
  const wsRef = useRef(null);
  const timerRef = useRef(null);

  useEffect(() => {
    // Fetch puzzle details
    const fetchPuzzle = async () => {
      try {
        const response = await puzzlesAPI.getById(puzzleId);
        setPuzzle(response.data);
      } catch (error) {
        console.error('Failed to fetch puzzle:', error);
      }
    };
    fetchPuzzle();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [puzzleId]);

  const connectWebSocket = (matchId) => {
    if (!token) return;
    
    try {
      const ws = createWebSocketConnection(matchId, token);
      
      ws.onopen = () => {
        console.log('WebSocket connected');
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'player_connected') {
          setOpponentStatus('connected');
        } else if (data.type === 'player_disconnected') {
          setOpponentStatus('disconnected');
        } else if (data.type === 'match_started') {
          setMode('active');
          startTimer();
        } else if (data.type === 'answer_submitted') {
          if (data.user_id !== user.id) {
            setOpponentStatus(data.is_correct ? 'solved' : 'attempted');
          }
        } else if (data.type === 'match_completed') {
          handleMatchComplete(data);
        }
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
      };
      
      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
    }
  };

  const startTimer = () => {
    timerRef.current = setInterval(() => {
      setTimeElapsed(prev => prev + 1);
    }, 1000);
  };

  const stopTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  };

  const handleCreateMatch = async (isPrivate) => {
    setLoading(true);
    try {
      const code = isPrivate ? generateRoomCode() : null;
      const response = await matchesAPI.create(puzzleId, code);
      const createdMatch = response.data;
      
      setMatch(createdMatch);
      setMatchId(createdMatch.id);
      setMode('waiting');
      
      if (isPrivate) {
        setRoomCode(createdMatch.room_code);
      }
      
      connectWebSocket(createdMatch.id);
      
      // Auto-start if both players join
      pollForOpponent(createdMatch.id);
    } catch (error) {
      console.error('Failed to create match:', error);
      setFeedback({ type: 'error', message: 'Failed to create match' });
    } finally {
      setLoading(false);
    }
  };

  const handleJoinMatch = async () => {
    setLoading(true);
    try {
      const response = await matchesAPI.join(roomCode || null);
      const joinedMatch = response.data;
      
      setMatch(joinedMatch);
      setMatchId(joinedMatch.id);
      
      connectWebSocket(joinedMatch.id);
      
      // Try to start the match
      await handleStartMatch(joinedMatch.id);
    } catch (error) {
      console.error('Failed to join match:', error);
      setFeedback({ type: 'error', message: error.response?.data?.detail || 'Failed to join match' });
    } finally {
      setLoading(false);
    }
  };

  const pollForOpponent = async (matchId) => {
    const interval = setInterval(async () => {
      try {
        const response = await matchesAPI.getDetails(matchId);
        const matchData = response.data;
        
        if (matchData.status === 'ready') {
          clearInterval(interval);
          // Both players joined, start match
          await handleStartMatch(matchId);
        }
      } catch (error) {
        clearInterval(interval);
      }
    }, 2000);
    
    // Stop polling after 5 minutes
    setTimeout(() => clearInterval(interval), 300000);
  };

  const handleStartMatch = async (matchId) => {
    try {
      const response = await matchesAPI.start(matchId);
      setInputData(response.data.input_data);
      setMode('active');
      startTimer();
      setFeedback({ type: 'info', message: 'Match started! Good luck!' });
    } catch (error) {
      console.error('Failed to start match:', error);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) return;
    
    setLoading(true);
    try {
      const response = await matchesAPI.submitAnswer(matchId, answer.trim());
      const result = response.data;
      
      if (result.is_correct) {
        setFeedback({ 
          type: 'success', 
          message: result.winner_id === user.id ? '🎉 Correct! You Win!' : '✓ Correct answer!' 
        });
        
        if (result.match_status === 'completed') {
          stopTimer();
          setMode('completed');
        }
      } else {
        setFeedback({ type: 'error', message: '✗ Incorrect answer, try again!' });
      }
    } catch (error) {
      setFeedback({ type: 'error', message: 'Failed to submit answer' });
    } finally {
      setLoading(false);
    }
  };

  const handleMatchComplete = (data) => {
    stopTimer();
    setMode('completed');
    
    const won = data.winner_id === user.id;
    setFeedback({
      type: won ? 'success' : 'info',
      message: won 
        ? `🎉 Congratulations! You won in ${formatTime(timeElapsed)}!`
        : `Match ended. ${data.winner_username} won!`
    });
  };

  const generateRoomCode = () => {
    return Math.random().toString(36).substring(2, 8).toUpperCase();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setFeedback({ type: 'info', message: 'Copied to clipboard!' });
  };

  if (!puzzle) {
    return <div className="loading">Loading puzzle...</div>;
  }

  return (
    <div className="puzzle-match-container">
      {/* Puzzle Description */}
      <article className="day-desc">
        <h2>--- Day {puzzle.day}: {puzzle.title} ---</h2>
        
        {puzzle.story && (
          <p className="puzzle-story">{puzzle.story}</p>
        )}
        
        <div className="puzzle-description">
          {puzzle.description}
        </div>
        
        <div className="puzzle-meta">
          <span className={`difficulty difficulty-${puzzle.difficulty}`}>
            {puzzle.difficulty}
          </span>
        </div>
      </article>

      {/* Match Controls */}
      {mode === 'select' && (
        <article className="day-desc match-controls">
          <h3>--- Choose Your Challenge ---</h3>
          <p>How would you like to compete?</p>
          
          <div className="match-options">
            <button 
              onClick={() => handleCreateMatch(false)}
              className="option-button public"
              disabled={loading}
            >
              <div className="option-title">⚔️ Quick Match</div>
              <div className="option-desc">Find a random opponent</div>
            </button>
            
            <button 
              onClick={() => handleCreateMatch(true)}
              className="option-button private"
              disabled={loading}
            >
              <div className="option-title">🎯 Private Room</div>
              <div className="option-desc">Challenge a friend</div>
            </button>
          </div>
          
          <div className="join-room">
            <p>Or join a friend's room:</p>
            <div className="join-input-group">
              <input
                type="text"
                placeholder="Enter room code"
                value={roomCode}
                onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
                maxLength={6}
              />
              <button 
                onClick={handleJoinMatch}
                disabled={!roomCode || loading}
              >
                Join
              </button>
            </div>
          </div>
        </article>
      )}

      {/* Waiting Room */}
      {mode === 'waiting' && (
        <article className="day-desc waiting-room">
          <h3>--- Waiting for Opponent ---</h3>
          <div className="waiting-animation">
            <span className="star">*</span>
            <span className="star">*</span>
            <span className="star">*</span>
          </div>
          
          {roomCode && (
            <div className="room-code-display">
              <p>Share this room code with your friend:</p>
              <div className="room-code">
                {roomCode}
                <button 
                  onClick={() => copyToClipboard(roomCode)}
                  className="copy-button"
                >
                  📋 Copy
                </button>
              </div>
            </div>
          )}
          
          <p className="quiet">Waiting for another player to join...</p>
        </article>
      )}

      {/* Active Match */}
      {mode === 'active' && (
        <>
          {/* Match HUD */}
          <div className="match-hud">
            <div className="hud-item timer">
              <span className="hud-label">Time:</span>
              <span className="hud-value">{formatTime(timeElapsed)}</span>
            </div>
            <div className="hud-item opponent">
              <span className="hud-label">Opponent:</span>
              <span className={`hud-value status-${opponentStatus || 'waiting'}`}>
                {opponentStatus === 'solved' ? '✓ Solved' :
                 opponentStatus === 'attempted' ? '⚠ Attempting' :
                 opponentStatus === 'disconnected' ? '⚠ Disconnected' :
                 '⏳ Working'}
              </span>
            </div>
          </div>

          {/* Input Data */}
          <article className="day-desc input-section">
            <h3>--- Your Puzzle Input ---</h3>
            <p className="hint">
              Copy this input to your IDE and solve the puzzle. 
              Submit your answer below when ready!
            </p>
            <div className="input-data">
              <button 
                onClick={() => copyToClipboard(inputData)}
                className="copy-button-float"
              >
                📋 Copy
              </button>
              <pre>{inputData}</pre>
            </div>
          </article>

          {/* Answer Submission */}
          <article className="day-desc answer-section">
            <h3>--- Submit Your Answer ---</h3>
            
            {feedback && (
              <div className={`feedback feedback-${feedback.type}`}>
                {feedback.message}
              </div>
            )}
            
            <div className="answer-input-group">
              <input
                type="text"
                placeholder="Enter your answer"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSubmitAnswer()}
                disabled={loading || mode === 'completed'}
              />
              <button 
                onClick={handleSubmitAnswer}
                disabled={!answer.trim() || loading || mode === 'completed'}
                className="submit-answer-button"
              >
                {loading ? 'Checking...' : 'Submit'}
              </button>
            </div>
          </article>
        </>
      )}

      {/* Match Completed */}
      {mode === 'completed' && (
        <article className="day-desc match-result">
          <h3>--- Match Complete ---</h3>
          
          {feedback && (
            <div className={`result-message ${feedback.type}`}>
              {feedback.message}
            </div>
          )}
          
          <div className="match-actions">
            <button onClick={() => navigate('/')}>
              Return to Calendar
            </button>
            <button onClick={() => navigate('/leaderboard')}>
              View Leaderboard
            </button>
            <button onClick={() => window.location.reload()}>
              Play Again
            </button>
          </div>
        </article>
      )}
    </div>
  );
};

export default PuzzleMatch;
