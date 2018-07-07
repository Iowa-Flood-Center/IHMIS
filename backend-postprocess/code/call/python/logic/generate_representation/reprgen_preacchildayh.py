from def_system import FolderDefinition, BinDefinition, LinksDefinition, ImageDefinition, Debug
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

model_id_arg = ReprGenInterface.get_model_id(sys.argv)
timestamp_arg = ReprGenInterface.get_timestamp_opt(sys.argv)
flextime_arg = ReprGenInterface.get_flextime(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def generate_representation(sc_model_id, timestamp, flextime=None, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp:
    :param flextime:
    :param debug_lvl:
    :return:
    """

    requiered_product = 'idv_p'
    generated_representation = 'preacchildayh'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                         runset_id=runset_id)

    # establish the current timestamp
    if timestamp is not None:
        if flextime is None:
            the_timestamp = timestamp
        else:
            the_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path, timestamp,
                                                                                      accept_range=flextime)
    else:
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    # basic checks 1
    if the_timestamp is None:
        Debug.dl("reprgen_preacchildayh: not a single bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return False

    # round current timestamp
    the_timestamp_rounded = GeneralUtils.floor_timestamp_day(the_timestamp)
    the_timestamp00 = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path, the_timestamp_rounded,
                                                                                accept_range=flextime)

    # check if ir really must be created
    img_file_path = ImageDefinition.define_historical_file_name(the_timestamp00, generated_representation)
    if os.path.exists(img_file_path):
        Debug.dl("reprgen_preacchildayh: file already exists: {0}.".format(img_file_path), 1, debug_lvl)
        return False

    # define previous comparison day
    the_timestamp24reference = the_timestamp_rounded - (24 * 60 * 60)
    the_timestamp24 = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path,
                                                                                the_timestamp24reference,
                                                                                accept_range=(39*60),
                                                                                debug_lvl=debug_lvl)

    timestamp_00_filepath = os.path.join(hist_folder_path,
                                         BinDefinition.define_file_name(the_timestamp00, requiered_product))
    timestamp_24_filepath = os.path.join(hist_folder_path,
                                         BinDefinition.define_file_name(the_timestamp24, requiered_product))

    # basich check 2
    if not os.path.exists(timestamp_00_filepath):
        Debug.dl("reprgen_preacchildayh: file 00h not found ({0}).".format(timestamp_00_filepath), 1, debug_lvl)
        return False
    if not os.path.exists(timestamp_24_filepath):
        Debug.dl("reprgen_preacchildayh: file 24h not found ({0} -> '{1}').".format(the_timestamp00,
                                                                                    timestamp_24_filepath),
            1, debug_lvl)
        return False

    # read data files
    time00_data = np.load(timestamp_00_filepath)
    time24_data = np.load(timestamp_24_filepath)

    Debug.dl("reprgen_preacchildayh: Composing with timestamps {0} : {1} -> {2} : {3}).".format(the_timestamp00,
                                                                                                the_timestamp_rounded,
                                                                                                the_timestamp24reference,
                                                                                                the_timestamp24),
             1, debug_lvl)

    # read mask
    aod = AncillaryOnDemand()
    mask = aod.get_linkid_hills_mask()

    # plot the data
    delta_data = time00_data - time24_data

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
    save_image_file(sc_model_id, generated_representation, bin_matrix, the_timestamp00, runset_id=runset_id,
                    debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("reprgen_preacchildayh: generate_representation({0}) function took {1} seconds ".format(sc_model_id,
                                                                                                     d_time),
             1, debug_lvl)

    return True

# ####################################################### CALL ####################################################### #

generate_representation(model_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
