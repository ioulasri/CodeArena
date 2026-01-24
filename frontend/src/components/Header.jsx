import React from 'react';
import './Header.css';

const Header = ({ 
  year = '2026',
  navLinks
}) => {
  // If no navLinks provided, show minimal header
  if (!navLinks) {
    return (
      <header>
        <div>
          <h1 className="title-global">
            <a href="/">CodeArena</a>
          </h1>
        </div>
        <div>
          <h1 className="title-event">
            <span className="title-event-wrap">/^</span>
            <a href={`/`}>{year}</a>
            <span className="title-event-wrap">$/</span>
          </h1>
        </div>
      </header>
    );
  }
  
  const handleLinkClick = (e, link) => {
    if (link.onClick) {
      e.preventDefault();
      link.onClick();
    }
  };
  
  return (
    <header>
      <div>
        <h1 className="title-global">
          <a href="/">CodeArena</a>
        </h1>
        <nav>
          <ul>
            {navLinks.global.map((link, index) => (
              <li key={index}>
                <a 
                  href={link.href} 
                  onClick={(e) => handleLinkClick(e, link)}
                >
                  [{link.label}]
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
      <div>
        <h1 className="title-event">
          <span className="title-event-wrap">/^</span>
          <a href={`/`}>{year}</a>
          <span className="title-event-wrap">$/</span>
        </h1>
        <nav>
          <ul>
            {navLinks.event.map((link, index) => (
              <li key={index}>
                <a 
                  href={link.href || '#'} 
                  onClick={(e) => handleLinkClick(e, link)}
                >
                  [{link.label}]
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
