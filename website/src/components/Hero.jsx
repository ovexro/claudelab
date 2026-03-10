import { useState, useEffect, useRef } from 'react'
import { LOGO, getHeroFrames } from '../assets/voxel-frames'
import './Hero.css'

const SCENE_NAMES = ['THINKING', 'CODING', 'DEBUGGING', 'RUNNING', 'BUILDING', 'IDLE'];
const SCENE_COLORS = {
  thinking: '#cc66ff',
  coding: '#00ff41',
  debugging: '#ff3333',
  running: '#00ccff',
  building: '#ffb000',
  idle: '#888888',
};

function Hero() {
  const [frameIndex, setFrameIndex] = useState(0);
  const [frames, setFrames] = useState([]);
  const [isVisible, setIsVisible] = useState(false);
  const terminalRef = useRef(null);

  useEffect(() => {
    const heroFrames = getHeroFrames(68, 18);
    setFrames(heroFrames);
    setIsVisible(true);
  }, []);

  useEffect(() => {
    if (frames.length === 0) return;
    const timer = setInterval(() => {
      setFrameIndex(prev => (prev + 1) % frames.length);
    }, 400);
    return () => clearInterval(timer);
  }, [frames]);

  const currentFrame = frames[frameIndex];
  const currentScene = currentFrame?.scene || 'thinking';
  const currentLabel = currentFrame?.label || 'Thinking';
  const sceneColor = SCENE_COLORS[currentScene];

  return (
    <section className={`hero ${isVisible ? 'hero--visible' : ''}`}>
      {/* ASCII Logo */}
      <div className="hero-logo">
        <pre className="hero-logo-ascii" dangerouslySetInnerHTML={{ __html: LOGO.join('\n') }} />
      </div>

      {/* Tagline */}
      <h1 className="hero-tagline">
        Watch your AI engineers work<span className="cursor-blink">_</span>
      </h1>
      <p className="hero-subtitle">
        A visual terminal companion for Claude Code
      </p>

      {/* Animated Terminal */}
      <div className="hero-terminal" ref={terminalRef}>
        <div className="terminal-chrome">
          <div className="terminal-dots">
            <span className="dot dot--red"></span>
            <span className="dot dot--yellow"></span>
            <span className="dot dot--green"></span>
          </div>
          <div className="terminal-title">
            claudelab --demo
          </div>
          <div className="terminal-scene-badge" style={{ color: sceneColor, borderColor: sceneColor + '40' }}>
            {currentLabel}
          </div>
        </div>
        <div className="terminal-titlebar">
          <span className="terminal-titlebar-text">
            {'═'.repeat(20)} AI ENGINEERING LAB {'═'.repeat(20)}
          </span>
        </div>
        <pre className="terminal-body" dangerouslySetInnerHTML={{ __html: currentFrame?.lines?.join('\n') || '' }} />
        <div className="terminal-statusbar">
          <span>Activity: <span style={{ color: sceneColor }}>{currentLabel.toUpperCase()}</span></span>
          <span>ClaudeLab v0.1.0</span>
        </div>
      </div>

      {/* CTA Buttons */}
      <div className="hero-actions">
        <a href="#install" className="btn btn--primary">
          <span className="btn-icon">$</span> Get Started
        </a>
        <a
          href="https://github.com/ovexro/claudelab"
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn--secondary"
        >
          <span className="btn-icon">&gt;</span> View on GitHub
        </a>
      </div>

      {/* Scene indicator dots */}
      <div className="hero-scenes">
        {SCENE_NAMES.map((name, i) => {
          const sceneKey = name.toLowerCase();
          const isActive = currentScene === sceneKey;
          return (
            <span
              key={name}
              className={`scene-dot ${isActive ? 'scene-dot--active' : ''}`}
              style={isActive ? { color: SCENE_COLORS[sceneKey], borderColor: SCENE_COLORS[sceneKey] + '60' } : {}}
            >
              {name}
            </span>
          );
        })}
      </div>
    </section>
  );
}

export default Hero;
