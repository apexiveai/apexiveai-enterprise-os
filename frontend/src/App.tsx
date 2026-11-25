import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  Activity, Bell, Boxes, BriefcaseBusiness, ChevronDown,
  CircleGauge, ClipboardCheck, Cloud, Cpu, Database, Factory,
  FileText, Fuel, Gauge, Hammer, HeartPulse,
  Hotel, Landmark, LayoutDashboard, Leaf, Menu,
  Moon, MoreHorizontal, Package, Plane, Search, Settings,
  ShieldCheck, ShoppingCart, Sparkles, Sun, Truck, UserRound,
  Users, WalletCards, Workflow, X, Play, Plus, CheckCircle2,
  AlertTriangle, Clock3, Copy, Rocket, RotateCcw, ChevronRight,
  GitBranch, Radio,
} from 'lucide-react'
import IndustrialOperations from './modules/industrial/IndustrialOperations'

type IconType = typeof LayoutDashboard

const navSections: Array<{ title: string; items: Array<{ label: string; icon: IconType }> }> = [
  { title: '', items: [{ label: 'Dashboard', icon: LayoutDashboard }, { label: 'Executive Center', icon: Gauge }] },
  { title: 'OPERATIONS', items: [
    { label: 'Group Management', icon: Users },
    { label: 'Finance', icon: Landmark },
    { label: 'Human Resources', icon: UserRound },
    { label: 'Procurement', icon: ShoppingCart },
    { label: 'Operations', icon: Activity },
    { label: 'Projects', icon: BriefcaseBusiness },
  ] },
  { title: 'BUSINESS UNITS', items: [
    { label: 'Energy', icon: Fuel },
    { label: 'Construction', icon: Hammer },
    { label: 'Manufacturing', icon: Factory },
    { label: 'Hospitality', icon: Hotel },
    { label: 'Logistics', icon: Truck },
    { label: 'Agriculture', icon: Leaf },
    { label: 'Trading', icon: Boxes },
    { label: 'Highway & Infrastructure', icon: Plane },
  ] },
  { title: 'INTELLIGENCE', items: [
    { label: 'AI Intelligence', icon: Sparkles },
    { label: 'Workflow Studio', icon: GitBranch },
    { label: 'RPA Automation', icon: Workflow },
    { label: 'RPA Orchestrator', icon: Radio },
    { label: 'Security', icon: ShieldCheck },
    { label: 'Reports & Analytics', icon: CircleGauge },
  ] },
  { title: 'INDUSTRIAL OPERATIONS', items: [
    { label: 'Robotics Fleet Management', icon: Truck },
    { label: 'Industrial OT Integration', icon: Radio },
    { label: 'IoT & Edge Gateway', icon: Database },
    { label: 'Robotic Process Control', icon: Cpu },
    { label: 'Drone & Inspection Management', icon: Plane },
    { label: 'Fleet & Logistics Automation', icon: Workflow },
    { label: 'Asset & Predictive Maintenance', icon: Activity },
    { label: 'Enterprise Operations Command Center', icon: Gauge },
  ] },
  { title: 'ENTERPRISE SUITES', items: [
    { label: 'AI Bot Studio', icon: Sparkles },
    { label: 'Agentic Process Automation', icon: Workflow },
    { label: 'Process & Task Mining', icon: CircleGauge },
    { label: 'Intelligent Documents', icon: FileText },
    { label: 'Integration Studio', icon: Cloud },
    { label: 'Decision & Rules', icon: GitBranch },
    { label: 'Workforce & Collaboration', icon: Users },
    { label: 'Automation Quality', icon: ClipboardCheck },
    { label: 'Automation Center', icon: Radio },
    { label: 'Low-Code Builder', icon: Boxes },
    { label: 'Enterprise Data', icon: Database },
    { label: 'Digital Twin', icon: Activity },
    { label: 'Security & Governance', icon: ShieldCheck },
    { label: 'Enterprise Marketplace', icon: Package },
    { label: 'Advanced Automation', icon: Cpu },
  ] },
]

const moduleCards: Array<{ label: string; icon: IconType }> = [
  { label: 'ERP System', icon: CircleGauge },
  { label: 'HR Management', icon: Users },
  { label: 'Finance Suite', icon: WalletCards },
  { label: 'Project Management', icon: ClipboardCheck },
  { label: 'RPA Studio', icon: Cpu },
  { label: 'Analytics', icon: Activity },
  { label: 'Asset Management', icon: Boxes },
  { label: 'Supply Chain', icon: Package },
  { label: 'CRM System', icon: HeartPulse },
  { label: 'Document Management', icon: FileText },
  { label: 'Security Center', icon: ShieldCheck },
]

const chartPoints = [
  '0,78 55,66 110,71 165,47 220,58 275,38 330,44 385,24 440,30',
  '0,92 55,86 110,76 165,80 220,68 275,65 330,54 385,48 440,40',
]

const enterpriseSuiteNames = [
  'AI Bot Studio',
  'Agentic Process Automation',
  'Process & Task Mining',
  'Intelligent Documents',
  'Integration Studio',
  'Decision & Rules',
  'Workforce & Collaboration',
  'Automation Quality',
  'Automation Center',
  'Low-Code Builder',
  'Enterprise Data',
  'Digital Twin',
  'Security & Governance',
  'Enterprise Marketplace',
  'Advanced Automation',
]

const studioCatalogGroups: Array<{
  title: string
  items: Array<{ label: string; description: string; icon: IconType }>
}> = [
  {
    title: 'Intelligence & AI',
    items: [
      { label: 'AI Bot Studio', description: 'Build and manage AI assistants', icon: Sparkles },
      { label: 'Intelligent Documents', description: 'Extract and validate document data', icon: FileText },
      { label: 'Agentic Process Automation', description: 'Coordinate agents, workflows, and RPA', icon: Workflow },
      { label: 'Advanced Automation', description: 'Automate tasks with AI and vision', icon: Cpu },
    ],
  },
  {
    title: 'Process & Integration',
    items: [
      { label: 'Workflow Studio', description: 'Design and manage business workflows', icon: GitBranch },
      { label: 'Process & Task Mining', description: 'Discover bottlenecks and process variants', icon: CircleGauge },
      { label: 'Integration Studio', description: 'Connect APIs, services, and events', icon: Cloud },
      { label: 'Decision & Rules', description: 'Manage policies and decision logic', icon: ClipboardCheck },
    ],
  },
  {
    title: 'Analytics & Operations',
    items: [
      { label: 'Reports & Analytics', description: 'Explore enterprise performance data', icon: Activity },
      { label: 'Automation Center', description: 'Monitor automation operations', icon: Radio },
      { label: 'Automation Quality', description: 'Test and measure automation quality', icon: ShieldCheck },
      { label: 'Enterprise Data', description: 'Manage trusted data and governance', icon: Database },
    ],
  },
  {
    title: 'Advanced & Ecosystem',
    items: [
      { label: 'Digital Twin', description: 'Model assets and simulate operations', icon: Boxes },
      { label: 'Workforce & Collaboration', description: 'Coordinate teams, skills, and approvals', icon: Users },
      { label: 'Security & Governance', description: 'Manage identity, policies, and audit', icon: ShieldCheck },
      { label: 'Enterprise Marketplace', description: 'Discover reusable enterprise solutions', icon: Package },
    ],
  },
]

const industrialModuleNames = [
  'Robotics Fleet Management',
  'Industrial OT Integration',
  'IoT & Edge Gateway',
  'Robotic Process Control',
  'Drone & Inspection Management',
  'Fleet & Logistics Automation',
  'Asset & Predictive Maintenance',
  'Enterprise Operations Command Center',
] as const

function isIndustrialModule(value: string): value is typeof industrialModuleNames[number] {
  return industrialModuleNames.some((name) => name === value)
}

