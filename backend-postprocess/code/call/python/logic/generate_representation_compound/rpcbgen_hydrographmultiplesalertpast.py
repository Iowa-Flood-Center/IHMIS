import numpy as np
import pickle
import time
import json
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.ReprCombGenInterface import ReprCombGenInterface
from libs.FolderDefinition import FolderDefinition
from libs.MetaFileManager import MetaFileManager
from libs.FileDefinition import FileDefinition
from libs.BinaryLibrary import BinaryLibrary
from libs.GeneralUtils import GeneralUtils
from libs.Hydrographs import Hydrographs
from libs.Debug import Debug

debug_level_arg = 9

# ####################################################### ARGS ####################################################### #

modelcomb_id_arg = ReprCombGenInterface.get_modelcomb_id(sys.argv)
runset_id_arg = ReprCombGenInterface.get_runset_id(sys.argv)
timestamp_arg = ReprCombGenInterface.get_timestamp(sys.argv)  # last expected observation, first forecast data
timestamp_min_arg = ReprCombGenInterface.get_min_timestamp_hist(sys.argv)  # graph forced minimum interval
timestamp_max_arg = ReprCombGenInterface.get_max_timestamp_hist(sys.argv)  # graph forced maximum interval


# ####################################################### DEFS ####################################################### #

class GlobalVar:
    represcomb_id = "hydrographmultiplesalertpast"
    days_past = 10
    days_fore = 10
    timestep = 3600  # in seconds between images

    def __init__(self):
        return


def generate_files(modelcomb_id, runset_id, timestamp, timestamp_min, timestamp_max, debug_lvl=0):
    """

    :param modelcomb_id:
    :param runset_id:
    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return:
    """

    represcomb_id = GlobalVar.represcomb_id

    # get all model comb file
    modelcomb_file_path = FileDefinition.obtain_modelcomb_file_path(modelcomb_id, runset_id, debug_lvl=debug_lvl)
    if (modelcomb_file_path is None) or (not os.path.exists(modelcomb_file_path)):
        Debug.dl("rpcbgen_hydrographmultiplesalert: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return

    # read file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbgen_hydrographmultiplesalert: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbgen_hydrographmultiplesalert: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".format(
            runset_id, modelcomb_id, represcomb_id), 0, debug_lvl)
        return

    # load common files
    all_stage_thresholds = Hydrographs.get_all_threshold(debug_lvl=debug_lvl)
    linkid_poisall_dict = Hydrographs.get_linkid_poisall_relationship(debug_lvl=debug_lvl)

    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info()

    #
    frame_set = represcomb_set[represcomb_id]
    link_ids = []
    the_links_alert = None
    any_alert = has_any_alert(frame_set)
    for cur_model_id in frame_set.keys():
        # generate all intermediate files
        if frame_set[cur_model_id] == "modelpaststg":
            print("No alert me: {0}".format(cur_model_id))
            cur_added_link_ids, cur_links_alert = generate_modelpaststg_stuff(cur_model_id, runset_id,
                                                                              linkid_poisall_dict, meta_mng,
                                                                              any_alert=any_alert,
                                                                              timestamp=timestamp,
                                                                              timestamp_min=timestamp_min,
                                                                              timestamp_max=timestamp_max,
                                                                              debug_lvl=debug_lvl)
        elif frame_set[cur_model_id] == "modelpaststgalert":
            print("Alert me: {0}".format(cur_model_id))
            cur_added_link_ids, cur_links_alert = generate_modelpaststg_stuff(cur_model_id, runset_id,
                                                                              linkid_poisall_dict, meta_mng,
                                                                              any_alert=any_alert,
                                                                              timestamp=timestamp,
                                                                              timestamp_min=timestamp_min,
                                                                              timestamp_max=timestamp_max,
                                                                              stage_thresholds=all_stage_thresholds,
                                                                              debug_lvl=debug_lvl)
        elif frame_set[cur_model_id] == "modelforestg":
            cur_added_link_ids, cur_links_alert = generate_modelforestg_stuff(cur_model_id, runset_id, meta_mng,
                                                                              timestamp, timestamp_min, timestamp_max,
                                                                              any_alert=any_alert,
                                                                              stage_thresholds=None,
                                                                              debug_lvl=debug_lvl)
        elif frame_set[cur_model_id] == "modelforestgalert":
            cur_added_link_ids, cur_links_alert = generate_modelforestg_stuff(cur_model_id, runset_id, meta_mng,
                                                                              timestamp, timestamp_min, timestamp_max,
                                                                              any_alert=any_alert,
                                                                              stage_thresholds=all_stage_thresholds,
                                                                              debug_lvl=debug_lvl)
        else:
            Debug.dl("rpcbgen_hydrographmultiplesalert: Unexpected frame '{0}' for model '{1}.{2}'.".format(
                frame_set[cur_model_id], runset_id, cur_model_id), 1, debug_lvl)
            continue

        # get together all link ids created
        for cur_added_link_id in cur_added_link_ids:
            if cur_added_link_id not in link_ids:
                link_ids.append(cur_added_link_id)

        if cur_links_alert is None:
            the_links_alert = the_links_alert
        else:
            if the_links_alert is None:
                the_links_alert = cur_links_alert
            else:
                if cur_model_id.endswith("ref"):
                    for cur_link_id in cur_links_alert.keys():
                        the_links_alert[cur_link_id] = cur_links_alert[cur_link_id]
                else:
                    for cur_link_id in cur_links_alert.keys():
                        if cur_link_id not in the_links_alert.keys():
                            the_links_alert[cur_link_id] = cur_links_alert[cur_link_id]

    # gages / virtual if necessary
    if not any_alert:
        if the_links_alert is not None:
            for cur_link_id in link_ids:
                if cur_link_id not in the_links_alert.keys():
                    the_links_alert[cur_link_id] = -5
        else:
            the_links_alert = {}
            for cur_link_id in link_ids:
                the_links_alert[cur_link_id] = -5

    # create / update common files
    out_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                           represcomb_id=GlobalVar.represcomb_id,
                                                                           frame_id="common")
    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)
    for cur_link_id in link_ids:
        create_common_file(out_folder_path, cur_link_id, all_stage_thresholds, the_links_alert, debug_lvl=debug_lvl)


