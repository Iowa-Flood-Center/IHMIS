import shutil
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.ReprCombGenInterface import ReprCombGenInterface
from libs.FilenameDefinition import FilenameDefinition
from libs.FolderDefinition import FolderDefinition
from libs.FileDefinition import FileDefinition
from libs.Debug import Debug

debug_level_arg = 9

# ####################################################### ARGS ####################################################### #

modelcomb_id_arg = ReprCombGenInterface.get_modelcomb_id(sys.argv)
runset_id_arg = ReprCombGenInterface.get_runset_id(sys.argv)
timestamp_arg = ReprCombGenInterface.get_timestamp(sys.argv)  # last expected observation, first forecast data
# timestamp_min_arg = ReprCombGenInterface.get_min_timestamp_hist(sys.argv)  # graph forced minimum interval
# timestamp_max_arg = ReprCombGenInterface.get_max_timestamp_hist(sys.argv)  # graph forced maximum interval


# ####################################################### DEFS ####################################################### #

def update_display_files(modelcomb_id, runset_id, timestamp, debug_lvl=0):
    """

    :param modelcomb_id:
    :param runset_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    sc_reprcomp = "bestrmsforecasted"

    # defining effective 0-ref timestamp
    if timestamp is None:
        modelpaststg_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                                        represcomb_id=sc_reprcomp)
        ref0_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(modelpaststg_folder_path)
        if ref0_timestamp is None:
            Debug.dl("rpcbupd_bestrmsforecasted: No file at '{0}'.".format(eval_folder_path), 2, debug_lvl)
        else:
            Debug.dl("rpcbupd_bestrmsforecasted: Most recent timestamp in '{0}' is {1}.".format(
                modelpaststg_folder_path, ref0_timestamp), 2, debug_lvl)
    else:
        ref0_timestamp = timestamp

    update_historical_representations_composition(modelcomb_id, sc_reprcomp, runset_id, ref0_timestamp,
                                                  clean_previous=True, debug_lvl=debug_lvl)


def update_historical_representations_composition(sc_modelcomb_id, sc_reprcomp_id, sc_runset_id, ref0_timestamp,
                                                  clean_previous=True, debug_lvl=0):
    """

    :param sc_modelcomb_id:
    :param sc_reprcomp_id:
    :param sc_runset_id:
    :param ref0_timestamp:
    :param clean_previous:
    :param debug_lvl:
    :return:
    """

    # define source and destination folder paths
    src_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id, represcomb_id=sc_reprcomp_id)
    dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id, sc_modelcomb_id,
                                                                           represcomb_id=sc_reprcomp_id)

    # create folder tree if necessary
    if not os.path.exists(dest_folder_path):
        os.makedirs(dest_folder_path)
        Debug.dl("rpcbupd_bestrmsforecasted: Created folder '{0}'.".format(dest_folder_path), 2, debug_lvl)

    # clean folder if necessary
    count_del = 0
    if clean_previous:
        prev_files = os.listdir(dest_folder_path)
        if len(prev_files) > 0:
            for cur_fname in prev_files:
                cur_fpath = os.path.join(dest_folder_path, cur_fname)
                os.remove(cur_fpath)
                count_del += 1

    submit_dict = FolderDefinition.retrive_most_recent_timestamps_in_hist_folder(src_folder_path)

    # copy all files with given timestamp0
    count_cpy = 0
    for cur_file_name in submit_dict.values():
        cur_src_file_path = os.path.join(src_folder_path, cur_file_name)
        cur_dst_file_path = os.path.join(dest_folder_path, cur_file_name)
        shutil.copy(cur_src_file_path, cur_dst_file_path)
        count_cpy += 1

    Debug.dl("rpcbupd_bestrmsforecasted: Deleted previous {0}, copied {1} new files...".format(
        count_del, count_cpy), 2, debug_lvl)
    Debug.dl("                         ... on folder '{0}'.".format(dest_folder_path), 2, debug_lvl)


# ####################################################### CALL ####################################################### #

update_display_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