function formatTime(date: Date) {
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

function App() {
  const [dark, setDark] = useState(true)
  const [active, setActive] = useState('AI Bot Studio')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [search, setSearch] = useState('')
  const [assistantOpen, setAssistantOpen] = useState(true)
  const [assistantText, setAssistantText] = useState('')
  const [assistantMessages, setAssistantMessages] = useState([
    'Good morning. How can I help you today?',
  ])
  const [now, setNow] = useState(new Date())
  const [notificationOpen, setNotificationOpen] = useState(false)
  const [records, setRecords] = useState<Record<string, Array<Record<string, string>>>>(() => {
    try { return JSON.parse(localStorage.getItem('apexive-module-records') || '{}') } catch { return {} }
  })

  useEffect(() => {
    const timer = window.setInterval(() => setNow(new Date()), 1000)
    return () => window.clearInterval(timer)
  }, [])

  useEffect(() => {
    localStorage.setItem('apexive-module-records', JSON.stringify(records))
  }, [records])

  const searchResults = useMemo(() => {
    const query = search.trim().toLowerCase()
    if (!query) return []
    return [...navSections.flatMap((section) => section.items), ...moduleCards]
      .filter((item) => item.label.toLowerCase().includes(query))
      .slice(0, 6)
  }, [search])

  const navigate = (label: string) => {
    setActive(label)
    setSidebarOpen(false)
  }

  const sendAssistantMessage = () => {
    const prompt = assistantText.trim()
    if (!prompt) return
    setAssistantMessages((messages) => [
      ...messages,
      prompt,
      `I’ve analyzed “${prompt}” and prepared the next recommended enterprise action.`,
    ])
    setAssistantText('')
  }

  const addRecord = () => {
    const next = {
      name: `New ${active} record`,
      owner: 'Aung Min Htet',
      status: 'Active',
      updated: now.toLocaleDateString(),
    }
    setRecords((current) => ({
      ...current,
      [active]: [...(current[active] || []), next],
    }))
  }

  const exportRecords = () => {
    const rows = records[active] || []
    const csv = 'Name,Owner,Status,Updated\n' + rows.map((row) =>
      [row.name, row.owner, row.status, row.updated].map((value) => `"${value || ''}"`).join(',')
    ).join('\n')
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }))
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `${active.toLowerCase().replace(/\s+/g, '-')}.csv`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  const isDashboard = active === 'Dashboard'
  const moduleName = active === 'Human Resources' ? 'HR Management' : active

  return (
    <div className={dark ? 'enterprise-app dark' : 'enterprise-app light'}>
      {sidebarOpen && <button className="sidebar-scrim" aria-label="Close menu" onClick={() => setSidebarOpen(false)} />}
      <aside className={`enterprise-sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="enterprise-brand">
          <div className="enterprise-brand-mark">A</div>
          <div>
            <strong>ApexiveAI</strong>
            <span>Enterprise Platform</span>
          </div>
          <button className="sidebar-close" onClick={() => setSidebarOpen(false)}><X /></button>
        </div>
        <nav className="enterprise-navigation">
          {navSections.map((section, sectionIndex) => (
            <div className="enterprise-nav-section" key={section.title || sectionIndex}>
              {section.title && <span className="enterprise-nav-heading">{section.title}</span>}
              {section.items.map(({ label, icon: Icon }) => (
                <button
                  key={label}
                  className={`enterprise-nav-item ${active === label ? 'active' : ''}`}
                  onClick={() => navigate(label)}
                >
                  <Icon size={16} />
                  <span>{label}</span>
                </button>
              ))}
            </div>
          ))}
        </nav>
        <div className="enterprise-sidebar-footer">
          <button onClick={() => navigate('Settings')}><Settings size={16} /> Settings</button>
          <div><span className="online-ring"><Cloud size={13} /></span><div><strong>ApexiveAI v1.0.0</strong><small>Enterprise Edition</small></div></div>
        </div>
      </aside>

      <main className="enterprise-main">
        <header className="enterprise-header">
          <button className="mobile-menu" onClick={() => setSidebarOpen(true)}><Menu /></button>
          <div className="enterprise-search">
            <Search size={16} />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search anything..."
              aria-label="Search modules"
            />
            <kbd>Ctrl + K</kbd>
            {searchResults.length > 0 && (
              <div className="search-results">
                {searchResults.map((item) => {
                  const Icon = item.icon
                  return (
                    <button key={item.label} onClick={() => { navigate(item.label); setSearch('') }}>
                      <Icon size={15} /> {item.label}
                    </button>
                  )
                })}
              </div>
            )}
          </div>
          <div className="header-status"><span /> System Online</div>
          <button className="theme-button" onClick={() => setDark(!dark)} title="Toggle theme">
            {dark ? <Sun size={17} /> : <Moon size={17} />}
          </button>
          <div className="header-notifications">
            <button className="notification-button" onClick={() => setNotificationOpen(!notificationOpen)}>
              <Bell size={18} /><span>2</span>
            </button>
            {notificationOpen && (
              <div className="notification-menu">
                <strong>Notifications</strong>
                <button onClick={() => navigate('Projects')}>Project approval requested</button>
                <button onClick={() => navigate('Security')}>Security scan completed</button>
              </div>
            )}
          </div>
          <button className="profile-button" onClick={() => navigate('Executive Center')}>
            <div className="profile-avatar">AM</div>
            <div><strong>Aung Min Htet</strong><span>Group CTO</span></div>
            <ChevronDown size={14} />
          </button>
        </header>

        <div className="enterprise-content">
          {isDashboard ? (
            <DashboardView
              now={now}
              navigate={navigate}
              assistantOpen={assistantOpen}
              setAssistantOpen={setAssistantOpen}
              assistantText={assistantText}
              setAssistantText={setAssistantText}
              assistantMessages={assistantMessages}
              setAssistantMessages={setAssistantMessages}
              sendAssistantMessage={sendAssistantMessage}
            />
          ) : active === 'RPA Automation' || active === 'RPA Studio' ? (
            <RPAStudio />
          ) : active === 'RPA Orchestrator' ? (
            <RPAOrchestrator />
          ) : active === 'Workflow Studio' ? (
            <WorkflowAutomationStudio />
          ) : isIndustrialModule(active) ? (
            <IndustrialOperations section={active} onNavigate={navigate} />
          ) : enterpriseSuiteNames.includes(active) ? (
            <EnterpriseAutomationSuite key={active} name={active} onNavigate={navigate} />
          ) : (
            <ModuleView
              name={moduleName}
              records={records[active] || records[moduleName] || []}
              addRecord={addRecord}
              exportRecords={exportRecords}
              navigate={navigate}
              isSettings={active === 'Settings'}
            />
          )}
        </div>

        <footer className="enterprise-footer">
          <span><strong>ApexiveAI</strong><i /> Empowering Enterprise. Driving a Smarter Future.</span>
          <span><b /> Secure <b /> Scalable <b /> Reliable <b /> Enterprise Grade</span>
        </footer>
      </main>
    </div>
  )
}

function DashboardView({
  now, navigate, assistantOpen, setAssistantOpen, assistantText, setAssistantText,
  assistantMessages, setAssistantMessages, sendAssistantMessage,
}: {
  now: Date
  navigate: (label: string) => void
  assistantOpen: boolean
  setAssistantOpen: (open: boolean) => void
  assistantText: string
  setAssistantText: (text: string) => void
  assistantMessages: string[]
  setAssistantMessages: (updater: (messages: string[]) => string[]) => void
  sendAssistantMessage: () => void
}) {
  const kpis = [
    { label: 'Total Group Revenue', value: 'MMK 842.5B', change: '+12.5%', icon: Landmark },
    { label: 'Total Assets', value: 'MMK 3.2T', change: '+8.7%', icon: Boxes },
    { label: 'Active Projects', value: '127', change: '+6.3%', icon: BriefcaseBusiness },
    { label: 'Total Employees', value: '12,850', change: '+4.1%', icon: Users },
    { label: 'Operational Efficiency', value: '94.2%', change: '+2.1%', icon: Gauge },
  ]

  return (
    <div className="dashboard-view">
      <section className="executive-hero">
        <div>
          <h1>Welcome back, Aung Min Htet!</h1>
          <p>Here&apos;s what&apos;s happening across your enterprise today.</p>
        </div>
        <div className="hero-time">
          <strong>{now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })}</strong>
          <span>{formatTime(now)}</span>
          <small>Yangon Time</small>
        </div>
      </section>

      <section className="kpi-strip">
        {kpis.map(({ label, value, change, icon: Icon }) => (
          <article key={label}>
            <Icon size={20} />
            <div><span>{label}</span><strong>{value}</strong><small>↗ {change}</small></div>
          </article>
        ))}
      </section>

      <section className="dashboard-middle">
        <article className="operations-map panel">
          <div className="panel-heading"><h2>Group Operations Overview <small>LIVE</small></h2><button>Last 30 Days <ChevronDown size={13} /></button></div>
          <div className="map-canvas">
            <div className="map-glow" />
            {[
              ['Construction', '92%', 'construction'],
              ['Energy', '98%', 'energy'],
              ['Manufacturing', '96%', 'manufacturing'],
              ['Logistics', '94%', 'logistics'],
              ['Hotels', '97%', 'hospitality'],
              ['Agriculture', '93%', 'agriculture'],
            ].map(([label, value, type]) => (
              <button className={`facility facility-${type}`} key={label} onClick={() => navigate(label)}>
                <span>{label}</span><strong>{value}</strong>
              </button>
            ))}
          </div>
        </article>

        <article className="performance panel">
          <div className="panel-heading"><h2>Business Performance</h2><div className="chart-legend"><span><i /> Revenue</span><span><i /> Profit</span><span><i /> Growth</span></div></div>
          <svg className="performance-chart" viewBox="0 0 440 145" preserveAspectRatio="none">
            {[20, 55, 90, 125].map((y) => <line key={y} x1="0" x2="440" y1={y} y2={y} />)}
            <polyline className="line-cyan" points={chartPoints[1]} />
            <polyline className="line-purple" points={chartPoints[0]} />
            <polyline className="line-blue" points="0,115 55,108 110,96 165,100 220,88 275,72 330,78 385,64 440,52" />
          </svg>
          <div className="chart-months"><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span><span>Nov</span></div>
        </article>

        {assistantOpen && (
          <article className="assistant panel">
            <div className="assistant-heading"><div><Sparkles size={17} /> AI Assistant</div><button onClick={() => setAssistantOpen(false)}><X size={15} /></button></div>
            <div className="assistant-status"><span /> Online</div>
            <div className="assistant-messages">
              {assistantMessages.slice(-4).map((message, index) => (
                <div className={index % 2 === 1 ? 'user-message' : ''} key={`${message}-${index}`}>{message}</div>
              ))}
            </div>
            <button className="assistant-action" onClick={() => setAssistantMessages((messages) => [...messages, 'Show group financial summary'])}>Show group financial summary <span>→</span></button>
            <button className="assistant-action" onClick={() => setAssistantMessages((messages) => [...messages, 'Analyze project risks'])}>Analyze project risks <span>→</span></button>
            <div className="assistant-input">
              <input value={assistantText} onChange={(event) => setAssistantText(event.target.value)} onKeyDown={(event) => event.key === 'Enter' && sendAssistantMessage()} placeholder="Ask anything..." />
              <button onClick={sendAssistantMessage}>➤</button>
            </div>
          </article>
        )}
      </section>

      <section className="dashboard-bottom">
        <article className="quick-modules panel">
          <div className="panel-heading"><div><h2>Key Modules</h2><p>Quick Access to Your Business Applications</p></div><button className="view-all">View All <span>→</span></button></div>
          <div className="module-grid">
            {moduleCards.map(({ label, icon: Icon }) => (
              <button key={label} onClick={() => navigate(label)}>
                <Icon size={21} /><span>{label}</span>
              </button>
            ))}
          </div>
        </article>
        <article className="activity-panel panel">
          <div className="panel-heading"><h2>Real-Time Activity</h2><button className="view-all">View All <span>→</span></button></div>
          {[
            ['10:20 AM', 'Fuel station #23 transaction completed', 'MMK 12,500,000'],
            ['10:18 AM', 'New project approved', 'Yangon Development'],
            ['10:15 AM', 'AI agent processed 1,248 documents', 'Engineering Dept'],
            ['10:12 AM', 'New employee onboarded', 'Aung Myat'],
          ].map(([time, title, detail]) => (
            <button className="activity-row" key={time} onClick={() => navigate('Reports & Analytics')}>
              <i /><div><strong>{time}</strong><span>{title}</span><small>{detail}</small></div>
            </button>
          ))}
        </article>
        <article className="health-panel panel">
          <div className="panel-heading"><h2>System Health</h2><span className="health-status">● All Systems Healthy</span></div>
          <div className="health-rings">
            {[['99.9%', 'Uptime'], ['96%', 'Performance'], ['98%', 'Security']].map(([value, label]) => (
              <div key={label}><div><strong>{value}</strong></div><span>{label}</span></div>
            ))}
          </div>
        </article>
      </section>
    </div>
  )
}

function EnterpriseAutomationSuite({ name, onNavigate }: {
  name: string
  onNavigate: (label: string) => void
}) {
  type SuiteAsset = {
    id: string
    name: string
    status: 'Draft' | 'Ready'
    updated: string
    features: string[]
  }
  type SuiteRun = {
    id: string
    asset: string
    status: 'Simulated'
    updated: string
  }
  type BuilderSettings = {
    name: string
    environment: string
    nodes: string[]
  }

  const suiteFeatures: Record<string, string[]> = {
    'AI Bot Studio': ['Bot Templates', 'Knowledge Base', 'Natural Language', 'Channels', 'Conversation Testing', 'Agent Tools'],
    'Agentic Process Automation': ['AI + RPA + Workflow', 'Autonomous Agents', 'Human-in-the-loop', 'Task Planning', 'Decision Control', 'Execution Evidence'],
    'Process & Task Mining': ['Event Discovery', 'Variant Analysis', 'Conformance', 'Task Capture', 'Bottlenecks', 'Mining Models'],
    'Intelligent Documents': ['OCR', 'Classification', 'Entity Extraction', 'Document Validation', 'Exception Review', 'Learning Models'],
    'Integration Studio': ['API Catalog', 'Connectors', 'OpenAPI', 'Mapping', 'Webhooks', 'Event Automation'],
    'Decision & Rules': ['Rule Tables', 'Decision Trees', 'Policy Testing', 'Versioning', 'Simulations', 'Conflict Detection'],
    'Workforce & Collaboration': ['Human Inbox', 'Team Spaces', 'Approvals', 'Comments', 'Skills & Capacity', 'Shift Operations'],
    'Automation Quality': ['Unit Tests', 'Visual Tests', 'Regression', 'Load Tests', 'Quality Gates', 'Coverage'],
    'Automation Center': ['Operations Overview', 'Incidents', 'Capacity', 'Queues', 'SLA Health', 'Command Center'],
    'Low-Code Builder': ['Pages', 'Forms', 'Data Models', 'Logic', 'Components', 'Publishing'],
    'Enterprise Data': ['Semantic Catalog', 'Lineage', 'Quality', 'Pipelines', 'Data Products', 'Governance'],
    'Digital Twin': ['Asset Models', 'IoT Streams', 'GIS Layers', 'Simulation', 'Predictive Alerts', 'Scene Replay'],
    'Security & Governance': ['Identity', 'Policies', 'Audit', 'Data Protection', 'Secrets', 'Compliance'],
    'Enterprise Marketplace': ['Connectors', 'Templates', 'Bots', 'Agents', 'Components', 'Developer Portal'],
    'Advanced Automation': ['Computer Vision', 'LLM Actions', 'Speech', 'Self-Healing', 'Edge Runtime', 'Robotics'],
  }
  const features = suiteFeatures[name] || ['Overview', 'Builder', 'Models', 'Runs', 'Analytics', 'Administration']
  const storagePrefix = `apexive-suite-${name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`
  const [activeTab, setActiveTab] = useState('Overview')
  const [toast, setToast] = useState('')
  const [search, setSearch] = useState('')
  const [assetDialogOpen, setAssetDialogOpen] = useState(false)
  const [newAssetName, setNewAssetName] = useState('')
  const [assets, setAssets] = useState<SuiteAsset[]>(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(`${storagePrefix}-assets`) || '[]')
      return Array.isArray(saved) ? saved : []
    } catch {
      return []
    }
  })
  const [runs, setRuns] = useState<SuiteRun[]>(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(`${storagePrefix}-runs`) || '[]')
      return Array.isArray(saved) ? saved : []
    } catch {
      return []
    }
  })
  const [builder, setBuilder] = useState<BuilderSettings>(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(`${storagePrefix}-builder`) || 'null')
      if (saved && typeof saved.name === 'string' && Array.isArray(saved.nodes)) return saved
    } catch {
      return { name, environment: 'Development', nodes: [] }
    }
    return { name, environment: 'Development', nodes: [] }
  })

  const notify = useCallback((message: string) => {
    setToast(message)
    window.setTimeout(() => setToast(''), 2200)
  }, [])

  useEffect(() => {
    try {
      localStorage.setItem(`${storagePrefix}-assets`, JSON.stringify(assets))
      localStorage.setItem(`${storagePrefix}-runs`, JSON.stringify(runs))
      localStorage.setItem(`${storagePrefix}-builder`, JSON.stringify(builder))
    } catch (error) {
      console.error(`Could not save ${name} workspace`, error)
    }
  }, [assets, builder, name, runs, storagePrefix])

  const createAsset = () => {
    setNewAssetName(`${name} Asset ${assets.length + 1}`)
    setAssetDialogOpen(true)
  }

  const saveAsset = () => {
    const assetName = newAssetName.trim()
    if (!assetName) {
      notify('Enter a name for the asset')
      return
    }
    setAssets((current) => [
      ...current,
      {
        id: `asset-${current.reduce((latest, item) => {
          const number = Number(item.id.replace('asset-', ''))
          return Number.isInteger(number) ? Math.max(latest, number) : latest
        }, 0) + 1}`,
        name: assetName,
        status: 'Draft',
        updated: 'Just now',
        features: [],
      },
    ])
    setAssetDialogOpen(false)
    setActiveTab('Assets')
    notify(`${assetName} saved to this workspace`)
  }

  const saveBuilder = () => {
    setAssets((current) => {
      const savedAsset: SuiteAsset = {
        id: 'builder',
        name: builder.name.trim() || name,
        status: 'Draft',
        updated: 'Just now',
        features: builder.nodes,
      }
      return current.some((asset) => asset.id === savedAsset.id)
        ? current.map((asset) => asset.id === savedAsset.id ? savedAsset : asset)
        : [...current, savedAsset]
    })
    notify(`${builder.name || name} configuration saved`)
  }

  const simulateRun = () => {
    const asset = assets[0]
    if (!asset) {
      notify('Create or save an asset before running it')
      setActiveTab('Assets')
      return
    }
    setRuns((current) => [
      {
        id: `run-${current.length + 1}`,
        asset: asset.name,
        status: 'Simulated',
        updated: 'Just now',
      },
      ...current,
    ])
    setActiveTab('Runs')
    notify(`${asset.name} simulation recorded`)
  }

  const exportWorkspace = () => {
    const data = activeTab === 'Runs' ? runs : assets
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `${storagePrefix}-${activeTab.toLowerCase()}.json`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="enterprise-suite">
      {toast && <div className="studio-toast"><CheckCircle2 size={16} /> {toast}</div>}
      {assetDialogOpen && (
        <div className="studio-modal-backdrop" onMouseDown={() => setAssetDialogOpen(false)}>
          <div className="studio-modal" onMouseDown={(event) => event.stopPropagation()}>
            <div className="studio-modal-header">
              <div><small>WORKSPACE ASSET</small><h2>Create {name} Asset</h2></div>
              <button onClick={() => setAssetDialogOpen(false)} aria-label="Close"><X size={16} /></button>
            </div>
            <label>Asset name<input autoFocus value={newAssetName} onChange={(event) => setNewAssetName(event.target.value)} /></label>
            <div className="studio-modal-actions">
              <button onClick={() => setAssetDialogOpen(false)}>Cancel</button>
              <button className="primary" onClick={saveAsset}>Create Asset</button>
            </div>
          </div>
        </div>
      )}
      <header className="suite-header">
        <div><span>ENTERPRISE AUTOMATION SUITE</span><h1>{name}</h1></div>
        <div className="suite-actions">
          <label><Search size={13} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search workspace" /></label>
          <button onClick={createAsset}><Plus size={14} /> Create New</button>
        </div>
      </header>
      <nav className="suite-tabs">
        {['Overview', 'Builder', 'Assets', 'Runs', 'Analytics', 'Settings'].map((tab) => (
          <button className={activeTab === tab ? 'active' : ''} key={tab} onClick={() => setActiveTab(tab)}>{tab}</button>
        ))}
      </nav>
      <div className="suite-content">
        {(name !== 'AI Bot Studio' || activeTab !== 'Overview') && (
          <section className="suite-kpis">
            {[
              ['Workspace Assets', String(assets.length), 'Saved locally'],
              ['Simulated Runs', String(runs.length), 'Local tests'],
              ['Builder Steps', String(builder.nodes.length), 'Configured'],
              ['Connection', 'Local', 'No live services'],
            ].map(([label, value, change]) => (
              <article key={label}><span>{label}</span><strong>{value}</strong><small>{change}</small></article>
            ))}
          </section>
        )}

        {activeTab === 'Overview' && (
          name === 'AI Bot Studio' ? (
            <div className="suite-catalog-layout">
              <div className="suite-catalog-groups">
                {studioCatalogGroups.map((group) => {
                  const items = group.items.filter((item) =>
                    !search || `${item.label} ${item.description}`.toLowerCase().includes(search.toLowerCase())
                  )
                  if (items.length === 0) return null
                  return (
                    <section className="suite-catalog-group" key={group.title}>
                      <h2>{group.title}</h2>
                      <div>
                        {items.map(({ label, description, icon: Icon }) => (
                          <button key={label} onClick={() => onNavigate(label)}>
                            <span><Icon size={16} /></span>
                            <div><strong>{label}</strong><small>{description}</small></div>
                            <ChevronRight size={14} />
                          </button>
                        ))}
                      </div>
                    </section>
                  )
                })}
                {studioCatalogGroups.every((group) =>
                  group.items.every((item) => !`${item.label} ${item.description}`.toLowerCase().includes(search.toLowerCase()))
                ) && <p className="suite-catalog-empty">No suites match your search.</p>}
              </div>
              <aside className="suite-insights">
                <strong>Recent Activity</strong>
                {runs.length === 0 && assets.length === 0 && <p>No workspace activity yet.</p>}
                {assets.slice(-3).reverse().map((asset) => (
                  <div key={asset.id}><i className="cyan" /><span><b>Asset saved</b><small>{asset.name} · {asset.updated}</small></span></div>
                ))}
                {runs.slice(0, 3).map((run) => (
                  <div key={run.id}><i className="green" /><span><b>Simulation recorded</b><small>{run.asset} · {run.updated}</small></span></div>
                ))}
              </aside>
            </div>
          ) : (
            <div className="suite-overview">
              <section className="suite-feature-grid">
                {features.filter((feature) => !search || feature.toLowerCase().includes(search.toLowerCase())).map((feature, index) => (
                  <button key={feature} onClick={() => { setActiveTab('Builder'); notify(`${feature} workspace opened`) }}>
                    <span>{String(index + 1).padStart(2, '0')}</span>
                    <div><strong>{feature}</strong><small>Configure and manage enterprise automation</small></div>
                    <ChevronRight size={14} />
                  </button>
                ))}
              </section>
              <aside className="suite-insights">
                <strong>Recent Activity</strong>
                {runs.length === 0 && assets.length === 0 && <p>No workspace activity yet.</p>}
                {assets.slice(-3).reverse().map((asset) => (
                  <div key={asset.id}><i className="cyan" /><span><b>Asset saved</b><small>{asset.name} · {asset.updated}</small></span></div>
                ))}
                {runs.slice(0, 3).map((run) => (
                  <div key={run.id}><i className="green" /><span><b>Simulation recorded</b><small>{run.asset} · {run.updated}</small></span></div>
                ))}
              </aside>
            </div>
          )
        )}

        {activeTab === 'Builder' && (
          <div className="suite-builder">
            <aside><strong>Toolbox</strong>{features.slice(0, 5).map((feature) => <button key={feature} onClick={() => setBuilder((current) => ({ ...current, nodes: [...current.nodes, feature] }))}><Plus size={12} /> {feature}</button>)}</aside>
            <main>
              <div className="suite-builder-heading"><strong>{name} Canvas</strong><span>Draft</span></div>
              <div className="suite-builder-canvas">
                {builder.nodes.length === 0 && <p>Select toolbox activities to add builder steps.</p>}
                {builder.nodes.map((feature, index) => (
                  <button key={`${feature}-${index}`} onClick={() => setBuilder((current) => ({ ...current, nodes: current.nodes.filter((_, nodeIndex) => nodeIndex !== index) }))}><span>{String(index + 1)}</span><strong>{feature}</strong><small>Click to remove</small></button>
                ))}
              </div>
            </main>
            <aside><strong>Properties</strong><label>Name<input value={builder.name} onChange={(event) => setBuilder((current) => ({ ...current, name: event.target.value }))} /></label><label>Environment<select value={builder.environment} onChange={(event) => setBuilder((current) => ({ ...current, environment: event.target.value }))}><option>Development</option><option>Staging</option><option>Production</option></select></label><button onClick={saveBuilder}>Save</button></aside>
          </div>
        )}

        {(activeTab === 'Assets' || activeTab === 'Runs' || activeTab === 'Analytics' || activeTab === 'Settings') && (
          <div className="suite-data-view">
            <div className="suite-data-toolbar">
              <strong>{activeTab}</strong>
              {activeTab === 'Runs' && <button onClick={simulateRun}><Play size={13} /> Simulate Run</button>}
              {activeTab === 'Assets' && <button onClick={createAsset}><Plus size={13} /> Add Asset</button>}
              {(activeTab === 'Assets' || activeTab === 'Runs') && <button onClick={exportWorkspace}>Export JSON</button>}
            </div>
            {activeTab === 'Assets' && assets.filter((asset) => asset.name.toLowerCase().includes(search.toLowerCase())).map((asset) => (
              <div className="suite-data-row" key={asset.id}><span><FileText size={15} /></span><strong>{asset.name}</strong><b>{asset.status}</b><small>{asset.updated} · {asset.features.length} steps</small><button onClick={() => setAssets((current) => current.filter((item) => item.id !== asset.id))} title="Delete asset"><X size={13} /></button></div>
            ))}
            {activeTab === 'Runs' && runs.map((run) => (
              <div className="suite-data-row" key={run.id}><span><Play size={15} /></span><strong>{run.asset}</strong><b>{run.status}</b><small>{run.updated}</small><span>{run.id}</span></div>
            ))}
            {activeTab === 'Analytics' && (
              <div className="suite-kpis">
                <article><span>Saved Assets</span><strong>{assets.length}</strong><small>Stored in this browser</small></article>
                <article><span>Simulation Runs</span><strong>{runs.length}</strong><small>Not connected to live systems</small></article>
                <article><span>Configured Steps</span><strong>{builder.nodes.length}</strong><small>{builder.environment}</small></article>
              </div>
            )}
            {activeTab === 'Settings' && (
              <div className="suite-settings">
                <strong>Workspace settings</strong>
                <label>Default asset name<input value={builder.name} onChange={(event) => setBuilder((current) => ({ ...current, name: event.target.value }))} /></label>
                <label>Environment<select value={builder.environment} onChange={(event) => setBuilder((current) => ({ ...current, environment: event.target.value }))}><option>Development</option><option>Staging</option><option>Production</option></select></label>
                <button onClick={() => notify('Workspace settings saved locally')}>Save Settings</button>
              </div>
            )}
            {activeTab === 'Assets' && assets.length === 0 && <p className="suite-empty">No saved assets yet. Create one to begin.</p>}
            {activeTab === 'Runs' && runs.length === 0 && <p className="suite-empty">No simulations yet. Save an asset, then run a local simulation.</p>}
          </div>
        )}
      </div>
    </div>
  )
}

function RPAOrchestrator() {
  type OrchestratorTab =
    | 'Fleet' | 'Machines' | 'Schedules' | 'Queues' | 'Deployments'
    | 'Monitoring' | 'Recovery' | 'Credentials' | 'Licenses' | 'Evidence'

  const [activeTab, setActiveTab] = useState<OrchestratorTab>('Fleet')
  const [killSwitch, setKillSwitch] = useState(false)
  const [toast, setToast] = useState('')
  const [robots, setRobots] = useState([
    { id: 'ROB-FIN-01', name: 'Finance Daily Bot', mode: 'Unattended', host: 'robot-prod-01', status: 'Running', load: 82, version: '1.4.0' },
    { id: 'ROB-HR-02', name: 'Payroll Reconciliation', mode: 'Attended', host: 'robot-att-03', status: 'Idle', load: 24, version: '1.2.1' },
    { id: 'ROB-DOC-03', name: 'Document Classifier', mode: 'Unattended', host: 'robot-prod-02', status: 'Running', load: 68, version: '2.1.0' },
    { id: 'ROB-ERP-04', name: 'ERP Reconciliation', mode: 'Unattended', host: 'robot-prod-01', status: 'Failed', load: 0, version: '1.8.2' },
  ])

  const notify = (message: string) => {
    setToast(message)
    window.setTimeout(() => setToast(''), 2600)
  }

  const stopRobot = (id: string) => {
    setRobots((current) => current.map((robot) =>
      robot.id === id ? { ...robot, status: 'Stopped', load: 0 } : robot
    ))
    notify(`${id} stopped remotely`)
  }

  return (
    <div className="orchestrator-view">
      {toast && <div className="studio-toast"><CheckCircle2 size={16} /> {toast}</div>}
      {killSwitch && (
        <div className="studio-modal-backdrop" onMouseDown={() => setKillSwitch(false)}>
          <div className="kill-switch-modal" onMouseDown={(event) => event.stopPropagation()}>
            <span><AlertTriangle size={23} /></span>
            <h2>Emergency Stop</h2>
            <p>This will stop all running robots and pause dispatched jobs.</p>
            <div><button onClick={() => setKillSwitch(false)}>Cancel</button><button className="danger" onClick={() => { setRobots((current) => current.map((robot) => ({ ...robot, status: 'Stopped', load: 0 }))); setKillSwitch(false); notify('Emergency stop activated') }}>Stop All Robots</button></div>
          </div>
        </div>
      )}

      <header className="orchestrator-header">
        <div><span>AUTOMATION CONTROL CENTER</span><h1>RPA Orchestrator</h1></div>
        <div className="orchestrator-actions">
          <span className="orchestrator-online"><i /> 4 robots connected</span>
          <button className="emergency-button" onClick={() => setKillSwitch(true)}><AlertTriangle size={14} /> Emergency Stop</button>
        </div>
      </header>

      <section className="orchestrator-kpis">
        {([
          ['Registered Robots', '24', Radio],
          ['Running Jobs', '7', Activity],
          ['Queue Backlog', '18', Boxes],
          ['Success Rate', '98.4%', CircleGauge],
        ] as [string, string, IconType][]).map(([label, value, MetricIcon]) => (
          <article key={label}><MetricIcon size={17} /><div><span>{label}</span><strong>{value}</strong></div></article>
        ))}
      </section>

      <div className="orchestrator-layout">
        <nav className="orchestrator-tabs">
          {(['Fleet', 'Machines', 'Schedules', 'Queues', 'Deployments', 'Monitoring', 'Recovery', 'Credentials', 'Licenses', 'Evidence'] as const).map((tab) => (
            <button className={activeTab === tab ? 'active' : ''} key={tab} onClick={() => setActiveTab(tab)}>{tab}</button>
          ))}
        </nav>

        <main className="orchestrator-content">
          {activeTab === 'Fleet' && (
            <section className="fleet-panel">
              <div className="orchestrator-panel-heading"><div><strong>Robot Registry</strong><span>Fleet and runtime status</span></div><button onClick={() => notify('Robot registry synchronized')}><RotateCcw size={13} /> Sync Fleet</button></div>
              <div className="robot-table">
                <div className="robot-row robot-head"><span>Robot</span><span>Mode</span><span>Machine</span><span>Status</span><span>CPU</span><span>Version</span><span /></div>
                {robots.map((robot) => (
                  <div className="robot-row" key={robot.id}>
                    <div><span className={`robot-avatar ${robot.status.toLowerCase()}`}><Cpu size={14} /></span><div><strong>{robot.name}</strong><small>{robot.id}</small></div></div>
                    <span>{robot.mode}</span><span>{robot.host}</span>
                    <span className={`runtime-status ${robot.status.toLowerCase()}`}><i /> {robot.status}</span>
                    <div className="cpu-load"><span><i style={{ width: `${robot.load}%` }} /></span><b>{robot.load}%</b></div>
                    <span>v{robot.version}</span>
                    <button className="robot-control" onClick={() => stopRobot(robot.id)} title="Stop robot"><X size={13} /></button>
                  </div>
                ))}
              </div>
            </section>
          )}

          {activeTab === 'Machines' && (
            <div className="orchestrator-card-grid">
              {[
                ['robot-prod-01', 'Production Pool', '8 / 10 slots', 'Running'],
                ['robot-prod-02', 'Production Pool', '5 / 8 slots', 'Running'],
                ['robot-att-03', 'Attended Pool', '2 / 6 slots', 'Running'],
                ['robot-dry-01', 'DR Pool', '0 / 4 slots', 'Standby'],
              ].map(([machine, pool, slots, status]) => (
                <section key={machine}>
                  <div><span><Database size={16} /></span><b className={status === 'Running' ? 'healthy' : ''}>{status}</b></div>
                  <strong>{machine}</strong><small>{pool}</small><div className="machine-slots"><span>{slots}</span><i /></div>
                  <button onClick={() => notify(`${machine} resource allocation opened`)}>Manage Pool</button>
                </section>
              ))}
            </div>
          )}

          {activeTab === 'Schedules' && (
            <section className="schedule-panel">
              <div className="orchestrator-panel-heading"><div><strong>Bot Scheduling</strong><span>Recurring and on-demand jobs</span></div><button onClick={() => notify('Schedule created')}><Plus size={13} /> New Schedule</button></div>
              {[
                ['DAILY_FINANCE_REPORT', 'Every day · 17:00', 'robot-prod-01', 'Active'],
                ['DOCUMENT_CLASSIFIER', 'Every 15 minutes', 'Unattended Pool', 'Active'],
                ['PAYROLL_RECONCILIATION', 'Mon–Fri · 09:00', 'robot-att-03', 'Paused'],
              ].map(([name, schedule, target, status]) => <div className="schedule-row" key={name}><Clock3 size={15} /><div><strong>{name}</strong><span>{schedule}</span></div><span>{target}</span><b className={status.toLowerCase()}>{status}</b><button onClick={() => notify(`${name} schedule updated`)}>Edit</button></div>)}
            </section>
          )}

          {activeTab === 'Queues' && (
            <section className="queue-panel">
              <div className="orchestrator-panel-heading"><div><strong>Queue Management</strong><span>Priority jobs and dispatcher</span></div><button onClick={() => notify('Job dispatcher started')}><Radio size={13} /> Dispatch</button></div>
              {[
                ['JOB-8821', 'DAILY_FINANCE_REPORT', 'Critical', 'Dispatching', '17:00:04'],
                ['JOB-8819', 'DOCUMENT_CLASSIFIER', 'High', 'Processing', '16:58:21'],
                ['JOB-8818', 'ERP_RECONCILIATION', 'Normal', 'Queued', '16:55:10'],
                ['JOB-8817', 'PAYROLL_RECONCILIATION', 'Low', 'Retrying', '16:48:03'],
              ].map(([id, job, priority, status, time]) => <div className="queue-row" key={id}><span>{id}</span><strong>{job}</strong><b className={priority.toLowerCase()}>{priority}</b><span className={`queue-status ${status.toLowerCase()}`}>{status}</span><small>{time}</small><button onClick={() => notify(`${id} moved to front of queue`)}>Prioritize</button></div>)}
            </section>
          )}

          {activeTab === 'Deployments' && (
            <div className="deployment-grid">
              {[
                ['DAILY_FINANCE_REPORT', '1.4.0', 'Production', 'Deployed'],
                ['DOCUMENT_CLASSIFIER', '2.1.0', 'Production', 'Deployed'],
                ['ERP_RECONCILIATION', '1.8.2', 'Staging', 'Testing'],
              ].map(([name, version, environment, status]) => <section key={name}><span><Package size={16} /></span><div><strong>{name}</strong><small>v{version} · {environment}</small></div><b className={status.toLowerCase()}>{status}</b><button onClick={() => notify(`${name} version promoted`)}>Promote</button></section>)}
            </div>
          )}

          {activeTab === 'Monitoring' && (
            <div className="monitoring-grid">
              <section className="runtime-chart"><strong>Runtime Monitoring</strong><div className="runtime-bars">{[58, 72, 64, 82, 76, 88, 71, 91, 84, 69, 77, 93].map((value, index) => <i key={index} style={{ height: `${value}%` }} />)}</div></section>
              <section className="execution-evidence"><strong>Execution Evidence</strong><div><CheckCircle2 size={14} /><span>Report file verified</span><b>Passed</b></div><div><CheckCircle2 size={14} /><span>Totals matched</span><b>Passed</b></div><div><AlertTriangle size={14} /><span>ERP response time</span><b>Warning</b></div></section>
              <section className="resource-panel"><strong>Resource Allocation</strong><div><span>CPU</span><b>68%</b><i><em style={{ width: '68%' }} /></i></div><div><span>Memory</span><b>54%</b><i><em style={{ width: '54%' }} /></i></div><div><span>Concurrent jobs</span><b>7 / 12</b><i><em style={{ width: '58%' }} /></i></div></section>
            </div>
          )}

          {activeTab === 'Recovery' && (
            <div className="recovery-grid">
              <section><AlertTriangle size={18} /><div><strong>Failure Recovery</strong><p>ERP_RECONCILIATION failed due to timeout.</p></div><button onClick={() => notify('Retry started according to policy')}>Retry Job</button></section>
              <section><RotateCcw size={18} /><div><strong>Retry Policy</strong><p>Maximum 3 retries · 5-minute interval</p></div><button onClick={() => notify('Retry policy configured')}>Configure</button></section>
              <section><Radio size={18} /><div><strong>Remote Robot Control</strong><p>Reconnect, restart or stop a worker.</p></div><button onClick={() => notify('Remote control session opened')}>Open Console</button></section>
            </div>
          )}

          {activeTab === 'Credentials' && (
            <section className="credential-panel">
              <div className="orchestrator-panel-heading"><div><strong>Credential Vault</strong><span>Encrypted robot credentials</span></div><button onClick={() => notify('Credential added securely')}><Plus size={13} /> Add Credential</button></div>
              {['Finance ERP', 'Document Center', 'Email Service', 'Production Database'].map((name) => <div className="credential-row" key={name}><ShieldCheck size={15} /><div><strong>{name}</strong><span>•••••••••••• · Rotated 12 days ago</span></div><button onClick={() => notify(`${name} credential details opened`)}>Manage</button></div>)}
            </section>
          )}

          {activeTab === 'Licenses' && (
            <section className="license-panel">
              <div className="orchestrator-panel-heading"><div><strong>Robot License Management</strong><span>Attended and unattended capacity</span></div><button onClick={() => notify('License usage refreshed')}>Refresh Usage</button></div>
              <div className="license-cards"><article><span>Unattended</span><strong>18 / 24</strong><i><b style={{ width: '75%' }} /></i></article><article><span>Attended</span><strong>6 / 10</strong><i><b style={{ width: '60%' }} /></i></article><article><span>AI Actions</span><strong>68.2K</strong><i><b style={{ width: '68%' }} /></i></article></div>
              <div className="usage-chart"><strong>Robot Usage Analytics</strong><div>{[38, 52, 46, 68, 61, 74, 82, 71, 88, 79, 92, 84].map((value, index) => <i key={index} style={{ height: `${value}%` }} />)}</div></div>
            </section>
          )}

          {activeTab === 'Evidence' && (
            <section className="evidence-panel">
              <div className="orchestrator-panel-heading"><div><strong>Execution Evidence</strong><span>Verified files and audit records</span></div><button onClick={() => notify('Evidence package exported')}>Export Package</button></div>
              {[
                ['EX-20481', 'DAILY_FINANCE_REPORT', 'Daily_Finance_Report_2026-11-25.xlsx', 'Validated'],
                ['EX-20480', 'DAILY_FINANCE_REPORT', 'Daily_Finance_Report_2026-11-24.xlsx', 'Validated'],
                ['EX-20479', 'DOCUMENT_CLASSIFIER', 'classified_documents.zip', 'Validated'],
              ].map(([id, bot, file, status]) => <div className="evidence-row" key={id}><FileText size={16} /><div><strong>{id}</strong><span>{bot}</span></div><small>{file}</small><b>{status}</b><button onClick={() => notify(`${file} evidence opened`)}>View</button></div>)}
            </section>
          )}
        </main>
      </div>
    </div>
  )
}

function WorkflowAutomationStudio() {
  type WorkflowTab = 'Designer' | 'Inbox' | 'Versions' | 'History' | 'Simulation'
  type ProcessNode = {
    id: string
    type: 'Start' | 'User' | 'AI' | 'Robot' | 'API' | 'Decision' | 'Parallel' | 'Timer' | 'Subprocess' | 'End'
    name: string
  }
  type WorkflowRecord = {
    workflow_id: string
    status: string
    nodes: ProcessNode[]
  }

  const [activeTab, setActiveTab] = useState<WorkflowTab>('Designer')
  const [selectedNode, setSelectedNode] = useState('approval')
  const [toast, setToast] = useState('')
  const [deployed, setDeployed] = useState(false)
  const [workflowId, setWorkflowId] = useState('')
  const [workflowLoaded, setWorkflowLoaded] = useState(false)
  const [nodes, setNodes] = useState<ProcessNode[]>([
    { id: 'start', type: 'Start', name: 'Purchase Request' },
    { id: 'validate', type: 'API', name: 'Validate Budget API' },
    { id: 'agent', type: 'AI', name: 'AI Risk Assessment' },
    { id: 'gateway', type: 'Decision', name: 'Within Budget?' },
    { id: 'approval', type: 'User', name: 'Finance Manager Approval' },
    { id: 'robot', type: 'Robot', name: 'Create ERP Purchase Order' },
    { id: 'notify', type: 'API', name: 'Notify Procurement' },
    { id: 'end', type: 'End', name: 'Request Completed' },
  ])
  const [inbox, setInbox] = useState([
    { id: 'WF-4821', title: 'Marketing equipment purchase', requester: 'Zaw Lin', sla: '2h 14m', priority: 'High' },
    { id: 'WF-4818', title: 'Supplier contract approval', requester: 'Thiri Moe', sla: '34m', priority: 'Critical' },
    { id: 'WF-4812', title: 'Annual budget adjustment', requester: 'Su Mon', sla: '1d 5h', priority: 'Normal' },
  ])

  const notify = (message: string) => {
    setToast(message)
    window.setTimeout(() => setToast(''), 2600)
  }

  useEffect(() => {
    let cancelled = false
    fetch('/api/v1/workflow/definitions')
      .then(async (response) => {
        if (!response.ok) throw new Error(`Workflow service returned ${response.status}`)
        return response.json() as Promise<WorkflowRecord[]>
      })
      .then((workflows) => {
        if (cancelled) return
        if (workflows.length > 0) {
          const workflow = workflows[0]
          setWorkflowId(workflow.workflow_id)
          setDeployed(workflow.status === 'deployed')
          setNodes(workflow.nodes)
          if (workflow.nodes.length > 0) setSelectedNode(workflow.nodes[0].id)
        }
        setWorkflowLoaded(true)
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setWorkflowLoaded(true)
          notify(`Workflow service unavailable: ${error instanceof Error ? error.message : String(error)}`)
        }
      })
    return () => { cancelled = true }
  }, [])

  const saveWorkflow = async () => {
    const response = await fetch(
      workflowId ? `/api/v1/workflow/definitions/${workflowId}` : '/api/v1/workflow/definitions',
      {
        method: workflowId ? 'PUT' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: 'Purchase Approval',
          description: 'Purchase request validation and approval workflow.',
          nodes,
        }),
      },
    )
    if (!response.ok) throw new Error(`Could not save workflow (${response.status})`)
    const workflow = await response.json() as WorkflowRecord
    setWorkflowId(workflow.workflow_id)
    return workflow
  }

  const runWorkflow = async () => {
    const workflow = await saveWorkflow()
    const response = await fetch(
      `/api/v1/workflow/executions?workflow_id=${encodeURIComponent(workflow.workflow_id)}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      },
    )
    if (!response.ok) throw new Error(`Could not start workflow (${response.status})`)
    const execution = await response.json() as { execution_id: string }
    notify(`Workflow execution started: ${execution.execution_id}`)
  }

  const deployWorkflow = async () => {
    const workflow = await saveWorkflow()
    const response = await fetch(`/api/v1/workflow/definitions/${workflow.workflow_id}/deploy`, {
      method: 'POST',
    })
    if (!response.ok) throw new Error(`Could not deploy workflow (${response.status})`)
    const deployedWorkflow = await response.json() as WorkflowRecord
    setDeployed(deployedWorkflow.status === 'deployed')
    notify(`Workflow version ${deployedWorkflow.status === 'deployed' ? 'deployed' : 'saved'}`)
  }

  const runWithNotification = (action: () => Promise<void>, label: string) => {
    void action().catch((error: unknown) => {
      notify(`${label}: ${error instanceof Error ? error.message : String(error)}`)
    })
  }

  const addNode = (type: ProcessNode['type']) => {
    const id = `${type.toLowerCase()}-${nodes.length + 1}`
    setNodes((current) => [...current, { id, type, name: `New ${type} Task` }])
    setSelectedNode(id)
    notify(`${type} node added to the process`)
  }

  const completeTask = (id: string) => {
    setInbox((current) => current.filter((task) => task.id !== id))
    notify(`${id} approved and sent to the next process step`)
  }

  const selected = nodes.find((node) => node.id === selectedNode) || nodes[0]

  const updateSelectedName = (name: string) => {
    setNodes((current) => current.map((node) =>
      node.id === selectedNode ? { ...node, name } : node
    ))
  }

  return (
    <div className="workflow-studio">
      {toast && <div className="studio-toast"><CheckCircle2 size={16} /> {toast}</div>}
      <header className="workflow-header">
        <div><span>BUSINESS PROCESS AUTOMATION</span><h1>Workflow Automation Studio</h1></div>
        <div className="workflow-actions">
          <button disabled={!workflowLoaded} onClick={() => runWithNotification(runWorkflow, 'Simulation failed')}><Play size={14} /> Simulate</button>
          <button disabled={!workflowLoaded} onClick={() => runWithNotification(deployWorkflow, 'Deployment failed')}><Rocket size={14} /> Deploy</button>
          <span className={`workflow-deploy-status ${deployed ? 'active' : ''}`}><i /> {deployed ? 'Deployed v3.2' : 'Draft v3.2'}</span>
        </div>
      </header>

      <div className="workflow-tabs">
        {(['Designer', 'Inbox', 'Versions', 'History', 'Simulation'] as const).map((tab) => (
          <button className={activeTab === tab ? 'active' : ''} key={tab} onClick={() => setActiveTab(tab)}>
            {tab}{tab === 'Inbox' && <span>{inbox.length}</span>}
          </button>
        ))}
      </div>

      {activeTab === 'Designer' && (
        <div className="workflow-studio-layout">
          <aside className="bpmn-palette">
            <strong>BPMN 2.0 Elements</strong>
            {([
              ['Start', 'Start Event', Activity],
              ['End', 'End Event', Activity],
              ['User', 'User Task', UserRound],
              ['AI', 'AI Agent Task', Sparkles],
              ['Robot', 'Robot Task', Cpu],
              ['API', 'API / Service Task', Cloud],
              ['Decision', 'Decision Gateway', GitBranch],
              ['Parallel', 'Parallel Gateway', Boxes],
              ['Timer', 'Timer / Event', Clock3],
              ['Subprocess', 'Subprocess', Package],
            ] as [ProcessNode['type'], string, IconType][]).map(([type, label, Icon]) => (
              <button draggable onDragStart={(event) => event.dataTransfer.setData('workflow-node', type)} onClick={() => addNode(type)} key={type}>
                <Icon size={14} /><span>{label}</span>
              </button>
            ))}
          </aside>

          <main
            className="bpmn-canvas"
            onDragOver={(event) => event.preventDefault()}
            onDrop={(event) => {
              event.preventDefault()
              const type = event.dataTransfer.getData('workflow-node') as ProcessNode['type']
              if (type) addNode(type)
            }}
          >
            <div className="bpmn-toolbar">
              <span><b>BPMN</b> PURCHASE_APPROVAL</span>
              <div><button onClick={() => notify('Process layout aligned')}>Align</button><button onClick={() => notify('Zoom reset')}>100%</button></div>
            </div>
            <div className="bpmn-flow">
              {nodes.map((node, index) => (
                <div className="bpmn-node-column" key={node.id}>
                  {index > 0 && <div className="bpmn-arrow"><ChevronRight size={13} /></div>}
                  <button
                    className={`bpmn-node ${node.type.toLowerCase().replace(' ', '-')} ${selectedNode === node.id ? 'selected' : ''}`}
                    onClick={() => setSelectedNode(node.id)}
                  >
                    <span className="bpmn-node-symbol">
                      {node.type === 'AI' ? <Sparkles size={16} /> :
                        node.type === 'Robot' ? <Cpu size={16} /> :
                        node.type === 'User' ? <UserRound size={16} /> :
                        node.type === 'Decision' ? <GitBranch size={16} /> :
                        node.type === 'API' ? <Cloud size={16} /> :
                        node.type === 'Timer' ? <Clock3 size={16} /> :
                        node.type === 'Subprocess' ? <Package size={16} /> :
                        <CircleGauge size={16} />}
                    </span>
                    <span><strong>{node.name}</strong><small>{node.type === 'Decision' ? 'Exclusive Gateway' : `${node.type} task`}</small></span>
                  </button>
                </div>
              ))}
              {nodes.length > 6 && <button className="bpmn-recovery" onClick={() => notify('Long-running recovery checkpoint restored')}><RotateCcw size={12} /> Recovery Point</button>}
            </div>
          </main>

          <aside className="bpmn-properties">
            {selected && (
              <>
                <div className="properties-heading"><strong>Properties</strong><span>{selected.type}</span></div>
                <label>Name<input value={selected.name} onChange={(event) => updateSelectedName(event.target.value)} /></label>
                {selected.type === 'User' && (
                  <>
                    <label>Approver<select defaultValue="manager"><option value="manager">Finance Manager</option><option value="director">Procurement Director</option><option value="committee">Approval Committee</option></select></label>
                    <label>Dynamic Form<select defaultValue="purchase"><option value="purchase">Purchase Approval Form</option><option value="contract">Contract Review Form</option></select></label>
                    <label>Priority<select defaultValue="high"><option>Normal</option><option>High</option><option>Critical</option></select></label>
                  </>
                )}
                {selected.type === 'AI' && (
                  <>
                    <label>AI Agent<select defaultValue="risk"><option value="risk">Enterprise Risk Agent</option><option value="policy">Policy Agent</option><option value="summary">Summary Agent</option></select></label>
                    <label>Data Scope<textarea defaultValue="Budget, vendor history, purchase amount" /></label>
                  </>
                )}
                {selected.type === 'Robot' && (
                  <>
                    <label>RPA Robot<select defaultValue="erp"><option value="erp">ERP Purchase Order Bot</option><option value="document">Document Classifier</option></select></label>
                    <label>Queue<select defaultValue="finance"><option value="finance">Finance Operations Queue</option><option value="procurement">Procurement Queue</option></select></label>
                  </>
                )}
                {selected.type === 'API' && (
                  <>
                    <label>Endpoint<input defaultValue="https://api.apexive.local/v1/purchase" /></label>
                    <label>Method<select defaultValue="POST"><option>POST</option><option>GET</option><option>PATCH</option></select></label>
                  </>
                )}
                {selected.type === 'Decision' && (
                  <>
                    <label>Condition<textarea defaultValue="purchaseAmount <= approvedBudget" /></label>
                    <div className="gateway-routes"><span><b>True</b><small>Continue approval</small></span><span><b>False</b><small>Escalate</small></span></div>
                  </>
                )}
                <label>SLA<select defaultValue="4h"><option value="4h">4 hours</option><option value="1d">1 business day</option><option value="3d">3 business days</option></select></label>
                <label>Error & Escalation<select defaultValue="manager"><option value="manager">Escalate to manager</option><option value="retry">Retry 3 times</option><option value="compensate">Run compensation</option></select></label>
              </>
            )}
          </aside>
        </div>
      )}

      {activeTab === 'Inbox' && (
        <div className="process-inbox">
          <header><div><strong>Human Task Inbox</strong><span>{inbox.length} tasks awaiting action</span></div><button onClick={() => notify('Inbox filter applied')}><Search size={13} /> Filter</button></header>
          {inbox.map((task) => (
            <div className="inbox-row" key={task.id}>
              <span className={`inbox-priority ${task.priority.toLowerCase()}`}><UserRound size={14} /></span>
              <div><strong>{task.title}</strong><span>{task.id} · Requested by {task.requester}</span></div>
              <span><Clock3 size={12} /> SLA {task.sla}</span>
              <b className={task.priority.toLowerCase()}>{task.priority}</b>
              <button onClick={() => completeTask(task.id)}>Review & Approve</button>
            </div>
          ))}
          {inbox.length === 0 && <div className="inbox-empty"><CheckCircle2 size={22} /><strong>No pending tasks</strong><span>The human approval queue is clear.</span></div>}
        </div>
      )}

      {activeTab === 'Versions' && (
        <div className="process-versions">
          {[
            ['3.2', 'Current Production', 'Deployed 2026-11-25', 'Active'],
            ['3.1', 'Previous Production', 'Deployed 2026-11-18', 'Archived'],
            ['3.0', 'Compliance Update', 'Deployed 2026-10-30', 'Archived'],
          ].map(([version, title, date, status]) => (
            <section key={version}><span>v{version}</span><div><strong>{title}</strong><small>{date}</small></div><b className={status.toLowerCase() === 'active' ? 'active' : ''}>{status}</b><button onClick={() => notify(`Workflow version ${version} actions opened`)}>Manage</button></section>
          ))}
        </div>
      )}

      {activeTab === 'History' && (
        <div className="process-history">
          {[
            ['WF-4821', 'Purchase Approval', 'Running', 'AI Risk Assessment', 'Finance Manager'],
            ['WF-4818', 'Supplier Contract', 'Waiting', 'Human Approval', 'Thiri Moe'],
            ['WF-4812', 'Budget Adjustment', 'Completed', 'ERP Purchase Order', 'System'],
          ].map(([id, name, status, step, owner]) => (
            <div className="history-row" key={id}><span>{id}</span><strong>{name}</strong><b className={status.toLowerCase()}>{status}</b><span>Current: {step}</span><span>Owner: {owner}</span><button onClick={() => notify(`${id} execution recovery view opened`)}><ChevronRight size={13} /></button></div>
          ))}
        </div>
      )}

      {activeTab === 'Simulation' && (
        <div className="process-simulation">
          <section><span><Activity size={18} /></span><div><strong>Workflow Simulation</strong><p>Run a test instance with simulated human and external responses.</p></div><button disabled={!workflowLoaded} onClick={() => runWithNotification(runWorkflow, 'Simulation failed')}>Run Simulation</button></section>
          <div className="simulation-metrics">
            {[['Steps', '8'], ['Branch Coverage', '87%'], ['SLA Risk', 'Low'], ['Recovery Point', '1']].map(([label, value]) => <article key={label}><span>{label}</span><strong>{value}</strong></article>)}
          </div>
        </div>
      )}
    </div>
  )
}

