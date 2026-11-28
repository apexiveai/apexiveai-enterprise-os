import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react'
import { apiUrl } from '../../lib/api'
import {
  ArrowRight, Bot, CalendarDays, Check, CircleAlert, ClipboardList,
  LoaderCircle, MapPin, PackageCheck, Plus, RefreshCw,
} from 'lucide-react'
import type { IndustrySolutionKey, IndustrySolutionProduct } from './industrySolutions'

type RecordStatus = 'open' | 'in_progress' | 'completed' | 'cancelled'

type IndustryRecord = {
  id: string
  tenant_id: string
  solution_key: IndustrySolutionKey
  title: string
  status: RecordStatus
  payload: Record<string, string>
  created_by: string
  created_at: string
  updated_at: string
}

const localActorId = 'local-workspace-user'

const statusLabels: Record<RecordStatus, string> = {
  open: 'Open',
  in_progress: 'In progress',
  completed: 'Completed',
  cancelled: 'Cancelled',
}

function isRecordStatus(value: string): value is RecordStatus {
  return Object.prototype.hasOwnProperty.call(statusLabels, value)
}

async function errorMessage(response: Response): Promise<string> {
  try {
    const body = await response.json() as { detail?: unknown }
    if (typeof body.detail === 'string') return body.detail
    if (Array.isArray(body.detail)) {
      const messages = body.detail
        .map((item) => item && typeof item === 'object' && 'msg' in item ? item.msg : null)
        .filter((message): message is string => typeof message === 'string')
      if (messages.length) return messages.join(' ')
    }
  } catch {
    // Use the HTTP status when the server does not return a JSON error body.
  }
  return response.statusText || `Request failed (${response.status}).`
}

