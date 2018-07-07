from PIL import Image
import numpy as np
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from plot_cmps_representations_lib import check_both_exists
from libs.FolderDefinition import FolderDefinition
from libs.ImageDefinition import ImageDefinition
from libs.FileDefinition import FileDefinition
from libs.ColorProvider import ColorProvider
from libs.Debug import Debug


# ###################################################### DEFS ######################################################## #

def build_data_matrix(linkid_2d_mask, linkid_value_vector, no_link_value=0, debug_lvl=0):
    """
    Generates a 2D map of values.
    :param linkid_2d_mask: 25 matrix with link ids
    :param linkid_value_vector: 1D vector with [linkid][value]
    :param no_link_value: value assigned to cells not related to a link
    :param debug_lvl:
    :return: A 2D matrix of the values to be considered in a map to be plotted if possible to generate. None otherwise.
    """

    # basic check
    if (linkid_2d_mask is None) or (linkid_value_vector is None):
        Debug.dl("plot_singsimp_representations_lib: One argument is None for build_data_matrix({0}, {1}) function.".format(
            linkid_2d_mask, linkid_value_vector), 0, debug_lvl)
        return None

    vlen = linkid_value_vector.size if isinstance(linkid_value_vector, np.ndarray) else len(linkid_value_vector)

    # basic check
    if vlen == 1:
        Debug.dl("plot_singsimp_representations_lib: Invalid file format.", 0, debug_lvl)
        return None

    # apply vectorization
    def mapping_subfunction_def(x):
        ret = None
        try:
            ret = no_link_value if x >= vlen else linkid_value_vector[x]
            '''
            if x >= vlen:
                ret = no_link_value
            else:
                ret = linkid_value_vector[x]
            '''
        except IndexError:
            Debug.dl("plot_instant_lib: Incompatible vector size({0} / {1}).".format(x, vlen), 0, debug_lvl)
        except TypeError:
            Debug.dl("plot_instant_lib: Unexpected type for 'linkid_value_vector' : '{0}'.".format(
                type(linkid_value_vector)), 0, debug_lvl)

        return ret
    mapping_subfunction = np.vectorize(mapping_subfunction_def)
    ret_mtx = mapping_subfunction(linkid_2d_mask)

    '''
    # debug
    d = 1
    print("[{0}x{1}]: {2}({3}) -> {4}".format(d, d, linkid_2d_mask[d][d], linkid_value_vector[linkid_2d_mask[d][d]],
                                              ret_mtx[d][d]))
    d = 1200
    print("[{0}x{1}]: {2}({3}) -> {4}".format(d, d, linkid_2d_mask[d][d], linkid_value_vector[linkid_2d_mask[d][d]],
                                              ret_mtx[d][d]))
    '''

    return ret_mtx


def save_image_file(sc_model_id, parameter_acronym, value_matrix, timestamp, par1=None, most_recent=False,
                    runset_id=None, debug_lvl=0):
    """
    Generates image files
    :param sc_model_id:
    :param parameter_acronym:
    :param value_matrix:
    :param timestamp:
    :param par1:
    :param most_recent:
    :param runset_id:
    :param debug_lvl:
    """

    if "_" not in sc_model_id:
        # define color, filename and filepath
        mtx_color = ColorProvider.get_matrix_color(parameter_acronym, value_matrix, par1=par1, debug_lvl=debug_lvl)
    else:
        mtx_color = ColorProvider.get_matrix_color_comparison(parameter_acronym, value_matrix, par1=par1,
                                                              debug_lvl=debug_lvl)

    img_folder_path = FolderDefinition.get_historical_img_folder_path(sc_model_id, parameter_acronym,
                                                                      runset_id=runset_id)
    img_file_name = ImageDefinition.define_historical_file_name(timestamp, parameter_acronym)

    # create folder if necessary
    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)

    # save
    print("reprgen_lib: Saving at {0}.".format(img_folder_path))
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
            Debug.dl("plot_singsimp_representations_lib: Removing recent file '{0}'.".format(remove_file_path), 1,
                     debug_lvl)
            os.remove(remove_file_path)