def has_any_alert(frame_set):
    """
    Check if there is any alert frame
    :param frame_set:
    :return: Boolean.
    """

    for cur_frame in frame_set.values():
        if cur_frame.endswith("alert"):
            print("---Found alert in '{0}' at {1}".format(cur_frame, frame_set.values()))
            return True
    print("---Not found alert in '{0}'".format(frame_set.values()))
    return False


def generate_modelpaststg_stuff(model_id, runset_id, all_usgs_rc, meta_mng, any_alert=False, timestamp=None,
                                timestamp_min=None, timestamp_max=None, stage_thresholds=None, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param all_usgs_rc:
    :param meta_mng:
    :param any_alert:
    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param stage_thresholds:
    :param debug_lvl:
    :return: List of added link ids
    """

    prod_id = "istg"

    added_link_ids = []

    if any_alert and (stage_thresholds is None):
        alert_links = None
    elif (not any_alert) and model_id.endswith("ref"):
        alert_links = {}
    elif any_alert and (stage_thresholds is not None):
        alert_links = {}
    else:
        alert_links = None

    # define frame id
    the_frame_id = "modelpaststg" if stage_thresholds is None else "modelpaststgalert"

    Debug.dl("rpcbgen_hydrographmultiplesalert: Processing 'modelpaststg' for model '{0}.{1}'.".format(runset_id,
                                                                                                       model_id),
             4, debug_lvl)

    # define output folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                          represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id=the_frame_id, model_id=model_id)
    if not os.path.exists(outfolder_path):
        os.makedirs(outfolder_path)

    # import information
    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=prod_id,
                                                                             runset_id=runset_id)
    # TODO - use proper def_sys commands
    mdl_prod_file_path_frame = os.path.join(mdl_prod_folder_path, "{0}{1}.p")
    Debug.dl("rpcbgen_hydrographmultiplesalert: Reading modeled data from '{0}'.".format(mdl_prod_folder_path), 1,
             debug_lvl)

    # define timestamps
    the_timestamps = define_timestamps(timestamp=timestamp, timestamp_min=timestamp_min, timestamp_max=timestamp_max,
                                       debug_lvl=debug_lvl)
    the_timestamp_min = the_timestamps[0]
    the_timestamp_mid = the_timestamps[1]

    #
    data_dictionary = {}

    # read all files and obtain discharge raw data
    for cur_timestamp in range(the_timestamp_min, the_timestamp_mid, GlobalVar.timestep):

        # define the file
        cur_effect_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                         cur_timestamp,
                                                                                         accept_range=29*60,
                                                                                         debug_lvl=debug_lvl)
        cur_prod_file_path = mdl_prod_file_path_frame.format(cur_effect_timestamp, prod_id)

        if cur_effect_timestamp is None:
            Debug.dl("rpcbgen_hydrographmultiplesalert: No file for '{0}'.".format(cur_timestamp), 19, debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_hydrographmultiplesalert: Considering file '{0}'.".format(cur_prod_file_path), 19,
                     debug_lvl)

        # read file
        with open(cur_prod_file_path, "rb") as r_file_mdl:
            cur_mdl_content = np.load(r_file_mdl)

        for cur_link_id in cur_mdl_content.keys():
            added_pair = cur_timestamp, cur_mdl_content[cur_link_id]
            if cur_link_id not in data_dictionary:
                data_dictionary[cur_link_id] = []
            data_dictionary[cur_link_id].append(added_pair)

    # check the last stage of each link with respect to the thresholds
    if alert_links is not None:
        for cur_link_id in data_dictionary.keys():
            if any_alert:
                cur_flood_level = define_flood_level(stage_thresholds, cur_link_id, model_id,
                                                     any_alert, data_dictionary, debug_lvl=debug_lvl)
                if cur_flood_level is not None:
                    alert_links[cur_link_id] = cur_flood_level
            else:
                alert_links[cur_link_id] = -6

    # write each file converting discharge to stage
    for cur_link_id in data_dictionary.keys():
        # basic check
        if (cur_link_id not in cur_mdl_content.keys()) or (cur_link_id == 0):
            continue

        # write file, converting rating curve
        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(the_timestamp_mid, cur_link_id))
        with open(out_file_path, "w+") as wfile:
            json.dump({"stage_mdl": data_dictionary[cur_link_id]}, wfile)
        added_link_ids.append(cur_link_id)
        Debug.dl("rpcbgen_hydrographmultiplesalert: Wrote file '{0}'.".format(out_file_path), 1, debug_lvl)

    return added_link_ids, alert_links


def define_flood_level(stage_thresholds_dict, link_id, sc_model_id, any_alert, data_dictionary,
                       debug_lvl=0):
    """

    :param stage_thresholds_dict:
    :param link_id:
    :param sc_model_id:
    :param current_flood_level:
    :param any_alert:
    :param data_dictionary:
    :param debug_lvl:
    :return:
    """

    flood_level = None

    if stage_thresholds_dict is not None:
        if link_id in stage_thresholds_dict["links"]:
            if stage_thresholds_dict["links"][link_id]["type"] == "elevation":
                for cur_pair in data_dictionary[link_id]:
                    if (stage_thresholds_dict["links"][link_id]["thresholds"]["fld_action"] != -1) and \
                            (flood_level <= 1) and \
                            (cur_pair[1] > stage_thresholds_dict["links"][link_id]["thresholds"]["fld_action"]):
                        flood_level = 1
                    if (stage_thresholds_dict["links"][link_id]["thresholds"]["fld_flood"] != -1) and \
                            (flood_level <= 2) and \
                            (cur_pair[1] > stage_thresholds_dict["links"][link_id]["thresholds"]["fld_flood"]):
                        flood_level = 2
                    if (stage_thresholds_dict["links"][link_id]["thresholds"]["fld_moderate"] != -1) and \
                            (flood_level <= 3) and \
                            (cur_pair[1] > stage_thresholds_dict["links"][link_id]["thresholds"]["fld_moderate"]):
                        flood_level = 3
                    if (stage_thresholds_dict["links"][link_id]["thresholds"]["fld_major"] != -1) and \
                            (flood_level <= 4) and \
                            (cur_pair[1] > stage_thresholds_dict["links"][link_id]["thresholds"]["fld_major"]):
                        flood_level = 4
            else:
                Debug.dl("rpcbgen_hydrographmultiplesalert: unexpected threshold type '{0}'.".format(
                    stage_thresholds_dict["links"][link_id]["type"]), 1, debug_lvl)
        else:
            Debug.dl("rpcbgen_hydrographmultiplesalert: link {0} not among thresholds.".format(link_id), 4, debug_lvl)
            flood_level = 0
    else:
        if (not any_alert) and sc_model_id.endswith("ref"):
            flood_level = -6

    return flood_level


def generate_modelforestg_stuff(model_id, runset_id, meta_mng, timestamp, timestamp_min, timestamp_max,
                                any_alert=False, stage_thresholds=None, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param meta_mng:
    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param stage_thresholds: If None, ignore alerts.
    :param debug_lvl:
    :return: List of added link ids
    """

    prod_id = "fsstg"
    frame_id = "modelforestg" if stage_thresholds is None else "modelforestgalert"

    added_link_ids = []
    alert_links = None if stage_thresholds is None else {}
    Debug.dl("rpcbgen_hydrographmultiplesalert: Processing 'modelforestg' for model '{0}.{1}'.".format(runset_id,
                                                                                                       model_id),
             4, debug_lvl)

    # import information
    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=prod_id,
                                                                             runset_id=runset_id)
    # TODO - use proper def_sys commands
    mdl_prod_file_path_frame = os.path.join(mdl_prod_folder_path, "{0}{1}.p")
    Debug.dl("rpcbgen_hydrographmultiplesalert: reading modeled data from '{0}'.".format(mdl_prod_folder_path), 1,
             debug_lvl)

    # define timestamps
    the_timestamps = define_timestamps(timestamp=timestamp, timestamp_min=timestamp_min, timestamp_max=timestamp_max,
                                       debug_lvl=debug_lvl)
    the_timestamp_mid = the_timestamps[1]
    the_timestamp_max = the_timestamps[2]

    effect_timestamp_mid = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                     the_timestamp_mid,
                                                                                     accept_range=120*60,
                                                                                     debug_lvl=debug_lvl)
    # basic check
    if effect_timestamp_mid is None:
        Debug.dl("rpcbgen_hydrographmultiplesalert: not a file close enough to '{0}' for '{1}.{2}.{3}'.".format(
            the_timestamp_mid, runset_id, model_id, prod_id), 1, debug_lvl)
        return added_link_ids, alert_links

    mdl_prod_file_path = mdl_prod_file_path_frame.format(effect_timestamp_mid, prod_id)

    # print("Using file '{0}' (closest to {1}).".format(mdl_prod_file_path, the_timestamp_mid))

    with open(mdl_prod_file_path, 'r') as rfile:
        data_dictionary = pickle.load(rfile)

    # define folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id, represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id=frame_id, model_id=model_id)
    if not os.path.exists(outfolder_path):
        os.makedirs(outfolder_path)

    for cur_link_id in data_dictionary.keys():

        # add each value to the list
        cur_stg = []
        flood_level = 0  # 0:no flood, 1:alert, 2:flood, 3:moderate, 4:major
        for cur_pair in data_dictionary[cur_link_id]:
            # add to list
            cur_stg.append([cur_pair[0], cur_pair[1]])
            # check for alert
            if stage_thresholds is not None:
                if cur_link_id in stage_thresholds["links"]:
                    if stage_thresholds["links"][cur_link_id]["type"] == "elevation":
                        # print("...{0}...".format(stage_thresholds["links"][cur_link_id].keys()))
                        if (stage_thresholds["links"][cur_link_id]["thresholds"]["fld_action"] != -1) and \
                                (flood_level <= 1) and \
                                (cur_pair[1] > stage_thresholds["links"][cur_link_id]["thresholds"]["fld_action"]):
                            flood_level = 1
                        if (stage_thresholds["links"][cur_link_id]["thresholds"]["fld_flood"] != -1) and \
                                (flood_level <= 2) and \
                                (cur_pair[1] > stage_thresholds["links"][cur_link_id]["thresholds"]["fld_flood"]):
                            flood_level = 2
                        if (stage_thresholds["links"][cur_link_id]["thresholds"]["fld_moderate"] != -1) and \
                                (flood_level <= 3) and \
                                (cur_pair[1] > stage_thresholds["links"][cur_link_id]["thresholds"]["fld_moderate"]):
                            flood_level = 3
                        if (stage_thresholds["links"][cur_link_id]["thresholds"]["fld_major"] != -1) and \
                                (flood_level <= 4) and \
                                (cur_pair[1] > stage_thresholds["links"][cur_link_id]["thresholds"]["fld_major"]):
                            flood_level = 4

        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(effect_timestamp_mid, cur_link_id))
        with open(out_file_path, "w+") as wfile:
            json.dump({"stage_mdl": cur_stg}, wfile)

        added_link_ids.append(cur_link_id)
        if alert_links is not None:
            alert_links[cur_link_id] = flood_level
        Debug.dl("rpcbgen_hydrographmultiplesalert: Writing file '{0}'.".format(out_file_path), 3, debug_lvl)

    return added_link_ids, alert_links


