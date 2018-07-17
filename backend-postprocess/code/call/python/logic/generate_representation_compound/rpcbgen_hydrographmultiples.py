import numpy as np
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
from libs.Interpolate import Interpolate
from libs.Debug import Debug

debug_level_arg = 4

# ################################################# ARGS ################################################# #

modelcomb_id_arg = ReprCombGenInterface.get_modelcomb_id(sys.argv)
runset_id_arg = ReprCombGenInterface.get_runset_id(sys.argv)
timestamp_arg = ReprCombGenInterface.get_timestamp(sys.argv)  # last expected observation, first forecast data
timestamp_min_arg = ReprCombGenInterface.get_min_timestamp_hist(sys.argv)  # graph forced minimum interval
timestamp_max_arg = ReprCombGenInterface.get_max_timestamp_hist(sys.argv)  # graph forced maximum interval


# ################################################# DEFS ################################################# #

class GlobalVar:
    represcomb_id = "hydrographmultiples"
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
    modelcomb_file_path = FileDefinition.obtain_modelcomb_file_path(modelcomb_id, runset_id,
                                                                    debug_lvl=debug_lvl)
    if (modelcomb_file_path is None) or (not os.path.exists(modelcomb_file_path)):
        Debug.dl("rpcbgen_hydrographmultiples: File '{0}' not found.".format(modelcomb_file_path), 0,
                 debug_lvl)
        return

    # read file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbgen_hydrographmultiples: File '{0}' is incomplete.".format(modelcomb_file_path), 0,
                 debug_lvl)
        return

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbgen_hydrographmultiples: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".
                 format(runset_id, modelcomb_id, represcomb_id), 0, debug_lvl)
        return

    # load common files
    all_stage_thresholds = Hydrographs.get_all_stage_threshold(debug_lvl=debug_lvl)
    linkid_descarea_dict = Hydrographs.get_linkid_desc_area(debug_lvl=debug_lvl)
    linkid_poisall_dict = Hydrographs.get_linkid_poisall_relationship(debug_lvl=debug_lvl)
    # all_usgs_rc = Hydrographs.get_all_usgs_rating_curves(debug_lvl=debug_lvl)
    all_rcs = Hydrographs.get_all_rating_curves(debug_lvl=debug_lvl)

    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info()

    #
    frame_set = represcomb_set[represcomb_id]
    link_ids = []
    for cur_model_id in frame_set.keys():
        # generate all intermediate files
        if frame_set[cur_model_id] == "modelpaststg":
            cur_added_link_ids = generate_modelpaststg_stuff(cur_model_id, runset_id, linkid_poisall_dict,
                                                             all_rcs, meta_mng,
                                                             timestamp=timestamp,
                                                             timestamp_min=timestamp_min,
                                                             timestamp_max=timestamp_max,
                                                             debug_lvl=debug_lvl)
        elif frame_set[cur_model_id] == "modelforestg":
            cur_added_link_ids = generate_modelforestg_stuff(cur_model_id, runset_id, all_rcs, meta_mng,
                                                             timestamp, timestamp_min, timestamp_max,
                                                             debug_lvl=debug_lvl)
        else:
            Debug.dl("rpcbgen_hydrographmultiples: Unexpected frame '{0}' for model '{1}.{2}'.".format(
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
    for cur_link_id in link_ids:
        create_common_file(out_folder_path, cur_link_id, all_stage_thresholds, linkid_descarea_dict,
                           linkid_poisall_dict, debug_lvl=debug_lvl)


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
    Debug.dl("rpcbgen_hydrographmultiples: Processing 'modelpaststg' for model '{0}.{1}'.".format(runset_id, model_id),
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
    Debug.dl("rpcbgen_hydrographmultiples: reading modeled data from '{0}'.".format(mdl_prod_folder_path), 1, debug_lvl)

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
    for cur_timestamp in range(the_timestamp_min, the_timestamp_mid, GlobalVar.timestep):

        # define the file
        cur_effect_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                         cur_timestamp,
                                                                                         accept_range=29*60,
                                                                                         debug_lvl=debug_lvl)
        cur_prod_file_path = mdl_prod_file_path_frame.format(cur_effect_timestamp, prod_id)

        if cur_effect_timestamp is None:
            Debug.dl("rpcbgen_hydrographmultiples: No file for '{0}'.".format(cur_timestamp), 19, debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_hydrographmultiples: Considering file '{0}'.".format(cur_prod_file_path), 19, debug_lvl)

        # read file
        with open(cur_prod_file_path, "rb") as r_file_mdl:
            cur_mdl_content = np.load(r_file_mdl)

        for cur_link_id in all_link_ids:
            if cur_link_id >= len(cur_mdl_content):
                continue
            added_pair = cur_timestamp, cur_mdl_content[cur_link_id]
            data_dictionary[cur_link_id].append(added_pair)

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
        Debug.dl("rpcbgen_hydrographmultiples: Wrote file '{0}'.".format(out_file_path), 1, debug_lvl)

    return added_link_ids


def generate_modelforestg_stuff(model_id, runset_id, all_usgs_rc, meta_mng, timestamp, timestamp_min,
                                timestamp_max, debug_lvl=0):
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
    Debug.dl("rpcbgen_hydrographmultiples: Processing 'modelforestg' for model '{0}.{1}'."
             .format(runset_id, model_id), 4, debug_lvl)

    # import information
    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id,
                                                                             product_id=prod_id,
                                                                             runset_id=runset_id)
    # TODO - use proper def_sys commands
    mdl_prod_file_path_frame = os.path.join(mdl_prod_folder_path, "{0}{1}.p")
    Debug.dl("rpcbgen_hydrographmultiples: reading modeled data from '{0}'."
             .format(mdl_prod_folder_path), 1, debug_lvl)

    # define timestamps
    the_timestamps = define_timestamps(timestamp=timestamp, timestamp_min=timestamp_min,
                                       timestamp_max=timestamp_max, debug_lvl=debug_lvl)
    the_timestamp_mid = the_timestamps[1]
    the_timestamp_max = the_timestamps[2]

    effect_timestamp_mid = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                     the_timestamp_mid,
                                                                                     accept_range=120*60,
                                                                                     debug_lvl=debug_lvl)
    # basic check
    if effect_timestamp_mid is None:
        Debug.dl("rpcbgen_hydrographmultiples: not a file close enough to '{0}' for '{1}.{2}.{3}'.".format(
            the_timestamp_mid, runset_id, model_id, prod_id), 1, debug_lvl)
        return added_link_ids

    # mdl_prod_file_path = mdl_prod_file_path_frame.format(effect_timestamp_mid, prod_id)

    # print("Using file '{0}' (closest to {1}).".format(mdl_prod_file_path, the_timestamp_mid))

    # with open(mdl_prod_file_path, 'r') as rfile:
    #     data_dictionary = pickle.load(rfile)

    # define folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id, represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id="modelforestg", model_id=model_id)
    if not os.path.exists(outfolder_path):
        os.makedirs(outfolder_path)

    # for cur_link_id in data_dictionary.keys():
    for cur_link_id in all_usgs_rc.keys():

        # basic check
        '''
        if cur_link_id not in all_usgs_rc.keys():
            Debug.dl("rpcbgen_hydrographmultiples: no rating curve for link '{0}'.".format(cur_link_id), 5, debug_lvl)
            continue
        '''

        cur_datadictionary = BinaryLibrary.get_timeseries_for_linkid_product(runset_id, model_id, prod_id, cur_link_id,
                                                                             timestamp_ini=None, timestamp_end=None,
                                                                             timestamp_release=effect_timestamp_mid,
                                                                             debug_lvl=debug_lvl)
        if cur_datadictionary is None:
            Debug.dl("rpcbgen_hydrographmultiples: no forecast data for '{0}'.".format(cur_link_id), 5, debug_lvl)
            continue

        cur_stg = []
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        # for cur_pair in data_dictionary[cur_link_id]:
        for cur_pair in cur_datadictionary:
            cur_stg.append([cur_pair[0], Interpolate.my_interpolation_xy(cur_dischs, cur_stages, cur_pair[1] * 35.315)])

        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(effect_timestamp_mid, cur_link_id))
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
            json.dump(the_dict, wfile)

        added_link_ids.append(cur_link_id)
        Debug.dl("rpcbgen_hydrographmultiples: Writing file '{0}'.".format(out_file_path), 3, debug_lvl)

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
            build_object['stage_threshold_fld'] = (thresholds[2]-thresholds[0])*0.0833333  # in to ft
            build_object['stage_threshold_mod'] = (thresholds[3]-thresholds[0])*0.0833333  # in to ft
            build_object['stage_threshold_maj'] = (thresholds[4]-thresholds[0])*0.0833333  # in to ft
        except TypeError:
            Debug.dl("rpcbgen_hydrographmultiples: Some stage thresholds for link_id {0} is missing.".format(link_id), 2,
                     debug_lvl)
        except IndexError:
            Debug.dl("rpcbgen_hydrographmultiples: unable to set up thresholds for link_id {0}.".format(link_id), 2,
                     debug_lvl)
            Debug.dl("       Thresholds: {0}.".format(thresholds), 2, debug_lvl)
            return

    # build content - upstream area
        build_object["up_area"] = linkid_poisall_dict[link_id][linkid_poisall_dict[link_id].keys()[0]]["up_area"]

    # build content - desc area
    if link_id in linkid_descarea_dict.keys():
        descarea = linkid_descarea_dict[link_id]
        build_object["description"] = descarea["description"]

    # write file
    file_name = "{0}.json".format(link_id)
    file_path = os.path.join(output_folder_path, file_name)
    with open(file_path, "w+") as wfile:
        json.dump(build_object, wfile)

    Debug.dl("rpcbgen_hydrographmultiples: Wrote file '{0}'.".format(file_path), 3, debug_lvl)

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
            Debug.dl("rpcbgen_hydrographmultiples: invalid timestamps: min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        the_timestamp_min = GeneralUtils.truncate_timestamp_hour(timestamp_min)
        the_timestamp_max = GeneralUtils.truncate_timestamp_hour(timestamp_max)
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(int((timestamp_max - timestamp_min)/2))
    elif (timestamp is not None) and (timestamp_min is not None) and (timestamp_max is not None):
        # basic check
        if not (timestamp_max > timestamp_min):
            Debug.dl("rpcbgen_hydrographmultiples: invalid timestamps - min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        elif not ((timestamp_max > timestamp) and (timestamp > timestamp_min)):
            Debug.dl("rpcbgen_hydrographmultiples: invalid timestamps sequence - not ({0} > {1} > {2})'.".format(
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
        Debug.dl("rpcbgen_hydrographmultiples: unexpected timestamp informations - min:{0}, mid:{1}, max:{2}'.".format(
                timestamp, timestamp_min, timestamp_max), 1, debug_lvl)
        return

    return the_timestamp_min, the_timestamp_mid, the_timestamp_max

# ####################################################### CALL ####################################################### #

generate_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, timestamp_min_arg, timestamp_max_arg,
               debug_lvl=debug_level_arg)
