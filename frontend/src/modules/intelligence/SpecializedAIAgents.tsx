import { useEffect, useMemo, useState, type FormEvent } from 'react'
import { apiUrl } from '../../lib/api'
import {
  Bot,
  CalendarDays,
  Check,
  ClipboardCheck,
  CircleAlert,
  LoaderCircle,
  Play,
  Search,
  ShieldCheck,
  Sparkles,
  Star,
} from 'lucide-react'

type AgentTemplate = {
  slug: string
  name: string
  responsibility: string
  job_description: string
  permissions: string[]
  kpis: string[]
  tasks: string[]
  guardrails: string[]
}

type Agent = {
  id: string
  slug: string
  name: string
  status: string
}

type AgentRun = {
  execution_id: string
  status: string
  output: string
}

type AgentReview = {
  id: string
  reviewer_id: string
  period_start: string
  period_end: string
  rating: number
  summary: string
  kpi_scores: Record<string, number>
  created_at: string
}

async function responseError(response: Response) {
  try {
    const body = await response.json() as { detail?: string }
    return body.detail || response.statusText || `Request failed (${response.status}).`
  } catch {
    return response.statusText || `Request failed (${response.status}).`
  }
}

async function fetchInstalledAgents(tenantId: string): Promise<Agent[]> {
  const response = await fetch(apiUrl(`/api/v1/agents?tenant_id=${encodeURIComponent(tenantId)}`))
  if (!response.ok) throw new Error(await responseError(response))
  return response.json() as Promise<Agent[]>
}

