import { useState, type FormEvent, type ReactNode } from 'react'
import {
  Activity,
  AlertTriangle,
  Boxes,
  CheckCircle2,
  ChevronRight,
  Cpu,
  Database,
  Factory,
  Gauge,
  Plane,
  Plus,
  Radio,
  ShieldCheck,
  Truck,
  Wrench,
  X,
} from 'lucide-react'

type IndustrialSection =
  | 'Robotics Fleet Management'
  | 'Industrial OT Integration'
  | 'IoT & Edge Gateway'
  | 'Robotic Process Control'
  | 'Drone & Inspection Management'
  | 'Fleet & Logistics Automation'
  | 'Asset & Predictive Maintenance'
  | 'Enterprise Operations Command Center'

type Robot = {
  id: string
  name: string
  kind: string
  route: string
  task: string
  battery: number
  status: 'Idle' | 'Running' | 'Charging' | 'Stopped'
}

type Connector = {
  id: string
  name: string
  protocol: string
  endpoint: string
  status: 'Draft' | 'Simulated OK'
}

type Sensor = {
  id: string
  name: string
  kind: string
  value: number
  unit: string
  threshold: number
}

type Workcell = {
  id: string
  name: string
  process: string
  safetyEnabled: boolean
  status: 'Stopped' | 'Running (simulated)'
}

type Inspection = {
  id: string
  site: string
  type: string
  status: 'Queued' | 'Completed (simulated)'
}

type Delivery = {
  id: string
  origin: string
  destination: string
  load: string
  status: 'Queued' | 'Optimized' | 'Dispatched (simulated)' | 'Verified (simulated)'
}

type PlantAsset = {
  id: string
  name: string
  area: string
  health: number
  maintenance: 'No schedule' | 'Scheduled'
}

type IndustrialData = {
  robots: Robot[]
  connectors: Connector[]
  sensors: Sensor[]
  workcells: Workcell[]
  inspections: Inspection[]
  deliveries: Delivery[]
  assets: PlantAsset[]
}

const STORAGE_KEY = 'apexive-industrial-operations-v1'

const initialData: IndustrialData = {
  robots: [
    { id: 'AMR-001', name: 'Warehouse AMR', kind: 'AMR', route: 'A1 → B3', task: 'Pallet transfer', battery: 84, status: 'Running' },
    { id: 'AGV-002', name: 'Line-side AGV', kind: 'AGV', route: 'Line 2 → Buffer', task: 'Material delivery', battery: 62, status: 'Idle' },
    { id: 'AMR-003', name: 'Inspection AMR', kind: 'AMR', route: 'Zone C', task: 'Standby', battery: 28, status: 'Charging' },
  ],
  connectors: [],
  sensors: [
    { id: 'S-001', name: 'Boiler temperature', kind: 'Temperature', value: 78.4, unit: '°C', threshold: 90 },
    { id: 'S-002', name: 'Hydraulic pressure', kind: 'Pressure', value: 6.2, unit: 'bar', threshold: 8 },
    { id: 'S-003', name: 'Motor vibration', kind: 'Vibration', value: 3.1, unit: 'mm/s', threshold: 5 },
    { id: 'S-004', name: 'Tank level', kind: 'Tank Level', value: 72, unit: '%', threshold: 95 },
    { id: 'S-005', name: 'Line energy', kind: 'Energy', value: 124.8, unit: 'kWh', threshold: 180 },
  ],
  workcells: [
    { id: 'CELL-01', name: 'Packaging Cell 01', process: 'Packaging', safetyEnabled: true, status: 'Stopped' },
    { id: 'CELL-02', name: 'Palletizing Cell 02', process: 'Palletizing', safetyEnabled: true, status: 'Stopped' },
    { id: 'CELL-03', name: 'Pick-and-Place Cell 03', process: 'Pick-and-Place', safetyEnabled: true, status: 'Stopped' },
  ],
  inspections: [],
  deliveries: [],
  assets: [
    { id: 'ASSET-001', name: 'Compressor A', area: 'Utilities', health: 81, maintenance: 'No schedule' },
    { id: 'ASSET-002', name: 'Conveyor Motor B', area: 'Line 2', health: 64, maintenance: 'No schedule' },
    { id: 'ASSET-003', name: 'Pump C', area: 'Water Plant', health: 92, maintenance: 'No schedule' },
  ],
}

