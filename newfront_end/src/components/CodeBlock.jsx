import React, { useRef } from 'react';
import './CodeBlock.css';

const CodeBlock = ({ children, language = 'text' }) => {
  const codeRef = useRef(null);

  const handleTripleClick = (e) => {
    if (e.detail === 3) {
      const selection = window.getSelection();
      selection.removeAllRanges();
      const range = document.createRange();
      range.selectNodeContents(codeRef.current);
      selection.addRange(range);
    }
  };

  return (
    <pre>
      <code 
        ref={codeRef}
        className={language ? `language-${language}` : ''}
        onClick={handleTripleClick}
      >
        {children}
      </code>
    </pre>
  );
};

export default CodeBlock;
