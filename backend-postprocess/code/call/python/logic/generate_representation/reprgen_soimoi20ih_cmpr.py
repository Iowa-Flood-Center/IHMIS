from def_system import FolderDefinition, BinDefinition, LinksDefinition, Debug
from reprgen_lib import build_data_matrix, save_image_file, clean_folder
from reprgen_interface import ReprGenInterface
from def_onDemand import AncillaryOnDemand
from def_utils import GeneralUtils
import numpy as np
import time
import sys
import os

debug_level_arg = 1

# ####################################################### ARGS ####################################################### #

comparison_id_arg = ReprGenInterface.get_model_id(sys.argv)
timestamp_arg = ReprGenInterface.get_timestamp_opt(sys.argv)
flextime_arg = ReprGenInterface.get_flextime(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def generate_representation(sc_comparison_id, timestamp, flextime=None, runset_id=None, debug_lvl=0):
    """

    :param sc_comparison_id:
    :param timestamp:
    :param flextime: Numeric value with acceptable ranges of values from timestamp. If None, must be exact timestamp
    :param debug_lvl:
    :return:
    """

    requiered_product = 'ids_l'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # gets the two models
    sc_model_1, sc_model_2 = FolderDefinition.extracts_models_acronym_from_combination(sc_comparison_id)

    timestamp_1 = determine_timestamp_for_model(sc_model_1, timestamp, flextime, runset_id, debug_lvl=debug_lvl)
    timestamp_2 = determine_timestamp_for_model(sc_model_2, timestamp, flextime, runset_id, debug_lvl=debug_lvl)

    the_timestamp = GeneralUtils.round_timestamp_hour(min((timestamp_1, timestamp_2)))

    # define folders
    hist_t1_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_1, requiered_product,
                                                                            runset_id=runset_id)
    hist_t2_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_2, requiered_product,
                                                                            runset_id=runset_id)

    # define timestamps
    the_timestamp1 = timestamp_1 if timestamp_1 == the_timestamp else FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_t1_folder_path,
                                                                                                                                the_timestamp,
                                                                                                                                accept_range=flextime)
    the_timestamp2 = timestamp_2 if timestamp_2 == the_timestamp else FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_t2_folder_path,
                                                                                                                                the_timestamp,
                                                                                                                                accept_range=flextime)

    the_data_1 = get_data_matrix(sc_model_1, the_timestamp1, flextime=flextime, runset_id=runset_id,
                                 debug_lvl=debug_lvl)
    the_data_2 = get_data_matrix(sc_model_2, the_timestamp2, flextime=flextime, runset_id=runset_id,
                                 debug_lvl=debug_lvl)

    # function to be vectorized
    def compare_to_vect(model1_value, model2_value):
        if (model1_value == 0) and (model2_value == 0):
            return 1
        elif (model1_value != 0) and (model2_value == 0):
            return 0
        elif (model1_value == -1) or (model2_value == -1):
            return -1
        else:
            return model1_value / model2_value

    # generates difference vector
    the_data = np.vectorize(compare_to_vect, otypes=[np.float])(the_data_1, the_data_2)
    the_data[0] = -1

    # read mask
    aod = AncillaryOnDemand()
    mask = aod.get_linkid_hills_mask()

    # plot the data
    bin_matrix = build_data_matrix(mask, the_data, debug_lvl=debug_lvl)
    save_image_file(sc_comparison_id, 'soimoi20ih', bin_matrix, the_timestamp, runset_id=runset_id, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("reprgen_soiwac20ih_cmpr: generate_representation({0}) function took {1} seconds ".format(sc_comparison_id,
                                                                                                       d_time),
             1, debug_lvl)

    return


def determine_timestamp_for_model(sc_model_id, timestamp, flextime, runset_id, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp:
    :param flextime:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    requiered_product = 'ids_l'

    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                         runset_id=runset_id)

    # establish the timestamps
    if timestamp is None:
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)
    else:
        if flextime is None:
            the_timestamp = timestamp
        else:
            the_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path, timestamp,
                                                                                      accept_range=flextime)

    # basic checks 1
    if the_timestamp is None:
        Debug.dl("reprgen_soimoi20ih: not a single sl bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return False

    return the_timestamp


def get_data_matrix(sc_model_id, timestamp, flextime=None, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp:
    :param flextime:
    :param debug_lvl:
    :return:
    """

    requiered_product = 'ids_l'

    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                         runset_id=runset_id)

    filepath = os.path.join(hist_folder_path, BinDefinition.define_file_name(timestamp, requiered_product))

    Debug.dl("reprgen_soimoi20ih_cmpr: Reading '{0}'.".format(filepath), 1, debug_lvl)

    # basich check 2
    if not os.path.exists(filepath):
        Debug.dl("reprgen_soimoi20ih_cmpr: sl file not found ({0}).".format(filepath), 1, debug_lvl)
        return False

    # read data files
    return np.load(filepath)

# ####################################################### CALL ####################################################### #

generate_representation(comparison_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
