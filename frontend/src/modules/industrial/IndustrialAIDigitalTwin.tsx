import { useState } from 'react'
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  Boxes,
  CheckCircle2,
  ChevronDown,
  Cpu,
  Database,
  Factory,
  Gauge,
  Plane,
  Radio,
  Truck,
} from 'lucide-react'

const sites = ['Factory Alpha', 'Construction Site North', 'Logistics Hub East']

const capabilities = [
  { title: 'IoT Sensor Monitoring', detail: 'Track live equipment telemetry and threshold alerts.', icon: Radio, target: 'Industrial IoT / Edge Gateway' },
  { title: 'Predictive Maintenance', detail: 'Prioritize maintenance from asset health signals.', icon: Gauge, target: 'Asset Management' },
  { title: 'Digital Twin', detail: 'Explore a connected operational model of the site.', icon: Boxes, target: 'Digital Twin' },
  { title: 'Robot Fleet Management', detail: 'Coordinate robot status, routes, and assignments.', icon: Cpu, target: 'Robotics Fleet Management' },
  { title: 'Warehouse Automation', detail: 'Connect material movement and warehouse missions.', icon: Truck, target: 'AMR / AGV Fleet Integration' },
  { title: 'Smart Factory Analytics', detail: 'Review throughput, uptime, and operational trends.', icon: Activity, target: 'Reports & Analytics' },
  { title: 'Drone Inspection', detail: 'Manage inspection missions and findings.', icon: Plane, target: 'Drone / Inspection Integration' },
  { title: 'PLC / SCADA Integration', detail: 'Connect control data, alarms, and historian signals.', icon: Database, target: 'PLC / SCADA Integration' },
]

const sensorReadings = [
  { name: 'Line 01 temperature', value: '72.4', unit: '°C', health: 'Normal', level: 68 },
  { name: 'Press vibration', value: '3.2', unit: 'mm/s', health: 'Normal', level: 44 },
  { name: 'Compressor pressure', value: '7.8', unit: 'bar', health: 'Watch', level: 82 },
  { name: 'Energy load', value: '124', unit: 'kWh', health: 'Normal', level: 58 },
]

const assets = [
  { name: 'Hydraulic Press P-04', area: 'Production line', health: 62, due: 'Service recommended in 6 days' },
  { name: 'Conveyor Motor C-12', area: 'Packaging', health: 78, due: 'Bearing inspection in 14 days' },
  { name: 'Compressor A-02', area: 'Utilities', health: 91, due: 'No maintenance risk detected' },
]

