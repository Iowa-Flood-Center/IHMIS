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
    represcomb_id = "richhydroforecast"
    days_past = 0.33  # replace by 10
    days_fore = 3  # replace by 10
    timestep = 3600  # in seconds between images

    def __init__(self):
        return


class JsonFields:
    TS_FORECASTS = "forecasts"
    TS_OBSERVED = "observed"

    TIMESERIES_ID = "id"
    TIMESERIES_TITLE = "title"
    TIMESERIES_DESC = "description"
    TIMESERIES_DATA_STG = "timeseries_stg"
    TIMESERIES_DATA_DSC = "timeseries_dsc"

    METADATA = "metadata"
    METADATA_CURRENTTIME = "current_time"
    METADATA_HASCURRENTT = "has_current_time"
    METADATA_LEADTIME = "lead_time"
    METADATA_HASLEADTIME = "has_lead_time"
    METADATA_MIN_X = "min_x"
    METADATA_MAX_X = "max_x"
    METADATA_MIN_Y = "min_y"
    METADATA_MAX_Y = "max_y"

    def __init__(self):
        return


class JsonLib:

    @staticmethod
    def create_model_forecast_if_needed(big_obj, model_id):
        """

        :param big_obj: Resume Object
        :param model_id:
        :return:
        """
        cur_exists = False
        for cur_mdl in big_obj[JsonFields.TS_FORECASTS]:
            if cur_mdl[JsonFields.TIMESERIES_ID] == model_id:
                cur_exists = True
                break
        if not cur_exists:
            big_obj[JsonFields.TS_FORECASTS].append({
                JsonFields.TIMESERIES_ID: model_id,
                JsonFields.TIMESERIES_TITLE: model_id,
                JsonFields.TIMESERIES_DATA_DSC: {},
                JsonFields.TIMESERIES_DATA_STG: {}
            })

    @staticmethod
    def calculate_meta_info(resume_obj, debug_lvl=0):
        """

        :param resume_obj:
        :param debug_lvl:
        :return:
        """
        min_y = None
        max_y = None
        # show_min = False
        # show_max = False

        # get observed max and min
        for cur_pair in resume_obj[JsonFields.TS_OBSERVED][JsonFields.TIMESERIES_DATA_STG]:
            min_y = float(cur_pair[1]) if (min_y is None) or (min_y < float(cur_pair[1])) else min_y
            max_y = float(cur_pair[1]) if (max_y is None) or (max_y > float(cur_pair[1])) else max_y
            '''
            if (not show_min) and (min_y is not None):
                print("{0} : {1}".format(min_y, type(min_y)))
                show_min = True
            if (not show_max) and (max_y is not None):
                print("{0} : {1}".format(max_y, type(max_y)))
                show_max = True
            '''

        # get forecasted max and min
        for cur_model in resume_obj[JsonFields.TS_FORECASTS]:
            # show_min = False
            # show_max = False
            for cur_pair in cur_model[JsonFields.TIMESERIES_DATA_STG]:
                min_y = float(cur_pair[1]) if (min_y is None) or (min_y < float(cur_pair[1])) else min_y
                max_y = float(cur_pair[1]) if (max_y is None) or (max_y > float(cur_pair[1])) else max_y
                '''
                if (not show_min) and (min_y is not None):
                    print("{0} : {1}".format(min_y, type(min_y)))
                    show_min = True
                if (not show_max) and (max_y is not None):
                    print("{0} : {1}".format(max_y, type(max_y)))
                    show_max = True
                '''

        Debug.dl("rpcbgen_richhydroforecast: Y values between {0} ({1}) and {2} ({3}).".format(min_y, type(min_y),
                                                                                               max_y, type(max_y)), 0,
                 debug_lvl)
        resume_obj[JsonFields.METADATA][JsonFields.METADATA_MIN_Y] = math.floor(min_y)
        resume_obj[JsonFields.METADATA][JsonFields.METADATA_MAX_X] = math.ceil(max_y)

    @staticmethod
    def create_new_resume_object():
        """

        :return:
        """
        return {
            JsonFields.TS_FORECASTS: [],
            JsonFields.TS_OBSERVED: {
                JsonFields.TIMESERIES_DATA_DSC: [],
                JsonFields.TIMESERIES_DATA_STG: []},
            JsonFields.METADATA: {}}

    @staticmethod
    def retrive_most_recent_timestamp_in_hist_folder(folder_path, link_id):
        """

        :param folder_path:
        :param link_id:
        :return:
        """
        print("Reading from '{0}'.".format(folder_path))
        listed_files = sorted(glob.glob(os.path.join(folder_path, "[0-9]*_{0}.json".format(link_id))))
        if len(listed_files) == 0:
            print("Ignoring link {0} - no files in folder:".format(link_id))
            print("  '{0}'.".format(folder_path))
            return None
        cur_last_basename = os.path.basename(listed_files[-1])
        return int(cur_last_basename.split("_")[0])

    @staticmethod
    def retrive_all_files_in_hist_folder(folder_path, link_id=None, min_timestamp=None, max_timestamp=None,
                                         debug_lvl=0):
        """

        :param folder_path:
        :param link_id:
        :param min_timestamp:
        :param max_timestamp:
        :param debug_lvl:
        :return:
        """
        if link_id is None:
            listed_files = sorted(glob.glob(os.path.join(folder_path, "[0-9]*.h5")))
        else:
            listed_files = sorted(glob.glob(os.path.join(folder_path, "[0-9]*_{0}.json".format(link_id))))
        return_list = []
        for cur_file_path in listed_files:
            cur_basename = os.path.basename(cur_file_path)
            cur_timestamp = int(re.search('^[0-9]+', cur_basename).group(0))
            if (min_timestamp is not None) and (cur_timestamp < min_timestamp):
                Debug.dl("rpcbgen_richhydroforecast: Ignoring '{0}'.".format(cur_basename), 6, debug_lvl)
                continue
            elif (max_timestamp is not None) and (cur_timestamp > max_timestamp):
                Debug.dl("rpcbgen_richhydroforecast: Ignoring '{0}'.".format(cur_basename), 6, debug_lvl)
                continue
            return_list.append(cur_file_path)
        return return_list

    @staticmethod
    def retrieve_most_recent_timestamp_in_resume_obj(resume_obj, model_id=None, ref_id=None):
        """

        :param resume_obj:
        :param model_id:
        :param ref_id:
        :return:
        """
        the_timeseries = None
        if model_id is not None:
            for cur_mdl in resume_obj[JsonFields.TS_FORECASTS]:
                if cur_mdl[JsonFields.TIMESERIES_ID] == model_id:
                    the_timeseries = cur_mdl[JsonFields.TIMESERIES_DATA_STG]
                    break
        elif ref_id is not None:
            the_timeseries = resume_obj[JsonFields.TS_OBSERVED][JsonFields.TIMESERIES_DATA_STG]
        else:
            return None

        return None if len(the_timeseries) == 0 else the_timeseries[-1][0]

    @staticmethod
    def retrieve_timestamp_from_file_path(file_path):
        """

        :param file_path:
        :return:
        """
        str_int = re.search('^[0-9]+', os.path.basename(file_path)).group(0)
        return int(str_int)

    @staticmethod
    def update_timeseries(resume_obj, cur_file_path, role, model_id=None):
        """

        :param resume_obj:
        :param cur_file_path:
        :param role:
        :param model_id:
        :return:
        """

        file_obj = None
        print("Reading '{0}'.".format(cur_file_path))
        with open(cur_file_path, "r+") as r_file:
            file_obj = json.load(r_file)

        if role == "stageref":
            for cur_data in file_obj["stage_obs"]:
                resume_obj[JsonFields.TS_OBSERVED][JsonFields.TIMESERIES_DATA_STG].append(cur_data)
            for cur_data in file_obj["disch_obs"]:
                resume_obj[JsonFields.TS_OBSERVED][JsonFields.TIMESERIES_DATA_DSC].append(cur_data)
        elif role == "modelforestg":
            file_timestamp = int(os.path.basename(cur_file_path).split("_")[0])
            leat_time = (resume_obj[JsonFields.METADATA][JsonFields.METADATA_CURRENTTIME] - file_timestamp)/3600
            lead_time = '%.2f' % leat_time
            for resume_mdl in resume_obj[JsonFields.TS_FORECASTS]:
                if resume_mdl[JsonFields.TIMESERIES_ID] == model_id:
                    resume_mdl[JsonFields.TIMESERIES_DATA_STG][lead_time] = file_obj["stage_mdl"]
                    resume_mdl[JsonFields.TIMESERIES_DATA_DSC][lead_time] = file_obj["disch_mdl"]

        return

    def __init__(self):
        return


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
        Debug.dl("rpcbgen_richhydroforecast: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return

    # read file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbgen_richhydroforecast: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbgen_richhydroforecast: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".format(
            runset_id, modelcomb_id, represcomb_id), 0, debug_lvl)
        return

    # load common files
    all_stage_thresholds = Hydrographs.get_all_stage_threshold(debug_lvl=debug_lvl)
    linkid_descarea_dict = Hydrographs.get_linkid_desc_area(debug_lvl=debug_lvl)
    linkid_poisall_dict = Hydrographs.get_linkid_poisall_relationship(debug_lvl=debug_lvl)
    # all_usgs_rc = Hydrographs.get_all_usgs_rating_curves(debug_lvl=debug_lvl)
    all_rc = Hydrographs.get_all_rating_curves(debug_lvl=debug_lvl)

    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info()
    meta_mng.load_all_screference_meta_info()

    #
    frame_set = represcomb_set[represcomb_id]
    link_ids = []
    for cur_model_id in frame_set.keys():
        # generate all intermediate files
        if frame_set[cur_model_id] == "modelpaststg":
            '''
            cur_added_link_ids = generate_modelpaststg_stuff(cur_model_id, runset_id, linkid_poisall_dict, all_usgs_rc,
                                                             meta_mng, timestamp=timestamp, timestamp_min=timestamp_min,
                                                             timestamp_max=timestamp_max, debug_lvl=debug_lvl)
            print("Dealing with {0} => {1}. A.".format(cur_model_id, frame_set[cur_model_id]))
            '''
            # continue
        elif frame_set[cur_model_id] == "modelforestg":
            cur_added_link_ids = generate_modelforestg_stuff(cur_model_id, runset_id, all_rc, meta_mng, timestamp,
                                                             timestamp_min, timestamp_max, debug_lvl=debug_lvl)
            continue
        elif frame_set[cur_model_id] == "stageref":
            cur_added_link_ids = generate_stageref_stuff(cur_model_id, runset_id, all_rc, meta_mng, timestamp,
                                                         timestamp_min, timestamp_max, debug_lvl=debug_lvl)
            print("Added {0} links from {1}.".format(len(cur_added_link_ids), cur_model_id))
        else:
            Debug.dl("rpcbgen_richhydroforecast: Unexpected frame '{0}' for model '{1}.{2}'.".format(
                frame_set[cur_model_id], runset_id, cur_model_id), 1, debug_lvl)
            continue

        # get together all link ids created
        for cur_added_link_id in cur_added_link_ids:
            if cur_added_link_id not in link_ids:
                link_ids.append(cur_added_link_id)

    # create / update common files
    out_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                           represcomb_id=GlobalVar.represcomb_id,
                                                                           frame_id="common")
    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)
    print("Creating links for {0} added links.".format(len(link_ids)))
    for cur_link_id in link_ids:
        create_common_file(out_folder_path, cur_link_id, all_stage_thresholds, linkid_descarea_dict,
                           linkid_poisall_dict, debug_lvl=debug_lvl)


