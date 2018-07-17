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
from libs.Interpolate import Interpolate
from libs.Debug import Debug

debug_level_arg = 20

# ####################################################### ARGS ####################################################### #

modelcomb_id_arg = ReprCombGenInterface.get_modelcomb_id(sys.argv)
runset_id_arg = ReprCombGenInterface.get_runset_id(sys.argv)
timestamp_arg = ReprCombGenInterface.get_timestamp(sys.argv)  # last expected observation, first forecast data
timestamp_min_arg = ReprCombGenInterface.get_min_timestamp_hist(sys.argv)  # graph forced minimum interval
timestamp_max_arg = ReprCombGenInterface.get_max_timestamp_hist(sys.argv)  # graph forced maximum interval


# ####################################################### DEFS ####################################################### #

class GlobalVar:
    represcomb_id = "hydrographmultiplespast"
    days_past = 10
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
        Debug.dl("rpcbgen_hydrographmultiplespast: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
        return

    # read file content
    with open(modelcomb_file_path, "r+") as rfile:
        modelcomb_json = json.load(rfile)

    # iterates over each stuff
    try:
        represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
    except KeyError:
        Debug.dl("rpcbgen_hydrographmultiplespast: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
        return

    #
    if represcomb_id not in represcomb_set:
        Debug.dl("rpcbgen_hydrographmultiplespast: Modelcomb '{0}.{1}' has no representation comb. '{2}'.".format(
            runset_id, modelcomb_id, represcomb_id), 0, debug_lvl)
        return

    # load common files
    all_stage_thresholds = Hydrographs.get_all_stage_threshold(debug_lvl=debug_lvl)
    linkid_descarea_dict = Hydrographs.get_linkid_desc_area(debug_lvl=debug_lvl)
    linkid_poisall_dict = Hydrographs.get_linkid_poisall_relationship(debug_lvl=debug_lvl)
    all_usgs_rc = Hydrographs.get_all_usgs_rating_curves(debug_lvl=debug_lvl)

    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_scrunset_meta_info()
    meta_mng.load_all_scmodel_meta_info()
    meta_mng.load_all_screference_meta_info()

    #
    frame_set = represcomb_set[represcomb_id]
    model_link_ids = []
    ref_link_ids = None
    for cur_source_id in frame_set.keys():
        # generate all intermediate files
        if frame_set[cur_source_id] == "modelpaststg":
            cur_added_link_ids = generate_modelpaststg_stuff(cur_source_id, runset_id, linkid_poisall_dict, all_usgs_rc,
                                                             meta_mng, timestamp=timestamp, timestamp_min=timestamp_min,
                                                             timestamp_max=timestamp_max, debug_lvl=debug_lvl)

            # get together all model link ids created
            model_link_ids = list(set(model_link_ids + cur_added_link_ids))

        elif frame_set[cur_source_id] == "stageref":
            ref_link_ids = generate_stageref_stuff(cur_source_id, runset_id, all_usgs_rc, meta_mng, timestamp,
                                                   timestamp_min, timestamp_max, debug_lvl=debug_lvl)
        elif frame_set[cur_source_id] == "dischref":
            ref_link_ids = generate_dischref_stuff(cur_source_id, runset_id, all_usgs_rc, meta_mng, timestamp,
                                                   timestamp_min, timestamp_max, debug_lvl=debug_lvl)
        else:
            Debug.dl("rpcbgen_hydrographmultiplespast: Unexpected frame '{0}' for source '{1}.{2}'.".format(
                frame_set[cur_source_id], runset_id, cur_source_id), 1, debug_lvl)
            continue

    # define effective links - if there is a reference, it dominates the common
    link_ids = model_link_ids if ref_link_ids is None else list(set(model_link_ids).intersection(ref_link_ids))

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
    Debug.dl("rpcbgen_hydrographmultiplespast: Processing 'modelpaststg' for model '{0}.{1}'.".format(runset_id,
                                                                                                      model_id),
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
    Debug.dl("rpcbgen_hydrographmultiplespast: reading modeled data from '{0}'?".format(mdl_prod_folder_path), 1,
             debug_lvl)

    # define timestamps
    if timestamp_max is None:
        the_timestamp_max = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(mdl_prod_folder_path)
        if the_timestamp_max is None:
            Debug.dl("rpcbgen_hydrographmultiplespast: unable to retrieve a max timestamp from '{0}'.".format(mdl_prod_folder_path),
                     1, debug_lvl)
            return []
    else:
        the_timestamp_max = timestamp_max
        print("Given {0}.".format(the_timestamp_max))
    if timestamp_min is None:
        the_timestamp_min = meta_mng.get_runset_timestamp_ini()
        print("Got {0} from metafile.".format(the_timestamp_min))
        if the_timestamp_min is None:
            the_timestamp_min = the_timestamp_max - (GlobalVar.days_past * 24 * 60 * 60)  # ten days ago
            print("Forced {0} from substraction.".format(the_timestamp_min))
    else:
        the_timestamp_min = timestamp_min

    all_link_ids = all_usgs_rc.keys()

    #
    data_dictionary = {}
    for cur_link_id in all_link_ids:
        data_dictionary[cur_link_id] = []

    # read all files and obtain discharge raw data
    print("rpcbgen_hydrographmultiplespast: Iterating from {0} to {1}.".format(the_timestamp_min, the_timestamp_max))
    for cur_timestamp in range(the_timestamp_min, the_timestamp_max, GlobalVar.timestep):

        # define the file
        cur_effect_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                         cur_timestamp,
                                                                                         accept_range=29*60,
                                                                                         debug_lvl=debug_lvl)
        cur_prod_file_path = mdl_prod_file_path_frame.format(cur_effect_timestamp, prod_id)

        if cur_effect_timestamp is None:
            Debug.dl("rpcbgen_hydrographmultiplespast: No file for '{0}'.".format(cur_timestamp), 19, debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_hydrographmultiplespast: Considering file '{0}'.".format(cur_prod_file_path), 19,
                     debug_lvl)

        # read file
        with open(cur_prod_file_path, "rb") as r_file_mdl:
            cur_mdl_content = np.load(r_file_mdl)

        if cur_mdl_content is None:
            print("Some error with '{0}'.".format(cur_prod_file_path))

        for cur_link_id in all_link_ids:
            if cur_link_id >= len(cur_mdl_content):
                continue
            added_pair = cur_timestamp, cur_mdl_content[cur_link_id]
            data_dictionary[cur_link_id].append(added_pair)

    Debug.dl("rpcbgen_hydrographmultiplespast: Considering {0} linkids.".format(len(data_dictionary.keys())), 19,
             debug_lvl)

    # write each file converting discharge to stage
    for cur_link_id in all_link_ids:
        # basic check - link must exist
        if (cur_link_id not in data_dictionary.keys()) or (cur_link_id == 0):
            Debug.dl("rpcbgen_hydrographmultiplespast: Ignoring link {0}.".format(cur_link_id), 19, debug_lvl)
            continue

        # basic check - link must have something
        if len(data_dictionary[cur_link_id]) <= 0:
            Debug.dl("rpcbgen_hydrographmultiplespast: No model data for link {0}.".format(cur_link_id), 10, debug_lvl)
            continue

        # write file, converting rating curve
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])

        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(the_timestamp_max, cur_link_id))
        with open(out_file_path, "w+") as wfile:
            cur_stg = []
            for cur_pair in data_dictionary[cur_link_id]:
                current_discharge = cur_pair[1] * 35.315
                if current_discharge <= 0:
                    continue
                current_stage = Interpolate.my_interpolation_xy(cur_dischs, cur_stages, current_discharge)
                if current_stage is not None:
                    cur_stg.append([cur_pair[0], current_stage])
            json.dump({"stage_mdl": cur_stg,
                       "disch_mdl": data_dictionary[cur_link_id],
                       "sc_model_title": meta_mng.get_title_of_scmodel(model_id, debug_lvl=debug_lvl)},
                      wfile)
        added_link_ids.append(cur_link_id)
        Debug.dl("rpcbgen_hydrographmultiplespast: Wrote file '{0}'.".format(out_file_path), 1, debug_lvl)

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

    print("In generate_stageref_stuff() for reference {0}.{1}".format(runset_id, reference_id))

    prod_id = "istg"

    added_link_ids = []
    Debug.dl("rpcbgen_hydrographmultiplespast: Processing 'modelforestg' for model '{0}.{1}'.".format(runset_id,
                                                                                                      reference_id),
             4, debug_lvl)

    # import information
    ref_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=reference_id, product_id=prod_id,
                                                                             runset_id=runset_id)
    # TODO - use proper def_sys commands
    ref_prod_file_path_frame = os.path.join(ref_prod_folder_path, "{0}{1}.p")
    Debug.dl("rpcbgen_hydrographmultiplespast: reading modeled data from '{0}'!".format(ref_prod_folder_path), 1,
             debug_lvl)

    # define timestamps
    the_timestamps = define_timestamps(timestamp=timestamp, timestamp_min=timestamp_min, timestamp_max=timestamp_max,
                                       debug_lvl=debug_lvl)
    the_timestamp_min = the_timestamps[0]
    the_timestamp_mid = the_timestamps[1]

    effect_timestamp_mid = FolderDefinition.retrive_closest_timestamp_in_hist_folder(ref_prod_folder_path,
                                                                                     the_timestamp_mid,
                                                                                     accept_range=120*60,
                                                                                     debug_lvl=debug_lvl)
    # basic check
    if effect_timestamp_mid is None:
        Debug.dl("rpcbgen_hydrographmultiplespast: not a file close enough to '{0}' for '{1}.{2}.{3}'.".format(
            the_timestamp_mid, runset_id, reference_id, prod_id), 1, debug_lvl)
        return added_link_ids

    # define output folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                          represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id="stageref", model_id=reference_id)
    if not os.path.exists(outfolder_path):
        Debug.dl("rpcbgen_hydrographmultiplespast: creating folder '{0}'.".format(outfolder_path), 5, debug_lvl)
        os.makedirs(outfolder_path)








    # ##########################################################################################

    # get all link ids
    all_link_ids = all_usgs_rc.keys()

    print("All link ids: {0}".format(all_link_ids))

    # prepare receiving data dictionary
    data_dictionary = {}
    for cur_link_id in all_link_ids:
        data_dictionary[cur_link_id] = []

    # load all information organized
    for cur_timestamp in range(the_timestamp_min, the_timestamp_mid, GlobalVar.timestep):

        # define the file
        cur_effect_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(ref_prod_folder_path,
                                                                                         cur_timestamp,
                                                                                         accept_range=29 * 60,
                                                                                         debug_lvl=debug_lvl)
        cur_prod_file_path = ref_prod_file_path_frame.format(cur_effect_timestamp, prod_id)

        if cur_effect_timestamp is None:
            Debug.dl("rpcbgen_hydrographmultiplespast: No file for '{0}'.".format(cur_timestamp), 19, debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_hydrographmultiplespast: Considering file '{0}'.".format(cur_prod_file_path), 19,
                     debug_lvl)

        # read file and basic check it
        with open(cur_prod_file_path, "rb") as r_file_mdl:
            cur_ref_content = np.load(r_file_mdl)
            if cur_ref_content is None:
                print("Some error with '{0}'.".format(cur_prod_file_path))
                continue

        # append data in file into dictionary
        for cur_link_id in all_link_ids:
            if cur_link_id not in cur_ref_content.keys():
                continue
            for cur_t, cur_stg in cur_ref_content[cur_link_id].items():
                added_pair = [cur_t, cur_stg]
                data_dictionary[cur_link_id].append(added_pair)

    # write output files, link by link
    for cur_link_id in data_dictionary.keys():

        # basic check
        if cur_link_id not in all_usgs_rc.keys():
            Debug.dl("rpcbgen_hydrographmultiplespast: no rating curve for link '{0}'.".format(cur_link_id), 5,
                     debug_lvl)
            continue

        cur_dsc = []
        cur_stg = []
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        last_t = None
        count_add = 0
        for cur_pair in data_dictionary[cur_link_id]:
            if (last_t is not None) and (last_t == cur_pair[0]):
                continue
            cur_stg_value = cur_pair[1] * 0.0833333   # in to ft
            cur_stg.append([cur_pair[0], cur_stg_value])
            cur_dsc.append([cur_pair[0], Interpolate.my_interpolation_xy(cur_stages, cur_dischs, cur_stg_value)])
            last_t = cur_pair[0]
            count_add += 1

        # basic check
        if count_add <= 1:
            print("Ignoring a link {0}: {1} registers".format(cur_link_id, count_add))
            continue
        else:
            print("Considering link {0}: {1} registers".format(cur_link_id, count_add))

        # write file
        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(effect_timestamp_mid, cur_link_id))
        forcing_title = meta_mng.get_title_of_screference(reference_id, debug_lvl=debug_lvl)
        forcing_title = reference_id if forcing_title is None else forcing_title
        with open(out_file_path, "w+") as wfile:
            json.dump({"stage_obs": cur_stg,
                       "disch_obs": cur_dsc,
                       "sc_reference_title": forcing_title}, wfile)

        added_link_ids.append(cur_link_id)
        Debug.dl("rpcbgen_hydrographmultiplespast: Writing file '{0}'.".format(out_file_path), 3, debug_lvl)


    '''
    # define and read ref. file
    ref_prod_file_path = ref_prod_file_path_frame.format(effect_timestamp_mid, prod_id)
    with open(ref_prod_file_path, 'r') as rfile:
        Debug.dl("rpcbgen_hydrographmultiplespast: reading file '{0}'.".format(ref_prod_file_path), 5, debug_lvl)
        data_dictionary = pickle.load(rfile)

    for cur_link_id in data_dictionary.keys():

        # basic check
        if cur_link_id not in all_usgs_rc.keys():
            Debug.dl("rpcbgen_hydrographmultiplespast: no rating curve for link '{0}'.".format(cur_link_id), 5,
                     debug_lvl)
            continue

        cur_dsc = []
        cur_stg = []
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
        for cur_timestamp in sorted(data_dictionary[cur_link_id].keys()):
            cur_stg_value = data_dictionary[cur_link_id][cur_timestamp] * 0.0833333   # in to ft
            cur_stg.append([cur_timestamp, cur_stg_value])
            cur_dsc.append([cur_timestamp, my_interpolation_xy(cur_stages, cur_dischs, cur_stg_value)])

        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(effect_timestamp_mid, cur_link_id))
        forcing_title = meta_mng.get_title_of_screference(reference_id, debug_lvl=debug_lvl)
        forcing_title = reference_id if forcing_title is None else forcing_title
        with open(out_file_path, "w+") as wfile:
            json.dump({"stage_obs": cur_stg,
                       "disch_obs": cur_dsc,
                       "sc_reference_title": forcing_title}, wfile)

        added_link_ids.append(cur_link_id)
        Debug.dl("rpcbgen_hydrographmultiplespast: Writing file '{0}'.".format(out_file_path), 3, debug_lvl)
    '''

    return added_link_ids


