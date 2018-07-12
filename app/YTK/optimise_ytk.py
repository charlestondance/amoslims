from app import db
from app.models import ytk_unique_clip, ytk_design, ytk_unique_part, ytk_job_master, ytk_stitch_list
import math
from copy import deepcopy
from dnacauldron import single_assembly
import random
from dna_features_viewer import BiopythonTranslator
import re
from ..main.jbei_ice_functions import *


def return_list_of_letters(number_of_clips_in_stitch):

    canonical_list_of_stitch_length = []

    letter = "A"

    canonical_list_of_stitch_length.append(letter)
    for x in range(0, number_of_clips_in_stitch-1):
        letter = str(chr(ord(letter)+1))
        canonical_list_of_stitch_length.append(letter)

    return canonical_list_of_stitch_length


def return_list_of_parts_for_a_clip(clip_parts):

    part_list = []

    for part in clip_parts:
        part_list.append(part['part_id'])

    return part_list


def return_dict_from_query(query_to_unpack):
    # take a db engine query and return a list of dict of each row
    list_of_query = []

    for line in query_to_unpack:
        line_dict = dict(zip(line.keys(), line))
        list_of_query.append(line_dict)

    return list_of_query


def optimise_ytk_design(jobname):
    # optimise design and return dict if there are any errors

    job_optimise_status = {}
    job_optimise_status['success'] = True

    unique_stitch_ids = get_list_of_unique_stitch_ids_ytk(jobname=jobname)

    # check all parts exist in database
    list_of_parts_missing = check_all_parts_exist_in_database_ytk(jobname=jobname)
    if len(list_of_parts_missing) != 0:
        job_optimise_status['list_of_missing_parts'] = list_of_parts_missing
        job_optimise_status['success'] = False
    else:
        # check design always as increments of letters starting from A for clip
        size_constant_letter_increment_bool = check_job_is_constant_letter_increment_ytk(jobname=jobname, unique_stitch_ids=unique_stitch_ids)

        if size_constant_letter_increment_bool == False:
            job_optimise_status['size_constant_letter_increment_bool'] = size_constant_letter_increment_bool
            job_optimise_status['success'] = False
        else:

            list_of_clip_list = create_unique_clip_list_ytk(jobname=jobname, unique_stitch_ids=unique_stitch_ids)
            add_unique_clips_to_db_ytk(jobname=jobname, list_of_clip_list=list_of_clip_list)
            find_clip_from_design_and_update_batches_ytk(jobname=jobname, unique_stitch_ids=unique_stitch_ids)
            update_design_with_clip_batches_ytk(jobname=jobname, unique_stitch_ids=unique_stitch_ids)
            create_unique_part_list_table_ytk(jobname=jobname, unique_stitch_ids=unique_stitch_ids)
            update_unique_parts_table_based_on_unique_clips_ytk(jobname=jobname)
            update_unique_parts_table_with_samples_required_ytk(jobname=jobname)
            update_design_with_part_batches_ytk(jobname=jobname)
            create_job_master_table_ytk(jobname=jobname)

    return job_optimise_status


def get_list_of_unique_stitch_ids_ytk(jobname):
    """this function returns a list of unique stitch ids from the table design for a given job number"""
    # stitch_ids = ytk_design.query.options(load_only(stitch_id)).distinct(ytk_design.stitch_id).filter_by(unique_job_id=jobname).order_by(ytk_design.stitch_id)
    stitch_ids = db.engine.execute("SELECT DISTINCT stitch_id FROM ytk_design WHERE unique_job_id=%s ORDER BY stitch_id", (jobname))

    unique_stitch_ids = []

    # pull out the first element in the tuple to form a list of unique stitch ids
    for x in stitch_ids:
        unique_stitch_ids.append(x[0])

    return unique_stitch_ids

def check_all_parts_exist_in_database_ytk(jobname):
    # return a list of parts from a design that is not in the database
    list_of_parts_not_in_db = []

    # get a list of the unique parts
    # unique_parts_dict = ytk_design.query.options(load_only(part_id)).filter_by(unique_job_id=jobname).distinct(ytk_design.part_id).order_by(ytk_design.part_id)
    sql = "SELECT DISTINCT part_id from ytk_design where unique_job_id=%s ORDER BY part_id"

    unique_parts_query = db.engine.execute(sql, jobname)
    unique_parts_dict = return_dict_from_query(unique_parts_query)

    for part in unique_parts_dict:
        query_parts_table = PartsTable.query.filter_by(part_id=part['part_id']).first()
        if query_parts_table is None:
            list_of_parts_not_in_db.append(part['part_id'])

    return list_of_parts_not_in_db


