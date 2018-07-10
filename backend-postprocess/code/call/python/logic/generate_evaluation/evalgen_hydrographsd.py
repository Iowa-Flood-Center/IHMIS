from decimal import Decimal
import numpy as np
import datetime
import pickle
import json
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.FilenameDefinition import FilenameDefinition
from libs.EvalGenInterface import EvalGenInterface
from libs.FolderDefinition import FolderDefinition
from libs.FileDefinition import FileDefinition
from libs.GeneralUtils import GeneralUtils
from libs.Interpolate import Interpolate
from libs.Hydrographs import Hydrographs
from libs.Debug import Debug

# create hydrograph SS : Discharge-Static

debug_level_arg = 9
timestamp_step = 1 * 60 * 60        # plots with hourly interval
graph_interval = 10 * 24 * 60 * 60  # graphs in a 10-days interval

# ####################################################### ARGS ####################################################### #

model_id_arg = EvalGenInterface.get_model_id(sys.argv)
reference_id_arg = EvalGenInterface.get_reference_id(sys.argv)
timestamp_arg = EvalGenInterface.get_timestamp(sys.argv)
runset_id_arg = EvalGenInterface.get_runset_id(sys.argv)
timestamp_min_arg = EvalGenInterface.get_min_timestamp_hist(sys.argv)
timestamp_max_arg = EvalGenInterface.get_max_timestamp_hist(sys.argv)


# ####################################################### DEFS ####################################################### #

def plot_graphs(model_id, reference_id, timestamp, runset_id, graph_interval, timestamp_step, timestamp_min,
                timestamp_max, debug_lvl=0):
    """

    :param model_id:
    :param reference_id:
    :param timestamp:
    :param runset_id:
    :param graph_interval:
    :param timestamp_step:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return:
    """

    if runset_id is not None:
        plot_graphs_runset(model_id, reference_id, timestamp, runset_id, graph_interval, timestamp_step, timestamp_min,
                           timestamp_max, debug_lvl=debug_lvl)
    else:
        print("evalgen_hydrographss: Realtime option not available")


