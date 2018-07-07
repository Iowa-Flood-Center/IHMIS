from def_system import FolderDefinition, BinDefinition, Debug
import numpy as np
import os


def determine_timestamp_for_model(sc_model_id, timestamp, flextime, runset_id=None, debug_lvl=0):
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
        Debug.dl("reprgen_cmpr_lib: Not a single sl bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return False

    return the_timestamp


def get_data_vector(sc_model_id, sc_product_id, timestamp, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param sc_product_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    # establish filename and path
    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, sc_product_id,
                                                                         runset_id=runset_id)
    filepath = os.path.join(hist_folder_path, BinDefinition.define_file_name(timestamp, sc_product_id))

    # read file if possible
    if os.path.exists(filepath):
        Debug.dl("reprgen_soimoi20ih_cmpr: Reading '{0}'.".format(filepath), 1, debug_lvl)
        return np.load(filepath)
    else:
        Debug.dl("reprgen_soimoi20ih_cmpr: File not found: '{0}'.".format(filepath), 1, debug_lvl)
        return False
