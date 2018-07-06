import numpy as np
import shutil
import pickle
import time
import h5py
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.RealtimeFilesMethods import RealtimeFilesMethods
from libs.FolderDefinition import FolderDefinition
from libs.ImportInterface import ImportInterface
from libs.BinDefinition import BinDefinition
from libs.BinaryLibrary import BinaryLibrary
from libs.H5FileReader import H5FileReader
from libs.Debug import Debug

debug_level_arg = 3

# ####################################################### ARGS ####################################################### #

model_id_arg = ImportInterface.get_model_id(sys.argv)
timestamp_arg = ImportInterface.get_timestamp(sys.argv)
runset_id_arg = ImportInterface.get_runset_id(sys.argv)

print("Model: {0}.{1}".format(runset_id_arg, model_id_arg))

# ####################################################### DEFS ####################################################### #


def update_local_bins_from_database(model_id, runset_id, timestamp=None, debug_lvl=0):
    """
    Reads the data from database and generates binary files for given hydro-forecasts
    :param model_id:
    :param runset_id:
    :param timestamp: If None, retrieves the most recent hydro-forecasts available
    :param debug_lvl:
    :return: None. Changes are perform at file system level
    """

    # basic check
    if model_id is None:
        Debug.dl("import_discharge_forecast_asynchmodel_hdf5: At least a model id must be provided.", 1, debug_lvl)
        return

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # define file name
    h5_folder_path = RealtimeFilesMethods.get_folder_with_h5_files(model_id, runset_id)
    h5_file_prefix = RealtimeFilesMethods.get_h5_file_name_prefix(model_id, runset_id)

    # define timestamp and basic check
    if timestamp is None:
        the_timestamp = RealtimeFilesMethods.get_current_timestamp_from_hdf5_files(h5_folder_path, h5_file_prefix,
                                                                                   debug_lvl=debug_lvl)
    else:
        the_timestamp = timestamp
    if the_timestamp is None:
        Debug.dl("import_discharge_forecast_asynchmodel_hdf5: Unable to define a timestamp for {0}.{1}.".format(runset_id, model_id),
                 1, debug_lvl)
        Debug.dl("                               (folder '{0}')".format(h5_folder_path), 1, debug_lvl)
        return

    # define file path and try to read it
    hdf5_file_path = os.path.join(h5_folder_path, "{0}{1}.h5".format(h5_file_prefix, the_timestamp))

    '''

    Debug.dl("import_discharge_forecast_asynchmodel_hdf5: Reading file '{0}'.".format(hdf5_file_path), 1, debug_lvl)
    h5_file_data = get_data_from_hdf5_file(hdf5_file_path, debug_lvl=debug_lvl)
    if h5_file_data[0] is None:
        Debug.dl("import_discharge_forecast_asynchmodel_hdf5: Unable to retrieve hydroforecast for {0} at {1}.".format(
            model_id, the_timestamp), 1, debug_lvl)
        return None

    # process file data
    min_timestamp = None
    count_prints = 0
    max_prints = 10
    ret_dictionary = {}
    last_linkid = h5_file_data[0][0]
    cur_linkid_timeseries = []
    for cur_row in h5_file_data:

        cur_linkid = cur_row[0]
        cur_timestamp = int(the_timestamp + (cur_row[1] * 60))
        cur_discharge = cur_row[2]

        if cur_linkid != last_linkid:
            ret_dictionary[last_linkid] = cur_linkid_timeseries
            cur_linkid_timeseries = []
        cur_linkid_timeseries.append([cur_timestamp, cur_discharge])

        # check timestamp if minimum
        if (min_timestamp is None) or (cur_timestamp < min_timestamp):
            min_timestamp = cur_timestamp

        # debug poor
        if count_prints < max_prints:
            count_prints += 1

        last_linkid = cur_linkid
        if len(cur_linkid_timeseries) > 0:
            ret_dictionary[last_linkid] = cur_linkid_timeseries

    # get reference timestamp and save binary file
    cur_timestamp = min_timestamp if timestamp is None else timestamp
    save_binary_file(model_id, runset_id, cur_timestamp, ret_dictionary, debug_lvl=debug_lvl)

    '''

    # replace above by the following
    copy_h5_file(hdf5_file_path, runset_id, model_id, "fq", the_timestamp, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("import_discharge_forecast_asynchmodel_hdf5: "
             "update_local_bins_from_database({0}) function took {1} seconds.".format(model_id, d_time), 1, debug_lvl)

    return


def get_data_from_hdf5_file(hdf5_file_path, debug_lvl=0):
    """

    :param hdf5_file_path:
    :param debug_lvl:
    :return:
    """

    # basic check - file must exist
    if (hdf5_file_path is None) or (not os.path.exists(hdf5_file_path)):
        Debug.dl("import_discharge_forecast_asynchmodel_hdf5: File '{0}' does not exist.".format(hdf5_file_path), 1, debug_lvl)
        return None, None

    # import data into matrix
    with h5py.File(hdf5_file_path, 'r') as hdf_file:
        hdf_data = np.array(hdf_file.get('outputs'))

    return hdf_data


def save_binary_file(model_id, runset_id, timestamp, hydroforecast_dictionary, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param timestamp:
    :param hydroforecast_dictionary:
    :param debug_lvl:
    :return:
    """

    product_id = "fq"

    # basic check
    if hydroforecast_dictionary is None:
        return

    bin_file_path = FolderDefinition.get_intermediate_bin_file_path(model_id, product_id, timestamp,
                                                                    runset_id=runset_id)

    # create folder if necessary
    bin_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id, product_id, runset_id=runset_id)
    if not os.path.exists(bin_folder_path):
        os.makedirs(bin_folder_path)

    Debug.dl("import_discharge_forecast_asynchmodel_hdf5: Saving '{0}' file.".format(bin_file_path), 2, debug_lvl)
    with open(bin_file_path, "wb") as w_file:
        pickle.dump(hydroforecast_dictionary, w_file)

    Debug.dl("import_discharge_forecast_asynchmodel_hdf5: Binary file saved: '{0}'.".format(bin_file_path), 1, debug_lvl)

    return


def copy_h5_file(h5_file_path, sc_runset_id, sc_model_id, sc_product_id, timestamp, debug_lvl=0):
    """

    :param h5_file_path:
    :param sc_runset_id:
    :param sc_model_id:
    :param sc_product_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    dest_file_path = BinaryLibrary.get_binary_file_path(sc_runset_id, sc_model_id, sc_product_id, timestamp,
                                                        debug_lvl=debug_lvl)

    # create folder structure if necessary
    folder_path = os.path.dirname(dest_file_path)
    if not os.path.exists(folder_path):
        Debug.dl("import_discharge_forecast_asynchmodel_hdf5: Creating folder '{0}'.".format(folder_path), 1, debug_lvl)
        os.makedirs(folder_path)

    shutil.copy(h5_file_path, dest_file_path)
    H5FileReader.create_linkid_index_asynch_hydrograph_h5(dest_file_path, debug_lvl=debug_lvl)

    Debug.dl("import_discharge_forecast_asynchmodel_hdf5: Copied file to '{0}'.".format(dest_file_path), 1, debug_lvl)


def import_hdf_as_sparce_snapshots(h5_file_path, sc_runset_id, sc_model_id, sc_product_id, debug_lvl=0):
    """

    :param h5_file_path:
    :param sc_runset_id:
    :param sc_model_id:
    :param sc_product_id:
    :param debug_lvl:
    :return:
    """
    return None


# ####################################################### CALL ####################################################### #

update_local_bins_from_database(model_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
