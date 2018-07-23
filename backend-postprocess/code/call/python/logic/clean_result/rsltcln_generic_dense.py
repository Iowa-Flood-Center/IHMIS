import shutil
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.FilenameDefinition import FilenameDefinition
from libs.FolderDefinition import FolderDefinition
from libs.RsltClnInterface import RsltClnInterface
from libs.FileDefinition import FileDefinition
from libs.Debug import Debug

debug_level_arg = 10
previous_days_repr_default = 30.5  # for how many days historical representation data must be hold by default
previous_days_eval_default = 2.1   # for how many days historical evaluation data must be hold by default
clean_if_no_replacement = False
any_error = False

# ####################################################### ARGS ####################################################### #

model_id_arg = RsltClnInterface.get_model_id(sys.argv)
evaluation_id_arg = RsltClnInterface.get_evaluation_id(sys.argv)
reference_id_arg = RsltClnInterface.get_reference_id(sys.argv)
representation_id_arg = RsltClnInterface.get_representation_id(sys.argv)
timestamp_arg = RsltClnInterface.get_timestamp(sys.argv)
prevdays_arg = RsltClnInterface.get_back_days(sys.argv)
runset_id_arg = RsltClnInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def is_representation_clean(model_id, evaluation_id, representation_id, debug_lvl=0):
    """
    Check if arguments given are related to a model representation cleaning request
    :param model_id:
    :param evaluation_id:
    :param representation_id:
    :param debug_lvl:
    :return:
    """

    return True if (model_id is not None) and (representation_id is not None) and (evaluation_id is None) else False


def is_evaluation_clean(model_id, evaluation_id, reference_id, debug_lvl=0):
    """
    Check if arguments given are related to a model evaluation cleaning request
    :param model_id:
    :param evaluation_id:
    :param reference_id:
    :param debug_lvl:
    :return:
    """

    return True if (model_id is not None) and (evaluation_id is not None) and (reference_id is not None) else False


def clean_historical_representation(model_id, representation_id, runset_id, timestamp, previous_max_time, debug_lvl=0):
    """

    :param model_id:
    :param representation_id:
    :param runset_id:
    :param timestamp:
    :param previous_max_time:
    :param debug_lvl:
    :return:
    """

    count_del_files = 0

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # establishing folders
    hist_folder_path = FolderDefinition.get_historical_img_folder_path(model_id, representation_id, runset_id)

    # define timestamps
    if timestamp is None:
        max_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)
    else:
        max_timestamp = timestamp
    if max_timestamp is None:
        Debug.dl("rsltcln_generic_dense: Failed to get a max timestamp from '{0}'.".format(hist_folder_path), 2,
                 debug_lvl)
        return
    min_timestamp = int(max_timestamp - (previous_max_time * 24 * 60 * 60))

    hist_file_names = os.listdir(hist_folder_path)

    # list all files, identifying the higher timestamp for each link id
    for cur_hist_filename in hist_file_names:
        try:
            cur_release_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_hist_filename)
        except ValueError:
            Debug.dl("rsltcln_generic_dense: File is not in 'dense naming' format '{0}'.".format(cur_hist_filename),
                     2, debug_lvl)
            break

        if min_timestamp <= cur_release_timestamp <= max_timestamp:
            continue
        else:
            cur_file_path = os.path.join(hist_folder_path, cur_hist_filename)
            Debug.dl("rsltcln_generic_dense: Deleting file {0} (references: {1} and {2}).".format(cur_file_path,
                                                                                                        min_timestamp,
                                                                                                        max_timestamp),
                     2, debug_lvl)
            count_del_files += 1
            os.unlink(os.path.join(hist_folder_path, cur_hist_filename))

    # debug info
    d_time = time.time()-start_time

    Debug.dl("rsltcln_generic_dense: Deleted {0} files in {1} seconds".format(count_del_files, d_time), 1, debug_lvl)


def clean_historical_evaluation(model_id, sc_evaluation_id, reference_id, runset_id, timestamp, previous_max_time,
                                debug_lvl=0):
    """

    :param model_id:
    :param sc_evaluation_id:
    :param reference_id:
    :param runset_id:
    :param timestamp:
    :param previous_max_time:
    :param debug_lvl:
    :return:
    """

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
        Debug.dl("rsltcln_generic_dense: Failed to get a max timestamp from '{0}'.".format(hist_folder_path), 2,
                 debug_lvl)
        return
    min_timestamp = int(max_timestamp - (previous_max_time * 24 * 60 * 60))

    hist_file_names = os.listdir(hist_folder_path)

    # list all files, identifying the higher timestamp for each link id
    for cur_hist_filename in hist_file_names:
        cur_release_timestamp = FileDefinition.obtain_hist_file_timestamp(cur_hist_filename)

        if min_timestamp <= cur_release_timestamp <= max_timestamp:
            continue
        else:
            cur_file_path = os.path.join(hist_folder_path, cur_hist_filename)
            Debug.dl("rsltcln_generic_dense: Deleting file {0} (references: {1} and {2}).".format(cur_file_path,
                                                                                                  min_timestamp,
                                                                                                  max_timestamp),
                     2, debug_lvl)
            count_del_files += 1
            os.unlink(os.path.join(hist_folder_path, cur_hist_filename))

    # debug info
    d_time = time.time()-start_time

    Debug.dl("rsltcln_generic_dense: Deleted {0} files in {1} seconds".format(count_del_files, d_time), 1, debug_lvl)

# ####################################################### CALL ####################################################### #

# basic check - must have a model and a runset at very least
if model_id_arg is None:
    Debug.dl("rsltcln_generic_dense: Missing sc_model_id.", 1, debug_level_arg)
    any_error = True
if runset_id_arg is None:
    Debug.dl("rsltcln_generic_dense: Missing runset_id.", 1, debug_level_arg)
    any_error = True

if is_representation_clean(model_id_arg, evaluation_id_arg, representation_id_arg, debug_lvl=debug_level_arg):
    if not any_error:
        Debug.dl("rsltcln_generic_dense: Cleaning representation for {0}.{1}.{2}".format(runset_id_arg, model_id_arg,
                                                                                         representation_id_arg),
                 1, debug_level_arg)
        prevdays_arg = prevdays_arg if prevdays_arg is not None else previous_days_repr_default
        clean_historical_representation(model_id_arg, representation_id_arg, runset_id_arg, timestamp_arg, prevdays_arg,
                                        debug_lvl=debug_level_arg)
elif is_evaluation_clean(model_id_arg, evaluation_id_arg, reference_id_arg, debug_lvl=debug_level_arg):
    if not any_error:
        Debug.dl("rsltcln_generic_dense: Cleaning evaluation for {0}.{1}.{2}_{3}".format(runset_id_arg, model_id_arg,
                                                                                         evaluation_id_arg,
                                                                                         reference_id_arg),
                 1, debug_level_arg)
        prevdays_arg = prevdays_arg if prevdays_arg is not None else previous_days_eval_default
        clean_historical_evaluation(model_id_arg, evaluation_id_arg, reference_id_arg, runset_id_arg, timestamp_arg,
                                    prevdays_arg, debug_lvl=debug_level_arg)
else:
    Debug.dl("rsltcln_generic_dense: Impossible to determine Representation or Evaluation task.", 1, debug_level_arg)
    any_error = True

if any_error:
    Debug.dl("rsltcln_generic_dense: Nothing performed.", 1, debug_level_arg)
    exit(0)

print("Done")
