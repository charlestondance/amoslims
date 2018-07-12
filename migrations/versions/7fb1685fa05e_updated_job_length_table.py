"""updated job length table

Revision ID: 7fb1685fa05e
Revises: 6d9db8212035
Create Date: 2017-01-15 15:42:11.304482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fb1685fa05e'
down_revision = '6d9db8212035'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('basic_joblength',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stitch_length', sa.Integer(), nullable=True),
    sa.Column('unique_job_id', sa.String(length=64), nullable=True),
    sa.Column('stitch_id', sa.String(length=64), nullable=True),
    sa.Column('buffer_volume', sa.Integer(), nullable=True),
    sa.Column('total_volume', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_basic_joblength_buffer_volume'), 'basic_joblength', ['buffer_volume'], unique=False)
    op.create_index(op.f('ix_basic_joblength_stitch_id'), 'basic_joblength', ['stitch_id'], unique=False)
    op.create_index(op.f('ix_basic_joblength_stitch_length'), 'basic_joblength', ['stitch_length'], unique=False)
    op.create_index(op.f('ix_basic_joblength_total_volume'), 'basic_joblength', ['total_volume'], unique=False)
    op.create_index(op.f('ix_basic_joblength_unique_job_id'), 'basic_joblength', ['unique_job_id'], unique=False)
    op.drop_table('job_length')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_length',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('unique_job_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('stitch_length', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('stitch_number', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='job_length_pkey')
    )
    op.drop_index(op.f('ix_basic_joblength_unique_job_id'), table_name='basic_joblength')
    op.drop_index(op.f('ix_basic_joblength_total_volume'), table_name='basic_joblength')
    op.drop_index(op.f('ix_basic_joblength_stitch_length'), table_name='basic_joblength')
    op.drop_index(op.f('ix_basic_joblength_stitch_id'), table_name='basic_joblength')
    op.drop_index(op.f('ix_basic_joblength_buffer_volume'), table_name='basic_joblength')
    op.drop_table('basic_joblength')
    # ### end Alembic commands ###