def plot_graphs_runset(model_id, reference_id, timestamp, runset_id, graph_interval, timestamp_step, timestamp_min,
                       timestamp_max, debug_lvl=0):
    """

    :param model_id:
    :param reference_id:
    :param timestamp:
    :param runset_id:
    :param timestamp_step:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return:
    """

    sc_mdl_prod = "idq"
    sc_ref_prods = ["isq", "istg"]
    sc_eval_repr = "hydrographsd"

    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=sc_mdl_prod,
                                                                             runset_id=runset_id)

    Debug.dl("evalgen_hydrographsd: reading modeled data from '{0}'.".format(mdl_prod_folder_path), 1, debug_lvl)

    # searches available reference product
    sc_ref_prod = None
    ref_prod_folder_path = None
    for cur_possible_ref_prod in sc_ref_prods:
        ref_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=reference_id,
                                                                                 product_id=cur_possible_ref_prod,
                                                                                 runset_id=runset_id)
        if os.path.exists(ref_prod_folder_path):
            sc_ref_prod = cur_possible_ref_prod
            break
        else:
            ref_prod_folder_path = None

    # check if it is possible to continue
    if ref_prod_folder_path is not None:
        Debug.dl("evalgen_hydrographsd: using '{0}' of '{1}' for {2}.{3})".format(sc_ref_prod, reference_id,
                                                                                  runset_id, model_id), 3, debug_lvl)
        Debug.dl("evalgen_hydrographsd: reading observed data from '{0}'.".format(ref_prod_folder_path), 1, debug_lvl)
    else:
        Debug.dl("evalgen_hydrographsd: not found a valid product of '{0}' for '{1}' ({3})".format(reference_id,
                                                                                                   model_id, runset_id),
                 3, debug_lvl)
        return

    # TODO - use proper def_sys commands
    mdl_prod_file_path = os.path.join(mdl_prod_folder_path, "{0}{1}.npy")
    ref_prod_file_path = os.path.join(ref_prod_folder_path, "{0}{1}.p")

    # define output folder path and ensure it exists
    output_filepath_folder_path = FolderDefinition.get_historical_eval_folder_path(model_id, sc_eval_repr, reference_id,
                                                                                   runset_id=runset_id)
    if not os.path.exists(output_filepath_folder_path):
        os.makedirs(output_filepath_folder_path)

    # TODO - use proper def_sys commands
    output_filepath_frame = os.path.join(output_filepath_folder_path, "{0}_{1}.json")

    # list all link_ids
    all_link_ids = list_all_considered_linkids(ref_prod_folder_path, debug_lvl=debug_lvl)

    # establish timestamps to be plotted
    all_timestamps = establish_timestamps_in_graph(mdl_prod_folder_path, ref_prod_folder_path, graph_interval,
                                                   timestamp_step, timestamp_min=timestamp_min,
                                                   timestamp_max=timestamp_max, debug_lvl=debug_lvl)

    if (all_timestamps is None) or (len(all_timestamps) <= 0):
        Debug.dl("evalgen_hydrographsd: unable to define timestamps for {0}.{1}.{2}".format(runset_id, model_id,
                                                                                            reference_id),
                 3, debug_lvl)
        return

    # prepares receiving dictionaries
    mdl_dict = {}
    ref_dict = {}
    for cur_link_id in all_link_ids:
        mdl_dict[cur_link_id] = {}
        ref_dict[cur_link_id] = {}

    # read ancillary files
    all_stage_thresholds = Hydrographs.get_all_stage_threshold(debug_lvl=debug_lvl)
    linkid_descarea_dict = Hydrographs.get_linkid_desc_area(debug_lvl=debug_lvl)
    linkid_poisall_dict = Hydrographs.get_linkid_poisall_relationship(debug_lvl=debug_lvl)
    # all_usgs_rc = Hydrographs.get_all_usgs_rating_curves(debug_lvl=debug_lvl)
    all_usgs_rc = Hydrographs.get_all_rating_curves(debug_lvl=debug_lvl)

    # for each timestamps, read both model results and obs data
    for cur_timestamp in all_timestamps:

        # for current timestamp, read modeled file
        cur_timestamp_close = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                        cur_timestamp)
        cur_mdl_file_path = mdl_prod_file_path.format(cur_timestamp_close, sc_mdl_prod)
        if os.path.exists(cur_mdl_file_path):
            with open(cur_mdl_file_path, "rb") as r_file_mdl:
                cur_mdl_content = np.load(r_file_mdl)
        else:
            Debug.dl("evalgen_hydrographsd: File not found '{0}'.".format(cur_mdl_file_path), 3, debug_lvl)
            cur_mdl_content = None

        # for current timestamp, read observed file
        cur_ref_file_path = ref_prod_file_path.format(cur_timestamp, sc_ref_prod)
        Debug.dl("evalgen_hydrographsd: Taking as reference for {0}.{1}: ".format(runset_id, model_id), 3, debug_lvl)
        Debug.dl("                           '{0}'".format(cur_ref_file_path), 3, debug_lvl)
        if os.path.exists(cur_ref_file_path):
            with open(cur_ref_file_path, "rb") as r_file_ref:
                cur_ref_content = np.load(r_file_ref)
        else:
            Debug.dl("evalgen_hydrographsd: File not found '{0}'.".format(cur_ref_file_path), 3, debug_lvl)

            # try rounding the time
            cur_timestamp_rounded = GeneralUtils.round_timestamp_hour(cur_timestamp)
            cur_ref_file_path = ref_prod_file_path.format(cur_timestamp_rounded, sc_ref_prod)
            Debug.dl("evalgen_hydrographsd: Trying as reference for {0}.{1}: ".format(runset_id, model_id), 3, debug_lvl)
            Debug.dl("                           '{0}'".format(cur_ref_file_path), 3, debug_lvl)
            if os.path.exists(cur_ref_file_path):
                with open(cur_ref_file_path, "rb") as r_file_ref:
                    cur_ref_content = np.load(r_file_ref)
            else:
                Debug.dl("evalgen_hydrographsd: File also not found '{0}'.".format(cur_ref_file_path), 3, debug_lvl)
                cur_ref_content = None

        # for each link_id, add it to dict
        Debug.dl("evalgen_hydrographsd: Got {0} links for time {1}".format(len(all_link_ids), cur_timestamp), 9,
                 debug_lvl)
        count_ignored_linkid = 0
        for cur_link_id in all_link_ids:
            # if cur_link_id < len(cur_mdl_content):
            try:
                if cur_mdl_content is not None:
                    if (cur_link_id not in mdl_dict.keys()) or (cur_link_id >= len(cur_mdl_content)):
                        Debug.dl("evalgen_hydrographsd:    Ignoring link id {0}".format(cur_link_id), 9, debug_lvl)
                        Debug.dl("evalgen_hydrographsd:     >= {0} , >= {1}".format(len(mdl_dict),
                                                                                    len(cur_mdl_content)), 9, debug_lvl)
                        count_ignored_linkid += 1
                        continue
                    cur_link_content = cur_mdl_content[cur_link_id]
                    mdl_dict[cur_link_id][cur_timestamp] = cur_link_content
            except KeyError:
                Debug.dl("evalgen_hydrographsd: cur_link_id: {0}, cur_timestamp: {1}".format(cur_link_id,
                                                                                             cur_timestamp),
                         10, debug_lvl)

            try:
                if cur_ref_content is not None:
                    if cur_link_id in cur_ref_content.keys():
                        if cur_link_id in ref_dict.keys():
                            if cur_timestamp in cur_ref_content[cur_link_id].keys():
                                Debug.dl("evalgen_hydrographsd: A found '{0}' in {1}".format(cur_timestamp,
                                                                                             cur_ref_content[cur_link_id].keys()),
                                         10, debug_lvl)
                                ref_dict[cur_link_id][cur_timestamp] = cur_ref_content[cur_link_id][cur_timestamp]
                            else:

                                if len(cur_ref_content[cur_link_id].keys()) > 0:
                                    temp_dists_to_current = [abs(c - cur_timestamp) for c in cur_ref_content[cur_link_id].keys()]
                                    min_idx_tmp = temp_dists_to_current.index(min(temp_dists_to_current))
                                    cur_timestamp_closest = cur_ref_content[cur_link_id].keys()[min_idx_tmp]
                                    ref_dict[cur_link_id][cur_timestamp_closest] = cur_ref_content[cur_link_id][cur_timestamp_closest]

                        else:
                            Debug.dl("evalgen_hydrographsd: B not found '{0}' in {1}".format(cur_link_id,
                                                                                             ref_dict.keys()),
                                     10, debug_lvl)
                    else:
                        Debug.dl("evalgen_hydrographsd: C not found '{0}' in {1}".format(cur_link_id,
                                                                                       cur_ref_content.keys()),
                                 10, debug_lvl)
            except KeyError:
                Debug.dl("evalgen_hydrographsd: cur_link_id: {0}, cur_timestamp: {1}".format(cur_link_id,
                                                                                             cur_timestamp),
                         10, debug_lvl)

        Debug.dl("evalgen_hydrographsd:    Ignoring {0} links for timestamp {1}.".format(count_ignored_linkid,
                                                                                         cur_timestamp), 9, debug_lvl)

        # exit()

    # for each link id, build dictionary
    for cur_link_id in all_link_ids:

        # get rating curve for link id, if available
        try:
            cur_rc = all_usgs_rc[cur_link_id]
        except KeyError:
            Debug.dl("evalgen_hydrographsd: Ignoring linkid {0} (no rating curve).".format(cur_link_id), 3, debug_lvl)
            continue

        # get thresholds for link id, if available
        cur_thr = None if cur_link_id not in all_stage_thresholds.keys() else all_stage_thresholds[cur_link_id]

        # get description and area for link id, if available
        cur_descarea = None if cur_link_id not in linkid_descarea_dict.keys() else linkid_descarea_dict[cur_link_id]
        cur_desc = cur_descarea["description"] if cur_descarea is not None else None
        try:
            cur_area = linkid_poisall_dict[cur_link_id][linkid_poisall_dict[cur_link_id].keys()[0]]["up_area"]
            # cur_area = cur_descarea["total_area"] if cur_descarea is not None else None
        except KeyError:
            cur_area = None

        Debug.dl("evalgen_hydrographsd: For link_id {0}, found {1} modeled, {2} reference data.".format(cur_link_id,
                                                                                                       len(mdl_dict[cur_link_id]),
                                                                                                       len(ref_dict[cur_link_id])),
                 2, debug_lvl)
        cur_out_file_path = output_filepath_frame.format(max(all_timestamps), cur_link_id)

        write_it(cur_link_id, ref_dict[cur_link_id], mdl_dict[cur_link_id], cur_out_file_path, cur_rc, sc_ref_prod,
                 pois_description=cur_desc, up_area=cur_area, thresholds=cur_thr, debug_lvl=debug_lvl)


