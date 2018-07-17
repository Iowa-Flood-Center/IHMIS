import shutil
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.EvalGenInterface import EvalGenInterface
from libs.FolderDefinition import FolderDefinition
from libs.Debug import Debug

debug_level_arg = 10
clean_if_no_replacement = False

# ####################################################### ARGS ####################################################### #

model_id_arg = EvalGenInterface.get_model_id(sys.argv)
timestamp_arg = EvalGenInterface.get_timestamp(sys.argv)
reference_id_arg = EvalGenInterface.get_reference_id(sys.argv)
runset_id_arg = EvalGenInterface.get_runset_id(sys.argv)


# ####################################################### DEFS ####################################################### #

def update_displayed_evaluation(model_id, reference_id, runset_id, timestamp, debug_lvl=0):
    """

    :param model_id:
    :param reference_id:
    :param runset_id:
    :param timestamp:
    :return:
    """

    sc_evaluation_id = "hydrographsd"

    count_del_files = 0
    count_cpy_files = 0

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # establishing folders
    folder_name = FolderDefinition.get_eval_folder_name(sc_evaluation_id, reference_id)
    display_folder_path = FolderDefinition.get_displayed_folder_path(model_id, folder_name, runset_id=runset_id)
    hist_folder_path = FolderDefinition.get_historical_eval_folder_path(model_id, sc_evaluation_id, reference_id,
                                                                        runset_id)

    # define timestamp
    if timestamp is None:
        max_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)
    else:
        max_timestamp = timestamp

    dict_updated_times = {}

    hist_file_names = os.listdir(hist_folder_path)

    # list all files, identifying the higher timestamp for each link id
    for cur_hist_filename in hist_file_names:
        cur_splitted_file_basename = os.path.splitext(cur_hist_filename)[0].split("_")
        cur_release_timestamp = int(cur_splitted_file_basename[0])
        cur_linkid = int(cur_splitted_file_basename[1])

        if cur_release_timestamp > max_timestamp:
            continue

        if (cur_linkid not in dict_updated_times.keys()) or (dict_updated_times[cur_linkid] < cur_release_timestamp):
            dict_updated_times[cur_linkid] = cur_release_timestamp

    # base check
    if (len(dict_updated_times.keys()) == 0) and (not clean_if_no_replacement):
        # TODO - add debug
        return

    # clean display folder and ensure it exists
    if os.path.exists(display_folder_path):
        for cur_disp_file_name in os.listdir(display_folder_path):
            os.unlink(os.path.join(display_folder_path, cur_disp_file_name))
            count_del_files += 1
    else:
        os.makedirs(display_folder_path)

    # define file names and copy files
    for cur_linkid in dict_updated_times.keys():
        cur_file_timestamp = dict_updated_times[cur_linkid]
        cur_file_name = "{0}_{1}.json".format(cur_file_timestamp, cur_linkid)
        cur_hist_file_path = os.path.join(hist_folder_path, cur_file_name)
        cur_disp_file_path = os.path.join(display_folder_path, cur_file_name)

        shutil.copy(cur_hist_file_path, cur_disp_file_path)
        count_cpy_files += 1

    # debug info
    d_time = time.time()-start_time

    Debug.dl("evalupd_hydroforecast_graph: Deleted {0} files, copied {1} files in {2} seconds".format(count_del_files,
                                                                                                      count_cpy_files,
                                                                                                      d_time),
             1, debug_lvl)


# ####################################################### CALL ####################################################### #

update_displayed_evaluation(model_id_arg, reference_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
