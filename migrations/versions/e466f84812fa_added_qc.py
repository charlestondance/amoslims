"""added qc

Revision ID: e466f84812fa
Revises: d08ff74c1574
Create Date: 2017-06-02 14:18:29.281159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e466f84812fa'
down_revision = 'd08ff74c1574'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('basic_clip_qc_part_sizes', sa.Column('qc', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('basic_clip_qc_part_sizes', 'qc')
    # ### end Alembic commands ###
