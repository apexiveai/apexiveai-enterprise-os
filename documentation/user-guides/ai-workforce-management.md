# AI Workforce Management

The agent catalog is available at `GET /api/v1/agents/catalog`. Each template
includes a job description, supported work, scoped permission statement, KPI
criteria, and role safeguards. The catalog includes Finance, HR, Sales,
Procurement, Legal, and Operations Manager roles.

Install the templates for a tenant with
`POST /api/v1/agents/catalog/install`. Templates have no external tools enabled
by default. Their permission statements describe the intended scope: analyze
information supplied by an authorized user and draft recommendations for human
review. They do not grant access to live ERP, finance, HR, CRM, email, or other
company systems.

Installed agents can be reviewed and managed through the agent APIs:

- `GET /api/v1/agents?tenant_id={tenant_id}` lists installed agents.
- `PUT /api/v1/agents/{agent_id}/policy` updates the agent's allowlisted tools.
- `PUT /api/v1/agents/{agent_id}/status` enables or disables an agent.
- `POST /api/v1/agents/{agent_id}/reviews` stores a human-entered rating,
  review period, KPI scores, reviewer ID, and written review.
- `GET /api/v1/agents/{agent_id}/reviews?tenant_id={tenant_id}` returns that
  agent's review history for the tenant.

Review scores are entered by a reviewer; they are not automatically inferred
from agent runs. The API validates the rating, period, and KPI score range and
records a corresponding agent audit event.

**Security limitation:** tenant and actor IDs are currently supplied by API
requests; authentication and authorization are not yet implemented. Keep these
endpoints on trusted development networks and do not send sensitive company
data until authenticated tenant identity, authorization, and approved model-gateway
controls are deployed.
