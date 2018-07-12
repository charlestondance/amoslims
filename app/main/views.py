from flask import redirect, request, url_for, flash, render_template, jsonify, Response
from . import main
from ..models import ConsumableDB, Permission, ProjectTable, JobTable, project_task, JobTypes, ytk_design, tube_storage
from .. import db
from .forms import AddInventoryItem, EditItem, AddProject, AddJob, ProjectLaunchpadForm, AddJobType, \
    DesignLaunchpadForm, AddTubeItem
from flask_login import login_required
from ..decorators import permission_required
import operator
import base36


@main.route('/')
def index():
    # get a list of projects
    projects = ProjectTable.query.all()

    # create a list of the projects for the drop down
    projects_list = []
    for x in projects:
        projects_list.append(x.project_number)

    return render_template('index.html', Permission=Permission, projects_list=projects_list)


@main.route('/registeritem', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def register_item():
    form = AddInventoryItem()
    print('register item')
    if form.validate_on_submit():
        flash('item added')
        item_add = ConsumableDB(item_name=form.item_name.data, supplier=form.supplier.data,
                                ref_number=form.ref_number.data, price=form.price.data, location_1=form.location_1.data,
                                location_2=form.location_2.data, Position=form.Position.data)

        db.session.add(item_add)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('registeritem.html', form=form)


@main.route('/showitem', methods=['GET'])
@login_required
def show_items():
    items = ConsumableDB.query.order_by(ConsumableDB.id)
    return render_template('showitems.html', items=items)


@main.route('/edititem/<string:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def edit_item(id):
    # this will take the id and allow the user to edit item

    item = ConsumableDB.query.filter_by(id=id).first_or_404()
    form = EditItem(item=item)
    if form.validate_on_submit():
        item.item_name = form.item_name.data
        item.supplier = form.supplier.data
        item.ref_number = form.ref_number.data
        item.price = form.price.data
        item.location_1 = form.location_1.data
        item.location_2 = form.location_2.data
        item.Position = form.Position.data

        db.session.commit()
        flash('Item updated')
        return redirect(url_for('main.index'))

    # set the defaults
    form.item_name.data = item.item_name
    form.supplier.data = item.supplier
    form.ref_number.data = item.ref_number
    form.price.data = item.price
    form.location_1.data = item.location_1
    form.location_2.data = item.location_2
    form.Position.data = item.Position

    return render_template('registeritem.html', form=form, item=item)


@main.route('/registerproject', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def register_project():
    form = AddProject()

    if form.validate_on_submit():
        flash('item added')
        item_add = ProjectTable(project_number=form.project_number.data)

        db.session.add(item_add)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('registeritem.html', form=form)


@main.route('/registerjobtype', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def register_job_type():
    form = AddJobType()

    if form.validate_on_submit():
        flash('item added')
        item_add = JobTypes(job_type=form.job_type.data)

        db.session.add(item_add)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('registeritem.html', form=form)


@main.route('/raisejob', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def raise_job():
    form = AddJob()
    projects = ProjectTable.query.all()

    # create a list of the projects for the dropdown
    projects_list = []
    for x in projects:
        projects_list.append([x.project_number, x.project_number])

    form.project_number.choices = projects_list

    # create a list of the job types for the dropdown
    job_type_query = JobTypes.query.all()
    job_type_list = []

    for job_type_row in job_type_query:
        job_type_list.append([job_type_row.job_type, job_type_row.job_type])

    form.choose_job_type.choices = job_type_list

    if form.validate_on_submit():
        # find larges job id to increment then create unique job number based on base 36 integer
        rows = JobTable.query.order_by(JobTable.job_integer.desc()).first()

        if rows:
            unique_job_id_base36 = base36.dumps(rows.job_integer+1)
            if len(unique_job_id_base36) < 4:
                padding = ''
                for pad in range(0, 4-len(unique_job_id_base36)):
                    padding = padding + '0'

            unique_job_id = 'J'+padding+base36.dumps(rows.job_integer+1)
            job_integer = rows.job_integer+1
        else:
            unique_job_id = 'J0001'
            job_integer = 1

        flash('job ' + unique_job_id + ' added')
        item_add = JobTable(project_number=form.project_number.data, job_integer=job_integer,
                            unique_job_id=unique_job_id, job_type=form.choose_job_type.data)
        db.session.add(item_add)

        if form.choose_job_type.data == 'YTK':
            item_add = project_task(unique_job_id=unique_job_id, task='uploaddesign', status="pending", locked=0)
            db.session.add(item_add)
            item_add = project_task(unique_job_id=unique_job_id, task='uploadjobmaster', status="pending", locked=0)
            db.session.add(item_add)
            item_add = project_task(unique_job_id=unique_job_id, task='uploadjobmaster_level_2', status="pending",
                                    locked=0)
            db.session.add(item_add)
            item_add = project_task(unique_job_id=unique_job_id, task='in_silico_assembly', status="pending", locked=0)
            db.session.add(item_add)

        elif form.choose_job_type.data == 'M-CELLFREE':
            item_add = project_task(unique_job_id=unique_job_id, task='uploaddesign', status="pending", locked=0)
            db.session.add(item_add)

        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('registeritem.html', form=form)


@main.route('/_add_numbers', methods=['GET', 'POST'])
@login_required
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@main.route('/adding_numbers', methods=['GET', 'POST'])
@login_required
def add_numbers_page():
    return render_template('add_numbers.html')


@main.route('/makejmpdesignlaunchpad', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def makejmpdesignlaunchpad():
    return render_template('jmpdesign.html')


@main.route('/downloaddesign', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def downloaddesignlaunchpad():
    # once the design is in the database then you get the choice to download the CSV or delete it per experiment id
    form = DesignLaunchpadForm()

    dict_of_designs = {}
    designs_choices = []

    # ytk
    sql = "SELECT experiment_id FROM ytk_virgin_design GROUP BY experiment_id"
    designs = db.engine.execute(sql)

    # create a list of the projects for the dropdown
    for design in designs:
        dict_of_designs[design.experiment_id] = 'YTK'
        designs_choices.append([design.experiment_id, design.experiment_id, ])

    form.design_name.choices = designs_choices
    form.design_action.choices = [['--Select--', '--Select--'], ['Download', 'Download'], ['Delete', 'Delete']]

    if form.validate_on_submit():
        if form.design_action.data == 'Delete':
            delete_v_design(experiment_id=form.design_name.data, experiment_type=dict_of_designs[form.design_name.data])
            flash("design deleted")
            return render_template('download_design.html', form=form)
        elif form.design_action.data == 'Download':
            # download the unoptimised design
            if dict_of_designs[form.design_name.data] == 'YTK':
                sql = """Select stitch_id, clip_id, part_id, part_name, assembly_level from ytk_virgin_design WHERE experiment_id=%s ORDER BY stitch_id,clip_id"""

            rows = db.engine.execute(sql, form.design_name.data)

            keys = rows.keys()

            list_of_dict = []
            for y in rows:
                row_dict = {}
                for x in range(0, len(keys)):
                    row_dict[keys[x]] = str(y[x])

                list_of_dict.append(row_dict)

            # create the header for the csv file
            header = {}
            for k, v in list_of_dict[0].items():
                header_list = list(k)
                header_list[0] = header_list[0].upper()

                k = "".join(header_list)

                header[k] = k

            list_of_dict.insert(0, header)

            return Response(generate_and_yield_row(list_of_dict), mimetype='text/csv')

    return render_template('download_design.html', form=form)


@main.route('/delete_v_design', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def delete_v_design(experiment_id, experiment_type):
    # delete the unoptimised design
    if experiment_type == 'YTK':
        db.engine.execute("DELETE FROM ytk_virgin_design WHERE experiment_id=%s", (experiment_id))
    db.session.commit()


@main.route('/project_launchpad/<string:projectnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def project_launchpad(projectnumber):

    form = ProjectLaunchpadForm()
    rows = JobTable.query.with_entities(JobTable.unique_job_id).filter_by(project_number=projectnumber)
    job_list = []
    for x in rows:
        job_list.append([x[0], x[0]])

    form.jobnumber.choices = job_list
    if form.validate_on_submit():
        # check job type to return the appropriate job number
        check_job_type_query = JobTable.query.filter_by(unique_job_id=form.jobnumber.data).first()
        if check_job_type_query.job_type == 'YTK':
            return redirect(url_for('YTK.ytk_job_launchpad', jobnumber=form.jobnumber.data))
        if check_job_type_query.job_type == 'MCELLFREE':
            return redirect(url_for('main.mcellfree_job_launchpad', jobnumber=form.jobnumber.data))

    return render_template('project_launchpad.html', projectnumber=projectnumber, form=form)


@main.route('/mcellfree_job_launchpad/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def mcellfree_job_launchpad(jobnumber):
    # get project number
    project_number_query = JobTable.query.filter_by(unique_job_id=jobnumber).first()

    return render_template('mcellfree_job_launchpad.html', jobnumber=jobnumber,
                           project_number=project_number_query.project_number)


def make_job_task_list_ytk(qc_tasks):
    # works out the logic of the job tasks available depending on the completed steps
    if qc_tasks['uploaddesign'].status == "pending":
        job_task_choices = [['--Select--', '--Select--'], ['Upload Design', 'Upload Design']]
    elif qc_tasks['uploaddesign'].status == "complete" and qc_tasks['uploadjobmaster'].status == 'pending' \
            and qc_tasks['in_silico_assembly'].status == 'pending':
        job_task_choices = [['--Select--', '--Select--'], ['Upload Job Master Processed', 'Upload Job Master Processed'],
                            ['In Silico Assembly', 'In Silico Assembly']]
    elif qc_tasks['uploaddesign'].status == "complete" and qc_tasks['uploadjobmaster'].status == 'complete' and \
            qc_tasks['in_silico_assembly'].status == 'pending':
        job_task_choices = [['--Select--', '--Select--'], ['In Silico Assembly', 'In Silico Assembly']]
    elif qc_tasks['uploaddesign'].status == "complete" and qc_tasks['uploadjobmaster'].status == 'pending' and \
            qc_tasks['in_silico_assembly'].status == 'complete':
        job_task_choices = [['--Select--', '--Select--'], ['Upload Job Master Processed',
                                                           'Upload Job Master Processed']]
    elif qc_tasks['uploaddesign'].status == "complete" and qc_tasks['uploadjobmaster'].status == 'complete':
        job_task_choices = [['--Select--', '--Select--'], ['Upload Level 2 Job Master Processed',
                                                           'Upload Level 2 Job Master Processed']]

    return job_task_choices


@main.route('/render_csv/<string:jobname_filename>.csv', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def render_csv(jobname_filename):

    # element 0 is the table
    split_jobname_filename = jobname_filename.split("_", 1)

    # ytk jobmaster
    if split_jobname_filename[1] == 'YM':
        sql = "SELECT unique_job_id, part_id, sample_number, storage_location_id, storage_plate_barcode FROM " \
              "ytk_job_master WHERE unique_job_id=%s"
        rows = db.engine.execute(sql, split_jobname_filename[0])
    # ytk clip
    elif split_jobname_filename[1] == 'YCL':
        sql = """SELECT
                unique_job_id AS unique_job_id,
                concatenated_part_id AS part_id,
                job_master_well_id AS Source_Well,
                job_master_barcode AS Source_Plate_Barcode,
                clip_well_id AS Destination_Well,
                clip_barcode AS Destination_Plate_Barcode,
                concatenated_clip_id AS Clip_id,
                transfer_volume as Transfer_Volume
              FROM ytk_clip_list WHERE unique_job_id=%s"""
        rows = db.engine.execute(sql, split_jobname_filename[0])

    # ytk clip enzyme
    elif split_jobname_filename[1] == 'YCLE':
        sql = """Select
                unique_job_id AS unique_job_id,
                enzyme_plate_well_id AS Source_Well,
                enzyme_plate_barcode AS Source_Plate_Barcode,
                clip_well_id AS Destination_Well,
                clip_barcode AS Destination_Plate_Barcode,
                concatenated_clip_id AS Clip_id,
                transfer_volume as Transfer_Volume
                From
                ytk_clip_enzyme WHERE unique_job_id=%s ORDER BY concatenated_clip_id"""

        rows = db.engine.execute(sql, split_jobname_filename[0])

    # ytk clip Clone
    elif split_jobname_filename[1] == 'YCLC':
        sql = """Select
                clip_id,
                unique_job_id,
                clone_plate_well_id_96,
                clone_plate_barcode
                From
                ytk_clip_clone WHERE unique_job_id=%s ORDER BY clone_plate_barcode, well_number_96"""

        rows = db.engine.execute(sql, split_jobname_filename[0])

    # ytk jobmaster2
    elif split_jobname_filename[1] == 'YM2':
        sql = "SELECT unique_job_id, part_id, sample_number, level1clone_location_id AS storage_location_id , level1clone_plate_barcode AS storage_plate_barcode FROM ytk_job_master_level2 WHERE unique_job_id=%s ORDER BY part_id, sample_number"
        rows = db.engine.execute(sql, split_jobname_filename[0])

    # ytkstitch
    elif split_jobname_filename[1] == 'YS':
        sql = """Select
                    unique_job_id AS unique_job_id,
                    clip_well_id AS Source_Well,
                    clip_barcode AS Source_Plate_Barcode,
                    stitch_well_id AS Destination_Well,
                    stitch_plate_barcode AS Destination_Plate_Barcode,
                    stitch_id AS stitch_id,
                    transfer_volume as Transfer_Volume,
                    concatenated_clip_id AS Clip_id
                    From
                    ytk_stitch_list WHERE unique_job_id=%s ORDER BY stitch_id"""

        rows = db.engine.execute(sql, split_jobname_filename[0])

    # ytk stitch buffer
    elif split_jobname_filename[1] == 'YSE':
        sql = """Select
                    unique_job_id AS unique_job_id,
                    enzyme_plate_well_id AS Source_Well,
                    enzyme_plate_barcode AS Source_Plate_Barcode,
                    stitch_well_id AS Destination_Well,
                    stitch_barcode AS Destination_Plate_Barcode,
                    stitch_id AS stitch_id,
                    transfer_volume as Transfer_Volume
                    From
                    ytk_stitch_enzyme WHERE unique_job_id=%s ORDER BY stitch_id"""

        rows = db.engine.execute(sql, split_jobname_filename[0])

    # ytk Stitch Clone
    elif split_jobname_filename[1] == 'YSC':
        sql = """Select
                        stitch_id,
                        unique_job_id,
                        clone_plate_well_id_96,
                        clone_plate_barcode
                        From
                        ytk_stitch_clone WHERE unique_job_id=%s ORDER BY stitch_plate_barcode, well_number_96"""

        rows = db.engine.execute(sql, split_jobname_filename[0])

    # parts_database
    elif split_jobname_filename[1] == 'PDB':
        sql = """Select * From partstable ORDER BY part_number"""
        rows = db.engine.execute(sql, split_jobname_filename[0])

    keys = rows.keys()
    list_of_dict = []
    for y in rows:
        row_dict = {}
        for x in range(0, len(keys)):
            row_dict[keys[x]] = str(y[x])

        list_of_dict.append(row_dict)

    # create the header for the csv file
    header = {}
    for k, v in list_of_dict[0].items():
        header_list = list(k)
        header_list[0] = header_list[0].upper()
        for letter in range(0, len(header_list)):
            if header_list[letter] == '_':
                header_list[letter] = " "
                header_list[letter+1] = header_list[letter+1].upper()

        k = "".join(header_list)

        header[k] = k

    list_of_dict.insert(0, header)

    return Response(generate_and_yield_row(list_of_dict), mimetype='text/csv')


def generate_and_yield_row(list_of_dict):

    # sorts the dict into tuples and yields the row
    for row in list_of_dict:
        li = []
        sorted_row = sorted(row.items(), key=operator.itemgetter(0))

        for r in sorted_row:
            val = r[1] or ''
            li.append(str(val.replace(',', '')))
        yield ','.join(li) + '\n'


@main.route('/registertubeitem', methods=['GET', 'POST'])
def registertubeitem():
    form = AddTubeItem()

    if form.validate_on_submit():
        flash('item added')
        item_add = tube_storage(item_name=form.name.data, tube_barcode=form.tube_barcode.data,
                                rack_barcode=form.rack_barcode.data, supplier=form.supplier.data,
                                location_id1=form.locationid1.data, item_decription=form.item_decription.data)

        db.session.add(item_add)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('registeritem.html', form=form)


@main.route('/amos/api/v1.0/request_tube/', methods=['GET', 'POST'])
def request_tube_api():
    # api version of getting the info from a tube
    find_tube = tube_storage.query.filter_by(tube_barcode=request.headers['tube_barcode']).first()

    if find_tube is None:
        find_tube_dict = {'tube_barcode': 'Not Found', 'item_name': 'Not Found',
                          'ref_number': 'Not Found',
                          'ldf_id': 'Not Found', 'ice_id': 'Not Found', 'dna_id': 'Not Found',
                          'supplier': 'Not Found',
                          'tube_barcode': 'Not Found', 'rack_barcode': 'Not Found',
                          'Position': 'Not Found',
                          'location_id1': 'Not Found', 'location_id2': 'not Found', 'item_description': 'Not Found'}
    else:
        find_tube_dict = {'tube_barcode': find_tube.tube_barcode, 'item_name': find_tube.item_name,
                          'ref_number': find_tube.ref_number, 'ldf_id': find_tube.ldf_id, 'ice_id': find_tube.ice_id,
                          'dna_id': find_tube.dna_id, 'supplier': find_tube.supplier,
                          'tube_barcode': find_tube.tube_barcode, 'rack_barcode': find_tube.rack_barcode,
                          'Position': find_tube.Position, 'location_id1': find_tube.location_id1,
                          'location_id2': find_tube.location_id2, 'item_description': find_tube.item_description}

    return jsonify(find_tube_dict)


@main.route('/amos/api/v1.0/register_tube/', methods=['GET', 'POST'])
def register_tube_api():
    # api version to update info from a tube
    print(request.headers['tube_barcode'])
    print(request.headers['item_name'])
    print(request.headers['item_description'])
    success = 'Something Fails'

    # check LDF-id
    item_number = 1
    if request.headers['ldf_id'] == "":
        print('not present')
    else:
        print('have an ldf id')
        print(request.headers['ldf_id'])
        request.headers['ldf_id']
        # ldf id must be 10 characters and start with LDF
        if len(request.headers['ldf_id']) != 10 or 'LDF-' not in request.headers['ldf_id']:
            return 'Error with LDF ID'
        else:
            # find the amound of padding in ldf
            ldf_padder = 'LDF-'

            ldf_padder_counter = 0
            while ldf_padder in request.headers['ldf_id']:
                ldf_padder += '0'
                ldf_padder_counter += 1

            last_letters = 10-(ldf_padder_counter+3)
            print(ldf_padder[0:ldf_padder_counter+3])
            print(request.headers['ldf_id'][-last_letters:])

            item_number = request.headers['ldf_id'][-last_letters:]

    find_tube = tube_storage.query.filter_by(tube_barcode=request.headers['tube_barcode']).first()
    if find_tube == None:
        tube_add = tube_storage(tube_barcode=request.headers['tube_barcode'],
                                item_description=request.headers['item_description'],
                                item_name=request.headers['item_name'], ldf_id=request.headers['ldf_id'],
                                ref_number=item_number)
        db.session.add(tube_add)
        success = 'Created new entry'
    else:
        find_tube.item_name = request.headers['item_name']
        find_tube.item_description = request.headers['item_description']
        find_tube.ldf_id = request.headers['ldf_id']
        find_tube.ref_number = item_number
        success = 'Updated entry'
    db.session.commit()

    return success


@main.route('/showtubes', methods=['GET'])
@login_required
def show_tubes():
    page = request.args.get('page', 1, type=int)
    pagination = tube_storage.query.order_by(tube_storage.id).paginate(page, per_page=15, error_out=False)
    compound = pagination.items

    # return a value for the big jump for next page so long as it doesnt go over the maximum
    page_10 = pagination.next_num+9
    if page_10 > pagination.pages:
        pageincrement = pagination.pages
    else:
        pageincrement = page_10

    # check the decrease doesnt go below 1
    page_decrement = page - 10
    if page_decrement < 1:
        page_decrement = 1

    return render_template('showtubetable.html', compound=compound, pagination=pagination, pageincrement=pageincrement,
                           page_decrement=page_decrement)


@main.route('/edittube/<string:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def edit_tube(id):
    """this will take the  id and allow the user to edit item
    """

    item = tube_storage.query.filter_by(id=id).first_or_404()
    form = AddTubeItem(item=item)

    if form.validate_on_submit():
        item.item_name = form.name.data
        item.tube_barcode = form.tube_barcode.data
        item.rack_barcode = form.rack_barcode.data
        item.supplier = form.supplier.data
        item.location_id1 = form.locationid1.data
        item.item_description = form.item_description.data

        db.session.commit()
        flash('Item updated')
        return redirect(url_for('main.index'))

    # set the defaults
    form.name.data = item.item_name
    form.tube_barcode.data = item.tube_barcode
    form.rack_barcode.data = item.rack_barcode
    form.supplier.data = item.supplier
    form.locationid1.data = item.location_id1
    form.item_description.data = item.item_description

    return render_template('registeritem.html', form=form, item=item)


@main.route('/about_amos', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def about_amos():

    unique_job_count = 0
    unique_stitch_count = 0

    # get list of unique ytk job ids
    unique_job_ids = ytk_design.query.distinct(ytk_design.unique_job_id).all()
    unique_job_count += len(unique_job_ids)

    # get list of unique ytk stitch ids
    for job in unique_job_ids:
        unique_stitch_ids = ytk_design.query.filter_by(unique_job_id=job.unique_job_id).distinct(ytk_design.stitch_id).all()
        unique_stitch_count += len(unique_stitch_ids)

    return render_template('about_amos.html', unique_job_count=unique_job_count, unique_stitch_count=unique_stitch_count)

