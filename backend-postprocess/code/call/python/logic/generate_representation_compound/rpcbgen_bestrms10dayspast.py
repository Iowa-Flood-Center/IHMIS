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
    represcomb_id = "bestrms10dayspast"
    days_past = 0.33  # replace by 10
    days_fore = 3  # replace by 10
    timestep = 3600  # in seconds between images

    def __init__(self):
        return


def try_calculate_rms(link_id, models_series, reference_series):
    """

    :param link_id:
    :param models_series:
    :param reference_series:
    :return:
    """

    # basic check 1
    if link_id not in reference_series.keys():
        # diagnose_site(link_id, models_series, reference_series, "Missing reference data")
        return None, None

    # basic check 2
    if (models_series is None) or (len(models_series.keys()) == 0):
        return diagnose_site(link_id, models_series, reference_series, "No models set up for this site.")

    # basic check 3
    link_ref_timeseries = reference_series[link_id]
    if len(link_ref_timeseries.keys()) == 0:
        return diagnose_site(link_id, models_series, reference_series, "Empty reference data for this site.")

    # establish all common timestamps
    valid_timestamps = []
    for cur_timestamp in link_ref_timeseries.keys():
        cur_flag = True
        for cur_model_timeserie in models_series.values():
            cmtl = cur_model_timeserie[link_id]
            if (cur_timestamp not in cmtl.keys()) or (cur_model_timeserie[link_id][cur_timestamp] is None):
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


