import React from 'react';
import { Layout, PuzzleArticle, CodeBlock } from '../components';

/**
 * Example showing how to customize the components
 */
const CustomExample = () => {
  // Custom sponsor data
  const customSponsor = {
    name: 'Your Company',
    url: 'https://yourcompany.com',
    description: 'Building awesome stuff with React! Check out our open positions.'
  };

  // Custom nav links
  const customNavLinks = {
    global: [
      { href: '/home', label: 'Home' },
      { href: '/about', label: 'About' },
      { href: '/blog', label: 'Blog' },
      { href: '/contact', label: 'Contact' }
    ],
    event: [
      { href: '/challenges', label: 'Challenges' },
      { href: '/leaderboard', label: 'Leaderboard' },
      { href: '/docs', label: 'Docs' }
    ]
  };

  return (
    <Layout 
      year="2026" 
      sponsor={customSponsor}
      headerNavLinks={customNavLinks}
    >
      <PuzzleArticle day={1} title="Your Custom Challenge" completed={false}>
        <p>This is your custom content! You can modify everything:</p>
        
        <ul>
          <li>Change colors in the CSS files</li>
          <li>Add new components</li>
          <li>Customize the layout</li>
          <li>Add interactivity</li>
        </ul>

        <p>Here's an example code block:</p>

        <CodeBlock language="javascript">
{`function solve() {
  // Your solution here
  return 42;
}`}
        </CodeBlock>

        <p>
          You can use <em>emphasis</em>, <code>code snippets</code>, and{' '}
          <a href="#">links</a> just like the original.
        </p>

        <p>
          Want a <em className="star">star</em>? Just add the star class!
        </p>
      </PuzzleArticle>
    </Layout>
  );
};

export default CustomExample;
