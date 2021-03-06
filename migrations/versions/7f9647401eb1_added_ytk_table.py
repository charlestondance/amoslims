"""added ytk table

Revision ID: 7f9647401eb1
Revises: 3cf127046be8
Create Date: 2017-03-01 16:37:44.034597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f9647401eb1'
down_revision = '3cf127046be8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('basic_ytk_design',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stitch_id', sa.String(length=64), nullable=True),
    sa.Column('clip_id', sa.String(length=64), nullable=True),
    sa.Column('part_id', sa.String(length=64), nullable=True),
    sa.Column('part_name', sa.String(length=64), nullable=True),
    sa.Column('experiment_id', sa.String(length=64), nullable=True),
    sa.Column('assembly_level', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_basic_ytk_design_assembly_level'), 'basic_ytk_design', ['assembly_level'], unique=False)
    op.create_index(op.f('ix_basic_ytk_design_clip_id'), 'basic_ytk_design', ['clip_id'], unique=False)
    op.create_index(op.f('ix_basic_ytk_design_experiment_id'), 'basic_ytk_design', ['experiment_id'], unique=False)
    op.create_index(op.f('ix_basic_ytk_design_part_id'), 'basic_ytk_design', ['part_id'], unique=False)
    op.create_index(op.f('ix_basic_ytk_design_part_name'), 'basic_ytk_design', ['part_name'], unique=False)
    op.create_index(op.f('ix_basic_ytk_design_stitch_id'), 'basic_ytk_design', ['stitch_id'], unique=False)
    op.drop_index('ix_consumable_location_1', table_name='consumable')
    op.create_index(op.f('ix_consumable_location_1'), 'consumable', ['location_1'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_consumable_location_1'), table_name='consumable')
    op.create_index('ix_consumable_location_1', 'consumable', ['location_1'], unique=True)
    op.drop_index(op.f('ix_basic_ytk_design_stitch_id'), table_name='basic_ytk_design')
    op.drop_index(op.f('ix_basic_ytk_design_part_name'), table_name='basic_ytk_design')
    op.drop_index(op.f('ix_basic_ytk_design_part_id'), table_name='basic_ytk_design')
    op.drop_index(op.f('ix_basic_ytk_design_experiment_id'), table_name='basic_ytk_design')
    op.drop_index(op.f('ix_basic_ytk_design_clip_id'), table_name='basic_ytk_design')
    op.drop_index(op.f('ix_basic_ytk_design_assembly_level'), table_name='basic_ytk_design')
    op.drop_table('basic_ytk_design')
    # ### end Alembic commands ###
