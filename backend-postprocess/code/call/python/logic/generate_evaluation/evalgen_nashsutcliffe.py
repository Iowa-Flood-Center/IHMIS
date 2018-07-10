import numpy as np
import pickle
import json
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.FilenameDefinition import FilenameDefinition
from libs.FolderDefinition import FolderDefinition
from libs.EvalGenInterface import EvalGenInterface
from libs.FileDefinition import FileDefinition
from libs.GeneralUtils import GeneralUtils
from libs.Hydrographs import Hydrographs
from libs.Interpolate import Interpolate
from libs.Debug import Debug


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

def calculate_mec(model_id, reference_id, timestamp, runset_id, graph_interval, timestamp_step, timestamp_min,
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

    sc_mdl_prod = "idq"
    sc_ref_prods = ["isq", "istg"]
    sc_eval_repr = "nashsutcliffe"

    mdl_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=sc_mdl_prod,
                                                                             runset_id=runset_id)

    Debug.dl("evalgen_nashsutcliffe: reading modeled data from '{0}'.".format(mdl_prod_folder_path), 1, debug_lvl)

    # searches available reference product
    # TODO - replace folder-search by meta-file reading
    sc_ref_prod = None
    ref_prod_folder_path = None
    for cur_possible_ref_prod in sc_ref_prods:
        ref_prod_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=reference_id,
                                                                                 product_id=cur_possible_ref_prod,
                                                                                 runset_id=runset_id)
        Debug.dl("evalgen_nashsutcliffe: prod '{0}.{1}' is at '{2}'.".format(reference_id, cur_possible_ref_prod,
                                                                             ref_prod_folder_path),
                 1, debug_lvl)
        if os.path.exists(ref_prod_folder_path):
            sc_ref_prod = cur_possible_ref_prod
            break
        else:
            ref_prod_folder_path = None

    # check if it is possible to continue
    if ref_prod_folder_path is not None:
        Debug.dl("evalgen_nashsutcliffe: using '{0}' of '{1}' for {2}.{3})".format(sc_ref_prod, reference_id,
                                                                                   runset_id, model_id), 3, debug_lvl)
        Debug.dl("evalgen_nashsutcliffe: reading observed data from '{0}'.".format(ref_prod_folder_path), 1, debug_lvl)
    else:
        Debug.dl("evalgen_nashsutcliffe: not found a valid product of '{0}' for '{1}' ({2})".format(reference_id,
                                                                                                    model_id,
                                                                                                    runset_id),
                 3, debug_lvl)
        return

    # if necessary, load rating curves
    all_usgs_rc = Hydrographs.get_all_usgs_rating_curves(debug_lvl=debug_lvl) if sc_ref_prod == "istg" else None

    # TODO - use proper def_sys commands
    mdl_prod_file_path = os.path.join(mdl_prod_folder_path, "{0}{1}.npy")
    ref_prod_file_path = os.path.join(ref_prod_folder_path, "{0}{1}.p")

    # define output folder path and ensure it exists - create it if necessary
    output_filepath_folder_path = FolderDefinition.get_historical_eval_folder_path(model_id, sc_eval_repr, reference_id,
                                                                                   runset_id=runset_id)
    if not os.path.exists(output_filepath_folder_path):
        os.makedirs(output_filepath_folder_path)
    # TODO - use proper def_sys commands
    output_filepath_frame = os.path.join(output_filepath_folder_path, "{0}{1}.json")

    # define

    # list all link_ids
    all_link_ids = list_all_considered_linkids(ref_prod_folder_path, debug_lvl=debug_lvl)

    # define possible time interval
    potential_timestamps = establish_potential_timestamps(mdl_prod_folder_path, ref_prod_folder_path, graph_interval,
                                                          timestamp_step, timestamp_min=timestamp_min,
                                                          timestamp_max=timestamp_max, debug_lvl=debug_lvl)

    # basic check
    if (potential_timestamps is None) or (len(potential_timestamps) == 0):
        Debug.dl("evalgen_nashsutcliffe: unable to establish potential timestamps.", 3, debug_lvl)
        return

    # build dictionary of modeled and reference data
    modeled_data = {}
    reference_data = {}
    reference_data_avg_support = []
    for cur_timestamp in potential_timestamps:

        # open model data file
        cur_effective_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_prod_folder_path,
                                                                                            cur_timestamp)
        cur_mdl_file_path = mdl_prod_file_path.format(cur_effective_timestamp, sc_mdl_prod)
        with open(cur_mdl_file_path, "rb") as r_file_mdl:
            cur_mdl_content = np.load(r_file_mdl)

        # print("Opened '{0}'".format(cur_mdl_file_path))

        # gather only the information related to relevant link ids
        for cur_link_in in all_link_ids:
            if cur_link_in >= len(cur_mdl_content):
                continue
            if cur_link_in not in modeled_data.keys():
                modeled_data[cur_link_in] = {}
            cur_rounded_timestamp = GeneralUtils.round_timestamp_hour(cur_effective_timestamp)
            modeled_data[cur_link_in][cur_rounded_timestamp] = cur_mdl_content[cur_link_in]

        # open observed data
        cur_effective_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(ref_prod_folder_path,
                                                                                            cur_timestamp)
        cur_ref_file_path = ref_prod_file_path.format(cur_effective_timestamp, sc_ref_prod)
        if not os.path.exists(cur_ref_file_path):
            continue
        with open(cur_ref_file_path, "rb") as r_file_mdl:
            cur_ref_content = pickle.load(r_file_mdl)

        for cur_link_in in all_link_ids:
            if cur_link_in not in reference_data.keys():
                reference_data[cur_link_in] = {}
            cur_rounded_timestamp = GeneralUtils.round_timestamp_hour(cur_effective_timestamp)

            # print("From '{0}'".format(cur_ref_file_path))
            # print("Adding {0}".format(cur_ref_content[cur_link_in]))
            try:
                cur_max_timestamp = max(cur_ref_content[cur_link_in].keys())
            except ValueError:
                # print("Ignoring link id {0}.".format(cur_link_in))
                continue
            except KeyError:
                Debug.dl("evalgen_nashsutcliffe: No link {0} in {1}.{2}.".format(cur_link_in, runset_id, reference_id),
                         3, debug_lvl)
                continue
            # print("Add {0}->{1}".format(cur_max_timestamp, cur_ref_content[cur_link_in][cur_max_timestamp]))
            if cur_rounded_timestamp in cur_ref_content[cur_link_in].keys():
                reference_data[cur_link_in][cur_rounded_timestamp] = cur_ref_content[cur_link_in][cur_rounded_timestamp]
            else:
                reference_data[cur_link_in][cur_rounded_timestamp] = cur_ref_content[cur_link_in][cur_max_timestamp]
            # return

    # from built dictionary, calculate Nash Stutcliffe for each link id
    ns_dict = {}
    max_of_max_timestamps = None
    for cur_link_id in all_link_ids:
        if not ((cur_link_id in modeled_data.keys()) and (cur_link_id in reference_data.keys())):
            Debug.dl("evalgen_nashsutcliffe: Ignoring link id {0} - missing model or reference data.".format(cur_link_id),
                     3, debug_lvl)
            continue

        # ensure reference data is in q
        if sc_ref_prod == "istg":
            if cur_link_id not in all_usgs_rc.keys():
                # print("Ignoring link id {0}: no USGS rating curve.".format(cur_link_id))
                continue
            cur_dischs_rc, cur_stages_rc = Hydrographs.extract_specific_disch_stage(all_usgs_rc[cur_link_id])
            for cur_timestamp in reference_data[cur_link_id].keys():
                cur_t_s = reference_data[cur_link_id][cur_timestamp] * 0.0833333               # from in to ft
                cur_t_q = Interpolate.my_interpolation_xy(cur_stages_rc, cur_dischs_rc, cur_t_s) / 35.315  # from cfs to cms
                reference_data[cur_link_id][cur_timestamp] = cur_t_q

        # perform nash algorithm and add to the writing list
        cur_mean_obs = np.mean(reference_data[cur_link_id].values())
        cur_form_up = 0
        cur_form_down = 0
        cur_min_timestamp = None
        cur_max_timestamp = None
        cur_number_values = 0
        for cur_timestamp in modeled_data[cur_link_id].keys():
            if cur_timestamp not in reference_data[cur_link_id].keys():
                continue
            cur_form_up += (modeled_data[cur_link_id][cur_timestamp] - reference_data[cur_link_id][cur_timestamp])**2
            cur_form_down += (reference_data[cur_link_id][cur_timestamp] - cur_mean_obs)**2

            # delete this debug
            if (sc_ref_prod == "isq") and (cur_link_id == 367769):
                print("For link {0} at {1}:".format(cur_link_id, cur_timestamp))
                print("  up: ({0} - {1})^2 = {2}".format(modeled_data[cur_link_id][cur_timestamp],
                                                         reference_data[cur_link_id][cur_timestamp], cur_form_up))
                print("  dw: ({0} - {1})^2 = {2}".format(reference_data[cur_link_id][cur_timestamp],
                                                         cur_mean_obs, cur_form_down))

            if (cur_min_timestamp is None) or (cur_min_timestamp > cur_timestamp):
                cur_min_timestamp = cur_timestamp
            else:
                cur_min_timestamp = cur_max_timestamp
            if (cur_max_timestamp is None) or (cur_max_timestamp < cur_timestamp):
                cur_max_timestamp = cur_timestamp
            else:
                cur_max_timestamp = cur_max_timestamp
            cur_number_values += 1
        cur_nscoef = 1-(cur_form_up / cur_form_down) if cur_form_down > 0 else -1
        ns_dict[cur_link_id] = {"ns_coeff": cur_nscoef,
                                "min_timestamp": cur_min_timestamp,
                                "max_timestamp": cur_max_timestamp,
                                "num_values": cur_number_values}

        # update maximum of maximum timestamp
        if (max_of_max_timestamps is None) or (max_of_max_timestamps < cur_max_timestamp):
            max_of_max_timestamps = cur_max_timestamp

    w_file_path = output_filepath_frame.format(max_of_max_timestamps, sc_eval_repr)
    with open(w_file_path, "w+") as w_file:
        json.dump(ns_dict, w_file)

    Debug.dl("evalgen_nashsutcliffe: Wrote file '{0}'.".format(w_file_path), 3, debug_lvl)


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
        Debug.dl("evalgen_nashsutcliffe: Not found any file at '{0}'.".format(reference_prod_folder_path), 1, debug_lvl)
        return None

    return [int(cur_key) for cur_key in cur_dict.keys()]


def establish_potential_timestamps(mdl_prod_folder_path, ref_prod_folder_path, graph_interval, timestamp_step,
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

        interval_limit = graph_interval
    else:
        min_timestamp_mdl = timestamp_min
        max_timestamp_mdl = timestamp_max
        interval_limit = max_timestamp_mdl - min_timestamp_mdl

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
    min_glb = min_glb if (max_glb - min_glb) <= interval_limit else max_glb - interval_limit

    Debug.dl("evalgen_hydrographsd: Eval interval: from {0} to {1}.".format(min_glb, max_glb), 3, debug_lvl)

    return range(min_glb, max_glb, timestamp_step)


# ####################################################### CALL ####################################################### #

calculate_mec(model_id_arg, reference_id_arg, timestamp_arg, runset_id_arg, graph_interval, timestamp_step,
              timestamp_min_arg, timestamp_max_arg, debug_lvl=debug_level_arg)
