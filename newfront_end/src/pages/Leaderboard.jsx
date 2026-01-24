import React, { useState, useEffect } from 'react';
import { statsAPI } from '../services/api';
import './Leaderboard.css';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await statsAPI.getLeaderboard(100);
        setLeaderboard(response.data);
      } catch (error) {
        console.error('Failed to fetch leaderboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  const formatTime = (seconds) => {
    if (!seconds) return '-';
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  if (loading) {
    return (
      <article className="day-desc">
        <h2>--- Leaderboard ---</h2>
        <p className="loading">Loading rankings...</p>
      </article>
    );
  }

  return (
    <div className="leaderboard-container">
      <article className="day-desc">
        <h2>--- Leaderboard ---</h2>
        <p>
          The greatest puzzle solvers in the arena. Compete, solve, and claim your place among the legends!
        </p>

        {leaderboard.length === 0 ? (
          <p className="empty-state">
            No rankings yet. Be the first to compete and set the pace!
          </p>
        ) : (
          <div className="leaderboard-table-container">
            <table className="leaderboard-table">
              <thead>
                <tr>
                  <th className="rank-col">Rank</th>
                  <th className="name-col">Player</th>
                  <th className="stat-col">Matches</th>
                  <th className="stat-col">Wins</th>
                  <th className="stat-col">Win Rate</th>
                  <th className="stat-col">Fastest</th>
                  <th className="stat-col">Avg Time</th>
                  <th className="stat-col">Streak</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((entry, index) => (
                  <tr 
                    key={entry.id}
                    className={`leaderboard-row ${index < 3 ? 'top-rank' : ''}`}
                  >
                    <td className="rank-col">
                      {index === 0 && <span className="medal gold">🥇</span>}
                      {index === 1 && <span className="medal silver">🥈</span>}
                      {index === 2 && <span className="medal bronze">🥉</span>}
                      {index > 2 && <span className="rank-number">#{index + 1}</span>}
                    </td>
                    <td className="name-col">
                      <span className="username">{entry.username}</span>
                    </td>
                    <td className="stat-col">{entry.total_matches}</td>
                    <td className="stat-col stat-wins">{entry.matches_won}</td>
                    <td className="stat-col">
                      <span className={`win-rate ${
                        entry.win_rate >= 70 ? 'excellent' :
                        entry.win_rate >= 50 ? 'good' : 'average'
                      }`}>
                        {entry.win_rate.toFixed(1)}%
                      </span>
                    </td>
                    <td className="stat-col stat-time">
                      {formatTime(entry.fastest_solve_seconds)}
                    </td>
                    <td className="stat-col stat-time">
                      {formatTime(Math.round(entry.average_solve_seconds))}
                    </td>
                    <td className="stat-col">
                      {entry.current_streak > 0 && (
                        <span className="streak">
                          {entry.current_streak}🔥
                        </span>
                      )}
                      {entry.current_streak === 0 && '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <p className="hint">
          💡 <em>Win matches to climb the ranks!</em> Fastest solve times and win streaks 
          make you a true champion.
        </p>
      </article>
    </div>
  );
};

export default Leaderboard;
