from def_system import FolderDefinition, BinDefinition, Debug
from reprgen_interface import ReprGenInterface
import pickle
import json
import sys
import os

debug_level_arg = 1
# reference_id = "usgsgagesdischclass"
representation_id = "disclausgssih"
product_id = "isdc"

# ####################################################### ARGS ####################################################### #

reference_id = ReprGenInterface.get_reference_id(sys.argv)
timestamp_arg = ReprGenInterface.get_timestamp_opt(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def generate_json_file(sc_reference_id, sc_product_id, sc_representation_id, timestamp, runset_id=None, debug_lvl=0):
    """

    :param sc_reference_id:
    :param sc_product_id:
    :param sc_representation_id:
    :param timestamp:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    # lat-lng file
    link_latlng_filepath = BinAncillaryDefinition.get_linkids_latlng_file_path()

    # establish the timestamps
    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_reference_id, sc_product_id,
                                                                         runset_id=runset_id)
    the_timestamp = timestamp if timestamp is not None \
        else FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    # basic checks
    if the_timestamp is None:
        Debug.dl("reprgen_usgsgagesdischclass: not a single isdc bin file for reference {0}.".format(sc_reference_id), 1,
                 debug_lvl)
        return False

    # read binary file of data
    bin_filename = BinDefinition.define_file_name(the_timestamp, sc_product_id)
    bin_filepath = os.path.join(hist_folder_path, bin_filename)
    with open(bin_filepath, "rb") as r_file:
        dict_data = pickle.load(r_file)

    # read binary file of lat-long positions
    with open(link_latlng_filepath, "rb") as r_file:
        dict_latlng = pickle.load(r_file)

    # change stuffs
    dict_datalatlng = {}
    for cur_linkid in dict_data.keys():
        if cur_linkid in dict_latlng.keys():
            dict_datalatlng[cur_linkid] = {'classif': dict_data[cur_linkid],
                                           'lat': dict_latlng[cur_linkid]['lat'],
                                           'lng': dict_latlng[cur_linkid]['lng']}

    # get destination folder
    json_folderpath = FolderDefinition.get_historical_img_folder_path(sc_reference_id, sc_representation_id,
                                                                      runset_id=runset_id)
    if not os.path.exists(json_folderpath):
        os.makedirs(json_folderpath)

    # write json file
    json_filename = bin_filename.replace('.p', '.json').replace(sc_product_id, sc_representation_id)  # TODO - do nicely
    json_filepath = os.path.join(json_folderpath, json_filename)
    with open(json_filepath, "w+") as w_file:
        json.dump(dict_datalatlng, w_file)

    Debug.dl("reprgen_usgsgagesdischclass: created file '{0}'.".format(json_filepath), 1, debug_lvl)

# ####################################################### CALL ####################################################### #

generate_json_file(reference_id, product_id, representation_id, timestamp_arg, runset_id=runset_id_arg,
                   debug_lvl=debug_level_arg)