def generate_final_files(modelcomb_id, runset_id, timestamp=None, timestamp_min=None, timestamp_max=None, debug_lvl=0):
    """

    :param modelcomb_id:
    :param runset_id:
    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return:
    """

    # 0 - initial loadings
    represcomb_id = GlobalVar.represcomb_id

    # get all model comb file
    modelcomb_file_path = FileDefinition.obtain_modelcomb_file_path(modelcomb_id, runset_id, debug_lvl=debug_lvl)
    if (modelcomb_file_path is None) or (not os.path.exists(modelcomb_file_path)):
        Debug.dl("rpcbgen_richhydroforecast: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return

    # read file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbgen_richhydroforecast: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return
    frame_set = represcomb_set[represcomb_id]

    # define reference id
    ref_model_id = None
    for cur_model_id in frame_set.keys():
        if frame_set[cur_model_id] != "stageref":
            continue
        ref_model_id = cur_model_id
    if ref_model_id is None:
        Debug.dl("rpcbgen_richhydroforecast: Missing a reference for {0}.{1}.".format(runset_id, modelcomb_id), 0,
                 debug_lvl)
        return

    # define reference folder path
    ref_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                           represcomb_id=GlobalVar.represcomb_id,
                                                                           frame_id="stageref",
                                                                           model_id=ref_model_id)

    out_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                           represcomb_id=GlobalVar.represcomb_id,
                                                                           frame_id="compact")
    if not os.path.exists(out_folder_path):
        os.makedirs(out_folder_path)

    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info()

    # 1 - list all link ids from 'common' folder
    common_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                              represcomb_id=GlobalVar.represcomb_id,
                                                                              frame_id="common")
    all_link_ids = [int(fn.replace(".json", "")) for fn in os.listdir(common_folder_path)]

    # 2 - for each link id:
    for cur_link_id in all_link_ids:
        # print("Solving for link {0}.".format(cur_link_id))

        # 2.0
        cur_timestamp = None

        # 2.1 - define the latest timestamp available (leadtime 0) and minimun timestamp
        print("2.1.a")
        if timestamp is None:

            # get most recent reference timestamp
            cur_timestamp = JsonLib.retrive_most_recent_timestamp_in_hist_folder(ref_folder_path, cur_link_id)
            if cur_timestamp is None:
                Debug.dl("rpcbgen_richhydroforecast: No reference data for link {0}.".format(cur_link_id), 2, debug_lvl)
                continue
        else:
            cur_timestamp = timestamp

        # define minimum and maximum timestamps
        # print("2.1.b")
        if timestamp_min is not None:
            min_timestamp = timestamp_min
        else:
            min_timestamp = cur_timestamp - (GlobalVar.days_past * 24 * GlobalVar.timestep)
        if timestamp_min is not None:
            max_timestamp = timestamp_max
        else:
            max_timestamp = cur_timestamp + (GlobalVar.days_past * 24 * GlobalVar.timestep)

        # 2.2 - create new resume object
        # print("2.2")
        cur_resume = JsonLib.create_new_resume_object()

        cur_resume[JsonFields.METADATA][JsonFields.METADATA_CURRENTTIME] = cur_timestamp
        cur_resume[JsonFields.METADATA][JsonFields.METADATA_HASCURRENTT] = True
        cur_resume[JsonFields.METADATA][JsonFields.METADATA_MIN_X] = min_timestamp
        cur_resume[JsonFields.METADATA][JsonFields.METADATA_MAX_X] = max_timestamp

        # 2.3 - fill reference data
        # print("2.3")
        all_ref_file_paths = JsonLib.retrive_all_files_in_hist_folder(ref_folder_path, cur_link_id, min_timestamp,
                                                                      max_timestamp, debug_lvl=debug_lvl)
        # print("Considering {0} files from {1} to {2}.".format(len(all_ref_file_paths), min_timestamp, max_timestamp))
        for cur_ref_file_path in all_ref_file_paths:
            JsonLib.update_timeseries(cur_resume, cur_ref_file_path, "stageref")

        # 2.4 - for each forecast model
        # print("2.4 - updating each forecast")
        for cur_model_id in frame_set.keys():

            if frame_set[cur_model_id] != "modelforestg":
                continue

            cur_hist_folder = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                                   represcomb_id=GlobalVar.represcomb_id,
                                                                                   frame_id="modelforestg",
                                                                                   model_id=cur_model_id)
            all_mdl_file_paths = JsonLib.retrive_all_files_in_hist_folder(cur_hist_folder, cur_link_id, min_timestamp,
                                                                          max_timestamp, debug_lvl=debug_lvl)

            JsonLib.create_model_forecast_if_needed(cur_resume, cur_model_id)
            for cur_mdl_file_path in all_mdl_file_paths:
                JsonLib.update_timeseries(cur_resume, cur_mdl_file_path, "modelforestg", model_id=cur_model_id)

        # 2.5 - calculate meta info
        # print("2.5 - ")
        JsonLib.calculate_meta_info(cur_resume, debug_lvl=debug_lvl)

        # 3 - save file is feasible
        # print("3.0")
        if cur_resume[JsonFields.METADATA][JsonFields.METADATA_CURRENTTIME] is None:
            print("Skipping link {0}: no current time available.".format(cur_link_id))
            continue

        # 3.1 - define file name and path
        cur_file_name = "{0}_{1}.json".format(cur_resume[JsonFields.METADATA][JsonFields.METADATA_CURRENTTIME],
                                              cur_link_id)
        cur_file_path = os.path.join(out_folder_path, cur_file_name)

        # 3.2 - save file
        with open(cur_file_path, "w+") as r_file:
            json.dump(cur_resume, r_file)
        Debug.dl("rpcbgen_richhydroforecast: Wrote file '{0}'.".format(cur_file_path), 0, debug_lvl)

        break

    return


