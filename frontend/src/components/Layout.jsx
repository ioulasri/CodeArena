import React from 'react';
import Header from './Header';
import './Layout.css';

const Layout = ({ 
  children,
  year = '2025',
  navLinks = null
}) => {
  return (
    <div className="aoc-layout">
      <Header year={year} navLinks={navLinks} />
      <main>
        {children}
      </main>
    </div>
  );
};

export default Layout;
