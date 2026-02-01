// DEV WORKFLOW TIP: For instant frontend updates (no rebuilds), add this to your docker-compose.yml under the frontend service ONLY:
//
//   services:
//     frontend:
//       # ...existing config...
//       volumes:
//         - ./frontend:/app/frontend
//
// Then run: docker-compose restart frontend
//
// This does NOT touch or rebuild the codearena backend image or container.
// DEV TIP: For instant frontend updates without rebuilding Docker images, add this to your docker-compose.yml (frontend service only):
//
//   services:
//     frontend:
//       # ...existing config...
//       volumes:
//         - ./frontend:/app/frontend
//
// Then run: docker-compose restart frontend
//
// This does NOT affect the codearena backend image or container.

import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { puzzlesAPI, matchesAPI, createWebSocketConnection } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './PuzzleMatch.css';

const PuzzleMatch = () => {
  const { puzzleId: routePuzzleId } = useParams();
  const [searchParams] = useSearchParams();
  // Support puzzleId from query (?puzzle=1) or route param
  const puzzleId = searchParams.get('puzzle') || routePuzzleId;
  const [resolvedPuzzleId, setResolvedPuzzleId] = useState(null);
  // Support mode from query (?mode=quick) or default
  const modeParam = searchParams.get('mode');
  const navigate = useNavigate();
  const { user, token } = useAuth();
  
  const [puzzle, setPuzzle] = useState(null);
  const [match, setMatch] = useState(null);
  const [matchId, setMatchId] = useState(null);
  const [inputData, setInputData] = useState('');
  const [expectedAnswer, setExpectedAnswer] = useState(null);
  const [answer, setAnswer] = useState('');
  const [roomCode, setRoomCode] = useState('');
  const [mode, setMode] = useState('select'); // select, waiting, active, completed
  const [feedback, setFeedback] = useState(null);
  const [opponentStatus, setOpponentStatus] = useState(null);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [loading, setLoading] = useState(false);
  
  const wsRef = useRef(null);
  const timerRef = useRef(null);
  const submittingRef = useRef(false);

  useEffect(() => {
    // Try to resolve puzzleId (may be a day or id)
    let isMounted = true;
    const resolveIdAndFetch = async () => {
      try {
        // Try direct fetch by id
        const response = await puzzlesAPI.getById(puzzleId);
        if (isMounted) {
          setPuzzle(response.data);
          setResolvedPuzzleId(response.data.id);
        }
      } catch (error) {
        // If not found, try to map day to id
        try {
          const all = await puzzlesAPI.getAll();
          const found = all.data.find(p => String(p.day) === String(puzzleId));
          if (found) {
            const resp2 = await puzzlesAPI.getById(found.id);
            if (isMounted) {
              setPuzzle(resp2.data);
              setResolvedPuzzleId(found.id);
            }
          } else {
            if (isMounted) setPuzzle(null);
          }
        } catch (e2) {
          if (isMounted) setPuzzle(null);
        }
      }
    };
    resolveIdAndFetch();
    return () => {
      isMounted = false;
      if (wsRef.current) wsRef.current.close();
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [puzzleId]);

  // If the page was opened with ?mode=quick, auto-start a quick (public) match
  useEffect(() => {
    if (modeParam === 'quick' && resolvedPuzzleId && !match && !matchId) {
      // small delay to ensure UI is ready
      handleCreateMatch(false).catch(err => console.error('Auto quick match failed:', err));
    }
  }, [modeParam, resolvedPuzzleId]);

  const connectWebSocket = (matchId) => {
    if (!token) return;
    
    try {
      const ws = createWebSocketConnection(matchId, token);
      
      ws.onopen = () => {
        // WebSocket connected
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'player_connected') {
          setOpponentStatus('connected');
        } else if (data.type === 'player_disconnected') {
          setOpponentStatus('disconnected');
        } else if (data.type === 'match_started') {
          // When informed the match started by another player, fetch our player-specific input
          (async () => {
            try {
              const detailsResp = await matchesAPI.getDetails(matchId);
              const details = detailsResp.data || {};
              setInputData(details.input_data || '');
              setExpectedAnswer(details.expected_answer || null);
              setMode('active');
              startTimer();
            } catch (err) {
              console.error('Failed to fetch match details after websocket start:', err);
            }
          })();
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
        // WebSocket disconnected
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
      if (!resolvedPuzzleId) {
        console.warn('Puzzle not resolved yet, cannot create match.');
        setFeedback({ type: 'error', message: 'Puzzle not loaded yet. Please wait.' });
        setLoading(false);
        return;
      }
      const code = isPrivate ? generateRoomCode() : null;
      const pid = resolvedPuzzleId;
      const response = await matchesAPI.create(pid, code);
      const createdMatch = response.data;
      setMatch(createdMatch);
      setMatchId(createdMatch.id);
      connectWebSocket(createdMatch.id);
      // If backend marked match as ready (another player joined), start it.
      // Also auto-start public quick matches without a room code and without a second player (solo play).
      if (createdMatch.status === 'ready' || (!createdMatch.room_code && !createdMatch.player2_id)) {
        await handleStartMatch(createdMatch.id);
        setMode('active');
      } else {
        // Otherwise show waiting room and poll for opponent (private rooms or public waiting)
        setMode('waiting');
        if (createdMatch.room_code) setRoomCode(createdMatch.room_code);
        pollForOpponent(createdMatch.id);
      }
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
      // Update match state from response
      const res = response.data || {};
      const updatedMatch = {
        id: res.match_id || matchId,
        status: res.status || (match && match.status) || 'active',
        started_at: res.started_at || null,
      };
      setMatch(updatedMatch);
      setMatchId(updatedMatch.id);
      setInputData(res.input_data || '');
      setExpectedAnswer(res.expected_answer || null);

      if (res.input_data) {
        setMode('active');
        startTimer();
        setFeedback({ type: 'info', message: 'Match started! Good luck!' });
      } else {
        console.warn('No input_data received from backend!', res);
        setFeedback({ type: 'error', message: 'No puzzle input received. Please try again or contact support.' });
        // Keep user in waiting state to avoid showing empty input
        setMode('waiting');
      }
    } catch (error) {
      console.error('Failed to start match:', error);
      setFeedback({ type: 'error', message: 'Failed to start match' });
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim() || loading || submittingRef.current) return;
    
    submittingRef.current = true;
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
      submittingRef.current = false;
    }
  };

  const handleMatchComplete = (data) => {
    stopTimer();
    setMode('completed');
    
    const won = data.winner_id === user.id;
    setFeedback({
      type: won ? 'success' : 'error',
      message: won 
        ? `🎉 Congratulations! You won in ${formatTime(timeElapsed)}!`
        : `✗ Match lost. ${data.winner_username} solved it.`
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

          {!user && (
            <div className="auth-warning">
              <strong>Sign in to create or join matches.</strong>
            </div>
          )}
          
          <div className="match-options">
            <button 
              onClick={() => handleCreateMatch(false)}
              className="option-button public"
              disabled={loading || !user}
            >
              <div className="option-title">⚔️ Quick Match</div>
              <div className="option-desc">Find a random opponent</div>
            </button>
            
            <button 
              onClick={() => handleCreateMatch(true)}
              className="option-button private"
              disabled={loading || !user}
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
                disabled={!roomCode || loading || !user}
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
              Click the button below to open your puzzle input in a new tab.
            </p>
            <div className="input-data">
              <button 
                onClick={() => {
                  const newWindow = window.open('', '_blank');
                  newWindow.document.write(`
                    <!DOCTYPE html>
                    <html>
                      <head>
                        <title>Puzzle Input - Day ${puzzle.day}</title>
                        <style>
                          body {
                            background-color: #0f0f23;
                            color: #cccccc;
                            font-family: 'Source Code Pro', monospace;
                            padding: 20px;
                            margin: 0;
                          }
                          pre {
                            background-color: #10101a;
                            border: 1px solid #333340;
                            padding: 15px;
                            overflow: auto;
                            white-space: pre-wrap;
                            word-wrap: break-word;
                          }
                          h1 {
                            color: #00cc00;
                          }
                          .copy-btn {
                            background-color: #009900;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            cursor: pointer;
                            font-family: 'Source Code Pro', monospace;
                            margin-bottom: 20px;
                          }
                          .copy-btn:hover {
                            background-color: #00cc00;
                          }
                        </style>
                      </head>
                      <body>
                        <h1>Day ${puzzle.day}: ${puzzle.title}</h1>
                        <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('input').textContent); this.textContent='Copied!';">📋 Copy to Clipboard</button>
                        <pre id="input">${inputData}</pre>
                      </body>
                    </html>
                  `);
                  newWindow.document.close();
                }}
                className="get-input-button"
              >
                📄 Get Puzzle Input
              </button>
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

      {/* Debug Panel */}
      <div className="debug-panel">
        <h4>Debug</h4>
        <pre style={{whiteSpace: 'pre-wrap', maxHeight: 200, overflow: 'auto'}}>
{JSON.stringify({ mode, matchId, match, inputData, expectedAnswer, feedback }, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default PuzzleMatch;