export default function SpecializedAIAgents() {
  const [tenantId, setTenantId] = useState(import.meta.env.VITE_TENANT_ID || 'local-workspace')
  const [actorId, setActorId] = useState('workspace-user')
  const [catalog, setCatalog] = useState<AgentTemplate[]>([])
  const [installedAgents, setInstalledAgents] = useState<Agent[]>([])
  const [selectedSlug, setSelectedSlug] = useState('')
  const [filter, setFilter] = useState('')
  const [prompt, setPrompt] = useState('')
  const [runResult, setRunResult] = useState<AgentRun | null>(null)
  const [reviews, setReviews] = useState<AgentReview[]>([])
  const [reviewSummary, setReviewSummary] = useState('')
  const [reviewRating, setReviewRating] = useState(4)
  const [reviewStart, setReviewStart] = useState('')
  const [reviewEnd, setReviewEnd] = useState('')
  const [reviewScores, setReviewScores] = useState<Record<string, string>>({})
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [loadingCatalog, setLoadingCatalog] = useState(true)
  const [working, setWorking] = useState(false)

  useEffect(() => {
    let active = true
    const loadCatalog = async () => {
      setLoadingCatalog(true)
      try {
        const response = await fetch(apiUrl('/api/v1/agents/catalog'))
        if (!response.ok) throw new Error(await responseError(response))
        const templates = await response.json() as AgentTemplate[]
        if (active) {
          setCatalog(templates)
          setSelectedSlug((current) => current || templates[0]?.slug || '')
          setError('')
        }
      } catch (loadError) {
        if (active) setError(loadError instanceof Error ? loadError.message : 'Could not load the agent catalog.')
      } finally {
        if (active) setLoadingCatalog(false)
      }
    }
    void loadCatalog()
    return () => { active = false }
  }, [])

  useEffect(() => {
    let active = true
    const loadAgents = async () => {
      if (!tenantId.trim()) {
        setInstalledAgents([])
        return
      }
      try {
        const agents = await fetchInstalledAgents(tenantId)
        if (active) setInstalledAgents(agents)
      } catch (loadError) {
        if (active) setError(loadError instanceof Error ? loadError.message : 'Could not load installed agents.')
      }
    }
    void loadAgents()
    return () => { active = false }
  }, [tenantId])

  const installedBySlug = useMemo(
    () => new Map(installedAgents.map((agent) => [agent.slug, agent])),
    [installedAgents],
  )
  const selectedTemplate = catalog.find((template) => template.slug === selectedSlug)
  const selectedAgent = selectedTemplate ? installedBySlug.get(selectedTemplate.slug) : undefined
  const filteredCatalog = catalog.filter((template) => {
    const query = filter.trim().toLowerCase()
    return !query || `${template.name} ${template.responsibility} ${template.tasks.join(' ')}`
      .toLowerCase()
      .includes(query)
  })

  useEffect(() => {
    let active = true
    const loadReviews = async () => {
      if (!selectedAgent || !tenantId.trim()) {
        setReviews([])
        return
      }
      try {
        const response = await fetch(
          apiUrl(`/api/v1/agents/${selectedAgent.id}/reviews?tenant_id=${encodeURIComponent(tenantId)}`),
        )
        if (!response.ok) throw new Error(await responseError(response))
        const items = await response.json() as AgentReview[]
        if (active) setReviews(items)
      } catch (loadError) {
        if (active) setError(loadError instanceof Error ? loadError.message : 'Could not load agent reviews.')
      }
    }
    void loadReviews()
    return () => { active = false }
  }, [selectedAgent, tenantId])

  const loadInstalledAgents = async (tenant = tenantId) => {
    setInstalledAgents(await fetchInstalledAgents(tenant))
  }

  const installAll = async () => {
    setWorking(true)
    setError('')
    setNotice('')
    try {
      const response = await fetch(apiUrl('/api/v1/agents/catalog/install'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenant_id: tenantId, actor_id: actorId }),
      })
      if (!response.ok) throw new Error(await responseError(response))
      const agents = await response.json() as Agent[]
      setInstalledAgents(agents)
      setNotice(`All ${agents.length} specialized agents are installed for ${tenantId}.`)
    } catch (installError) {
      setError(installError instanceof Error ? installError.message : 'Could not install the agent catalog.')
    } finally {
      setWorking(false)
    }
  }

  const refreshAgents = async () => {
    setWorking(true)
    setError('')
    setNotice('')
    try {
      await loadInstalledAgents()
      setNotice(`Agent list refreshed for ${tenantId}.`)
    } catch (refreshError) {
      setError(refreshError instanceof Error ? refreshError.message : 'Could not load installed agents.')
    } finally {
      setWorking(false)
    }
  }

  const runSelectedAgent = async () => {
    if (!selectedAgent || !prompt.trim()) return
    setWorking(true)
    setError('')
    setNotice('')
    setRunResult(null)
    try {
      const response = await fetch(apiUrl(`/api/v1/agents/${selectedAgent.id}/run`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenant_id: tenantId, actor_id: actorId, prompt: prompt.trim() }),
      })
      if (!response.ok) throw new Error(await responseError(response))
      setRunResult(await response.json() as AgentRun)
    } catch (runError) {
      setError(runError instanceof Error ? runError.message : 'Agent execution failed.')
    } finally {
      setWorking(false)
    }
  }

  const submitPerformanceReview = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!selectedAgent || !selectedTemplate) return
    setWorking(true)
    setError('')
    setNotice('')
    try {
      const response = await fetch(apiUrl(`/api/v1/agents/${selectedAgent.id}/reviews`), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tenant_id: tenantId,
          reviewer_id: actorId,
          period_start: reviewStart,
          period_end: reviewEnd,
          rating: reviewRating,
          summary: reviewSummary.trim(),
          kpi_scores: Object.fromEntries(
            selectedTemplate.kpis.map((kpi) => [kpi, Number(reviewScores[kpi])]),
          ),
        }),
      })
      if (!response.ok) throw new Error(await responseError(response))
      const review = await response.json() as AgentReview
      setReviews((current) => [review, ...current])
      setReviewSummary('')
      setReviewScores({})
      setNotice(`Performance review saved for ${selectedTemplate.name}.`)
    } catch (reviewError) {
      setError(reviewError instanceof Error ? reviewError.message : 'Could not save the performance review.')
    } finally {
      setWorking(false)
    }
  }

  return (
    <div className="specialized-page">
      <header className="specialized-header">
        <div>
          <span className="specialized-eyebrow"><Sparkles size={13} /> SPECIALIZED AI WORKFORCE</span>
          <h1>Specialized AI Agents</h1>
          <p>Install role-focused assistants for analysis, review, and recommendations.</p>
        </div>
        <span className="specialized-count"><Bot size={14} /> {catalog.length} AGENT TEMPLATES</span>
      </header>

      <section className="specialized-toolbar" aria-label="Agent workspace controls">
        <label>
          Workspace tenant
          <input value={tenantId} onChange={(event) => setTenantId(event.target.value)} />
        </label>
        <label>
          Operator ID
          <input value={actorId} onChange={(event) => setActorId(event.target.value)} />
        </label>
        <button type="button" className="specialized-secondary" disabled={working || !tenantId.trim()} onClick={() => void refreshAgents()}>
          Refresh installed
        </button>
        <button type="button" className="specialized-primary" disabled={working || !tenantId.trim() || !actorId.trim() || !catalog.length} onClick={() => void installAll()}>
          {working ? <LoaderCircle className="specialized-spinner" size={14} /> : <Check size={14} />}
        Install all {catalog.length}
        </button>
      </section>

      {error && <div className="specialized-message error" role="alert"><CircleAlert size={14} /> {error}</div>}
      {notice && <div className="specialized-message success" role="status"><Check size={14} /> {notice}</div>}

      <div className="specialized-workspace">
        <section className="specialized-catalog">
          <div className="specialized-section-heading">
            <div><h2>Agent catalog</h2><p>Select a role to review its remit and run it.</p></div>
            <label className="specialized-search"><Search size={14} /><input value={filter} onChange={(event) => setFilter(event.target.value)} placeholder="Filter agents" aria-label="Filter agents" /></label>
          </div>
          {loadingCatalog ? (
            <div className="specialized-empty"><LoaderCircle className="specialized-spinner" size={18} /> Loading agent templates…</div>
          ) : (
            <div className="specialized-card-grid">
              {filteredCatalog.map((template) => {
                const installed = installedBySlug.has(template.slug)
                return (
                  <button
                    type="button"
                    className={`specialized-agent-card ${selectedSlug === template.slug ? 'selected' : ''}`}
                    key={template.slug}
                    onClick={() => { setSelectedSlug(template.slug); setRunResult(null) }}
                  >
                    <span className="specialized-card-top">
                      <span className="specialized-card-icon"><Bot size={16} /></span>
                      <span className={`specialized-installed ${installed ? 'yes' : ''}`}>{installed ? 'Installed' : 'Template'}</span>
                    </span>
                    <strong>{template.name}</strong>
                    <small>{template.responsibility}</small>
                  </button>
                )
              })}
              {!filteredCatalog.length && <div className="specialized-empty">No agents match this filter.</div>}
            </div>
          )}
        </section>

        <aside className="specialized-detail">
          {selectedTemplate ? (
            <>
              <div className="specialized-detail-heading">
                <span className="specialized-card-icon"><Bot size={18} /></span>
                <div><small>ROLE PROFILE</small><h2>{selectedTemplate.name}</h2></div>
              </div>
              <p className="specialized-responsibility">{selectedTemplate.job_description}</p>
              <h3>Supported work</h3>
              <ul>{selectedTemplate.tasks.map((task) => <li key={task}>{task}</li>)}</ul>
              <h3>Scoped permissions</h3>
              <ul>{selectedTemplate.permissions.map((permission) => <li key={permission}>{permission}</li>)}</ul>
              <h3>Performance KPIs</h3>
              <ul>{selectedTemplate.kpis.map((kpi) => <li key={kpi}>{kpi}</li>)}</ul>
              <div className="specialized-guardrail">
                <ShieldCheck size={15} />
                <span>{selectedTemplate.guardrails[0]}</span>
              </div>
              {selectedAgent ? (
                <div className="specialized-run">
                  <label htmlFor="specialized-agent-prompt">Task and authorized context</label>
                  <textarea
                    id="specialized-agent-prompt"
                    value={prompt}
                    onChange={(event) => setPrompt(event.target.value)}
                    placeholder={`What should ${selectedTemplate.name} review? Paste only information you are authorized to share.`}
                    maxLength={12000}
                  />
                  <button type="button" className="specialized-primary" disabled={working || !prompt.trim()} onClick={() => void runSelectedAgent()}>
                    {working ? <LoaderCircle className="specialized-spinner" size={14} /> : <Play size={14} />}
                    Run agent
                  </button>
                  {runResult && (
                    <div className="specialized-result">
                      <div><strong>Run complete</strong><small>{runResult.execution_id}</small></div>
                      <p>{runResult.output}</p>
                    </div>
                  )}
                  <small className="specialized-privacy">Uses the configured model gateway. No live business systems are connected to these role templates.</small>
                  <section className="specialized-review">
                    <div className="specialized-review-heading">
                      <div><h3><ClipboardCheck size={13} /> Human performance review</h3><small>Manager-entered ratings and KPI evidence</small></div>
                      <span>{reviews.length} reviews</span>
                    </div>
                    <form onSubmit={(event) => void submitPerformanceReview(event)}>
                      <label>Review period
                        <span className="specialized-review-dates">
                          <input aria-label="Review period start" type="date" required value={reviewStart} onChange={(event) => setReviewStart(event.target.value)} />
                          <input aria-label="Review period end" type="date" required value={reviewEnd} onChange={(event) => setReviewEnd(event.target.value)} />
                        </span>
                      </label>
                      <label>Overall rating
                        <select value={reviewRating} onChange={(event) => setReviewRating(Number(event.target.value))}>
                          {[1, 2, 3, 4, 5].map((rating) => <option key={rating} value={rating}>{rating} / 5</option>)}
                        </select>
                      </label>
                      <div className="specialized-review-kpis">
                        {selectedTemplate.kpis.map((kpi) => (
                          <label key={kpi}>{kpi}
                            <span><input
                              aria-label={`${kpi} score`}
                              type="number"
                              min="0"
                              max="100"
                              step="1"
                              required
                              value={reviewScores[kpi] ?? ''}
                              onChange={(event) => setReviewScores((current) => ({ ...current, [kpi]: event.target.value }))}
                            /> / 100</span>
                          </label>
                        ))}
                      </div>
                      <label>Review notes
                        <textarea required maxLength={4000} value={reviewSummary} onChange={(event) => setReviewSummary(event.target.value)} placeholder="Summarize evidence, strengths, and improvement areas." />
                      </label>
                      <button type="submit" className="specialized-secondary" disabled={working || !actorId.trim()}>
                        {working ? <LoaderCircle className="specialized-spinner" size={13} /> : <Star size={13} />}
                        Save performance review
                      </button>
                    </form>
                    <div className="specialized-review-history">
                      {reviews.slice(0, 5).map((review) => (
                        <article key={review.id}>
                          <div><strong>{review.rating}/5</strong><span><CalendarDays size={11} /> {review.period_start} – {review.period_end}</span></div>
                          <p>{review.summary}</p>
                          <small>Reviewed by {review.reviewer_id} · {Object.entries(review.kpi_scores).map(([name, score]) => `${name}: ${score}`).join(' · ')}</small>
                        </article>
                      ))}
                      {!reviews.length && <small>No saved reviews for this agent yet.</small>}
                    </div>
                  </section>
                </div>
              ) : (
                <div className="specialized-not-installed">
                  <p>This role is not installed for the selected tenant.</p>
                  <button type="button" className="specialized-primary" disabled={working || !tenantId.trim() || !actorId.trim()} onClick={() => void installAll()}>
                    Install agent catalog
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="specialized-empty">Choose an agent role to view its profile.</div>
          )}
        </aside>
      </div>
    </div>
  )
}
