from app import db
from app.models import quadrant_wells_lookup, ytk_unique_clip, ytk_clip_list, ytk_design, ytk_job_master, ytk_clip_enzyme, ytk_buffer_plate_wells, ytk_job_master_level2, ytk_clip_clone, ytk_stitch_list, ytk_stitch_enzyme, ytk_stitch_clone
from ..YTK.optimise_ytk import get_list_of_unique_stitch_ids_ytk
import math
import itertools
import random


def get_list_of_level1_clips_in_stitch_ytk(jobnumber, stitch):
    # return a list of unique tuples containing the clip number and batch number for each stitch

    design_query = ytk_design.query.filter_by(unique_job_id=jobnumber, stitch_id=stitch, level=1).all()
    ytk_clip_list = []
    for x in design_query:
        ytk_clip_list.append((x.unique_clip_number, x.clip_id_batch_id))

    return set(ytk_clip_list)


def get_list_of_level2_clips_in_stitch_ytk(jobnumber, stitch):
    # return a list of unique tuples containing the part id and batch number for each stitch

    design_query = ytk_design.query.filter_by(unique_job_id=jobnumber, stitch_id=stitch, level=2).all()

    list_of_level_2 = []

    for level2 in design_query:

        list_of_level_2.append([level2.part_id, level2.clip_id_batch_id])

    return list_of_level_2


def return_volume_from_part_query(part_query):
    linker_vol = 500
    part_vol = 1000
    if part_query.part_class == 'Part':
        return part_vol
    elif part_query.part_class == 'Linker':
        return linker_vol
    else:
        return 0


def count_number_of_clips_ytk(jobnumber):
    # Return the number of clips in the study
    sql = "SELECT COUNT(*) AS counter_hing FROM ytk_unique_clip WHERE unique_job_id=%s"
    params = (jobnumber)
    count_it = db.engine.execute(sql, params)
    for x in count_it:
        counts=x
    return counts[0]


def infinite_6well_generator():
    columns = 3
    end_letter = "B"
    plate_counter = 1

    row_list = []
    column_list = []

    # generate the list of columns and number
    for x in range(ord("A"), ord(end_letter)+1):
        row_list.append(chr(x))
    for y in range(1, columns+1):
        column_list.append(str(y))

    while True:
        for x in row_list:
            for y in column_list:
                yield (x+y, plate_counter)
        plate_counter += 1


def infinite_quadrant_wells_generator_clip_plate():

    """yields an infinite list of 384 wells but in quadrants. THE LAST WELL IS SKIPPED DUE TO LADDER WELL"""
    columns = 24
    end_letter = "P"
    plate_counter = 1

    row_list = []
    column_list = []

    # generate the list of columns and number
    for x in range(ord("A"), ord(end_letter)+1):
        row_list.append(chr(x))
    for y in range(1, columns+1):
        column_list.append(str(y))

    quadrant_list = ["A1", "A2", "B1", "B2"]

    while True:
        for quadrant in quadrant_list:
            # check the starting quadrant and generate the list
            if quadrant == "A1":
                for x in row_list[::2]:
                    for y in column_list[::2]:
                        if x+y == 'O23':
                            pass
                        else:
                            yield (x+y, plate_counter)

            elif quadrant == "A2":
                for x in row_list[::2]:
                    for y in column_list[1::2]:
                        if x+y == 'O24':
                            pass
                        else:
                            yield (x+y, plate_counter)

            elif quadrant == "B1":
                for x in row_list[1::2]:
                    for y in column_list[0::2]:
                        if x+y == 'P23':
                            pass
                        else:
                            yield (x+y, plate_counter)

            elif quadrant == "B2":
                for x in row_list[1::2]:
                    for y in column_list[1::2]:
                        if x+y == 'P24':
                            pass
                        else:
                            yield (x+y, plate_counter)

        plate_counter += 1


def infinite_quadrant_wells_generator():

    """ yields an infinite list of 384 wells but in quadrants.
    Second value in the tuple is the plate counter (when reaches limit)
    """
    columns = 24
    end_letter = "P"
    plate_counter = 1

    row_list = []
    column_list = []

    # generate the list of columns and number
    for x in range(ord("A"), ord(end_letter)+1):
        row_list.append(chr(x))
    for y in range(1, columns+1):
        column_list.append(str(y))

    quadrant_list = ["A1", "A2", "B1", "B2"]

    while True:
        for quadrant in quadrant_list:
            # check the starting quadrant and generate the list
            if quadrant == "A1":
                for x in row_list[::2]:
                    for y in column_list[::2]:
                        yield (x+y, plate_counter)
            elif quadrant == "A2":
                for x in row_list[::2]:
                    for y in column_list[1::2]:
                        yield (x+y, plate_counter)
            elif quadrant == "B1":
                for x in row_list[1::2]:
                    for y in column_list[0::2]:
                        yield (x+y, plate_counter)
            elif quadrant == "B2":
                for x in row_list[1::2]:
                    for y in column_list[1::2]:
                        yield (x+y, plate_counter)
        plate_counter += 1


