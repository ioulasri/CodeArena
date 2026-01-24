import React from 'react';
import './AuthPrompt.css';

const AuthPrompt = ({ 
  providers = [
    { name: 'GitHub', url: '/auth/github' },
    { name: 'Google', url: '/auth/google' },
    { name: 'Twitter', url: '/auth/twitter' },
    { name: 'Reddit', url: '/auth/reddit' }
  ],
  promptText = 'To play, please identify yourself via one of these services:'
}) => {
  return (
    <div className="auth-prompt">
      <p>{promptText}</p>
      <p>
        {providers.map((provider, index) => (
          <React.Fragment key={provider.name}>
            <a href={provider.url}>[{provider.name}]</a>
            {index < providers.length - 1 && ' '}
          </React.Fragment>
        ))}
        {' '}
        <span className="quiet">
          - <a href="/about#faq_auth">[How Does Auth Work?]</a>
        </span>
      </p>
    </div>
  );
};

export default AuthPrompt;
