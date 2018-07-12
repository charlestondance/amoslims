import csv
from .. import db
from app.models import PartsTable, ytk_virgin_design


def check_part_ids_exist_in_database(cds_A, cds_B, cds_C, pcopy_A, pcopy_B, pcopy_C):
    pass


def check_part_id_exists_in_database(part_id):
    pass


def enough_parts_for_design():
    pass


def find_promoter(row, jobset_part, jobset_linker):
    clip_list_from_file = []

    # Find the promoter and return the id or error if the query returns more than one
    find_promoter_query = PartsTable.query.filter_by(job_set=jobset_part, part_class='Part',
                                                     part_type='Promoter',
                                                     level=row['Promoter_PC1']).all()

    clip_list_from_file.append(part_id_when_unique_query(find_promoter_query))

    # Get the methylated A prefix linker
    find_prefix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='Methylated', relative_position='Prefix', offset=1,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_prefix_query))

    # Get the RBS suffix pos 1 linker
    find_suffix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='RBS', relative_position='Suffix', offset=1,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_suffix_query))

    return clip_list_from_file


def part_id_when_unique_query(len_query):
    # returns the part id or error if len 1
    if len(len_query) == 1:
        return [len_query[0].part_id, len_query[0].part_name]
    else:
        return ['Error', 'Error']


def find_gene_a(row, jobset_part, jobset_linker, cds_partA):
    clip_list_from_file = []

    # find the gene a and return the id or error if the query returns more than one
    find_part_query = PartsTable.query.filter_by(part_id=cds_partA).all()
    clip_list_from_file.append(part_id_when_unique_query(find_part_query))

    # find the prefix linker wich is based on the strenth from the row
    find_prefix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                               part_type='RBS', relative_position='Prefix', offset=1,
                                               level=row['RBS_PC1_Pos1']).all()

    clip_list_from_file.append(part_id_when_unique_query(find_prefix_query))

    # get the RBS suffix pos 2 linker
    find_suffix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='RBS', relative_position='Suffix', offset=2,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_suffix_query))

    return clip_list_from_file


def find_gene_b(row, jobset_part, jobset_linker, cds_partB):
    clip_list_from_file = []

    # find the gene a and return the id or error if the query returns more than one
    find_part_query = PartsTable.query.filter_by(part_id=cds_partB).all()
    clip_list_from_file.append(part_id_when_unique_query(find_part_query))

    # find the prefix linker wich is based on the strength from the row
    find_prefix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='RBS', relative_position='Prefix', offset=2,
                                                   level=row['RBS_PC1_Pos2']).all()

    clip_list_from_file.append(part_id_when_unique_query(find_prefix_query))

    # get the RBS suffix pos 3 linker
    find_suffix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='RBS', relative_position='Suffix', offset=3,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_suffix_query))

    return clip_list_from_file

def find_gene_c(row, jobset_part, jobset_linker, cds_partC):
    clip_list_from_file = []

    # find the gene a and return the id or error if the query returns more than one
    find_part_query = PartsTable.query.filter_by(part_id=cds_partC).all()
    clip_list_from_file.append(part_id_when_unique_query(find_part_query))

    # find the prefix linker which is based on the strenth from the row
    find_prefix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='RBS', relative_position='Prefix', offset=3,
                                                   level=row['RBS_PC1_Pos3']).all()

    clip_list_from_file.append(part_id_when_unique_query(find_prefix_query))

    # get the methylated suffix
    find_suffix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='Methylated', relative_position='Suffix', offset=2,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_suffix_query))

    return clip_list_from_file


def find_plasmid(row, jobset_part, jobset_linker):
    clip_list_from_file = []

    # find the gene a and return the id or error if the query returns more than one
    find_part_query = PartsTable.query.filter_by(job_set=jobset_part, part_class='Part',
                                                 part_type='Plasmid',level=row['PCopy_PC1']).all()
    clip_list_from_file.append(part_id_when_unique_query(find_part_query))

    # find the prefix linker which is based on the strength from the row
    find_prefix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='Methylated', relative_position='Prefix', offset=2,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_prefix_query))

    # get the neutral suffix
    find_suffix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='Neutral', relative_position='Suffix', offset=1,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_suffix_query))

    return clip_list_from_file


def find_cmr(row, jobset_linker):

    clip_list_from_file = []

    # find the gene a and return the id or error if the query returns more than one
    find_part_query = PartsTable.query.filter_by(job_set="Standard_CmR").all()
    clip_list_from_file.append(part_id_when_unique_query(find_part_query))

    # find the prefix linker which is based on the strength from the row
    find_prefix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='Neutral', relative_position='Prefix', offset=1,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_prefix_query))

    # get the neutral suffix
    find_suffix_query = PartsTable.query.filter_by(job_set=jobset_linker, part_class='Linker',
                                                   part_type='Methylated', relative_position='Suffix', offset=1,
                                                   level=1).all()

    clip_list_from_file.append(part_id_when_unique_query(find_suffix_query))

    return clip_list_from_file


def which_plasmid_asked_for(level):
    pass


def delete_design_from(experiment_id):
    db.engine.execute("DELETE FROM ytk_virgin_design WHERE experiment_id=%s" % experiment_id)
    db.session.commit()


