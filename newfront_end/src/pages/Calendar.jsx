import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { puzzlesAPI, statsAPI } from '../services/api';
import './Calendar.css';

const Calendar = () => {
  const [puzzles, setPuzzles] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [puzzlesRes, statsRes] = await Promise.all([
          puzzlesAPI.getAll(),
          statsAPI.getMyStats()
        ]);
        setPuzzles(puzzlesRes.data);
        setStats(statsRes.data);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handlePuzzleClick = (puzzle) => {
    navigate(`/puzzle/${puzzle.id}`);
  };

  if (loading) {
    return (
      <article className="day-desc">
        <h2>Loading puzzles...</h2>
        <p className="loading-stars">
          <span className="star">*</span>
          <span className="star">*</span>
          <span className="star">*</span>
        </p>
      </article>
    );
  }

  return (
    <div className="calendar-container">
      {/* User Stats Summary */}
      {stats && stats.total_matches > 0 && (
        <article className="day-desc stats-summary">
          <h2>--- Your Stats ---</h2>
          <p>
            You've completed <em className="star">{stats.total_matches}</em> matches,
            winning <em className="star">{stats.matches_won}</em> of them
            (win rate: <em className="star">{stats.win_rate}%</em>).
          </p>
          {stats.current_streak > 0 && (
            <p>
              Current streak: <em className="star">{stats.current_streak}</em> 🔥
            </p>
          )}
        </article>
      )}

      {/* Puzzle Calendar */}
      <article className="day-desc">
        <h2>--- Puzzle Calendar ---</h2>
        <p>
          Welcome to CodeArena! Challenge your friends to solve these mind-bending puzzles.
          Each player gets unique input data - solve it in your own IDE, then submit your answer.
          First one to solve wins! 🏆
        </p>

        <div className="calendar-grid">
          {puzzles.map((puzzle) => (
            <div
              key={puzzle.id}
              className={`calendar-day difficulty-${puzzle.difficulty}`}
              onClick={() => handlePuzzleClick(puzzle)}
            >
              <div className="day-number">{puzzle.day}</div>
              <div className="day-title">{puzzle.title}</div>
              <div className="day-difficulty">{puzzle.difficulty}</div>
            </div>
          ))}
        </div>

        <p className="hint">
          💡 <em>Tip:</em> Create a private room to challenge a specific friend, 
          or join the public queue for a random opponent!
        </p>
      </article>
    </div>
  );
};

export default Calendar;
