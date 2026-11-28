import {
  Activity,
  ArrowRight,
  Bot,
  BrainCircuit,
  CheckCircle2,
  Clock3,
  GitBranch,
  Network,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  Timer,
  Users,
  Workflow,
  Zap,
} from 'lucide-react'

const agents = [
  { name: 'Planning Agent', role: 'Task decomposition', state: 'Planning', icon: BrainCircuit },
  { name: 'Research Agent', role: 'Context gathering', state: 'Working', icon: Sparkles },
  { name: 'Data Agent', role: 'Data analysis', state: 'Working', icon: Activity },
  { name: 'Workflow Agent', role: 'Process execution', state: 'Queued', icon: Workflow },
  { name: 'Validation Agent', role: 'Quality checks', state: 'Ready', icon: ShieldCheck },
  { name: 'Recovery Agent', role: 'Retry and recovery', state: 'Ready', icon: RotateCcw },
]

const capabilities = [
  { title: 'Multi-Agent Collaboration', detail: 'Coordinate specialized agents on shared tasks.', icon: Users },
  { title: 'Task Decomposition', detail: 'Break complex goals into trackable steps.', icon: GitBranch },
  { title: 'Agent-to-Agent Communication', detail: 'Pass context and results between agents.', icon: Network },
  { title: 'Dynamic Agent Selection', detail: 'Match each task to the most suitable agent.', icon: BrainCircuit },
  { title: 'Parallel Task Execution', detail: 'Run independent tasks concurrently.', icon: Zap },
  { title: 'Failure Recovery & Retry', detail: 'Recover from errors with controlled retries.', icon: RotateCcw },
  { title: 'Workflow Scheduling', detail: 'Schedule orchestration across workflows.', icon: Clock3 },
]

export default function AdvancedAIOrchestrator({ onNavigate }: { onNavigate: (label: string) => void }) {
  return (
    <div className="orchestrator-page">
      <header className="orchestrator-header">
        <div>
          <span className="orchestrator-eyebrow"><Sparkles size={13} /> AGENT CONTROL PLANE</span>
          <h1>Advanced AI Orchestrator</h1>
          <p>Coordinate AI agents, tasks, and workflows from one central workspace.</p>
        </div>
        <div className="orchestrator-header-actions">
          <span className="orchestrator-status"><i /> Orchestration Online</span>
          <button className="orchestrator-open-workflows" onClick={() => onNavigate('Workflow Studio')}>
            Open Workflow Studio <ArrowRight size={14} />
          </button>
        </div>
      </header>

      <div className="orchestrator-metrics" aria-label="Simulated orchestration metrics">
        <article><span><Bot size={14} /> Active Agents</span><strong>08 <small>/ 10</small></strong><em>Across 4 workflows</em></article>
        <article><span><Activity size={14} /> Tasks In Queue</span><strong>24</strong><em>6 running in parallel</em></article>
        <article><span><Zap size={14} /> Task Throughput</span><strong>186 <small>/ hr</small></strong><em className="orchestrator-positive">+12.8% this week</em></article>
        <article><span><CheckCircle2 size={14} /> Successful Runs</span><strong>99.2<small>%</small></strong><em>Last 30 days</em></article>
      </div>

      <div className="orchestrator-workspace">
        <section className="orchestrator-panel orchestrator-network-panel">
          <div className="orchestrator-panel-heading">
            <div><h2>Multi-Agent Collaboration</h2><p>Live task routing across specialized agents</p></div>
            <span className="orchestrator-live"><i /> SIMULATED LIVE VIEW</span>
          </div>
          <div className="orchestrator-flow">
            <div className="orchestrator-hub">
              <span><Network size={18} /></span>
              <div><strong>AI Orchestrator</strong><small>Routing • Scheduling • Coordination</small></div>
              <b>ACTIVE</b>
            </div>
            <div className="orchestrator-agent-grid">
              {agents.map(({ name, role, state, icon: Icon }) => (
                <article className={`orchestrator-agent ${state === 'Working' || state === 'Planning' ? 'working' : ''}`} key={name}>
                  <span className="orchestrator-agent-icon"><Icon size={16} /></span>
                  <div><strong>{name}</strong><small>{role}</small></div>
                  <em>{state}</em>
                </article>
              ))}
            </div>
          </div>
          <div className="orchestrator-flow-footer">
            <span><span className="orchestrator-legend-dot working" /> Working</span>
            <span><span className="orchestrator-legend-dot queued" /> Queued</span>
            <span><span className="orchestrator-legend-dot ready" /> Ready</span>
            <span className="orchestrator-sim-note">Demo data only</span>
          </div>
        </section>

        <aside className="orchestrator-panel orchestrator-activity-panel">
          <div className="orchestrator-panel-heading">
            <div><h2>Execution Monitor</h2><p>Workflow activity snapshot</p></div>
            <Activity size={16} />
          </div>
          <div className="orchestrator-throughput">
            <div><span>Task throughput</span><strong>186 <small>tasks / hr</small></strong></div>
            <svg viewBox="0 0 280 72" role="img" aria-label="Simulated task throughput trend">
              <defs><linearGradient id="orchestrator-chart-fill" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stopColor="#8b72ff" stopOpacity=".4" /><stop offset="100%" stopColor="#8b72ff" stopOpacity="0" /></linearGradient></defs>
              <path className="orchestrator-chart-area" d="M0 60 C22 48 28 54 48 42 S78 50 96 34 S126 46 145 27 S176 38 194 24 S220 30 238 16 S260 22 280 5 V72 H0 Z" />
              <path className="orchestrator-chart-line" d="M0 60 C22 48 28 54 48 42 S78 50 96 34 S126 46 145 27 S176 38 194 24 S220 30 238 16 S260 22 280 5" />
            </svg>
            <div className="orchestrator-chart-labels"><span>09:00</span><span>11:00</span><span>13:00</span><span>15:00</span><span>Now</span></div>
          </div>
          <div className="orchestrator-activity-list">
            <div><span className="orchestrator-activity-icon"><GitBranch size={13} /></span><p><strong>Planning Agent</strong><small>Decomposed quarterly report task</small></p><time><Timer size={11} /> 2m</time></div>
            <div><span className="orchestrator-activity-icon"><Network size={13} /></span><p><strong>Research → Data Agent</strong><small>Context handoff completed</small></p><time><Timer size={11} /> 5m</time></div>
            <div><span className="orchestrator-activity-icon"><ShieldCheck size={13} /></span><p><strong>Validation Agent</strong><small>Waiting for next task</small></p><time><Timer size={11} /> 8m</time></div>
          </div>
        </aside>
      </div>

      <section className="orchestrator-capabilities">
        <div className="orchestrator-capabilities-heading">
          <div><h2>Orchestration Capabilities</h2><p>Core controls for managing your AI agent workforce</p></div>
          <span>7 CAPABILITIES</span>
        </div>
        <div className="orchestrator-capability-grid">
          {capabilities.map(({ title, detail, icon: Icon }, index) => (
            <article key={title}>
              <span className="orchestrator-capability-icon"><Icon size={16} /></span>
              <div><small>0{index + 1}</small><h3>{title}</h3><p>{detail}</p></div>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
