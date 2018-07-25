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

    requiered_product = 'ids_l'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

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

    filepath = os.path.join(hist_folder_path, BinDefinition.define_file_name(the_timestamp, requiered_product))

    # basich check 2
    if not os.path.exists(filepath):
        Debug.dl("reprgen_soimoi20ih: sl file not found ({0}).".format(filepath), 1, debug_lvl)
        return False

    # read data files
    the_data = np.load(filepath)

    # read mask
    aod = AncillaryOnDemand()
    mask = aod.get_linkid_hills_mask()

    # plot the data
    the_data *= 10
    the_data[0] = -1
    bin_matrix = build_data_matrix(mask, the_data, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, 'soimoi20ih', bin_matrix, the_timestamp, runset_id=runset_id, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time() - start_time
    Debug.dl("reprgen_soimoi20ih: generate_representation({0}) function took {1} seconds ".format(sc_model_id, d_time),
             1, debug_lvl)

    return


# ####################################################### CALL ####################################################### #

generate_representation(model_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
