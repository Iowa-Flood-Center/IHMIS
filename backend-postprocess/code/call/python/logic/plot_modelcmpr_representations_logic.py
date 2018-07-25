import numpy as np
import datetime
import os

from generate_representation.reprgen_lib import save_image_file, build_data_matrix
from libs.AncillaryOnDemand import AncillaryOnDemand
from libs.ParamDisclausgsih import ParamDisclausgsih
from libs.ParamFldidxusgsih import ParamFldidxusgsih
from libs.FolderDefinition import FolderDefinition
from libs.MetaFileManager import MetaFileManager
from libs.ImageDefinition import ImageDefinition
from libs.BinDefinition import BinDefinition
from libs.ColorProvider import ColorProvider
from libs.Debug import Debug


# from def_onDemand import AncillaryOnDemand, ParamDisclausgsih, ParamFldidxusgsih, build_data_matrix, save_image_file


# #################################################################################################################### #
# ####################################################### DEFS ####################################################### #
# #################################################################################################################### #


def generate_cmprsimp_representations(comparison_acronyms, unix_timestamp, runset_id, debug_lvl=0):
    """

    :param comparison_acronyms: List of comparisons strings ("MODEL1_MODEL2", "MODEL2_MODEL1", ...)
    :param unix_timestamp:
    :param debug_lvl:
    :return:
    """

    on_demand = AncillaryOnDemand()
    meta_mngr = MetaFileManager(runset_id=runset_id)
    meta_mngr.load_comparison_matrix(debug_lvl=debug_lvl)
    meta_mngr.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)

    for cur_comparison_acronym in comparison_acronyms:

        # gets both models names
        both_models = FolderDefinition.extracts_models_acronym_from_combination(cur_comparison_acronym)
        if both_models is None:
            Debug.dl("plot_modelcmpr_representations_logic: {0} is not a valid comparison acronym.".format(comparison_acronym),
                 0, debug_lvl)
            return
        cur_sc_model_1 = both_models[0]
        cur_sc_model_2 = both_models[1]
        all_parameters = meta_mngr.get_all_representations_of_comparison(comparison_acronym=cur_comparison_acronym,
                                                                         debug_lvl=debug_lvl)

        for cur_repr_id in all_parameters:
            reprgen_script = meta_mngr.get_genscript_of_representation_cmpr(cur_repr_id, debug_lvl=debug_lvl)
            the_timestamp = "" if unix_timestamp is None else unix_timestamp
            the_runsetid = "" if runset_id is None else "-runsetid {0}".format(runset_id)
            if reprgen_script is not None:
                call_command = "{0} {1} {2} {3}".format(reprgen_script, cur_comparison_acronym, the_timestamp,
                                                        the_runsetid)
                Debug.dl("plot_modelcmpr_representations_logic: Calling '{0}' ({1}).".format(call_command, cur_repr_id),
                         2, debug_lvl)
                os.system(call_command)
            else:
                Debug.dl("plot_modelcmpr_representations_logic: Not comparison script available for '{0}'.".format(
                    cur_repr_id),
                         1, debug_lvl)