def infinite_quadrant_wells_stitch_generator():

    """yields an infinite list of 384 wells but in quadrants.
    Second value in the tuple is the plate counter (when reaches limit)
    """
    columns = 24
    end_letter = "P"
    plate_counter = 1

    row_list = []
    column_list = []

    # generate the list of columns and number
    for x in range(ord("A"), ord(end_letter)+1):
        row_list.append(chr(x))
    for y in range(1, columns+1):
        column_list.append(str(y))

    quadrant_list = ["A1", "A2", "B1", "B2"]

    while True:
        for quadrant in quadrant_list:
            # check the sarting quadrant and generate the list
            if quadrant == "A1":
                for x in row_list[::2]:
                    for y in column_list[::2]:
                        if y=='23':
                            pass
                        else:
                            yield (x+y, plate_counter)
            elif quadrant == "A2":
                for x in row_list[::2]:
                    for y in column_list[1::2]:
                        if y=='24':
                            pass
                        else:
                            yield (x+y, plate_counter)
            elif quadrant == "B1":
                for x in row_list[1::2]:
                    for y in column_list[0::2]:
                        if y == '23':
                            pass
                        else:
                            yield (x+y, plate_counter)

            elif quadrant == "B2":
                for x in row_list[1::2]:
                    for y in column_list[1::2]:
                        if y == '24':
                            pass
                        else:
                            yield (x+y, plate_counter)
        plate_counter += 1


def infinite_6well_generator():
    columns = 3
    end_letter = "B"
    plate_counter = 1

    row_list = []
    column_list = []

    # generate the list of columns and number
    for x in range(ord("A"), ord(end_letter)+1):
        row_list.append(chr(x))
    for y in range(1, columns+1):
        column_list.append(str(y))

    while True:
        for x in row_list:
            for y in column_list:
                yield (x+y, plate_counter)
        plate_counter += 1


def infinite_96well_generator():
    columns = 12
    end_letter = "H"
    plate_counter = 1

    row_list = []
    column_list = []

    # generate the list of columns and number
    for x in range(ord("A"), ord(end_letter)+1):
        row_list.append(chr(x))
    for y in range(1, columns+1):
        column_list.append(str(y))

    while True:
        for x in row_list:
            for y in column_list:
                yield (x+y, plate_counter)
        plate_counter += 1


def return_quadrant(plate_number_96):
    # take a number 1 to 4 and return the quadrant on a 384-well plate
    if plate_number_96 == 1:
        plate_name = "A1"
    elif plate_number_96 == 2:
        plate_name = "A2"
    elif plate_number_96 == 3:
        plate_name = "B1"
    elif plate_number_96 == 4:
        plate_name = "B2"

    return plate_name


def create_level_one_picklist_ytk(jobnumber):

    assign_wells_for_clip_ytk(jobnumber=jobnumber)
    assign_wells_for_enzyme_level_1_ytk(jobnumber=jobnumber)
    create_clone_plate_level1_ytk(jobnumber=jobnumber)
    assign_wells_for_jobmaster_level2_ytk(jobnumber=jobnumber)
    pull_out_the_level_2_from_desgign_for_level2_ytk(jobnumber=jobnumber)


