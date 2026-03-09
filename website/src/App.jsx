import './App.css'
import Hero from './components/Hero'
import Features from './components/Features'
import Installation from './components/Installation'
import HowItWorks from './components/HowItWorks'
import Demo from './components/Demo'
import Footer from './components/Footer'

function App() {
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
          <ul className="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#install">Install</a></li>
            <li><a href="#how-it-works">How It Works</a></li>
            <li><a href="#demo">Demo</a></li>
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
