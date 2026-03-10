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
          Zero dependencies. Just pip install and go.
        </p>
      </div>

      <div className={`install-grid ${isVisible ? 'install-grid--visible' : ''}`}>
        {/* Step 1: Install */}
        <div className="install-step">
          <div className="step-number">01</div>
          <h3 className="step-title">Install ClaudeLab</h3>
          <TerminalBlock title="terminal">
            <TypedLine
              text="pip install claudelab"
              outputLines={[
                { text: 'Collecting claudelab', type: 'term-output--dim' },
                { text: '  Downloading claudelab-0.1.0-py3-none-any.whl', type: 'term-output--dim' },
                { text: 'Installing collected packages: claudelab', type: 'term-output--dim' },
                { text: 'Successfully installed claudelab-0.1.0', type: 'term-output--success' },
              ]}
            />
          </TerminalBlock>
        </div>

        {/* Step 2: tmux Setup */}
        <div className="install-step">
          <div className="step-number">02</div>
          <h3 className="step-title">Split Your Terminal with tmux</h3>
          <TerminalBlock title="terminal — tmux setup">
            <div className="term-line">
              <span className="term-comment"># Start a new tmux session</span>
            </div>
            <TypedLine text="tmux new-session -s claude" delay={200} />
            <div className="term-spacer"></div>
            <div className="term-line">
              <span className="term-comment"># Split the pane (Ctrl+b then %)</span>
            </div>
            <div className="term-spacer"></div>
            <div className="term-line">
              <span className="term-comment"># In the right pane, run ClaudeLab:</span>
            </div>
            <TypedLine text="claudelab" delay={600} outputLines={[
              { text: '═══════════ AI ENGINEERING LAB ═══════════', type: 'term-output--amber' },
              { text: 'Watching for Claude Code activity...', type: 'term-output--dim' },
            ]} />
          </TerminalBlock>
        </div>

        {/* Step 3: Hooks */}
        <div className="install-step">
          <div className="step-number">03</div>
          <h3 className="step-title">Configure Claude Code Hooks</h3>
          <TerminalBlock title="~/.claude/hooks.json">
            <pre className="term-json">{`{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "/path/to/claudelab-hook.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "/path/to/claudelab-hook.sh"
      }]
    }],
    "PostToolUseFailure": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "/path/to/claudelab-hook.sh"
      }]
    }]
  }
}`}</pre>
          </TerminalBlock>
          <p className="step-note">
            <span className="note-label">Note:</span> Hooks let Claude Code notify
            ClaudeLab what it is doing, so the right scene plays automatically.
          </p>
        </div>
      </div>
    </section>
  );
}

export default Installation;
