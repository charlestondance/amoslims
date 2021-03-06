"""added virgin design table

Revision ID: dc4b990068f2
Revises: 196f94f160e1
Create Date: 2017-01-31 08:37:25.239134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc4b990068f2'
down_revision = '196f94f160e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('virgindesign',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stitch_id', sa.String(length=64), nullable=True),
    sa.Column('clip_id', sa.String(length=64), nullable=True),
    sa.Column('part_id', sa.String(length=64), nullable=True),
    sa.Column('part_name', sa.Integer(), nullable=True),
    sa.Column('experiment_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_virgindesign_clip_id'), 'virgindesign', ['clip_id'], unique=False)
    op.create_index(op.f('ix_virgindesign_experiment_id'), 'virgindesign', ['experiment_id'], unique=False)
    op.create_index(op.f('ix_virgindesign_part_id'), 'virgindesign', ['part_id'], unique=False)
    op.create_index(op.f('ix_virgindesign_part_name'), 'virgindesign', ['part_name'], unique=False)
    op.create_index(op.f('ix_virgindesign_stitch_id'), 'virgindesign', ['stitch_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_virgindesign_stitch_id'), table_name='virgindesign')
    op.drop_index(op.f('ix_virgindesign_part_name'), table_name='virgindesign')
    op.drop_index(op.f('ix_virgindesign_part_id'), table_name='virgindesign')
    op.drop_index(op.f('ix_virgindesign_experiment_id'), table_name='virgindesign')
    op.drop_index(op.f('ix_virgindesign_clip_id'), table_name='virgindesign')
    op.drop_table('virgindesign')
    # ### end Alembic commands ###
