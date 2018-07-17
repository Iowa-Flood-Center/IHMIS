import numpy as np
import datetime
import time
import os

from libs.BinAncillaryDefinition import BinAncillaryDefinition
from libs.AncillaryOnDemand import AncillaryOnDemand
from libs.FolderDefinition import FolderDefinition
from libs.ImageDefinition import ImageDefinition
from libs.MetaFileManager import MetaFileManager
from libs.ColorProvider import ColorProvider
from libs.Debug import Debug


# #################################################################################################################### #
# ####################################################### DEFS ####################################################### #
# #################################################################################################################### #


def generate_singsimp_representations(sc_models_ids, sc_runset_id, unix_timestamp, debug_lvl=0):
    """

    :param sc_models_ids:
    :param sc_runset_id:
    :param unix_timestamp:
    :param debug_lvl:
    :return:
    """

    # basic check
    if (sc_models_ids is None) or (type(sc_models_ids) is not list):
        Debug.dl("plot_modelsing_representations_logic: First argument must be a list of sc_model_ids.", 0, debug_lvl)
        return

    # basic check
    if sc_runset_id is None:
        Debug.dl("plot_modelsing_representations_logic: Invalid runset_id: '{0}'.".format(sc_runset_id), 0, debug_lvl)
        return

    # creating guiding objects
    meta_mng = MetaFileManager(runset_id=sc_runset_id)
    meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
    meta_mng.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)

    # preparing arguments
    the_timestamp_arg = "" if unix_timestamp is None else "-t {0}".format(unix_timestamp)
    cur_runset_arg = "-runsetid {0}".format(sc_runset_id)

    # for each representation of each module, run its plotting function
    for cur_sc_model_id in sc_models_ids:

        cur_repr_ids = meta_mng.get_all_representations_of_scmodel(cur_sc_model_id)

        if cur_repr_ids is None:
            continue

        for cur_repr_id in cur_repr_ids:
            Debug.dl("plot_modelsing_representations_logic: Getting genscript for representation '{0}'.".format(cur_repr_id), 2, debug_lvl)
            reprgen_script = meta_mng.get_genscript_of_representation_sing(cur_repr_id)
            if reprgen_script is None:
                Debug.dl("plot_modelsing_representations_logic: Skipping plotting for {0} - None script".format(
                    cur_repr_id), 2, debug_lvl)
                continue
            elif reprgen_script.strip() == "":
                Debug.dl("plot_modelsing_representations_logic: Skipping plotting for {0} - '' script".format(
                    cur_repr_id), 2, debug_lvl)
                continue

            call_command = "{0} {1} {2} {3}".format(reprgen_script, cur_sc_model_id, the_timestamp_arg, cur_runset_arg)

            Debug.dl("plot_modelsing_representations_logic: CALL '{0}' ({1}).".format(call_command, cur_repr_id),
                     2, debug_lvl)
            os.system(call_command)


def generate_singsimp_representations_hist(sc_models_ids, runset_id=None, timestamp_min=None, timestamp_max=None,
                                           debug_lvl=0):
    """

    :param sc_models_ids:
    :param runset_id:
    :param timestamp_min:
    :param timestamp_max:
    :param debug_lvl:
    :return:
    """

    # basic check
    if (sc_models_ids is None) or (type(sc_models_ids) is not list):
        Debug.dl("plot_modelsing_representations_logic: First argument must be a list of sc_model_ids.", 0, debug_lvl)
        return

    # creating guiding objects
    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
    meta_mng.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)

    # for each representation of each module, identifies the timestamps and run its plotting function
    for cur_sc_model_id in sc_models_ids:

        cur_repr_ids = meta_mng.get_all_representations_of_scmodel(cur_sc_model_id)

        if cur_repr_ids is None:
            continue

        for cur_repr_id in cur_repr_ids:

            reprgen_script = meta_mng.get_genscript_of_representation_sing(cur_repr_id)
            # print("Going for {0} ({1}).".format(cur_repr_id, cur_sc_model_id))
            # print("  {0}".format(reprgen_script))

            # TODO - make product a variable
            cur_folder_path = FolderDefinition.get_intermediate_bin_folder_path(cur_sc_model_id, 'idq',
                                                                                runset_id=runset_id)
            considered_timestamps = FolderDefinition.retrive_timestamps_between_interval_in_hist_folder(
                cur_folder_path, timestamp_min=timestamp_min, timestamp_max=timestamp_max, debug_lvl=debug_lvl)

            if considered_timestamps is None:
                continue

            considered_timestamps.sort()

            # debug purpose
            for cur_timestamp in considered_timestamps:
                cur_timestamp_arg = "-t {0}".format(cur_timestamp)
                call_command = "{0} {1} {2} -runsetid {3}".format(reprgen_script, cur_sc_model_id, cur_timestamp_arg,
                                                                  runset_id)
                Debug.dl("plot_modelsing_representations_logic: CALL '{0}' ({1}).".format(call_command, cur_repr_id),
                         2, debug_lvl)
                os.system(call_command)