def generate_modelpaststg_stuff(model_id, runset_id, linkid_poisall_dict, all_usgs_rc, meta_mng, timestamp=None,
                                timestamp_min=None, timestamp_max=None, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param debug_lvl:
    :return: List of added link ids
    """

    prod_id = "idq"

    added_link_ids = []
    Debug.dl("rpcbgen_richhydroforecast: Processing 'modelpaststg' for model '{0}.{1}'.".format(runset_id, model_id),
             4, debug_lvl)

    # define output folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                          represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id="modelpaststg", model_id=model_id)
    if not os.path.exists(outfolder_path):
        os.makedirs(outfolder_path)

    # import information
    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=prod_id,
                                                                             runset_id=runset_id)
    # TODO - use proper def_sys commands
    mdl_prod_file_path_frame = os.path.join(mdl_prod_folder_path, "{0}{1}.npy")
    Debug.dl("rpcbgen_richhydroforecast: reading modeled data from '{0}'.".format(mdl_prod_folder_path), 1, debug_lvl)

    # define timestamps
    the_timestamps = define_timestamps(timestamp=timestamp, timestamp_min=timestamp_min, timestamp_max=timestamp_max,
                                       debug_lvl=debug_lvl)
    the_timestamp_min = the_timestamps[0]
    the_timestamp_mid = the_timestamps[1]

    all_link_ids = all_usgs_rc.keys()

    #
    data_dictionary = {}
    for cur_link_id in all_link_ids:
        data_dictionary[cur_link_id] = []

    # read all files and obtain discharge raw data
    cur_effect_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                     the_timestamp_mid,
                                                                                     accept_range=59*60,
                                                                                     debug_lvl=debug_lvl)
    cur_prod_file_path = mdl_prod_file_path_frame.format(cur_effect_timestamp, prod_id)

    if cur_effect_timestamp is None:
        Debug.dl("rpcbgen_richhydroforecast: No up-to-date file at", 3, debug_lvl)
        Debug.dl("                              '{0}'.".format(mdl_prod_folder_path), 3, debug_lvl)
        return
    else:
        Debug.dl("rpcbgen_richhydroforecast: Considering file '{0}'.".format(cur_prod_file_path), 3, debug_lvl)

    with open(cur_prod_file_path, "rb") as r_file_mdl:
        cur_mdl_content = np.load(r_file_mdl)

    '''
    for cur_link_id in all_link_ids:
        if cur_link_id >= len(cur_mdl_content):
            continue
        added_pair = cur_timestamp, cur_mdl_content[cur_link_id]
        data_dictionary[cur_link_id].append(added_pair)
    '''

    '''
    # read all files and obtain discharge raw data
    for cur_timestamp in range(the_timestamp_min, the_timestamp_mid, GlobalVar.timestep):

        # define the file
        cur_effect_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                         cur_timestamp,
                                                                                         accept_range=29*60,
                                                                                         debug_lvl=debug_lvl)
        cur_prod_file_path = mdl_prod_file_path_frame.format(cur_effect_timestamp, prod_id)

        if cur_effect_timestamp is None:
            Debug.dl("rpcbgen_richhydroforecast: No file for '{0}'.".format(cur_timestamp), 19, debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_richhydroforecast: Considering file '{0}'.".format(cur_prod_file_path), 19, debug_lvl)

        # read file
        with open(cur_prod_file_path, "rb") as r_file_mdl:
            cur_mdl_content = np.load(r_file_mdl)

        for cur_link_id in all_link_ids:
            if cur_link_id >= len(cur_mdl_content):
                continue
            added_pair = cur_timestamp, cur_mdl_content[cur_link_id]
            data_dictionary[cur_link_id].append(added_pair)
    '''

    # write each file converting discharge to stage
    for cur_link_id in all_link_ids:
        # basic check
        if (cur_link_id >= len(cur_mdl_content)) or (cur_link_id == 0):
            continue

        # write file, converting rating curve
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(the_timestamp_mid, cur_link_id))
        with open(out_file_path, "w+") as wfile:
            cur_stg = []
            for cur_pair in data_dictionary[cur_link_id]:
                cur_stg.append([cur_pair[0], Interpolate.my_interpolation_xy(cur_dischs, cur_stages, cur_pair[1] * 35.315)])
            json.dump({"stage_mdl": cur_stg,
                       "disch_mdl": data_dictionary[cur_link_id],
                       "sc_model_title": meta_mng.get_title_of_scmodel(model_id, debug_lvl=debug_lvl)},
                      wfile)
        added_link_ids.append(cur_link_id)
        Debug.dl("rpcbgen_richhydroforecast: Wrote file '{0}'.".format(out_file_path), 1, debug_lvl)

    return added_link_ids


def generate_modelforestg_stuff(model_id, runset_id, all_usgs_rc, meta_mng, timestamp, timestamp_min, timestamp_max,
                                debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param all_usgs_rc:
    :param meta_mng:
    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return: List of added link ids
    """

    prod_id = "fq"

    added_link_ids = []
    Debug.dl("rpcbgen_richhydroforecast: Processing 'modelforestg' for model '{0}.{1}'.".format(runset_id, model_id),
             4, debug_lvl)

    # import information
    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=prod_id,
                                                                             runset_id=runset_id)
    # define folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id, represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id="modelforestg", model_id=model_id)
    # TODO - use proper def_sys commands
    mdl_prod_file_path_frame = os.path.join(mdl_prod_folder_path, "{0}{1}.p")
    Debug.dl("rpcbgen_richhydroforecast: Reading modeled data from:", 1, debug_lvl)
    Debug.dl("                                   '{0}'.".format(mdl_prod_folder_path), 1, debug_lvl)

    # define timestamps
    the_timestamps = define_timestamps(timestamp=timestamp, timestamp_min=timestamp_min, timestamp_max=timestamp_max,
                                       debug_lvl=debug_lvl)
    the_timestamp_min = int(the_timestamps[0])
    the_timestamp_max = int(the_timestamps[2])

    # list all missing timestamps
    all_file_paths = JsonLib.retrive_all_files_in_hist_folder(mdl_prod_folder_path, min_timestamp=the_timestamp_min,
                                                              max_timestamp=the_timestamp_max, debug_lvl=debug_lvl)

    # just a check
    if len(all_file_paths) == 0:
        Debug.dl("rpcbgen_richhydroforecast: No files from {0}.{1}.{2} between {3} and {4}.".format(runset_id, model_id,
                                                                                                    prod_id,
                                                                                                    the_timestamp_min,
                                                                                                    the_timestamp_max),
                 1, debug_lvl)
        return added_link_ids

    for cur_file_path in all_file_paths:
        cur_file_timestamp = JsonLib.retrieve_timestamp_from_file_path(cur_file_path)
        Debug.dl("rpcbgen_richhydroforecast: Check if '{0}.{1}.{2}.{3}' was imported..".format(runset_id, model_id,
                                                                                               prod_id,
                                                                                               cur_file_timestamp), 1,
                 debug_lvl)

        cur_closest_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(outfolder_path,
                                                                                          cur_file_timestamp,
                                                                                          accept_range=60,
                                                                                          debug_lvl=debug_lvl)

        # basic check
        if (cur_closest_timestamp is not None) and (cur_closest_timestamp == cur_file_timestamp):
            Debug.dl("rpcbgen_richhydroforecast: Timestamp {0} already imported.".format(cur_closest_timestamp),
                     1, debug_lvl)
            continue

        print("Closest to {0} ({1})".format(cur_file_timestamp, cur_file_path))
        print("        is {0} ({1}).".format(cur_closest_timestamp, outfolder_path))

        if not os.path.exists(outfolder_path):
            os.makedirs(outfolder_path)

        # for cur_link_id in data_dictionary.keys():
        for cur_link_id in all_usgs_rc.keys():

            # basic check
            '''
            if cur_link_id not in all_usgs_rc.keys():
                Debug.dl("rpcbgen_richhydroforecast: no rating curve for link '{0}'.".format(cur_link_id), 5, debug_lvl)
                continue
            '''

            cur_datadictionary = BinaryLibrary.get_timeseries_for_linkid_product(runset_id, model_id, prod_id, cur_link_id,
                                                                                 timestamp_ini=None, timestamp_end=None,
                                                                                 timestamp_release=cur_file_timestamp,
                                                                                 debug_lvl=debug_lvl)
            if cur_datadictionary is None:
                Debug.dl("rpcbgen_richhydroforecast: no forecast data for '{0}'.".format(cur_link_id), 5, debug_lvl)
                continue

            cur_stg = []
            cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
            # for cur_pair in data_dictionary[cur_link_id]:
            for cur_pair in cur_datadictionary:
                cur_stg.append([cur_pair[0], Interpolate.my_interpolation_xy(cur_dischs, cur_stages, cur_pair[1] * 35.315)])

            out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(cur_file_timestamp, cur_link_id))
            with open(out_file_path, "w+") as wfile:

                # TODO - remove the following dirt step
                # convert 'numpy float' to 'python float'
                '''
                cur_link_timeseries = []
                for cur_pair in data_dictionary[cur_link_id]:
                    cur_link_timeseries.append([cur_pair[0], float(cur_pair[1])])
                '''
                cur_link_timeseries = [(int(pair[0]), float(pair[1])) for pair in cur_datadictionary]

                # write file
                the_dict = {"stage_mdl": cur_stg,
                            "disch_mdl": cur_link_timeseries,
                            "sc_model_title": meta_mng.get_title_of_scmodel(model_id, debug_lvl=debug_lvl)}
                '''
                print("The dict: {0}".format(the_dict))
                print("Types: {0} and {1}.".format(type(data_dictionary[cur_link_id][0][0]),
                                                   type(data_dictionary[cur_link_id][0][1])))
                '''
                encoder.FLOAT_REPR = lambda o: format(o, '.3f')
                json.dump(the_dict, wfile)

            added_link_ids.append(cur_link_id)
            Debug.dl("rpcbgen_richhydroforecast: Writing file: '{0}'.".format(out_file_path), 3, debug_lvl)

            # exit()

    return added_link_ids


