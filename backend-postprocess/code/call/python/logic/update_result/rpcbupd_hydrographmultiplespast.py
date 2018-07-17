import shutil
import json
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.ReprCombGenInterface import ReprCombGenInterface
from libs.FilenameDefinition import FilenameDefinition
from libs.FolderDefinition import FolderDefinition
from libs.FileDefinition import FileDefinition
from libs.GeneralUtils import GeneralUtils
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

    sc_reprcomp = "hydrographmultiplespast"
    ref0_frame = "modelpaststg"

    # defining effective 0-ref timestamp
    all_ref0_timestamps = []
    ref0_timestamps = None
    if timestamp is None:
        modelpaststg_model_ids = ensure_list(get_frame_model_ids(modelcomb_id, runset_id, sc_reprcomp, ref0_frame,
                                                                 debug_lvl=debug_lvl))

        if modelpaststg_model_ids is None:
            print("We got a None here!")
            return

        # define the most recent timestamp of all models
        for cur_modelpaststg_model_id in modelpaststg_model_ids:
            cur_modelpaststg_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                                                represcomb_id=sc_reprcomp,
                                                                                                frame_id=ref0_frame,
                                                                                                model_id=cur_modelpaststg_model_id)
            cur_ref0_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(cur_modelpaststg_folder_path)
            if cur_ref0_timestamp is None:
                Debug.dl("rpcbupd_hydrographmultiplespast: No file at '{0}'.".format(cur_modelpaststg_folder_path), 2,
                         debug_lvl)
            else:
                Debug.dl("rpcbupd_hydrographmultiplespast: Most recent timestamp in '{0}' is {1}.".format(
                    cur_modelpaststg_folder_path, cur_ref0_timestamp), 2, debug_lvl)
                all_ref0_timestamps.append(cur_ref0_timestamp)

        # the maximum timestamp will be the minimum of all maximums
        ref0_timestamp = min(all_ref0_timestamps) if len(all_ref0_timestamps) > 0 else None

    else:
        ref0_timestamp = timestamp

    # basic check
    if ref0_timestamp is None:
        Debug.dl("rpcbupd_hydrographmultiplespast: Impossible to establish minimum timestamp for '{0}.{1}'.".format(
            runset_id, modelcomb_id), 2, debug_lvl)
        return

    #
    update_historical_representations_composition(modelcomb_id, sc_reprcomp, runset_id, ref0_timestamp,
                                                  clean_previous=True, debug_lvl=debug_lvl)


def get_frame_model_ids(modelcomb_id, runset_id, represcomb_id, frame, debug_lvl=0):
    """

    :param modelcomb_id:
    :param runset_id:
    :param debug_lvl:
    :return: A string if there is only one model of given frame, an assay of strings if there are more.
    """

    # TODO - move to a shared place. FolderDefinition ?

    # get entire model comb file
    modelcomb_file_path = FileDefinition.obtain_modelcomb_file_path(modelcomb_id, runset_id, debug_lvl=debug_lvl)
    if (modelcomb_file_path is None) or (not os.path.exists(modelcomb_file_path)):
        Debug.dl("rpcbupd_hydrographmultiplespast: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return None

    # read file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbupd_hydrographmultiplespast: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return None

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbupd_hydrographmultiplespast: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".format(
            runset_id, modelcomb_id, represcomb_id), 0, debug_lvl)
        return None

    # looks for required frame
    frame_set = represcomb_set[represcomb_id]
    model_ids = []
    for cur_model_id in frame_set.keys():
        if frame_set[cur_model_id] == frame:
            model_ids.append(str(cur_model_id))

    # return None, one string or a list of strings
    if len(model_ids) == 0:
        return None
    elif len(model_ids) == 1:
        return model_ids[0]
    else:
        return model_ids