# ####################################################### DEFS ####################################################### #
# ################################################ SPECIFIC PARAMETERS ############################################### #


def plot_preacchil24hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'preacchil24hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_preacchil12hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'preacchil12hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_preacchil06hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'preacchil06hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_preacchil03hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'preacchil03hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_runacchil24hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'runacchil24hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_runacchil12hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'runacchil12hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_runacchil06hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'runacchil06hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_runacchil03hh(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'runacchil03hh', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_soimoi20ih(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'soimoi20ih', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_soiwac20ih(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    plot_standard_direct(sc_model_id, unix_timestamp, 'soiwac20ih', aod.get_linkid_hills_mask(), debug_lvl=debug_lvl)


def plot_standard_direct(sc_model_id, unix_timestamp, param_id, mask, debug_lvl=0):
    """
    Plot images directly from file contents.
    :param sc_model_id:
    :param unix_timestamp:
    :param param_id:
    :param mask:
    :param debug_lvl:
    :return:
    """

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # define the timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, param_id)
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    # get the binary file path, check if it exists, read its content, converts into a 2D matrix, save as image
    bin_file_path = FolderDefinition.get_intermediate_bin_file_path(sc_model_id, param_id, the_timestamp)
    if not os.path.exists(bin_file_path):
        Debug.dl("plot_modelsing_representations_logic: File not found - {0}.".format(bin_file_path), 1, debug_lvl)
        return
    else:
        Debug.dl("plot_modelsing_representations_logic: Loading file - {0}.".format(bin_file_path), 1, debug_lvl)
    bin_file_content = np.load(bin_file_path)
    bin_matrix = build_data_matrix(mask, bin_file_content, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, param_id, bin_matrix, the_timestamp, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("plot_modelsing_representations_logic: Ploted image for parameter '{0}', model '{1}', in {2} seconds ".format(
        param_id, sc_model_id, d_time), 1, debug_lvl)


def plot_fldidxusgsih(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_id:
    :param unix_timestamp: AncillaryOnDemand
    :param aod:
    :param debug_lvl:
    :return:
    """

    param_source = 'disrawih'
    param = 'fldidxusgsih'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # define the timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, param_source)
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    if the_timestamp is None:
        Debug.dl("plot_modelsing_representations_logic: Not a single bin file for '{0}', model '{1}'.".format(param_source,
                                                                                                              sc_model_id),
                 1, debug_lvl)
        return

    # load thresholds and mask
    thresholds = aod.get_fidx_thresholds()
    linkid_mask = aod.get_linkid_link_mask()

    bin_file_path = FolderDefinition.get_intermediate_bin_file_path(sc_model_id, param_source, the_timestamp)
    qraw_value_vector = np.load(bin_file_path)

    # ensures both 'thresholds' and 'q_raw' vectors have the same size
    max_link_id = min(len(qraw_value_vector), len(thresholds))
    qraw_value_vector = qraw_value[0:max_link_id-1] if (len(qraw_value_vector) < max_link_id) else qraw_value_vector
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
            Debug.dl("plot_modelsing_representations_logic: "
                     "IndexError - type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                     len(qraw_value),
                                                                                                     link_id),
                     0, debug_lvl)
            return None
        except ValueError:
            Debug.dl("plot_modelsing_representations_logic: "
                     "ValueError: type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                    len(qraw_value),
                                                                                                    link_id),
                     0, debug_lvl)
            return None

    vect_classify_linkid = np.vectorize(to_vect_classify_linkid, otypes=[np.int])

    classified_vector = vect_classify_linkid(range(0, len(qraw_value_vector)), qraw_value_vector)
    classified_matrix = build_data_matrix(linkid_mask, classified_vector, debug_lvl=debug_lvl)

    save_image_file(sc_model_id, param, classified_matrix, the_timestamp, most_recent=False, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("plot_modelsing_representations_logic: Plotted image for parameter '{0}', model '{1}', in {2} seconds".format(
        param, sc_model_id, d_time), 1, debug_lvl)


def plot_disclausgsih(sc_model_id, unix_timestamp, aod, debug_lvl=0):
    """

    :param sc_model_id:
    :param unix_timestamp:
    :param aod: AncillaryOnDemand object
    :param debug_lvl:
    :return:
    """

    param_source = 'disrawih'
    param = 'disclausgsih'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # define the timestamp
    if unix_timestamp is not None:
        the_timestamp = unix_timestamp
    else:
        hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, param_source)
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)

    if the_timestamp is None:
        Debug.dl("plot_modelsing_representations_logic: Not a single bin file for '{0}', model '{1}'.".format(param_source,
                                                                                                              sc_model_id),
                 1, debug_lvl)
        return

    # this is a intermediate step: defining current month
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
            Debug.dl("plot_modelsing_representations_logic: IndexError - "
                     "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                        len(qraw_value), link_id))
            return None
        except ValueError:
            print("plot_modelsing_representations_logic: ValueError - "
                  "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                     len(qraw_value), link_id))
            return None

    # get the binary file path, read its content, converts into a 2D matrix, save as image
    bin_file_path = FolderDefinition.get_intermediate_bin_file_path(sc_model_id, param_source, the_timestamp)
    raw_dischs = np.load(bin_file_path)
    classes_vector = np.vectorize(to_vect_classify_linkid, otypes=[np.int])(range(0, len(raw_dischs)), raw_dischs)
    Debug.dl("plot_modelsing_representations_logic: linkid:{0}, disch:{1}, class:{2}".format(
        434514, raw_dischs[434514], classes_vector[434514]), 3, debug_lvl)
    classes_matrix = build_data_matrix(aod.get_linkid_link_mask(), classes_vector, debug_lvl=debug_lvl)
    save_image_file(sc_model_id, param, classes_matrix, the_timestamp, par1=data_month, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time() - start_time
    Debug.dl("plot_modelsing_representations_logic: Plotted image for parameter '{0}', model '{1}', in {2} secs.".format(
        param, sc_model_id, d_time), 1, debug_lvl)


# ####################################################### DEFS ####################################################### #
# ################################################# COMMON FUNCTIONS ################################################# #

def build_data_matrix(linkid_2d_mask, linkid_value_vector, debug_lvl=0):
    """
    Generates a 2D map of values.
    :param linkid_2d_mask: 25 matrix with link ids
    :param linkid_value_vector: 1D vector with [linkid][value]
    :param debug_lvl:
    :return: A 2D matrix of the values to be considered in a map to be plotted if possible to generate. None otherwise.
    """

    # basic check
    if (linkid_2d_mask is None) or (linkid_value_vector is None):
        Debug.dl("plot_modelsing_representations_logic: One argument is None for build_data_matrix({0}, {1}) function.".format(
            linkid_2d_mask, linkid_value_vector), 0, debug_lvl)
        return None

    vlen = linkid_value_vector.size if isinstance(linkid_value_vector, np.ndarray) else len(linkid_value_vector)

    # basic check
    if vlen == 1:
        Debug.dl("plot_modelsing_representations_logic: Invalid file format.", 0, debug_lvl)
        return None

    # apply vectorization
    def mapping_subfunction_def(x):
        try:
            ret = 0 if x >= vlen else linkid_value_vector[x]
        except IndexError:
            Debug.dl("plot_modelsing_representations_logic: Incompatible vector size({0} / {1}).".format(x, vlen),
                     0, debug_lvl)
        except TypeError:
            Debug.dl("plot_modelsing_representations_logic: Unexpected type for 'linkid_value_vector' : '{0}'.".format(
                type(linkid_value_vector)), 0, debug_lvl)
        return ret
    mapping_subfunction = np.vectorize(mapping_subfunction_def)

    return mapping_subfunction(linkid_2d_mask)


def save_image_file(sc_model_id, parameter_acronym, value_matrix, timestamp, par1=None, most_recent=False, debug_lvl=0):
    """
    Generates image files
    :param sc_model_id:
    :param parameter_acronym:
    :param value_matrix:
    :param timestamp:
    :param par1:
    :param debug_lvl:
    """

    mtx_color = ColorProvider.get_matrix_color(parameter_acronym, value_matrix, par1=par1, debug_lvl=debug_lvl)
    img_folder_path = FolderDefinition.get_historical_img_folder_path(sc_model_id, parameter_acronym)
    img_file_name = ImageDefinition.define_historical_file_name(timestamp, parameter_acronym)
    ColorProvider.save_matrix_color(mtx_color, os.path.join(img_folder_path, img_file_name),
                                    ImageDefinition.get_image_ext_name(), debug_lvl=debug_lvl)

    # deletes posterior images if necessary
    if most_recent:
        clean_folder(timestamp, FolderDefinition.get_historical_img_folder_path(sc_model_id, parameter_acronym),
                     debug_lvl=debug_lvl)


def clean_folder(higher_timestamp, folder_path, debug_lvl=0):
    """
    Delete all files in folder with higher timestamp values than the one presented.
    :param higher_timestamp: Higher timestamp value accepted in folder
    :param folder_path: Path of the folder to be cleaned
    :param debug_lvl:
    :return: None. Changes are performed in file system.
    """

    for cur_filename in os.listdir(folder_path):
        cur_timestamp = FileDefinition.obtain_hist_file_timestamp(cur_filename)
        if cur_timestamp > higher_timestamp:
            remove_file_path = os.path.join(folder_path, cur_filename)
            Debug.dl("plot_modelsing_representations_logic: Removing recent file '{0}'.".format(remove_file_path), 1,
                     debug_lvl)
            os.remove(remove_file_path)
