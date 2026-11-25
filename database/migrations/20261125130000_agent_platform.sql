BEGIN;

CREATE TABLE IF NOT EXISTS public.agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'active', 'paused', 'archived')),
    version INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.agent_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    role_key TEXT NOT NULL,
    display_name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    permissions JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, role_key)
);

CREATE TABLE IF NOT EXISTS public.agent_goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    priority SMALLINT NOT NULL DEFAULT 100 CHECK (priority >= 0),
    success_criteria JSONB NOT NULL DEFAULT '[]'::jsonb,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'completed', 'paused', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.agent_instructions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    version INTEGER NOT NULL CHECK (version > 0),
    instructions TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, version)
);

CREATE TABLE IF NOT EXISTS public.agent_model_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    config_name TEXT NOT NULL DEFAULT 'default',
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    endpoint_url TEXT,
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    credential_ref TEXT,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, config_name)
);

CREATE TABLE IF NOT EXISTS public.agent_memory_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    config_name TEXT NOT NULL DEFAULT 'default',
    memory_type TEXT NOT NULL,
    provider TEXT,
    configuration JSONB NOT NULL DEFAULT '{}'::jsonb,
    retention_days INTEGER CHECK (retention_days IS NULL OR retention_days >= 0),
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, config_name)
);

CREATE TABLE IF NOT EXISTS public.agent_tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tool_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    category TEXT NOT NULL DEFAULT 'general',
    handler TEXT,
    input_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_schema JSONB NOT NULL DEFAULT '{}'::jsonb,
    risk_level TEXT NOT NULL DEFAULT 'low'
        CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.agent_tool_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES public.agent_tools(id) ON DELETE CASCADE,
    permission TEXT NOT NULL DEFAULT 'deny'
        CHECK (permission IN ('deny', 'read', 'execute', 'admin')),
    policy JSONB NOT NULL DEFAULT '{}'::jsonb,
    granted_by UUID,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, tool_id)
);

CREATE TABLE IF NOT EXISTS public.agent_tool_bindings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES public.agent_tools(id) ON DELETE CASCADE,
    binding_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    position INTEGER NOT NULL DEFAULT 0 CHECK (position >= 0),
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, tool_id)
);

CREATE TABLE IF NOT EXISTS public.knowledge_bases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    source_type TEXT NOT NULL DEFAULT 'manual'
        CHECK (source_type IN ('manual', 'file', 'url', 'connector')),
    configuration JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'indexing', 'paused', 'error')),
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    knowledge_base_id UUID NOT NULL
        REFERENCES public.knowledge_bases(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    source_uri TEXT,
    content_type TEXT,
    content TEXT,
    content_hash TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'indexed', 'error', 'deleted')),
    error_message TEXT,
    indexed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.agent_knowledge_bindings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    knowledge_base_id UUID NOT NULL
        REFERENCES public.knowledge_bases(id) ON DELETE CASCADE,
    binding_config JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, knowledge_base_id)
);

CREATE TABLE IF NOT EXISTS public.agent_test_suites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    version INTEGER NOT NULL DEFAULT 1 CHECK (version > 0),
    configuration JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_by UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (agent_id, name, version)
);

CREATE TABLE IF NOT EXISTS public.agent_test_cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_suite_id UUID NOT NULL REFERENCES public.agent_test_suites(id) ON DELETE CASCADE,
    case_key TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    input JSONB NOT NULL DEFAULT '{}'::jsonb,
    expected_output JSONB NOT NULL DEFAULT '{}'::jsonb,
    assertions JSONB NOT NULL DEFAULT '[]'::jsonb,
    position INTEGER NOT NULL DEFAULT 0 CHECK (position >= 0),
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (test_suite_id, case_key)
);

