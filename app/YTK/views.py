from . import YTK
from .. import db
from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from ..main.database_helper_functions import upload_jobmaster_processed1_ytk, upload_jobmaster_processed2_ytk
from ..main.forms import YtkDesignForm, JobLaunchpadForm
from ..main.views import make_job_task_list_ytk
from ..decorators import  permission_required
from werkzeug.utils import secure_filename
from ..models import Permission, project_task, ytk_clip_clone, JobTable, ytk_design, ytk_job_master, \
    ytk_job_master_level2, ytk_unique_clip, ytk_stitch_list
from ..main.create_design import create_ytk_design_max_4_gene
from .optimise_ytk import optimise_ytk_design, YeastClipReaction, YeastStitchReaction
from ..main.assign_design_locations import create_level_one_picklist_ytk, create_level_two_picklists_ytk


@YTK.route('/makeytkdesign', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def makeytkdesign():
    form = YtkDesignForm()
    ploblem = False

    # get the jobsets
    sql = "SELECT job_set FROM partstable where part_method='YTK' GROUP BY job_set, part_method"
    job_sets = db.engine.execute(sql)
    job_sets_choices = []

    # create a list of the projects for the dropdown
    for jobio in job_sets:
        job_sets_choices.append([jobio.job_set, jobio.job_set])

    form.jobset_parts.choices = job_sets_choices
    form.jobset_cassetes.choices = job_sets_choices

    if form.validate_on_submit():

        if ploblem == False:
            pass
            filename = secure_filename(form.jmp_file.data.filename)
            form.jmp_file.data.save("app/uploads/" + filename)
            filename_read = "app/uploads/" + filename
            create_ytk_design_max_4_gene(filename_read=filename_read, cds_partA=form.cds_partA.data,
                                         cds_partB=form.cds_partB.data, cds_partC=form.cds_partC.data,
                                         cds_partD=form.cds_partD.data, experiment_id=form.experiment_id.data,
                                         jobset_part=form.jobset_parts.data, jobset_cassetes=form.jobset_cassetes.data)

        return redirect(url_for('main.index'))

    return render_template('YTK/make_ytk_design.html', form=form)


@YTK.route('/ytk_job_launchpad/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def ytk_job_launchpad(jobnumber):
    qc_tasks = {}
    # find out all the qc task status
    qc_tasks['uploaddesign'] = project_task.query.filter_by(unique_job_id=jobnumber, task="uploaddesign").first()
    qc_tasks['in_silico_assembly'] = project_task.query.filter_by(unique_job_id=jobnumber,
                                                                  task="in_silico_assembly").first()
    qc_tasks['uploadjobmaster'] = project_task.query.filter_by(unique_job_id=jobnumber, task="uploadjobmaster").first()
    qc_tasks['uploadjobmaster_level_2'] = project_task.query.filter_by(unique_job_id=jobnumber,
                                                                       task="uploadjobmaster_level_2").first()

    # get project number
    project_number_query = JobTable.query.filter_by(unique_job_id=jobnumber).first()

    # if the design upload is complete then get the filename to pass to the view
    if qc_tasks['uploaddesign'].status == 'complete':
        design_uploaded_filename_query = ytk_design.query.filter_by(unique_job_id=jobnumber).first()
        design_uploaded_filename = design_uploaded_filename_query.uploaded_filename
    else:
        design_uploaded_filename = 'pending'

    # if the jobmaster upload is complete then get the filename to pass to the view
    if qc_tasks['uploadjobmaster'].status == 'complete':
        job_master_uploaded_filename_query = ytk_job_master.query.filter_by(unique_job_id=jobnumber).first()
        job_master_uploaded_filename = job_master_uploaded_filename_query.uploaded_filename
    else:
        job_master_uploaded_filename = 'pending'

    if qc_tasks['uploadjobmaster_level_2'].status == 'complete':
        job_master_uploaded2_filename_query = ytk_job_master_level2.query.filter_by(unique_job_id=jobnumber).first()
        job_master_uploaded2_filename = job_master_uploaded2_filename_query.uploaded_filename
        job_master_uploaded_filename_query = ytk_job_master.query.filter_by(unique_job_id=jobnumber).first()
        job_master_uploaded_filename = job_master_uploaded_filename_query.uploaded_filename
    else:
        job_master_uploaded2_filename = 'pending'

    task_list = make_job_task_list_ytk(qc_tasks)

    form = JobLaunchpadForm()
    form.job_tasks.choices = task_list

    # click actions
    if form.validate_on_submit():
        if form.job_tasks.data == 'Upload Design':
            filename = secure_filename(form.compounds.data.filename)
            form.compounds.data.save("app/uploads/" + filename)
            filename_read = "app/uploads/" + filename
            design_uploaded = ytk_design.upload_csv(filename_read, jobnumber, filename)

            # update the task

            # check the status of the upload
            if design_uploaded :
                flash(design_uploaded)
                return redirect(url_for('YTK.delete_ytk_design', jobnumber=jobnumber))

            # check the status of the optimise
            optimise_status = optimise_ytk_design(jobnumber)
            if optimise_status['success'] == False:
                flash(optimise_status)
                #return redirect(url_for('YTK.delete_ytk_design', jobnumber=jobnumber))

            # if all good then update the status
            update_task = project_task.query.filter_by(unique_job_id=jobnumber, task="uploaddesign").first()
            update_task.status = 'complete'
            db.session.commit()

        elif form.job_tasks.data == 'In Silico Assembly':
            clip_list = YeastClipReaction(jobnumber)
            clip_list.create_directory()
            clip_list.database_query()
            clip_list.create_genbankfiles_and_assembly()
            clip_png = clip_list.create_png_files()

            stitch_list = YeastStitchReaction(jobnumber)
            stitch_list.stitch_pathway()
            stitch_list.database_query()
            stitch_list.strip_features_from_gbfiles()
            stitch_list.create_genbank_and_stitch_reaction()
            stitch_png = stitch_list.create_png_files()

            if clip_png:
                flash("Clip Reaction successful!")
            if stitch_png:
                flash("Stitch Reaction successful!")
            update_task = project_task.query.filter_by(unique_job_id=jobnumber, task="in_silico_assembly").first()
            update_task.status = 'complete'
            db.session.commit()

        elif form.job_tasks.data == 'Upload Job Master Processed':
            filename = secure_filename(form.compounds.data.filename)
            form.compounds.data.save("app/uploads/" + filename)
            filename_read = "app/uploads/" + filename

            job_master_status = upload_jobmaster_processed1_ytk(filename=filename_read, jobname=jobnumber,
                                                                filename_for_db=filename)

            if job_master_status:
                flash(job_master_status)
                return redirect(url_for('YTK.delete_ytk_jobmaster1', jobnumber=jobnumber))

            # create picklists
            create_level_one_picklist_ytk(jobnumber=jobnumber)

            # update the task list
            update_task = project_task.query.filter_by(unique_job_id=jobnumber, task="uploadjobmaster").first()
            update_task.status = 'complete'
            db.session.commit()

        elif form.job_tasks.data == 'Upload Level 2 Job Master Processed':
            filename = secure_filename(form.compounds.data.filename)
            form.compounds.data.save("app/uploads/" + filename)
            filename_read = "app/uploads/" + filename

            job_master_status = upload_jobmaster_processed2_ytk(filename=filename_read, jobname=jobnumber,
                                                                filename_for_db=filename)

            if job_master_status:
                flash(job_master_status)
                return redirect(url_for('YTK.delete_ytk_jobmaster2', jobnumber=jobnumber))

            # create picklists

            create_level_two_picklists_ytk(jobnumber=jobnumber)

            # update the task list
            update_task = project_task.query.filter_by(unique_job_id=jobnumber, task="uploadjobmaster_level_2").first()
            update_task.status = 'complete'
            db.session.commit()

        return redirect(url_for('YTK.ytk_job_launchpad', jobnumber=jobnumber))

    return render_template('YTK/ytk_job_launchpad.html', jobnumber=jobnumber,
                           project_number=project_number_query.project_number, qc_tasks=qc_tasks,
                           job_master_uploaded_filename=job_master_uploaded_filename,
                           design_uploaded_filename=design_uploaded_filename, form=form,
                           job_master_uploaded2_filename=job_master_uploaded2_filename)


@YTK.route('/delete_ytk_design/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def delete_ytk_design(jobnumber):
    # just delete all the other tables in case of crash

    db.engine.execute("DELETE FROM ytk_job_master WHERE unique_job_id=%s", (jobnumber))
    db.engine.execute("DELETE FROM ytk_clip_list WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_buffer_plate_wells WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_clip_enzyme WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_clip_clone WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    # delete stitch list
    db.engine.execute("DELETE FROM ytk_stitch_list WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_job_master_level2 WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_job_master WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()

    """this function deletes all the tables associated with the design"""
    # delete from design table
    db.engine.execute("DELETE FROM ytk_design WHERE unique_job_id=%s", (jobnumber))

    # delete the project qc
    db.engine.execute("DELETE FROM project_task WHERE unique_job_id=%s", (jobnumber))

    # add pending qc (put this in a function)
    item_add = project_task(unique_job_id=jobnumber, task='uploaddesign', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=jobnumber, task='uploadjobmaster', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=jobnumber, task='uploadjobmaster_level_2', status="pending", locked=0)
    db.session.add(item_add)

    # delete unique clip
    db.engine.execute("DELETE FROM ytk_unique_clip WHERE unique_job_id=%s", (jobnumber))
    # delete unique part
    db.engine.execute("DELETE FROM ytk_unique_part WHERE unique_job_id=%s", (jobnumber))
    # delete unique part
    db.engine.execute("DELETE FROM ytk_job_master WHERE unique_job_id=%s", (jobnumber))

    db.session.commit()

    flash(jobnumber + " Deleted")

    return redirect(url_for('YTK.ytk_job_launchpad', jobnumber=jobnumber))


@YTK.route('/delete_ytk_jobmaster1/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def delete_ytk_jobmaster1(jobnumber):
    # delete all the other tables in case of crash
    # delete stitch list
    db.engine.execute("DELETE FROM ytk_stitch_list WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_job_master_level2 WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_stitch_enzyme WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_stitch_clone WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()

    # delete unique clip
    db.engine.execute("DELETE FROM ytk_clip_list WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_buffer_plate_wells WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_clip_enzyme WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_clip_clone WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_job_master_level2 WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()

    sql = "UPDATE ytk_job_master SET job_master_well_id=%s, job_master_barcode = %s, uploaded_filename=%s WHERE unique_job_id=%s"

    params = ('-', '-', '-', jobnumber)
    # params = (batch_counter_increment, jobname, stitch, letter)
    db.engine.execute(sql, params)
    db.session.commit()

    uloadjobmaster_update = project_task.query.filter_by(unique_job_id=jobnumber, task='uploadjobmaster').first()
    uloadjobmaster_update.status = 'pending'

    db.session.commit()

    flash(jobnumber + " Deleted")

    return redirect(url_for('YTK.ytk_job_launchpad', jobnumber=jobnumber))


@YTK.route('/delete_ytk_jobmaster2/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def delete_ytk_jobmaster2(jobnumber):
    # delete all the other tables in case of crash
    # delete from design table
    # delete stitch list
    db.engine.execute("DELETE FROM ytk_stitch_list WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_stitch_enzyme WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()
    db.engine.execute("DELETE FROM ytk_stitch_clone WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()

    sql = "UPDATE ytk_job_master_level2 SET job_master2_well_id=%s, job_master2_barcode = %s, uploaded_filename=%s " \
          "WHERE unique_job_id=%s"

    params = ('-', '-', '-', jobnumber)
    # params = (batch_counter_increment, jobname, stitch, letter)
    db.engine.execute(sql, params)
    db.session.commit()

    uloadjobmaster_update = project_task.query.filter_by(unique_job_id=jobnumber, task='uploadjobmaster_level_2').first()
    uloadjobmaster_update.status = 'pending'

    db.session.commit()

    flash(jobnumber + " Deleted")

    return redirect(url_for('YTK.ytk_job_launchpad', jobnumber=jobnumber))


@YTK.route('/ytk_show_miniprep_positions/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def ytk_show_miniprep_positions(jobnumber):
    #list_of_clones = return_list_of_clone_plates_for_visualisation(jobnumber)

    clip_query = ytk_clip_clone.query.filter_by(unique_job_id=jobnumber).order_by(
        ytk_clip_clone.well_number_96, ytk_clip_clone.clone_plate_barcode).all()

    return render_template('YTK/ytk_show_miniprep_position.html', clip_query=clip_query)


@YTK.route('/ytk_clip_report/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def ytk_clip_report(jobnumber):
    clip_count = ytk_unique_clip.query.filter_by(unique_job_id=jobnumber).count()
    clip_num =list(range(1, (clip_count +1)))
    clip_list = [ "C" + str(clip) for clip in clip_num]

    return render_template('YTK/ytk_clip_viewer.html', jobnumber = jobnumber, clip_list=clip_list)


@YTK.route('/ytk_stitch_report/<string:jobnumber>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.EDIT_DB)
def ytk_stitch_report(jobnumber):
    stitch_count = ytk_stitch_list.query.distinct(ytk_stitch_list.stitch_id).count()
    stitch_num =list(range(1, (stitch_count +1)))
    stitch_list = [ "stitch_" + str(stitch) for stitch in stitch_num]

    return render_template('YTK/ytk_stitch_viewer.html', jobnumber = jobnumber, stitch_list=stitch_list)