def generate_cmprsimp_representations_hist(meta_mngr, comparison_acronyms, runset_id, timestamp_min=None,
                                           timestamp_max=None, debug_lvl=0):
    """

    :param meta_mngr:
    :param models_id:
    :param runset_id:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return:
    """

    timestep = 3600

    # load meta data
    meta_mngr.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)
    meta_mngr.load_scrunset_meta_info(debug_lvl=debug_lvl)

    #
    min_timestamp = meta_mngr.get_runset_timestamp_ini() if timestamp_min is None else timestamp_min
    max_timestamp = meta_mngr.get_runset_timestamp_end() if timestamp_max is None else timestamp_max

    # basic check
    if (min_timestamp is None) or (max_timestamp is None):
        Debug.dl("plot_modelcmpr_representations_logic: Missing one time constrain (min:{0}, max{1}).".format(
            min_timestamp, max_timestamp), 0, debug_lvl)
        return

    #
    all_timestamps = range(min_timestamp, max_timestamp, timestep)
    if len(all_timestamps) == 0:
        Debug.dl("plot_modelcmpr_representations_logic: No internal dates between {0} and {1}.".format(
            min_timestamp, max_timestamp), 0, debug_lvl)
        return

    for cur_comparison_acronym in comparison_acronyms:

        # gets both models names
        both_models = FolderDefinition.extracts_models_acronym_from_combination(cur_comparison_acronym)
        if both_models is None:
            Debug.dl("plot_modelcmpr_representations_logic: {0} is not a valid comparison acronym.".format(comparison_acronym),
                 0, debug_lvl)
            return

        cur_sc_model_1 = both_models[0]
        cur_sc_model_2 = both_models[1]
        all_representations = meta_mngr.get_all_representations_of_comparison(comparison_acronym=cur_comparison_acronym,
                                                                              debug_lvl=debug_lvl)

        for cur_repr_id in all_representations:

            for cur_timestamp in all_timestamps:
                reprgen_script = meta_mngr.get_genscript_of_representation_cmpr(cur_repr_id, debug_lvl=debug_lvl)
                if reprgen_script is not None:
                    call_command = "{0} {1} -t {2} -runsetid {3}".format(reprgen_script, cur_comparison_acronym,
                                                                         cur_timestamp, runset_id)
                    Debug.dl("plot_modelcmpr_representations_logic: Calling '{0}' ({1}).".format(call_command, cur_repr_id),
                             2, debug_lvl)
                    os.system(call_command)
                else:
                    Debug.dl("plot_modelcmpr_representations_logic: Not comparison script available for '{0}'.".format(
                        cur_repr_id), 1, debug_lvl)


def plot_preacchil24hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'preacchil24hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)


def plot_preacchil12hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'preacchil12hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)

def plot_preacchil06hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'preacchil06hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)

def plot_preacchil03hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'preacchil03hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)

def plot_runacchil24hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'runacchil24hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)


def plot_runacchil12hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'runacchil12hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)


def plot_runacchil06hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'runacchil06hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)


def plot_runacchil03hh(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'runacchil03hh'
    plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod,
                       debug_lvl=debug_lvl)


def plot_soiwac20ih(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'soiwac20ih'

    # identifies timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_1, sc_model_2, param_acronym, debug_lvl=debug_lvl)
        if the_timestamp is None:
            return

    # read data from binary files
    sc_model_1_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_1, param_acronym, the_timestamp)
    sc_model_2_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_2, param_acronym, the_timestamp)
    considered_1_data = np.load(sc_model_1_bin_filepath)
    considered_2_data = np.load(sc_model_2_bin_filepath)

    # generates difference vector
    diff_vector = (considered_1_data - considered_2_data) * 1000

    # translate difference vector into matrix and plot it
    diff_matrix = build_data_matrix(aod.get_linkid_hills_mask(), diff_vector, debug_lvl=debug_lvl)
    save_image_file(combination_acronym, param_acronym, diff_matrix, the_timestamp, most_recent=False, debug_lvl=0)


def plot_soimoi20ih(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_acronym = 'soimoi20ih'

    # identifies timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_1, sc_model_2, param_acronym, debug_lvl=debug_lvl)
        if the_timestamp is None:
            return

    # read data from binary files
    sc_model_1_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_1, param_acronym, the_timestamp)
    sc_model_2_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_2, param_acronym, the_timestamp)
    considered_1_data = np.load(sc_model_1_bin_filepath)
    considered_2_data = np.load(sc_model_2_bin_filepath)

    # function to be vectorized
    def compare_to_vect(model1_value, model2_value):
        if (model1_value == 0) and (model2_value == 0):
            return 1
        elif (model1_value != 0) and (model2_value == 0):
            return 0
        else:
            ret_value = model1_value / model2_value
            return ret_value

    # generates difference vector
    diff_vector = np.vectorize(compare_to_vect, otypes=[np.float])(considered_1_data, considered_2_data)

    # translate difference vector into matrix and plot it
    diff_matrix = build_data_matrix(aod.get_linkid_hills_mask(), diff_vector, debug_lvl=debug_lvl)
    save_image_file(combination_acronym, param_acronym, diff_matrix, the_timestamp, most_recent=False, debug_lvl=0)


