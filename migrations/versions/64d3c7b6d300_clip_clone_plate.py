"""clip clone plate

Revision ID: 64d3c7b6d300
Revises: 7139eca901c0
Create Date: 2017-03-07 17:16:12.248665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d3c7b6d300'
down_revision = '7139eca901c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ytk_clip_clone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_job_id', sa.String(length=64), nullable=True),
    sa.Column('clone_plate_well_id_96', sa.String(length=64), nullable=True),
    sa.Column('well_number_96', sa.Integer(), nullable=True),
    sa.Column('clip_well_id', sa.String(length=64), nullable=True),
    sa.Column('clip_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('clone_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('clip_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ytk_clip_clone_clip_id'), 'ytk_clip_clone', ['clip_id'], unique=False)
    op.create_index(op.f('ix_ytk_clip_clone_clip_plate_barcode'), 'ytk_clip_clone', ['clip_plate_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_clip_clone_clip_well_id'), 'ytk_clip_clone', ['clip_well_id'], unique=False)
    op.create_index(op.f('ix_ytk_clip_clone_clone_plate_barcode'), 'ytk_clip_clone', ['clone_plate_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_clip_clone_clone_plate_well_id_96'), 'ytk_clip_clone', ['clone_plate_well_id_96'], unique=False)
    op.create_index(op.f('ix_ytk_clip_clone_unique_job_id'), 'ytk_clip_clone', ['unique_job_id'], unique=False)
    op.create_index(op.f('ix_ytk_clip_clone_well_number_96'), 'ytk_clip_clone', ['well_number_96'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ytk_clip_clone_well_number_96'), table_name='ytk_clip_clone')
    op.drop_index(op.f('ix_ytk_clip_clone_unique_job_id'), table_name='ytk_clip_clone')
    op.drop_index(op.f('ix_ytk_clip_clone_clone_plate_well_id_96'), table_name='ytk_clip_clone')
    op.drop_index(op.f('ix_ytk_clip_clone_clone_plate_barcode'), table_name='ytk_clip_clone')
    op.drop_index(op.f('ix_ytk_clip_clone_clip_well_id'), table_name='ytk_clip_clone')
    op.drop_index(op.f('ix_ytk_clip_clone_clip_plate_barcode'), table_name='ytk_clip_clone')
    op.drop_index(op.f('ix_ytk_clip_clone_clip_id'), table_name='ytk_clip_clone')
    op.drop_table('ytk_clip_clone')
    # ### end Alembic commands ###
