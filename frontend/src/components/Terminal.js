import React, { useState, useEffect } from 'react';
import './Terminal.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Terminal({ user, onLogout, token }) {
  const [problems, setProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [submissions, setSubmissions] = useState([]);
  const [currentView, setCurrentView] = useState('problems'); // problems, editor, submissions
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProblems();
  }, []);

  const fetchProblems = async () => {
    try {
      const res = await fetch(`${API_URL}/api/v1/problems/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setProblems(data);
    } catch (err) {
      console.error('Failed to fetch problems:', err);
    }
  };

  const fetchSubmissions = async () => {
    try {
      const res = await fetch(`${API_URL}/api/v1/submissions/user/${user.id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setSubmissions(data);
    } catch (err) {
      console.error('Failed to fetch submissions:', err);
    }
  };

  const handleSelectProblem = (problem) => {
    setSelectedProblem(problem);
    setCurrentView('editor');
    setCode(getStarterCode(language));
  };

  const getStarterCode = (lang) => {
    const starters = {
      python: '# Write your solution here\ndef solution():\n    pass\n',
      javascript: '// Write your solution here\nfunction solution() {\n    \n}\n',
      java: '// Write your solution here\npublic class Solution {\n    public void solution() {\n        \n    }\n}\n',
      cpp: '// Write your solution here\n#include <iostream>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}\n'
    };
    return starters[lang] || '';
  };

  const handleSubmit = async () => {
    if (!selectedProblem || !code.trim()) return;

    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/v1/submissions/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          problem_id: selectedProblem.id,
          user_id: user.id,
          code: code,
          language: language
        })
      });

      if (res.ok) {
        const submission = await res.json();
        alert(`Submission created! Status: ${submission.status}`);
        setCurrentView('submissions');
        fetchSubmissions();
      } else {
        alert('Submission failed');
      }
    } catch (err) {
      alert('Error submitting code');
    } finally {
      setLoading(false);
    }
  };

  const renderProblemsView = () => (
    <div className="terminal-content">
      <div className="terminal-line">
        <span className="prompt">root@codearena:~$</span> ls -la /problems
      </div>
      <div className="terminal-line">total {problems.length} problems found</div>
      <div className="terminal-line separator">{'─'.repeat(80)}</div>

      {problems.map((problem, idx) => (
        <div
          key={problem.id}
          className="problem-item"
          onClick={() => handleSelectProblem(problem)}
        >
          <span className="problem-number">[{idx + 1}]</span>
          <span className={`difficulty ${problem.difficulty.toLowerCase()}`}>
            {problem.difficulty}
          </span>
          <span className="problem-title">{problem.title}</span>
          <span className="problem-category">({problem.category})</span>
        </div>
      ))}

      <div className="terminal-line separator">{'─'.repeat(80)}</div>
      <div className="terminal-line hint">> Click on a problem to start coding</div>
    </div>
  );

  const renderEditorView = () => (
    <div className="terminal-content">
      <div className="terminal-line">
        <span className="prompt">root@codearena:~$</span> vim /problems/{selectedProblem?.slug}
      </div>
      
      <div className="problem-details">
        <h2 className="problem-title">{selectedProblem?.title}</h2>
        <div className="problem-meta">
          <span className={`difficulty ${selectedProblem?.difficulty.toLowerCase()}`}>
            {selectedProblem?.difficulty}
          </span>
          <span className="category">{selectedProblem?.category}</span>
        </div>
        
        <div className="problem-description">
          {selectedProblem?.description}
        </div>

        {selectedProblem?.examples && selectedProblem.examples.length > 0 && (
          <div className="examples">
            <div className="section-title">> TEST CASES:</div>
            {selectedProblem.examples.map((ex, idx) => (
              <div key={idx} className="example">
                <div className="example-title">Example {idx + 1}:</div>
                <div className="example-io">
                  <div>Input: {ex.input}</div>
                  <div>Output: {ex.output}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="editor-section">
        <div className="editor-header">
          <select
            value={language}
            onChange={(e) => {
              setLanguage(e.target.value);
              setCode(getStarterCode(e.target.value));
            }}
            className="language-select"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="java">Java</option>
            <option value="cpp">C++</option>
          </select>
          <span className="editor-title">> CODE EDITOR</span>
        </div>
        
        <textarea
          className="code-editor"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="// Write your solution here..."
          spellCheck={false}
        />

        <div className="editor-actions">
          <button onClick={handleSubmit} disabled={loading} className="action-btn submit">
            {loading ? '> SUBMITTING...' : '> SUBMIT CODE'}
          </button>
          <button onClick={() => setCurrentView('problems')} className="action-btn">
            > BACK TO PROBLEMS
          </button>
        </div>
      </div>
    </div>
  );

  const renderSubmissionsView = () => (
    <div className="terminal-content">
      <div className="terminal-line">
        <span className="prompt">root@codearena:~$</span> cat /submissions/user_{user.id}.log
      </div>
      <div className="terminal-line separator">{'─'.repeat(80)}</div>

      {submissions.length === 0 ? (
        <div className="terminal-line">No submissions yet</div>
      ) : (
        submissions.map((sub) => (
          <div key={sub.id} className="submission-item">
            <span className="submission-id">[{sub.id}]</span>
            <span className={`status ${sub.status.toLowerCase().replace('_', '-')}`}>
              {sub.status}
            </span>
            <span className="submission-time">
              {sub.test_cases_passed || 0}/{sub.test_cases_total || 0} tests
            </span>
            {sub.execution_time_ms && (
              <span className="submission-time">{sub.execution_time_ms}ms</span>
            )}
          </div>
        ))
      )}

      <div className="terminal-line separator">{'─'.repeat(80)}</div>
    </div>
  );

  return (
    <div className="terminal-container">
      <div className="terminal-header">
        <span className="terminal-title">CodeArena Terminal - {user.username}@localhost</span>
        <button onClick={onLogout} className="logout-btn">LOGOUT</button>
      </div>

      <div className="terminal-nav">
        <button
          className={currentView === 'problems' ? 'active' : ''}
          onClick={() => setCurrentView('problems')}
        >
          > PROBLEMS
        </button>
        <button
          className={currentView === 'submissions' ? 'active' : ''}
          onClick={() => {
            setCurrentView('submissions');
            fetchSubmissions();
          }}
        >
          > SUBMISSIONS
        </button>
      </div>

      <div className="terminal-body">
        {currentView === 'problems' && renderProblemsView()}
        {currentView === 'editor' && renderEditorView()}
        {currentView === 'submissions' && renderSubmissionsView()}
      </div>
    </div>
  );
}

export default Terminal;
