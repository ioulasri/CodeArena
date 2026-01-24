import React from 'react';
import './PuzzleArticle.css';

const PuzzleArticle = ({ 
  day,
  title,
  children,
  completed = false 
}) => {
  return (
    <article className={`day-desc ${completed ? 'completed' : ''}`}>
      <h2>--- Day {day}: {title} ---</h2>
      {children}
    </article>
  );
};

export default PuzzleArticle;
