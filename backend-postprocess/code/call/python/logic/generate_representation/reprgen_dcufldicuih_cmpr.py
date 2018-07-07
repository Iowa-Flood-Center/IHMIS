from def_system import FolderDefinition, BinDefinition, LinksDefinition, Debug
from reprgen_cmpr_lib import determine_timestamp_for_model, get_data_vector
from reprgen_lib import build_data_matrix, save_image_file, clean_folder
from reprgen_interface import ReprGenInterface
from def_onDemand import AncillaryOnDemand
from def_utils import GeneralUtils
import numpy as np
import datetime
import time
import sys
import os

debug_level_arg = 1

# ####################################################### ARGS ####################################################### #

comparison_id_arg = ReprGenInterface.get_model_id(sys.argv)
timestamp_arg = ReprGenInterface.get_timestamp_opt(sys.argv)
flextime_arg = ReprGenInterface.get_flextime(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)


# ####################################################### DEFS ####################################################### #

def generate_representation(sc_comparison_id, timestamp, flextime=None, runset_id=None, debug_lvl=0):
    """

    :param sc_comparison_id:
    :param timestamp:
    :param flextime:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    requiered_product = 'idq'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # gets the two models
    sc_model_1, sc_model_2 = FolderDefinition.extracts_models_acronym_from_combination(sc_comparison_id)

    # get timestamp for each model
    timestamp_1 = determine_timestamp_for_model(sc_model_1, timestamp, flextime=flextime, runset_id=runset_id,
                                                debug_lvl=debug_lvl)
    timestamp_2 = determine_timestamp_for_model(sc_model_2, timestamp, flextime=flextime, runset_id=runset_id,
                                                debug_lvl=debug_lvl)

    the_timestamp = GeneralUtils.round_timestamp_hour(min((timestamp_1, timestamp_2)))

    # define folders
    hist_t1_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_1, requiered_product,
                                                                            runset_id=runset_id)
    hist_t2_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_2, requiered_product,
                                                                            runset_id=runset_id)

    the_timestamp1 = timestamp_1 if timestamp_1 == the_timestamp else FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_t1_folder_path,
                                                                                                                                the_timestamp,
                                                                                                                                accept_range=flextime)
    the_timestamp2 = timestamp_2 if timestamp_2 == the_timestamp else FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_t2_folder_path,
                                                                                                                                the_timestamp,
                                                                                                                                accept_range=flextime)

    # read files
    the_data_1 = get_data_vector(sc_model_1, requiered_product, the_timestamp1, runset_id=runset_id,
                                 debug_lvl=debug_lvl)
    the_data_2 = get_data_vector(sc_model_2, requiered_product, the_timestamp2, runset_id=runset_id,
                                 debug_lvl=debug_lvl)

    # basic check
    if the_data_1 is None:
        Debug.dl("reprgen_disclausgsdih_cmpr: Unable to get a file for '{0}' at {1}.".format(sc_model_1, the_timestamp1),
             1, debug_lvl)
        return
    elif the_data_2 is None:
        Debug.dl("reprgen_disclausgsdih_cmpr: Unable to get a file for '{0}' at {1}.".format(sc_model_2, the_timestamp2),
             1, debug_lvl)
        return

    # trim vectors to have same size
    aod = AncillaryOnDemand()
    fldidx_thresholds = aod.get_fidx_thresholds()
    max_link_id = min(min(len(the_data_1), len(the_data_2)), len(fldidx_thresholds))
    the_data_1 = qraw_value[0:max_link_id-1] if (len(the_data_1) < max_link_id) else the_data_1
    the_data_2 = qraw_value[0:max_link_id-1] if (len(the_data_2) < max_link_id) else the_data_2
    fldidx_thresholds = fldidx_thresholds[0:max_link_id-1] if (len(fldidx_thresholds) < max_link_id) else fldidx_thresholds

    # classify flow and floods
    discla_1 = define_flow_classes(aod, the_data_1, the_timestamp)
    discla_2 = define_flow_classes(aod, the_data_2, the_timestamp)
    fldidx_1 = define_flood_indexes(the_data_1, fldidx_thresholds)
    fldidx_2 = define_flood_indexes(the_data_2, fldidx_thresholds)

    # unify classes
    def the_synthesis(discla, fldidx):
        return discla if fldidx < 2 else (4 + fldidx)
    the_synthesis_vect = np.vectorize(the_synthesis, otypes=[np.int])
    classes_vector_1 = the_synthesis_vect(discla_1, fldidx_1)
    classes_vector_2 = the_synthesis_vect(discla_2, fldidx_2)

    # perform comparison
    def the_comp(class_1, class_2):
        return class_1 - class_2 if (class_1 != 0) and (class_2 != 0) else -999
    the_comp_vec = np.vectorize(the_comp)
    classes_vector = the_comp_vec(classes_vector_1, classes_vector_2)

    # read mask
    mask = aod.get_linkid_link_mask()

    # plot the data
    bin_matrix = build_data_matrix(mask, classes_vector, debug_lvl=debug_lvl)
    save_image_file(sc_comparison_id, 'dcufldicuih', bin_matrix, the_timestamp, runset_id=runset_id,
                    debug_lvl=debug_lvl)

    # debug info
    d_time = time.time() - start_time
    Debug.dl("reprgen_disclausgsih_cmpr: generate_representation({0}) function took {1} seconds ".format(sc_comparison_id,
                                                                                                         d_time),
             1, debug_lvl)

    return


def define_flow_classes(aod, q_data_vector, the_timestamp):
    """

    :param aod:
    :param q_data_vector:
    :return:
    """

    data_month = datetime.date.fromtimestamp(the_timestamp).month - 1
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
            Debug.dl("reprgen_disclausgsdih_cmpr: IndexError - "
                     "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                        len(qraw_value), link_id))
            return None
        except ValueError:
            print("reprgen_disclausgsdih_cmpr: ValueError - "
                  "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                     len(qraw_value), link_id))
            return None

    # classify values
    classes_vector = np.vectorize(to_vect_classify_linkid, otypes=[np.int])(range(0, len(q_data_vector)), q_data_vector)
    return classes_vector


def define_flood_indexes(q_data_vector, thresholds):
    """

    :param q_data_vector:
    :param thresholds:
    :return:
    """

    # ensures both 'thresholds' and 'q_raw' vectors have the same size
    # the_data = qraw_value[0:max_link_id-1] if (len(q_data_vector) < max_link_id) else q_data_vector
    # thresholds = thresholds[0:max_link_id-1] if (len(thresholds) < max_link_id) else thresholds

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
            Debug.dl("reprgen_fldidxusgsih_cmpr: "
                     "IndexError - type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                     len(qraw_value),
                                                                                                     link_id),
                     0, debug_lvl)
            return None
        except ValueError:
            Debug.dl("reprgen_fldidxusgsih_cmpr: "
                     "ValueError: type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                    len(qraw_value),
                                                                                                    link_id),
                     0, debug_lvl)
            return None

    # classify values
    classes_vector = np.vectorize(to_vect_classify_linkid, otypes=[np.int])(range(0, len(q_data_vector)), q_data_vector)
    return classes_vector

# ####################################################### CALL ####################################################### #

generate_representation(comparison_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                        debug_lvl=debug_level_arg)