def check_all_list_of_sequential_letters_ytk(jobname, unique_stitch_ids, number_of_clips_in_stitch):
    # return true if all stitches are correctly in range of letters

    list_of_bad_stitches = []

    canonical_list_of_stitch_length = return_list_of_letters(number_of_clips_in_stitch)

    for stitch in unique_stitch_ids:
        check_stitch = []
        # clip_letters = ytk_design.query.options(load_only(clip_id)).filter_by(unique_job_id=jobname, stitch_id=stitch).distinct(ytk_design.clip_id).order_by(ytk_design.clip_id)
        clip_letters = db.engine.execute("SELECT DISTINCT clip_id from ytk_design where unique_job_id=%s "
                                         "AND stitch_id=%s ORDER BY clip_id", (jobname, stitch))

        for letter in clip_letters:
            check_stitch.append(letter[0])

        if canonical_list_of_stitch_length == check_stitch:
            pass
        else:
            list_of_bad_stitches.append(stitch)

    return list_of_bad_stitches


def create_unique_clip_list_ytk(jobname, unique_stitch_ids):
# find the list of only unique clips from the database with level 1

    list_of_clip_list = []

    for stitch in unique_stitch_ids:
        # for each stitch get the incremental letter list
        #clip_length_query = basic_joblength.query.filter_by(unique_job_id=jobname, stitch_id=stitch).first()
        clip_letters = return_list_of_letters(4)

        for letter in clip_letters:

            clip_list = []
            # clip = ytk_design.query.options(load_only(clip_id, part_id)).filter_by(unique_job_id=jobname, stitch_id=stitch, clip_id=letter, level=1).load_only(ytk_design.clip_id, ytk_design.part_id).order_by(ytk_design.part_id)
            clip = db.engine.execute("SELECT clip_id, part_id from ytk_design where unique_job_id=%s AND stitch_id=%s"
                                     " AND clip_id=%s AND level=%s ORDER BY part_id",(jobname, stitch, letter, 1))

            for part in clip:
                part_list = dict(zip(clip.keys(), part))
                clip_list.append(part_list['part_id'])

            if clip_list not in list_of_clip_list:
                list_of_clip_list.append(clip_list)

    return list_of_clip_list


def add_unique_clips_to_db_ytk(jobname, list_of_clip_list):
    # load the unique clips to the database and give them a number
    # clips must be 4 in length or ploblems
    clip_number = 1

    for clip in list_of_clip_list:

        if len(clip) == 4:
            print(clip)
            item_add = ytk_unique_clip(unique_job_id=jobname, clip_number=clip_number, part_1_id=clip[0],
                                       part_2_id=clip[1], part_3_id=clip[2], part_4_id=clip[3], number_of_times_used=0,
                                       clip_batches_required=1, clip_id_job_id_no_batch_id=jobname+'-C'+str(clip_number))
            db.session.add(item_add)

            clip_number += 1

def check_job_is_constant_letter_increment_ytk(jobname, unique_stitch_ids):
    # check each stitch of the job is a set of incrementing letters and return a boolean
    successful_letters = True

    for stitch in unique_stitch_ids:
        # check each stitch of the job is a set of incrementing letters and return a boolean
        letter_list = []
        # check_clip_query = ytk_design.query.options(load_only(clip_id)).filter_by(unique_job_id=jobname, stitch_id=stitch).distinct(ytk_design.clip_id).order_by(ytk_design.clip_id)
        sql = "SELECT clip_id FROM ytk_design WHERE unique_job_id=%s AND stitch_id=%s GROUP BY clip_id ORDER BY clip_id"
        params = (jobname, stitch)
        check_clip_query = db.engine.execute(sql, params)
        for clip in check_clip_query:
            letter_list.append(clip[0])

        if letter_list == return_list_of_letters(len(letter_list)):
            pass
        else:
            successful_letters = False

    return successful_letters