def assign_wells_for_clip_ytk(jobnumber):

    GOLDEN_GATE_PART_VOL = 500

    number_of_clips = count_number_of_clips_ytk(jobnumber=jobnumber)

    wells_list = infinite_quadrant_wells_stitch_generator()

    for clip in range(1, number_of_clips + 1):

        clip_info = ytk_unique_clip.query.filter_by(unique_job_id=jobnumber, clip_number=clip).first()
        # check the number of batches in the table
        for clip_batch in range(1, clip_info.clip_batches_required + 1):

            well_plate = next(wells_list)

            # look up the design table to find the sample bumber for the assigned part
            if clip_info.part_1_id != 'EMPTY':
                part_1_sample_number = ytk_design.query.filter_by(unique_job_id=jobnumber, unique_clip_number=clip,
                                                                  clip_id_batch_id=clip_batch,
                                                                  part_id=clip_info.part_1_id).first()

                # find that sample location in the plate
                part_1_sample_location = ytk_job_master.query.filter_by(unique_job_id=jobnumber,
                                                                        part_id=clip_info.part_1_id,
                                                                        sample_number=part_1_sample_number.part_id_sample_id).first()

                part_1_volume = GOLDEN_GATE_PART_VOL

                add_part_1_to_clip_table = ytk_clip_list(unique_job_id=jobnumber, part_id=str(clip_info.part_1_id),
                                                         part_id_sample_number=str(
                                                             part_1_sample_number.part_id_sample_id),
                                                         concatenated_part_id=str(clip_info.part_1_id) + "-" + str(
                                                             part_1_sample_number.part_id_sample_id),
                                                         job_master_well_id=str(
                                                             part_1_sample_location.job_master_well_id),
                                                         job_master_barcode=str(
                                                             part_1_sample_location.job_master_barcode),
                                                         concatenated_clip_id="C" + str(clip) + "-" + str(clip_batch),
                                                         clip_number=clip, clip_batch_number=clip_batch,
                                                         transfer_volume=part_1_volume,
                                                         clip_well_id=str(well_plate[0]),
                                                         clip_barcode=str(jobnumber) + "-C-" + str(well_plate[1]),
                                                         destination_plate_number=well_plate[1])

                db.session.add(add_part_1_to_clip_table)

            else:
                pass

            if clip_info.part_2_id != 'EMPTY':

                # part 2
                part_2_sample_number = ytk_design.query.filter_by(unique_job_id=jobnumber, unique_clip_number=clip,
                                                                  clip_id_batch_id=clip_batch,
                                                                  part_id=clip_info.part_2_id).first()

                part_2_sample_location = ytk_job_master.query.filter_by(unique_job_id=jobnumber,
                                                                        part_id=clip_info.part_2_id,
                                                                        sample_number=part_2_sample_number.part_id_sample_id).first()

                part_2_volume = GOLDEN_GATE_PART_VOL

                add_part_2_to_clip_table = ytk_clip_list(unique_job_id=jobnumber, part_id=str(clip_info.part_2_id),
                                                         part_id_sample_number=str(
                                                             part_2_sample_number.part_id_sample_id),
                                                         concatenated_part_id=str(clip_info.part_2_id) + "-" + str(
                                                             part_2_sample_number.part_id_sample_id),
                                                         job_master_well_id=str(
                                                             part_2_sample_location.job_master_well_id),
                                                         job_master_barcode=str(
                                                             part_2_sample_location.job_master_barcode),
                                                         concatenated_clip_id="C" + str(clip) + "-" + str(clip_batch),
                                                         clip_number=clip, clip_batch_number=clip_batch,
                                                         transfer_volume=part_2_volume,
                                                         clip_well_id=str(well_plate[0]),
                                                         clip_barcode=str(jobnumber) + "-C-" + str(well_plate[1]),
                                                         destination_plate_number=well_plate[1])

                db.session.add(add_part_2_to_clip_table)
            else:
                pass

            if clip_info.part_3_id != 'EMPTY':

                part_3_sample_number = ytk_design.query.filter_by(unique_job_id=jobnumber, unique_clip_number=clip,
                                                                  clip_id_batch_id=clip_batch,
                                                                  part_id=clip_info.part_3_id).first()

                part_3_sample_location = ytk_job_master.query.filter_by(unique_job_id=jobnumber,
                                                                        part_id=clip_info.part_3_id,
                                                                        sample_number=part_3_sample_number.part_id_sample_id).first()

                part_3_volume = GOLDEN_GATE_PART_VOL

                add_part_3_to_clip_table = ytk_clip_list(unique_job_id=jobnumber, part_id=str(clip_info.part_3_id),
                                                         part_id_sample_number=str(
                                                             part_3_sample_number.part_id_sample_id),
                                                         concatenated_part_id=str(clip_info.part_3_id) + "-" + str(
                                                             part_3_sample_number.part_id_sample_id),
                                                         job_master_well_id=str(
                                                             part_3_sample_location.job_master_well_id),
                                                         job_master_barcode=str(
                                                             part_3_sample_location.job_master_barcode),
                                                         concatenated_clip_id="C" + str(clip) + "-" + str(clip_batch),
                                                         clip_number=clip, clip_batch_number=clip_batch,
                                                         transfer_volume=part_3_volume,
                                                         clip_well_id=str(well_plate[0]),
                                                         clip_barcode=str(jobnumber) + "-C-" + str(well_plate[1]),
                                                         destination_plate_number=well_plate[1])

                db.session.add(add_part_3_to_clip_table)
            else:
                pass

            if clip_info.part_4_id != 'EMPTY':

                part_4_sample_number = ytk_design.query.filter_by(unique_job_id=jobnumber, unique_clip_number=clip,
                                                                  clip_id_batch_id=clip_batch,
                                                                  part_id=clip_info.part_4_id).first()

                part_4_sample_location = ytk_job_master.query.filter_by(unique_job_id=jobnumber,
                                                                        part_id=clip_info.part_4_id,
                                                                        sample_number=part_4_sample_number.part_id_sample_id).first()

                part_4_volume = GOLDEN_GATE_PART_VOL

                add_part_4_to_clip_table = ytk_clip_list(unique_job_id=jobnumber, part_id=str(clip_info.part_4_id),
                                                         part_id_sample_number=str(
                                                         part_4_sample_number.part_id_sample_id),
                                                         concatenated_part_id=str(clip_info.part_4_id) + "-" + str(
                                                         part_4_sample_number.part_id_sample_id),
                                                         job_master_well_id=str(
                                                         part_4_sample_location.job_master_well_id),
                                                         job_master_barcode=str(
                                                         part_4_sample_location.job_master_barcode),
                                                         concatenated_clip_id="C" + str(clip) + "-" + str(clip_batch),
                                                         clip_number=clip, clip_batch_number=clip_batch,
                                                         transfer_volume=part_4_volume,
                                                         clip_well_id=str(well_plate[0]),
                                                         clip_barcode=str(jobnumber) + "-C-" + str(well_plate[1]),
                                                         destination_plate_number=well_plate[1])

                db.session.add(add_part_4_to_clip_table)

    db.session.commit()


