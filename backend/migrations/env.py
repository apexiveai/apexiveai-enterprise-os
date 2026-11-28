
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.db.base import Base
from app.modules.process_automation import models as process_models
from app.modules.agents import models as agent_models
from app.modules.platform import models as platform_models
from app.modules.industry_solutions import models as industry_solution_models


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)

target_metadata = Base.metadata

MANAGED_TABLES = {
    "process_definitions",
    "process_versions",
    "process_executions",
    "process_approvals",
    "process_audit_logs",
    "agent_definitions",
    "agent_memories",
    "agent_executions",
    "agent_audit_logs",
    "agent_teams",
    "agent_team_executions",
    "agent_performance_reviews",
    "knowledge_documents",
    "knowledge_relations",
    "platform_events",
    "evaluation_runs",
    "stored_objects",
    "industry_solution_records",
}


def include_object(
    object,
    name,
    type_,
    reflected,
    compare_to,
):
    if type_ == "table":
        return name in MANAGED_TABLES

    parent_table = getattr(object, "table", None)

    if parent_table is not None:
        return parent_table.name in MANAGED_TABLES

    return True


def run_migrations_offline():
    url = settings.database_url

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
