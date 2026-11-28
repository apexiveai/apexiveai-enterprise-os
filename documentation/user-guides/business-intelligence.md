# Business Intelligence APIs

The Reports & Analytics workspace exposes three data-driven tools:

- `POST /api/v1/insights/forecast` applies a straight-line trend to at least
  three supplied historical values and returns a bounded forecast horizon. It
  is an estimate, not a causal model or guarantee.
- `POST /api/v1/insights/reconciliation` compares statement and ledger rows by
  normalized reference, exact decimal amount, and currency. It reports duplicate
  references as exceptions instead of guessing how to pair them.
- `GET /api/v1/insights/process-mining?tenant_id={tenant_id}` summarizes
  recorded process execution counts, outcomes, and cycle times. It reports only
  data already persisted by Process Automation.

Forecasting and reconciliation do not retrieve or persist external financial
data. Process-mining metrics are limited to recorded execution timestamps and
statuses; the API does not infer step-level bottlenecks or SLA breaches without
those event records and configured targets.

The supplied tenant identifier is not authenticated. Keep the API on trusted
networks until authenticated tenant identity and authorization are deployed.
