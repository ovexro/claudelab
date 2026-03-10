import { useState, useEffect, useRef } from 'react'
import './Installation.css'

function TerminalBlock({ title, children }) {
  return (
    <div className="term-block">
      <div className="term-block-chrome">
        <div className="term-block-dots">
          <span className="dot dot--red"></span>
          <span className="dot dot--yellow"></span>
          <span className="dot dot--green"></span>
        </div>
        <span className="term-block-title">{title}</span>
      </div>
      <div className="term-block-body">
        {children}
      </div>
    </div>
  );
}

function TypedLine({ prompt = '$', text, delay = 0, outputLines = [] }) {
  const [displayedText, setDisplayedText] = useState('');
  const [showOutput, setShowOutput] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setIsVisible(true);
      },
      { threshold: 0.5 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!isVisible) return;
    let idx = 0;
    const startTimeout = setTimeout(() => {
      const timer = setInterval(() => {
        idx++;
        setDisplayedText(text.slice(0, idx));
        if (idx >= text.length) {
          clearInterval(timer);
          setTimeout(() => setShowOutput(true), 300);
        }
      }, 40);
      return () => clearInterval(timer);
    }, delay);
    return () => clearTimeout(startTimeout);
  }, [isVisible, text, delay]);

  return (
    <div ref={ref}>
      <div className="term-line">
        <span className="term-prompt">{prompt}</span>
        <span className="term-command">{displayedText}</span>
        {displayedText.length < text.length && <span className="cursor-blink">█</span>}
      </div>
      {showOutput && outputLines.map((line, i) => (
        <div key={i} className={`term-output ${line.type || ''}`}>
          {line.text}
        </div>
      ))}
    </div>
  );
}

function Installation() {
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
    <section className="section" id="install" ref={sectionRef}>
      <div className="section-header">
        <span className="section-label">// install</span>
        <h2 className="section-title">Get Up and Running in 60 Seconds</h2>
        <p className="section-subtitle">
          Zero dependencies. Two commands. No manual config.
        </p>
      </div>

      <div className={`install-grid ${isVisible ? 'install-grid--visible' : ''}`}>
        {/* Step 1: Install & Setup */}
        <div className="install-step">
          <div className="step-number">01</div>
          <h3 className="step-title">Install & Auto-Configure</h3>
          <TerminalBlock title="terminal">
            <TypedLine
              text="pip install claudelab"
              outputLines={[
                { text: 'Collecting claudelab', type: 'term-output--dim' },
                { text: '  Downloading claudelab-0.1.5-py3-none-any.whl', type: 'term-output--dim' },
                { text: 'Successfully installed claudelab-0.1.5', type: 'term-output--success' },
              ]}
            />
            <div className="term-spacer"></div>
            <TypedLine
              text="claudelab install"
              delay={1200}
              outputLines={[
                { text: '[1/4] Found hook script: ~/.local/.../claudelab-hook.sh', type: 'term-output--dim' },
                { text: '[2/4] Hook script already executable', type: 'term-output--dim' },
                { text: '[3/4] Added hooks to ~/.claude/settings.json', type: 'term-output--dim' },
                { text: '[4/4] State file OK', type: 'term-output--dim' },
                { text: '', type: '' },
                { text: 'ClaudeLab installed successfully!', type: 'term-output--success' },
              ]}
            />
          </TerminalBlock>
          <p className="step-note">
            <span className="note-label">That{"'"}s it.</span> The install command auto-detects the hook script,
            configures Claude Code hooks, and verifies everything works. No manual JSON editing needed.
          </p>
        </div>

        {/* Step 2: Run */}
        <div className="install-step">
          <div className="step-number">02</div>
          <h3 className="step-title">Run in a Side Pane</h3>
          <TerminalBlock title="terminal — tmux setup">
            <div className="term-line">
              <span className="term-comment"># Start a tmux session and split (Ctrl+b then %)</span>
            </div>
            <TypedLine text="tmux new-session -s claude" delay={200} />
            <div className="term-spacer"></div>
            <div className="term-line">
              <span className="term-comment"># In the side pane, run ClaudeLab:</span>
            </div>
            <TypedLine text="claudelab" delay={600} outputLines={[
              { text: '═══════════ AI ENGINEERING LAB ═══════════', type: 'term-output--amber' },
              { text: 'Isometric 2.5D office — watching for activity...', type: 'term-output--dim' },
            ]} />
            <div className="term-spacer"></div>
            <div className="term-line">
              <span className="term-comment"># Use Claude Code in the other pane — ClaudeLab reacts live!</span>
            </div>
          </TerminalBlock>
        </div>

        {/* Bonus: Troubleshooting */}
        <div className="install-step">
          <div className="step-number">++</div>
          <h3 className="step-title">Built-in Diagnostics</h3>
          <TerminalBlock title="terminal">
            <TypedLine
              text="claudelab doctor"
              outputLines={[
                { text: '[ OK ] Hook script: ~/.local/.../claudelab-hook.sh', type: 'term-output--success' },
                { text: '[ OK ] Hooks configured in Claude Code settings', type: 'term-output--success' },
                { text: '[ OK ] State file: /tmp/claudelab.state (value=\'coding\', 2s ago)', type: 'term-output--success' },
                { text: '[ OK ] Python 3.12.3', type: 'term-output--success' },
                { text: '', type: '' },
                { text: 'All checks passed! ClaudeLab is ready.', type: 'term-output--success' },
              ]}
            />
          </TerminalBlock>
          <p className="step-note">
            <span className="note-label">Something wrong?</span> Run <code>claudelab doctor</code> to
            diagnose hook config, permissions, state file freshness, and more. It tells you exactly what to fix.
          </p>
        </div>
      </div>
    </section>
  );
}

export default Installation;