def generate_stageref_stuff(reference_id, runset_id, all_usgs_rc, meta_mng, timestamp, timestamp_min, timestamp_max,
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

    added_link_ids = []
    Debug.dl("rpcbgen_richhydroforecast: Processing 'modelforestg' for model '{0}.{1}'.".format(runset_id,
                                                                                                      reference_id),
             4, debug_lvl)

    # import information
    ref_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=reference_id, product_id=prod_id,
                                                                             runset_id=runset_id)
    # TODO - use proper def_sys commands
    ref_prod_file_path_frame = os.path.join(ref_prod_folder_path, "{0}{1}.p")
    Debug.dl("rpcbgen_richhydroforecast: reading modeled data from '{0}'!".format(ref_prod_folder_path), 1,
             debug_lvl)

    # define timestamps
    the_timestamps = define_timestamps(timestamp=timestamp, timestamp_min=timestamp_min, timestamp_max=timestamp_max,
                                       debug_lvl=debug_lvl)
    the_timestamp_mid = the_timestamps[1]
    the_timestamp_max = the_timestamps[2]

    effect_timestamp_mid = FolderDefinition.retrive_closest_timestamp_in_hist_folder(ref_prod_folder_path,
                                                                                     the_timestamp_mid,
                                                                                     accept_range=120*60,
                                                                                     debug_lvl=debug_lvl)
    # basic check
    if effect_timestamp_mid is None:
        Debug.dl("rpcbgen_richhydroforecast: not a file close enough to '{0}' for '{1}.{2}.{3}'.".format(
            the_timestamp_mid, runset_id, reference_id, prod_id), 1, debug_lvl)
        return added_link_ids

    ref_prod_file_path = ref_prod_file_path_frame.format(effect_timestamp_mid, prod_id)

    # print("Using file '{0}' (closest to {1}).".format(mdl_prod_file_path, the_timestamp_mid))

    with open(ref_prod_file_path, 'r') as rfile:
        Debug.dl("rpcbgen_richhydroforecast: reading file '{0}'.".format(ref_prod_file_path), 5, debug_lvl)
        data_dictionary = pickle.load(rfile)

    # define folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                          represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id="stageref", model_id=reference_id)
    if not os.path.exists(outfolder_path):
        Debug.dl("rpcbgen_richhydroforecast: creating folder '{0}'.".format(outfolder_path), 5, debug_lvl)
        os.makedirs(outfolder_path)

    for cur_link_id in data_dictionary.keys():

        # basic check
        if cur_link_id not in all_usgs_rc.keys():
            Debug.dl("rpcbgen_richhydroforecast: no rating curve for link '{0}'.".format(cur_link_id), 5,
                     debug_lvl)
            continue

        '''
        cur_stg = []
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        for cur_pair in data_dictionary[cur_link_id]:
            cur_stg.append([cur_pair[0], my_interpolation_xy(cur_dischs, cur_stages, cur_pair[1] * 35.315)])
        '''
        cur_dsc = []
        cur_stg = []
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        # print("For link {0}: {1}".format(cur_link_id, data_dictionary[cur_link_id]))
        # if True:
        #    exit()
        for cur_timestamp in sorted(data_dictionary[cur_link_id].keys()):
            cur_stg_value = data_dictionary[cur_link_id][cur_timestamp] * 0.0833333   # in to ft
            cur_stg.append([cur_timestamp, cur_stg_value])
            cur_dsc.append([cur_timestamp, Interpolate.my_interpolation_xy(cur_stages, cur_dischs, cur_stg_value)])

        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(effect_timestamp_mid, cur_link_id))
        forcing_title = meta_mng.get_title_of_screference(reference_id, debug_lvl=debug_lvl)
        forcing_title = reference_id if forcing_title is None else forcing_title
        encoder.FLOAT_REPR = lambda o: format(o, '.3f')
        with open(out_file_path, "w+") as wfile:
            json.dump({"stage_obs": cur_stg,
                       "disch_obs": cur_dsc,
                       "sc_reference_title": forcing_title}, wfile)

        added_link_ids.append(cur_link_id)
        Debug.dl("rpcbgen_richhydroforecast: Writing file '{0}'...".format(out_file_path), 3, debug_lvl)

    return added_link_ids