export default function IndustrialAIDigitalTwin({ onNavigate }: { onNavigate: (label: string) => void }) {
  const [activeSite, setActiveSite] = useState(sites[0])

  return (
    <div className="industrial-ai-page">
      <header className="industrial-ai-header">
        <div>
          <span className="industrial-ai-eyebrow"><Factory size={13} /> INDUSTRIAL INTELLIGENCE</span>
          <h1>Industrial AI &amp; Digital Twin</h1>
          <p>Unify assets, sensors, robots, and site operations in one workspace.</p>
        </div>
        <div className="industrial-ai-controls">
          <label>
            <span>Workspace</span>
            <span className="industrial-ai-select-wrap">
              <select value={activeSite} onChange={(event) => setActiveSite(event.target.value)} aria-label="Select industrial workspace">
                {sites.map((site) => <option key={site}>{site}</option>)}
              </select>
              <ChevronDown size={13} />
            </span>
          </label>
          <span className="industrial-ai-simulated"><i /> SIMULATED DATA</span>
        </div>
      </header>

      <section className="industrial-ai-metrics" aria-label="Industrial operations overview">
        <article><span><Activity size={14} /> Connected Sensors</span><strong>248 <small>/ 256</small></strong><em>96.8% online</em></article>
        <article><span><Gauge size={14} /> Asset Health</span><strong>87<small>%</small></strong><em>3 assets need attention</em></article>
        <article><span><Cpu size={14} /> Robots Active</span><strong>18 <small>/ 21</small></strong><em>2 missions in progress</em></article>
        <article><span><AlertTriangle size={14} /> Open Alerts</span><strong>04</strong><em>1 high priority</em></article>
      </section>

      <div className="industrial-ai-overview">
        <section className="industrial-ai-panel industrial-ai-twin">
          <div className="industrial-ai-panel-heading">
            <div><h2>Digital Twin · {activeSite}</h2><p>Live operational map and equipment state</p></div>
            <button onClick={() => onNavigate('Digital Twin')}>Open Twin <ArrowUpRight size={13} /></button>
          </div>
          <div className="industrial-ai-twin-canvas">
            <div className="industrial-ai-map-grid" />
            <svg className="industrial-ai-connectors" viewBox="0 0 720 230" preserveAspectRatio="none" aria-hidden="true">
              <path d="M92 113 H225 M255 113 H385 M415 113 H545 M575 113 H660" />
              <path d="M255 113 V178 H385 M415 113 V58 H545" />
            </svg>
            <div className="industrial-ai-zone industrial-ai-zone-a">PRODUCTION</div>
            <div className="industrial-ai-zone industrial-ai-zone-b">WAREHOUSE</div>
            <div className="industrial-ai-equipment twin-sensor"><span><Radio size={15} /></span><strong>Sensor Hub</strong><small>32 signals · Normal</small></div>
            <div className="industrial-ai-equipment twin-machine"><span><Factory size={15} /></span><strong>Assembly Line</strong><small>Running · 92% OEE</small></div>
            <div className="industrial-ai-equipment twin-robot"><span><Cpu size={15} /></span><strong>Robot Cell 03</strong><small>Cycle active</small></div>
            <div className="industrial-ai-equipment twin-drone"><span><Plane size={15} /></span><strong>Inspection Drone</strong><small>Mission queued</small></div>
            <div className="industrial-ai-equipment twin-warehouse"><span><Truck size={15} /></span><strong>Warehouse AMR</strong><small>Route clear</small></div>
            <div className="industrial-ai-twin-legend"><span><i className="normal" /> Normal</span><span><i className="watch" /> Attention</span><span><i className="active" /> Active</span></div>
          </div>
        </section>

        <section className="industrial-ai-panel industrial-ai-maintenance">
          <div className="industrial-ai-panel-heading">
            <div><h2>Predictive Maintenance</h2><p>Asset condition and recommended actions</p></div>
            <Gauge size={15} />
          </div>
          <div className="industrial-ai-asset-list">
            {assets.map((asset) => (
              <article key={asset.name}>
                <div className="industrial-ai-asset-title"><span><strong>{asset.name}</strong><small>{asset.area}</small></span><b className={asset.health < 70 ? 'attention' : ''}>{asset.health}%</b></div>
                <div className="industrial-ai-health-track"><i style={{ width: `${asset.health}%` }} className={asset.health < 70 ? 'attention' : ''} /></div>
                <p>{asset.due}</p>
              </article>
            ))}
          </div>
          <button className="industrial-ai-text-action" onClick={() => onNavigate('Asset Management')}>View all assets <ArrowUpRight size={12} /></button>
        </section>
      </div>

      <section className="industrial-ai-panel industrial-ai-sensors">
        <div className="industrial-ai-panel-heading">
          <div><h2>IoT Sensor Monitoring</h2><p>Selected telemetry from {activeSite}</p></div>
          <button onClick={() => onNavigate('Industrial IoT / Edge Gateway')}>Open sensor workspace <ArrowUpRight size={13} /></button>
        </div>
        <div className="industrial-ai-sensor-grid">
          {sensorReadings.map((sensor) => (
            <article key={sensor.name}>
              <div><span>{sensor.name}</span><b className={sensor.health === 'Watch' ? 'attention' : ''}><i /> {sensor.health}</b></div>
              <strong>{sensor.value}<small>{sensor.unit}</small></strong>
              <div className="industrial-ai-sensor-track"><i style={{ width: `${sensor.level}%` }} className={sensor.health === 'Watch' ? 'attention' : ''} /></div>
            </article>
          ))}
        </div>
      </section>

      <section className="industrial-ai-capabilities">
        <div className="industrial-ai-section-heading">
          <div><h2>Industrial Operations</h2><p>Choose a capability to open its workspace.</p></div>
          <span>8 CAPABILITIES</span>
        </div>
        <div className="industrial-ai-capability-grid">
          {capabilities.map(({ title, detail, icon: Icon, target }) => (
            <button key={title} onClick={() => onNavigate(target)}>
              <span><Icon size={16} /></span>
              <div><strong>{title}</strong><small>{detail}</small></div>
              <ArrowUpRight size={13} />
            </button>
          ))}
        </div>
      </section>

      <div className="industrial-ai-footnote"><CheckCircle2 size={13} /> Operational values are sample data for this local workspace.</div>
    </div>
  )
}
