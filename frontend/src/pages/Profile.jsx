import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { statsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

const Profile = () => {
  const { username: urlUsername } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const [profileData, setProfileData] = useState(null);
  const [matchHistory, setMatchHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const isOwnProfile = !urlUsername || urlUsername === user?.username;

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        // Fetch user stats
        const statsResponse = isOwnProfile 
          ? await statsAPI.getMyStats()
          : await statsAPI.getUserStats(urlUsername);
        
        setProfileData(statsResponse.data);

        // Fetch match history
        const historyResponse = isOwnProfile
          ? await statsAPI.getMyMatchHistory()
          : await statsAPI.getUserMatchHistory(urlUsername);
        
        setMatchHistory(historyResponse.data || []);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfileData();
  }, [urlUsername, isOwnProfile]);

  const formatTime = (seconds) => {
    if (!seconds) return '-';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    });
  };

  const getRankBadge = (winRate) => {
    if (winRate >= 80) return { name: 'Legend', color: '#ffff66', icon: '👑' };
    if (winRate >= 70) return { name: 'Master', color: '#ff9966', icon: '⭐' };
    if (winRate >= 60) return { name: 'Expert', color: '#9999ff', icon: '💎' };
    if (winRate >= 50) return { name: 'Skilled', color: '#66ff99', icon: '🎯' };
    if (winRate >= 40) return { name: 'Intermediate', color: '#99ffff', icon: '📈' };
    return { name: 'Novice', color: '#cccccc', icon: '🌱' };
  };

  if (loading) {
    return (
      <article className="day-desc">
        <h2>--- Loading Profile ---</h2>
        <p className="loading-stars">
          <span className="star">*</span>
          <span className="star">*</span>
          <span className="star">*</span>
        </p>
      </article>
    );
  }

  if (!profileData) {
    return (
      <article className="day-desc">
        <h2>--- Profile Not Found ---</h2>
        <p>The user you're looking for doesn't exist or hasn't played any matches yet.</p>
        <button onClick={() => navigate('/')}>Return to Calendar</button>
      </article>
    );
  }

  const rank = getRankBadge(profileData.win_rate || 0);

  return (
    <div className="profile-container">
      {/* Profile Header */}
      <article className="day-desc profile-header">
        <div className="profile-title-row">
          <h2>--- Player Profile ---</h2>
          {isOwnProfile && (
            <button className="edit-profile-btn" onClick={() => navigate('/settings')}>
              ⚙️ Settings
            </button>
          )}
        </div>

        <div className="profile-main">
          <div className="profile-avatar">
            <div className="avatar-placeholder">
              {profileData.username?.charAt(0).toUpperCase() || '?'}
            </div>
          </div>

          <div className="profile-info">
            <h1 className="username">{profileData.username}</h1>
            
            <div className="rank-badge" style={{ borderColor: rank.color, color: rank.color }}>
              <span className="rank-icon">{rank.icon}</span>
              <span className="rank-name">{rank.name}</span>
            </div>

            <div className="profile-stats-quick">
              <div className="quick-stat">
                <span className="stat-label">Matches</span>
                <span className="stat-value">{profileData.total_matches || 0}</span>
              </div>
              <div className="quick-stat">
                <span className="stat-label">Wins</span>
                <span className="stat-value win">{profileData.matches_won || 0}</span>
              </div>
              <div className="quick-stat">
                <span className="stat-label">Win Rate</span>
                <span className="stat-value">{(profileData.win_rate || 0).toFixed(1)}%</span>
              </div>
              {profileData.current_streak > 0 && (
                <div className="quick-stat">
                  <span className="stat-label">Streak</span>
                  <span className="stat-value streak">{profileData.current_streak}🔥</span>
                </div>
              )}
            </div>

            {profileData.joined_date && (
              <p className="member-since">
                Member since {formatDate(profileData.joined_date)}
              </p>
            )}
          </div>
        </div>
      </article>

      {/* Detailed Statistics */}
      <article className="day-desc stats-detail">
        <h2>--- Statistics ---</h2>
        
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-card-icon">⚔️</div>
            <div className="stat-card-value">{profileData.total_matches || 0}</div>
            <div className="stat-card-label">Total Matches</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-icon">🏆</div>
            <div className="stat-card-value success">{profileData.matches_won || 0}</div>
            <div className="stat-card-label">Victories</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-icon">💔</div>
            <div className="stat-card-value">{(profileData.total_matches || 0) - (profileData.matches_won || 0)}</div>
            <div className="stat-card-label">Defeats</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-icon">📊</div>
            <div className="stat-card-value">{(profileData.win_rate || 0).toFixed(1)}%</div>
            <div className="stat-card-label">Win Rate</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-icon">⚡</div>
            <div className="stat-card-value">{formatTime(profileData.fastest_solve_seconds)}</div>
            <div className="stat-card-label">Fastest Solve</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-icon">⏱️</div>
            <div className="stat-card-value">{formatTime(Math.round(profileData.average_solve_seconds || 0))}</div>
            <div className="stat-card-label">Avg Solve Time</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-icon">🔥</div>
            <div className="stat-card-value streak">{profileData.current_streak || 0}</div>
            <div className="stat-card-label">Current Streak</div>
          </div>

          <div className="stat-card">
            <div className="stat-card-icon">🌟</div>
            <div className="stat-card-value">{profileData.best_streak || 0}</div>
            <div className="stat-card-label">Best Streak</div>
          </div>
        </div>
      </article>

      {/* Match History */}
      <article className="day-desc match-history">
        <h2>--- Match History ---</h2>
        
        {matchHistory.length === 0 ? (
          <p className="empty-state">
            No matches played yet. {isOwnProfile ? 'Start competing to build your legacy!' : 'This player hasn\'t competed yet.'}
          </p>
        ) : (
          <div className="history-table-container">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Puzzle</th>
                  <th>Opponent</th>
                  <th>Result</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {matchHistory.slice(0, 20).map((match, index) => {
                  const won = match.winner_username === profileData.username;
                  const opponent = match.player1_username === profileData.username 
                    ? match.player2_username 
                    : match.player1_username;
                  
                  return (
                    <tr key={match.id || index} className={won ? 'match-won' : 'match-lost'}>
                      <td className="match-date">{formatDate(match.created_at)}</td>
                      <td className="match-puzzle">
                        <button 
                          className="puzzle-link"
                          onClick={() => navigate(`/puzzle/${match.puzzle_id}`)}
                        >
                          Day {match.puzzle_day || '?'}
                        </button>
                      </td>
                      <td className="match-opponent">
                        {opponent ? (
                          <button
                            className="opponent-link"
                            onClick={() => navigate(`/profile/${opponent}`)}
                          >
                            {opponent}
                          </button>
                        ) : (
                          <span className="no-opponent">Solo</span>
                        )}
                      </td>
                      <td className={`match-result ${won ? 'result-win' : 'result-loss'}`}>
                        {won ? '✓ Win' : '✗ Loss'}
                      </td>
                      <td className="match-time">
                        {formatTime(match.solve_time_seconds)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {matchHistory.length > 20 && (
          <p className="hint">
            Showing 20 most recent matches out of {matchHistory.length} total
          </p>
        )}
      </article>

      {/* Actions */}
      {!isOwnProfile && (
        <article className="day-desc profile-actions">
          <h2>--- Actions ---</h2>
          <div className="action-buttons">
            <button className="action-btn challenge" onClick={() => navigate('/')}>
              ⚔️ Challenge to a Match
            </button>
            <button className="action-btn" onClick={() => navigate('/leaderboard')}>
              📊 Compare on Leaderboard
            </button>
          </div>
        </article>
      )}
    </div>
  );
};

export default Profile;
