import shutil
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.FilenameDefinition import FilenameDefinition
from libs.EvalGenInterface import EvalGenInterface
from libs.FolderDefinition import FolderDefinition
from libs.FileDefinition import FileDefinition
from libs.Debug import Debug

debug_level_arg = 10
previous_max_time_arg = 10.5  # for how many days historical evaluation data must be hold
clean_if_no_replacement = False

sc_reference_id_default = "usgsgagesdischclass"

# ####################################################### ARGS ####################################################### #

model_id_arg = EvalGenInterface.get_model_id(sys.argv)
timestamp_arg = EvalGenInterface.get_timestamp(sys.argv)
reference_id_arg = EvalGenInterface.get_reference_id(sys.argv, default_val=sc_reference_id_default)
runset_id_arg = EvalGenInterface.get_runset_id(sys.argv)


# ####################################################### DEFS ####################################################### #

def clean_historical_evaluation(model_id, reference_id, runset_id, timestamp, previous_max_time, debug_lvl=0):
    """

    :param model_id:
    :param reference_id:
    :param runset_id:
    :param timestamp:
    :param previous_max_time:
    :param debug_lvl:
    :return:
    """

    sc_evaluation_id = "disctimeexceeval"

    count_del_files = 0

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # establishing folders
    hist_folder_path = FolderDefinition.get_historical_eval_folder_path(model_id, sc_evaluation_id, reference_id,
                                                                        runset_id)

    # define timestamps
    if timestamp is None:
        max_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)
    else:
        max_timestamp = timestamp
    if max_timestamp is None:
        Debug.dl("evalcln_disctimeexceeval: Failed to get a max timestamp from '{0}'.".format(hist_folder_path), 2,
                 debug_lvl)
        return
    min_timestamp = int(max_timestamp - (previous_max_time * 24 * 60 * 60))

    hist_file_names = os.listdir(hist_folder_path)

    # list all files and remove the older ones
    for cur_hist_filename in hist_file_names:

        cur_release_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_hist_filename)
        if min_timestamp <= cur_release_timestamp <= max_timestamp:
            continue

        cur_file_path = os.path.join(hist_folder_path, cur_hist_filename)
        Debug.dl("evalcln_disctimeexceeval: Deleting file {0} (references: {1} and {2}).".format(cur_file_path,
                                                                                                 min_timestamp,
                                                                                                 max_timestamp),
                 2, debug_lvl)
        count_del_files += 1
        os.unlink(os.path.join(hist_folder_path, cur_hist_filename))

    # debug info
    d_time = time.time()-start_time

    Debug.dl("evalcln_disctimeexceeval: Deleted {0} files in {1} seconds".format(count_del_files, d_time), 1, debug_lvl)


# ####################################################### CALL ####################################################### #

clean_historical_evaluation(model_id_arg, reference_id_arg, runset_id_arg, timestamp_arg, previous_max_time_arg,
                            debug_lvl=debug_level_arg)