def assign_wells_for_enzyme_level_1_ytk(jobnumber):

    total_vol_enzyme = 0
    total_vol_buffer = 0
    enzyme_volume = 8000
    dead_volume_6well = 0.175 * 1000000
    max_volume_6well = 2.55 * 1000000

    working_volume_6well = max_volume_6well - dead_volume_6well

    # find_number_of_clip_plates and iterate through the wells
    sql = "SELECT DISTINCT destination_plate_number FROM ytk_clip_list WHERE unique_job_id=%s"
    params = jobnumber
    count_it = db.engine.execute(sql, params)

    wells_list_6_well = infinite_6well_generator()

    well_from_6well = next(wells_list_6_well)

    # add the first well to the list for the buffer
    buffer_plate_list = []

    # create the table for the clip plate enzyme

    for clip_plate in range(0, (len(count_it.fetchall()))):

        sql = "SELECT DISTINCT clip_well_id FROM ytk_clip_list WHERE unique_job_id=%s"
        params = (jobnumber)

        wells_per_clip_plate = db.engine.execute(sql, params)

        for clip_well in wells_per_clip_plate:

            total_vol_enzyme += enzyme_volume

            if total_vol_enzyme >= working_volume_6well:
                # write the information to the buffer_plate table
                add_enzyme_amounts_to_table = ytk_buffer_plate_wells(unique_job_id=jobnumber,
                                                                     buffer_plate_well_id=well_from_6well[0],
                                                                     loading_volume=total_vol_enzyme - enzyme_volume,
                                                                     buffer_plate_barcode=str(
                                                                           jobnumber) + "-B-" + str(
                                                                           well_from_6well[1]),
                                                                     buffer_name="Enzyme Mastermix",
                                                                     buffer_plate_number=well_from_6well[1])
                db.session.add(add_enzyme_amounts_to_table)

                well_from_6well = next(wells_list_6_well)
                total_vol_enzyme = 0

            query_clip_in_design = ytk_clip_list.query.filter_by(unique_job_id=jobnumber, clip_well_id=clip_well[0],
                                                                 destination_plate_number=clip_plate + 1).first()

            add_to_enzyme_plate = ytk_clip_enzyme(unique_job_id=jobnumber, clip_well_id=clip_well[0],
                                                  clip_barcode=str(jobnumber) + "-C-" + str(clip_plate + 1),
                                                  concatenated_clip_id=query_clip_in_design.concatenated_clip_id,
                                                  clip_number=query_clip_in_design.clip_number,
                                                  clip_batch_number=query_clip_in_design.clip_batch_number,
                                                  transfer_volume=enzyme_volume,
                                                  clip_plate_number=clip_plate + 1,
                                                  enzyme_plate_barcode=str(jobnumber) + "-B-" + str(
                                                        well_from_6well[1]),
                                                  enzyme_plate_well_id=well_from_6well[0],
                                                  enzyme_plate_number=well_from_6well[1]
                                                  )

            db.session.add(add_to_enzyme_plate)

    # fill in the table with the amounts of enzyme
    add_enzyme_amounts_to_table = ytk_buffer_plate_wells(unique_job_id=jobnumber,
                                                         buffer_plate_well_id=well_from_6well[0],
                                                         loading_volume=total_vol_enzyme,
                                                         buffer_plate_barcode=str(jobnumber) + "-B-" + str(
                                                               well_from_6well[1]),
                                                         buffer_name="Enzyme Mastermix",
                                                         buffer_plate_number=well_from_6well[1])
    db.session.add(add_enzyme_amounts_to_table)


