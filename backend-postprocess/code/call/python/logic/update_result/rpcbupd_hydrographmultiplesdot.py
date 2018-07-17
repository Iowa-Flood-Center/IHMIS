import shutil
import json
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

    sc_reprcomp = "hydrographmultiplesdot"
    ref0_frame = "modelpaststg"

    # defining effective 0-ref timestamp
    if timestamp is None:
        modelpaststg_model_id = get_frame_model_ids(modelcomb_id, runset_id, sc_reprcomp, ref0_frame,
                                                    debug_lvl=debug_lvl)
        if isinstance(modelpaststg_model_id, str) or isinstance(modelpaststg_model_id, basestring):
            modelpaststg_model_ids = [modelpaststg_model_id]
        else:
            modelpaststg_model_ids = modelpaststg_model_id
        ref0_timestamp = None
        for cur_modelpaststg_model_id in modelpaststg_model_ids:
            cur_modelpaststg_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                                                represcomb_id=sc_reprcomp,
                                                                                                frame_id=ref0_frame,
                                                                                                model_id=cur_modelpaststg_model_id)
            cur_ref0_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(cur_modelpaststg_folder_path)
            if (ref0_timestamp is None) or (cur_ref0_timestamp > ref0_timestamp):
                ref0_timestamp = cur_ref0_timestamp
            if ref0_timestamp is None:
                Debug.dl("rpcbupd_hydrographmultiples: No file at '{0}'.".format(cur_modelpaststg_folder_path), 2, debug_lvl)
            else:
                Debug.dl("rpcbupd_hydrographmultiples: Most recent timestamp in '{0}' is {1}.".format(cur_modelpaststg_folder_path,
                                                                                                      ref0_timestamp),
                         2, debug_lvl)

    else:
        ref0_timestamp = timestamp

    #
    update_historical_representations_composition(modelcomb_id, sc_reprcomp, runset_id, ref0_timestamp,
                                                  clean_previous=True, debug_lvl=debug_lvl)


