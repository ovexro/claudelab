import { useState, useEffect, useRef } from 'react'
import { SCENES } from '../assets/voxel-frames'
import './Features.css'

const SCENE_KEYS = ['thinking', 'coding', 'debugging', 'running', 'building', 'idle'];
const SCENE_COLORS = {
  thinking: '#cc66ff',
  coding: '#00ff41',
  debugging: '#ff3333',
  running: '#00ccff',
  building: '#ffb000',
  idle: '#888888',
};

function FeatureCard({ sceneKey, index }) {
  const [preview, setPreview] = useState([]);
  const [frameIdx, setFrameIdx] = useState(0);
  const [allFrames, setAllFrames] = useState([]);
  const [isVisible, setIsVisible] = useState(false);
  const cardRef = useRef(null);
  const scene = SCENES[sceneKey];
  const color = SCENE_COLORS[sceneKey];

  useEffect(() => {
    const frames = scene.generateFrames(38, 12, 4);
    setAllFrames(frames);
    if (frames.length > 0) setPreview(frames[0]);
  }, [sceneKey]);

  useEffect(() => {
    if (allFrames.length === 0) return;
    const timer = setInterval(() => {
      setFrameIdx(prev => {
        const next = (prev + 1) % allFrames.length;
        setPreview(allFrames[next]);
        return next;
      });
    }, 500);
    return () => clearInterval(timer);
  }, [allFrames]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setTimeout(() => setIsVisible(true), index * 100);
        }
      },
      { threshold: 0.1 }
    );
    if (cardRef.current) observer.observe(cardRef.current);
    return () => observer.disconnect();
  }, [index]);

  return (
    <div
      ref={cardRef}
      className={`feature-card ${isVisible ? 'feature-card--visible' : ''}`}
      style={{ '--accent': color }}
    >
      <div className="feature-card-header">
        <span className="feature-icon" style={{ color }}>{scene.icon}</span>
        <h3 className="feature-name" style={{ color }}>{scene.name}</h3>
      </div>
      <div className="feature-preview">
        <pre className="feature-ascii" dangerouslySetInnerHTML={{ __html: preview.join('\n') }} />
      </div>
      <p className="feature-description">{scene.description}</p>
      <p className="feature-trigger">
        <span className="trigger-label">Trigger:</span> {scene.trigger}
      </p>
    </div>
  );
}

function Features() {
  return (
    <section className="section" id="features">
      <div className="section-header">
        <span className="section-label">// scenes</span>
        <h2 className="section-title">Six Animated Office Scenes</h2>
        <p className="section-subtitle">
          Each scene activates automatically based on what Claude Code is doing.
          Watch your AI engineers think, code, debug, and build in real time.
        </p>
      </div>

      <div className="features-grid">
        {SCENE_KEYS.map((key, i) => (
          <FeatureCard key={key} sceneKey={key} index={i} />
        ))}
      </div>
    </section>
  );
}

export default Features;
