import { useState } from 'react'
import './App.css'
import Hero from './components/Hero'
import Features from './components/Features'
import Installation from './components/Installation'
import HowItWorks from './components/HowItWorks'
import Demo from './components/Demo'
import Footer from './components/Footer'

function App() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="app">
      {/* Navigation */}
      <nav className="nav">
        <div className="nav-inner">
          <a href="#" className="nav-logo">
            <span className="bracket">[</span>
            ClaudeLab
            <span className="bracket">]</span>
          </a>
          <button
            className={`nav-hamburger ${menuOpen ? 'nav-hamburger--open' : ''}`}
            onClick={() => setMenuOpen(prev => !prev)}
            aria-label="Toggle navigation menu"
            aria-expanded={menuOpen}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
          <ul className={`nav-links ${menuOpen ? 'nav-links--open' : ''}`}>
            <li><a href="#features" onClick={() => setMenuOpen(false)}>Features</a></li>
            <li><a href="#install" onClick={() => setMenuOpen(false)}>Install</a></li>
            <li><a href="#how-it-works" onClick={() => setMenuOpen(false)}>How It Works</a></li>
            <li><a href="#demo" onClick={() => setMenuOpen(false)}>Demo</a></li>
          </ul>
          <a
            href="https://github.com/ovexro/claudelab"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-github"
          >
            GitHub
          </a>
        </div>
      </nav>

      {/* Main Content */}
      <Hero />
      <hr className="section-divider" />
      <Features />
      <hr className="section-divider" />
      <Installation />
      <hr className="section-divider" />
      <HowItWorks />
      <hr className="section-divider" />
      <Demo />
      <Footer />
    </div>
  )
}

export default App