def create_unique_part_list_table_ytk(jobname, unique_stitch_ids):
    sql = "SELECT DISTINCT part_id from ytk_design where unique_job_id=%s AND level=%s ORDER BY part_id"

    unqiue_parts_query = db.engine.execute(sql, (jobname, 1))
    unique_parts_dict = return_dict_from_query(unqiue_parts_query)

    for part in unique_parts_dict:
        item_add = ytk_unique_part(unique_job_id=jobname, part_id=part['part_id'], number_of_times_used=0,
                                   samples_required=0)
        db.session.add(item_add)

    db.session.commit()


def update_unique_parts_table_based_on_unique_clips_ytk(jobname):

    # for each part in the unique clip table update the number of times used
    sql = "SELECT DISTINCT clip_number from ytk_unique_clip where unique_job_id=%s ORDER BY clip_number"
    unique_clip_query = db.engine.execute(sql, jobname)
    unique_clip_dict = return_dict_from_query(unique_clip_query)

    for clip in unique_clip_dict:
        # do part 1
        clip_query = ytk_unique_clip.query.filter_by(unique_job_id=jobname, clip_number=clip['clip_number']).first()
        if clip_query.part_1_id != 'EMPTY':
            find_part = ytk_unique_part.query.filter_by(unique_job_id=jobname, part_id=clip_query.part_1_id).first()
            find_part.number_of_times_used += clip_query.clip_batches_required
            db.session.commit()
        else:
            pass
        # do part 2
        if clip_query.part_2_id != 'EMPTY':
            clip_query = ytk_unique_clip.query.filter_by(unique_job_id=jobname, clip_number=clip['clip_number']).first()
            find_part = ytk_unique_part.query.filter_by(unique_job_id=jobname, part_id=clip_query.part_2_id).first()
            find_part.number_of_times_used += clip_query.clip_batches_required
            db.session.commit()
        else:
            pass
        # do part 3
        if clip_query.part_3_id != 'EMPTY':
            clip_query = ytk_unique_clip.query.filter_by(unique_job_id=jobname, clip_number=clip['clip_number']).first()
            find_part = ytk_unique_part.query.filter_by(unique_job_id=jobname, part_id=clip_query.part_3_id).first()
            find_part.number_of_times_used += clip_query.clip_batches_required
            db.session.commit()
        else:
            pass
        # do part 4
        if clip_query.part_4_id != 'EMPTY':
            clip_query = ytk_unique_clip.query.filter_by(unique_job_id=jobname, clip_number=clip['clip_number']).first()
            find_part = ytk_unique_part.query.filter_by(unique_job_id=jobname, part_id=clip_query.part_4_id).first()
            find_part.number_of_times_used += clip_query.clip_batches_required
            db.session.commit()
        else:
            pass

def update_unique_parts_table_with_samples_required_ytk(jobname):
    # from the number of times a part is used, calculate the number of samples required
    part_vol = 500
    ldv_limit = 8000

    # get a list of the unique parts
    sql = "SELECT DISTINCT part_id from ytk_unique_part where unique_job_id=%s ORDER BY part_id"

    unique_parts_query = db.engine.execute(sql, jobname)
    unique_parts_dict = return_dict_from_query(unique_parts_query)

    for part in unique_parts_dict:

        find_part = ytk_unique_part.query.filter_by(unique_job_id=jobname, part_id=part['part_id']).first()

        find_part.total_volume_required = (find_part.number_of_times_used*part_vol)
        find_part.volume_per_part = part_vol
        find_part.samples_required = math.ceil(find_part.total_volume_required/ldv_limit)
        db.session.commit()


