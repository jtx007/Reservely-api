import sys
import os
from logging.config import fileConfig
from typing import Optional, cast

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Engine
from alembic import context

# Add project root so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.config import settings
from app.db.base import Base  # import your metadata

# Alembic Config object
config = context.config

# Override sqlalchemy.url with strongly-typed settings
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Configure logging
cfg_file: Optional[str] = config.config_file_name
if cfg_file:
    fileConfig(cfg_file)

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    alembic_config_dict = config.get_section(config.config_ini_section) or {}
    connectable = engine_from_config(
        cast(dict[str, object], alembic_config_dict),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
