from json import encoder
import numpy as np
import pickle
import math
import time
import glob
import json
import sys
import os
import re

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.ReprCombGenInterface import ReprCombGenInterface
from libs.FilenameDefinition import FilenameDefinition
from libs.FolderDefinition import FolderDefinition
from libs.MetaFileManager import MetaFileManager
from libs.MetaFileManager import MetaFileManager
from libs.FileDefinition import FileDefinition
from libs.BinaryLibrary import BinaryLibrary
from libs.GeneralUtils import GeneralUtils
from libs.Hydrographs import Hydrographs
from libs.Interpolate import Interpolate
from libs.Debug import Debug

debug_level_arg = 4

# ####################################################### ARGS ####################################################### #

modelcomb_id_arg = ReprCombGenInterface.get_modelcomb_id(sys.argv)
runset_id_arg = ReprCombGenInterface.get_runset_id(sys.argv)
timestamp_arg = ReprCombGenInterface.get_timestamp(sys.argv)  # last expected observation, first forecast data
timestamp_min_arg = ReprCombGenInterface.get_min_timestamp_hist(sys.argv)  # graph forced minimum interval
timestamp_max_arg = ReprCombGenInterface.get_max_timestamp_hist(sys.argv)  # graph forced maximum interval


# ####################################################### DEFS ####################################################### #

class GlobalVar:
    represcomb_id = "bestrmsforecasted"
    days_past_max = 10  # replace by 10
    timestep = 3600  # in seconds between images

    def __init__(self):
        return


def try_calculate_rms(link_id, models_series, reference_series):
    """

    :param link_id:
    :param models_series:
    :param reference_series:
    :return: Dictionary with {models:{model_a:value_a, model_b:value_b}, valid_points:value
    """

    # basic check 1
    if link_id not in reference_series.keys():
        return None, None

    # basic check 2
    if (models_series is None) or (len(models_series.keys()) == 0):
        return diagnose_site(link_id, models_series, reference_series, "No models set up for this site.")

    # basic check 3
    link_ref_timeseries = reference_series[link_id]
    if len(link_ref_timeseries.keys()) == 0:
        diagnose_site(link_id, models_series, reference_series, "Empty reference data for this site.")

    # establish all common timestamps
    valid_timestamps = []
    for cur_timestamp in link_ref_timeseries.keys():
        cur_flag = True
        for cur_model_timeserie in models_series.values():
            if cur_timestamp not in cur_model_timeserie[link_id].keys():
                cur_flag = False
                break
        if cur_flag:
            valid_timestamps.append(cur_timestamp)

    # basic check 4
    if len(valid_timestamps) == 0:
        return diagnose_site(link_id, models_series, reference_series, "Unable to find matching timestamps.")
    elif len(valid_timestamps) == 1:
        return diagnose_site(link_id, models_series, reference_series, "Not enough matching timestamps ({0}).".format(
            len(valid_timestamps)))

    return calculate_rms(link_id, models_series, link_ref_timeseries, valid_timestamps)


def calculate_rms(link_id, models_series, link_ref_timeseries, valid_timestamps):
    """

    :param link_id:
    :param models_series:
    :param link_ref_timeseries:
    :param valid_timestamps:
    :return:
    """

    # open output obj
    out_dict = {
        "models": {},
        "timestamp_max": max(valid_timestamps),
        "timestamp_min": min(valid_timestamps),
        "num_points": len(valid_timestamps),
        "success": True}

    # calculate rms for each one
    max_r, min_r = None, None
    for cur_model_id, cur_model_dict in models_series.items():
        cur_sum = 0
        for cur_t in valid_timestamps:
            cur_r = link_ref_timeseries[cur_t] * 0.0833333               # from in to ft
            cur_m = cur_model_dict[link_id][cur_t]
            if None in (cur_r, cur_m):
                return None, None
            cur_s = (cur_r - cur_m) ** 2
            cur_sum += cur_s
            max_r = cur_r if (max_r is None) or (max_r < cur_r) else max_r
            min_r = cur_r if (min_r is None) or (min_r > cur_r) else min_r
        cur_rmse = math.sqrt(cur_sum/len(valid_timestamps))
        if max_r == min_r:
            continue
        cur_rmse /= max_r - min_r
        out_dict["models"][cur_model_id] = cur_rmse

    return out_dict, max(valid_timestamps)