def create_ytk_design_max_4_gene(filename_read, cds_partA, cds_partB, cds_partC, cds_partD, experiment_id, jobset_part, jobset_cassetes):

    CHECK_KEYS = ['Stitch_ID', 'Promoter_MC1', 'Promoter_MC2', 'Promoter_MC3', 'Auxotrophic_Level', 'Auxotrophic_Type',
                  'GFP', 'RFP', 'BFP']

    # delete the design if it exits
    delete_design_from(experiment_id=experiment_id)

    with open(filename_read) as csvfile:
        reader = csv.DictReader(csvfile)
        dict_keys = reader.fieldnames
        print(dict_keys)
        for row in reader:

            # pad it out so it always uses a 4 part monocistron
            row = pad_out_row_if_promoter_is_not_there(row)
            # position 1
            get_pos1 = get_PW_info(promoter=row['Promoter_MC1'], cds=cds_partA, position=1, clip_id='A',
                                   jobset_part=jobset_part, jobset_cassetes=jobset_cassetes)
            for part in get_pos1:

                if row['Promoter_MC1'] == 'None':
                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="A", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='2')
                    db.session.add(add_part)
                else:
                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="A", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='1')
                    db.session.add(add_part)

            get_pos2 = get_PW_info(promoter=row['Promoter_MC2'], cds=cds_partB, position=2, clip_id='B',
                                   jobset_part=jobset_part, jobset_cassetes=jobset_cassetes)
            for part in get_pos2:

                if row['Promoter_MC2'] == 'None':
                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="B", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='2')
                    db.session.add(add_part)
                else:
                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="B", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='1')
                    db.session.add(add_part)

            get_pos3 = get_PW_info(promoter=row['Promoter_MC3'], cds=cds_partC, position=3, clip_id='C',
                                   jobset_part=jobset_part, jobset_cassetes=jobset_cassetes)
            for part in get_pos3:
                if row['Promoter_MC3'] == 'None':
                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="C", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='2')
                    db.session.add(add_part)
                else:
                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="C", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='1')
                    db.session.add(add_part)

            get_pos4 = get_PW_info(promoter=row['Promoter_MC4'], cds=cds_partD, position=4, clip_id='D',
                                   jobset_part=jobset_part, jobset_cassetes=jobset_cassetes)
            for part in get_pos4:

                if row['Promoter_MC4'] == 'None':

                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="D", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='2')
                    db.session.add(add_part)
                else:
                    add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="D", part_id=part[0],
                                                 part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='1')
                    db.session.add(add_part)

            get_yeast_int = get_yeast_integration(Auxotrophic_PW1_Level=row['Auxotrophic_Level'],
                                                  Auxotrophic_PW1_Type=row['Auxotrophic_Type'],
                                                  jobset_casettes=jobset_cassetes)
            for part in get_yeast_int:
                add_part = ytk_virgin_design(experiment_id=experiment_id, clip_id="E", part_id=part[0],
                                             part_name=part[1], stitch_id=row['Stitch_ID'], assembly_level='2')
                db.session.add(add_part)

    db.session.commit()


def get_PW_info(promoter, cds, position, clip_id, jobset_part, jobset_cassetes):
    # create the clip lists for the four genes if they are there or not
    clip_list = []

    # if no gene given then pad it with the spacer
    if cds == "":
        find_cds_query = PartsTable.query.filter_by(job_set=jobset_cassetes, part_class='Cassette',
                                                    part_type='Cassette_Spacer', offset=int(position)).all()
        clip_list.append(part_id_when_unique_query(find_cds_query))

    else:
        find_promoter_query = PartsTable.query.filter_by(job_set=jobset_part, part_class='Part', part_type='Promoter',
                                                         level=int(promoter), offset=int(position)).all()
        clip_list.append(part_id_when_unique_query(find_promoter_query))
        find_cds_query = PartsTable.query.filter_by(part_id=cds).all()
        clip_list.append(part_id_when_unique_query(find_cds_query))
        find_terminator_query = PartsTable.query.filter_by(job_set=jobset_part, part_class='Part',
                                                           part_type='Terminator', offset=int(position)).all()
        clip_list.append(part_id_when_unique_query(find_terminator_query))
        find_cassette_query = PartsTable.query.filter_by(job_set=jobset_cassetes, part_class='Cassette',
                                                         part_type='Cassette', offset=int(position)).all()
        clip_list.append(part_id_when_unique_query(find_cassette_query))

    return clip_list


def get_yeast_integration(Auxotrophic_PW1_Level, Auxotrophic_PW1_Type, jobset_casettes):

    # get the yeast integration plasmid

    yeast_integrations = {'1': 'URA3', '2': 'LEU2', '3': 'HIS3'}

    clip_list = []

    find_yeast_cassette_query = PartsTable.query.filter_by(job_set=jobset_casettes, part_class='Cassette',
                                                           part_type=Auxotrophic_PW1_Type,
                                                           level=Auxotrophic_PW1_Level).all()
    clip_list.append(part_id_when_unique_query(find_yeast_cassette_query))

    return clip_list


def pad_out_row_if_promoter_is_not_there(row):

    if 'Promoter_MC1' in row:
        pass
    else:
        row['Promoter_MC1'] = 'None'

    if 'Promoter_MC2':
        pass
    else:
        row['Promoter_MC2'] = 'None'

    if 'Promoter_MC3' in row:
        pass
    else:
        row['Promoter_MC3'] = 'None'

    if 'Promoter_MC4' in row:
        pass
    else:
        row['Promoter_MC4'] = 'None'

    return row
