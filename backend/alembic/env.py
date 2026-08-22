from alembic import context
from sqlalchemy import engine_from_config, pool
import os
import logging
from logging.config import fileConfig

# Import all model metadata so Alembic can autogenerate migrations
from models.base import Base
import models.geography
import models.representative
import models.election
import models.finance
import models.project
import models.provenance
import models.resolution
import models.source
import models.ai

config = context.config
fileConfig(config.config_file_name)

db_url = os.environ.get("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def include_object(object, name, type_, reflected, compare_to):
    # Ignore tables in tiger, tiger_data, and topology schemas
    if getattr(object, "schema", None) in ["tiger", "tiger_data", "topology"]:
        return False
        
    # Ignore specific PostGIS/Geocoder tables that might appear in public schema
    if type_ == "table" and name in [
        'spatial_ref_sys', 'topology', 'layer', 'zip_lookup_base', 'zip_lookup_all', 'county',
        'place_lookup', 'state_lookup', 'tabblock20', 'cousub', 'edges', 'loader_platform',
        'zcta5', 'place', 'countysub_lookup', 'street_type_lookup', 'direction_lookup',
        'addrfeat', 'loader_variables', 'county_lookup', 'bg', 'featnames', 'layer',
        'state', 'zip_lookup', 'tabblock', 'zip_state_loc', 'geocode_settings_default',
        'faces', 'geocode_settings', 'tract', 'addr', 'pagc_lex', 'pagc_gaz', 'pagc_rules',
        'secondary_unit_lookup', 'zip_state', 'loader_lookuptables'
    ]:
        return False
    return True

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
            include_object=include_object
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
