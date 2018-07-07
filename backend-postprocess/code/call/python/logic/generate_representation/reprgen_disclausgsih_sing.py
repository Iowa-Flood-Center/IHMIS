import numpy as np
import datetime
import time
import sys
import csv
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from reprgen_lib import build_data_matrix, save_image_file, clean_folder
from libs.BinAncillaryDefinition import BinAncillaryDefinition
from libs.AncillaryOnDemand import AncillaryOnDemand
from libs.FolderDefinition import FolderDefinition
from libs.ReprGenInterface import ReprGenInterface
from libs.LinksDefinition import LinksDefinition
from libs.MetaFileManager import MetaFileManager
from libs.BinDefinition import BinDefinition
from libs.GeneralUtils import GeneralUtils
from libs.Debug import Debug

debug_level_arg = 1

# ####################################################### ARGS ####################################################### #

model_id_arg = ReprGenInterface.get_model_id(sys.argv)
timestamp_arg = ReprGenInterface.get_timestamp_opt(sys.argv)
flextime_arg = ReprGenInterface.get_flextime(sys.argv)
runset_id_arg = ReprGenInterface.get_runset_id(sys.argv)

# ####################################################### CLAS ####################################################### #


class WeightedMonths:
    _prev_month = None
    _next_month = None
    _prev_weight = None
    _next_weight = None

    def __init__(self, timestamp):

        # convert to date
        cur_date = datetime.datetime.fromtimestamp(timestamp)

        # weights
        cur_day = cur_date.day
        if cur_day == 15:
            delta_prev_month = delta_next_month = None
        elif cur_day < 15:
            self._prev_weight = float(15 - cur_day)/30
            self._next_weight = float(15 + cur_day)/30
            delta_prev_month = -1
            delta_next_month = 0
        else:
            self._prev_weight = float(45 - cur_day)/30
            self._next_weight = float(cur_day - 15)/30
            delta_prev_month = 0
            delta_next_month = 1

        #
        cur_month = cur_date.month
        if None not in (delta_prev_month, delta_next_month):
            prev_month = cur_month + delta_prev_month
            next_month = cur_month + delta_next_month
            self._prev_month = prev_month if prev_month > 0 else 12
            self._next_month = next_month if next_month < 13 else 1
        else:
            self._prev_weight = 0.5
            self._next_weight = 0.5
            self._prev_month = cur_month
            self._next_month = cur_month

    def get_prev_month(self):
        return self._prev_month

    def get_next_month(self):
        return self._next_month

    def get_prev_weight(self):
        return self._prev_weight

    def get_next_weight(self):
        return self._next_weight


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

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, requiered_product,
                                                                         runset_id=runset_id)

    # establish the current timestamp
    if timestamp is not None:
        if flextime is None:
            the_timestamp = timestamp
        else:
            the_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path, timestamp,
                                                                                      accept_range=flextime)
    else:
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    # basic checks 1
    if the_timestamp is None:
        Debug.dl("reprgen_disclausgsih_sing: not a single iq bin file for model {0}.".format(sc_model_id), 1, debug_lvl)
        return False

    filepath = os.path.join(hist_folder_path, BinDefinition.define_file_name(the_timestamp, requiered_product))

    # basich check 2
    if not os.path.exists(filepath):
        Debug.dl("reprgen_disclausgsih_sing: sl file not found ({0}).".format(filepath), 1, debug_lvl)
        return False

    # read data files
    the_data = np.load(filepath)

    # classify the flow
    aod = AncillaryOnDemand()
    # data_month = datetime.date.fromtimestamp(the_timestamp).month - 1
    # thresholds = aod.get_qunit_thresholds(data_month)

    w_months = WeightedMonths(the_timestamp)
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
            Debug.dl("reprgen_disclausgsih_sing: IndexError - "
                     "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                        len(qraw_value), link_id))
            return None
        except ValueError:
            print("reprgen_disclausgsih_sing: ValueError - "
                  "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                     len(qraw_value), link_id))
            return None

    classes_vector = np.vectorize(to_vect_classify_linkid, otypes=[np.int])(range(0, len(the_data)), the_data)

    # exclude mississipi and missuri
    ecl_vec = build_exclusion_vector(len(classes_vector))
    classes_vector = classes_vector * ecl_vec

    # read mask
    mask = aod.get_linkid_link_mask()

    # plot the data
    bin_matrix = build_data_matrix(mask, classes_vector, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, 'disclausgsih', bin_matrix, the_timestamp, runset_id=runset_id, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time() - start_time
    Debug.dl("reprgen_disclausgsih_sing: generate_representation({0}) function took {1} seconds ".format(sc_model_id,
                                                                                                         d_time),
             1, debug_lvl)

    return


def build_exclusion_vector(max_linkid):
    """

    :return:
    """

    # read file
    bin_file_path = BinAncillaryDefinition.get_linkids_missi_missu_file_path()
    if os.path.exists(bin_file_path):
        with open(bin_file_path, 'rb') as f:
            exc_list = np.load(f)
    else:
        exc_list = np.zeros(0, dtype=np.int)

    ret_list = np.ones(max_linkid, dtype=np.int)
    for cur_excluded in exc_list:
        ret_list[cur_excluded] = 0

    return ret_list


# ####################################################### CALL ####################################################### #

if __name__ == "__main__":
    generate_representation(model_id_arg, timestamp_arg, flextime=flextime_arg, runset_id=runset_id_arg,
                            debug_lvl=debug_level_arg)