export default function IndustrySolutionsWorkspace({
  solution,
}: {
  solution: IndustrySolutionProduct
}) {
  const tenantId = import.meta.env.VITE_TENANT_ID || 'local-workspace'
  const [records, setRecords] = useState<IndustryRecord[]>([])
  const [statusFilter, setStatusFilter] = useState<'all' | RecordStatus>('all')
  const [formOpen, setFormOpen] = useState(false)
  const [title, setTitle] = useState('')
  const [values, setValues] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const recordsUrl = `/api/v1/industry-solutions/${solution.key}/records`

  const fetchRecords = useCallback(async () => {
    const query = new URLSearchParams({ tenant_id: tenantId, limit: '500' })
    const response = await fetch(apiUrl(`${recordsUrl}?${query}`))
    if (!response.ok) throw new Error(await errorMessage(response))
    return await response.json() as IndustryRecord[]
  }, [recordsUrl, tenantId])

  useEffect(() => {
    let active = true
    const loadRecords = async () => {
      try {
        const savedRecords = await fetchRecords()
        if (active) {
          setRecords(savedRecords)
          setError('')
        }
      } catch (requestError) {
        if (active) setError(requestError instanceof Error ? requestError.message : 'Could not load workspace records.')
      } finally {
        if (active) setLoading(false)
      }
    }
    void loadRecords()
    return () => { active = false }
  }, [fetchRecords])

  const totals = useMemo(() => ({
    open: records.filter((record) => record.status === 'open').length,
    inProgress: records.filter((record) => record.status === 'in_progress').length,
    completed: records.filter((record) => record.status === 'completed').length,
  }), [records])
  const visibleRecords = statusFilter === 'all'
    ? records
    : records.filter((record) => record.status === statusFilter)

  const refreshRecords = () => {
    setLoading(true)
    void fetchRecords()
      .then((savedRecords) => {
        setRecords(savedRecords)
        setError('')
      })
      .catch((requestError: unknown) => {
        setError(requestError instanceof Error ? requestError.message : 'Could not load workspace records.')
      })
      .finally(() => setLoading(false))
  }

  const openForm = () => {
    setTitle('')
    setValues({})
    setError('')
    setFormOpen(true)
  }

  const createRecord = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      const response = await fetch(apiUrl(recordsUrl), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          actor_id: localActorId,
          title: title.trim(),
          payload: values,
        }),
      })
      if (!response.ok) throw new Error(await errorMessage(response))
      const created = await response.json() as IndustryRecord
      setRecords((current) => [created, ...current])
      setFormOpen(false)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Could not save this record.')
    } finally {
      setSaving(false)
    }
  }

  const updateStatus = async (record: IndustryRecord, nextStatus: RecordStatus) => {
    setError('')
    try {
      const response = await fetch(apiUrl(`${recordsUrl}/${record.id}`), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          actor_id: localActorId,
          status: nextStatus,
        }),
      })
      if (!response.ok) throw new Error(await errorMessage(response))
      const updated = await response.json() as IndustryRecord
      setRecords((current) => current.map((item) => item.id === updated.id ? updated : item))
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Could not update record status.')
    }
  }

  const Icon = solution.icon

  return (
    <div className="industry-workspace">
      <header className="industry-workspace-hero">
        <div className="industry-workspace-title">
          <span className="industry-solution-icon"><Icon size={22} /></span>
          <div>
            <p>APEXIVE AI · INDUSTRY SOLUTION</p>
            <h1>{solution.label}</h1>
            <span>{solution.description}</span>
          </div>
        </div>
        <div className="industry-mode-badges">
          <span><Check size={13} /> Standalone work queue</span>
          <span><CircleAlert size={13} /> External connectors not configured</span>
        </div>
      </header>

      <section className="industry-workspace-overview">
        <article><span>Open</span><strong>{totals.open}</strong></article>
        <article><span>In progress</span><strong>{totals.inProgress}</strong></article>
        <article><span>Completed</span><strong>{totals.completed}</strong></article>
        <article className="industry-connectivity-card">
          <span>Data persistence</span>
          <strong>Application database</strong>
          <small>Records are tenant-scoped and audit logged.</small>
        </article>
      </section>

      <section className="industry-workspace-grid">
        <article className="industry-workflow-panel">
          <div className="industry-section-heading">
            <div><small>OPERATING MODEL</small><h2>Workflows included</h2></div>
            <Bot size={18} />
          </div>
          <ol>
            {solution.workflows.map((workflow, index) => (
              <li key={workflow}><span>{index + 1}</span>{workflow}<ArrowRight size={14} /></li>
            ))}
          </ol>
          <div className="industry-setup-note">
            <strong>Before live automation</strong>
            <span>Connect and validate vendor systems, credentials, AI model access, permissions, and approval rules before automation. This workspace currently supports manual record entry and status tracking; it does not execute AI actions or live integrations.</span>
          </div>
        </article>

        <section className="industry-records-panel">
          <div className="industry-records-heading">
            <div>
              <small>OPERATIONS QUEUE</small>
              <h2>Work queue</h2>
            </div>
            <button type="button" className="industry-primary-button" onClick={openForm}>
              <Plus size={15} /> New record
            </button>
          </div>
          <div className="industry-record-filters">
            {(['all', 'open', 'in_progress', 'completed', 'cancelled'] as const).map((filter) => (
              <button
                type="button"
                key={filter}
                className={statusFilter === filter ? 'active' : ''}
                onClick={() => setStatusFilter(filter)}
              >
                {filter === 'all' ? 'All' : statusLabels[filter]}
              </button>
            ))}
            <button type="button" className="industry-refresh-button" onClick={refreshRecords} title="Refresh records">
              <RefreshCw size={14} />
            </button>
          </div>
          {error && <div className="industry-inline-error" role="alert"><CircleAlert size={15} />{error}</div>}
          {loading ? (
            <div className="industry-empty-state"><LoaderCircle size={20} className="industry-spinner" /><span>Loading saved records…</span></div>
          ) : visibleRecords.length === 0 ? (
            <div className="industry-empty-state">
              <ClipboardList size={23} />
              <strong>{statusFilter === 'all' || records.length === 0 ? 'No records yet' : `No ${statusLabels[statusFilter].toLowerCase()} records`}</strong>
              <span>{records.length === 0 ? 'Start with a verified work item. No sample business data is preloaded.' : 'Change the status filter or add a new work item.'}</span>
              {records.length === 0 && <button type="button" onClick={openForm}>Create the first record</button>}
            </div>
          ) : (
            <div className="industry-record-list">
              {visibleRecords.map((record) => (
                <article className="industry-record-card" key={record.id}>
                  <div className="industry-record-card-title">
                    <div><strong>{record.title}</strong><small>Updated {new Date(record.updated_at).toLocaleString()}</small></div>
                    <label className={`industry-record-status status-${record.status}`}>
                      <span>{statusLabels[record.status]}</span>
                      <select
                        aria-label={`Update status for ${record.title}`}
                        value={record.status}
                        onChange={(event) => {
                          const nextStatus = event.target.value
                          if (isRecordStatus(nextStatus)) void updateStatus(record, nextStatus)
                        }}
                      >
                        {Object.entries(statusLabels).map(([value, label]) => (
                          <option key={value} value={value}>{label}</option>
                        ))}
                      </select>
                    </label>
                  </div>
                  <div className="industry-record-fields">
                    {solution.fields.map((field) => (
                      <span key={field.key}>
                        {field.type === 'date' ? <CalendarDays size={12} /> : field.key === 'site' || field.key === 'origin' || field.key === 'destination' ? <MapPin size={12} /> : <PackageCheck size={12} />}
                        <b>{field.label}:</b> {record.payload[field.key]}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </section>

      {formOpen && (
        <div className="industry-modal-backdrop" role="presentation">
          <form className="industry-record-form" onSubmit={(event) => void createRecord(event)}>
            <div className="industry-records-heading">
              <div><small>NEW WORK ITEM</small><h2>Create {solution.titleLabel.toLowerCase()}</h2></div>
              <button type="button" onClick={() => setFormOpen(false)} aria-label="Close form">×</button>
            </div>
            <label>
              {solution.titleLabel}
              <input value={title} onChange={(event) => setTitle(event.target.value)} maxLength={250} required />
            </label>
            {solution.fields.map((field) => (
              <label key={field.key}>
                {field.label}
                <input
                  type={field.type || 'text'}
                  step={field.type === 'number' ? 'any' : undefined}
                  value={values[field.key] || ''}
                  onChange={(event) => setValues((current) => ({ ...current, [field.key]: event.target.value }))}
                  maxLength={1000}
                  required
                />
              </label>
            ))}
            {error && <div className="industry-inline-error" role="alert"><CircleAlert size={15} />{error}</div>}
            <div className="industry-form-actions">
              <button type="button" onClick={() => setFormOpen(false)}>Cancel</button>
              <button type="submit" className="industry-primary-button" disabled={saving}>
                {saving ? <LoaderCircle size={14} className="industry-spinner" /> : <Plus size={14} />}
                Save record
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
