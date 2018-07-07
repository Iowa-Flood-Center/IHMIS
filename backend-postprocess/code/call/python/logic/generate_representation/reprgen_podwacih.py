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

    requiered_product = 'ids_p'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # load meta information
    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
    all_products = meta_mng.get_all_products_of_scmodel(sc_model_id, debug_lvl=debug_lvl)

    if requiered_product in all_products:
        the_data, the_timestamp = calculate_by_1(runset_id, sc_model_id, requiered_product, timestamp, flextime=flextime,
                                                 debug_lvl=debug_lvl)
    else:
        the_data, the_timestamp = None, None

    # basic check
    if the_data is None:
        Debug.dl("reprgen_podwacih: Model {0}.{1} does not have a valid set of products.".format(runset_id,
                                                                                                 sc_model_id), 1,
                 debug_lvl)
        return

    # read mask
    aod = AncillaryOnDemand()
    mask = aod.get_linkid_hills_mask()

    # plot the data
    bin_matrix = build_data_matrix(mask, the_data, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, 'podwacih', bin_matrix, the_timestamp, runset_id=runset_id, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("reprgen_podwacih: generate_representation({0}) function took {1} seconds ".format(sc_model_id, d_time),
             1, debug_lvl)

    return


def calculate_by_1(sc_runset_id, sc_model_id, requiered_product, timestamp, flextime=None, debug_lvl=0):
    """

    :param sc_runset_id:
    :param sc_model_id:
    :param requiered_product:
    :param timestamp:
    :param flextime:
    :param debug_lvl:
    :return:
    """

    hist_pd_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                            runset_id=sc_runset_id)

    # establish the timestamp for st
    if timestamp is not None:
        if flextime is None:
            the_timestamp = timestamp
        else:
            the_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_pd_folder_path, timestamp,
                                                                                      accept_range=flextime)
    else:
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_pd_folder_path)

    pd_filepath = os.path.join(hist_pd_folder_path, BinDefinition.define_file_name(the_timestamp, requiered_product))

    # basic check 2
    if not os.path.exists(pd_filepath):
        Debug.dl("reprgen_podwacih: pd file not found ({0}).".format(pd_filepath), 1, debug_lvl)
        return None, None

    # read data files and get the values
    the_data = np.load(pd_filepath)

    return the_data, the_timestamp

# ####################################################### CALL ####################################################### #

generate_representation(model_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
