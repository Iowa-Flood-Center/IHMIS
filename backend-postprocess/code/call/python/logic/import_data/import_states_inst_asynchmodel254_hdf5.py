import numpy as np
import argparse
import time
import h5py
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.FolderDefinition import FolderDefinition
from libs.SettingsRealtime import SettingsRealtime
from libs.LinksDefinition import LinksDefinition
from libs.MetaFileManager import MetaFileManager
from libs.BinDefinition import BinDefinition
from libs.GeneralUtils import GeneralUtils
from libs.Debug import Debug

debug_level_arg = 10

# ####################################### ARGS ####################################### #

# define arguments
parser = argparse.ArgumentParser(description='Import state files.')
parser.add_argument('-model_sing_id', metavar='MODEL_SING_ID', type=str, required=True,
                    help="a sc_model_sing id or 'all' for all available models")
parser.add_argument('-runset_id', metavar='RUNSET_ID', type=str, required=True,
                    help="a sc_runset id or 'all' for all available models")
parser.add_argument('-t', metavar='TIMESTAMP', type=int, required=False,
                    help="a timestamp")
parser.add_argument('-flex', metavar='FLEX_TIME', type=int, required=False,
                    help="TODO")

# read arguments
args = parser.parse_args()


# ####################################### DEFS ####################################### #

