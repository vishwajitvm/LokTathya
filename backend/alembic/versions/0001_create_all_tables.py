"""create all loktathya tables

Revision ID: 0001_create_all_tables
Revises: 1234567890ab
Create Date: 2026-08-22

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_create_all_tables'
down_revision = '1234567890ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure required PostgreSQL extensions are enabled
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # --- geo_entity ---
    op.create_table(
        'geo_entity',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('canonical_name', sa.String(512), nullable=False),
        sa.Column('entity_type', sa.String(100), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('geo_entity.id'), nullable=True),
        sa.Column('valid_from', sa.DateTime(timezone=True), nullable=True),
        sa.Column('valid_until', sa.DateTime(timezone=True), nullable=True),
    )

    # --- geo_relationship ---
    op.create_table(
        'geo_relationship',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('from_entity_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('geo_entity.id'), nullable=False),
        sa.Column('to_entity_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('geo_entity.id'), nullable=False),
        sa.Column('relationship_type', sa.String(100), nullable=False),
        sa.Column('valid_from', sa.DateTime(timezone=True), nullable=True),
        sa.Column('valid_until', sa.DateTime(timezone=True), nullable=True),
    )

    # --- sys_entity_resolution ---
    op.create_table(
        'sys_entity_resolution',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('canonical_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_id', sa.String(512), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
    )

    # --- src_source ---
    op.create_table(
        'src_source',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(512), nullable=False),
        sa.Column('category', sa.String(100), nullable=True),
        sa.Column('official_url', sa.String(2048), nullable=True),
        sa.Column('last_fetched', sa.DateTime(timezone=True), nullable=True),
    )

    # --- src_endpoint ---
    op.create_table(
        'src_endpoint',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_source.id'), nullable=False),
        sa.Column('url', sa.String(2048), nullable=False),
        sa.Column('method', sa.String(10), nullable=False),
    )

    # --- src_dataset ---
    op.create_table(
        'src_dataset',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_source.id'), nullable=False),
        sa.Column('name', sa.String(512), nullable=False),
    )

    # --- src_ingestion_run ---
    op.create_table(
        'src_ingestion_run',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('dataset_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_dataset.id'), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
    )

    # --- src_fetch_event ---
    op.create_table(
        'src_fetch_event',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('run_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_ingestion_run.id'), nullable=False),
        sa.Column('url', sa.String(2048), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('fetched_at', sa.DateTime(timezone=True), nullable=True),
    )

    # --- src_document ---
    op.create_table(
        'src_document',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('fetch_event_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_fetch_event.id'), nullable=False),
        sa.Column('raw_url', sa.String(2048), nullable=False),
        sa.Column('content_hash', sa.String(64), nullable=True),
    )

    # --- src_content_version ---
    op.create_table(
        'src_content_version',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_document.id'), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    # --- prov_claim ---
    op.create_table(
        'prov_claim',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('entity_type', sa.String(100), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('field_name', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
    )

    # --- prov_evidence ---
    op.create_table(
        'prov_evidence',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('claim_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('prov_claim.id'), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_source.id'), nullable=False),
        sa.Column('value_text', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
    )

    # --- rep_person ---
    op.create_table(
        'rep_person',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('raw_source_name', sa.String(255), nullable=True),
    )

    # --- rep_party ---
    op.create_table(
        'rep_party',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
    )

    # --- rep_position ---
    op.create_table(
        'rep_position',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('level', sa.String(100), nullable=False),
    )

    # --- rep_term ---
    op.create_table(
        'rep_term',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('person_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('rep_person.id'), nullable=False),
        sa.Column('position_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('rep_position.id'), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('rep_party.id'), nullable=True),
        sa.Column('jurisdiction_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('geo_entity.id'), nullable=False),
        sa.Column('valid_from', sa.DateTime(timezone=True), nullable=True),
        sa.Column('valid_until', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('valid_until >= valid_from', name='check_valid_dates_term'),
    )

    # --- elec_election ---
    op.create_table(
        'elec_election',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(512), nullable=False),
        sa.Column('election_type', sa.String(100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
    )

    # --- elec_event ---
    op.create_table(
        'elec_event',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('election_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elec_election.id'), nullable=False),
        sa.Column('constituency_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('geo_entity.id'), nullable=False),
        sa.Column('event_date', sa.DateTime(timezone=True), nullable=True),
    )

    # --- elec_candidate ---
    op.create_table(
        'elec_candidate',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('election_event_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elec_event.id'), nullable=False),
        sa.Column('person_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('rep_person.id'), nullable=False),
        sa.Column('party_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('rep_party.id'), nullable=True),
        sa.Column('status', sa.String(50), nullable=False),
    )

    # --- elec_result ---
    op.create_table(
        'elec_result',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('candidate_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('elec_candidate.id'), nullable=False),
        sa.Column('votes', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(50), nullable=False),
    )

    # --- proj_project ---
    op.create_table(
        'proj_project',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(1024), nullable=False),
        sa.Column('raw_name', sa.String(1024), nullable=False),
    )

    # --- proj_work ---
    op.create_table(
        'proj_work',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('proj_project.id'), nullable=False),
        sa.Column('name', sa.String(1024), nullable=False),
    )

    # --- proj_contractor ---
    op.create_table(
        'proj_contractor',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
    )

    # --- proj_tender ---
    op.create_table(
        'proj_tender',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('work_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('proj_work.id'), nullable=False),
        sa.Column('tender_reference', sa.String(255), nullable=False),
    )

    # --- proj_contract ---
    op.create_table(
        'proj_contract',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tender_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('proj_tender.id'), nullable=True),
        sa.Column('contractor_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('proj_contractor.id'), nullable=True),
        sa.Column('amount', sa.Numeric(15, 2), nullable=False),
    )

    # --- fin_year ---
    op.create_table(
        'fin_year',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('label', sa.String(20), nullable=False),
    )

    # --- fin_budget ---
    op.create_table(
        'fin_budget',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('year_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('fin_year.id'), nullable=False),
        sa.Column('jurisdiction_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('geo_entity.id'), nullable=False),
        sa.Column('total_allocation', sa.Numeric(20, 2), nullable=True),
    )

    # --- fin_allocation ---
    op.create_table(
        'fin_allocation',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('budget_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('fin_budget.id'), nullable=False),
        sa.Column('amount', sa.Numeric(20, 2), nullable=False),
    )

    # --- fin_release ---
    op.create_table(
        'fin_release',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('allocation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('fin_allocation.id'), nullable=False),
        sa.Column('amount', sa.Numeric(20, 2), nullable=False),
        sa.Column('released_at', sa.DateTime(timezone=True), nullable=True),
    )

    # --- fin_expenditure ---
    op.create_table(
        'fin_expenditure',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('release_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('fin_release.id'), nullable=False),
        sa.Column('amount', sa.Numeric(20, 2), nullable=False),
        sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=True),
    )

    # --- ai_embedding_model ---
    op.create_table(
        'ai_embedding_model',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('dimensions', sa.Integer(), nullable=False),
    )

    # --- ai_chunk ---
    op.create_table(
        'ai_chunk',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('src_document.id'), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
    )

    # --- ai_embedding ---
    op.create_table(
        'ai_embedding',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('chunk_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ai_chunk.id'), nullable=False),
        sa.Column('model_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('ai_embedding_model.id'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('ai_embedding')
    op.drop_table('ai_chunk')
    op.drop_table('ai_embedding_model')
    op.drop_table('fin_expenditure')
    op.drop_table('fin_release')
    op.drop_table('fin_allocation')
    op.drop_table('fin_budget')
    op.drop_table('fin_year')
    op.drop_table('proj_contract')
    op.drop_table('proj_tender')
    op.drop_table('proj_contractor')
    op.drop_table('proj_work')
    op.drop_table('proj_project')
    op.drop_table('elec_result')
    op.drop_table('elec_candidate')
    op.drop_table('elec_event')
    op.drop_table('elec_election')
    op.drop_table('rep_term')
    op.drop_table('rep_position')
    op.drop_table('rep_party')
    op.drop_table('rep_person')
    op.drop_table('prov_evidence')
    op.drop_table('prov_claim')
    op.drop_table('src_content_version')
    op.drop_table('src_document')
    op.drop_table('src_fetch_event')
    op.drop_table('src_ingestion_run')
    op.drop_table('src_dataset')
    op.drop_table('src_endpoint')
    op.drop_table('src_source')
    op.drop_table('sys_entity_resolution')
    op.drop_table('geo_relationship')
    op.drop_table('geo_entity')
