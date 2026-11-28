import { useState } from 'react'
import { apiUrl } from '../../lib/api'
import { Activity, CircleAlert, LoaderCircle, RefreshCw, TrendingUp } from 'lucide-react'

type ForecastResult = {
  series_name: string
  historical_count: number
  horizon: number
  trend_per_period: number
  forecast_values: number[]
  caveat: string
}

type ReconciliationResult = {
  matched_count: number
  exception_count: number
  rows: Array<{
    reference: string
    status: string
    statement_amount: string | null
    ledger_amount: string | null
    statement_currency: string | null
    ledger_currency: string | null
  }>
  totals_by_currency: Record<string, {
    statement_total: string
    ledger_total: string
    difference: string
  }>
}

type ProcessSummary = {
  process_id: string
  process_name: string
  run_count: number
  completed_runs: number
  failed_runs: number
  average_cycle_time_seconds: number | null
  median_cycle_time_seconds: number | null
  duration_sample_count: number
}

const demoStatement = JSON.stringify([
  { reference: 'INV-1001', amount: '1250.00', currency: 'USD' },
  { reference: 'INV-1002', amount: '840.50', currency: 'USD' },
], null, 2)

const demoLedger = JSON.stringify([
  { reference: 'INV-1001', amount: '1250.00', currency: 'USD' },
  { reference: 'INV-1002', amount: '804.50', currency: 'USD' },
], null, 2)

async function responseError(response: Response) {
  try {
    const body = await response.json() as { detail?: unknown }
    if (typeof body.detail === 'string') return body.detail
    if (Array.isArray(body.detail)) {
      const messages = body.detail
        .map((item) => item && typeof item === 'object' && 'msg' in item ? item.msg : null)
        .filter((message): message is string => typeof message === 'string')
      if (messages.length) return messages.join(' ')
    }
    return response.statusText || `Request failed (${response.status}).`
  } catch {
    return response.statusText || `Request failed (${response.status}).`
  }
}

