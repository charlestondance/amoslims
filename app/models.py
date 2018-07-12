import csv
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {'User': (Permission.MAKE_LIST, True),
                 'SuperUser': (Permission.MAKE_LIST | Permission.EDIT_DB, False),
                 'Administrator': (0xFF, False)
                 }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Permission:
    EDIT_DB = 0x01
    MAKE_LIST = 0x02
    ADMINISTER = 0x80


class ConsumableDB(db.Model):
    __tablename__ = 'consumable'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(64), unique=False, index=True)
    ref_number = db.Column(db.String(64), unique=False, index=True)
    supplier = db.Column(db.String(64), unique=False, index=True)
    price = db.Column(db.Float, unique=False, index=True)
    location_1 = db.Column(db.String(64), unique=False, index=True)
    location_2 = db.Column(db.String(64), unique=False, index=True)
    Position = db.Column(db.String(64), unique=False, index=True)

    def __repr__(self):
        return '<consumable_id %r>' % self.id


class PartsTable(db.Model):
    __tablename__ = 'partstable'
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(64), unique=True, index=True)
    part_name = db.Column(db.String(64), unique=False, index=True)
    part_class = db.Column(db.String(64), unique=False, index=True)
    part_type = db.Column(db.String(64), unique=False, index=True)
    relative_position = db.Column(db.String(64), unique=False, index=True)
    level = db.Column(db.Integer, primary_key=False, index=True)
    offset = db.Column(db.Integer, primary_key=False, index=True)
    project_number = db.Column(db.String(64), primary_key=False, index=True)
    job_set = db.Column(db.String(64), primary_key=False, index=True)
    sequence = db.Column(db.String(256), unique=False, index=True)
    part_method = db.Column(db.String(64), unique=False, index=True)
    composite_part = db.Column(db.Integer, primary_key=False, index=True)
    external_id = db.Column(db.String(64), unique=False, index=True)
    part_number = db.Column(db.Integer, primary_key=False, index=True)

    def __repr__(self):
        return '<part_id %r>' % self.id


class PartsBatchTable(db.Model):
    __tablename__ = 'partsbatchtable'
    id = db.Column(db.Integer, primary_key=True)
    storage_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    storage_location_id = db.Column(db.String(64), unique=False, index=True)
    part_id = db.Column(db.String(64), index=True)
    part_number = db.Column(db.Integer, primary_key=False, index=True)
    batch_number = db.Column(db.Integer, primary_key=False, index=True)


class ProjectTable(db.Model):
    __tablename__ = 'projecttable'
    id = db.Column(db.Integer, primary_key=True)
    project_number = db.Column(db.String(64), unique=True, index=True)


class JobTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=True, index=True)
    project_number = db.Column(db.String(64), unique=False, index=True)
    job_integer = db.Column(db.Integer, primary_key=False, index=True)
    job_type = db.Column(db.String(64), unique=False, index=True)


class JobTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_type = db.Column(db.String(64), unique=True, index=True)


class project_task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    task = db.Column(db.String(64), unique=False, index=True)
    status = db.Column(db.String(64), unique=False, index=True)
    locked = db.Column(db.Integer, unique=False, index=True)


class quadrant_wells_lookup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    well_id_96 = db.Column(db.String(64), unique=False, index=True)
    well_id_384 = db.Column(db.String(64), unique=False, index=True)
    plate_number_96 = db.Column(db.Integer, unique=False, index=True)
    well_number_96 = db.Column(db.Integer, unique=False, index=True)
    well_number_384 = db.Column(db.Integer, unique=False, index=True)


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class ytk_virgin_design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stitch_id = db.Column(db.String(64), unique=False, index=True)
    clip_id = db.Column(db.String(64), unique=False, index=True)
    part_id = db.Column(db.String(64), index=True)
    part_name = db.Column(db.String(64), index=True)
    experiment_id = db.Column(db.String(64), index=True)
    assembly_level = db.Column(db.String(64), index=True)


