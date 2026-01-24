import React from 'react';
import Header from './Header';
import './Layout.css';

const Layout = ({ 
  children,
  year = '2025',
  headerNavLinks = null
}) => {
  return (
    <div className="aoc-layout">
      <Header year={year} navLinks={headerNavLinks} />
      <main>
        {children}
      </main>
    </div>
  );
};

export default Layout;