def list_all_considered_linkids(reference_prod_folder_path, debug_lvl=0):
    """

    :param reference_prod_folder_path:
    :param debug_lvl:
    :return:
    """

    # get any file and read it
    cur_dict = None
    all_file_names = os.listdir(reference_prod_folder_path)
    for cur_filename in all_file_names:
        if cur_filename.endswith(".p"):
            cur_filepath = os.path.join(reference_prod_folder_path, cur_filename)
            with open(cur_filepath, "r") as r_file:
                cur_dict = pickle.load(r_file)
            break

    # basic check - no file readen
    if cur_dict is None:
        return None

    return cur_dict.keys()


def establish_timestamps_in_graph(mdl_prod_folder_path, ref_prod_folder_path, graph_interval, timestamp_step,
                                  timestamp_min=None, timestamp_max=None, debug_lvl=0):
    """
    ATTENTION: this is brute-forced to work with runsets. Must be generalized.
    :param mdl_prod_folder_path:
    :param ref_prod_folder_path:
    :param graph_interval:
    :param timestamp_step:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return:
    """

    # get the minimum and maximum timestamps available for model
    if (timestamp_min is None) or (timestamp_max is None):
        if not os.path.exists(mdl_prod_folder_path):
            return None
        all_mdl_filenames = os.listdir(mdl_prod_folder_path)
        if len(all_mdl_filenames) <= 0:
            return None
        all_mdl_filenames.sort()
        if timestamp_min is None:
            min_timestamp_mdl = FilenameDefinition.obtain_hist_file_timestamp(all_mdl_filenames[0])
        else:
            min_timestamp_mdl = timestamp_min
        if timestamp_max is None:
            max_timestamp_mdl = FilenameDefinition.obtain_hist_file_timestamp(all_mdl_filenames[-1])
        else:
            max_timestamp_mdl = timestamp_max
        graph_interval_limit = graph_interval
    else:
        min_timestamp_mdl = timestamp_min
        max_timestamp_mdl = timestamp_max
        graph_interval_limit = max_timestamp_mdl - min_timestamp_mdl

    # get the minimum and maximum timestamps available for reference
    all_ref_filenames = os.listdir(ref_prod_folder_path)
    if len(all_ref_filenames) <= 0:
        return None
    all_ref_filenames.sort()
    min_timestamp_ref = FilenameDefinition.obtain_hist_file_timestamp(all_ref_filenames[0])
    max_timestamp_ref = FilenameDefinition.obtain_hist_file_timestamp(all_ref_filenames[-1])

    # get the minimum and maximum timestamps global
    min_glb = max(min_timestamp_ref, min_timestamp_mdl)
    max_glb = min(max_timestamp_ref, max_timestamp_mdl)

    # check if time interval is bigger than the expected
    min_glb = min_glb if (max_glb - min_glb) <= graph_interval_limit else max_glb - graph_interval_limit

    Debug.dl("evalgen_hydrographsd: Graph interval: from {0} to {1}.".format(min_glb, max_glb), 3, debug_lvl)

    return range(min_glb, max_glb, timestamp_step)