def generate_dischref_stuff(reference_id, runset_id, all_usgs_rc, meta_mng, timestamp, timestamp_min, timestamp_max,
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
    :return:
    """

    prod_id = "isq"

    added_link_ids = []
    Debug.dl("In generate_dischref_stuff() for reference {0}.{1}".format(runset_id, reference_id), 4, debug_lvl)

    # import information
    ref_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=reference_id, product_id=prod_id,
                                                                             runset_id=runset_id)
    # TODO - use proper def_sys commands
    ref_prod_file_path_frame = os.path.join(ref_prod_folder_path, "{0}{1}.p")
    Debug.dl("rpcbgen_hydrographmultiplespast: reading reference data from '{0}'...".format(ref_prod_folder_path), 1,
             debug_lvl)

    # get maximum and minimum timestamps from file content
    tmp_timestamp_min = timestamp_min
    tmp_timestamp_max = timestamp_max
    if (tmp_timestamp_min is None) or (tmp_timestamp_max is None):
        all_ref_prod_file_names = sorted(os.listdir(ref_prod_folder_path))
        if len(all_ref_prod_file_names) > 0:
            if tmp_timestamp_min is None:
                tmp_timestamp_min = meta_mng.get_runset_timestamp_ini()
                if tmp_timestamp_min is None:
                    tmp_timestamp_min = FileDefinition.obtain_hist_file_timestamp(all_ref_prod_file_names[0])
            if tmp_timestamp_max is None:
                tmp_timestamp_max = meta_mng.get_runset_timestamp_end()
                if tmp_timestamp_max is None:
                    tmp_timestamp_max = FileDefinition.obtain_hist_file_timestamp(all_ref_prod_file_names[-1])
            Debug.dl("rpcbgen_hydrographmultiplespast: Timestamps between {0} and {1}.".format(tmp_timestamp_min,
                                                                                   tmp_timestamp_max), 1, debug_lvl)

        else:
            Debug.dl("rpcbgen_hydrographmultiplespast: no files in '{0}'.".format(ref_prod_folder_path), 1, debug_lvl)
    else:
        Debug.dl("rpcbgen_hydrographmultiplespast: Provided {0} and {1}.".format(tmp_timestamp_min, tmp_timestamp_max),
                 1, debug_lvl)

    all_link_ids = all_usgs_rc.keys()

    # prepare receiving data dictionary
    data_dictionary = {}
    for cur_link_id in all_link_ids:
        data_dictionary[cur_link_id] = []

    # load all information organized
    for cur_timestamp in range(tmp_timestamp_min, tmp_timestamp_max, GlobalVar.timestep):

        # define the file
        cur_effect_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(ref_prod_folder_path,
                                                                                         cur_timestamp,
                                                                                         accept_range=29*60,
                                                                                         debug_lvl=debug_lvl)
        cur_prod_file_path = ref_prod_file_path_frame.format(cur_effect_timestamp, prod_id)

        if cur_effect_timestamp is None:
            Debug.dl("rpcbgen_hydrographmultiplespast: No file for '{0}'.".format(cur_timestamp), 19, debug_lvl)
            continue
        else:
            Debug.dl("rpcbgen_hydrographmultiplespast: Considering file '{0}'.".format(cur_prod_file_path), 19,
                     debug_lvl)

        # read file
        with open(cur_prod_file_path, "rb") as r_file_mdl:
            cur_ref_content = np.load(r_file_mdl)

        if cur_ref_content is None:
            print("Some error with '{0}'.".format(cur_prod_file_path))

        for cur_link_id in all_link_ids:
            if cur_link_id not in cur_ref_content.keys():
                continue
            added_pair = cur_timestamp, cur_ref_content[cur_link_id]
            data_dictionary[cur_link_id].append(added_pair)
            if cur_link_id == 434514:
                print("Link {0} has {1}.".format(cur_link_id, len(data_dictionary[cur_link_id])))

    # define folder path and create it if necessary
    outfolder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                          represcomb_id=GlobalVar.represcomb_id,
                                                                          frame_id="dischref", model_id=reference_id)

    if not os.path.exists(outfolder_path):
        Debug.dl("rpcbgen_hydrographmultiplespast: creating folder '{0}'.".format(outfolder_path), 5, debug_lvl)
        os.makedirs(outfolder_path)

    # writing each link file
    for cur_link_id in data_dictionary.keys():

        # basic check
        if cur_link_id not in all_usgs_rc.keys():
            Debug.dl("rpcbgen_hydrographmultiplespast: no rating curve for link '{0}'.".format(cur_link_id), 5,
                     debug_lvl)
            continue

        # get hydrograph for the link
        cur_dsc = []
        cur_stg = []
        cur_dischs, cur_stages = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])

        # get both stage and discharge for all values
        if len(data_dictionary[cur_link_id]) == 0:
            continue
        for cur_pair in data_dictionary[cur_link_id]:
            cur_dsc_value = cur_pair[1]
            # print("disch_val: {0}".format(cur_dsc_value))
            try:
                cur_stg_value = Interpolate.my_interpolation_xy(cur_dischs, cur_stages, cur_dsc_value[cur_pair[0]] * 35.315)
                if cur_stg_value is None:
                    # TODO - understand how it is possible
                    continue
                cur_stg.append([cur_pair[0], cur_stg_value])
                cur_dsc.append([cur_pair[0], cur_dsc_value])
            except KeyError:
                continue

        # write file
        out_file_path = os.path.join(outfolder_path, "{0}_{1}.json".format(tmp_timestamp_max, cur_link_id))
        forcing_title = meta_mng.get_title_of_screference(reference_id, debug_lvl=debug_lvl)
        forcing_title = reference_id if forcing_title is None else forcing_title
        Debug.dl("rpcbgen_hydrographmultiplespast: About to write file '{0}'.".format(out_file_path), 3, debug_lvl)
        with open(out_file_path, "w+") as wfile:
            json.dump({"stage_obs": cur_stg,
                       "disch_obs": cur_dsc,
                       "sc_reference_title": forcing_title}, wfile)

        added_link_ids.append(cur_link_id)

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
        except (TypeError, IndexError):
            Debug.dl("evalgen_hydrographsd: Some stage thresholds for link_id {0} is missing.".format(link_id), 2,
                     debug_lvl)

    # build content - upstream area
    if link_id in linkid_poisall_dict.keys():
        pois_key = linkid_poisall_dict[link_id].keys()[0]
        link_pois = linkid_poisall_dict[link_id][pois_key]
        build_object["up_area"] = link_pois["up_area"]

    # build content - desc area
    if link_id in linkid_descarea_dict.keys():
        descarea = linkid_descarea_dict[link_id]
        build_object["description"] = descarea["description"]

    # write file
    file_name = "{0}.json".format(link_id)
    file_path = os.path.join(output_folder_path, file_name)
    with open(file_path, "w+") as wfile:
        json.dump(build_object, wfile)

    Debug.dl("rpcbgen_hydrographmultiplespast: Wrote file '{0}'.".format(file_path), 3, debug_lvl)

    return


def define_timestamps(timestamp=None, timestamp_min=None, timestamp_max=None, debug_lvl=0):
    """

    :param timestamp:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return: Three values: min timestamp, mid timestamp, max timestamp (in this sequence)
    """

    # define intervals
    if (timestamp is None) and (timestamp_min is None) and (timestamp_max is None):
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(time.time())
        the_timestamp_min = the_timestamp_mid - (GlobalVar.days_past * 24 * 60 * 60)
        the_timestamp_max = the_timestamp_mid
    elif (timestamp is None) and (timestamp_min is not None) and (timestamp_max is not None):
        # basic check
        if not (timestamp_max > timestamp_min):
            Debug.dl("rpcbgen_hydrographmultiplespast: invalid timestamps: min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        the_timestamp_min = GeneralUtils.truncate_timestamp_hour(timestamp_min)
        the_timestamp_max = GeneralUtils.truncate_timestamp_hour(timestamp_max)
        the_timestamp_mid = GeneralUtils.truncate_timestamp_hour(int((timestamp_max + timestamp_min)/2))
    elif (timestamp is not None) and (timestamp_min is not None) and (timestamp_max is not None):
        # basic check
        if not (timestamp_max > timestamp_min):
            Debug.dl("rpcbgen_hydrographmultiplespast: invalid timestamps - min ({0}) >= max ({1})'.".format(
                timestamp_min, timestamp_max), 1, debug_lvl)
            return
        elif not ((timestamp_max > timestamp) and (timestamp > timestamp_min)):
            Debug.dl("rpcbgen_hydrographmultiplespast: invalid timestamps sequence - not ({0} > {1} > {2})'.".format(
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
        Debug.dl("rpcbgen_hydrographmultiplespast: unexpected timestamp informations - min:{0}, mid:{1}, max:{2}'.".format(
                timestamp, timestamp_min, timestamp_max), 1, debug_lvl)
        return

    return the_timestamp_min, the_timestamp_mid, the_timestamp_max

# ####################################################### CALL ####################################################### #

generate_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, timestamp_min_arg, timestamp_max_arg,
               debug_lvl=debug_level_arg)