def create_clone_plate_level1_ytk(jobnumber):

    query_clip_in_design = ytk_clip_enzyme.query.filter_by(unique_job_id=jobnumber).all()

    list_of_clip_barcodes = []

    for iter_though_list in query_clip_in_design:
        if iter_though_list.clip_barcode not in list_of_clip_barcodes:
            list_of_clip_barcodes.append(iter_though_list.clip_barcode)
        else:
            pass

    # iterate through the barcodes
    for barcode in list_of_clip_barcodes:
        # iterate through the stitches for eah barcode
        clip_query = ytk_clip_enzyme.query.filter_by(unique_job_id=jobnumber, clip_barcode=barcode).all()
        for clip in clip_query:

            # lookup the equivalent well
            find_equivalent_well = quadrant_wells_lookup.query.filter_by(
                well_id_384=clip.clip_well_id).first()

            # turn number into quadrant
            plate_name=return_quadrant(find_equivalent_well.plate_number_96)

            add_record_to_clip_clone = ytk_clip_clone(unique_job_id=jobnumber,
                                                      clone_plate_well_id_96=find_equivalent_well.well_id_96,
                                                      well_number_96=find_equivalent_well.well_number_96,
                                                      clip_well_id=clip.clip_well_id,
                                                      clip_plate_barcode=barcode,
                                                      clone_plate_barcode=barcode + "-" + plate_name,
                                                      clip_id=clip.concatenated_clip_id,
                                                      clip_id_no_batch='C'+str(clip.clip_number),
                                                      clip_id_job_id=jobnumber+'-'+clip.concatenated_clip_id,
                                                      clip_id_job_id_no_batch_id=jobnumber+'-'+'C'+str(clip.clip_number))

            db.session.add(add_record_to_clip_clone)

    db.session.commit()


def return_list_of_clone_plates_for_visualisation(jobnumber):

    # get a list of the unique barcodes
    query_clip_in_design = ytk_clip_clone.query.filter_by(unique_job_id=jobnumber).all()

    list_of_clip_barcodes = []

    for iter_though_list in query_clip_in_design:
        if iter_though_list.clone_plate_barcode not in list_of_clip_barcodes:
            list_of_clip_barcodes.append(iter_though_list.clone_plate_barcode)
        else:
            pass
    # for each barcode get a list of the clips

    plates_list = []

    for barcode in list_of_clip_barcodes:
        clip_query = ytk_clip_clone.query.filter_by(unique_job_id=jobnumber,
                                                    clone_plate_barcode=barcode).order_by(ytk_clip_clone.well_number_96).all()

        well_contents =[]

        for well in range(0,96):

            try:
                well_contents.append([well, clip_query[well].clip_id, clip_query[well].clone_plate_well_id_96])
            except:
                well_contents.append([well, "Empty"])

        plates_list.append([barcode, well_contents])

    return plates_list


