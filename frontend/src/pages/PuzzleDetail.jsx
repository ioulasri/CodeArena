import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { puzzlesAPI } from '../services/api';
import './PuzzleDetail.css';

const PuzzleDetail = () => {
  const { puzzleId } = useParams();
  const navigate = useNavigate();
  const [puzzle, setPuzzle] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPuzzle = async () => {
      try {
        const response = await puzzlesAPI.getById(puzzleId);
        setPuzzle(response.data);
      } catch (error) {
        console.error('Failed to fetch puzzle:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPuzzle();
  }, [puzzleId]);

  const handleStartMatch = (mode) => {
    navigate(`/match?puzzle=${puzzleId}&mode=${mode}`);
  };

  if (loading) {
    return (
      <article className="day-desc">
        <h2>Loading puzzle...</h2>
      </article>
    );
  }

  if (!puzzle) {
    return (
      <article className="day-desc">
        <h2>Puzzle not found</h2>
        <p>
          <a href="/" onClick={(e) => { e.preventDefault(); navigate('/'); }}>
            Return to calendar
          </a>
        </p>
      </article>
    );
  }

  // Story content based on puzzle type
  const getStoryContent = () => {
    switch (puzzle.generator_type) {
      case 'crystal_sum':
        return (
          <>
            <p>
              The elves have discovered a mysterious cave filled with glowing crystals. 
              Each crystal contains a unique magical energy value, represented by numbers 
              carved into their surfaces.
            </p>
            <p>
              The ancient texts speak of a <em className="star">Great Sum</em> - the total 
              energy that can be harnessed when all crystals are combined. However, each 
              adventurer receives a <em>unique set</em> of crystals, so no two explorers 
              will have the same answer!
            </p>
            <p>
              Your task is simple: <span className="puzzle-marker">calculate the sum of 
              all crystal values in your personal input</span>. The first to submit the 
              correct answer wins the race! ⚡
            </p>
          </>
        );
      
      case 'pattern_counter':
        return (
          <>
            <p>
              Deep in the northern data streams, patterns emerge from the chaos. The 
              elves need help counting how many times a specific sequence appears in 
              the corrupted transmission logs.
            </p>
            <p>
              Your scanner has picked up <em className="star">unique transmission data</em> 
              - different from any other adventurer's. Within this data, a pattern repeats 
              itself, sometimes overlapping, sometimes hidden in plain sight.
            </p>
            <p>
              <span className="puzzle-marker">Count all occurrences of the target pattern</span> 
              in your input data. Remember: patterns can overlap! The fastest pattern 
              detective wins. 🔍
            </p>
          </>
        );
      
      case 'grid_path':
        return (
          <>
            <p>
              The ice maze of the North Pole shifts every hour. Each traveler who enters 
              receives a <em className="star">unique maze configuration</em> - walls appear 
              in different locations, creating a personal challenge.
            </p>
            <p>
              You must navigate from the <code>START</code> position to the <code>END</code> 
              position, but you can only move up, down, left, or right. Walls (marked as <code>#</code>) 
              block your path, while open spaces (marked as <code>.</code>) are traversable.
            </p>
            <p>
              <span className="puzzle-marker">Find the length of the shortest path</span> from 
              START to END. Every step counts, and the quickest pathfinder wins the challenge! 🗺️
            </p>
          </>
        );
      
      case 'sequence_finder':
        return (
          <>
            <p>
              The elves' number sequences have been scrambled by a mischievous imp! Each 
              sequence follows a mathematical pattern, but one number has gone missing.
            </p>
            <p>
              Your mystical detector has captured a <em className="star">unique sequence</em> 
              - different from all other adventurers. The numbers follow a hidden rule, 
              and somewhere in the pattern, there's a gap where a number should be.
            </p>
            <p>
              <span className="puzzle-marker">Identify and report the missing number</span>. 
              The sequence might be arithmetic, geometric, or follow a more complex pattern. 
              The first to decode it wins! 🔢
            </p>
          </>
        );
      
      case 'tower_blocks':
        return (
          <>
            <p>
              The elves are building towers from magical blocks. Each block has a specific 
              height value, and they can be stacked according to ancient construction rules.
            </p>
            <p>
              You've received a <em className="star">unique set of blocks</em> - each 
              adventurer gets different heights and quantities. The tower must be stable, 
              and certain blocks can only be placed on top of others following the 
              magical laws of physics.
            </p>
            <p>
              <span className="puzzle-marker">Calculate the maximum height</span> your 
              tower can reach using the blocks in your input. Stack wisely - the tallest 
              tower built fastest wins the competition! 🏗️
            </p>
          </>
        );
      
      default:
        return (
          <p>
            Solve this puzzle by analyzing your unique input data. Each player receives 
            different input, ensuring a fair competition. The first to submit the correct 
            answer wins!
          </p>
        );
    }
  };

  return (
    <div className="puzzle-detail-container">
      <article className="day-desc">
        <h2>--- Day {puzzle.day}: {puzzle.title} ---</h2>
        {getStoryContent()}
      </article>

      <article className="day-desc">
        <h2>--- Challenge Modes ---</h2>
        <p>
          Choose how you want to compete:
        </p>
        
        <div className="challenge-modes">
          <div className="mode-card" onClick={() => handleStartMatch('quick')}>
            <h3>⚡ Quick Match</h3>
            <p>
              Jump into the action immediately! Get matched with a random opponent 
              from the queue and race to solve your puzzle.
            </p>
            <button className="mode-button quick">Start Quick Match</button>
          </div>

          <div className="mode-card" onClick={() => handleStartMatch('private')}>
            <h3>🔐 Private Room</h3>
            <p>
              Create a private room and challenge a specific friend. Share the 
              room code and compete head-to-head!
            </p>
            <button className="mode-button private">Create Private Room</button>
          </div>
        </div>

        <div className="puzzle-info">
          <p>
            <span className={`difficulty-badge ${puzzle.difficulty}`}>
              {puzzle.difficulty.toUpperCase()}
            </span>
            <span className="puzzle-type">
              Type: {puzzle.generator_type.replace('_', ' ')}
            </span>
          </p>
        </div>

        <p className="back-link">
          <a href="/" onClick={(e) => { e.preventDefault(); navigate('/'); }}>
            ← Back to Calendar
          </a>
        </p>
      </article>
    </div>
  );
};

export default PuzzleDetail;
