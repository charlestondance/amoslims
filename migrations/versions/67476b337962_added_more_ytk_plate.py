"""added more ytk plate

Revision ID: 67476b337962
Revises: 29b76ed5358c
Create Date: 2017-03-17 17:25:56.039832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67476b337962'
down_revision = '29b76ed5358c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ytk_job_master_level2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_job_id', sa.String(length=64), nullable=True),
    sa.Column('part_id', sa.String(length=64), nullable=True),
    sa.Column('job_master2_well_id', sa.String(length=64), nullable=True),
    sa.Column('job_master2_barcode', sa.String(length=64), nullable=True),
    sa.Column('sample_number', sa.Integer(), nullable=True),
    sa.Column('uploaded_filename', sa.String(length=64), nullable=True),
    sa.Column('level1clone_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('level1clone_location_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ytk_job_master_level2_job_master2_barcode'), 'ytk_job_master_level2', ['job_master2_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_job_master_level2_job_master2_well_id'), 'ytk_job_master_level2', ['job_master2_well_id'], unique=False)
    op.create_index(op.f('ix_ytk_job_master_level2_level1clone_location_id'), 'ytk_job_master_level2', ['level1clone_location_id'], unique=False)
    op.create_index(op.f('ix_ytk_job_master_level2_level1clone_plate_barcode'), 'ytk_job_master_level2', ['level1clone_plate_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_job_master_level2_part_id'), 'ytk_job_master_level2', ['part_id'], unique=False)
    op.create_index(op.f('ix_ytk_job_master_level2_sample_number'), 'ytk_job_master_level2', ['sample_number'], unique=False)
    op.create_index(op.f('ix_ytk_job_master_level2_unique_job_id'), 'ytk_job_master_level2', ['unique_job_id'], unique=False)
    op.create_index(op.f('ix_ytk_job_master_level2_uploaded_filename'), 'ytk_job_master_level2', ['uploaded_filename'], unique=False)
    op.create_table('ytk_stitch_clone',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_job_id', sa.String(length=64), nullable=True),
    sa.Column('clone_plate_well_id_96', sa.String(length=64), nullable=True),
    sa.Column('well_number_96', sa.Integer(), nullable=True),
    sa.Column('stitch_well_id', sa.String(length=64), nullable=True),
    sa.Column('stitch_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('clone_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('stitch_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ytk_stitch_clone_clone_plate_barcode'), 'ytk_stitch_clone', ['clone_plate_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_clone_clone_plate_well_id_96'), 'ytk_stitch_clone', ['clone_plate_well_id_96'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_clone_stitch_id'), 'ytk_stitch_clone', ['stitch_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_clone_stitch_plate_barcode'), 'ytk_stitch_clone', ['stitch_plate_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_clone_stitch_well_id'), 'ytk_stitch_clone', ['stitch_well_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_clone_unique_job_id'), 'ytk_stitch_clone', ['unique_job_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_clone_well_number_96'), 'ytk_stitch_clone', ['well_number_96'], unique=False)
    op.create_table('ytk_stitch_enzyme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_job_id', sa.String(length=64), nullable=True),
    sa.Column('stitch_well_id', sa.String(length=64), nullable=True),
    sa.Column('stitch_barcode', sa.String(length=64), nullable=True),
    sa.Column('stitch_id', sa.String(length=64), nullable=True),
    sa.Column('transfer_volume', sa.Integer(), nullable=True),
    sa.Column('enzyme_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('enzyme_plate_well_id', sa.String(length=64), nullable=True),
    sa.Column('enzyme_plate_number', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ytk_stitch_enzyme_enzyme_plate_barcode'), 'ytk_stitch_enzyme', ['enzyme_plate_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_enzyme_enzyme_plate_number'), 'ytk_stitch_enzyme', ['enzyme_plate_number'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_enzyme_enzyme_plate_well_id'), 'ytk_stitch_enzyme', ['enzyme_plate_well_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_enzyme_stitch_barcode'), 'ytk_stitch_enzyme', ['stitch_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_enzyme_stitch_id'), 'ytk_stitch_enzyme', ['stitch_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_enzyme_stitch_well_id'), 'ytk_stitch_enzyme', ['stitch_well_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_enzyme_transfer_volume'), 'ytk_stitch_enzyme', ['transfer_volume'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_enzyme_unique_job_id'), 'ytk_stitch_enzyme', ['unique_job_id'], unique=False)
    op.create_table('ytk_stitch_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_job_id', sa.String(length=64), nullable=True),
    sa.Column('stitch_id', sa.String(length=64), nullable=True),
    sa.Column('clip_number', sa.Integer(), nullable=True),
    sa.Column('clip_batch_number', sa.Integer(), nullable=True),
    sa.Column('concatenated_clip_id', sa.String(length=64), nullable=True),
    sa.Column('clip_well_id', sa.String(length=64), nullable=True),
    sa.Column('clip_barcode', sa.String(length=64), nullable=True),
    sa.Column('stitch_well_id', sa.String(length=64), nullable=True),
    sa.Column('stitch_plate_barcode', sa.String(length=64), nullable=True),
    sa.Column('stitch_plate_number', sa.Integer(), nullable=True),
    sa.Column('transfer_volume', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ytk_stitch_list_clip_barcode'), 'ytk_stitch_list', ['clip_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_clip_batch_number'), 'ytk_stitch_list', ['clip_batch_number'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_clip_number'), 'ytk_stitch_list', ['clip_number'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_clip_well_id'), 'ytk_stitch_list', ['clip_well_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_concatenated_clip_id'), 'ytk_stitch_list', ['concatenated_clip_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_stitch_id'), 'ytk_stitch_list', ['stitch_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_stitch_plate_barcode'), 'ytk_stitch_list', ['stitch_plate_barcode'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_stitch_plate_number'), 'ytk_stitch_list', ['stitch_plate_number'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_stitch_well_id'), 'ytk_stitch_list', ['stitch_well_id'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_transfer_volume'), 'ytk_stitch_list', ['transfer_volume'], unique=False)
    op.create_index(op.f('ix_ytk_stitch_list_unique_job_id'), 'ytk_stitch_list', ['unique_job_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ytk_stitch_list_unique_job_id'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_transfer_volume'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_stitch_well_id'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_stitch_plate_number'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_stitch_plate_barcode'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_stitch_id'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_concatenated_clip_id'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_clip_well_id'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_clip_number'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_clip_batch_number'), table_name='ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_list_clip_barcode'), table_name='ytk_stitch_list')
    op.drop_table('ytk_stitch_list')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_unique_job_id'), table_name='ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_transfer_volume'), table_name='ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_stitch_well_id'), table_name='ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_stitch_id'), table_name='ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_stitch_barcode'), table_name='ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_enzyme_plate_well_id'), table_name='ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_enzyme_plate_number'), table_name='ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_enzyme_enzyme_plate_barcode'), table_name='ytk_stitch_enzyme')
    op.drop_table('ytk_stitch_enzyme')
    op.drop_index(op.f('ix_ytk_stitch_clone_well_number_96'), table_name='ytk_stitch_clone')
    op.drop_index(op.f('ix_ytk_stitch_clone_unique_job_id'), table_name='ytk_stitch_clone')
    op.drop_index(op.f('ix_ytk_stitch_clone_stitch_well_id'), table_name='ytk_stitch_clone')
    op.drop_index(op.f('ix_ytk_stitch_clone_stitch_plate_barcode'), table_name='ytk_stitch_clone')
    op.drop_index(op.f('ix_ytk_stitch_clone_stitch_id'), table_name='ytk_stitch_clone')
    op.drop_index(op.f('ix_ytk_stitch_clone_clone_plate_well_id_96'), table_name='ytk_stitch_clone')
    op.drop_index(op.f('ix_ytk_stitch_clone_clone_plate_barcode'), table_name='ytk_stitch_clone')
    op.drop_table('ytk_stitch_clone')
    op.drop_index(op.f('ix_ytk_job_master_level2_uploaded_filename'), table_name='ytk_job_master_level2')
    op.drop_index(op.f('ix_ytk_job_master_level2_unique_job_id'), table_name='ytk_job_master_level2')
    op.drop_index(op.f('ix_ytk_job_master_level2_sample_number'), table_name='ytk_job_master_level2')
    op.drop_index(op.f('ix_ytk_job_master_level2_part_id'), table_name='ytk_job_master_level2')
    op.drop_index(op.f('ix_ytk_job_master_level2_level1clone_plate_barcode'), table_name='ytk_job_master_level2')
    op.drop_index(op.f('ix_ytk_job_master_level2_level1clone_location_id'), table_name='ytk_job_master_level2')
    op.drop_index(op.f('ix_ytk_job_master_level2_job_master2_well_id'), table_name='ytk_job_master_level2')
    op.drop_index(op.f('ix_ytk_job_master_level2_job_master2_barcode'), table_name='ytk_job_master_level2')
    op.drop_table('ytk_job_master_level2')
    # ### end Alembic commands ###