def plot_disclausgsih(sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_source = 'disrawih'
    param_acronym = 'disclausgsih'

    # identifies timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_1, sc_model_2, param_source, debug_lvl=debug_lvl)
        if the_timestamp is None:
            return

    # read data from binary files
    sc_model_1_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_1, param_source, the_timestamp)
    sc_model_2_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_2, param_source, the_timestamp)
    considered_1_data = np.load(sc_model_1_bin_filepath)
    considered_2_data = np.load(sc_model_2_bin_filepath)

    ParamDisclausgsih.set_ancillary_on_demand(aod)
    ParamDisclausgsih.set_data_month(datetime.date.fromtimestamp(the_timestamp).month - 1)

    model_1_classes = np.vectorize(ParamDisclausgsih.to_vect_classify, otypes=[np.float])(range(0, len(considered_1_data)),
                                                                                          considered_1_data)
    model_2_classes = np.vectorize(ParamDisclausgsih.to_vect_classify, otypes=[np.float])(range(0, len(considered_2_data)),
                                                                                          considered_2_data)

    # generates difference vector
    diff_vector = model_1_classes - model_2_classes

    # translate difference vector into matrix and plot it.
    diff_matrix = build_data_matrix(aod.get_linkid_link_mask(), diff_vector, debug_lvl=debug_lvl)
    save_image_file(combination_acronym, param_acronym, diff_matrix, the_timestamp, most_recent=False, debug_lvl=0)


def plot_fldidxusgsih(sc_model_1, sc_model_2, comparison_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_1:
    :param sc_model_2:
    :param comparison_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """
    param_source = 'disrawih'
    param_acronym = 'fldidxusgsih'

    # identifies timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_1, sc_model_2, param_source, debug_lvl=debug_lvl)
        if the_timestamp is None:
            return

    # read data from binary files
    sc_model_1_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_1, param_source, the_timestamp)
    sc_model_2_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_2, param_source, the_timestamp)
    considered_1_data = np.load(sc_model_1_bin_filepath)
    considered_2_data = np.load(sc_model_2_bin_filepath)

    ParamFldidxusgsih.set_ancillary_on_demand(aod)

    model_1_classes = np.vectorize(ParamFldidxusgsih.to_vect_classify, otypes=[np.float])(range(0, len(considered_1_data)),
                                                                                          considered_1_data)
    model_2_classes = np.vectorize(ParamFldidxusgsih.to_vect_classify, otypes=[np.float])(range(0, len(considered_2_data)),
                                                                                          considered_2_data)

    # generates difference vector
    diff_vector = model_1_classes - model_2_classes

    # translate difference vector into matrix and plot it
    diff_matrix = build_data_matrix(aod.get_linkid_link_mask(), diff_vector, debug_lvl=debug_lvl)
    save_image_file(comparison_acronym, param_acronym, diff_matrix, the_timestamp, most_recent=False, debug_lvl=0)


def plot_preacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param param_acronym:
    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """

    # identifies timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_1, sc_model_2, param_acronym, debug_lvl=debug_lvl)
        if the_timestamp is None:
            return

    # performs comparison
    sc_model_1_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_1, param_acronym, the_timestamp)
    sc_model_2_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_2, param_acronym, the_timestamp)

    # load data
    considered_1_data = np.load(sc_model_1_bin_filepath)
    considered_2_data = np.load(sc_model_2_bin_filepath)

    # generates difference vector
    diff_vector = considered_1_data - considered_2_data

    # translate difference vector into matrix
    diff_matrix = build_data_matrix(aod.get_linkid_hills_mask(), diff_vector, debug_lvl=debug_lvl)

    # get rgba vector
    save_image_file(combination_acronym, param_acronym, diff_matrix, the_timestamp, most_recent=False, debug_lvl=0)