def calculate_rms(link_id, models_series, link_ref_timeseries, valid_timestamps):
    """

    :param link_id:
    :param models_series:
    :param link_ref_timeseries:
    :param valid_timestamps:
    :return: Dictionary with {models:{model_a:value_a, model_b:value_b}, num_points:value, ...} & current timestamp
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
            cur_s = (cur_r - cur_m) ** 2
            cur_sum += cur_s
            max_r = cur_r if (max_r is None) or (max_r < cur_r) else max_r
            min_r = cur_r if (min_r is None) or (min_r > cur_r) else min_r
        cur_rmse = math.sqrt(cur_sum/len(valid_timestamps))
        cur_rmse /= (max_r - min_r) if (max_r != min_r) else (max_r * 0.1)
        out_dict["models"][cur_model_id] = cur_rmse

    return out_dict, max(valid_timestamps)


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
        Debug.dl("rpcbgen_bestrms10dayspast: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return

    # read meta file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbgen_bestrms10dayspast: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbgen_bestrms10dayspast: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".format(
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
    models_dict = {}
    ref_dict = None
    for cur_model_id in frame_set.keys():
        # build intermediate dictionaries
        if frame_set[cur_model_id] == "modelpastdsc":

            cur_dict = get_modelpastdsc_stuff(cur_model_id, runset_id, linkid_poisall_dict,
                                              all_usgs_rc, meta_mng, timestamp=timestamp,
                                              timestamp_min=timestamp_min, timestamp_max=timestamp_max,
                                              debug_lvl=debug_lvl)
            if cur_dict is None:
                continue
            models_dict[cur_model_id] = cur_dict

        elif frame_set[cur_model_id] == "stageref":
            ref_dict = get_stageref_stuff(cur_model_id, runset_id, all_usgs_rc, meta_mng, timestamp,
                                          timestamp_min, timestamp_max, debug_lvl=debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_bestrms10dayspast: Unexpected frame '{0}' for model '{1}.{2}'.".format(
                frame_set[cur_model_id], runset_id, cur_model_id), 1, debug_lvl)
            continue

    # basic check
    if ref_dict is None:
        Debug.dl("rpcbgen_bestrms10dayspast: Unable to process. No reference information.", 1, debug_lvl)
        return

    # define / create output folder
    out_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                           represcomb_id=GlobalVar.represcomb_id)
    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)
        Debug.dl("rpcbgen_bestrms10dayspast: Created folder '{0}'.".format(out_folder_path), 1, debug_lvl)

    # process rms pondered and write output file
    out_dict = {}
    for cur_link_id in all_usgs_rc.keys():
        out_dict[cur_link_id], max_timestamp = try_calculate_rms(cur_link_id, models_dict, ref_dict)

        # basic check
        if None in (out_dict[cur_link_id], max_timestamp):
            continue

        # define file name and path
        cur_file_name = "{0}_{1}.json".format(max_timestamp, cur_link_id)
        cur_file_path = os.path.join(out_folder_path, cur_file_name)

        # save file
        with open(cur_file_path, "w+") as r_file:
            json.dump(out_dict[cur_link_id], r_file)
        Debug.dl("rpcbgen_richhydroforecast: Wrote file '{0}'.".format(cur_file_path), 0, debug_lvl)


def get_modelpastdsc_stuff(model_id, runset_id, linkid_poisall_dict, all_usgs_rc, meta_mng, timestamp=None,
                           timestamp_min=None, timestamp_max=None, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param debug_lvl:
    :return: List of added link ids
    """

    prod_id = "idq"

    Debug.dl("rpcbgen_bestrms10dayspast: Processing 'modelpastdsc' for model '{0}.{1}'.".format(runset_id, model_id),
             4, debug_lvl)

    # import information
    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=prod_id,
                                                                             runset_id=runset_id)

    all_link_ids = all_usgs_rc.keys()

    #
    return_dictionary = {}  # this is the dictionary to be returned
    for cur_link_id in all_link_ids:
        return_dictionary[cur_link_id] = {}

    # basic check
    if not os.path.exists(mdl_prod_folder_path):
        Debug.dl("rpcbgen_bestrms10dayspast: Folder '{0}' not found.".format(mdl_prod_folder_path), 4, debug_lvl)
        return None

    # read link id data timeseries
    for cur_prod_file_name in os.listdir(mdl_prod_folder_path):
        # read file content
        cur_mdl_content = np.load(os.path.join(mdl_prod_folder_path, cur_prod_file_name))
        cur_file_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_prod_file_name)
        cur_file_round_timestamp = GeneralUtils.round_timestamp_hour(cur_file_timestamp)

        # initially, gets all discharges
        for cur_link_id in all_link_ids:
            if (cur_link_id >= len(cur_mdl_content)) or (cur_link_id == 0):
                continue

            return_dictionary[cur_link_id][cur_file_round_timestamp] = cur_mdl_content[cur_link_id]

    # read rating curve file and convert discharge to stage
    for cur_link_id in all_link_ids:
        # basic check
        if cur_link_id not in return_dictionary.keys():
            continue

        # get all disch and stages and convert
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        for cur_timestamp, cur_disch in return_dictionary[cur_link_id].items():
            cur_stage = Interpolate.my_interpolation_xy(cur_dischs, cur_stages, cur_disch * 35.315)
            return_dictionary[cur_link_id][cur_timestamp] = cur_stage

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

    Debug.dl("rpcbgen_bestrms10dayspast: Processing 'stageref' for model '{0}.{1}'.".format(runset_id, reference_id),
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
            Debug.dl("rpcbgen_bestrms10dayspast: reading file '{0}'.".format(cur_prod_file_path), 5, debug_lvl)
            data_dictionary = pickle.load(rfile)

        for cur_link_id_l, cur_dict in data_dictionary.items():
            cur_link_id = int(cur_link_id_l)
            if cur_link_id not in return_dictionary.keys():
                continue
            for cur_timestamp, cur_stg in cur_dict.items():
                cur_round_timestamp = GeneralUtils.round_timestamp_hour(cur_timestamp)
                return_dictionary[cur_link_id][cur_round_timestamp] = cur_stg

    return return_dictionary


# ####################################################### CALL ####################################################### #

generate_cache_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, timestamp_min_arg, timestamp_max_arg,
                     debug_lvl=debug_level_arg)