def assign_wells_for_jobmaster_level2_ytk(jobnumber):

    # get list of clips
    clip_query = ytk_unique_clip.query.filter_by(unique_job_id=jobnumber).order_by(
        ytk_unique_clip.clip_number).all()

    for clip in clip_query:
        for clip_batches in range(0, clip.clip_batches_required):
            print(str(clip.clip_number), str(clip_batches))

            clip_clone_postition = ytk_clip_clone.query.filter_by(unique_job_id=jobnumber,
                                                                  clip_id='C' + str(clip.clip_number) + '-'
                                                                          + str(clip_batches+1)).first()

            for samples in range(0,3):

                add_level2_takeout = ytk_job_master_level2(unique_job_id=jobnumber, part_id=jobnumber + '-C' +
                                                                                            str(clip.clip_number) + '-'
                                                                                            + str(clip_batches+1),
                                                           job_master2_well_id='-', job_master2_barcode='-',
                                                           sample_number=samples+1, uploaded_filename='-',
                                                           level1clone_plate_barcode=clip_clone_postition.clone_plate_barcode,
                                                           level1clone_location_id=clip_clone_postition.clone_plate_well_id_96)

                db.session.add(add_level2_takeout)

        db.session.commit()


def pull_out_the_level_2_from_desgign_for_level2_ytk(jobnumber):
    """Look up the level 2 positions count them and add the takeout to the job master list

    Update the design with the take out"""

    GOLDEN_GATE_VOLUME = 500

    level2_design_query = ytk_design.query.filter_by(unique_job_id=jobnumber, level=2).all()

    list_of_level2_parts = []

    for x in level2_design_query:
        list_of_level2_parts.append(x.part_id)

    unique_level_2_parts = set(list_of_level2_parts)

    level2_part_dict = {}
    level2_number_of_samples_required = {}

    # make empty part dict
    for part in unique_level_2_parts:
        level2_part_dict[part] = 0
        level2_number_of_samples_required[part] = 0

    # count the parts
    for x in level2_design_query:
        level2_part_dict[x.part_id] += 1

    # figure out how many samples are required for each level 2 part
    for part in unique_level_2_parts:
        level2_number_of_samples_required[part] = math.ceil((level2_part_dict[part]*GOLDEN_GATE_VOLUME)/8000)

    # add the take out to the pick list
    for part in unique_level_2_parts:
        # get the highest number batch of the part and write the number of copies to the table
        sql2 = "SELECT * from partsbatchtable WHERE part_id=%s order by batch_number DESC"
        query_batch_table = db.engine.execute(sql2, part)
        query_batch_table = query_batch_table.fetchone()
        # loop round number of samples required
        for unit in range(1,level2_number_of_samples_required[part]+1):
            add_level2_takeout = ytk_job_master_level2(unique_job_id=jobnumber, part_id=part,
                                                       job_master2_well_id='-', job_master2_barcode='-',
                                                       sample_number=unit, uploaded_filename='-',
                                                       level1clone_plate_barcode=query_batch_table.storage_plate_barcode,
                                                       level1clone_location_id=query_batch_table.storage_location_id)

            db.session.add(add_level2_takeout)

    db.session.commit()

    # update the design
    for part in unique_level_2_parts:
        # create the cycle iterator for the samples
        samples_list = list(range(1,level2_number_of_samples_required[part]+1))
        random.shuffle(samples_list)
        cycle_part_sample = itertools.cycle(samples_list)
        query_level2_part = ytk_design.query.filter_by(unique_job_id=jobnumber, level=2, part_id=part).all()
        for level2_part_in_design in query_level2_part:
            level2_part_in_design.clip_id_batch_id = next(cycle_part_sample)

    db.session.commit()


def create_level_two_picklists_ytk(jobnumber):

    distribute_clip_id_sample_ids(jobnumber)
    create_level_two_stitchlist_ytk(jobnumber)
    create_level_2_enzyme_picklist_ytk(jobnumber)
    create_clone_plate_level2_ytk(jobnumber)


def distribute_clip_id_sample_ids(jobnumber):

    # assume that clip reaction is 30ul so take out is 3
    # run through a list of the level one clips, pull out a unique stitch id, then cycle through 1-3

    # get list of clips
    clip_query = ytk_unique_clip.query.filter_by(unique_job_id=jobnumber).order_by(
        ytk_unique_clip.clip_number).all()

    for clip in clip_query:
        for clip_batch in range(1, clip.clip_batches_required+1):

            # create the sample iterator
            list_of_samples_integers = list(range(1, 4))
            # randomise the list so it doesnt start at the same sample each time
            #random.shuffle(list_of_samples_integers)
            cycle_part_sample = itertools.cycle(list_of_samples_integers)

            # get a list of stitches per clip batch
            disinct_stitches_per_clip_batch = ytk_design.query.filter_by(unique_job_id=jobnumber,
                                                                         unique_clip_number=clip.clip_number,
                                                                         clip_id_batch_id=clip_batch).distinct(ytk_design.stitch_id).order_by(ytk_design.stitch_id)
            for stitch in disinct_stitches_per_clip_batch:
                # cycle through the samples
                part_sample_number = next(cycle_part_sample)

                sql = "UPDATE ytk_design SET clip_id_sample_id=%s where unique_job_id=%s AND unique_clip_number=%s " \
                      "AND clip_id_batch_id=%s and stitch_id=%s"
                db.engine.execute(sql, [part_sample_number, jobnumber, clip.clip_number, clip_batch, stitch.stitch_id])

                db.session.commit()


