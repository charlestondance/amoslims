from Bio.Seq import Seq
from Bio import SeqIO, SeqFeature
from Bio.Alphabet.IUPAC import IUPACAmbiguousDNA
import requests, json
from dna_features_viewer import BiopythonTranslator
from dna_features_viewer import (GraphicFeature, GraphicRecord,
                                 CircularGraphicRecord)
from dnacauldron import (load_record, BASICLigationMix, full_assembly_report)
from ..models import PartsTable, part_dna_sizes
from .. import db
from Bio.Restriction import *


URL_OF_ICE_REST_PARTS = ICE_URL

HEADERS = {
        'x-ice-api-token': OWN_TOKEN,
        'x-ice-api-token-client': "amos_app"
}


def return_ice_id(part_id):
    # lookup the parts table and get the ice id
    ice_part_id = PartsTable.query.filter_by(part_id=part_id).first()

    return ice_part_id.sequence


def return_full_url(URL_OF_ICE_REST_PARTS, ice_id):
    # return the url of the ice id
    full_url = URL_OF_ICE_REST_PARTS + ice_id +'/sequence/'

    return full_url


def return_seqrecord_from_ice_id(ice_id, URL_OF_ICE_REST_PARTS, HEADERS, ldf_id):

    url_of_ice_part = return_full_url(URL_OF_ICE_REST_PARTS=URL_OF_ICE_REST_PARTS, ice_id=ice_id)
    r = requests.get(url_of_ice_part, headers=HEADERS, verify=False)

    sequence_record = return_seq_record_with_features_from_genbank(r=r, part_id=ldf_id)

    return sequence_record


def add_feature(sequence_rec, start_postion, end_position, strand, name, feature_type, feature_id):
    # add a feature to the seq record

    my_feature_location = SeqFeature.FeatureLocation(start_postion-1, end_position, strand=strand)
    my_feature = SeqFeature.SeqFeature(my_feature_location, type=feature_type, id=feature_id)
    my_feature.qualifiers["label"] = name

    return my_feature


def return_seq_record_with_features_from_genbank(r, part_id):
    # take a request object and add the features to it

    sequence_from_ice = r.json()
    amb = IUPACAmbiguousDNA()
    sequence_rec = SeqIO.SeqRecord(Seq(sequence_from_ice['sequence'], amb), id=part_id, name=part_id)

    for feature in sequence_from_ice['features']:
        # add_feature(sequence_rec=sequence_rec)
        start_position = feature['locations'][0]['genbankStart']
        end_position = feature['locations'][0]['end']
        strand = feature['strand']
        name_of_feature = feature['name']
        type_of_feature = feature['type']
        id_of_feature = feature['id']

        my_feature = add_feature(sequence_rec=sequence_rec, start_postion=start_position, end_position=end_position,
                                 strand=strand, name=name_of_feature, feature_type=type_of_feature,
                                 feature_id=id_of_feature)

        sequence_rec.features.append(my_feature)

    return sequence_rec


def return_part_ids_for_clip_in_correct_order(part1id, part2id, part3id):

    ldf_part1_id = PartsTable.query.filter_by(part_id=part1id).first()
    ldf_part2_id = PartsTable.query.filter_by(part_id=part2id).first()
    ldf_part3_id = PartsTable.query.filter_by(part_id=part3id).first()

    dict_of_postiion = {}

    dict_of_postiion[ldf_part1_id.relative_position] = ldf_part1_id
    dict_of_postiion[ldf_part2_id.relative_position] = ldf_part2_id
    dict_of_postiion[ldf_part3_id.relative_position] = ldf_part3_id

    return dict_of_postiion


def do_virtual_cutter(part_info):

    seq_record = return_seqrecord_from_ice_id(ice_id=part_info.sequence, URL_OF_ICE_REST_PARTS=URL_OF_ICE_REST_PARTS,
                                              HEADERS=HEADERS, ldf_id=part_info.part_id)

    # check if basic part
    if part_info.part_method == 'BASIC' and part_info.relative_position == 'Centre':
        cargo_sizes = return_basic_cargo(seq_record)
        write_sizes_to_database(cargo_sizes=cargo_sizes, name_of_fragment='BsaI', part_info=part_info)
    else:
        cargo_sizes = [len(seq_record.seq)]

    return


def return_basic_cargo(seq_record):

    digest = BsaI.catalyse(seq_record.seq, linear=False)

    list_of_sizes = []

    for fragment in digest:
        lower_fragment = fragment.lower()
        print(lower_fragment[0:4], lower_fragment[-4:])

        if lower_fragment[0:4] == "gtcc" and lower_fragment[-2:] == 'gg':
            list_of_sizes.insert(0, len(fragment))
            print('in hing')
        else:
            list_of_sizes.append(len(fragment))
        print(list_of_sizes)

    return list_of_sizes


def write_sizes_to_database(cargo_sizes, name_of_fragment, part_info):

    # delete the existing sizes
    delete_parts = part_dna_sizes.query.filter_by(part_id=part_info.part_id).all()

    if delete_parts:
        for row in delete_parts:
            print('in delete')
            db.session.delete(row)
            db.session.commit()

    for i, size in enumerate(cargo_sizes):
        add_part = part_dna_sizes(part_id=part_info.part_id, enzyme=name_of_fragment, size=size, cargo_number=i)
        db.session.add(add_part)

    db.session.commit()

    return
