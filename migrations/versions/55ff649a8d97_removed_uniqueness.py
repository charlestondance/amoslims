"""removed uniqueness

Revision ID: 55ff649a8d97
Revises: ed1caa589999
Create Date: 2017-06-29 18:23:38.661895

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55ff649a8d97'
down_revision = 'ed1caa589999'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_metrology_plate_types_well_type', table_name='metrology_plate_types')
    op.create_index(op.f('ix_metrology_plate_types_well_type'), 'metrology_plate_types', ['well_type'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_metrology_plate_types_well_type'), table_name='metrology_plate_types')
    op.create_index('ix_metrology_plate_types_well_type', 'metrology_plate_types', ['well_type'], unique=True)
    # ### end Alembic commands ###