def create_level_two_stitchlist_ytk(jobnumber):
    stitch_volume = 500

    unique_stitch_ids = get_list_of_unique_stitch_ids_ytk(jobname=jobnumber)

    wells_list = infinite_quadrant_wells_stitch_generator()

    for stitch in unique_stitch_ids:

        well_plate = next(wells_list)

        list_of_clip_list_set_level2 = get_list_of_level2_clips_in_stitch_ytk(jobnumber=jobnumber, stitch=str(stitch))

        for clip_list_set_level2 in list_of_clip_list_set_level2:

            # add the level2 part
            find_clip = ytk_job_master_level2.query.filter_by(unique_job_id=jobnumber,
                                                              part_id=str(clip_list_set_level2[0]),
                                                              sample_number=clip_list_set_level2[1]).first()
            add_stitch = ytk_stitch_list(unique_job_id=jobnumber, stitch_id=str(stitch), clip_number=0,
                                         clip_batch_number=clip_list_set_level2[1],
                                         concatenated_clip_id=str(clip_list_set_level2[0]) + "-" + str(clip_list_set_level2[1]),
                                         clip_well_id=find_clip.job_master2_well_id,
                                         clip_barcode=find_clip.job_master2_barcode,
                                         stitch_well_id=well_plate[0],
                                         stitch_plate_barcode=str(jobnumber) + "-S-" + str(well_plate[1]),
                                         stitch_plate_number=well_plate[1], transfer_volume=stitch_volume)
            db.session.add(add_stitch)

        # get the list of the level 1 and add to the stitch list
        clip_list_set = get_list_of_level1_clips_in_stitch_ytk(jobnumber=jobnumber, stitch=str(stitch))
        for clip in clip_list_set:

            get_sample_number = ytk_design.query.filter_by(unique_job_id=jobnumber, stitch_id=stitch,
                                                           unique_clip_number=clip[0],
                                                           clip_id_batch_id=clip[1]).first()

            find_clip = ytk_job_master_level2.query.filter_by(unique_job_id=jobnumber,
                                                              part_id=jobnumber+'-C' + str(clip[0])+'-'+str(clip[1]),
                                                              sample_number=get_sample_number.clip_id_sample_id).first()

            print(jobnumber+'-C'+str(clip[0])+'-'+str(clip[1]), get_sample_number.clip_id_sample_id)

            add_stitch = ytk_stitch_list(unique_job_id=jobnumber, stitch_id=str(stitch), clip_number=clip[0],
                                         clip_batch_number=clip[1],
                                         concatenated_clip_id="C" + str(clip[0]) + "-" + str(clip[1]) + '-' +
                                                              str(get_sample_number.clip_id_sample_id),
                                         clip_well_id=find_clip.job_master2_well_id,
                                         clip_barcode=find_clip.job_master2_barcode,
                                         stitch_well_id=well_plate[0],
                                         stitch_plate_barcode=str(jobnumber) + "-S-" + str(well_plate[1]),
                                         stitch_plate_number=well_plate[1], transfer_volume=stitch_volume)

            db.session.add(add_stitch)

    db.session.commit()


