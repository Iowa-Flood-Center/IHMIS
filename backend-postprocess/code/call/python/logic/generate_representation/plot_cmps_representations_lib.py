from PIL import Image
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.BinAncillaryDefinition import BinAncillaryDefinition
from libs.FolderDefinition import FolderDefinition
from libs.ImageDefinition import ImageDefinition
from libs.MetaFileManager import MetaFileManager
from libs.Debug import Debug


# #################################################################################################################### #
# ####################################################### DEFS ####################################################### #
# #################################################################################################################### #

def generate_cmps_representations(sc_models_ids, unix_timestamp, runset_id=None, debug_lvl=0):
    """

    :param sc_models_ids:
    :param unix_timestamp:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    # basic check
    if (sc_models_ids is None) or (type(sc_models_ids) is not list):
        Debug.dl("plot_cmps_representations_lib: First argument must be a list of sc_model_ids.", 0, debug_lvl)
        return

    # creating guiding objects
    meta_mng = MetaFileManager()
    meta_mng.load_all_asynchmodel_meta_info()
    meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)

    # for each parameter of each method, run its plotting function
    for cur_sc_model_id in sc_models_ids:

        cur_pars_id = meta_mng.get_all_parameters_of_scmodel(cur_sc_model_id)
        FolderDefinition.create_folders_for_model_if_necessary(cur_sc_model_id, cur_pars_id)

        if 'pah03hdcuih' in cur_pars_id:
            plot_pah03hdcuih(cur_sc_model_id, unix_timestamp, debug_lvl=debug_lvl)
        if 'dcufldicuih' in cur_pars_id:
            plot_dcufldicuih(cur_sc_model_id, unix_timestamp, runset_id=runset_id, debug_lvl=debug_lvl)


# ####################################################### DEFS ####################################################### #
# ################################################ SPECIFIC PARAMETERS ############################################### #


def plot_pah03hdcuih(sc_model_id, unix_timestamp, debug_lvl=0):
    """

    :param sc_model_id:
    :param unix_timestamp:
    :param debug_lvl:
    :return:
    """

    abv_par = 'disclausgsih'
    blw_par = 'preacchil03hh'
    cmps_par = 'pah03hdcuih'

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # define the timestamp
    if unix_timestamp is not None:
        if check_both_exists(sc_model_id, abv_par, blw_par, unix_timestamp, debug_lvl=0):
            the_timestamp = unix_timestamp
        else:
            the_timestamp = None
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_id, abv_par, blw_par,
                                                          debug_lvl=debug_lvl)

    # must have a matching timestamp
    if the_timestamp is None:
        Debug.dl("plot_cmps_representations_lib: Not found y matching timestamp for '{0}' and '{1}' ('{2}').".format(
            abv_par, blw_par, sc_model_id), 1, debug_lvl)
        return None

    plot_composition_map(sc_model_id, the_timestamp, cmps_par, blw_par, abv_par, debug_lvl=debug_lvl)

    # debug info
    d_time = time.time() - start_time
    Debug.dl("plot_cmps_representations_lib: Plotted image for parameter '{0}', model '{1}', in {2} seconds".format(
        cmps_par, sc_model_id, d_time), 1, debug_lvl)


def plot_dcufldicuih(sc_model_id, unix_timestamp, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param unix_timestamp:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    abv_par = 'fldidxusgsih'
    blw_par = 'disclausgsih'
    cmps_par = 'dcufldicuih'

    generate_cmps_representation(sc_model_id, unix_timestamp, abv_par, blw_par, cmps_par, runset_id=runset_id,
                                 debug_lvl=debug_lvl)


def get_most_recent_timestamp_between(sc_model_id, param_id1, param_id2, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param param_id1:
    :param param_id2:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    hist_folder_path_1 = FolderDefinition.get_historical_img_folder_path(sc_model_id, param_id1, runset_id=runset_id)
    the_timestamp_1 = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path_1)

    hist_folder_path_2 = FolderDefinition.get_historical_img_folder_path(sc_model_id, param_id2, runset_id=runset_id)
    the_timestamp_2 = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path_2)

    # the the biggest present in both
    if (the_timestamp_1 is not None) and (the_timestamp_2 is not None):
        if the_timestamp_1 == the_timestamp_2:
            return the_timestamp_2
        else:
            c_max = min([the_timestamp_1, the_timestamp_2])
            return c_max if check_both_exists(sc_model_id, param_id1, param_id2, c_max, debug_lvl=debug_lvl) else None

    # if something is missing, Debug it and return None
    if the_timestamp_1 is None:
        Debug.dl("plot_cmps_representations_lib: "
                 "Not a single image for '{0}', model '{1}'. Skipping composition.".format(param_id1, sc_model_id),
                 1, debug_lvl)
    if the_timestamp_2 is None:
        Debug.dl("plot_cmps_representations_lib: "
                 "Not a single image for '{0}', model '{1}'. Skipping composition.".format(param_id2, sc_model_id),
                 1, debug_lvl)
    return None


def check_both_exists(sc_model_id, param_id1, param_id2, unix_timestamp, debug_lvl=0):
    """

    :param sc_model_id:
    :param param_id1:
    :param param_id2:
    :param unix_timestamp:
    :param debug_lvl:
    :return:
    """

    # TODO - implement it properly

    return True


def generate_cmps_representation(sc_model_id, unix_timestamp, abv_par, blw_par, cmps_par, runset_id=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param unix_timestamp:
    :param abv_par:
    :param blw_par:
    :param cmps_par:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # define the timestamp
    if unix_timestamp is not None:
        if check_both_exists(sc_model_id, abv_par, blw_par, unix_timestamp, debug_lvl=0):
            the_timestamp = unix_timestamp
        else:
            the_timestamp = None
    else:
        the_timestamp = get_most_recent_timestamp_between(sc_model_id, abv_par, blw_par, runset_id=runset_id,
                                                          debug_lvl=debug_lvl)

    # must have a matching timestamp
    if the_timestamp is None:
        Debug.dl("plot_cmps_representations_lib: Not found x matching timestamp for '{0}' and '{1}' ('{2}').".format(
            abv_par, blw_par, sc_model_id), 1, debug_lvl)
        return None

    plot_composition_map(sc_model_id, the_timestamp, cmps_par, blw_par, abv_par, runset_id=runset_id,
                         debug_lvl=debug_lvl)

    # debug info
    d_time = time.time() - start_time
    Debug.dl("plot_cmps_representations_lib: Plotted image for parameter '{0}', model '{1}', in {2} seconds".format(
        cmps_par, sc_model_id, d_time), 1, debug_lvl)


def plot_composition_map(sc_model_id, timestamp, composite_par, bellow_par, above_par, runset_id=None,
                         debug_lvl=0):
    """
    Create a composition of two images of same size
    :param sc_model_id:
    :param timestamp:
    :param bellow_par:
    :param composite_par:
    :param above_par:
    :param debug_lvl:
    :return: None. Changes are performed in filesystem.
    """

    print("Mira: {0}".format(runset_id))

    # setting file paths
    image_bellow_file_path = FolderDefinition.get_historical_img_file_path(sc_model_id, bellow_par, timestamp,
                                                                           runset_id=runset_id)
    image_above_file_path = FolderDefinition.get_historical_img_file_path(sc_model_id, above_par, timestamp,
                                                                           runset_id=runset_id)
    output_image_file_path = FolderDefinition.get_historical_img_file_path(sc_model_id, composite_par, timestamp,
                                                                           runset_id=runset_id)

    # create folder structure if necessary
    destination_folder = os.path.dirname(output_image_file_path)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # do it
    merge_images(image_bellow_file_path, image_above_file_path, output_image_file_path, debug_lvl=debug_lvl)

    return


def merge_images(background_image_file_path, above_image_file_path, output_image_file_path, debug_lvl=0):
    """

    :param background_image_file_path:
    :param above_image_file_path:
    :param output_image_file_path:
    :param debug_lvl:
    :return:
    """

    # basic check - files must exist
    if not os.path.exists(background_image_file_path):
        Debug.dl("plot_cmps_representations_lib: File '{0}' does not exist. Skipping composition.".format(
            background_image_file_path), 1, debug_lvl)
        return
    elif not os.path.exists(above_image_file_path):
        Debug.dl("plot_cmps_representations_lib: File '{0}' does not exist. Skipping composition.".format(
            above_image_file_path), 1, debug_lvl)
        return

    # read first file and convert to RGB
    try:
        background_image = Image.open(background_image_file_path).convert('RGBA')
    except IOError:
        Debug.dl("plot_cmps_representations_lib: Unable to open file: {0}.".format(background_image_file_path),
                 1, debug_lvl)
        return

    # read second file and convert to RGB
    try:
        above_image = Image.open(above_image_file_path).convert('RGBA').resize(background_image.size)
    except IOError:
        Debug.dl("plot_cmps_representations_lib: Unable to open file: {0}.".format(above_image_file_path), 1,
                 debug_lvl)
        return

    # TODO - replace color?

    '''
    # save the composition, converting it back to indexed
    composite_img = Image.alpha_composite(background_image, above_image).convert('P', palette=Image.ADAPTIVE, colors=20)
    composite_img.save(output_image_file_path)
    Debug.dl("plot_cmps_representations_lib: Saving {0} file.".format(output_image_file_path), 1, debug_lvl)
    '''

    # save the composition
    try:
        composite_img = Image.alpha_composite(background_image, above_image)

        # Get the alpha band in a mask of value 21
        alpha = composite_img.split()[-1]
        mask = Image.eval(alpha, lambda a: 21 if a == 0 else 0)

        # convert image to indexed format
        composite_img = composite_img.convert("RGB")
        composite_img = composite_img.convert('P', palette=Image.ADAPTIVE, colors=21)

        # apply mask and save it
        composite_img.paste(21, mask)
        composite_img.save(output_image_file_path, transparency=max(composite_img.getdata()))
        Debug.dl("plot_cmps_representations_lib: Saving {0} file.".format(output_image_file_path), 1, debug_lvl)
    except ValueError:
        Debug.dl("plot_cmps_representations_lib: Problems merging {0} and {1}.".format(background_image, above_image),
                 0, debug_lvl)
        Debug.dl("plot_cmps_representations_lib:   Wrong mode {0}.".format(composite_img.mode), 0, debug_lvl)

    return
