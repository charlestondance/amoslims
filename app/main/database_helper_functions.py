__author__ = 'dmcclymo'

import csv
from ..models import project_task, PartsBatchTable, PartsTable, ytk_job_master, ytk_job_master_level2, part_dna_sizes
from .. import db


def upload_csv_check_keys(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        dict_keys = reader.fieldnames
        return dict_keys, reader


def write_pending_job_tasks_qc(unique_job_id):
    # set the tasks to pending
    item_add = project_task(unique_job_id=unique_job_id, task='uploaddesign', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=unique_job_id, task='uploadjobmaster', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=unique_job_id, task='clipqc', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=unique_job_id, task='stitchqc', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=unique_job_id, task='uploadjmp', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=unique_job_id, task='clip_qc_echo', status="pending", locked=0)
    db.session.add(item_add)
    item_add = project_task(unique_job_id=unique_job_id, task='stitch_qc_echo', status="pending", locked=0)
    db.session.add(item_add)
    db.session.commit()


def upload_parts_to_table(filename):

    all_ok = True
    PART_KEYS_CHECK = ['part_name', 'part_class', 'part_type', 'relative_position', 'level', 'offset', 'project_number',
                       'job_set', 'sequence', 'composite_part', 'external_id', 'part_method', 'part_number',
                       'storage_location_id', 'storage_plate_barcode']
    dict_keys, reader = upload_csv_check_keys(filename)

    # check dict keys match PART_KEYS_CHECK
    if sorted(dict_keys) == sorted(PART_KEYS_CHECK):
        for row in reader:
            # check if part exists. If part number is zero raise a new part number, otherwise raise a batch
            if row['part_number'] == str(0):
                # new part
                new_part_number = return_new_part_number()

                padded_part = paded_part_number(new_part_number=new_part_number)

                add_part = PartsTable(part_id="LDF-"+padded_part, part_name=row['part_name'],
                                      part_class=row['part_class'],
                                      part_type=row['part_type'], relative_position=row['relative_position'],
                                      level=row['level'], offset=row['offset'],
                                      project_number=row['project_number'],
                                      job_set=row['job_set'], sequence=row['sequence'],
                                      composite_part=row['composite_part'],
                                      external_id=row['external_id'], part_method=row['part_method'],
                                      part_number=new_part_number)

                add_batch = PartsBatchTable(storage_plate_barcode=row['storage_plate_barcode'],
                                            storage_location_id=row['storage_location_id'], part_id="LDF-"+padded_part,
                                            part_number=new_part_number, batch_number=1)

                db.session.add(add_part)
                db.session.add(add_batch)
            else:
                # new part so only make a batch

                padded_part = paded_part_number(int(row['part_number']))

                new_batch_number = return_new_batch_number(int(row['part_number']))

                add_batch = PartsBatchTable(storage_plate_barcode=row['storage_plate_barcode'],
                                            storage_location_id=row['storage_location_id'], part_id="LDF-"+padded_part,
                                            part_number=int(row['part_number']), batch_number=new_batch_number)

                db.session.add(add_batch)

            db.session.commit()

    else:
        all_ok = False
        print(sorted(dict_keys))
        print(sorted(PART_KEYS_CHECK))

    return all_ok


def upload_sizes_to_table(filename):

    all_ok = True
    PART_KEYS_CHECK = ['part_id', 'enzyme', 'size', 'cargo_number']

    dict_keys, reader = upload_csv_check_keys(filename)
    # check dict keys match PART_KEYS_CHECK

    if sorted(dict_keys) == sorted(PART_KEYS_CHECK):
        for row in reader:
            add_size = part_dna_sizes(part_id=row['part_id'], enzyme=row['enzyme'], size=int(row['size']),
                                      cargo_number=int(row['cargo_number']))
            db.session.add(add_size)

        db.session.commit()

    else:
        all_ok = False

    return all_ok


def return_new_part_number():
    # this function checks the part database and returns the highest number +1 or 1
    sql = "SELECT part_number FROM partstable ORDER BY part_number DESC "
    query_table = db.engine.execute(sql)
    query_table = query_table.fetchone()
    if query_table:
        part_number = query_table.part_number+1
    else:
        part_number = 1

    return part_number


def paded_part_number(new_part_number):
    # find the length of the number and pad it out with zeros and return it as a string
    length_of_part = len(str(new_part_number))
    part_string = ""
    if length_of_part < 6:
        padding = ''
        for pad in range(0, 6 - length_of_part):
            part_string = part_string + '0'

    part_string = part_string + str(new_part_number)

    return part_string


def return_new_batch_number(part_number):
    # this function checks the part database and returns the highest number +1 or 1
    sql = "SELECT batch_number from partsbatchtable WHERE part_number=%s order by batch_number DESC "
    query_table = db.engine.execute(sql, part_number)
    query_table = query_table.fetchone()

    return query_table.batch_number+1


def upload_jobmaster_processed1_ytk(filename, jobname, filename_for_db):

    KEYS_CHECK = ['Part Id', 'Sample Number', 'Storage Location Id', 'Storage Plate Barcode', 'Unique Job Id',
                  'Job Master Barcode', 'Job Master Well ID']

    job_master_error_flag = []

    dict_keys, reader = upload_csv_check_keys(filename)

    if sorted(dict_keys) != sorted(KEYS_CHECK):
        return job_master_error_flag.append('key_error')
    for row in reader:

        update_jobmaster = ytk_job_master.query.filter_by(part_id=row['Part Id'], sample_number=row['Sample Number'],
                                                          unique_job_id=row['Unique Job Id']).first()

        if update_jobmaster and row['Unique Job Id'] == jobname:
            print("True")
            update_jobmaster.job_master_well_id = row['Job Master Well ID']
            update_jobmaster.job_master_barcode = row['Job Master Barcode']
            update_jobmaster.uploaded_filename = filename_for_db
            db.session.commit()
        else:
            print('False')
            job_master_error_flag.append([row['Part Id'], row['Sample Number'], row['Unique Job Id']])

    return job_master_error_flag


def upload_jobmaster_processed2_ytk(filename, jobname, filename_for_db):

    KEYS_CHECK = ['Part Id', 'Sample Number', 'Storage Location Id', 'Storage Plate Barcode', 'Unique Job Id',
                  'Job Master Barcode', 'Job Master Well ID']

    job_master_error_flag = []

    dict_keys, reader = upload_csv_check_keys(filename)

    if sorted(dict_keys) != sorted(KEYS_CHECK):
        return job_master_error_flag.append('key_error')
    for row in reader:

        update_jobmaster = ytk_job_master_level2.query.filter_by(part_id=row['Part Id'],
                                                                 sample_number=row['Sample Number'],
                                                                 unique_job_id=row['Unique Job Id'], ).first()

        if update_jobmaster and row['Unique Job Id'] == jobname:
            update_jobmaster.job_master2_well_id = row['Job Master Well ID']
            update_jobmaster.job_master2_barcode = row['Job Master Barcode']
            update_jobmaster.uploaded_filename = filename_for_db
            db.session.commit()

        else:
            print('False')
            job_master_error_flag.append([row['Part Id'], row['Sample Number'], row['Unique Job Id']])

    return job_master_error_flag


def upload_uploadicelink_to_table(filename):
    # this function takes the entries file from ice and adds it to the sequence space in the parts database
    all_ok = True
    PART_KEYS_CHECK = ['Part ID', 'Name', 'Alias']

    dict_keys, reader = upload_csv_check_keys(filename)
    # check dict keys match PART_KEYS_CHECK

    if sorted(dict_keys) == sorted(PART_KEYS_CHECK):
        for row in reader:
            find_part = PartsTable.query.filter_by(part_id=row['Name']).first()

            if find_part:
                find_part.sequence = row['Part ID']
                db.session.add(find_part)
            else:
                all_ok = False

    else:
        all_ok = False

    if all_ok == True:
        db.session.commit()
    else:
        db.session.remove()

    return all_ok


def search_compounds():

    return PartsTable.query.distinct(PartsTable.project_number)
