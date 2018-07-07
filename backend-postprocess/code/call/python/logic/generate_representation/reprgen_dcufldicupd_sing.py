from def_system import FolderDefinition, BinDefinition, LinksDefinition, ImageDefinition, Debug
from reprgen_disclausgsih_sing import WeightedMonths, build_exclusion_vector
from reprgen_lib import build_data_matrix, save_image_file, clean_folder
from reprgen_interface import ReprGenInterface
from def_onDemand import AncillaryOnDemand
import numpy as np
import datetime
import time
import sys
import csv
import os

debug_level_arg = 1

# ####################################################### ARGS ####################################################### #

model_id_arg = ReprGenInterface.get_model_id(sys.argv)
timestamp_arg = ReprGenInterface.get_timestamp_opt(sys.argv)
flextime_arg = ReprGenInterface.get_flextime(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)

# ####################################################### CLAS ####################################################### #


# ####################################################### DEFS ####################################################### #

def generate_representation(sc_model_id, timestamp, flextime=None, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param timestamp:
    :param flextime:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    requiered_product = 'idq'
    resulting_repres = 'dcufldicupd'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                         runset_id=runset_id)

    # establish the current timestamp
    if timestamp is not None:
        if flextime is None:
            cur_timestamp = timestamp
        else:
            cur_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path, timestamp,
                                                                                      accept_range=flextime)
    else:
        cur_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    # basic checks 1
    if cur_timestamp is None:
        Debug.dl("reprgen_dcufldicupd_sing: not a single iq bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return False

    # round timestamp for the closest previous midnight(end) and defines the initial time considered
    the_dt = datetime.datetime.fromtimestamp(cur_timestamp)
    the_dt = the_dt.replace(hour=0, minute=0, second=0)
    last_timestamp = int(time.mktime(the_dt.timetuple()))
    init_timestamp = last_timestamp - (24 * 60 * 60)

    # check if file already exists
    img_folder_path = FolderDefinition.get_historical_img_folder_path(sc_model_id, resulting_repres,
                                                                      runset_id=runset_id)
    img_file_name = ImageDefinition.define_historical_file_name(last_timestamp, resulting_repres)
    img_file_path = os.path.join(img_folder_path, img_file_name)
    if os.path.exists(img_file_path):
        Debug.dl("reprgen_pa03dcufldicupd_sing: file already exists '{0}' ".format(img_file_path), 1, debug_lvl)
        return None

    # read all files, updating the maximum discharge each iteration
    peak_data = None
    for cur_timestamp_round in range(init_timestamp, last_timestamp+1, 3600):
        cur_timestamp_effect = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path,
                                                                                         cur_timestamp_round,
                                                                                         accept_range=(29 * 60))
        if cur_timestamp_effect is None:
            continue
        cur_file_path = os.path.join(hist_folder_path,
                                     BinDefinition.define_file_name(cur_timestamp_effect, requiered_product))

        cur_np_data = np.load(cur_file_path)
        peak_data = cur_np_data if peak_data is None else np.maximum(cur_np_data, peak_data)

    # basic check - if no information found: give up
    if peak_data is None:
        return
    aod = AncillaryOnDemand()

    # classify discharge
    classes_vector = classify_discharge_index(aod, (last_timestamp - init_timestamp)/2, peak_data)

    # classify flood index
    floods_vector = classify_flood_index(aod, peak_data)

    # merge classifications
    mixed_vector = classify_mixed(classes_vector, floods_vector)

    # exclude mississipi and missuri
    ecl_vec = build_exclusion_vector(len(mixed_vector))
    mixed_vector = mixed_vector * ecl_vec

    # read mask
    mask = aod.get_linkid_link_mask()

    # plot the data
    bin_matrix = build_data_matrix(mask, mixed_vector, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, resulting_repres, bin_matrix, last_timestamp, runset_id=runset_id,
                    debug_lvl=debug_lvl)

    # debug info
    d_time = time.time() - start_time
    Debug.dl("reprgen_dcufldicupd_sing: generate_representation({0}) function took {1} seconds ".format(sc_model_id,
                                                                                                        d_time),
             1, debug_lvl)


def classify_discharge_index(aod, ref_timestamp, peak_data):

    w_months = WeightedMonths(ref_timestamp)
    thresholds_prev = aod.get_qunit_thresholds(w_months.get_prev_month())
    thresholds_next = aod.get_qunit_thresholds(w_months.get_next_month())
    thresholds = (thresholds_prev * w_months.get_prev_weight()) + (thresholds_next * w_months.get_next_weight())

    # prepares vectorizated function to generate list of classes
    def to_vect_classify_linkid(link_id, qraw_value):
        the_thresholds = thresholds[link_id]
        try:
            if qraw_value == 0:
                return -1
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
            Debug.dl("reprgen_dcufldicupd_sing: IndexError - "
                     "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                        len(qraw_value), link_id))
            return None
        except ValueError:
            print("reprgen_dcufldicupd_sing: ValueError - "
                  "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                     len(qraw_value), link_id))
            return None

    return np.vectorize(to_vect_classify_linkid, otypes=[np.int])(range(0, len(peak_data)), peak_data)


def classify_flood_index(aod, peak_data):

    thresholds = aod.get_fidx_thresholds()

    # ensures both 'thresholds' and 'q_raw' vectors have the same size
    max_link_id = min(len(peak_data), len(thresholds))
    the_data = qraw_value[0:max_link_id-1] if (len(peak_data) < max_link_id) else peak_data
    thresholds = thresholds[0:max_link_id-1] if (len(thresholds) < max_link_id) else thresholds

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
            Debug.dl("reprgen_fldidxusgsih_sing: "
                     "IndexError - type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                     len(qraw_value),
                                                                                                     link_id),
                     0, debug_lvl)
            return None
        except ValueError:
            Debug.dl("reprgen_fldidxusgsih_sing: "
                     "ValueError: type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                    len(qraw_value),
                                                                                                    link_id),
                     0, debug_lvl)
            return None

    return np.vectorize(to_vect_classify_linkid, otypes=[np.int])(range(0, len(the_data)), the_data)


def classify_mixed(disch_class, fldidx_class):
    """

    :param disch_class:
    :param fldidx_class:
    :return:
    """

    def to_vect_classify_linkid(d_data, f_data):
        return d_data if f_data <= 1 else f_data + 5

    return np.vectorize(to_vect_classify_linkid, otypes=[np.int])(disch_class, fldidx_class)


# ####################################################### CALL ####################################################### #

generate_representation(model_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
