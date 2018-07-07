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

model_id_arg = ReprGenInterface.get_model_id_hist(sys.argv)
timestamp_min_arg = ReprGenInterface.get_min_timestamp_hist_opt(sys.argv)
timestamp_max_arg = ReprGenInterface.get_max_timestamp_hist_opt(sys.argv)
flextime_arg = ReprGenInterface.get_flextime(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def generate_representation(sc_model_id, timestamp_min, timestamp_max, flextime=None, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp_min:
    :param timestamp_max:
    :param flextime:
    :param debug_lvl:
    :return:
    """

    requiered_product = 'idv_r'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                         runset_id=runset_id)

    # establish min timestamp
    if timestamp_min is not None:
        if flextime is None:
            the_timestamp_min = timestamp_min
        else:
            the_timestamp_min = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path,
                                                                                          timestamp_min,
                                                                                          accept_range=flextime)
    else:
        the_timestamp_min = FolderDefinition.retrive_earliest_timestamp_in_hist_folder(hist_folder_path)

    # establish max timestamp
    if timestamp_max is not None:
        if flextime is None:
            the_timestamp_max = timestamp_max
        else:
            the_timestamp_max = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path,
                                                                                          timestamp_max,
                                                                                          accept_range=flextime)
    else:
        the_timestamp_max = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    # basic check 1
    if None in (the_timestamp_min, the_timestamp_max):
        Debug.dl("reprgen_runacchilh_arbitrary: unable to define a maximum or a minimum timestamp for model...", 1,
                 debug_lvl)
        Debug.dl("                      ...{0}.{1}: ({2}, {3})".format(runset_id, sc_model_id, the_timestamp_min,
                                                                       the_timestamp_max), 1, debug_lvl)
        return False

    # round timestamps
    timestamp_max_filepath = os.path.join(hist_folder_path,
                                          BinDefinition.define_file_name(the_timestamp_max, requiered_product))
    timestamp_min_filepath = os.path.join(hist_folder_path,
                                          BinDefinition.define_file_name(the_timestamp_min, requiered_product))

    # round timestamps
    the_timestamp_max_rounded = GeneralUtils.round_timestamp_hour(the_timestamp_max)
    the_timestamp_min_rounded = GeneralUtils.round_timestamp_hour(the_timestamp_min)

    # basic check 2
    if not os.path.exists(timestamp_min_filepath):
        Debug.dl("reprgen_runacchilh_arbitrary: file 00h not found ({0}).".format(timestamp_min_filepath), 1, debug_lvl)
        return False
    if not os.path.exists(timestamp_max_filepath):
        Debug.dl("reprgen_runacchilh_arbitrary: file 24h not found ({0} -> '{1}').".format(the_timestamp_max,
                                                                                           timestamp_max_filepath),
            1, debug_lvl)
        return False

    # read data files
    timestamp_max_data = np.load(timestamp_max_filepath)
    timestamp_min_data = np.load(timestamp_min_filepath)

    Debug.dl("reprgen_runacchilh_arbitrary: Composing with timestamps {0} : {1} -> {2} : {3}).".format(the_timestamp_max,
                                                                                                       the_timestamp_max_rounded,
                                                                                                       the_timestamp_min,
                                                                                                       the_timestamp_min_rounded),
             1, debug_lvl)

    # read mask
    aod = AncillaryOnDemand()
    mask = aod.get_linkid_hills_mask()

    # plot the data
    delta_data = timestamp_max_data - timestamp_min_data

    print("Basic info: most recent data ranges from {0} to {1}.".format(np.min(timestamp_max_data),
                                                                        np.max(timestamp_max_data)))
    print("            least recent data ranges from {0} to {1}.".format(np.min(timestamp_min_data),
                                                                         np.max(timestamp_min_data)))
    print("            differences range from {0} to {1}.".format(np.min(delta_data), np.max(delta_data)))


    '''
    linkid = 434514
    print("Link {0}: {1}".format(linkid, time00_data[linkid]))
    print("Link {0}: {1}".format(linkid, time24_data[linkid]))
    print("Linka {0}: {1}".format(linkid, delta_data[linkid]))
    for i, d in enumerate(delta_data):
        if d > 0:
            print("Link {0}: {1}".format(i, delta_data[i]))
            break
    '''

    bin_matrix = build_data_matrix(mask, delta_data, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, "runacchilharbitrary", bin_matrix, the_timestamp_max, runset_id=runset_id,
                    debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("reprgen_runacchilh_arbitrary: generate_representation({0}) function took {1} seconds ".format(sc_model_id,
                                                                                                            d_time),
             1, debug_lvl)

    return

# ####################################################### CALL ####################################################### #

generate_representation(model_id_arg, timestamp_min_arg, timestamp_max_arg, flextime=flextime_arg,
                        runset_id=runset_id_arg, debug_lvl=debug_level_arg)