def plot_runacchilXXhh(param_acronym, sc_model_1, sc_model_2, combination_acronym, unix_timestamp, aod, debug_lvl=0):
    """

    :param param_acronym:
    :param sc_model_1:
    :param sc_model_2:
    :param combination_acronym:
    :param unix_timestamp:
    :param aod:
    :param debug_lvl:
    :return:
    """

    # identifies timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_1, sc_model_2, param_acronym, debug_lvl=debug_lvl)
        if the_timestamp is None:
            return

    # performs comparison
    sc_model_1_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_1, param_acronym, the_timestamp)
    sc_model_2_bin_filepath = FolderDefinition.get_intermediate_bin_file_path(sc_model_2, param_acronym, the_timestamp)

    # load data
    considered_1_data = np.load(sc_model_1_bin_filepath)
    considered_2_data = np.load(sc_model_2_bin_filepath)

    # generates difference vector
    diff_vector = considered_1_data - considered_2_data

    # translate difference vector into matrix
    diff_matrix = build_data_matrix(aod.get_linkid_hills_mask(), diff_vector, debug_lvl=debug_lvl)

    # get rgba vector
    save_image_file(combination_acronym, param_acronym, diff_matrix, the_timestamp, most_recent=False, debug_lvl=0)


def get_most_recent_timestamp_between(sc_model_id1, sc_model_id2, param_id, debug_lvl=0):
    """

    :param sc_model_id1:
    :param sc_model_id2:
    :param param_id:
    :param debug_lvl:
    :return:
    """

    hist_folder_path_1 = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id1, param_id)
    the_timestamp_1 = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path_1)

    hist_folder_path_2 = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id2, param_id)
    the_timestamp_2 = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path_2)

    # the the biggest present in both
    if (the_timestamp_1 is not None) and (the_timestamp_2 is not None):
        if the_timestamp_1 == the_timestamp_2:
            return the_timestamp_2
        else:
            c_max = min([the_timestamp_1, the_timestamp_2])
            return c_max if check_both_exists(sc_model_id1, sc_model_id2, param_id, c_max, debug_lvl=debug_lvl) else None

    # if something is missing, Debug it and return None
    if the_timestamp_1 is None:
        Debug.dl("plot_modelcmpr_representations_logic: "
                 "Not a single image for '{0}', model '{1}'. Skipping composition.".format(param_id, sc_model_id1),
                 1, debug_lvl)
    if the_timestamp_2 is None:
        Debug.dl("plot_modelcmpr_representations_logic: "
                 "Not a single image for '{0}', model '{1}'. Skipping composition.".format(param_id, sc_model_id2),
                 1, debug_lvl)

    return None


def check_both_exists(sc_model_id1, sc_model_id2, param_id, unix_timestamp, debug_lvl=0):
    """

    :param sc_model_id1:
    :param sc_model_id2:
    :param param_id:
    :param unix_timestamp:
    :param debug_lvl:
    :return:
    """
    file1_exists = FolderDefinition.check_intermediate_bin_file_exists(sc_model_id1, param_id, unix_timestamp)
    file2_exists = FolderDefinition.check_intermediate_bin_file_exists(sc_model_id2, param_id, unix_timestamp)
    if file1_exists and file2_exists:
        Debug.dl("plot_modelcmpr_representations_logic: files for both {0}, {1} models exist for {2} at {3}".format(
            sc_model_id1, sc_model_id2, param_id, unix_timestamp
        ), 2, debug_lvl)
        return True
    else:
        Debug.dl("plot_modelcmpr_representations_logic: no common files for {0}, {1} models exist for {2} at {3}".format(
            sc_model_id1, sc_model_id2, param_id, unix_timestamp
        ), 2, debug_lvl)
        return False