def create_level_2_enzyme_picklist_ytk(jobnumber):

    total_vol_enzyme = 0
    total_vol_buffer = 0
    enzyme_volume = 7500
    dead_volume_6well = 0.175 * 1000000
    max_volume_6well = 2.55 * 1000000

    working_volume_6well = max_volume_6well - dead_volume_6well

    # wipe the enzyme plate
    db.engine.execute("DELETE FROM ytk_clip_enzyme WHERE unique_job_id=%s", (jobnumber))
    db.session.commit()

    # find_number_of_clip_plates and iterate through the wells

    sql = "SELECT DISTINCT stitch_plate_number FROM ytk_stitch_list WHERE unique_job_id=%s"
    params = (jobnumber)
    count_it = db.engine.execute(sql, params)

    wells_list_6_well = infinite_6well_generator()

    well_from_6well = next(wells_list_6_well)

    # add the first well to the list for the buffer
    buffer_plate_list = []

    # create the table for the clip plate enzyme

    for stitch_plate in range(0, (len(count_it.fetchall()))):
        print("stitch Plate", stitch_plate)

        sql = "SELECT DISTINCT stitch_well_id FROM ytk_stitch_list WHERE unique_job_id=%s and stitch_plate_number=%s"
        params = (jobnumber, stitch_plate+1)

        wells_per_clip_plate = db.engine.execute(sql, params)

        for stitch_well in wells_per_clip_plate:

            total_vol_enzyme += enzyme_volume

            if total_vol_enzyme >= working_volume_6well:
                # write the information to the buffer_plate table
                add_enzyme_amounts_to_table = ytk_buffer_plate_wells(unique_job_id=jobnumber,
                                                                     buffer_plate_well_id=well_from_6well[0],
                                                                     loading_volume=total_vol_enzyme - enzyme_volume,
                                                                     buffer_plate_barcode=str(
                                                                         jobnumber) + "-B-" + str(
                                                                         well_from_6well[1]),
                                                                     buffer_name="Enzyme Mastermix",
                                                                     buffer_plate_number=well_from_6well[1])
                db.session.add(add_enzyme_amounts_to_table)

                well_from_6well = next(wells_list_6_well)
                total_vol_enzyme = 0

            query_clip_in_design = ytk_stitch_list.query.filter_by(unique_job_id=jobnumber, stitch_well_id=stitch_well[0],
                                                                   stitch_plate_number=stitch_plate + 1).first()

            add_to_enzyme_plate = ytk_stitch_enzyme(unique_job_id=jobnumber, stitch_well_id=stitch_well[0],
                                                    stitch_barcode=str(jobnumber) + "-S-" + str(stitch_plate + 1),
                                                    stitch_id=query_clip_in_design.stitch_id,
                                                    transfer_volume=enzyme_volume,
                                                    enzyme_plate_barcode=str(jobnumber) + "-B-" + str(
                                                      well_from_6well[1]),
                                                    enzyme_plate_well_id=well_from_6well[0],
                                                    enzyme_plate_number=well_from_6well[1]
                                                    )

            db.session.add(add_to_enzyme_plate)

    # fill in the table with the amounts of enzyme
    add_enzyme_amounts_to_table = ytk_buffer_plate_wells(unique_job_id=jobnumber,
                                                         buffer_plate_well_id=well_from_6well[0],
                                                         loading_volume=total_vol_enzyme,
                                                         buffer_plate_barcode=str(jobnumber) + "-B-" + str(
                                                             well_from_6well[1]),
                                                         buffer_name="Enzyme Mastermix",
                                                         buffer_plate_number=well_from_6well[1])
    db.session.add(add_enzyme_amounts_to_table)


def create_clone_plate_level2_ytk(jobnumber):

    query_stitch_in_design = ytk_stitch_enzyme.query.filter_by(unique_job_id=jobnumber).all()

    list_of_stitch_barcodes = []

    for iter_though_list in query_stitch_in_design:
        if iter_though_list.stitch_barcode not in list_of_stitch_barcodes:
            list_of_stitch_barcodes.append(iter_though_list.stitch_barcode)
        else:
            pass


    # iterate through the barcodes
    for barcode in list_of_stitch_barcodes:
        # iterate through the stitches for each barcode
        stitch_query = ytk_stitch_enzyme.query.filter_by(unique_job_id=jobnumber, stitch_barcode=barcode).all()
        for stitch in stitch_query:

            # lookup the equivalent well
            find_equivalent_well = quadrant_wells_lookup.query.filter_by(
                well_id_384=stitch.stitch_well_id).first()

            # turn number into quadrant
            plate_name=return_quadrant(find_equivalent_well.plate_number_96)

            add_record_to_stitch_clone = ytk_stitch_clone(unique_job_id=jobnumber,
                                                          clone_plate_well_id_96=find_equivalent_well.well_id_96,
                                                          well_number_96=find_equivalent_well.well_number_96,
                                                          stitch_well_id=stitch.stitch_well_id,
                                                          stitch_plate_barcode=barcode,
                                                          clone_plate_barcode=barcode + "-" + plate_name,
                                                          stitch_id=stitch.stitch_id)

            db.session.add(add_record_to_stitch_clone)

    db.session.commit()

