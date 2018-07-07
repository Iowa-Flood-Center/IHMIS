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
from libs.MetaFileManager import MetaFileManager
from libs.BinDefinition import BinDefinition
from libs.GeneralUtils import GeneralUtils
from libs.Debug import Debug


debug_level_arg = 1

# ####################################################### ARGS ####################################################### #

model_id_arg = ReprGenInterface.get_model_id(sys.argv)
timestamp_arg = ReprGenInterface.get_timestamp_opt(sys.argv)
flextime_arg = ReprGenInterface.get_flextime(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def generate_representation(sc_model_id, timestamp, flextime=None, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp:
    :param flextime: Numeric value with acceptable ranges of values from timestamp. If None, must be exact timestamp
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    requiered_products_1 = ['ids_l', 'ids_s']  # when top layer and sub-surface are present
    requiered_products_2 = ['ids_t']           # when only total sub-surface is present

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # load meta information
    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
    all_products = meta_mng.get_all_products_of_scmodel(sc_model_id, debug_lvl=debug_lvl)

    # TODO - decide which method will be used
    if set(requiered_products_1).issubset(all_products):
        the_data, the_timestamp = calculate_by_1(runset_id, sc_model_id, requiered_products_1, timestamp,
                                                 flextime=flextime, debug_lvl=debug_lvl)
    elif set(requiered_products_2).issubset(all_products):
        the_data, the_timestamp = calculate_by_2(runset_id, sc_model_id, requiered_products_2, timestamp,
                                                 flextime=flextime, debug_lvl=debug_lvl)
    else:
        the_data, the_timestamp = None, None

    # basic check
    if the_data is None:
        Debug.dl("reprgen_soiwac20ih: Model {0}.{1} does not have a valid set of products.".format(runset_id,
                                                                                                   sc_model_id), 1,
                 debug_lvl)
        return

    # read mask
    aod = AncillaryOnDemand()
    mask = aod.get_linkid_hills_mask()

    # plot the data
    bin_matrix = build_data_matrix(mask, the_data, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, 'soiwac20ih', bin_matrix, the_timestamp, runset_id=runset_id, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("reprgen_soiwac20ih: generate_representation({0}) function took {1} seconds ".format(sc_model_id, d_time),
             1, debug_lvl)

    return


def calculate_by_1(sc_runset_id, sc_model_id, requiered_products, timestamp, flextime=None, debug_lvl=0):
    """

    :param sc_runset_id:
    :param sc_model_id:
    :param requiered_products:
    :param timestamp:
    :param flextime:
    :param debug_lvl:
    :return:
    """

    Debug.dl("reprgen_soiwac20ih: Get to the first case.", 1, debug_lvl)

    hist_sl_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_products[0],
                                                                            runset_id=sc_runset_id)
    hist_ss_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_products[1],
                                                                            runset_id=sc_runset_id)

    # establish the timestamp for sl
    if timestamp is not None:
        if flextime is None:
            the_timestamp_sl = timestamp
        else:
            the_timestamp_sl = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_sl_folder_path, timestamp,
                                                                                         accept_range=flextime)
    else:
        the_timestamp_sl = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_sl_folder_path)

    # establish the timestamp for ss
    if timestamp is not None:
        if flextime is None:
            the_timestamp_ss = timestamp
        else:
            the_timestamp_ss = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_ss_folder_path, timestamp,
                                                                                         accept_range=flextime)
    else:
        the_timestamp_ss = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_ss_folder_path)

    # basic checks 1
    if the_timestamp_sl is None:
        Debug.dl("reprgen_soiwac20ih: not a single sl bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return None, None
    if the_timestamp_ss is None:
        Debug.dl("reprgen_soiwac20ih: not a single ss bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return None, None

    the_timestamp = min((the_timestamp_sl, the_timestamp_ss))

    sl_filepath = os.path.join(hist_sl_folder_path, BinDefinition.define_file_name(the_timestamp,
                                                                                   requiered_products[0]))
    ss_filepath = os.path.join(hist_ss_folder_path, BinDefinition.define_file_name(the_timestamp,
                                                                                   requiered_products[1]))

    # basich check 2
    if not os.path.exists(sl_filepath):
        Debug.dl("reprgen_soiwac20ih: sl file not found ({0}).".format(sl_filepath), 1, debug_lvl)
        return None, None
    if not os.path.exists(ss_filepath):
        Debug.dl("reprgen_soiwac20ih: ss file not found ({0}).".format(ss_filepath), 1, debug_lvl)
        return None, None

    # read data files and get the values
    sl_data = np.load(sl_filepath)
    ss_data = np.load(ss_filepath)
    the_data = ss_data + sl_data

    return the_data, the_timestamp


def calculate_by_2(sc_runset_id, sc_model_id, requiered_products, timestamp, flextime=None, debug_lvl=0):
    """

    :param sc_runset_id:
    :param sc_model_id:
    :param requiered_products:
    :param timestamp:
    :param flextime:
    :param debug_lvl:
    :return:
    """

    Debug.dl("reprgen_soiwac20ih: Get to the first case.", 1, debug_lvl)

    hist_st_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_products[0],
                                                                            runset_id=sc_runset_id)

    # establish the timestamp for st
    if timestamp is not None:
        if flextime is None:
            the_timestamp = timestamp
        else:
            the_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_st_folder_path, timestamp,
                                                                                      accept_range=flextime)
    else:
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_st_folder_path)

    st_filepath = os.path.join(hist_st_folder_path, BinDefinition.define_file_name(the_timestamp,
                                                                                   requiered_products[0]))

    # basich check 2
    if not os.path.exists(st_filepath):
        Debug.dl("reprgen_soiwac20ih: st file not found ({0}).".format(st_filepath), 1, debug_lvl)
        return None, None

    # read data files and get the values
    the_data = np.load(st_filepath)

    return the_data, the_timestamp


# ####################################################### CALL ####################################################### #

generate_representation(model_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