export default function BusinessInsights() {
  const [activeTab, setActiveTab] = useState<'forecast' | 'reconciliation' | 'mining'>('forecast')
  const [tenantId, setTenantId] = useState(import.meta.env.VITE_TENANT_ID || 'local-workspace')
  const [seriesName, setSeriesName] = useState('Monthly revenue')
  const [history, setHistory] = useState('120, 128, 132, 145, 151, 160')
  const [horizon, setHorizon] = useState(3)
  const [forecast, setForecast] = useState<ForecastResult | null>(null)
  const [statement, setStatement] = useState(demoStatement)
  const [ledger, setLedger] = useState(demoLedger)
  const [reconciliation, setReconciliation] = useState<ReconciliationResult | null>(null)
  const [processes, setProcesses] = useState<ProcessSummary[]>([])
  const [working, setWorking] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  const request = async <T,>(url: string, init?: RequestInit): Promise<T> => {
    const response = await fetch(apiUrl(url), init)
    if (!response.ok) throw new Error(await responseError(response))
    return response.json() as Promise<T>
  }

  const runForecast = async () => {
    setWorking(true)
    setError('')
    setNotice('')
    try {
      const historicalValues = history.split(',').map((value) => Number(value.trim()))
      if (historicalValues.length < 3 || historicalValues.some((value) => !Number.isFinite(value))) {
        throw new Error('Enter at least three comma-separated finite numbers.')
      }
      const result = await request<ForecastResult>('/api/v1/insights/forecast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ series_name: seriesName, historical_values: historicalValues, horizon }),
      })
      setForecast(result)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Forecast request failed.')
    } finally {
      setWorking(false)
    }
  }

  const runReconciliation = async () => {
    setWorking(true)
    setError('')
    setNotice('')
    try {
      const statementRows = JSON.parse(statement) as unknown
      const ledgerRows = JSON.parse(ledger) as unknown
      const result = await request<ReconciliationResult>('/api/v1/insights/reconciliation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ statement: statementRows, ledger: ledgerRows }),
      })
      setReconciliation(result)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Reconciliation request failed.')
    } finally {
      setWorking(false)
    }
  }

  const loadProcessMining = async () => {
    if (!tenantId.trim()) return
    setWorking(true)
    setError('')
    setNotice('')
    try {
      const result = await request<ProcessSummary[]>(
        `/api/v1/insights/process-mining?tenant_id=${encodeURIComponent(tenantId)}`,
      )
      setProcesses(result)
      setNotice(`Loaded ${result.length} process summaries from recorded runs.`)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Process mining request failed.')
    } finally {
      setWorking(false)
    }
  }

  return (
    <div className="business-insights">
      <header className="business-insights-header">
        <div>
          <span>APEXIVE INTELLIGENCE · BUSINESS INSIGHTS</span>
          <h1>Business Intelligence</h1>
          <p>Forecast supplied data, reconcile financial entries, and analyze persisted process runs.</p>
        </div>
        <label>Tenant ID
          <input value={tenantId} onChange={(event) => setTenantId(event.target.value)} />
        </label>
      </header>

      <nav className="business-insights-tabs" aria-label="Business intelligence tools">
        <button className={activeTab === 'forecast' ? 'active' : ''} onClick={() => setActiveTab('forecast')}>
          <TrendingUp size={15} /> Predictive Analytics
        </button>
        <button className={activeTab === 'reconciliation' ? 'active' : ''} onClick={() => setActiveTab('reconciliation')}>
          <RefreshCw size={15} /> Automated Reconciliation
        </button>
        <button className={activeTab === 'mining' ? 'active' : ''} onClick={() => setActiveTab('mining')}>
          <Activity size={15} /> Process Mining
        </button>
      </nav>

      {error && <div className="business-insights-message error" role="alert"><CircleAlert size={14} />{error}</div>}
      {notice && <div className="business-insights-message success" role="status">{notice}</div>}

      {activeTab === 'forecast' && (
        <section className="business-insights-panel">
          <div className="business-insights-panel-heading">
            <div><h2>Trend forecast</h2><p>Linear trend extrapolation based only on the values you provide.</p></div>
            <span>ESTIMATE · NOT A GUARANTEE</span>
          </div>
          <label>Series name<input value={seriesName} onChange={(event) => setSeriesName(event.target.value)} maxLength={100} /></label>
          <label>Historical values, oldest first<input value={history} onChange={(event) => setHistory(event.target.value)} placeholder="120, 128, 132, 145" /></label>
          <label>Periods to forecast<input type="number" min="1" max="24" value={horizon} onChange={(event) => setHorizon(Number(event.target.value))} /></label>
          <button disabled={working} onClick={() => void runForecast()}>
            {working ? <LoaderCircle className="business-insights-spinner" size={14} /> : <TrendingUp size={14} />}
            Calculate trend
          </button>
          {forecast && (
            <div className="business-insights-result">
              <strong>{forecast.series_name} · {forecast.horizon} period estimate</strong>
              <div className="business-insights-values">{forecast.forecast_values.map((value, index) => <span key={index}><small>Period {index + 1}</small>{value}</span>)}</div>
              <p>{forecast.caveat} Trend: {forecast.trend_per_period} per period.</p>
            </div>
          )}
        </section>
      )}

      {activeTab === 'reconciliation' && (
        <section className="business-insights-panel">
          <div className="business-insights-panel-heading">
            <div><h2>Statement ↔ ledger reconciliation</h2><p>Match unique references, amounts, and currencies. Duplicate references are flagged, not guessed.</p></div>
            <span>INPUT DATA ONLY</span>
          </div>
          <div className="business-insights-editors">
            <label>Bank statement rows (JSON)<textarea value={statement} onChange={(event) => setStatement(event.target.value)} spellCheck={false} /></label>
            <label>Ledger rows (JSON)<textarea value={ledger} onChange={(event) => setLedger(event.target.value)} spellCheck={false} /></label>
          </div>
          <button disabled={working} onClick={() => void runReconciliation()}>
            {working ? <LoaderCircle className="business-insights-spinner" size={14} /> : <RefreshCw size={14} />}
            Reconcile records
          </button>
          {reconciliation && (
            <div className="business-insights-result">
              <strong>{reconciliation.matched_count} matched · {reconciliation.exception_count} exceptions</strong>
              <div className="business-insights-table-wrap">
                <table><thead><tr><th>Reference</th><th>Status</th><th>Statement</th><th>Ledger</th></tr></thead>
                  <tbody>{reconciliation.rows.map((row) => (
                    <tr key={`${row.reference}-${row.status}`}>
                      <td>{row.reference}</td><td>{row.status.replaceAll('_', ' ')}</td>
                      <td>{row.statement_amount ?? '—'} {row.statement_currency}</td>
                      <td>{row.ledger_amount ?? '—'} {row.ledger_currency}</td>
                    </tr>
                  ))}</tbody>
                </table>
              </div>
            </div>
          )}
        </section>
      )}

      {activeTab === 'mining' && (
        <section className="business-insights-panel">
          <div className="business-insights-panel-heading">
            <div><h2>Business process performance</h2><p>Aggregates cycle time and outcomes from persisted process execution records.</p></div>
            <button disabled={working || !tenantId.trim()} onClick={() => void loadProcessMining()}>
              {working ? <LoaderCircle className="business-insights-spinner" size={14} /> : <RefreshCw size={14} />}
              Refresh
            </button>
          </div>
          <div className="business-insights-processes">
            {processes.map((process) => (
              <article key={process.process_id}>
                <div><strong>{process.process_name}</strong><small>{process.run_count} recorded runs · {process.duration_sample_count} duration samples</small></div>
                <span>Avg {process.average_cycle_time_seconds ?? '—'}s</span>
                <span>Median {process.median_cycle_time_seconds ?? '—'}s</span>
                <span>{process.completed_runs} completed · {process.failed_runs} failed</span>
              </article>
            ))}
            {!processes.length && <p>No recorded process runs are available for this tenant.</p>}
          </div>
        </section>
      )}
    </div>
  )
}
