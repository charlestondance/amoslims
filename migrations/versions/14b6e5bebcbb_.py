"""empty message

Revision ID: 14b6e5bebcbb
Revises: 4be59e16e00f
Create Date: 2017-10-23 12:44:00.379469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14b6e5bebcbb'
down_revision = '4be59e16e00f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jmp_tracker', sa.Column('item_count', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_jmp_tracker_item_count'), 'jmp_tracker', ['item_count'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_jmp_tracker_item_count'), table_name='jmp_tracker')
    op.drop_column('jmp_tracker', 'item_count')
    # ### end Alembic commands ###