def update_local_bins_from_hdf5(model_id, runset_id, timestamp=None, flextime=None,
                                debug_lvl=0):
    """
    Reads the data from hdf5 files and generates binary files for current states
    :param model_id:
    :param timestamp: If None, retrieves the most recent available
    :param flextime:
    :param debug_lvl:
    :return: None. Changes are perform at file system level
    """

    # basic check
    if model_id is None:
        Debug.dl("import_states_inst_asynchmodel254_hdf5: At least a model id must be provided.", 1, debug_lvl)
        return

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # define model's output folder
    model_output_folder = FolderDefinition.get_model_output_hdf5_folder(model_id)
    if model_output_folder is None:
        Debug.dl("import_states_inst_asynchmodel254_hdf5: No output folder definition found for model '{0}'.".format(model_id), 1,
                 debug_lvl)
        return None
    Debug.dl("import_states_inst_asynchmodel254_hdf5: Output folder for model '{0}': '{1}'".format(model_id,
                                                                                                   model_output_folder),
             1, debug_lvl)

    # get reference timestamp
    if timestamp is None:
        higher_timestamp = get_current_timestamp_from_hdf5_files(model_output_folder, model_id, debug_lvl=debug_lvl)
        if higher_timestamp is None:
            Debug.dl("import_states_inst_asynchmodel254_hdf5: Unable to retrieve a timestamp for {0}.{1}".format(
                runset_id, model_id), 1, debug_lvl)
            return
        the_timestamp_rounded = GeneralUtils.round_timestamp_hour(higher_timestamp)
        filename_prefix = SettingsRealtime.get("input_file_prefix", sc_model_id=model_id)
        cur_timestamp = FolderDefinition.retrive_closest_timestamp_in_dist_folder(model_output_folder,
                                                                                  the_timestamp_rounded,
                                                                                  accept_range=(30 * 60),
                                                                                  filename_prefix=filename_prefix,
                                                                                  debug_lvl=debug_lvl)
        Debug.dl("import_states_inst_asynchmodel254_hdf5: Current timestamp at {0} is {1}. Rounded to {2} (searched for {3}).".format(
            model_output_folder, higher_timestamp, cur_timestamp, the_timestamp_rounded),
                 2, debug_lvl)
        can_round = True
    else:
        the_timestamp_rounded = GeneralUtils.round_timestamp_hour(timestamp)
        if flextime is None:
            cur_timestamp = timestamp
        else:
            filename_prefix = SettingsRealtime.get("input_file_prefix", sc_model_id=model_id)
            cur_timestamp = FolderDefinition.retrive_closest_timestamp_in_dist_folder(model_output_folder, timestamp,
                                                                                      accept_range=flextime,
                                                                                      filename_prefix=filename_prefix,
                                                                                      debug_lvl=debug_lvl)

        can_round = False

    # start counting time for debug
    start_read_time = time.time() if debug_lvl > 0 else None

    # assert file is ok
    hdf5_file_path = FolderDefinition.get_model_output_hdf5_file_path(model_id, cur_timestamp)
    if not os.path.exists(hdf5_file_path) and can_round:
        Debug.dl("import_states_inst_asynchmodel254_hdf5: But file '{0}' does not exist.".format(hdf5_file_path), 2,
                 debug_lvl)
        cur_timestamp = the_timestamp_rounded - 3600
        Debug.dl("import_states_inst_asynchmodel254_hdf5: Re-rounded to {0}".format(cur_timestamp), 2, debug_lvl)
        hdf5_file_path = FolderDefinition.get_model_output_hdf5_file_path(model_id, cur_timestamp)

    # read file
    cur_file_data = get_data_from_hdf5_file(hdf5_file_path, debug_lvl=debug_lvl)

    # read file
    # cur_file_data = get_data_from_hdf5_file(None, debug_lvl=debug_lvl)

    # basic check
    if cur_file_data is None:
        Debug.dl("import_states_inst_asynchmodel254_hdf5: Failed to retrieve data from '{0}'".format(hdf5_file_path), 1,
                 debug_lvl)
        return
    elif len(cur_file_data) == 0:
        Debug.dl("import_states_inst_asynchmodel254_hdf5: File '{0}' is empty.".format(hdf5_file_path), 1, debug_lvl)
        return
    elif (len(cur_file_data) == 2) and (cur_file_data[0] is None) and (cur_file_data[1] is None):
        Debug.dl("import_states_inst_asynchmodel254_hdf5: Skipping file creation.", 1, debug_lvl)
        return

    # debug info
    d_time = time.time()-start_read_time
    Debug.dl("import_states_inst_asynchmodel254_hdf5: Reading HDF5 file for {0} took {1} seconds.".format(model_id,
                                                                                                          d_time),
             1, debug_lvl)

    # create empty receiving vectors
    max_link_id = LinksDefinition.get_max_link_id()
    map_vect_iq = np.zeros(max_link_id + 1, dtype=np.float)
    map_vect_isp = np.zeros(max_link_id + 1, dtype=np.float)
    map_vect_isl = np.zeros(max_link_id + 1, dtype=np.float)
    map_vect_iss = np.zeros(max_link_id + 1, dtype=np.float)
    map_vect_ivp = np.zeros(max_link_id + 1, dtype=np.float)
    map_vect_ivr = np.zeros(max_link_id + 1, dtype=np.float)

    # fill receiving vectors
    for cur_i, cur_item in enumerate(cur_file_data):
        if cur_item is None:
            Debug.dl("import_states_inst_asynchmodel254_hdf5: None item {0}.".format(cur_i), 1, debug_lvl)
            continue
        cur_linkid = cur_item[0]
        map_vect_iq[cur_linkid] = cur_item[1]
        map_vect_isp[cur_linkid] = cur_item[2]
        map_vect_isl[cur_linkid] = cur_item[3]
        map_vect_iss[cur_linkid] = cur_item[4]
        map_vect_ivp[cur_linkid] = cur_item[5]
        map_vect_ivr[cur_linkid] = cur_item[6]

    # get all products to be saved for specific model
    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info()
    svd_prods = meta_mng.get_all_products_of_scmodel(model_id)

    # create folders if necessary
    FolderDefinition.create_folders_for_model_if_necessary(model_id, svd_prods, runset_id)

    # save all related products
    save_binary_file(model_id, runset_id, 'idq', map_vect_iq, cur_timestamp, saved_prods=svd_prods,
                     debug_lvl=debug_lvl)
    save_binary_file(model_id, runset_id, 'ids_p', map_vect_isp, cur_timestamp, saved_prods=svd_prods,
                     debug_lvl=debug_lvl)
    save_binary_file(model_id, runset_id, 'ids_l', map_vect_isl, cur_timestamp, saved_prods=svd_prods,
                     debug_lvl=debug_lvl)
    save_binary_file(model_id, runset_id, 'ids_s', map_vect_iss, cur_timestamp, saved_prods=svd_prods,
                     debug_lvl=debug_lvl)
    save_binary_file(model_id, runset_id, 'idv_p', map_vect_ivp, cur_timestamp, saved_prods=svd_prods,
                     debug_lvl=debug_lvl)
    save_binary_file(model_id, runset_id, 'idv_r', map_vect_ivr, cur_timestamp, saved_prods=svd_prods,
                     debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("import_states_inst_asynchmodel254_hdf5: update_local_bins_from_hdf5({0}) function took {1} seconds ".format(
        model_id, d_time), 1, debug_lvl)

    return


def get_current_timestamp_from_hdf5_files(output_folder_path, sc_model_id, debug_lvl=0):
    """

    :param output_folder_path:
    :param debug_lvl:
    :param sc_model_id:
    :return:
    """

    # basic check
    if output_folder_path is None:
        return None
    elif not os.path.exists(output_folder_path):
        Debug.dl("import_states_inst_asynchmodel254_hdf5: Folder {0} does not exist.".format(output_folder_path), 1,
                 debug_lvl)
        return None

    all_file_names = os.listdir(output_folder_path)

    # basic check - must have at least one file
    if len(all_file_names) == 0:
        Debug.dl("import_states_inst_asynchmodel254_hdf5: No file found at {0}".format(output_folder_path), 1,
                 debug_lvl)
        return None

    all_file_names.sort(reverse=True)

    for cur_file_name in all_file_names:
        cur_timestamp = retrieve_timestamp_from_hdf5_state_filename(cur_file_name, sc_model_id, debug_lvl=debug_lvl)
        if cur_timestamp is not None:
            return cur_timestamp

    return None


def retrieve_timestamp_from_hdf5_state_filename(hdf5_filename, sc_model_id, debug_lvl=0):
    """

    :param hdf5_filename:
    :param sc_model_id:
    :param debug_lvl:
    :return:
    """

    # basic check
    if hdf5_filename is None:
        return None

    # process filename
    try:
        filename_prefix = SettingsRealtime.get("input_file_prefix", sc_model_id=sc_model_id)
        return int(hdf5_filename.replace(filename_prefix, "").replace(".h5", ""))
    except ValueError:
        Debug.dl("import_states_inst_asynchmodel254_hdf5: Wrong HDF5 file name '{0}'.".format(hdf5_filename),
                 debug_lvl, 1)
        return None


def get_data_from_hdf5_file(hdf5_file_path, debug_lvl=0):
    """
    Read HDF5 file
    :param hdf5_file_path:
    :param debug_lvl:
    :return: Array of linkids and array parameters matrix
    """

    # basic check
    if (hdf5_file_path is None) or (not os.path.exists(hdf5_file_path)):
        Debug.dl("import_states_inst_asynchmodel254_hdf5: File '{0}' does not exist.".format(hdf5_file_path),
                 1, debug_lvl)
        return None, None

    # read file content
    Debug.dl("import_states_inst_asynchmodel254_hdf5: Reading from '{0}'.".format(hdf5_file_path), 1, debug_lvl)
    with h5py.File(hdf5_file_path, 'r') as hdf_file:
        hdf_data = np.array(hdf_file.get('snapshot'))

    return hdf_data


def save_binary_file(model_id, sc_runset_id, sc_product_id, value_matrix, timestamp, saved_prods=None, debug_lvl=0):
    """

    :param model_id:
    :param sc_product_id:
    :param sc_runset_id:
    :param value_matrix:
    :param timestamp:
    :param saved_prods: List of sc_product IDs that should be saved - serves as possible constraint. If None, save it
    :param debug_lvl:
    :return:
    """

    if (saved_prods is not None) and (sc_product_id not in saved_prods):
        Debug.dl("import_states_inst_asynchmodel254_hdf5: sc_product {0} not among {1}".format(sc_product_id, saved_prods), 3,
                 debug_lvl)
        return

    # create folder if necessary
    bin_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id, sc_product_id, sc_runset_id)
    if not os.path.exists(bin_folder_path):
        os.makedirs(bin_folder_path)

    # establish fll file path
    bin_file_name = BinDefinition.define_file_name(timestamp, sc_product_id)
    bin_file_path = os.path.join(bin_folder_path, bin_file_name)

    # create destination folder if necessary
    if not os.path.exists(bin_folder_path):
        os.makedirs(bin_folder_path)

    # just a debug
    Debug.dl("import_states_inst_asynchmodel254_hdf5: Saving {0} object as {1}".format(bin_file_path, type(value_matrix)),
             2, debug_lvl)

    # saving file
    np.save(bin_file_path, value_matrix)

    # just a debug
    Debug.dl("import_states_inst_asynchmodel254_hdf5: Binary file saved: '{0}'".format(bin_file_path), 1, debug_lvl)

    return


# ####################################### CALL ####################################### #

update_local_bins_from_hdf5(args.model_sing_id, args.runset_id,
                            args.t, flextime=args.flex,
                            debug_lvl=debug_level_arg)