def update_design_with_part_batches_ytk(jobname):

    # get a unique list of clips
    sql = "SELECT clip_number from ytk_unique_clip where unique_job_id=%s ORDER BY clip_number"
    unique_clip_query = db.engine.execute(sql, jobname)
    unique_clip_list = return_dict_from_query(unique_clip_query)

    big_list_of_hing = []
    print(unique_clip_list)
    # for each clip
    for clip in range(1, len(unique_clip_list)+1):
        print('clip ', str(clip))
        # this query can be used for the unique clips
        clip_parts_query = ytk_unique_clip.query.filter_by(clip_number=clip, unique_job_id=jobname).first()

        # get the parts in each clip
        clip_parts = return_list_of_parts_from_ORM_unique_clip_query_ytk(clip_parts_query=clip_parts_query)
        for part in clip_parts:
            if part != 'EMPTY':
                # find out the number of samples take out for part and create an intertools cycle iterator
                unique_part_query = ytk_unique_part.query.filter_by(part_id=part, unique_job_id=jobname).first()
                list_of_samples_integers = list(range(1, unique_part_query.samples_required+1))

                # randomise the list so it doesnt start at the same sample each time
                random.shuffle(list_of_samples_integers)
                cycle_part_sample = itertools.cycle(list_of_samples_integers)

                for clip_batch_iterate in range(1, clip_parts_query.clip_batches_required):

                    part_sample_number = next(cycle_part_sample)

                    #sql = "UPDATE ytk_design SET part_id_sample_id=%s where unique_job_id=%s AND unique_clip_number=%s AND clip_id_batch_id=%s AND part_id=%s"
                    #unique_clip_query = db.engine.execute(sql, [part_sample_number, jobname, clip['clip_number'], clip_batch_iterate, part])

                    design_query = ytk_design.query.filter_by(unique_job_id=jobname, unique_clip_number=clip,
                                                              clip_id_batch_id=clip_batch_iterate, part_id=part).order_by(ytk_design.stitch_id).all()

                    for row in design_query:
                        row_string = ''.join([row.part_id, ', unique clip number', str(row.unique_clip_number),
                                              ', clip id batch id ', str(row.clip_id_batch_id), 'clip batch iterator ',
                                              str(clip_batch_iterate), ', stitch id ',str(row.stitch_id),
                                              ', sample number ', str(part_sample_number)])
                        line_qeury_to_update = ytk_design.query.filter_by(unique_job_id=jobname,
                                                                          unique_clip_number=clip,
                                                                          clip_id_batch_id=clip_batch_iterate,
                                                                          part_id=part,
                                                                          stitch_id=row.stitch_id).first()
                        line_qeury_to_update.part_id_sample_id = part_sample_number

                        db.session.commit()
            else:
                pass


def return_random_batch_from_part_id(part_id, jobname):
    # return a random integer between the number of samples required
    unique_part_query = ytk_unique_part.query.filter_by(part_id=part_id, unique_job_id=jobname).first()

    return random.randint(1, unique_part_query.samples_required)


def return_list_of_parts_from_ORM_unique_clip_query_ytk(clip_parts_query):

    clip_parts = []
    clip_parts.append(clip_parts_query.part_1_id)
    clip_parts.append(clip_parts_query.part_2_id)
    clip_parts.append(clip_parts_query.part_3_id)
    clip_parts.append(clip_parts_query.part_4_id)

    return clip_parts


def create_job_master_table_ytk(jobname):
    sql = "SELECT ytk_unique_part.unique_job_id, ytk_unique_part.part_id, ytk_unique_part.samples_required AS units " \
          "FROM ytk_unique_part WHERE ytk_unique_part.unique_job_id=%s"

    unique_part_query = db.engine.execute(sql, jobname)

    for part in unique_part_query:
        for unit in range(1,part.units+1):
            # get the highest number batch of the part and write the number of copies to the htable
            # PartsBatchTable.query.filter_by(part_id=part.part_id).order_by(PartsBatchTable.batch_number.desc())
            sql2 = "SELECT * from partsbatchtable WHERE part_id=%s order by batch_number DESC"
            query_batch_table = db.engine.execute(sql2, part.part_id)
            query_batch_table = query_batch_table.fetchone()
            add_batch = ytk_job_master(unique_job_id=jobname, part_id=part.part_id, sample_number=unit,
                                       storage_location_id=query_batch_table.storage_location_id,
                                       storage_plate_barcode=query_batch_table.storage_plate_barcode)
            db.session.add(add_batch)

    db.session.commit()