def create_common_file(output_folder_path, link_id, all_stage_thresholds, cur_links_alert, debug_lvl=0):
    """

    :param output_folder_path:
    :param link_id:
    :param all_stage_thresholds:
    :param cur_links_alert:
    :param debug_lvl:
    :return:
    """

    # build content
    build_object = {}

    # build content - thresholds
    if link_id in all_stage_thresholds["links"].keys():
        thresholds = all_stage_thresholds["links"][link_id]["thresholds"]
        print("Link id {0} found on thresholds.".format(link_id))
        # build_object["thresholds"] = thresholds
        try:
            build_object['stage_threshold_act'] = thresholds["fld_action"]    # thresholds of DOT gages are in ft
            build_object['stage_threshold_fld'] = thresholds["fld_flood"]     # thresholds of DOT gages are in ft
            build_object['stage_threshold_mod'] = thresholds["fld_moderate"]  # thresholds of DOT gages are in ft
            build_object['stage_threshold_maj'] = thresholds["fld_major"]     # thresholds of DOT gages are in ft
        except TypeError:
            Debug.dl("rpcbgen_hydrographmultiplesalert: Some stage thresholds for link_id {0} is missing.".format(
                link_id), 2, debug_lvl)

    # write file
    file_name = "{0}.json".format(link_id)
    file_path = os.path.join(output_folder_path, file_name)
    if link_id in cur_links_alert:
        build_object["fld_level"] = cur_links_alert[link_id]
    else:
        Debug.dl("rpcbgen_hydrographmultiplesalert: Link {0} not in list of alerts.".format(link_id), 2, debug_lvl)
        build_object["fld_level"] = 0
    with open(file_path, "w+") as wfile:
        if cur_links_alert is not None:
            json.dump(build_object, wfile)
        else:
            json.dump({"It is": "empty"}, wfile)

    Debug.dl("rpcbgen_hydrographmultiplesalert: Wrote file '{0}'.".format(file_path), 3, debug_lvl)

    return


