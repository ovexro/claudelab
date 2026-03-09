import { useState, useEffect, useRef } from 'react'
import './HowItWorks.css'

const STEPS = [
  {
    number: '01',
    title: 'Claude Code Runs',
    ascii: [
      '┌──────────────────┐',
      '│  $ claude         │',
      '│                    │',
      '│  > Reading files...│',
      '│  > Planning...     │',
      '│  > Writing code... │',
      '│                    │',
      '└──────────────────┘',
    ],
    description: 'Claude Code executes tasks like reading files, writing code, running commands. Hooks emit events on each tool use.',
    color: '#00ccff',
  },
  {
    number: '02',
    title: 'ClaudeLab Detects Activity',
    ascii: [
      '  ┌─────────────┐  ',
      '  │ hook signal  │  ',
      '  └──────┬──────┘  ',
      '         │         ',
      '         ▼         ',
      '  ┌─────────────┐  ',
      '  │  claudelab   │  ',
      '  │  detector    │  ',
      '  └─────────────┘  ',
    ],
    description: 'The hook command writes to a shared state file. ClaudeLab watches for changes and maps tool names to scene types.',
    color: '#ffb000',
  },
  {
    number: '03',
    title: 'ASCII Office Updates',
    ascii: [
      '┌──────────────────┐',
      '│ ═══ AI LAB ═══   │',
      '│                    │',
      '│   ◉   .o( ! )     │',
      '│  /|\\              │',
      '│  / \\  ┌────────┐ │',
      '│       │▓▓░░▓▓░░│ │',
      '│       └────────┘ │',
      '└──────────────────┘',
    ],
    description: 'The terminal scene animates in real time. ASCII engineers think, code, debug, or build depending on the current activity.',
    color: '#00ff41',
  },
];

function HowItWorks() {
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

  return (
    <section className="section" id="how-it-works" ref={sectionRef}>
      <div className="section-header">
        <span className="section-label">// architecture</span>
        <h2 className="section-title">How It Works</h2>
        <p className="section-subtitle">
          Three simple steps. No configuration hell.
        </p>
      </div>

      <div className={`how-steps ${isVisible ? 'how-steps--visible' : ''}`}>
        {STEPS.map((step, i) => (
          <div key={i} className="how-step" style={{ '--step-color': step.color, transitionDelay: `${i * 150}ms` }}>
            <div className="how-step-number" style={{ color: step.color }}>
              {step.number}
            </div>
            <h3 className="how-step-title">{step.title}</h3>
            <div className="how-step-ascii-box">
              <pre className="how-step-ascii" style={{ color: step.color }}>
                {step.ascii.join('\n')}
              </pre>
            </div>
            <p className="how-step-desc">{step.description}</p>
            {i < STEPS.length - 1 && (
              <div className="how-step-arrow">
                <span className="arrow-line">│</span>
                <span className="arrow-line">│</span>
                <span className="arrow-head">▼</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Flow diagram */}
      <div className={`how-flow ${isVisible ? 'how-flow--visible' : ''}`}>
        <pre className="how-flow-ascii">{`
  ┌──────────────┐     hook      ┌──────────────┐     render    ┌──────────────┐
  │              │  ──────────>  │              │  ──────────>  │              │
  │  Claude Code │   pre/post    │   ClaudeLab  │    curses     │   Terminal   │
  │              │   tool_use    │   Detector   │    frames     │   Display    │
  │              │  <──────────  │              │  <──────────  │              │
  └──────────────┘   state file  └──────────────┘     8 FPS     └──────────────┘
        `}</pre>
      </div>
    </section>
  );
}

export default HowItWorks;