def find_clip_from_design_and_update_batches_ytk(jobname, unique_stitch_ids):

    # assumption is that with 50ul elution you can get 3x12 ul out
    working_elution_volume = 24000
    GOLDEN_GATE_VOLUME = 500

    for stitch in unique_stitch_ids:

        # for each stitch get the incremental letter list which for ytk is 4
        clip_letters = return_list_of_letters_in_stitch(jobname=jobname, stitch=stitch)

        for letter in clip_letters:
            clip_ids = db.engine.execute("SELECT clip_id, stitch_id, part_id FROM ytk_design WHERE unique_job_id=%s "
                                         "AND stitch_id=%s AND clip_id=%s AND level=%s ORDER BY part_id",
                                         (jobname, stitch, letter, 1))

            # turn the query into a usable dict
            clip_parts = return_dict_from_query(clip_ids)
            # turn that into an ordered list of just the parts
            part_list_of_clip = return_list_of_parts_for_a_clip(clip_parts)

            if len(part_list_of_clip) == 4:
                pass
            else:
                padding = 4 - len(part_list_of_clip)
                for y in range(0, padding):
                    part_list_of_clip.append('EMPTY')

            print(part_list_of_clip)

            find_clip = ytk_unique_clip.query.filter_by(unique_job_id=jobname, part_1_id=part_list_of_clip[0],
                                                        part_2_id=part_list_of_clip[1], part_3_id=part_list_of_clip[2],
                                                        part_4_id=part_list_of_clip[3]).first()

            # increment the use counter and batches in unique table if required
            find_clip.number_of_times_used += 1
            if find_clip.number_of_times_used != 1:
                # check if a new batch is required
                if (find_clip.number_of_times_used*GOLDEN_GATE_VOLUME) % working_elution_volume == 0:
                    find_clip.clip_batches_required += 1

            db.session.commit()

            # update the design table
            sql = "UPDATE ytk_design SET unique_clip_number=%s WHERE unique_job_id=%s AND stitch_id=%s AND clip_id=%s"
            #sql = "UPDATE design SET clip_id_batch_id = clip_id_batch_id + %s WHERE unique_job_id=%s AND stitch_id=%s AND clip_id=%s"

            params = (find_clip.clip_number, jobname, stitch, letter)
            #params = (batch_counter_increment, jobname, stitch, letter)
            db.engine.execute(sql, params)
            db.session.commit()


def update_design_with_clip_batches_ytk(jobname, unique_stitch_ids):

    # get a unique list of clips
    sql = "SELECT clip_number from ytk_unique_clip where unique_job_id=%s ORDER BY clip_number"
    unique_clip_query = db.engine.execute(sql, jobname)
    unique_clip_list = return_dict_from_query(unique_clip_query)

    for clip in range(1, len(unique_clip_list)+1):

        find_clip_batches = ytk_unique_clip.query.filter_by(unique_job_id=jobname, clip_number=clip).first()
        print(find_clip_batches)

        list_of_samples_integers = list(range(1, find_clip_batches.clip_batches_required + 1))
        # randomise the list so it doesnt start at the same sample each time
        random.shuffle(list_of_samples_integers)
        cycle_part_sample = itertools.cycle(list_of_samples_integers)

        # get list of unique stitches that contain this clip
        find_stitches_to_this_clip = ytk_design.query.filter_by(unique_job_id=jobname,
                                                                unique_clip_number=clip).distinct(ytk_design.stitch_id).all()

        for stitch in find_stitches_to_this_clip:

            batch_chooser = next(cycle_part_sample)
            print(batch_chooser, jobname, clip, stitch.stitch_id)

            stitch_cast = str(stitch.stitch_id)
            #find_design_stitch = ytk_design.query.filter_by(unique_job_id=jobname, stitch_id=stitch, unique_clip_number=clip,level=1).first()
            sql = "UPDATE ytk_design SET clip_id_batch_id=%s where unique_job_id=%s AND unique_clip_number=%s " \
                  "AND stitch_id=%s"
            db.engine.execute(sql, [batch_chooser, jobname, clip, stitch_cast])

            db.session.commit()
"""
    for stitch in unique_stitch_ids:

        clip_letters = return_list_of_letters_in_stitch(jobname=jobname, stitch=stitch)

        for letter in clip_letters:

            find_design_stitch = ytk_design.query.filter_by(unique_job_id=jobname, stitch_id=stitch, clip_id=letter,
                                                            level=1).first()

            find_clip_batches = ytk_unique_clip.query.filter_by(unique_job_id=jobname,
                                                                clip_number=find_design_stitch.unique_clip_number).first()

            list_of_samples_integers = list(range(1, find_clip_batches.clip_batches_required + 1))
            # randomise the list so it doesnt start at the same sample each time
            random.shuffle(list_of_samples_integers)

            update_design_stitch = ytk_design.query.filter_by(unique_job_id=jobname, stitch_id=stitch, clip_id=letter,
                                                              level=1).all()

            for clip_update in update_design_stitch:
                clip_update.clip_id_batch_id = list_of_samples_integers[0]

    db.session.commit()
"""


