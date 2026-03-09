import { useState, useEffect, useRef } from 'react'
import { SCENES } from '../assets/ascii-frames'
import './Demo.css'

const SCENE_KEYS = ['thinking', 'coding', 'debugging', 'running', 'building', 'idle'];
const SCENE_COLORS = {
  thinking: '#cc66ff',
  coding: '#00ff41',
  debugging: '#ff3333',
  running: '#00ccff',
  building: '#ffb000',
  idle: '#888888',
};

function Demo() {
  const [activeScene, setActiveScene] = useState('coding');
  const [frames, setFrames] = useState([]);
  const [frameIdx, setFrameIdx] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setIsVisible(true);
      },
      { threshold: 0.1 }
    );
    if (sectionRef.current) observer.observe(sectionRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const scene = SCENES[activeScene];
    if (scene) {
      const f = scene.generateFrames(60, 18, 8);
      setFrames(f);
      setFrameIdx(0);
    }
  }, [activeScene]);

  useEffect(() => {
    if (frames.length === 0) return;
    const timer = setInterval(() => {
      setFrameIdx(prev => (prev + 1) % frames.length);
    }, 350);
    return () => clearInterval(timer);
  }, [frames]);

  const currentFrame = frames[frameIdx] || [];
  const color = SCENE_COLORS[activeScene];

  return (
    <section className="section" id="demo" ref={sectionRef}>
      <div className="section-header">
        <span className="section-label">// demo</span>
        <h2 className="section-title">Try It Live</h2>
        <p className="section-subtitle">
          Click a scene to see it animate. In the real tool, run <code className="inline-code">claudelab --demo</code> to
          cycle through all scenes.
        </p>
      </div>

      <div className={`demo-container ${isVisible ? 'demo-container--visible' : ''}`}>
        {/* Scene Selector */}
        <div className="demo-selector">
          {SCENE_KEYS.map(key => {
            const scene = SCENES[key];
            const isActive = activeScene === key;
            const sceneColor = SCENE_COLORS[key];
            return (
              <button
                key={key}
                className={`demo-scene-btn ${isActive ? 'demo-scene-btn--active' : ''}`}
                style={isActive ? { borderColor: sceneColor, color: sceneColor, boxShadow: `0 0 15px ${sceneColor}20` } : {}}
                onClick={() => setActiveScene(key)}
              >
                <span className="demo-scene-icon">{scene.icon}</span>
                <span className="demo-scene-name">{scene.name}</span>
              </button>
            );
          })}
        </div>

        {/* Demo Terminal */}
        <div className="demo-terminal">
          <div className="demo-terminal-chrome">
            <div className="term-block-dots">
              <span className="dot dot--red"></span>
              <span className="dot dot--yellow"></span>
              <span className="dot dot--green"></span>
            </div>
            <span className="demo-terminal-title">claudelab --demo</span>
            <span className="demo-terminal-badge" style={{ color, borderColor: color + '40' }}>
              {SCENES[activeScene]?.name}
            </span>
          </div>
          <div className="demo-terminal-titlebar" style={{ color: '#ffb000' }}>
            {'═'.repeat(18)} AI ENGINEERING LAB {'═'.repeat(18)}
          </div>
          <pre className="demo-terminal-body">
            {currentFrame.join('\n')}
          </pre>
          <div className="demo-terminal-status">
            <span>
              Activity: <span style={{ color }}>{SCENES[activeScene]?.name.toUpperCase()}</span>
            </span>
            <span>8 FPS</span>
            <span>ClaudeLab v0.1.0</span>
          </div>
        </div>

        {/* Command hint */}
        <div className="demo-command">
          <span className="demo-command-prompt">$</span>
          <span className="demo-command-text">claudelab --demo</span>
          <span className="demo-command-hint">  # run this to see all scenes cycle in your terminal</span>
        </div>
      </div>
    </section>
  );
}

export default Demo;
