import shutil
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.ReprCombGenInterface import ReprCombGenInterface
from libs.FolderDefinition import FolderDefinition
from libs.Debug import Debug

debug_level_arg = 10
previous_max_time_arg = 10.1  # for how many days historical evaluation data must be hold
clean_if_no_replacement = False

# ####################################################### ARGS ####################################################### #

modelcomb_id_arg = ReprCombGenInterface.get_modelcomb_id(sys.argv)
reprcomb_id_arg = ReprCombGenInterface.get_reprcomb_id(sys.argv)
timestamp_arg = ReprCombGenInterface.get_timestamp(sys.argv)
runset_id_arg = ReprCombGenInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def clean_historical_reprcomp(modelcomb_id, reprcomp_id, runset_id, timestamp, previous_max_time, debug_lvl=0):
    """

    :param modelcomb_id:
    :param reprcomp_id:
    :param runset_id:
    :param timestamp:
    :param previous_max_time:
    :param debug_lvl:
    :return:
    """

    count_del_files = 0

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # establishing folders (root and frames)
    hist_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id, represcomb_id=reprcomp_id,
                                                                            model_id=modelcomb_id)
    all_files = os.listdir(hist_folder_path)
    all_folders = []
    for cur_file in all_files:
        cur_file_path = os.path.join(hist_folder_path, cur_file)
        if os.path.isdir(cur_file_path):
            all_subfiles = os.listdir(cur_file_path)
            for cur_subfile in all_subfiles:
                cur_folder_path = os.path.join(cur_file_path, cur_subfile)
                if os.path.isdir(cur_folder_path):
                    all_folders.append(cur_folder_path)

    for cur_folder in all_folders:

        # define timestamps
        if timestamp is None:
            max_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(cur_folder)
        else:
            max_timestamp = timestamp
        if max_timestamp is None:
            Debug.dl("rpcbcln_generic_sparse: Failed to get a max timestamp from '{0}'.".format(cur_folder), 2,
                     debug_lvl)
            continue
        min_timestamp = int(max_timestamp - (previous_max_time * 24 * 60 * 60))

        # list all files, identifying the higher timestamp for each link id
        hist_file_names = os.listdir(cur_folder)
        count_del_files = 0
        for cur_hist_filename in hist_file_names:
            cur_splitted_file_basename = os.path.splitext(cur_hist_filename)[0].split("_")
            cur_release_timestamp = int(cur_splitted_file_basename[0])

            if min_timestamp <= cur_release_timestamp <= max_timestamp:
                continue
            else:
                cur_file_path = os.path.join(cur_folder, cur_hist_filename)
                Debug.dl("rpcbcln_generic_sparse: Deleting file {0} (references: {1} and {2}).".format(cur_file_path,
                                                                                                       min_timestamp,
                                                                                                       max_timestamp),
                         2, debug_lvl)
                count_del_files += 1
                os.unlink(os.path.join(cur_folder, cur_hist_filename))
        Debug.dl("rpcbcln_generic_sparse: Deleted {0} files from '{1}'.".format(count_del_files, cur_folder), 2,
                 debug_lvl)

    # debug info
    d_time = time.time()-start_time

    Debug.dl("rpcbcln_generic_sparse: Deleted {0} files in {1} seconds".format(count_del_files, d_time), 1, debug_lvl)

# ####################################################### CALL ####################################################### #

clean_historical_reprcomp(modelcomb_id_arg, reprcomb_id_arg, runset_id_arg, timestamp_arg, previous_max_time_arg,
                          debug_lvl=debug_level_arg)