def get_frame_model_ids(modelcomb_id, runset_id, represcomb_id, frame, debug_lvl=0):
    """

    :param modelcomb_id:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    # TODO - move to a shared place. FolderDefinition ?

    # get entire model comb file
    modelcomb_file_path = FileDefinition.obtain_modelcomb_file_path(modelcomb_id, runset_id, debug_lvl=debug_lvl)
    if (modelcomb_file_path is None) or (not os.path.exists(modelcomb_file_path)):
        Debug.dl("rpcbupd_hydrographmultiplesalert: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return None

    # read file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbupd_hydrographmultiplesalert: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return None

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbupd_hydrographmultiplesalert: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".format(
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
    modelpaststg_model_ids = get_frame_model_ids(sc_modelcomb_id, sc_runset_id, sc_reprcomp_id, "modelpaststg",
                                                debug_lvl=debug_lvl)
    modelforestg_model_ids = get_frame_model_ids(sc_modelcomb_id, sc_runset_id, sc_reprcomp_id, "modelforestg",
                                                 debug_lvl=debug_lvl)
    modelforestgalert_model_ids = get_frame_model_ids(sc_modelcomb_id, sc_runset_id, sc_reprcomp_id,
                                                      "modelforestgalert", debug_lvl=debug_lvl)

    # basic check
    if modelpaststg_model_ids is None:
        Debug.dl("rpcbupd_hydrographmultiplesalert: Needs at least one 'modelpaststg' model.", 0, debug_lvl)
        return
    elif isinstance(modelpaststg_model_ids, str) or isinstance(modelpaststg_model_ids, basestring):
        # ensure we have a list for 'modelforestg_model_ids' variable
        modelpaststg_model_ids = [modelpaststg_model_ids]
    elif modelforestg_model_ids is None:
        Debug.dl("rpcbupd_hydrographmultiplesalert: Needs at least one 'modelforestg' model.", 0, debug_lvl)
        return
    elif isinstance(modelforestg_model_ids, str) or isinstance(modelforestg_model_ids, basestring):
        # ensure we have a list for 'modelforestg_model_ids' variable
        modelforestg_model_ids = [modelforestg_model_ids]

    # replace files for 'modelpaststg' frame
    for modelpaststg_model_id in modelpaststg_model_ids:
        modelpaststg_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id, sc_modelcomb_id,
                                                                                            represcomb_id=sc_reprcomp_id,
                                                                                            frame_id="modelpaststg",
                                                                                            model_id=modelpaststg_model_id)
        if clean_previous and os.path.exists(modelpaststg_dest_folder_path):
            shutil.rmtree(modelpaststg_dest_folder_path)
        os.makedirs(modelpaststg_dest_folder_path)
        modelpaststg_source_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id,
                                                                                               represcomb_id=sc_reprcomp_id,
                                                                                               frame_id="modelpaststg",
                                                                                               model_id=modelpaststg_model_id)
        if not os.path.exists(modelpaststg_source_folder_path):
            Debug.dl("rpcbupd_hydrographmultiplespast: Folder '{0}' not found.".format(modelpaststg_source_folder_path),
                     1, debug_lvl)
            return
        all_modelpaststg_hist_files = os.listdir(modelpaststg_source_folder_path)
        for cur_modelpaststg_hist_file_name in all_modelpaststg_hist_files:
            cur_modelpaststg_hist_file_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_modelpaststg_hist_file_name)
            if cur_modelpaststg_hist_file_timestamp == ref0_timestamp:
                cur_file_path = os.path.join(modelpaststg_source_folder_path, cur_modelpaststg_hist_file_name)
                shutil.copy(cur_file_path, modelpaststg_dest_folder_path)

        Debug.dl("rpcbupd_hydrographmultiplesalert: Filled '{0}' folder.".format(modelpaststg_dest_folder_path), 1, debug_lvl)

    # replace files for 'modelforestg' frame models
    min_timestamp_limit = ref0_timestamp - 3600
    max_timestamp_limit = ref0_timestamp + 3600
    for cur_modelforestg_model_id in modelforestg_model_ids:
        modelforestg_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id,
                                                                                            sc_modelcomb_id,
                                                                                            represcomb_id=sc_reprcomp_id,
                                                                                            frame_id="modelforestg",
                                                                                            model_id=cur_modelforestg_model_id)
        if clean_previous and os.path.exists(modelforestg_dest_folder_path):
            shutil.rmtree(modelforestg_dest_folder_path)
        os.makedirs(modelforestg_dest_folder_path)
        modelforestg_source_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id,
                                                                                               represcomb_id=sc_reprcomp_id,
                                                                                               frame_id="modelforestg",
                                                                                               model_id=cur_modelforestg_model_id)
        all_modelforestg_hist_files = os.listdir(modelforestg_source_folder_path)
        for cur_modelforestg_hist_file_name in all_modelforestg_hist_files:
            cur_modelforestg_hist_file_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_modelforestg_hist_file_name)
            if (cur_modelforestg_hist_file_timestamp >= min_timestamp_limit) and \
                    (cur_modelforestg_hist_file_timestamp <= max_timestamp_limit):
                cur_file_path = os.path.join(modelforestg_source_folder_path, cur_modelforestg_hist_file_name)
                shutil.copy(cur_file_path, modelforestg_dest_folder_path)

        Debug.dl("rpcbupd_hydrographmultiplesalert: Filled '{0}' folder.".format(modelforestg_dest_folder_path), 1,
                 debug_lvl)

    if modelforestgalert_model_ids is not None:
        if isinstance(modelforestgalert_model_ids, basestring):
            modelforestgalert_model_ids = [modelforestgalert_model_ids]
        min_timestamp_limit = ref0_timestamp - 3600
        max_timestamp_limit = ref0_timestamp + 3600
        for cur_modelforestg_model_id in modelforestgalert_model_ids:
            modelforestg_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(sc_runset_id,
                                                                                                sc_modelcomb_id,
                                                                                                represcomb_id=sc_reprcomp_id,
                                                                                                frame_id="modelforestgalert",
                                                                                                model_id=cur_modelforestg_model_id)
            if clean_previous and os.path.exists(modelforestg_dest_folder_path):
                shutil.rmtree(modelforestg_dest_folder_path)
            os.makedirs(modelforestg_dest_folder_path)
            modelforestg_source_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(sc_runset_id,
                                                                                                   represcomb_id=sc_reprcomp_id,
                                                                                                   frame_id="modelforestgalert",
                                                                                                   model_id=cur_modelforestg_model_id)
            all_modelforestg_hist_files = os.listdir(modelforestg_source_folder_path)
            for cur_modelforestg_hist_file_name in all_modelforestg_hist_files:
                cur_modelforestg_hist_file_timestamp = FileDefinition.obtain_hist_file_timestamp(cur_modelforestg_hist_file_name)
                if (cur_modelforestg_hist_file_timestamp >= min_timestamp_limit) and \
                        (cur_modelforestg_hist_file_timestamp <= max_timestamp_limit):
                    cur_file_path = os.path.join(modelforestg_source_folder_path, cur_modelforestg_hist_file_name)
                    shutil.copy(cur_file_path, modelforestg_dest_folder_path)

            Debug.dl("rpcbupd_hydrographmultiplesalert: Filled '{0}' folder.".format(modelforestg_dest_folder_path), 1,
                     debug_lvl)

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

    Debug.dl("rpcbupd_hydrographmultiplesalert: Filled '{0}' folder.".format(common_dest_folder_path), 1, debug_lvl)

# ####################################################### CALL ####################################################### #

update_display_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