def return_list_of_letters_in_stitch(jobname, stitch):
    # check the design for the number of level one ltters and return its length

    sql = "SELECT clip_id FROM ytk_design WHERE unique_job_id=%s and stitch_id=%s and level=%s group by clip_id"


    query_the_table = db.engine.execute(sql, (jobname, stitch, 1))

    return return_list_of_letters(query_the_table.rowcount)


class MyCustomTranslator(BiopythonTranslator):
    """
        Custom translator implementing the following theme:

        Terminators in red, CDS in gold, promoter in green, origin of replication in purple.

    """

    def compute_feature_color(self, feature):
        if feature.type == "CDS":
            return "gold"
        elif feature.type == "promoter":
            return "green"
        elif feature.type == "terminator":
            return "red"
        elif feature.type == "rep_origin":
            return "purple"
        else:
            return "blue"

    # remove residual homology labels in the PNG files
    def compute_feature_label(self, feature):

        if "homology" in str(feature.qualifiers.get("label", '')):
            return None
        else:
            return BiopythonTranslator.compute_feature_label(feature)


def feature_removal(filename, jobnumber):
    # take out unnecessary features that confuse the assembly process
    discard = ['homology', 'parta', 'partb', 'partc', 'cassette (RECEPTOR)']
    if not os.path.exists('./app/YTK/static/YTK/%s/stitches/fixed_clips' % jobnumber):
        os.makedirs('./app/YTK/static/YTK/%s/stitches/fixed_clips' % jobnumber)
    with open(filename, 'rU') as input:
        file = os.path.basename(filename)
        for record in SeqIO.parse(input, 'genbank'):
            for index, feature in enumerate(record.features):
                if "label" in feature.qualifiers:
                    if feature.qualifiers['label'][0] in discard:
                        record.features.pop(index)
                elif "source" in feature.qualifiers:
                    if feature.qualifiers['source'][0] in discard:
                        record.features.pop(index)
            SeqIO.write(record, './app/YTK/static/YTK/%s/stitches/fixed_clips/%s' % (jobnumber, file), 'genbank')


