export function StatusBadge({ status }: { status: 'healthy' | 'warning' | 'critical' | 'planned' }) {
  return <span className={`status-badge ${status}`}>{status}</span>
}
