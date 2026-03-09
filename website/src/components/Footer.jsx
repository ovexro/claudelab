import './Footer.css'

const FOOTER_ASCII = [
  '       ◉      ◉  ',
  '      /|\\    /|\\ ',
  '      / \\    / \\ ',
  '   ┌────────────────┐',
  '   │  Happy Coding! │',
  '   └────────────────┘',
];

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <pre className="footer-ascii">
          {FOOTER_ASCII.join('\n')}
        </pre>

        <div className="footer-links">
          <a
            href="https://github.com/ovexro/claudelab"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            GitHub
          </a>
          <span className="footer-sep">|</span>
          <a
            href="https://pypi.org/project/claudelab/"
            target="_blank"
            rel="noopener noreferrer"
            className="footer-link"
          >
            PyPI
          </a>
          <span className="footer-sep">|</span>
          <span className="footer-license">MIT License</span>
        </div>

        <p className="footer-tagline">
          Made for Claude Code users
        </p>

        <div className="footer-border">
          {'═'.repeat(60)}
        </div>

        <p className="footer-copy">
          <span className="footer-bracket">[</span>
          ClaudeLab
          <span className="footer-bracket">]</span>
          {' '}&mdash; Watch your AI engineers work
        </p>
      </div>
    </footer>
  );
}

export default Footer;