class YeastClipReaction:

    def __init__(self, jobnumber):
        self.jobnumber = jobnumber
        self.clip_list = []
        self.list_of_parts_dict = []
        self.clip_ID_set = []

    def create_directory(self):
        if not os.path.exists('./app/YTK/static/YTK/%s/sequences' % self.jobnumber):
            os.makedirs('./app/YTK/static/YTK/%s/sequences' % self.jobnumber)

    def database_query(self):
        # pull LDF ID's for each clip reaction in specific job
        clip_query = ytk_unique_clip.query.filter_by(unique_job_id=self.jobnumber).all()

        # obtain part type and ICE ID for each part in specific job
        sql = "SELECT partstable.part_id, partstable.part_type, partstable.sequence FROM partstable JOIN ytk_unique_part " \
              "ON partstable.part_id = ytk_unique_part.part_id WHERE ytk_unique_part.unique_job_id =%s "
        parts_query = db.engine.execute(sql, (self.jobnumber))
        unique_part_list = return_dict_from_query(parts_query)

        part_dict = {}
        # compare queries to obtain all required information for the clip reaction and put into one list of dictionaries
        for clip in clip_query:
            clip_part_list = [clip.part_1_id, clip.part_2_id, clip.part_3_id, clip.part_4_id]
            for part in unique_part_list:
                part_num = part['part_id']
                if part_num in clip_part_list:
                    part_dict['LDF_ID'] = part['part_id']
                    part_dict['part_type'] = part['part_type']
                    part_dict['ICE_ID'] = part['sequence']
                    part_dict['clip_num'] = clip.clip_number
                    part_dict['job_id'] = clip.unique_job_id
                    self.list_of_parts_dict.append(deepcopy(part_dict))
        return self.list_of_parts_dict

    def create_genbankfiles_and_assembly(self):
        # get unique clip ID's
        self.clip_ID_set = set(p['clip_num'] for p in self.list_of_parts_dict)

        for i in self.clip_ID_set:
            clip_name = i
            specific_clip_list = []
            # Create GenBank files for each part from ICE
            URL_OF_ICE_REST_PARTS = 'https://ice.bg.ic.ac.uk:8443/rest/parts/'
            HEADERS = {
                'x-ice-api-token': "4/yPGRunJ1cGHAc0N7qw2SJ8bHZVlOEhDyU56VPwFBM=",
                'x-ice-api-token-client': "amos_app"
            }

            # create list with all entries from one clip to make assembly from
            for entry in self.list_of_parts_dict:
                if (entry['clip_num']) == clip_name:
                    specific_clip_list.append(entry)
                else:
                    continue
            print(specific_clip_list)
            # Create GenBank files for each part from ICE
            for part in specific_clip_list:
                if part['part_type'] == "Promoter":
                    partA = return_seqrecord_from_ice_id(part['ICE_ID'], URL_OF_ICE_REST_PARTS, HEADERS, part['LDF_ID'])
                    print(partA)
                    SeqIO.write(partA, './app/YTK/static/YTK/%s/partA.gb' % self.jobnumber, 'genbank')
                elif part['part_type'] == "CDS":
                    partB = return_seqrecord_from_ice_id(part['ICE_ID'], URL_OF_ICE_REST_PARTS, HEADERS, part['LDF_ID'])
                    SeqIO.write(partB, './app/YTK/static/YTK/%s/partB.gb' % self.jobnumber, 'genbank')
                elif part['part_type'] == "Terminator":
                    partC = return_seqrecord_from_ice_id(part['ICE_ID'], URL_OF_ICE_REST_PARTS, HEADERS, part['LDF_ID'])
                    SeqIO.write(partC, './app/YTK/static/YTK/%s/partC.gb' % self.jobnumber, 'genbank')
                else:
                    cassette = return_seqrecord_from_ice_id(part['ICE_ID'], URL_OF_ICE_REST_PARTS, HEADERS, part['LDF_ID'])

                    SeqIO.write(cassette, './app/YTK/static/YTK/%s/cassette.gb' % self.jobnumber, 'genbank')

            single_assembly(
                parts=["./app/YTK/static/YTK/%s/partA.gb" % self.jobnumber, "./app/YTK/static/YTK/%s/partB.gb" % self.jobnumber,
                       "./app/YTK/static/YTK/%s/partC.gb" % self.jobnumber],
                receptor="./app/YTK/static/YTK/%s/cassette.gb" % self.jobnumber, enzyme="BsaI",
                outfile=("./app/YTK/static/YTK/%s/sequences/" % self.jobnumber + "/C%s.gb" % clip_name))

        return self.clip_ID_set

    def create_png_files(self):
        for clip_name in self.clip_ID_set:
            graphic_record = MyCustomTranslator().translate_record("./app/YTK/static/YTK/%s/sequences/C%s.gb" % (self.jobnumber, clip_name))
            ax, _ = graphic_record.plot(figure_width=10)
            ax.figure.savefig("./app/YTK/static/YTK/%s/sequences/C%s.png" % (self.jobnumber, clip_name))
            clip_dict = {}
            clip_dict['Clip_ID'] = clip_name
            clip_dict['GB_file'] = str("./app/YTK/static/YTK/%s/sequences/C%s.gb" % (self.jobnumber, clip_name))
            clip_dict['PNG_file'] = str("./app/YTK/static/YTK/%s/sequences/C%s.png" % (self.jobnumber, clip_name))
            self.clip_list.append(clip_dict)

        return self.clip_list