function RPAStudio() {
  type Bot = {
    id: string
    name: string
    description: string
    trigger: string
    status: 'Draft' | 'Tested' | 'Deployed'
    updated: string
  }
  type Execution = {
    id: string
    bot: string
    status: 'Completed' | 'Failed' | 'Running'
    started: string
    duration: string
  }

  const [bots, setBots] = useState<Bot[]>(() => {
    try {
      const saved = JSON.parse(localStorage.getItem('apexive-rpa-bots') || 'null')
      if (Array.isArray(saved)) return saved
    } catch { /* use defaults */ }
    return [{
      id: 'BOT-DAILY-FINANCE',
      name: 'DAILY_FINANCE_REPORT',
      description: 'Generate, validate and distribute the daily finance report.',
      trigger: 'Every day at 5:00 PM',
      status: 'Deployed',
      updated: 'Today',
    }]
  })
  const [executions, setExecutions] = useState<Execution[]>(() => {
    try {
      const saved = JSON.parse(localStorage.getItem('apexive-rpa-executions') || 'null')
      if (Array.isArray(saved)) return saved
    } catch { /* use defaults */ }
    return [
      { id: 'EX-20481', bot: 'DAILY_FINANCE_REPORT', status: 'Completed', started: 'Today 17:00', duration: '2m 14s' },
      { id: 'EX-20480', bot: 'DAILY_FINANCE_REPORT', status: 'Completed', started: 'Yesterday 17:00', duration: '2m 08s' },
    ]
  })
  const [selectedId, setSelectedId] = useState('BOT-DAILY-FINANCE')
  type StudioTab =
    | 'Design' | 'Triggers' | 'Recorders' | 'Selectors' | 'Vision'
    | 'Marketplace' | 'Code' | 'Debug' | 'Data' | 'Exceptions'
    | 'Testing' | 'Packages' | 'Publish' | 'Executions'
    | 'AI Generate' | 'Components' | 'Hybrid' | 'Visual Test'
    | 'Profiler' | 'Dependencies'
  const [activeTab, setActiveTab] = useState<StudioTab>('Design')
  const [designerMode, setDesignerMode] = useState<'Sequence' | 'Flowchart' | 'State Machine'>('Sequence')
  const [droppedActivities, setDroppedActivities] = useState<string[]>([])
  const [breakpoints, setBreakpoints] = useState<number[]>([3])
  const [debugRunning, setDebugRunning] = useState(false)
  const [naturalPrompt, setNaturalPrompt] = useState('Create a daily finance report robot that retrieves ERP transactions, validates totals, generates Excel and sends it to the finance manager.')
  const [healingEnabled, setHealingEnabled] = useState(true)
  const [codeText, setCodeText] = useState(
    "# Python automation action\nfrom apexive import finance\n\ndef validate(records):\n    return sum(r['amount'] for r in records)\n"
  )
  const [creating, setCreating] = useState(false)
  const [newBotName, setNewBotName] = useState('')
  const [triggerTime, setTriggerTime] = useState('17:00')
  const [toast, setToast] = useState('')

  useEffect(() => { localStorage.setItem('apexive-rpa-bots', JSON.stringify(bots)) }, [bots])
  useEffect(() => { localStorage.setItem('apexive-rpa-executions', JSON.stringify(executions)) }, [executions])

  const selected = bots.find((bot) => bot.id === selectedId) || bots[0]
  const steps = [
    { name: 'Trigger', detail: 'Every day at 5:00 PM', icon: Clock3 },
    { name: 'Connect to Finance ERP', detail: 'Finance ERP · ERP Connector', icon: Database },
    { name: "Retrieve today's transactions", detail: 'Transaction query', icon: Search },
    { name: 'Validate transaction records', detail: 'Required fields and totals', icon: CheckCircle2 },
    { name: 'Generate Excel report', detail: 'Excel workbook', icon: FileText },
    { name: 'Compare with previous day', detail: 'Variance analysis', icon: CircleGauge },
    { name: 'Upload to Document Center', detail: 'Finance / Daily Reports', icon: Cloud },
    { name: 'Notify Finance Manager', detail: 'Email and in-app notification', icon: Bell },
  ]

  const notify = (message: string) => {
    setToast(message)
    window.setTimeout(() => setToast(''), 2600)
  }

  const createBot = () => {
    const name = newBotName.trim()
    if (!name) return
    const id = `BOT-${Date.now()}`
    const bot: Bot = {
      id,
      name: name.toUpperCase().replace(/\s+/g, '_'),
      description: 'Custom automation workflow.',
      trigger: `Every day at ${triggerTime}`,
      status: 'Draft',
      updated: 'Just now',
    }
    setBots((current) => [bot, ...current])
    setSelectedId(id)
    setNewBotName('')
    setCreating(false)
    notify('Bot created as a draft')
  }

  const testBot = () => {
    if (!selected) return
    const id = `EX-${Date.now().toString().slice(-5)}`
    setExecutions((current) => [{
      id,
      bot: selected.name,
      status: 'Running',
      started: 'Just now',
      duration: 'Running',
    }, ...current])
    window.setTimeout(() => {
      setExecutions((current) => current.map((execution) =>
        execution.id === id
          ? { ...execution, status: 'Completed', duration: '1m 46s' }
          : execution
      ))
      setBots((current) => current.map((bot) =>
        bot.id === selected.id ? { ...bot, status: 'Tested', updated: 'Just now' } : bot
      ))
      notify('Test completed: file exists and totals are valid')
    }, 1200)
  }

  const deployBot = () => {
    if (!selected) return
    setBots((current) => current.map((bot) =>
      bot.id === selected.id ? { ...bot, status: 'Deployed', updated: 'Just now' } : bot
    ))
    notify(`${selected.name} deployed successfully`)
  }

  return (
    <div className="rpa-studio">
      {toast && <div className="studio-toast"><CheckCircle2 size={16} /> {toast}</div>}
      <header className="rpa-header">
        <div>
          <span className="module-kicker">AUTOMATION SPECIALIST</span>
          <h1>RPA Studio</h1>
        </div>
        <button className="studio-create" onClick={() => setCreating(true)}><Plus size={15} /> Create Robot</button>
      </header>

      {creating && (
        <div className="studio-modal-backdrop" onMouseDown={() => setCreating(false)}>
          <div className="studio-modal" onMouseDown={(event) => event.stopPropagation()}>
            <div className="studio-modal-header"><div><small>NEW AUTOMATION</small><h2>Create Robot</h2></div><button onClick={() => setCreating(false)}><X size={16} /></button></div>
            <label>Robot name<input value={newBotName} onChange={(event) => setNewBotName(event.target.value)} placeholder="DAILY_FINANCE_REPORT" /></label>
            <label>Trigger time<input type="time" value={triggerTime} onChange={(event) => setTriggerTime(event.target.value)} /></label>
            <div className="studio-modal-actions"><button onClick={() => setCreating(false)}>Cancel</button><button className="primary" onClick={createBot}>Create Draft</button></div>
          </div>
        </div>
      )}

      <div className="rpa-layout">
        <aside className="rpa-bot-list">
          <div className="rpa-list-heading"><strong>Robots</strong><span>{bots.length}</span></div>
          {bots.map((bot) => (
            <button className={selectedId === bot.id ? 'active' : ''} key={bot.id} onClick={() => setSelectedId(bot.id)}>
              <span className="bot-symbol"><Cpu size={15} /></span>
              <div><strong>{bot.name}</strong><small>{bot.status} · {bot.updated}</small></div>
              <ChevronRight size={14} />
            </button>
          ))}
        </aside>

        <main className="rpa-workspace">
          {selected && (
            <>
              <div className="rpa-workspace-header">
                <div><span className={`bot-status ${selected.status.toLowerCase()}`}><i /> {selected.status}</span><h2>{selected.name}</h2><p>{selected.description}</p></div>
                <div className="rpa-actions">
                  <button onClick={() => notify('Workflow copied to clipboard')}><Copy size={14} /> Copy</button>
                  <button onClick={testBot}><Play size={14} /> Test Run</button>
                  <button className="deploy" onClick={deployBot}><Rocket size={14} /> Deploy</button>
                </div>
              </div>
              <div className="rpa-tabs">
                {(['AI Generate', 'Design', 'Triggers', 'Recorders', 'Selectors', 'Vision', 'Marketplace', 'Code', 'Debug', 'Data', 'Exceptions', 'Testing', 'Packages', 'Publish', 'Components', 'Hybrid', 'Visual Test', 'Profiler', 'Dependencies', 'Executions'] as const).map((tab) => (
                  <button className={activeTab === tab ? 'active' : ''} key={tab} onClick={() => setActiveTab(tab)}>
                    {tab}{tab === 'Exceptions' && <span>1</span>}
                  </button>
                ))}
              </div>

              {activeTab === 'Design' && (
                <div className="workflow-designer">
                  <aside className="workflow-toolbox">
                    <strong>Activities</strong>
                    {['Control', 'Desktop', 'Web', 'Excel', 'ERP', 'Document', 'Email', 'Approval'].map((item) => (
                      <button
                        draggable
                        onDragStart={(event) => event.dataTransfer.setData('text/plain', item)}
                        key={item}
                        onClick={() => setDroppedActivities((current) => [...current, item])}
                      ><Plus size={12} /> {item}</button>
                    ))}
                  </aside>
                  <div
                    className="workflow-canvas"
                    onDragOver={(event) => event.preventDefault()}
                    onDrop={(event) => {
                      event.preventDefault()
                      const activity = event.dataTransfer.getData('text/plain')
                      if (activity) setDroppedActivities((current) => [...current, activity])
                    }}
                  >
                    <div className="workflow-title"><span>MAIN WORKFLOW</span><strong>{selected.name}</strong></div>
                    <div className="designer-mode">
                      {(['Sequence', 'Flowchart', 'State Machine'] as const).map((mode) => (
                        <button className={designerMode === mode ? 'active' : ''} key={mode} onClick={() => setDesignerMode(mode)}>{mode}</button>
                      ))}
                    </div>
                    {steps.map(({ name, detail, icon: Icon }, index) => (
                      <div className="workflow-node-wrap" key={name}>
                        {index > 0 && <div className="workflow-line"><ChevronRight size={12} /></div>}
                        <button
                          className={`workflow-node ${index === 0 ? 'trigger' : ''} ${breakpoints.includes(index) ? 'breakpoint' : ''}`}
                          onDoubleClick={() => setBreakpoints((current) => current.includes(index) ? current.filter((item) => item !== index) : [...current, index])}
                        >
                          <span className="workflow-node-icon"><Icon size={16} /></span>
                          <span><strong>{name}</strong><small>{detail}</small></span>
                          <MoreHorizontal size={14} />
                        </button>
                      </div>
                    ))}
                    {droppedActivities.map((activity, index) => (
                      <div className="workflow-node-wrap" key={`${activity}-${index}`}>
                        <div className="workflow-line"><ChevronRight size={12} /></div>
                        <button className="workflow-node">
                          <span className="workflow-node-icon"><Boxes size={16} /></span>
                          <span><strong>{activity} activity</strong><small>Custom workflow action</small></span>
                          <span
                            className="node-remove"
                            role="button"
                            tabIndex={0}
                            onClick={() => setDroppedActivities((current) => current.filter((_, itemIndex) => itemIndex !== index))}
                          ><X size={12} /></span>
                        </button>
                      </div>
                    ))}
                    {designerMode !== 'Sequence' && (
                      <div className="branch-preview"><span>True</span><strong>{designerMode} branch</strong><span>False</span></div>
                    )}
                  </div>
                  <aside className="workflow-properties">
                    <strong>Properties</strong>
                    <label>Timeout<select defaultValue="300"><option value="300">300 seconds</option><option value="600">600 seconds</option></select></label>
                    <label>Retry policy<select defaultValue="3"><option value="3">3 attempts</option><option value="5">5 attempts</option></select></label>
                    <label>Failure action<select defaultValue="human"><option value="human">Escalate to human</option><option value="stop">Stop execution</option></select></label>
                  </aside>
                </div>
              )}

              {activeTab === 'Triggers' && (
                <div className="rpa-panel-grid">
                  <section className="rpa-data-panel"><h3>Schedule</h3><div className="schedule-card"><Clock3 size={18} /><div><strong>Every day at 5:00 PM</strong><small>Asia/Yangon · Active</small></div><button>Change</button></div></section>
                  <section className="rpa-data-panel"><h3>Retry & Failure Policy</h3><div className="policy-row"><span>Maximum retries</span><strong>3</strong></div><div className="policy-row"><span>Retry interval</span><strong>5 minutes</strong></div><div className="policy-row"><span>On failure</span><strong>Notify operator</strong></div></section>
                </div>
              )}

              {activeTab === 'Recorders' && (
                <div className="authoring-panel">
                  <section><span className="authoring-icon"><Cpu size={20} /></span><div><strong>Desktop Recorder</strong><p>Capture Windows application actions.</p></div><button onClick={() => notify('Desktop recording started')}>Start Recording</button></section>
                  <section><span className="authoring-icon"><Cloud size={20} /></span><div><strong>Web Recorder</strong><p>Record browser clicks and form data.</p></div><button onClick={() => notify('Web recording started')}>Start Recording</button></section>
                  <section><span className="authoring-icon"><Activity size={20} /></span><div><strong>User Action Log</strong><p>Review and edit captured actions.</p></div><button onClick={() => notify('Action log opened')}>Open Log</button></section>
                </div>
              )}

              {activeTab === 'Selectors' && (
                <div className="authoring-panel selectors-panel">
                  <section><span className="authoring-icon"><Search size={20} /></span><div><strong>Selector Editor</strong><p>Inspect UI elements and validate selectors.</p></div><button onClick={() => notify('Selector highlighted and validated')}>Validate</button></section>
                  <div className="selector-preview">
                    <div className="mock-window"><strong>Finance ERP</strong><div>Company <span>APEXIVE</span></div><div>Transaction Date <span>2026-11-25</span></div><button>Submit</button></div>
                    <label>
                      Selector<textarea defaultValue='window:FinanceERP >> button:Submit' />
                      <button className="self-healing-toggle" onClick={() => setHealingEnabled((enabled) => !enabled)}>
                        <Sparkles size={12} /> Self-Healing {healingEnabled ? 'Enabled' : 'Disabled'}
                      </button>
                    </label>
                  </div>
                </div>
              )}

              {activeTab === 'Vision' && (
                <div className="authoring-panel">
                  <section><span className="authoring-icon"><Sparkles size={20} /></span><div><strong>Computer Vision</strong><p>Detect screen-based elements.</p></div><button onClick={() => notify('Screen element detection completed')}>Detect</button></section>
                  <section><span className="authoring-icon"><FileText size={20} /></span><div><strong>OCR Engine</strong><p>Recognize text from images and screens.</p></div><button onClick={() => notify('OCR extracted 248 text elements')}>Scan Screen</button></section>
                  <section><span className="authoring-icon"><Boxes size={20} /></span><div><strong>Image Recognition</strong><p>Match visual elements across resolutions.</p></div><button onClick={() => notify('Visual template matched')}>Match Image</button></section>
                </div>
              )}

              {activeTab === 'Marketplace' && (
                <div className="marketplace-grid">
                  {[
                    ['Excel Report Builder', 'Generate formatted workbooks', 'Excel'],
                    ['ERP Transaction Connector', 'Read and validate ERP records', 'ERP'],
                    ['Document Upload', 'Publish files to Document Center', 'Cloud'],
                    ['Finance Variance Analysis', 'Compare report periods', 'Finance'],
                    ['Email Delivery', 'Send files and notifications', 'Email'],
                    ['Approval Request', 'Route work to managers', 'Approval'],
                  ].map(([title, detail, icon]) => (
                    <section key={title}><span className="marketplace-icon">{icon.slice(0, 2)}</span><div><strong>{title}</strong><p>{detail}</p></div><button onClick={() => notify(`${title} added to workflow`)}><Plus size={12} /> Add</button></section>
                  ))}
                </div>
              )}

              {activeTab === 'Code' && (
                <div className="code-workbench">
                  <aside><strong>Python / C#</strong><button className="active">Python</button><button>C#</button></aside>
                  <section><div className="code-heading"><span>validate_transactions.py</span><button onClick={() => notify('Script syntax validated')}>Validate</button></div><textarea value={codeText} onChange={(event) => setCodeText(event.target.value)} spellCheck={false} /></section>
                  <aside className="code-output"><strong>Output</strong><pre>{'Ready\nNo syntax errors detected.'}</pre></aside>
                </div>
              )}

              {activeTab === 'Debug' && (
                <div className="debug-workbench">
                  <aside><strong>Debug Controls</strong><button onClick={() => { setDebugRunning(!debugRunning); notify(debugRunning ? 'Debug execution paused' : 'Debug execution started') }}>{debugRunning ? <RotateCcw size={13} /> : <Play size={13} />} {debugRunning ? 'Pause' : 'Start'}</button><button onClick={() => notify('Advanced to next action')}><ChevronRight size={13} /> Step Over</button><button onClick={() => notify('Debugger stopped')}><X size={13} /> Stop</button></aside>
                  <section><strong>Breakpoints</strong>{steps.slice(1, 6).map((step, index) => <button className={breakpoints.includes(index + 1) ? 'active' : ''} key={step.name} onClick={() => setBreakpoints((current) => current.includes(index + 1) ? current.filter((item) => item !== index + 1) : [...current, index + 1])}><span /><div>{step.name}<small>{breakpoints.includes(index + 1) ? 'Breakpoint enabled' : 'Click to enable'}</small></div></button>)}</section>
                  <aside><strong>Execution</strong><div className={`debug-state ${debugRunning ? 'running' : ''}`}><i /> {debugRunning ? 'Running' : 'Paused'}</div><div className="debug-frame"><span>Current step</span><strong>Validate transaction records</strong></div></aside>
                </div>
              )}

              {activeTab === 'Data' && (
                <div className="data-workbench">
                  <section><div className="data-heading"><strong>Variables</strong><button onClick={() => notify('Variable created')}><Plus size={12} /> Add</button></div>{[['transactionList', 'List', 'Local'], ['reportPath', 'String', 'Local'], ['erpConnection', 'Connection', 'Global'], ['retryCount', 'Integer', 'Argument']].map(([name, type, scope]) => <div className="data-row-authoring" key={name}><strong>{name}</strong><span>{type}</span><span>{scope}</span><MoreHorizontal size={13} /></div>)}</section>
                  <section><div className="data-heading"><strong>Arguments</strong><button onClick={() => notify('Argument created')}><Plus size={12} /> Add</button></div>{[['in_ReportDate', 'DateTime', 'In'], ['out_ValidatedTotal', 'Decimal', 'Out'], ['io_RetryPolicy', 'Dictionary', 'In/Out']].map(([name, type, direction]) => <div className="data-row-authoring" key={name}><strong>{name}</strong><span>{type}</span><span>{direction}</span><MoreHorizontal size={13} /></div>)}</section>
                  <section className="exception-rules"><strong>Exception Handling</strong><div><AlertTriangle size={15} /><span>ERP unavailable</span><b>Retry 3 times</b></div><div><AlertTriangle size={15} /><span>Validation failed</span><b>Escalate</b></div><button onClick={() => notify('Exception recovery rule saved')}>Save Rules</button></section>
                </div>
              )}

              {activeTab === 'AI Generate' && (
                <div className="ai-generate-workbench">
                  <section className="ai-prompt-panel">
                    <div><Sparkles size={18} /><strong>Natural Language to Robot</strong></div>
                    <textarea value={naturalPrompt} onChange={(event) => setNaturalPrompt(event.target.value)} />
                    <button
                      className="ai-generate-button"
                      onClick={() => {
                        setDroppedActivities((current) => [...current, 'ERP Transaction', 'Excel Report', 'Document Upload', 'Finance Notification'])
                        setActiveTab('Design')
                        notify('AI generated 8 workflow activities with validation and exception branches')
                      }}
                    ><Sparkles size={14} /> Generate Workflow</button>
                  </section>
                  <section className="ai-suggestion-panel">
                    <strong>Generated automation plan</strong>
                    {[
                      ['1', 'Connect to Finance ERP', 'Recommended connector'],
                      ['2', 'Retrieve today&apos;s transactions', 'Add transaction date filter'],
                      ['3', 'Validate totals', 'Required business-rule check'],
                      ['4', 'Generate and upload report', 'Excel + Document Center'],
                      ['5', 'Notify Finance Manager', 'Email + in-app alert'],
                    ].map(([number, title, detail]) => (
                      <div key={number}><span>{number}</span><div><b>{title}</b><small>{detail}</small></div><CheckCircle2 size={13} /></div>
                    ))}
                    <button onClick={() => notify('AI Code Assistant generated validation code')}><Cpu size={13} /> Generate Code Assistant</button>
                  </section>
                </div>
              )}

              {activeTab === 'Components' && (
                <div className="component-library">
                  {[
                    ['Login to ERP', 'Authentication', 'ERP'],
                    ['Read transaction table', 'Data extraction', 'Database'],
                    ['Write Excel report', 'Spreadsheet', 'Excel'],
                    ['Upload document', 'Storage', 'Document'],
                    ['Send approval request', 'Workflow', 'Approval'],
                    ['Capture UI evidence', 'Diagnostics', 'Vision'],
                  ].map(([name, category, icon]) => (
                    <section key={name}><span>{icon.slice(0, 2)}</span><div><strong>{name}</strong><small>{category} · Reusable</small></div><button onClick={() => { setDroppedActivities((current) => [...current, name]); notify(`${name} added to workflow`) }}><Plus size={12} /> Use</button></section>
                  ))}
                </div>
              )}

              {activeTab === 'Hybrid' && (
                <div className="hybrid-workbench">
                  <section><span className="authoring-icon"><Cpu size={20} /></span><div><strong>Desktop Automation</strong><p>Windows UI, legacy applications, Citrix and installed software.</p></div><button onClick={() => notify('Desktop context attached')}>Attach Desktop</button></section>
                  <section><span className="authoring-icon"><Cloud size={20} /></span><div><strong>Browser Automation</strong><p>Modern web portals, browser forms and authenticated sessions.</p></div><button onClick={() => notify('Browser context attached')}>Attach Browser</button></section>
                  <section className="hybrid-flow"><strong>Hybrid execution flow</strong><div><span>Desktop ERP</span><ChevronRight size={12} /><span>Browser Portal</span><ChevronRight size={12} /><span>Document Center</span></div></section>
                </div>
              )}

              {activeTab === 'Visual Test' && (
                <div className="visual-test-workbench">
                  <section className="visual-baseline"><strong>Visual regression baseline</strong><div className="mock-window"><strong>Daily Finance Report</strong><div>Transactions <span>1,248</span></div><div>Validated total <span>MMK 842.5B</span></div><div>Status <span>Ready</span></div></div></section>
                  <section className="visual-result"><strong>Comparison result</strong><div className="visual-score"><span>99.8%</span><small>Visual match</small></div><div className="policy-row"><span>Layout difference</span><strong>0.02%</strong></div><div className="policy-row"><span>Changed elements</span><strong>1</strong></div><button onClick={() => notify('Visual regression test passed')}><CheckCircle2 size={13} /> Accept Baseline</button></section>
                </div>
              )}

              {activeTab === 'Profiler' && (
                <div className="profiler-workbench">
                  <section><div><strong>Robot Performance Profiler</strong><p>Execution time and resource usage.</p></div><button onClick={() => notify('Profiler started for the selected workflow')}><Play size={13} /> Start Profile</button></section>
                  {[
                    ['ERP connection', '420 ms', '18%'],
                    ['Transaction retrieval', '680 ms', '29%'],
                    ['Record validation', '340 ms', '14%'],
                    ['Excel generation', '510 ms', '22%'],
                    ['Document upload', '390 ms', '17%'],
                  ].map(([name, time, usage]) => <div className="profile-row" key={name}><strong>{name}</strong><div><i style={{ width: usage }} /></div><span>{time}</span><span>{usage} CPU</span></div>)}
                </div>
              )}

              {activeTab === 'Dependencies' && (
                <div className="dependency-workbench">
                  <section>
                    <strong>Workflow Dependency Analyzer</strong>
                    <div className="dependency-map">
                      {['ERP', 'Transaction Service', 'Excel Package', 'Document Center', 'Email Service'].map((item, index) => (
                        <div key={item} className={index === 1 ? 'critical' : ''}><span>{index + 1}</span><strong>{item}</strong>{index < 4 && <ChevronRight size={13} />}</div>
                      ))}
                    </div>
                  </section>
                  <aside><strong>Risk analysis</strong><div><span>Missing dependencies</span><b>0</b></div><div><span>External services</span><b>4</b></div><div><span>Approval points</span><b>1</b></div><button onClick={() => notify('Dependency graph validated')}><CheckCircle2 size={13} /> Validate Graph</button></aside>
                </div>
              )}

              {activeTab === 'Testing' && (
                <div className="testing-workbench">
                  <header><div><strong>Automation Unit Tests</strong><p>Validate activities and workflow behavior.</p></div><button onClick={() => notify('All automation tests passed')}><Play size={13} /> Run Tests</button></header>
                  {[
                    ['ERP connection test', 'Passed', '124 ms'],
                    ['Transaction validation test', 'Passed', '238 ms'],
                    ['Excel generation test', 'Passed', '512 ms'],
                    ['Previous-day comparison test', 'Passed', '196 ms'],
                    ['Document upload test', 'Passed', '341 ms'],
                  ].map(([name, status, duration]) => <div className="test-row" key={name}><CheckCircle2 size={14} /><strong>{name}</strong><span>{status}</span><span>{duration}</span></div>)}
                </div>
              )}

              {activeTab === 'Packages' && (
                <div className="packages-workbench">
                  <section><div className="data-heading"><strong>Package Manager</strong><button onClick={() => notify('Dependencies restored')}><RotateCcw size={12} /> Restore</button></div>{[['Apexive.ERP', '2.4.1', 'Installed'], ['Apexive.Excel', '3.1.0', 'Installed'], ['Apexive.Documents', '1.8.3', 'Installed'], ['Apexive.CV', '2.0.0', 'Available']].map(([name, version, status]) => <div className="package-row" key={name}><Boxes size={15} /><div><strong>{name}</strong><small>v{version}</small></div><button onClick={() => notify(`${name} ${status.toLowerCase() === 'available' ? 'installed' : 'is ready'}`)}>{status}</button></div>)}</section>
                  <section className="git-panel"><strong>Version Control</strong><div className="git-status"><GitBranch size={18} /><div><b>main</b><span>Clean working tree</span></div></div><div className="git-actions"><button onClick={() => notify('Changes committed to local Git repository')}>Commit</button><button onClick={() => notify('Pushed to the configured remote')}>Push</button><button onClick={() => notify('Pulled latest workflow changes')}>Pull</button></div><small>Last commit: Workflow retry policy · 12 minutes ago</small></section>
                </div>
              )}

              {activeTab === 'Publish' && (
                <div className="publish-workbench">
                  <section><span className="publish-icon"><Rocket size={22} /></span><div><strong>Publish Manager</strong><p>Deploy this robot to an enterprise runtime.</p></div></section>
                  <div className="publish-grid">
                    <label>Environment<select defaultValue="production"><option value="development">Development</option><option value="staging">Staging</option><option value="production">Production</option></select></label>
                    <label>Runtime<select defaultValue="robot-prod-01"><option value="robot-prod-01">robot-prod-01</option><option value="robot-prod-02">robot-prod-02</option></select></label>
                    <label>Version<select defaultValue="1.4.0"><option value="1.4.0">1.4.0 (latest)</option><option value="1.3.2">1.3.2</option></select></label>
                    <label>Release notes<textarea defaultValue="Daily finance report validation and document upload improvements." /></label>
                  </div>
                  <button className="publish-button" onClick={deployBot}><Rocket size={14} /> Publish to Production</button>
                </div>
              )}

              {activeTab === 'Executions' && (
                <section className="execution-panel">
                  <div className="execution-heading"><strong>Execution History</strong><button onClick={testBot}><RotateCcw size={13} /> Run now</button></div>
                  {executions.map((execution) => (
                    <button className="execution-row" key={execution.id} onClick={() => notify(`Evidence for ${execution.id}: report exists and totals are valid`)}>
                      <span className={execution.status.toLowerCase()}>{execution.status === 'Completed' ? <CheckCircle2 size={15} /> : execution.status === 'Failed' ? <AlertTriangle size={15} /> : <RotateCcw size={15} />}</span>
                      <div><strong>{execution.id}</strong><small>{execution.bot}</small></div>
                      <span>{execution.started}</span><span>{execution.duration}</span><span className={`execution-status ${execution.status.toLowerCase()}`}>{execution.status}</span><ChevronRight size={14} />
                    </button>
                  ))}
                </section>
              )}

              {activeTab === 'Exceptions' && (
                <section className="exception-panel">
                  <div className="exception-icon"><AlertTriangle size={22} /></div><div><strong>Human operator queue</strong><p>No unresolved production exceptions.</p></div><button onClick={() => notify('No exceptions require escalation')}>View queue</button>
                </section>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  )
}

function ModuleView({ name, records, addRecord, exportRecords, navigate, isSettings }: {
  name: string
  records: Array<Record<string, string>>
  addRecord: () => void
  exportRecords: () => void
  navigate: (label: string) => void
  isSettings: boolean
}) {
  const [query, setQuery] = useState('')
  const filtered = records.filter((record) => Object.values(record).join(' ').toLowerCase().includes(query.toLowerCase()))
  const Icon = isSettings ? Settings : Boxes

  return (
    <div className="module-view">
      <header className="module-header">
        <div><span className="module-icon"><Icon size={22} /></span><div><small>Enterprise Application</small><h1>{name}</h1></div></div>
        <div className="module-actions">
          <button onClick={exportRecords}><Database size={15} /> Export</button>
          <button className="primary" onClick={addRecord}>+ Add Record</button>
        </div>
      </header>
      {isSettings ? (
        <div className="settings-grid">
          {[
            ['General', 'Company profile and regional settings'],
            ['Identity & Access', 'Users, roles and authentication'],
            ['Notifications', 'Email, SMS and system alerts'],
            ['Integrations', 'Connected external services'],
            ['Security', 'Policies, audit and encryption'],
            ['Data', 'Backups, retention and exports'],
          ].map(([title, detail]) => (
            <button key={title} onClick={() => navigate(title)}><Settings size={18} /><strong>{title}</strong><span>{detail}</span></button>
          ))}
        </div>
      ) : (
        <section className="module-content panel">
          <div className="table-toolbar">
            <div><strong>Records</strong><span>{filtered.length} items</span></div>
            <label><Search size={14} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Filter records" /></label>
          </div>
          <div className="data-table">
            <div className="data-row data-header"><span>Name</span><span>Owner</span><span>Status</span><span>Updated</span><span /></div>
            {(filtered.length ? filtered : [
              { name: `${name} Overview`, owner: 'Aung Min Htet', status: 'Active', updated: 'Today' },
              { name: 'Group Operations Record', owner: 'Enterprise Team', status: 'Processing', updated: 'Today' },
            ]).map((record, index) => (
              <div className="data-row" key={`${record.name}-${index}`}>
                <strong>{record.name}</strong><span>{record.owner}</span><span className="record-status">{record.status}</span><span>{record.updated}</span>
                <button title="More options"><MoreHorizontal size={16} /></button>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

export default App
