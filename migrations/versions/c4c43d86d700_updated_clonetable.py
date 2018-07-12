"""updated clonetable

Revision ID: c4c43d86d700
Revises: 2e35e3944322
Create Date: 2017-01-18 15:53:35.332067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4c43d86d700'
down_revision = '2e35e3944322'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('basic_stitch_clone', sa.Column('stitch_id', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_basic_stitch_clone_stitch_id'), 'basic_stitch_clone', ['stitch_id'], unique=False)
    op.drop_index('ix_basic_stitch_clone_stitch_plate_number', table_name='basic_stitch_clone')
    op.drop_column('basic_stitch_clone', 'stitch_plate_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('basic_stitch_clone', sa.Column('stitch_plate_number', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_index('ix_basic_stitch_clone_stitch_plate_number', 'basic_stitch_clone', ['stitch_plate_number'], unique=False)
    op.drop_index(op.f('ix_basic_stitch_clone_stitch_id'), table_name='basic_stitch_clone')
    op.drop_column('basic_stitch_clone', 'stitch_id')
    # ### end Alembic commands ###
