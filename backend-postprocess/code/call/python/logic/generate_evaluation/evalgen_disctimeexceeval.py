import numpy as np
import datetime
import pickle
import json
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.BinAncillaryDefinition import BinAncillaryDefinition
from libs.AncillaryOnDemand import AncillaryOnDemand
from libs.FolderDefinition import FolderDefinition
from libs.EvalGenInterface import EvalGenInterface
from libs.FileDefinition import FileDefinition
from libs.BinDefinition import BinDefinition
from libs.Debug import Debug

debug_level_arg = 1
previous_days_arg = 10

# ####################################################### ARGS ####################################################### #

model_id_arg = EvalGenInterface.get_model_id(sys.argv)
timestamp_arg = EvalGenInterface.get_timestamp(sys.argv)
reference_id_arg = EvalGenInterface.get_reference_id(sys.argv)
runset_id_arg = EvalGenInterface.get_runset_id(sys.argv)


# #################################################### DEFS - ALL #################################################### #

def evaluate_disclas(sc_model_id, sc_reference_id, sc_runset_id, timestamp=None, debug_lvl=0):
    """

    :param sc_model_id: A model ID that has 'idq' product.
    :param sc_reference_id: A reference id that has 'isdc' product.
    :param sc_runset_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    # some constants
    sc_model_prod = "idq"
    sc_reference_prod = "isdc"
    sc_evaluation = "disctimeexceeval"
    link_latlng_filepath = BinAncillaryDefinition.get_linkids_latlng_file_path()

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    mdl_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, sc_model_prod,
                                                                        runset_id=sc_runset_id)
    ref_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_reference_id, sc_reference_prod,
                                                                        runset_id=sc_runset_id)

    # set up common timestamp
    if timestamp is not None:
        # check if requested timestamp is available for both model and reference
        # TODO - implement this case
        timestamp = timestamp
    else:
        cur_timestamp_mdl = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(mdl_folder_path)
        cur_timestamp_ref = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(ref_folder_path)

        # basic checks
        if cur_timestamp_mdl is None:
            Debug.dl("evalgen_disctimeexceeval: No files in {0} folder.".format(mdl_folder_path), 1, debug_lvl)
            return
        if cur_timestamp_ref is None:
            Debug.dl("evalgen_disctimeexceeval: No files in {0} folder.".format(ref_folder_path), 1, debug_lvl)
            return

        # establish common timestamp
        min_timestamp = min(cur_timestamp_mdl, cur_timestamp_mdl)
        if min_timestamp != cur_timestamp_mdl:
            cur_timestamp_mdl = FolderDefinition.retrive_closest_timestamp_in_hist_folder(mdl_folder_path,
                                                                                          min_timestamp,
                                                                                          accept_range=(29*60),
                                                                                          debug_lvl=10)
        if min_timestamp != cur_timestamp_ref:
            cur_timestamp_ref = FolderDefinition.retrive_closest_timestamp_in_hist_folder(ref_folder_path,
                                                                                          min_timestamp,
                                                                                          accept_range=(29*60),
                                                                                          debug_lvl=10)

        # basic check
        if (cur_timestamp_mdl is None) or (cur_timestamp_ref is None):
            Debug.dl("evalgen_disctimeexceeval: No common timestamp for {0} ('{1}' and '{2}').".format(min_timestamp,
                                                                                                       sc_model_id,
                                                                                                       sc_reference_id),
                     1, debug_lvl)
            return

    # define file paths
    ref_file_name = BinDefinition.define_file_name(cur_timestamp_ref, sc_reference_prod)
    mdl_file_path = os.path.join(mdl_folder_path, BinDefinition.define_file_name(cur_timestamp_mdl, sc_model_prod))
    ref_file_path = os.path.join(ref_folder_path, ref_file_name)

    # read selected files
    with open(mdl_file_path, 'rb') as mdl_file:
        Debug.dl("evalgen_disctimeexceeval: Reading Numpy file '{0}'.".format(mdl_file_path), 3, debug_lvl)
        mdl_data_raw = np.load(mdl_file)
    with open(ref_file_path, 'rb') as ref_file:
        Debug.dl("evalgen_disctimeexceeval: Readning Pickle file '{0}'.".format(ref_file_path), 3, debug_lvl)
        ref_data_cls = pickle.load(ref_file)

    # read classification ancillary data
    aod = AncillaryOnDemand()
    data_month = datetime.date.fromtimestamp(cur_timestamp_mdl).month
    thresholds = aod.get_qunit_thresholds(data_month)

    # prepares vectorizated function to generate list of classes
    def to_vect_classify_linkid(link_id, qraw_value):
        the_thresholds = thresholds[link_id]
        try:
            if qraw_value == 0:
                return 0
            elif qraw_value < the_thresholds[0]:
                return 1
            elif qraw_value < the_thresholds[1]:
                return 2
            elif qraw_value < the_thresholds[2]:
                return 3
            elif qraw_value < the_thresholds[3]:
                return 4
            else:
                return 5
        except IndexError:
            Debug.dl("evalgen_disctimeexceeval: IndexError - "
                     "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                        len(qraw_value), link_id))
            return None
        except ValueError:
            print("evalgen_disctimeexceeval: ValueError - "
                  "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                     len(qraw_value), link_id))
            return None
    mdl_data_cls = np.vectorize(to_vect_classify_linkid, otypes=[np.int])(range(0, len(mdl_data_raw)), mdl_data_raw)

    # read binary file of lat-long positions
    with open(link_latlng_filepath, "rb") as r_file:
        dict_latlng = pickle.load(r_file)

    eval_dict = {}

    # iterate over values, evaluating them
    for cur_linkid in ref_data_cls.keys():
        if (cur_linkid >= len(mdl_data_cls))or(ref_data_cls[cur_linkid] == 0)or(cur_linkid not in dict_latlng.keys()):
            continue

        # separate data
        cur_ref_raw = ref_data_cls[cur_linkid]
        cur_mdl_std = mdl_data_cls[cur_linkid]

        # standardize reference data
        if cur_ref_raw in (1, 2, 3):
            cur_ref_std = 1
        elif cur_ref_raw == 4:
            cur_ref_std = 2
        elif cur_ref_raw == 5:
            cur_ref_std = 3
        elif cur_ref_raw == 6:
            cur_ref_std = 4
        elif cur_ref_raw >= 7:
            cur_ref_std = 5

        # define comparison
        cur_eval_val = cur_mdl_std - cur_ref_std
        eval_dict[cur_linkid] = {'eval': cur_eval_val,
                                 'lat': dict_latlng[cur_linkid]['lat'],
                                 'lng': dict_latlng[cur_linkid]['lng']}

    # get destination folder
    json_folderpath = FolderDefinition.get_historical_eval_folder_path(sc_model_id, sc_evaluation, sc_reference_id,
                                                                       runset_id=sc_runset_id)
    if not os.path.exists(json_folderpath):
        os.makedirs(json_folderpath)

    # write json file
    json_filename = ref_file_name.replace('.p', '.json').replace(sc_reference_prod, sc_evaluation)  # TODO - do nicely
    json_filepath = os.path.join(json_folderpath, json_filename)
    with open(json_filepath, "w+") as w_file:
        json.dump(eval_dict, w_file)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("evalgen_disctimeexceeval: Wrote file {0} in {1} seconds.".format(json_filepath, d_time), 1, debug_lvl)


# ####################################################### CALL ####################################################### #

evaluate_disclas(model_id_arg, reference_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