const capabilities: Array<{ name: IndustrialSection; description: string }> = [
  { name: 'Robotics Fleet Management', description: 'AMR/AGV routes, task queues, battery and fleet status.' },
  { name: 'Industrial OT Integration', description: 'Connector setup for PLC, SCADA, OPC UA, Modbus and MQTT.' },
  { name: 'IoT & Edge Gateway', description: 'Temperature, pressure, vibration, tank level and energy signals.' },
  { name: 'Robotic Process Control', description: 'Safety-interlocked packaging, palletizing and pick-and-place cells.' },
  { name: 'Drone & Inspection Management', description: 'Construction surveys, stockpiles and infrastructure inspections.' },
  { name: 'Fleet & Logistics Automation', description: 'Dispatch, route planning, delivery tracking and verification.' },
  { name: 'Asset & Predictive Maintenance', description: 'Asset health indicators and maintenance schedules.' },
  { name: 'Enterprise Operations Command Center', description: 'One view of agents, automation, robots, machines and alerts.' },
]

const architecture = [
  { title: 'AI Agent Studio', subtitle: 'Plans tasks from user intent and executes approved actions.', target: 'AI Bot Studio', tone: 'aqua' },
  { title: 'Workflow + RPA + Policy Engine', subtitle: 'Coordinates workflows, approvals, policies, and automation.', target: 'Workflow Studio', tone: 'blue' },
  { title: 'Integration Hub + Edge Gateway', subtitle: 'Connects ERP, APIs, PLCs, IoT devices, and robot interfaces.', target: 'Industrial OT Integration', tone: 'sand' },
  { title: 'Physical Robots & Industrial Machines', subtitle: 'Integrates robots and machines behind safety interlocks.', target: 'Robotics Fleet Management', tone: 'mint' },
]

function loadData(): IndustrialData {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (!saved) return initialData
    const value: unknown = JSON.parse(saved)
    if (!value || typeof value !== 'object') throw new Error('Stored industrial workspace is not an object')
    return { ...initialData, ...(value as Partial<IndustrialData>) }
  } catch (error) {
    console.error('Could not load the industrial workspace', error)
    return initialData
  }
}

function nextId(prefix: string, records: Array<{ id: string }>) {
  const next = records.reduce((latest, item) => {
    const number = Number(item.id.replace(`${prefix}-`, ''))
    return Number.isInteger(number) ? Math.max(latest, number) : latest
  }, 0) + 1
  return `${prefix}-${String(next).padStart(3, '0')}`
}

function InputField({ label, name, placeholder, type = 'text' }: {
  label: string
  name: string
  placeholder?: string
  type?: string
}) {
  return (
    <label className="industrial-field">
      <span>{label}</span>
      <input name={name} type={type} placeholder={placeholder} />
    </label>
  )
}

function SelectField({ label, name, options }: {
  label: string
  name: string
  options: string[]
}) {
  return (
    <label className="industrial-field">
      <span>{label}</span>
      <select name={name} defaultValue={options[0]}>
        {options.map((option) => <option key={option}>{option}</option>)}
      </select>
    </label>
  )
}

function PanelHeading({ title, detail, action }: {
  title: string
  detail?: string
  action?: ReactNode
}) {
  return (
    <div className="industrial-panel-heading">
      <div><h2>{title}</h2>{detail && <p>{detail}</p>}</div>
      {action}
    </div>
  )
}

