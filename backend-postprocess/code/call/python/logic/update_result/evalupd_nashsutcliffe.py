import shutil
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.ResultsDisplayUpdater import ResultsDisplayUpdater
from libs.FolderDefinition import FolderDefinition
from libs.EvalGenInterface import EvalGenInterface
from libs.ImageDefinition import ImageDefinition
from libs.Debug import Debug

debug_level_arg = 3

# ####################################################### ARGS ####################################################### #

model_id_arg = EvalGenInterface.get_model_id(sys.argv)
reference_id_arg = EvalGenInterface.get_reference_id(sys.argv)
timestamp_arg = EvalGenInterface.get_timestamp(sys.argv)
runset_id_arg = EvalGenInterface.get_runset_id(sys.argv)


# ####################################################### DEFS ####################################################### #

def update_display_files(sc_model_id, sc_reference_id, sc_runset_id, timestamp, debug_lvl=0):
    """

    :param sc_model_id:
    :param sc_reference_id:
    :param sc_runset_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    sc_evaluation = "nashsutcliffe"

    # defining effective 0-ref timestamp
    if timestamp is None:
        eval_folder_path = FolderDefinition.get_historical_eval_folder_path(sc_model_id, sc_evaluation, sc_reference_id,
                                                                            sc_runset_id)
        ref0_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(eval_folder_path)
        if ref0_timestamp is None:
            Debug.dl("evalupd_nashsutcliffe: No file at '{0}'.".format(eval_folder_path), 2, debug_lvl)
        else:
            Debug.dl("evalupd_nashsutcliffe: Most recent timestamp in '{0}' is {1}.".format(eval_folder_path,
                                                                                            ref0_timestamp),
                     2, debug_lvl)
    else:
        ref0_timestamp = timestamp

    update_historical_parameter_representations(sc_model_id, sc_evaluation, sc_evaluation, sc_reference_id, sc_runset_id,
                                                3600, ref0_timestamp, clean_previous=True, debug_lvl=debug_lvl)

    folder_name = FolderDefinition.get_eval_folder_name(sc_evaluation, sc_reference_id)
    ResultsDisplayUpdater.update_ref0_file(sc_model_id, folder_name, sc_runset_id, ref0_timestamp, debug_lvl=debug_lvl)


def update_historical_parameter_representations(sc_model_id, sc_evaluation_id, sc_evaluation, sc_reference_id,
                                                sc_runset_id, time_interval, ref0_timestamp, clean_previous=True,
                                                debug_lvl=0):
    """

    :param sc_model_id: String.
    :param sc_evaluation_id: String.
    :param time_interval: Integer. Delta time between representations in seconds
    :param ref0_timestamp: Integer.
    :param clean_previous: Boolean.
    :param debug_lvl: Integer.
    :return: Integer. Number of copied files.
    """

    # TODO - rethink this constant location
    historical_maximum_back_time = 10 * 24 * 60 * 60    # 10 days in seconds

    # basic check
    if ref0_timestamp is None:
        Debug.dl("evalupd_nashsutcliffe: Timestamp 0-ref is None. Skipping.", 2, debug_lvl)
        return

    folder_name = FolderDefinition.get_eval_folder_name(sc_evaluation, sc_reference_id)

    # define update and historical folders
    upd_folder_path = FolderDefinition.get_displayed_folder_path(model_id=sc_model_id, parameter_id=folder_name,
                                                                 runset_id=sc_runset_id)

    # clear previous file
    if clean_previous:
        if os.path.exists(upd_folder_path):
            for cur_filename in os.listdir(upd_folder_path):
                cur_filepath = os.path.join(upd_folder_path, cur_filename)
                if os.path.isfile(cur_filepath):
                    os.unlink(cur_filepath)
        else:
            os.makedirs(upd_folder_path)

    # check and copy-renaming as possible
    cur_delta_timestamp = 0
    cur_index = 0
    count_copied = 0
    while cur_delta_timestamp < historical_maximum_back_time:
        cur_timestamp = ref0_timestamp - cur_delta_timestamp
        cur_hist_folderpath = FolderDefinition.get_historical_eval_folder_path(sc_model_id, sc_evaluation,
                                                                               sc_reference_id, sc_runset_id)
        cur_hist_filename = ImageDefinition.define_displayed_file_name(cur_timestamp, sc_evaluation_id,
                                                                       file_extension=".json")
        cur_hist_filepath = os.path.join(cur_hist_folderpath, cur_hist_filename)
        if os.path.exists(cur_hist_filepath):
            cur_disp_folderpath = FolderDefinition.get_displayed_folder_path(sc_model_id, folder_name, sc_runset_id)
            cur_disp_filename = ImageDefinition.define_displayed_file_name(cur_index, sc_evaluation_id,
                                                                           file_extension=".json")
            cur_disp_filepath = os.path.join(cur_disp_folderpath, cur_disp_filename)
            shutil.copy(cur_hist_filepath, cur_disp_filepath)
            Debug.dl("evalupd_nashsutcliffe: Updated '{0}' => '{1}'.".format(os.path.basename(cur_hist_filepath),
                                                                                cur_disp_filepath), 2, debug_lvl)
            count_copied += 1
        else:
            print("evalupd_nashsutcliffe: Not found {0}.".format(cur_hist_filepath))

        cur_index += 1
        cur_delta_timestamp += time_interval

    return count_copied

# ####################################################### CALL ####################################################### #

update_display_files(model_id_arg, reference_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