class YeastStitchReaction:

    def __init__(self, jobnumber):
        self.jobnumber = jobnumber
        self.list_of_dict = []
        self.stitch_list = []
        self.stitch_ID_set = []

    def stitch_pathway(self):
        # create new directory for output files with jobnumber assigned
        if not os.path.exists('./app/YTK/static/YTK/%s/stitches' % self.jobnumber):
            os.makedirs('./app/YTK/static/YTK/%s/stitches' % self.jobnumber)

    def database_query(self):
        # NEEDS TO BE CHANGED TO THIS WHEN IMPLENTED
        # parts_query = ytk_stitch_list.query.filter_by(unique_job_id=self.jobnumber).all()
        parts_query = ytk_stitch_list.query.all()
        part_dict = {}
        for part in parts_query:
            # strip out trailing clip reaction codes ie. C1-2 to C1
            part_dict['Part_ID'] = re.sub(r'(.*[0-9])-[0-9]', r'\1', part.concatenated_clip_id)
            part_dict['Stitch_ID'] = part.stitch_id
            self.list_of_dict.append(deepcopy(part_dict))

        return self.list_of_dict

    def strip_features_from_gbfiles(self):
        # strip out unnecessary features from clip files that cause errors during the Single Assembly
        directory = os.fsencode("./app/YTK/static/YTK/%s/sequences" % self.jobnumber)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".gb"):
                feature_removal("./app/YTK/static/YTK/%s/sequences/%s" % (self.jobnumber, filename), self.jobnumber)
                continue
            else:
                continue

    def create_genbank_and_stitch_reaction(self):
        # create set of unique clips
        self.stitch_ID_set = set(p['Stitch_ID'] for p in self.list_of_dict)

        URL_OF_ICE_REST_PARTS = 'https://ice.bg.ic.ac.uk:8443/rest/parts/'
        HEADERS = {'x-ice-api-token': "4/yPGRunJ1cGHAc0N7qw2SJ8bHZVlOEhDyU56VPwFBM=", 'x-ice-api-token-client': "amos_app" }
   
        for i in self.stitch_ID_set:
            specific_stitch_list = []
            stitch_name = "stitch_" + str(i)
            for entry in self.list_of_dict:
                # pull out the LDF ID's in stitch list as to obtain the files needed from GenBank
                LDF_list = re.findall(r'LDF.*', entry['Part_ID'])
                if (entry['Stitch_ID']) == i:
                    # find entries that need files from ICE
                    if (entry['Part_ID']) in LDF_list:
                        # look up the ICE ID and part type in the partstable to pull records from GenBank
                        ldf_id = entry['Part_ID']
                        ICE_id_query = PartsTable.query.filter_by(part_id=ldf_id).all()
                        for item in ICE_id_query:
                            if item.part_type == 'Cassette_Spacer':
                                spacer = return_seqrecord_from_ice_id(item.sequence, URL_OF_ICE_REST_PARTS,
                                                                      HEADERS,entry['Part_ID'])
                                SeqIO.write(spacer,'./app/YTK/static/YTK/%s/stitches/spacer.gb' % self.jobnumber,'genbank')
                                specific_stitch_list.append('./app/YTK/static/YTK/%s/stitches/spacer.gb' % self.jobnumber)
                            else:
                                receptor = return_seqrecord_from_ice_id(item.sequence, URL_OF_ICE_REST_PARTS,
                                                                        HEADERS,entry['Part_ID'])
                                SeqIO.write(receptor, './app/YTK/static/YTK/%s/stitches/receptor.gb' % self.jobnumber,'genbank')

                    else:
                        specific_stitch_list.append('./app/YTK/static/YTK/%s/stitches/fixed_clips/%s.gb' %
                                                    (self.jobnumber, entry['Part_ID']))

            single_assembly(parts=specific_stitch_list,
                            receptor='./app/YTK/static/YTK/%s/stitches/receptor.gb' % self.jobnumber,
                            enzyme="BsmBI",
                            outfile=("./app/YTK/static/YTK/%s/stitches/%s.gb" % (self.jobnumber, stitch_name)))

        return self.stitch_ID_set

    def create_png_files(self):
        for stitch_name in self.stitch_ID_set:
            graphic_record = MyCustomTranslator().translate_record("./app/YTK/static/YTK/%s/stitches/stitch_%s.gb" %
                                                                   (self.jobnumber, stitch_name))
            ax, _ = graphic_record.plot(figure_width=10)
            ax.figure.savefig("./app/YTK/static/YTK/%s/stitches/stitch_%s.png" % (self.jobnumber, stitch_name))
            stitch_dict = {}
            stitch_dict['Stitch_ID'] = stitch_name
            stitch_dict['filename'] = str("stitch_%s" % stitch_name)
            self.stitch_list.append(stitch_dict)

        return self.stitch_list