export default function IndustrialOperations({ section, onNavigate }: {
  section: IndustrialSection
  onNavigate: (label: string) => void
}) {
  const [data, setData] = useState<IndustrialData>(loadData)
  const [notice, setNotice] = useState('')
  const [storageError, setStorageError] = useState('')

  const commit = (update: (current: IndustrialData) => IndustrialData) => {
    const next = update(data)
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
      setData(next)
      setStorageError('')
    } catch (error) {
      setStorageError(`Could not save local operations data: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  const announce = (message: string) => {
    setNotice(message)
    window.setTimeout(() => setNotice(''), 2600)
  }

  const submitRecord = (
    event: FormEvent<HTMLFormElement>,
    create: (form: FormData) => void,
  ) => {
    event.preventDefault()
    create(new FormData(event.currentTarget))
    event.currentTarget.reset()
  }

  const alertCount = data.sensors.filter((sensor) => sensor.value > sensor.threshold).length
    + data.assets.filter((asset) => asset.health < 70 && asset.maintenance !== 'Scheduled').length

  return (
    <div className="industrial-shell">
      <header className="industrial-header">
        <div><span>INDUSTRIAL OPERATIONS</span><h1>{section}</h1></div>
        <span className="industrial-simulator"><i /> LOCAL SIMULATOR · NO FIELD CONNECTION</span>
      </header>
      <div className="industrial-disclaimer">
        <ShieldCheck size={16} />
        <span>This workspace runs in local simulation mode. It does not send commands to PLC/SCADA systems, drones, or physical robots.</span>
      </div>
      {storageError && <div className="industrial-error" role="alert">{storageError}</div>}
      {notice && <div className="industrial-notice" role="status"><CheckCircle2 size={15} />{notice}</div>}

      {section === 'Enterprise Operations Command Center' ? (
        <CommandCenter data={data} alertCount={alertCount} onNavigate={onNavigate} />
      ) : section === 'Robotics Fleet Management' ? (
        <RobotFleet data={data} commit={commit} announce={announce} />
      ) : section === 'Industrial OT Integration' ? (
        <OtIntegration data={data} commit={commit} announce={announce} submitRecord={submitRecord} />
      ) : section === 'IoT & Edge Gateway' ? (
        <SensorMonitor data={data} commit={commit} announce={announce} />
      ) : section === 'Robotic Process Control' ? (
        <RoboticProcessControl data={data} commit={commit} announce={announce} />
      ) : section === 'Drone & Inspection Management' ? (
        <DroneInspections data={data} commit={commit} announce={announce} submitRecord={submitRecord} />
      ) : section === 'Fleet & Logistics Automation' ? (
        <Logistics data={data} commit={commit} announce={announce} submitRecord={submitRecord} />
      ) : (
        <Maintenance data={data} commit={commit} announce={announce} submitRecord={submitRecord} />
      )}
    </div>
  )
}

function CommandCenter({ data, alertCount, onNavigate }: {
  data: IndustrialData
  alertCount: number
  onNavigate: (label: string) => void
}) {
  const metrics = [
    ['Robots', data.robots.length, Cpu],
    ['OT connectors', data.connectors.length, Radio],
    ['Sensor points', data.sensors.length, Activity],
    ['Open alerts', alertCount, AlertTriangle],
  ] as const

  return (
    <div className="industrial-command">
      <section className="industrial-metrics">
        {metrics.map(([label, value, Icon]) => (
          <article key={label}><Icon size={18} /><div><span>{label}</span><strong>{value}</strong><small>Local workspace</small></div></article>
        ))}
      </section>

      <section className="industrial-architecture">
        <PanelHeading title="End-to-end operations architecture" detail="System-wide control and data flow" />
        <div className="industrial-flow">
          {architecture.map((node, index) => (
            <div className="industrial-flow-step" key={node.title}>
              <button className={`industrial-flow-node ${node.tone}`} onClick={() => onNavigate(node.target)}>
                <strong>{node.title}</strong><span>{node.subtitle}</span>
              </button>
              {index < architecture.length - 1 && <span className="industrial-flow-arrow" aria-hidden="true">↓</span>}
            </div>
          ))}
        </div>
      </section>

      <section className="industrial-capability-section">
        <PanelHeading title="Industrial capabilities" detail="Manage local data and simulation workflows within each selected module." />
        <div className="industrial-capability-grid">
          {capabilities.map(({ name, description }) => (
            <button key={name} onClick={() => onNavigate(name)}>
              <span><Factory size={17} /></span>
              <strong>{name}</strong>
              <small>{description}</small>
              <ChevronRight size={15} />
            </button>
          ))}
        </div>
      </section>

      <div className="industrial-sample-note"><AlertTriangle size={15} /> Dashboard counts are local workspace records, not live factory telemetry.</div>
    </div>
  )
}

function RobotFleet({ data, commit, announce }: {
  data: IndustrialData
  commit: (update: (current: IndustrialData) => IndustrialData) => void
  announce: (message: string) => void
}) {
  const addRobot = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    const name = String(form.get('name') || '').trim()
    if (!name) return
    const robot: Robot = {
      id: nextId('BOT', data.robots),
      name,
      kind: String(form.get('kind')),
      route: String(form.get('route') || 'Unassigned'),
      task: 'Standby',
      battery: 100,
      status: 'Idle',
    }
    commit((current) => ({ ...current, robots: [...current.robots, robot] }))
    event.currentTarget.reset()
    announce(`${robot.name} added to the local fleet`)
  }

  const updateRobot = (id: string, update: (robot: Robot) => Robot, message: string) => {
    commit((current) => ({
      ...current,
      robots: current.robots.map((robot) => robot.id === id ? update(robot) : robot),
    }))
    announce(message)
  }

  return (
    <div className="industrial-page">
      <section className="industrial-panel">
        <PanelHeading title="AMR / AGV fleet" detail="Task assignment, route state and battery levels · simulator data only" />
        <form className="industrial-form" onSubmit={addRobot}>
          <InputField label="Robot name" name="name" placeholder="e.g. Warehouse AMR 04" />
          <SelectField label="Robot type" name="kind" options={['AMR', 'AGV']} />
          <InputField label="Route / zone" name="route" placeholder="A1 → B3" />
          <button className="industrial-primary" type="submit"><Plus size={14} /> Add robot</button>
        </form>
        <div className="industrial-table">
          <div className="industrial-row industrial-table-head"><span>Robot</span><span>Route / task</span><span>Battery</span><span>Status</span><span>Local controls</span></div>
          {data.robots.map((robot) => (
            <div className="industrial-row" key={robot.id}>
              <strong>{robot.name}<small>{robot.id} · {robot.kind}</small></strong>
              <span>{robot.route}<small>{robot.task}</small></span>
              <div className="industrial-battery"><i><b style={{ width: `${robot.battery}%` }} /></i><small>{robot.battery}%</small></div>
              <StatusPill status={robot.status} />
              <div className="industrial-row-actions">
                <button onClick={() => updateRobot(robot.id, (item) => ({
                  ...item,
                  status: item.status === 'Running' ? 'Idle' : 'Running',
                  task: item.status === 'Running' ? 'Standby' : 'Transfer task (simulated)',
                }), 'Robot task state updated in the simulator')}>{robot.status === 'Running' ? 'Pause' : 'Assign task'}</button>
                <button onClick={() => updateRobot(robot.id, (item) => ({ ...item, battery: Math.min(100, item.battery + 10), status: 'Charging' }), 'Battery level updated in the simulator')}>Charge +10%</button>
                <button className="industrial-danger-button" onClick={() => updateRobot(robot.id, (item) => ({ ...item, status: 'Stopped', task: 'Stopped' }), 'Robot stopped in the simulator')} title="Simulated stop"><X size={13} /></button>
              </div>
            </div>
          ))}
          {data.robots.length === 0 && <EmptyState text="No robots registered. Add a simulator robot above." />}
        </div>
      </section>
    </div>
  )
}

function OtIntegration({ data, commit, announce, submitRecord }: {
  data: IndustrialData
  commit: (update: (current: IndustrialData) => IndustrialData) => void
  announce: (message: string) => void
  submitRecord: (event: FormEvent<HTMLFormElement>, create: (form: FormData) => void) => void
}) {
  const addConnector = (form: FormData) => {
    const name = String(form.get('name') || '').trim()
    const endpoint = String(form.get('endpoint') || '').trim()
    if (!name || !endpoint) return
    const connector: Connector = {
      id: nextId('OT', data.connectors),
      name,
      protocol: String(form.get('protocol')),
      endpoint,
      status: 'Draft',
    }
    commit((current) => ({ ...current, connectors: [...current.connectors, connector] }))
    announce(`${connector.name} saved as a local connector profile`)
  }

  return (
    <div className="industrial-page">
      <section className="industrial-panel">
        <PanelHeading title="Industrial OT connectors" detail="Profiles for PLC, SCADA, OPC UA, Modbus and MQTT · no network session is opened" />
        <form className="industrial-form" onSubmit={(event) => submitRecord(event, addConnector)}>
          <InputField label="Connector name" name="name" placeholder="Line 01 controller" />
          <SelectField label="Protocol" name="protocol" options={['OPC UA', 'Modbus TCP', 'MQTT', 'PLC / SCADA gateway']} />
          <InputField label="Endpoint" name="endpoint" placeholder="opc.tcp://gateway.local:4840" />
          <button className="industrial-primary" type="submit"><Plus size={14} /> Save profile</button>
        </form>
        <div className="industrial-connector-list">
          {data.connectors.map((connector) => (
            <article key={connector.id}>
              <div className="industrial-icon-box"><Radio size={18} /></div>
              <div><strong>{connector.name}</strong><small>{connector.protocol} · {connector.endpoint}</small></div>
              <StatusPill status={connector.status} />
              <button onClick={() => {
                commit((current) => ({ ...current, connectors: current.connectors.map((item) => item.id === connector.id ? { ...item, status: 'Simulated OK' } : item) }))
                announce(`${connector.name}: simulated handshake passed; no device was contacted`)
              }}>Test in simulator</button>
            </article>
          ))}
          {data.connectors.length === 0 && <EmptyState text="No connector profiles. Add a local profile to document your intended OT interface." />}
        </div>
      </section>
      <section className="industrial-panel industrial-protocol-note">
        <ShieldCheck size={18} /><p>Production protocol access requires an approved gateway, network allowlist, read-only credentials and a safety review. This build stores configuration only.</p>
      </section>
    </div>
  )
}

function SensorMonitor({ data, commit, announce }: {
  data: IndustrialData
  commit: (update: (current: IndustrialData) => IndustrialData) => void
  announce: (message: string) => void
}) {
  const updateSamples = () => {
    commit((current) => ({
      ...current,
      sensors: current.sensors.map((sensor, index) => ({
        ...sensor,
        value: Number((sensor.value + (index % 2 === 0 ? 0.4 : -0.2)).toFixed(2)),
      })),
    }))
    announce('Sample telemetry values advanced; no physical sensor was queried')
  }

  return (
    <div className="industrial-page">
      <section className="industrial-panel">
        <PanelHeading
          title="IoT & Edge telemetry"
          detail="Temperature · pressure · vibration · tank level · energy consumption"
          action={<button className="industrial-secondary" onClick={updateSamples}><Activity size={14} /> Advance sample data</button>}
        />
        <div className="industrial-sensor-grid">
          {data.sensors.map((sensor) => {
            const alarm = sensor.value > sensor.threshold
            return (
              <article key={sensor.id} className={alarm ? 'alarm' : ''}>
                <div><span>{sensor.kind}</span><StatusPill status={alarm ? 'Threshold alert' : 'Sample'}/></div>
                <strong>{sensor.value}<small>{sensor.unit}</small></strong>
                <span>{sensor.name}</span>
                <div className="industrial-threshold"><i><b style={{ width: `${Math.min(100, sensor.value / sensor.threshold * 100)}%` }} /></i><small>Threshold {sensor.threshold}{sensor.unit}</small></div>
              </article>
            )
          })}
        </div>
      </section>
      <section className="industrial-panel industrial-protocol-note">
        <Database size={18} /><p>Displayed readings are seeded sample values kept in this browser. Live edge ingestion and alert delivery are not configured.</p>
      </section>
    </div>
  )
}

function RoboticProcessControl({ data, commit, announce }: {
  data: IndustrialData
  commit: (update: (current: IndustrialData) => IndustrialData) => void
  announce: (message: string) => void
}) {
  return (
    <div className="industrial-page">
      <section className="industrial-panel">
        <PanelHeading title="Robot workcells" detail="Packaging · palletizing · pick-and-place · simulation only" />
        <div className="industrial-workcell-grid">
          {data.workcells.map((cell) => (
            <article key={cell.id}>
              <div className="industrial-workcell-top"><Cpu size={19} /><StatusPill status={cell.status} /></div>
              <strong>{cell.name}</strong><span>{cell.process}</span>
              <label className="industrial-interlock"><input type="checkbox" checked={cell.safetyEnabled} onChange={(event) => commit((current) => ({
                ...current,
                workcells: current.workcells.map((item) => item.id === cell.id ? { ...item, safetyEnabled: event.target.checked } : item),
              }))} /> Safety interlock enabled</label>
              <div className="industrial-row-actions">
                <button className="industrial-primary" disabled={!cell.safetyEnabled} onClick={() => {
                  if (!cell.safetyEnabled) return
                  commit((current) => ({ ...current, workcells: current.workcells.map((item) => item.id === cell.id ? { ...item, status: 'Running (simulated)' } : item) }))
                  announce(`${cell.process} cycle simulated; no physical equipment was activated`)
                }}>Run simulated cycle</button>
                <button className="industrial-danger-button" onClick={() => {
                  commit((current) => ({ ...current, workcells: current.workcells.map((item) => item.id === cell.id ? { ...item, status: 'Stopped' } : item) }))
                  announce(`${cell.name} placed in simulated safe-stop state`)
                }}>Stop</button>
              </div>
            </article>
          ))}
        </div>
      </section>
      <section className="industrial-safety-note"><ShieldCheck size={18} /><div><strong>Safety boundary</strong><span>These controls only update local simulation state. Real robot motion requires vendor safety PLC, E-stop, guarded cells, risk assessment and commissioning.</span></div></section>
    </div>
  )
}

function DroneInspections({ data, commit, announce, submitRecord }: {
  data: IndustrialData
  commit: (update: (current: IndustrialData) => IndustrialData) => void
  announce: (message: string) => void
  submitRecord: (event: FormEvent<HTMLFormElement>, create: (form: FormData) => void) => void
}) {
  const createMission = (form: FormData) => {
    const site = String(form.get('site') || '').trim()
    if (!site) return
    const mission: Inspection = {
      id: nextId('DRONE', data.inspections),
      site,
      type: String(form.get('type')),
      status: 'Queued',
    }
    commit((current) => ({ ...current, inspections: [...current.inspections, mission] }))
    announce(`${mission.id} queued for local planning`)
  }

  return (
    <div className="industrial-page">
      <section className="industrial-panel">
        <PanelHeading title="Drone inspection missions" detail="Construction surveys · stockpile measurement · infrastructure inspection" />
        <form className="industrial-form" onSubmit={(event) => submitRecord(event, createMission)}>
          <InputField label="Site / asset" name="site" placeholder="North bridge, sector 4" />
          <SelectField label="Inspection type" name="type" options={['Construction survey', 'Stockpile measurement', 'Infrastructure inspection']} />
          <button className="industrial-primary" type="submit"><Plus size={14} /> Plan mission</button>
        </form>
        <div className="industrial-list">
          {data.inspections.map((mission) => (
            <article key={mission.id}><span className="industrial-icon-box"><Plane size={18} /></span><div><strong>{mission.site}</strong><small>{mission.id} · {mission.type}</small></div><StatusPill status={mission.status} /><button disabled={mission.status !== 'Queued'} onClick={() => {
              commit((current) => ({ ...current, inspections: current.inspections.map((item) => item.id === mission.id ? { ...item, status: 'Completed (simulated)' } : item) }))
              announce('Inspection marked complete in the simulator; no drone was dispatched')
            }}>Simulate completion</button></article>
          ))}
          {data.inspections.length === 0 && <EmptyState text="No inspection missions planned." />}
        </div>
      </section>
    </div>
  )
}

function Logistics({ data, commit, announce, submitRecord }: {
  data: IndustrialData
  commit: (update: (current: IndustrialData) => IndustrialData) => void
  announce: (message: string) => void
  submitRecord: (event: FormEvent<HTMLFormElement>, create: (form: FormData) => void) => void
}) {
  const createDelivery = (form: FormData) => {
    const origin = String(form.get('origin') || '').trim()
    const destination = String(form.get('destination') || '').trim()
    if (!origin || !destination) return
    const delivery: Delivery = {
      id: nextId('SHIP', data.deliveries),
      origin,
      destination,
      load: String(form.get('load') || '').trim() || 'General cargo',
      status: 'Queued',
    }
    commit((current) => ({ ...current, deliveries: [...current.deliveries, delivery] }))
    announce(`${delivery.id} added to the local dispatch queue`)
  }

  const setDeliveryStatus = (delivery: Delivery, status: Delivery['status']) => {
    commit((current) => ({ ...current, deliveries: current.deliveries.map((item) => item.id === delivery.id ? { ...item, status } : item) }))
    announce(`${delivery.id}: ${status}`)
  }

  return (
    <div className="industrial-page">
      <section className="industrial-panel">
        <PanelHeading title="Fleet & logistics dispatch" detail="Truck tracking · route planning · delivery verification · warehouse hand-off" />
        <form className="industrial-form" onSubmit={(event) => submitRecord(event, createDelivery)}>
          <InputField label="Origin" name="origin" placeholder="Warehouse A" />
          <InputField label="Destination" name="destination" placeholder="Distribution hub B" />
          <InputField label="Load" name="load" placeholder="Pallets / order reference" />
          <button className="industrial-primary" type="submit"><Plus size={14} /> Add dispatch</button>
        </form>
        <div className="industrial-list">
          {data.deliveries.map((delivery) => (
            <article key={delivery.id}><span className="industrial-icon-box"><Truck size={18} /></span><div><strong>{delivery.origin} → {delivery.destination}</strong><small>{delivery.id} · {delivery.load}</small></div><StatusPill status={delivery.status} /><div className="industrial-row-actions">
              {delivery.status === 'Queued' && <button onClick={() => setDeliveryStatus(delivery, 'Optimized')}>Plan route</button>}
              {delivery.status === 'Optimized' && <button onClick={() => setDeliveryStatus(delivery, 'Dispatched (simulated)')}>Dispatch (sim.)</button>}
              {delivery.status === 'Dispatched (simulated)' && <button onClick={() => setDeliveryStatus(delivery, 'Verified (simulated)')}>Verify delivery</button>}
            </div></article>
          ))}
          {data.deliveries.length === 0 && <EmptyState text="No shipments. Add a dispatch to build a local logistics queue." />}
        </div>
      </section>
    </div>
  )
}

function Maintenance({ data, commit, announce, submitRecord }: {
  data: IndustrialData
  commit: (update: (current: IndustrialData) => IndustrialData) => void
  announce: (message: string) => void
  submitRecord: (event: FormEvent<HTMLFormElement>, create: (form: FormData) => void) => void
}) {
  const addAsset = (form: FormData) => {
    const name = String(form.get('name') || '').trim()
    if (!name) return
    const asset: PlantAsset = {
      id: nextId('ASSET', data.assets),
      name,
      area: String(form.get('area') || '').trim() || 'Unassigned',
      health: 100,
      maintenance: 'No schedule',
    }
    commit((current) => ({ ...current, assets: [...current.assets, asset] }))
    announce(`${asset.name} added to the local maintenance register`)
  }

  return (
    <div className="industrial-page">
      <section className="industrial-panel">
        <PanelHeading title="Asset health & maintenance" detail="Condition indicators and planned maintenance · predictions are sample heuristics" />
        <form className="industrial-form" onSubmit={(event) => submitRecord(event, addAsset)}>
          <InputField label="Asset name" name="name" placeholder="Pump D" />
          <InputField label="Area" name="area" placeholder="Utilities" />
          <button className="industrial-primary" type="submit"><Plus size={14} /> Register asset</button>
        </form>
        <div className="industrial-list">
          {data.assets.map((asset) => {
            const risk = asset.health < 70 && asset.maintenance !== 'Scheduled'
            return (
              <article key={asset.id}><span className="industrial-icon-box"><Wrench size={18} /></span><div><strong>{asset.name}</strong><small>{asset.id} · {asset.area}</small></div><div className="industrial-health"><Gauge size={15} /><strong>{asset.health}%</strong><small>sample health</small></div><StatusPill status={asset.maintenance === 'Scheduled' ? 'Scheduled' : risk ? 'Review advised' : 'Monitoring'} /><button disabled={asset.maintenance === 'Scheduled'} onClick={() => {
                commit((current) => ({ ...current, assets: current.assets.map((item) => item.id === asset.id ? { ...item, maintenance: 'Scheduled' } : item) }))
                announce(`${asset.name}: maintenance scheduled locally`)
              }}>Schedule service</button></article>
            )
          })}
        </div>
      </section>
      <section className="industrial-panel industrial-protocol-note"><Activity size={18} /><p>Health percentages are sample indicators, not predictions from real vibration, temperature or PLC history.</p></section>
    </div>
  )
}

function StatusPill({ status }: { status: string }) {
  const alert = /alert|stopped|review/i.test(status)
  return <span className={`industrial-status ${alert ? 'warning' : ''}`}>{status}</span>
}

function EmptyState({ text }: { text: string }) {
  return <div className="industrial-empty"><Boxes size={18} /><span>{text}</span></div>
}
