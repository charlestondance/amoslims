"""metrology assay plate

Revision ID: 566d4b4ebb6e
Revises: 55ff649a8d97
Create Date: 2017-06-29 18:46:17.784853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566d4b4ebb6e'
down_revision = '55ff649a8d97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metrology_assay_plate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clone_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('clone_plate_well_id', sa.String(length=64), nullable=True),
    sa.Column('stitch_number', sa.Integer(), nullable=True),
    sa.Column('concatenated_stitch_id', sa.String(length=64), nullable=True),
    sa.Column('registered_dna_id', sa.String(length=64), nullable=True),
    sa.Column('build_job_id', sa.String(length=64), nullable=True),
    sa.Column('nice_name_id', sa.String(length=64), nullable=True),
    sa.Column('doe_id', sa.String(length=64), nullable=True),
    sa.Column('plate_type', sa.String(length=64), nullable=True),
    sa.Column('uploaded_filename', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_metrology_assay_plate_build_job_id'), 'metrology_assay_plate', ['build_job_id'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_clone_plate_barcode'), 'metrology_assay_plate', ['clone_plate_barcode'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_clone_plate_well_id'), 'metrology_assay_plate', ['clone_plate_well_id'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_concatenated_stitch_id'), 'metrology_assay_plate', ['concatenated_stitch_id'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_doe_id'), 'metrology_assay_plate', ['doe_id'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_nice_name_id'), 'metrology_assay_plate', ['nice_name_id'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_plate_type'), 'metrology_assay_plate', ['plate_type'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_registered_dna_id'), 'metrology_assay_plate', ['registered_dna_id'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_stitch_number'), 'metrology_assay_plate', ['stitch_number'], unique=False)
    op.create_index(op.f('ix_metrology_assay_plate_uploaded_filename'), 'metrology_assay_plate', ['uploaded_filename'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_metrology_assay_plate_uploaded_filename'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_stitch_number'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_registered_dna_id'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_plate_type'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_nice_name_id'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_doe_id'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_concatenated_stitch_id'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_clone_plate_well_id'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_clone_plate_barcode'), table_name='metrology_assay_plate')
    op.drop_index(op.f('ix_metrology_assay_plate_build_job_id'), table_name='metrology_assay_plate')
    op.drop_table('metrology_assay_plate')
    # ### end Alembic commands ###