def diagnose_site(link_id, models_series, reference_series, comment=None):
    """

    :param link_id:
    :param models_series:
    :param reference_series:
    :param comment:
    :return:
    """

    # create output dictionary
    out_dict = {"diagnosis": {"models": {},
                              "reference": {},
                              "comment": comment},
                "success": False}
    timestamp_max = None

    # set reference data:
    if link_id in reference_series.keys():
        link_ref_timestamps = reference_series[link_id].keys()
        cur_num_points = len(link_ref_timestamps)
        cur_time_min = min(link_ref_timestamps) if (cur_num_points > 0) else None
        cur_time_max = max(link_ref_timestamps) if (cur_num_points > 0) else None
        out_dict["diagnosis"]["reference"]["timestamp_min"] = cur_time_min
        out_dict["diagnosis"]["reference"]["timestamp_max"] = cur_time_max
        out_dict["diagnosis"]["reference"]["num_points"] = cur_num_points
        timestamp_max = cur_time_max if (cur_time_max is None) or (timestamp_max < cur_time_max) else timestamp_max

    # set modules data
    if (models_series is not None) and (len(models_series.keys()) > 0):
        for cur_model_id, cur_model_dict in models_series.items():
            cur_num_points = len(cur_model_dict[link_id])
            cur_time_min = min(cur_model_dict[link_id].keys()) if cur_num_points > 0 else None
            cur_time_max = max(cur_model_dict[link_id].keys()) if cur_num_points > 0 else None
            out_dict["diagnosis"]["models"][cur_model_id] = {
                "timestamp_min": cur_time_min,
                "timestamp_max": cur_time_max,
                "num_points": cur_num_points}
        timestamp_max = cur_time_max if (cur_time_max is None) or (timestamp_max < cur_time_max) else timestamp_max

    return out_dict, timestamp_max


def generate_cache_files(modelcomb_id, runset_id, timestamp, timestamp_min, timestamp_max, debug_lvl=0):
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
        Debug.dl("rpcbgen_bestrmsforecasted: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return

    # read meta file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbgen_bestrmsforecasted: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbgen_bestrmsforecasted: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".format(
            runset_id, modelcomb_id, represcomb_id), 0, debug_lvl)
        return

    # load common files
    linkid_poisall_dict = Hydrographs.get_linkid_poisall_relationship(debug_lvl=debug_lvl)
    all_usgs_rc = Hydrographs.get_all_usgs_rating_curves(debug_lvl=debug_lvl)

    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info()
    meta_mng.load_all_screference_meta_info()

    # read all files and load only necessary data
    frame_set = represcomb_set[represcomb_id]
    round_timestamp, timestamp_dict = define_launch_date(frame_set, "fq", runset_id)

    # basic check
    if None in (round_timestamp, timestamp_dict):
        Debug.dl("rpcbgen_bestrmsforecasted: Unable to define a common launching timestamp.", 1, debug_lvl)
        return

    # read the data to be processed
    models_dict = {}
    ref_dict = None
    for cur_model_id in frame_set.keys():
        # generate all intermediate files
        if frame_set[cur_model_id] == "modelforedsc":

            cur_dict = get_modelforedsc_stuff(cur_model_id, runset_id, linkid_poisall_dict,
                                              all_usgs_rc, meta_mng, timestamp=timestamp_dict[cur_model_id],
                                              debug_lvl=debug_lvl)
            if cur_dict is None:
                continue
            models_dict[cur_model_id] = cur_dict

        elif frame_set[cur_model_id] == "stageref":
            ref_dict = get_stageref_stuff(cur_model_id, runset_id, all_usgs_rc, meta_mng, round_timestamp,
                                          timestamp_min, timestamp_max, debug_lvl=debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_bestrmsforecasted: Unexpecteds frame '{0}' for model '{1}.{2}'.".format(
                frame_set[cur_model_id], runset_id, cur_model_id), 1, debug_lvl)
            continue

    # basic check
    if ref_dict is None:
        Debug.dl("rpcbgen_bestrmsforecasted: Unable to process. No reference information.", 1, debug_lvl)
        return

    # define / create output folder
    out_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                           represcomb_id=GlobalVar.represcomb_id)

    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)
        Debug.dl("rpcbgen_bestrmsforecasted: Created folder '{0}'.".format(out_folder_path), 1, debug_lvl)

    # process rms pondered and write output file
    out_dict = {}
    skipped_links = 0
    for cur_link_id in all_usgs_rc.keys():
        out_dict[cur_link_id], max_timestamp = try_calculate_rms(cur_link_id, models_dict, ref_dict)

        # basic check
        if None in (out_dict[cur_link_id], max_timestamp):
            skipped_links += 1
            continue

        # define file name and path
        cur_file_name = "{0}_{1}.json".format(max_timestamp, cur_link_id)
        cur_file_path = os.path.join(out_folder_path, cur_file_name)

        # save file
        with open(cur_file_path, "w+") as r_file:
            json.dump(out_dict[cur_link_id], r_file)
        Debug.dl("rpcbgen_richhydroforecast: Wrote file '{0}'.".format(cur_file_path), 0, debug_lvl)

    Debug.dl("Skipped {0} out of {1} possible links.".format(skipped_links, len(all_usgs_rc.keys())), 0, debug_lvl)


