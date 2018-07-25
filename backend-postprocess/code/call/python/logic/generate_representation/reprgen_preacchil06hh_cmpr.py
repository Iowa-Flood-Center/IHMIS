import numpy as np
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from reprgen_lib import build_data_matrix, save_image_file, clean_folder
from libs.AncillaryOnDemand import AncillaryOnDemand
from libs.FolderDefinition import FolderDefinition
from libs.ReprGenInterface import ReprGenInterface
from libs.LinksDefinition import LinksDefinition
from libs.BinDefinition import BinDefinition
from libs.GeneralUtils import GeneralUtils
from libs.Debug import Debug
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
    :param flextime:
    :param debug_lvl:
    :return:
    """

    requiered_product = 'idv_p'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # gets the two models
    sc_model_1, sc_model_2 = FolderDefinition.extracts_models_acronym_from_combination(sc_comparison_id)

    timestamp00_1 = determine_timestamp00_for_model(sc_model_1, timestamp, flextime, requiered_product, runset_id,
                                                    debug_lvl=debug_lvl)
    timestamp00_2 = determine_timestamp00_for_model(sc_model_2, timestamp, flextime, requiered_product, runset_id,
                                                    debug_lvl=debug_lvl)

    the_timestamp = min((timestamp00_1, timestamp00_2))

    # determine timestamps at time 0 hour
    hist_folder_path_1 = FolderDefinition.get_intermediate_bin_folder_path(sc_model_1, requiered_product,
                                                                           runset_id=runset_id)
    hist_folder_path_2 = FolderDefinition.get_intermediate_bin_folder_path(sc_model_2, requiered_product,
                                                                           runset_id=runset_id)

    # define the closes timestamp available
    timestamp00_1 = timestamp00_1 if timestamp00_1 == the_timestamp else FolderDefinition.retrive_closest_timestamp_in_hist_folder(
        hist_folder_path_1, the_timestamp, accept_range=flextime)
    timestamp00_2 = timestamp00_2 if timestamp00_2 == the_timestamp else FolderDefinition.retrive_closest_timestamp_in_hist_folder(
        hist_folder_path_2, the_timestamp, accept_range=flextime)

    # basic checks 1
    if timestamp00_1 is None:
        Debug.dl("reprgen_preacchil06hh_cmpr: not a single bin file for model {0}.".format(sc_model_1), 1, debug_lvl)
        return False
    if timestamp00_2 is None:
        Debug.dl("reprgen_preacchil06hh_cmpr: not a single bin file for model {0}.".format(sc_model_2), 1, debug_lvl)
        return False

    # determine timestamps at time +6 hour
    timestamp06_1 = determine_timestamp06_for_model(sc_model_1, timestamp00_1, requiered_product, runset_id=runset_id,
                                                    debug_lvl=debug_lvl)
    timestamp06_2 = determine_timestamp06_for_model(sc_model_2, timestamp00_2, requiered_product, runset_id=runset_id,
                                                    debug_lvl=debug_lvl)

    # determine all file paths
    timestamp_00_1_filepath = os.path.join(hist_folder_path_1,
                                           BinDefinition.define_file_name(timestamp00_1, requiered_product))
    timestamp_06_1_filepath = os.path.join(hist_folder_path_1,
                                           BinDefinition.define_file_name(timestamp06_1, requiered_product))
    timestamp_00_2_filepath = os.path.join(hist_folder_path_2,
                                           BinDefinition.define_file_name(timestamp00_2, requiered_product))
    timestamp_06_2_filepath = os.path.join(hist_folder_path_2,
                                           BinDefinition.define_file_name(timestamp06_2, requiered_product))

    # basich check 2
    if not os.path.exists(timestamp_00_1_filepath):
        Debug.dl("reprgen_preacchil06hh_cmpr: file 00h not found ({0}).".format(timestamp_00_1_filepath), 1, debug_lvl)
        return False
    if not os.path.exists(timestamp_06_1_filepath):
        Debug.dl("reprgen_preacchil06hh_cmpr: file 06h not found ({0} -> '{1}').".format(timestamp00_1,
                                                                                    timestamp_06_1_filepath),
            1, debug_lvl)
        return False
    if not os.path.exists(timestamp_00_2_filepath):
        Debug.dl("reprgen_preacchil06hh_cmpr: file 00h not found ({0}).".format(timestamp_00_2_filepath), 1, debug_lvl)
        return False
    if not os.path.exists(timestamp_06_2_filepath):
        Debug.dl("reprgen_preacchil06hh_cmpr: file 06h not found ({0} -> '{1}').".format(timestamp00_1,
                                                                                    timestamp_06_2_filepath),
            1, debug_lvl)
        return False

    # read data files
    time00_data_1 = np.load(timestamp_00_1_filepath)
    time06_data_1 = np.load(timestamp_06_1_filepath)
    time00_data_2 = np.load(timestamp_00_2_filepath)
    time06_data_2 = np.load(timestamp_06_2_filepath)

    # read mask
    aod = AncillaryOnDemand()
    mask = aod.get_linkid_hills_mask()

    the_timestamp00 = GeneralUtils.round_timestamp_hour(the_timestamp)

    # plot the data
    delta_data_1 = time00_data_1 - time06_data_1
    delta_data_2 = time00_data_2 - time06_data_2
    delta_data = delta_data_1 - delta_data_2

    bin_matrix = build_data_matrix(mask, delta_data, debug_lvl=debug_lvl)
    save_image_file(sc_comparison_id, "preacchil06hh", bin_matrix, the_timestamp00, runset_id=runset_id,
                    debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("reprgen_preacchil06hh_cmpr: generate_representation({0}) function took {1} seconds ".format(sc_comparison_id,
                                                                                                          d_time),
             1, debug_lvl)

    return


def determine_timestamp00_for_model(sc_model_id, timestamp, flextime, requiered_product, runset_id, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp:
    :param flextime:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

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
        Debug.dl("reprgen_preacchil06hh_cmpr: not a single sl bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return False

    return the_timestamp


def determine_timestamp06_for_model(sc_model_id, timestamp00, requiered_product, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp00:
    :param requiered_product:
    :param debug_lvl:
    :return:
    """

    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                         runset_id=runset_id)

    the_timestamp00rounded = GeneralUtils.round_timestamp_hour(timestamp00)
    the_timestamp06reference = the_timestamp00rounded - (6 * 60 * 60)
    the_timestamp06 = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path,
                                                                                the_timestamp06reference,
                                                                                accept_range=(39 * 60))

    return the_timestamp06

# ####################################################### CALL ####################################################### #

generate_representation(comparison_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