class ytk_design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(64), unique=False, index=True)
    part_id_sample_id = db.Column(db.Integer, primary_key=False, index=True)
    clip_id = db.Column(db.String(64), unique=False, index=True)
    clip_id_batch_id = db.Column(db.Integer, primary_key=False, index=True)
    clip_id_sample_id = db.Column(db.Integer, primary_key=False, index=True)
    stitch_id = db.Column(db.String(64), unique=False, index=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    unique_clip_number = db.Column(db.Integer, primary_key=False, index=True)
    level = db.Column(db.Integer, primary_key=False, index=True)
    uploaded_filename = db.Column(db.String(64), unique=False, index=True)

    @staticmethod
    def upload_csv(filename, jobname, filename_for_db):

        error_list = []

        design_error_flag = False

        YTK_UPLOAD_DESIGN_KEY = ['Clip_id', 'Part_id', 'Part_name', 'Stitch_id', 'Assembly_level']

        # check no design exists
        query_design_table = ytk_design.query.filter_by(unique_job_id=jobname).first()
        if query_design_table is None:

            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile)

                dict_keys = reader.fieldnames
                # check dict keys match BASIC_UPLOAD_DESIGN_KEY
                if sorted(dict_keys) == sorted(YTK_UPLOAD_DESIGN_KEY):

                    for row in reader:
                        # check part ID exists in the database
                        query_parts_table = PartsTable.query.filter_by(part_id=row['Part_id']).first()
                        if query_parts_table is None:
                            error_list.append(row['Part_id'])

                        # add basic design to database
                        add_design = ytk_design(part_id=row['Part_id'], part_id_sample_id=1, clip_id=row['Clip_id'],
                                                clip_id_batch_id=1, stitch_id=row['Stitch_id'], unique_job_id=jobname,
                                                level=row['Assembly_level'], unique_clip_number=0,
                                                uploaded_filename=filename_for_db, clip_id_sample_id=1)
                        db.session.add(add_design)

                    db.session.commit()

                else:
                    error_list.append('key error')

        return error_list


class ytk_unique_clip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    clip_number = db.Column(db.Integer, unique=False, index=True)
    part_1_id = db.Column(db.String(64), unique=False, index=True)
    part_2_id = db.Column(db.String(64), unique=False, index=True)
    part_3_id = db.Column(db.String(64), unique=False, index=True)
    part_4_id = db.Column(db.String(64), unique=False, index=True)
    number_of_times_used = db.Column(db.Integer, unique=False, index=True)
    clip_batches_required = db.Column(db.Integer, unique=False, index=True)
    clip_id_job_id_no_batch_id = db.Column(db.String(64), unique=False, index=True)


class ytk_unique_part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    part_id = db.Column(db.String(64), unique=False, index=True)
    samples_required = db.Column(db.Integer, unique=False, index=True)
    number_of_times_used = db.Column(db.Integer, unique=False, index=True)
    total_volume_required = db.Column(db.Integer, unique=False, index=True)
    volume_per_part = db.Column(db.Integer, unique=False, index=True)