def write_it(link_id, obs_timeseries_dict, mdl_timeseries_dict, out_file_path, rating_curve, reference_product_id,
             pois_description=None, up_area=None, thresholds=None, debug_lvl=0):
    """
    Writes the output json file with threshold stages, observed timeseries and modeled timeseries
    :param link_id:
    :param obs_timeseries_dict:
    :param mdl_timeseries_dict:
    :param out_file_path:
    :param rating_curve:
    :param reference_product_id:
    :param pois_description:
    :param debug_lvl:
    :return:
    """

    #
    all_disch, all_stage = extract_specific_disch_stage(rating_curve)

    # establish minimum/maximum x values to be used in the axis
    try:
        min_timestamp, max_timestamp = get_min_max_timestamps(mdl_timeseries_dict, obs_timeseries_dict)
    except ValueError:
        Debug.dl("evalgen_hydrographsd: Observed timeseries is empty for link id {0}.".format(link_id), 2, debug_lvl)
        return False

    # output obj
    output_obj = {}

    # plot modeled first
    all_mdl_tstamp = mdl_timeseries_dict.keys()
    all_mdl_tstamp.sort()
    mdl_set = []
    for cur_mdl_tstamp in all_mdl_tstamp:
        if (cur_mdl_tstamp > max_timestamp) or (cur_mdl_tstamp < min_timestamp):
            continue
        cur_disch = mdl_timeseries_dict[cur_mdl_tstamp]
        cur_stage = Interpolate.my_interpolation_xy(all_disch, all_stage, cur_disch * 35.315)
        mdl_set.append([cur_mdl_tstamp, cur_stage])
    output_obj['stage_mdl'] = mdl_set

    # plot observed first
    all_obs_tstamp = obs_timeseries_dict.keys()
    all_obs_tstamp.sort()
    obs_set = []
    for cur_obs_tstamp in all_obs_tstamp:
        if (cur_obs_tstamp > max_timestamp) or (cur_obs_tstamp < min_timestamp):
            continue
        if reference_product_id == "isq":
            cur_disch = obs_timeseries_dict[cur_obs_tstamp]
            cur_stage = Interpolate.my_interpolation_xy(all_disch, all_stage, cur_disch * 35.315)
        elif reference_product_id == "istg":
            cur_stage = obs_timeseries_dict[cur_obs_tstamp]
            if (cur_stage < 480) or (cur_stage > 1670):
                cur_stage *= 0.0833333    # from in to ft if value is unrealistic for ft
        else:
            cur_stage = None
        obs_set.append([cur_obs_tstamp, cur_stage])
    output_obj['stage_obs'] = obs_set

    Debug.dl("evalgen_hydrographsd: For link_id {0}: plot {1} modeled, {2} reference data.".format(
        link_id, len(output_obj['stage_mdl']), len(output_obj['stage_obs'])), 2, debug_lvl)

    # basic check: timeseries should not be empty
    if (len(output_obj['stage_mdl']) == 0) and (len(output_obj['stage_obs']) == 0):
        Debug.dl("evalgen_hydrographsd: No file writen for link: {0}.".format(link_id), 1, debug_lvl)
        return

    # check if units are compatible by comparing the means
    try:
        mean_mdl = 0
        for cur_mdl_pain in mdl_set:
            mean_mdl += cur_mdl_pain[1]
        mean_mdl = mean_mdl / len(mdl_set)
        mean_obs = 0
        for cur_obs_pain in obs_set:
            mean_obs += cur_obs_pain[1]
        mean_obs = mean_obs / len(obs_set)
        d = abs(mean_obs - mean_mdl)
        if d > 100:
            Debug.dl("evalgen_hydrographsd: SKIPPING link {0} (delta mdl x obs: {1}).".format(link_id, d),
                     1, debug_lvl)
    except TypeError:
        Debug.dl("evalgen_hydrographsd: SKIPPING link: {0} (unable to calculate delta).".format(link_id), 1, debug_lvl)

    # plot thresholds
    if thresholds is not None:
        try:
            output_obj['stage_threshold_act'] = (thresholds[1]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("evalgen_hydrographsd: Missing action thresholds for link_id {0}.".format(link_id), 2,
                     debug_lvl)
        try:
            output_obj['stage_threshold_fld'] = (thresholds[2]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("evalgen_hydrographsd: Missing flood thresholds for link_id {0}.".format(link_id), 2,
                     debug_lvl)
        try:
            output_obj['stage_threshold_mod'] = (thresholds[3]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("evalgen_hydrographsd: Missing moderate thresholds for link_id {0}.".format(link_id), 2,
                     debug_lvl)
        try:
            output_obj['stage_threshold_maj'] = (thresholds[4]-thresholds[0])*0.0833333  # in to ft
        except (TypeError, IndexError):
            Debug.dl("evalgen_hydrographsd: Missing major thresholds for link_id {0}.".format(link_id), 2,
                     debug_lvl)

    # set description and upstream area
    output_obj['pois_description'] = "" if pois_description is None else pois_description
    output_obj['up_area'] = "" if up_area is None else up_area

    # save it
    with open(out_file_path, "w+") as w_file:
        json.dump(output_obj, w_file)

    Debug.dl("evalgen_hydrographsd: File writen: {0}.".format(out_file_path), 1, debug_lvl)

    return True


def get_min_max_timestamps(dict_timeseries_mdl, obs_timeseries_dict, debug_lvl=0):
    """

    :param dict_timeseries_mdl:
    :param obs_timeseries_dict:
    :param debug_lvl:
    :return:
    """

    # start variables
    min_mdl_timestamp = -1
    max_mdl_timestamp = Decimal('Infinity')
    min_obs_timestamp = -1
    max_obs_timestamp = Decimal('Infinity')

    # view all modeled data
    if dict_timeseries_mdl is not None:
        all_mdl_timestamps = [int(float(key)) for key in dict_timeseries_mdl.keys()]
        min_mdl_timestamp = min(all_mdl_timestamps)
        max_mdl_timestamp = max(all_mdl_timestamps)

    # view all observed data
    if obs_timeseries_dict is not None:
        all_obs_timestamps = [int(float(key)) for key in obs_timeseries_dict.keys()]
        min_obs_timestamp = min(all_obs_timestamps)
        max_obs_timestamp = max(all_obs_timestamps)

    # establish limits and return them
    max_timestamp = min(max_mdl_timestamp, max_obs_timestamp)
    min_timestamp = max(min_mdl_timestamp, min_obs_timestamp)
    return min_timestamp, max_timestamp


def extract_specific_disch_stage(the_rc):
    """

    :param the_rc:
    :return:
    """

    all_disch = []
    all_stage = []
    for cur_rc_elem in the_rc:
        all_disch.append(cur_rc_elem[1])
        all_stage.append(cur_rc_elem[0])

    return all_disch, all_stage


# ####################################################### CALL ####################################################### #

plot_graphs(model_id_arg, reference_id_arg, timestamp_arg, runset_id_arg, graph_interval, timestamp_step,
            timestamp_min_arg, timestamp_max_arg, debug_lvl=debug_level_arg)