def ensure_list(get_frame_model_ids_return):
    """

    :param get_frame_model_ids_return:
    :return:
    """
    if get_frame_model_ids_return is None:
        return []
    elif isinstance(get_frame_model_ids_return, str) or isinstance(get_frame_model_ids_return, basestring):
        return [get_frame_model_ids_return]
    else:
        return get_frame_model_ids_return


def update_historical_representations_composition(sc_modelcomb_id, sc_reprcomp_id, sc_runset_id, ref0_timestamp,
                                                  clean_previous=True, debug_lvl=0):
    """

    :param sc_modelcomp_id:
    :param sc_reprcomp_id:
    :param sc_runset_id:
    :param ref0_timestamp:
    :param clean_previous:
    :param debug_lvl:
    :return:
    """

    # define models
    modelpaststg_model_ids = ensure_list(get_frame_model_ids(sc_modelcomb_id, sc_runset_id, sc_reprcomp_id,
                                                             "modelpaststg", debug_lvl=debug_lvl))
    stageref_reference_ids = ensure_list(get_frame_model_ids(sc_modelcomb_id, sc_runset_id, sc_reprcomp_id, "stageref",
                                                             debug_lvl=debug_lvl))
    dischref_reference_ids = ensure_list(get_frame_model_ids(sc_modelcomb_id, sc_runset_id, sc_reprcomp_id, "dischref",
                                                            debug_lvl=debug_lvl))

    # basic check
    if modelpaststg_model_ids == None:
        Debug.dl("rpcbupd_hydrographmultiplespast: Needs at least one 'modelpaststg' model.", 0, debug_lvl)
        return

    # replace files for 'modelpaststg' frame
    for cur_modelpaststg_model_id in modelpaststg_model_ids:
        cur_modelpaststg_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id,
                                                                                                sc_modelcomb_id,
                                                                                                represcomb_id=sc_reprcomp_id,
                                                                                                frame_id="modelpaststg",
                                                                                                model_id=cur_modelpaststg_model_id)
        if clean_previous and os.path.exists(cur_modelpaststg_dest_folder_path):
            shutil.rmtree(cur_modelpaststg_dest_folder_path)
        os.makedirs(cur_modelpaststg_dest_folder_path)
        cur_modelpaststg_source_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id,
                                                                                                   represcomb_id=sc_reprcomp_id,
                                                                                                   frame_id="modelpaststg",
                                                                                                   model_id=cur_modelpaststg_model_id)
        all_modelpaststg_hist_files = os.listdir(cur_modelpaststg_source_folder_path)
        count_copied = 0
        for cur_modelpaststg_hist_file_name in all_modelpaststg_hist_files:
            cur_modelpaststg_hist_file_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_modelpaststg_hist_file_name)
            if cur_modelpaststg_hist_file_timestamp == ref0_timestamp:
                cur_file_path = os.path.join(cur_modelpaststg_source_folder_path, cur_modelpaststg_hist_file_name)
                shutil.copy(cur_file_path, cur_modelpaststg_dest_folder_path)
                count_copied += 1
            else:
                cur_modelpaststg_hist_file_timestamp_rounded = GeneralUtils.round_timestamp_hour(cur_modelpaststg_hist_file_timestamp)
                if cur_modelpaststg_hist_file_timestamp_rounded == ref0_timestamp:
                    cur_file_path = os.path.join(cur_modelpaststg_source_folder_path, cur_modelpaststg_hist_file_name)
                    shutil.copy(cur_file_path, cur_modelpaststg_dest_folder_path)
                    count_copied += 1

        Debug.dl("rpcbupd_hydrographmultiplespast: Filled '{0}' folder.".format(cur_modelpaststg_dest_folder_path), 1,
                 debug_lvl)
        Debug.dl("                                     Copied {0} files.".format(count_copied), 1, debug_lvl)

    # replace files for 'stageref_reference_ids' frame
    print("Got {0} stageref_reference_ids.".format(len(stageref_reference_ids)))
    for cur_stageref_reference_id in stageref_reference_ids:
        # define destination and source folder paths
        cur_stageref_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id,
                                                                                            sc_modelcomb_id,
                                                                                            represcomb_id=sc_reprcomp_id,
                                                                                            frame_id="stageref",
                                                                                            model_id=cur_stageref_reference_id)
        if clean_previous and os.path.exists(cur_stageref_dest_folder_path):
            shutil.rmtree(cur_stageref_dest_folder_path)
        os.makedirs(cur_stageref_dest_folder_path)
        cur_stageref_source_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id,
                                                                                               represcomb_id=sc_reprcomp_id,
                                                                                               frame_id="stageref",
                                                                                               model_id=cur_stageref_reference_id)

        # list all source files, getting the closest ones that is possible (range of 6 hours)
        ref_timestamp_dist = {}
        ref_timestamp_timestamp = {}
        all_stageref_hist_files = os.listdir(cur_stageref_source_folder_path)
        print("Evaluating {0} stageref files.".format(len(all_stageref_hist_files)))
        for cur_stageref_hist_file_name in all_stageref_hist_files:
            cur_stageref_hist_file_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_stageref_hist_file_name)
            cur_stageref_hist_file_linkid = FilenameDefinition.obtain_hist_file_linkid(cur_stageref_hist_file_name)
            cur_time_dist = abs(ref0_timestamp - cur_stageref_hist_file_timestamp)
            if cur_time_dist <= 6 * 60 * 60:
                if (cur_stageref_hist_file_linkid not in ref_timestamp_dist.keys()) or \
                                cur_time_dist < ref_timestamp_dist[cur_stageref_hist_file_linkid]:
                    ref_timestamp_dist[cur_stageref_hist_file_linkid] = cur_time_dist
                    ref_timestamp_timestamp[cur_stageref_hist_file_linkid] = cur_stageref_hist_file_timestamp
                else:
                    print("Ignoring '{0}' ({1}, {2}).".format(cur_stageref_hist_file_name,
                                                              cur_stageref_hist_file_timestamp,
                                                              cur_stageref_hist_file_linkid))
            else:
                Debug.dl("rpcbupd_hydrographmultiplespast: Ignoring '{0}' ({1} > {2}).".format(cur_stageref_hist_file_name,
                                                                                               cur_time_dist,
                                                                                               6 * 60 * 60),
                         1, debug_lvl)

        # copy all selected files
        print("Listed {0} files for copying.".format(len(ref_timestamp_timestamp)))
        for cur_copy_linkid in ref_timestamp_timestamp.keys():
            cur_stageref_file_name = "{0}_{1}.json".format(ref_timestamp_timestamp[cur_copy_linkid], cur_copy_linkid)  # TODO - this should be in a shared library
            cur_file_path = os.path.join(cur_stageref_source_folder_path, cur_stageref_file_name)
            shutil.copy(cur_file_path, cur_stageref_dest_folder_path)
            Debug.dl("rpcbupd_hydrographmultiplespast: Copying '{0}' to '{1}'.".format(cur_file_path,
                                                                                       cur_stageref_dest_folder_path),
                     1, debug_lvl)


        Debug.dl("rpcbupd_hydrographmultiplespast: Filled '{0}' folder.".format(cur_stageref_dest_folder_path), 1,
                 debug_lvl)

    # replace files for 'dischref_reference_ids' frame
    ## min_timestamp_limit = ref0_timestamp - 3600  # old
    ## max_timestamp_limit = ref0_timestamp + 3600  # old
    print("Got {0} dischref_reference_ids.".format(len(dischref_reference_ids)))
    for cur_dischref_reference_id in dischref_reference_ids:
        cur_dischref_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id,
                                                                                            sc_modelcomb_id,
                                                                                            represcomb_id=sc_reprcomp_id,
                                                                                            frame_id="dischref",
                                                                                            model_id=cur_dischref_reference_id)
        if clean_previous and os.path.exists(cur_dischref_dest_folder_path):
            shutil.rmtree(cur_dischref_dest_folder_path)
        os.makedirs(cur_dischref_dest_folder_path)
        cur_dischref_source_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id,
                                                                                               represcomb_id=sc_reprcomp_id,
                                                                                               frame_id="dischref",
                                                                                               model_id=cur_dischref_reference_id)

        # list all source files, getting the closest ones that is possible (range of 6 hours)
        ref_timestamp_dist = {}
        ref_timestamp_timestamp = {}
        all_dischref_hist_files = os.listdir(cur_dischref_source_folder_path)
        print("Evaluating {0} dischref files.".format(len(all_dischref_hist_files)))
        for cur_dischref_hist_file_name in all_dischref_hist_files:
            cur_dischref_hist_file_timestamp = FileDefinition.obtain_hist_file_timestamp(cur_dischref_hist_file_name)
            cur_dischref_hist_file_linkid = FileDefinition.obtain_hist_file_linkid(cur_dischref_hist_file_name)
            cur_time_dist = abs(ref0_timestamp - cur_dischref_hist_file_timestamp)
            if cur_time_dist <= 6 * 60 * 60:
                Debug.dl("rpcbupd_hydrographmultiplespast: Considering '{0}' file.".format(cur_dischref_hist_file_name),
                         1, debug_lvl)

                if (cur_dischref_hist_file_linkid not in ref_timestamp_dist.keys()) or \
                                cur_time_dist < ref_timestamp_dist[cur_dischref_hist_file_linkid]:
                    ref_timestamp_dist[cur_dischref_hist_file_linkid] = cur_time_dist
                    ref_timestamp_timestamp[cur_dischref_hist_file_linkid] = cur_dischref_hist_file_timestamp
                else:
                    print("Ignoring '{0}' ({1}, {2}).".format(cur_dischref_hist_file_name,
                                                              cur_dischref_hist_file_timestamp,
                                                              cur_dischref_hist_file_linkid))

            else:
                Debug.dl("rpcbupd_hydrographmultiplespast: Ignoring '{0}' file.".format(cur_dischref_hist_file_name), 1,
                         debug_lvl)

        # copy all selected files
        Debug.dl("rpcbupd_hydrographmultiplespast: Listed {0} files of dischref for copying.".format(
            len(ref_timestamp_timestamp)), 4, debug_lvl)
        for cur_copy_linkid in ref_timestamp_timestamp.keys():
            cur_dischref_file_name = "{0}_{1}.json".format(ref_timestamp_timestamp[cur_copy_linkid], cur_copy_linkid)  # TODO - this should be in a shared library
            cur_file_path = os.path.join(cur_dischref_source_folder_path, cur_dischref_file_name)
            shutil.copy(cur_file_path, cur_dischref_dest_folder_path)
            Debug.dl("rpcbupd_hydrographmultiplespast: Copying '{0}' to '{1}'.".format(cur_file_path,
                                                                                       cur_dischref_dest_folder_path),
                     1, debug_lvl)

    # replace 'common' files
    common_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id, sc_modelcomb_id,
                                                                                  represcomb_id=sc_reprcomp_id,
                                                                                  frame_id="common")
    if clean_previous and os.path.exists(common_dest_folder_path):
        shutil.rmtree(common_dest_folder_path)
    os.makedirs(common_dest_folder_path)
    common_source_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id,
                                                                                     represcomb_id=sc_reprcomp_id,
                                                                                     frame_id="common")
    all_common_hist_files = os.listdir(common_source_folder_path)
    for cur_common_hist_file_name in all_common_hist_files:
        cur_file_path = os.path.join(common_source_folder_path, cur_common_hist_file_name)
        shutil.copy(cur_file_path, common_dest_folder_path)

    Debug.dl("rpcbupd_hydrographmultiplespast: Filled '{0}' folder.".format(common_dest_folder_path), 1, debug_lvl)

# ####################################################### CALL ####################################################### #

update_display_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
