from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import PartsTable


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterConsumable(Form):
    consumable = StringField('Batch ID', validators=[DataRequired(), Length(1, 64)])


class AddInventoryItem(Form):
    item_name = StringField('item name', validators=[DataRequired(), Length(1, 64)])
    supplier = StringField('supplier', validators=[DataRequired(), Length(1, 64)])
    ref_number = StringField('supplier_ref', validators=[DataRequired(), Length(1, 64)])
    price = StringField('Price', validators=[DataRequired(), Length(1, 64)])
    location_1 = StringField('Location_1', validators=[DataRequired(), Length(1, 64)])
    location_2 = StringField('location_2', validators=[DataRequired(), Length(1, 64)])
    Position = StringField('Position', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit Item')


class AddPart(Form):
    part_id = StringField('Part id', validators=[DataRequired(), Length(1, 64)])
    part_name = StringField('Part Name', validators=[DataRequired(), Length(1, 64)])
    part_class = StringField('Part Class', validators=[DataRequired(), Length(1, 64)])
    part_type = StringField('Part Type', validators=[DataRequired(), Length(1, 64)])
    relative_position = StringField('Relative Position', validators=[DataRequired(), Length(1, 64)])
    level = StringField('Level', validators=[DataRequired(), Length(1, 64)])
    offset = StringField('offset', validators=[DataRequired(), Length(1, 64)])
    project = StringField('Project', validators=[DataRequired(), Length(1, 64)])
    sequence = StringField('Sequence', validators=[DataRequired(), Length(1, 256)])
    submit = SubmitField('Submit Item')


class EditItem(Form):
    item_name = StringField('item name', validators=[DataRequired(), Length(1, 64)])
    supplier = StringField('supplier', validators=[DataRequired(), Length(1, 64)])
    ref_number = StringField('supplier_ref', validators=[DataRequired(), Length(1, 64)])
    price = StringField('Price', validators=[DataRequired(), Length(1, 64)])
    location_1 = StringField('Location_1', validators=[DataRequired(), Length(1, 64)])
    location_2 = StringField('location_2', validators=[DataRequired(), Length(1, 64)])
    Position = StringField('Position', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit Item')


class AddProject(Form):
    project_number = StringField('project number', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit Item')


class AddJobType(Form):
    job_type = StringField('Job Type', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit Item')


class AddJob(Form):
    project_number = SelectField('Project Number')
    choose_job_type = SelectField('Job Type')
    submit = SubmitField('Submit Item')


class YtkDesignForm(Form):
    cds_partA = StringField('CDS A')
    cds_partB = StringField('CDS B')
    cds_partC = StringField('CDS C')
    cds_partD = StringField('CDS D')
    jmp_file = FileField('Upload JMP File')
    experiment_id = StringField('Experiment ID')
    jobset_parts = SelectField('Parts Jobset')
    jobset_cassetes = SelectField('casettes Jobset')
    submit = SubmitField('Submit Item')


class ProjectLaunchpadForm(Form):
    jobnumber = SelectField('Job Number')
    submit = SubmitField('Next')


class JobLaunchpadForm(Form):
    job_tasks = SelectField('Task')
    compounds = FileField('Upload File')
    submit = SubmitField('Go!')


class UploadCSVfile(Form):
    compounds = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DesignLaunchpadForm(Form):
    design_name = SelectField('Design')
    design_action = SelectField('Action')
    submit = SubmitField('Go!')


class AddTubeItem(Form):
    name = StringField('Name')
    tube_barcode = StringField('Tube Barcode')
    rack_barcode = StringField('Rack Barcode')
    supplier = StringField('Supplier')
    locationid1 = StringField('Location')
    item_description = TextAreaField('Description')
    submit = SubmitField('Submit Item')


class ProjectSearch(Form):
    select = QuerySelectField('Project Number', validators=[DataRequired()],
                              query_factory=lambda: PartsTable.query.distinct(PartsTable.project_number),
                              get_label='project_number')
    submit = SubmitField('Submit')