def get_modelforedsc_stuff(model_id, runset_id, linkid_poisall_dict, all_usgs_rc, meta_mng, timestamp=None,
                           debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param debug_lvl:
    :return: List of added link ids
    """

    prod_id = "fq"

    Debug.dl("rpcbgen_bestrmsforecasted: Processing 'modelforedsc' for model '{0}.{1}'.".format(runset_id, model_id),
             4, debug_lvl)

    all_link_ids = all_usgs_rc.keys()

    #
    return_dictionary = {}  # this is the dictionary to be returned
    for cur_link_id in all_link_ids:
        return_dictionary[cur_link_id] = {}

    # read rating curve file and convert discharge to stage
    for cur_link_id in all_link_ids:
        # basic checks
        if cur_link_id is None:
            continue
        if cur_link_id not in return_dictionary.keys():
            continue

        cur_datadictionary = BinaryLibrary.get_timeseries_for_linkid_product(runset_id, model_id, prod_id,
                                                                             cur_link_id, timestamp_release=timestamp,
                                                                             debug_lvl=2)

        if cur_datadictionary is None:
            continue

        # get all disch and stages and convert
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        for cur_pair in cur_datadictionary:
            cur_timestamp, cur_disch = GeneralUtils.round_timestamp_hour(cur_pair[0]),  cur_pair[1]
            cur_stage = Interpolate.my_interpolation_xy(cur_dischs, cur_stages, cur_disch * 35.315)
            return_dictionary[cur_link_id][cur_timestamp] = cur_stage
            cur_timestamp += GlobalVar.timestep

    return return_dictionary


def get_stageref_stuff(reference_id, runset_id, all_usgs_rc, meta_mng, timestamp, timestamp_min, timestamp_max,
                       debug_lvl=0):
    """

    :param reference_id:
    :param runset_id:
    :param all_usgs_rc:
    :param meta_mng:
    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return: List of added link ids
    """

    prod_id = "istg"

    Debug.dl("rpcbgen_bestrmsforecasted: Processing 'stageref' for model '{0}.{1}'.".format(runset_id, reference_id),
             4, debug_lvl)

    # import information
    ref_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=reference_id, product_id=prod_id,
                                                                             runset_id=runset_id)

    all_link_ids = all_usgs_rc.keys()

    # this is the dictionary to be returned
    return_dictionary = {}

    for cur_link_id in all_link_ids:
        return_dictionary[cur_link_id] = {}

    for cur_prod_file_name in os.listdir(ref_prod_folder_path):
        # read file content
        cur_prod_file_path = os.path.join(ref_prod_folder_path, cur_prod_file_name)
        with open(cur_prod_file_path, 'r') as rfile:
            Debug.dl("rpcbgen_bestrmsforecasted: reading file '{0}'.".format(cur_prod_file_path), 5, debug_lvl)
            data_dictionary = pickle.load(rfile)

        for cur_link_id_l, cur_dict in data_dictionary.items():
            cur_link_id = int(cur_link_id_l)
            if cur_link_id not in return_dictionary.keys():
                continue
            for cur_timestamp, cur_stg in cur_dict.items():
                cur_round_timestamp = GeneralUtils.round_timestamp_hour(cur_timestamp)
                return_dictionary[cur_link_id][cur_round_timestamp] = cur_stg

    return return_dictionary


def define_launch_date(frame_set, sc_product_id, sc_runset_id):
    """

    :param frame_set:
    :param sc_product_id:
    :param sc_runset_id:
    :return: Integer and dictionary of model_id:effective_date
    """

    count_launch_dates = 0
    all_round_timestamps_count = {}

    # count the number of available data ets for each rounded timestamp
    for cur_model_id in frame_set.keys():
        # generate all intermediate files
        if frame_set[cur_model_id] == "modelforedsc":
            count_launch_dates += 1

            # import information
            mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=cur_model_id,
                                                                                     product_id=sc_product_id,
                                                                                     runset_id=sc_runset_id)
            for cur_prod_file_name in os.listdir(mdl_prod_folder_path):
                cur_file_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_prod_file_name)
                cur_file_round_timestamp = GeneralUtils.round_timestamp_hour(cur_file_timestamp)
                if cur_file_round_timestamp not in all_round_timestamps_count.keys():
                    all_round_timestamps_count[cur_file_round_timestamp] = {}
                all_round_timestamps_count[cur_file_round_timestamp][cur_model_id] = cur_file_timestamp

        else:
            continue

    # return rounded + model:timestamp
    for cur_timestamp in sorted(all_round_timestamps_count.keys()):
        if len(all_round_timestamps_count[cur_timestamp]) == count_launch_dates:
            return cur_timestamp, all_round_timestamps_count[cur_timestamp]

    return None, None


# ####################################################### CALL ####################################################### #

generate_cache_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, timestamp_min_arg, timestamp_max_arg,
                     debug_lvl=debug_level_arg)