def define_timestamps(timestamp=None, timestamp_min=None, timestamp_max=None, debug_lvl=0):
    """

    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return: Three values: min timestamp, mid timestamp, max timestamp (in this sequence)
    """

    the_timestamp_max = None
    the_timestamp_min = None
    the_timestamp_mid = None

    # define intervals
    if (timestamp is None) and (timestamp_min is None) and (timestamp_max is None):
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(time.time())
        the_timestamp_min = the_timestamp_mid - (GlobalVar.days_past * 24 * 60 * 60)
        the_timestamp_max = the_timestamp_mid + (GlobalVar.days_fore * 24 * 60 * 60)
    elif (timestamp is None) and (timestamp_min is not None) and (timestamp_max is not None):
        # basic check
        if not (timestamp_max > timestamp_min):
            Debug.dl("rpcbgen_hydrographmultiplesalert: invalid timestamps: min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        the_timestamp_min = GeneralUtils.truncate_timestamp_hour(timestamp_min)
        the_timestamp_max = GeneralUtils.truncate_timestamp_hour(timestamp_max)
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(int((timestamp_max - timestamp_min)/2))
    elif (timestamp is not None) and (timestamp_min is not None) and (timestamp_max is not None):
        # basic check
        if not (timestamp_max > timestamp_min):
            Debug.dl("rpcbgen_hydrographmultiplesalert: invalid timestamps - min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        elif not ((timestamp_max > timestamp) and (timestamp > timestamp_min)):
            Debug.dl("rpcbgen_hydrographmultiplesalert: invalid timestamps sequence - not ({0} > {1} > {2})'.".format(
                timestamp_min, timestamp, timestamp_max), 1, debug_lvl)
            return
        the_timestamp_min = GeneralUtils.truncate_timestamp_hour(timestamp_min)
        the_timestamp_max = GeneralUtils.truncate_timestamp_hour(timestamp_max)
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(timestamp)
    elif (timestamp is not None) and (timestamp_min is None) and (timestamp_max is None):
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(timestamp)
        the_timestamp_min = the_timestamp_mid - (GlobalVar.days_past * 24 * 60 * 60)
        the_timestamp_max = the_timestamp_mid - (GlobalVar.days_past * 24 * 60 * 60)
    else:
        Debug.dl("rpcbgen_hydrographmultiplesalert: unexpected timestamp informations - min:{0}, mid:{1}, max:{2}'.".format(
                timestamp, timestamp_min, timestamp_max), 1, debug_lvl)
        return

    return the_timestamp_min, the_timestamp_mid, the_timestamp_max

# ####################################################### CALL ####################################################### #

generate_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, timestamp_min_arg, timestamp_max_arg,
               debug_lvl=debug_level_arg)