def create_common_file(output_folder_path, link_id, all_stage_thresholds, linkid_descarea_dict, linkid_poisall_dict,
                       debug_lvl=0):
    """

    :param output_folder_path:
    :param link_id:
    :param all_stage_thresholds:
    :param linkid_descarea_dict:
    :param linkid_poisall_dict:
    :param debug_lvl:
    :return:
    """

    # build content
    build_object = {}

    # build content - thresholds
    if link_id in all_stage_thresholds.keys():
        thresholds = all_stage_thresholds[link_id]
        # build_object["thresholds"] = thresholds
        try:
            build_object['stage_threshold_act'] = (thresholds[1]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("rpcbgen_richhydroforecast: Missing action stage for link {0}.".format(link_id), 2, debug_lvl)

        try:
            build_object['stage_threshold_fld'] = (thresholds[2]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("rpcbgen_richhydroforecast: Missing flood stage for link {0}.".format(link_id), 2, debug_lvl)

        try:
            build_object['stage_threshold_mod'] = (thresholds[3]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("rpcbgen_richhydroforecast: Missing moderate stage for link {0}.".format(link_id), 2, debug_lvl)

        try:
            build_object['stage_threshold_maj'] = (thresholds[4]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("rpcbgen_richhydroforecast: Missing major stage for link {0}.".format(link_id), 2, debug_lvl)

    # build content - upstream area
    try:
        build_object["up_area"] = linkid_poisall_dict[link_id][linkid_poisall_dict[link_id].keys()[0]]["up_area"]
    except (TypeError, IndexError, KeyError):
        Debug.dl("rpcbgen_richhydroforecast: Missing upstream area for link {0}.".format(link_id), 2, debug_lvl)

    # build content - desc area
    if link_id in linkid_descarea_dict.keys():
        descarea = linkid_descarea_dict[link_id]
        build_object["description"] = descarea["description"]

    # write file
    file_name = "{0}.json".format(link_id)
    file_path = os.path.join(output_folder_path, file_name)
    with open(file_path, "w+") as wfile:
        json.dump(build_object, wfile)

    Debug.dl("rpcbgen_richhydroforecast: Wrote file '{0}'.".format(file_path), 3, debug_lvl)

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
            Debug.dl("rpcbgen_richhydroforecast: invalid timestamps: min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        the_timestamp_min = GeneralUtils.truncate_timestamp_hour(timestamp_min)
        the_timestamp_max = GeneralUtils.truncate_timestamp_hour(timestamp_max)
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(int((timestamp_max - timestamp_min)/2))
    elif (timestamp is not None) and (timestamp_min is not None) and (timestamp_max is not None):
        # basic check
        if not (timestamp_max > timestamp_min):
            Debug.dl("rpcbgen_richhydroforecast: invalid timestamps - min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        elif not ((timestamp_max > timestamp) and (timestamp > timestamp_min)):
            Debug.dl("rpcbgen_richhydroforecast: invalid timestamps sequence - not ({0} > {1} > {2})'.".format(
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
        Debug.dl("rpcbgen_richhydroforecast: unexpected timestamp informations - min:{0}, mid:{1}, max:{2}'.".format(
                timestamp, timestamp_min, timestamp_max), 1, debug_lvl)
        return

    return the_timestamp_min, the_timestamp_mid, the_timestamp_max


# ####################################################### CALL ####################################################### #

generate_cache_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, timestamp_min_arg, timestamp_max_arg,
                     debug_lvl=debug_level_arg)

'''
generate_final_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, timestamp_min_arg, timestamp_max_arg,
                     debug_lvl=debug_level_arg)
'''