CREATE TABLE IF NOT EXISTS public.agent_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE RESTRICT,
    test_suite_id UUID REFERENCES public.agent_test_suites(id) ON DELETE SET NULL,
    trigger_type TEXT NOT NULL DEFAULT 'manual',
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'waiting_approval', 'succeeded', 'failed', 'cancelled')),
    input JSONB NOT NULL DEFAULT '{}'::jsonb,
    output JSONB,
    error_message TEXT,
    idempotency_key TEXT,
    created_by UUID,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.agent_execution_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    execution_id UUID NOT NULL REFERENCES public.agent_executions(id) ON DELETE CASCADE,
    sequence BIGINT NOT NULL CHECK (sequence >= 0),
    level TEXT NOT NULL DEFAULT 'info'
        CHECK (level IN ('debug', 'info', 'warning', 'error')),
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (execution_id, sequence)
);

CREATE TABLE IF NOT EXISTS public.agent_approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES public.agents(id) ON DELETE RESTRICT,
    execution_id UUID REFERENCES public.agent_executions(id) ON DELETE SET NULL,
    approval_type TEXT NOT NULL DEFAULT 'tool_execution',
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'approved', 'rejected', 'expired', 'cancelled')),
    requested_action JSONB NOT NULL DEFAULT '{}'::jsonb,
    requested_by UUID,
    decided_by UUID,
    decision_comment TEXT,
    expires_at TIMESTAMPTZ,
    decided_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.agent_audit_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    agent_id UUID REFERENCES public.agents(id) ON DELETE SET NULL,
    actor_type TEXT NOT NULL DEFAULT 'system',
    actor_id UUID,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    before_state JSONB,
    after_state JSONB,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_agent_roles_agent_id ON public.agent_roles(agent_id);
CREATE INDEX IF NOT EXISTS ix_agent_goals_agent_status ON public.agent_goals(agent_id, status);
CREATE INDEX IF NOT EXISTS ix_agent_instructions_active ON public.agent_instructions(agent_id, is_active);
CREATE UNIQUE INDEX IF NOT EXISTS uq_agent_model_configs_default
    ON public.agent_model_configs(agent_id) WHERE is_default;
CREATE INDEX IF NOT EXISTS ix_agent_memory_configs_agent ON public.agent_memory_configs(agent_id);
CREATE INDEX IF NOT EXISTS ix_agent_tool_permissions_tool ON public.agent_tool_permissions(tool_id);
CREATE INDEX IF NOT EXISTS ix_agent_tool_bindings_tool ON public.agent_tool_bindings(tool_id);
CREATE INDEX IF NOT EXISTS ix_knowledge_documents_base_status
    ON public.knowledge_documents(knowledge_base_id, status);
CREATE INDEX IF NOT EXISTS ix_knowledge_documents_content_hash
    ON public.knowledge_documents(knowledge_base_id, content_hash);
CREATE INDEX IF NOT EXISTS ix_agent_knowledge_bindings_base
    ON public.agent_knowledge_bindings(knowledge_base_id);
CREATE INDEX IF NOT EXISTS ix_agent_test_suites_agent
    ON public.agent_test_suites(agent_id, is_enabled);
CREATE INDEX IF NOT EXISTS ix_agent_test_cases_suite_position
    ON public.agent_test_cases(test_suite_id, position);
CREATE INDEX IF NOT EXISTS ix_agent_executions_agent_created
    ON public.agent_executions(agent_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_agent_executions_status_created
    ON public.agent_executions(status, created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS uq_agent_executions_idempotency
    ON public.agent_executions(agent_id, idempotency_key)
    WHERE idempotency_key IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_agent_execution_logs_execution_created
    ON public.agent_execution_logs(execution_id, created_at);
CREATE INDEX IF NOT EXISTS ix_agent_approvals_status_created
    ON public.agent_approvals(status, created_at);
CREATE INDEX IF NOT EXISTS ix_agent_audit_logs_agent_created
    ON public.agent_audit_logs(agent_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_agent_audit_logs_resource
    ON public.agent_audit_logs(resource_type, resource_id, created_at DESC);

COMMIT;
