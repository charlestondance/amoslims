"""added metrology plates

Revision ID: e292a21703ca
Revises: 32603ed8f589
Create Date: 2017-06-29 18:01:37.830636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e292a21703ca'
down_revision = '32603ed8f589'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metrology_plate_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('well_type', sa.String(length=64), nullable=True),
    sa.Column('well_id', sa.String(length=64), nullable=True),
    sa.Column('total_well_number', sa.Integer(), nullable=True),
    sa.Column('sample', sa.Integer(), nullable=True),
    sa.Column('sample_group1', sa.Integer(), nullable=True),
    sa.Column('sample_group2', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_metrology_plate_types_sample'), 'metrology_plate_types', ['sample'], unique=False)
    op.create_index(op.f('ix_metrology_plate_types_sample_group1'), 'metrology_plate_types', ['sample_group1'], unique=False)
    op.create_index(op.f('ix_metrology_plate_types_sample_group2'), 'metrology_plate_types', ['sample_group2'], unique=False)
    op.create_index(op.f('ix_metrology_plate_types_total_well_number'), 'metrology_plate_types', ['total_well_number'], unique=False)
    op.create_index(op.f('ix_metrology_plate_types_well_id'), 'metrology_plate_types', ['well_id'], unique=False)
    op.create_index(op.f('ix_metrology_plate_types_well_type'), 'metrology_plate_types', ['well_type'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_metrology_plate_types_well_type'), table_name='metrology_plate_types')
    op.drop_index(op.f('ix_metrology_plate_types_well_id'), table_name='metrology_plate_types')
    op.drop_index(op.f('ix_metrology_plate_types_total_well_number'), table_name='metrology_plate_types')
    op.drop_index(op.f('ix_metrology_plate_types_sample_group2'), table_name='metrology_plate_types')
    op.drop_index(op.f('ix_metrology_plate_types_sample_group1'), table_name='metrology_plate_types')
    op.drop_index(op.f('ix_metrology_plate_types_sample'), table_name='metrology_plate_types')
    op.drop_table('metrology_plate_types')
    # ### end Alembic commands ###