class ytk_job_master(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    part_id = db.Column(db.String(64), unique=False, index=True)
    job_master_well_id = db.Column(db.String(64), unique=False, index=True)
    job_master_barcode = db.Column(db.String(64), unique=False, index=True)
    sample_number = db.Column(db.Integer, unique=False, index=True)
    uploaded_filename = db.Column(db.String(64), unique=False, index=True)
    storage_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    storage_location_id = db.Column(db.String(64), unique=False, index=True)


class ytk_clip_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    part_id = db.Column(db.String(64), unique=False, index=True)
    concatenated_part_id = db.Column(db.String(64), unique=False, index=True)
    job_master_well_id = db.Column(db.String(64), unique=False, index=True)
    job_master_barcode = db.Column(db.String(64), unique=False, index=True)
    part_id_sample_number = db.Column(db.Integer, unique=False, index=True)
    clip_well_id = db.Column(db.String(64), unique=False, index=True)
    clip_barcode = db.Column(db.String(64), unique=False, index=True)
    concatenated_clip_id = db.Column(db.String(64), unique=False, index=True)
    clip_number = db.Column(db.Integer, unique=False, index=True)
    clip_batch_number = db.Column(db.Integer, unique=False, index=True)
    destination_plate_number = db.Column(db.Integer, unique=False, index=True)
    transfer_volume = db.Column(db.Integer, unique=False, index=True)


class ytk_clip_enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    clip_well_id = db.Column(db.String(64), unique=False, index=True)
    clip_barcode = db.Column(db.String(64), unique=False, index=True)
    concatenated_clip_id = db.Column(db.String(64), unique=False, index=True)
    clip_number = db.Column(db.Integer, unique=False, index=True)
    clip_batch_number = db.Column(db.Integer, unique=False, index=True)
    clip_plate_number = db.Column(db.Integer, unique=False, index=True)
    transfer_volume = db.Column(db.Integer, unique=False, index=True)
    enzyme_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    enzyme_plate_well_id = db.Column(db.String(64), unique=False, index=True)
    enzyme_plate_number = db.Column(db.String(64), unique=False, index=True)


class ytk_buffer_plate_wells(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    buffer_plate_well_id = db.Column(db.String(64), unique=False, index=True)
    loading_volume = db.Column(db.Float, unique=False, index=True)
    buffer_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    buffer_plate_number = db.Column(db.Integer, unique=False, index=True)
    buffer_name = db.Column(db.String(64), unique=False, index=True)


class ytk_clip_clone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    clone_plate_well_id_96 = db.Column(db.String(64), unique=False, index=True)
    well_number_96 = db.Column(db.Integer, unique=False, index=True)
    clip_well_id = db.Column(db.String(64), unique=False, index=True)
    clip_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    clone_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    clip_id = db.Column(db.String(64), unique=False, index=True)
    clip_id_no_batch = db.Column(db.String(64), unique=False, index=True)
    clip_id_job_id = db.Column(db.String(64), unique=False, index=True)
    clip_id_job_id_no_batch_id = db.Column(db.String(64), unique=False, index=True)


class ytk_job_master_level2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    part_id = db.Column(db.String(64), unique=False, index=True)
    job_master2_well_id = db.Column(db.String(64), unique=False, index=True)
    job_master2_barcode = db.Column(db.String(64), unique=False, index=True)
    sample_number = db.Column(db.Integer, unique=False, index=True)
    uploaded_filename = db.Column(db.String(64), unique=False, index=True)
    level1clone_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    level1clone_location_id = db.Column(db.String(64), unique=False, index=True)


class ytk_stitch_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    stitch_id = db.Column(db.String(64), unique=False, index=True)
    clip_number = db.Column(db.Integer, unique=False, index=True)
    clip_batch_number = db.Column(db.Integer, unique=False, index=True)
    concatenated_clip_id = db.Column(db.String(64), unique=False, index=True)
    clip_well_id = db.Column(db.String(64), unique=False, index=True)
    clip_barcode = db.Column(db.String(64), unique=False, index=True)
    stitch_well_id = db.Column(db.String(64), unique=False, index=True)
    stitch_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    stitch_plate_number = db.Column(db.Integer, unique=False, index=True)
    transfer_volume = db.Column(db.Integer, unique=False, index=True)


class ytk_stitch_enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    stitch_well_id = db.Column(db.String(64), unique=False, index=True)
    stitch_barcode = db.Column(db.String(64), unique=False, index=True)
    stitch_id = db.Column(db.String(64), unique=False, index=True)
    transfer_volume = db.Column(db.Integer, unique=False, index=True)
    enzyme_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    enzyme_plate_well_id = db.Column(db.String(64), unique=False, index=True)
    enzyme_plate_number = db.Column(db.String(64), unique=False, index=True)


class ytk_stitch_clone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_job_id = db.Column(db.String(64), unique=False, index=True)
    clone_plate_well_id_96 = db.Column(db.String(64), unique=False, index=True)
    well_number_96 = db.Column(db.Integer, unique=False, index=True)
    stitch_well_id = db.Column(db.String(64), unique=False, index=True)
    stitch_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    clone_plate_barcode = db.Column(db.String(64), unique=False, index=True)
    stitch_id = db.Column(db.String(64), unique=False, index=True)


class part_dna_sizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(64), unique=False, index=True)
    enzyme = db.Column(db.String(64), unique=False, index=True)
    size = db.Column(db.Integer, unique=False, index=True)
    cargo_number = db.Column(db.Integer, unique=False, index=True)


class tube_storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(64), unique=False, index=True)
    ref_number = db.Column(db.String(64), unique=False, index=True)
    ldf_id = db.Column(db.String(64), unique=False, index=True)
    ice_id = db.Column(db.String(64), unique=False, index=True)
    dna_id = db.Column(db.String(64), unique=False, index=True)
    supplier = db.Column(db.String(64), unique=False, index=True)
    tube_barcode = db.Column(db.String(64), unique=False, index=True)
    rack_barcode = db.Column(db.String(64), unique=False, index=True)
    Position = db.Column(db.String(64), unique=False, index=True)
    location_id1 = db.Column(db.String(64), unique=False, index=True)
    location_id2 = db.Column(db.String(64), unique=False, index=True)
    item_description = db.Column(db.Text, unique=False, index=True)


class jmp_tracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), unique=False, index=True)
    project_number = db.Column(db.String(64), unique=False, index=True)
    job_number = db.Column(db.String(64), unique=False, index=True)
    item_description = db.Column(db.Text, unique=False, index=True)
    item_count = db.Column(db.Integer, unique=False, index=True)