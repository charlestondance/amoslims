from . import parts_database
from .. import db
from ..models import PartsBatchTable, PartsTable, Permission, part_dna_sizes
from flask import render_template, flash, url_for, request, redirect
from flask_login import login_required
from ..decorators import permission_required
from ..main.forms import ProjectSearch
from app.main.forms import AddPart, UploadCSVfile
import json
import plotly
from werkzeug.utils import secure_filename
from app.main.database_helper_functions import upload_parts_to_table, upload_sizes_to_table, \
    upload_uploadicelink_to_table
from app.main.jbei_ice_functions import do_virtual_cutter


@parts_database.route('/registerpart', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def register_part():
    form = AddPart()
    if form.validate_on_submit():
        flash('item added')
        item_add = PartsTable(part_id=form.part_id.data, part_name=form.part_name.data, part_class=form.part_class.data,
                              part_type=form.part_type.data, relative_position=form.relative_position.data,
                              level=form.level.data, offset=form.offset.data, project=form.project.data,
                              sequence=form.sequence.data)

        db.session.add(item_add)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('registeritem.html', form=form)


@parts_database.route('/searchcompound', methods=['GET', 'POST'])
@login_required
def compounds_search():
    form = ProjectSearch(request.form)
    if form.validate_on_submit():
        search_string = form.select.data.project_number

        return redirect(url_for('parts_database.show_compound', search_string=search_string))

    return render_template('parts_database/search_compounds.html', form=form)


@parts_database.route('/showcompound/<search_string>', methods=['GET'])
@login_required
def show_compound(search_string):
    page = request.args.get('page', 1, type=int)
    pagination = PartsTable.query.filter_by(project_number=search_string).order_by(PartsTable.part_number).paginate(
        page, per_page=15, error_out=False)
    compound = pagination.items

    page_10 = 10
    if page_10 > pagination.pages:
        pageincrement = pagination.pages
    else:
        pageincrement = page_10

    # check the decrease doesnt go below 1
    page_decrement = page - 10
    if page_decrement < 1:
        page_decrement = 1

    return render_template('parts_database/showpartstable.html', compound=compound, pagination=pagination,
                           pageincrement=pageincrement, page_decrement=page_decrement, search_string=search_string)


@parts_database.route('/showbatch/<string:part_number>', methods=['GET'])
@login_required
def show_part_batch(part_number):
    # get the batch info and return the batchviewpage
    batches = PartsBatchTable.query.filter_by(part_number=int(part_number)).order_by(PartsBatchTable.batch_number)
    part_info = PartsTable.query.filter_by(part_number=int(part_number)).first()
    part_sizes = part_dna_sizes.query.filter_by(part_id=part_info.part_id).all()

    # test plolty
    graphs = [
        dict(
            data=[
                dict(
                    x=[1, 2, 3],
                    y=[10, 20, 30],
                    type='scatter'
                ),
            ],
            layout=dict(
                title='first graph'
            )
        )]

    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('parts_database/showpartbatches.html', batches=batches, part_info=part_info,
                           part_sizes=part_sizes, ids=ids, graphJSON=graphJSON)


@parts_database.route('/editpart/<string:id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def edit_part(id):
    """this will take the  id and allow the user to edit item
    """

    item = PartsTable.query.filter_by(id=id).first_or_404()
    form = AddPart(item=item)
    if form.validate_on_submit():
        item.part_id = form.part_id.data
        item.part_name = form.part_name.data
        item.part_class = form.part_class.data
        item.part_type = form.part_type.data
        item.relative_position = form.relative_position.data
        item.level = form.level.data
        item.offset = form.offset.data
        item.project = form.project.data
        item.sequence = form.sequence.data

        db.session.commit()
        flash('Item updated')
        return redirect(url_for('main.index'))

    # set the defaults
    form.part_id.data = item.part_id
    form.part_name .data = item.part_name
    form.part_class.data = item.part_class
    form.part_type.data = item.part_type
    form.relative_position.data = item.relative_position
    form.level.data = item.level
    form.offset.data = item.offset
    form.project.data = item.project_number
    form.sequence.data = item.sequence

    return render_template('registeritem.html', form=form, item=item)


@parts_database.route('/uploadpartscsv', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def uploadpartscsv():
    """upload csv files of compounds to the database"""
    form = UploadCSVfile()
    if form.validate_on_submit():
        filename = secure_filename(form.compounds.data.filename)
        form.compounds.data.save("app/uploads/" + filename)
        filename_read = "app/uploads/" + filename

        upload_successful = upload_parts_to_table(filename_read=filename_read)
        if upload_successful:

            flash('Parts Database updated')
        else:
            flash('there is a ploblem with the csv')
        return redirect(url_for('main.index'))

    return render_template('parts_database/uploadpartcsv.html', form=form)


@parts_database.route('/uploadsizesscsv', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def uploadsizesscsv():
    """upload csv files of compounds to the database"""
    form = UploadCSVfile()
    if form.validate_on_submit():
        filename = secure_filename(form.compounds.data.filename)
        form.compounds.data.save("app/uploads/" + filename)
        filename_read = "app/uploads/" + filename

        upload_successful = upload_sizes_to_table(filename_read=filename_read)
        if upload_successful:

            flash('Parts Database updated')
        else:
            flash('there is a ploblem with the csv')
        return redirect(url_for('main.index'))

    return render_template('parts_database/uploadsizescsv.html', form=form)


@parts_database.route('/get_part_size/<string:partid>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def get_part_size(partid):
    part_info = PartsTable.query.filter_by(part_id=partid).first()
    get_sizes = do_virtual_cutter(part_info=part_info)

    return redirect(url_for('parts_database.show_part_batch', part_number=part_info.part_number))


@parts_database.route('/showpartplates', methods=['GET'])
@login_required
def showpartplates():
    # return a list of all the plate barcodes
    find_barcodes = PartsBatchTable.query.distinct(PartsBatchTable.storage_plate_barcode).all()

    return render_template('parts_database/show_barcodes.html', find_barcodes=find_barcodes)


@parts_database.route('/showpartplates/<string:barcode>', methods=['GET', 'POST'])
@login_required
def show_plate_parts(barcode):
    # get the part ID's and well location on specific plate barcode
    plate_barcode = PartsBatchTable.query.filter_by(storage_plate_barcode=barcode).all()

    return render_template('parts_database/show_platebatch_parts.html', storage_plate_barcode=plate_barcode,
                           barcode=barcode)


@parts_database.route('/uploadicelink', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def uploadicelink():
    """upload csv files of compounds to the database"""
    form = UploadCSVfile()
    if form.validate_on_submit():
        filename = secure_filename(form.compounds.data.filename)
        form.compounds.data.save("app/uploads/" + filename)
        filename_read = "app/uploads/" + filename

        upload_successful = upload_uploadicelink_to_table(filename_read=filename_read)

        if upload_successful:

            flash('Parts Database updated')
        else:
            flash('there is a ploblem with the csv')
        return redirect(url_for('main.index'))

    return render_template('parts_database/uploadicelink.html', form=form)


