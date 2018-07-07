from PIL import Image
import os

from FolderDefinition import FolderDefinition
from Debug import Debug


class ReprComposition:

    @staticmethod
    def get_most_recent_timestamp_between(sc_model_id, repr_id1, repr_id2, runset_id=None, debug_lvl=0):
        """

        :param sc_model_id:
        :param repr_id1:
        :param repr_id2:
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        hist_folder_path_1 = FolderDefinition.get_historical_img_folder_path(sc_model_id, repr_id1, runset_id=runset_id)
        the_timestamp_1 = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path_1)

        hist_folder_path_2 = FolderDefinition.get_historical_img_folder_path(sc_model_id, repr_id2, runset_id=runset_id)
        the_timestamp_2 = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path_2)

        # print("Looked at 1: {0}".format(hist_folder_path_1))
        # print("Looked at 2: {0}".format(hist_folder_path_2))

        # the the biggest present in both
        if (the_timestamp_1 is not None) and (the_timestamp_2 is not None):
            if the_timestamp_1 == the_timestamp_2:
                return the_timestamp_2
            else:
                c_max = min([the_timestamp_1, the_timestamp_2])
                return c_max if check_both_exists(sc_model_id, repr_id1, repr_id2, c_max, debug_lvl=debug_lvl) else None

        # if something is missing, Debug it and return None
        if the_timestamp_1 is None:
            Debug.dl("ReprComposition: "
                     "Not a single image for '{0}', model '{1}'. Skipping composition.".format(repr_id1, sc_model_id),
                     1, debug_lvl)
        if the_timestamp_2 is None:
            Debug.dl("ReprComposition: "
                     "Not a single image for '{0}', model '{1}'. Skipping composition.".format(repr_id2, sc_model_id),
                     1, debug_lvl)
        return None

    @staticmethod
    def check_both_exists(sc_model_id, repr1_id, repr2_id, unix_timestamp, debug_lvl=0):
        """

        :param sc_model_id:
        :param repr1_id:
        :param repr2_id:
        :param unix_timestamp:
        :param debug_lvl:
        :return:
        """

        # TODO - implement it properly
        repr1_img_path = FolderDefinition.get_historical_img_file_path(sc_model_id, repr1_id, unix_timestamp)
        repr2_img_path = FolderDefinition.get_historical_img_file_path(sc_model_id, repr2_id, unix_timestamp)

        return True if os.path.exists(repr1_img_path) and os.path.exists(repr2_img_path) else False

    @staticmethod
    def generate_cmps_representation(sc_model_id, unix_timestamp, abv_par, blw_par, cmps_par, debug_lvl=0):
        """

        :param sc_model_id:
        :param unix_timestamp:
        :param abv_par:
        :param blw_par:
        :param cmps_par:
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
            the_timestamp = get_most_recent_timestamp_between(sc_model_id, abv_par, blw_par, debug_lvl=debug_lvl)

        # must have a matching timestamp
        if the_timestamp is None:
            Debug.dl("ReprComposition: Not found a matching timestamp for '{0}' and '{1}' ('{2}').".format(
                abv_par, blw_par, sc_model_id), 1, debug_lvl)
            return None

        plot_composition_map(sc_model_id, the_timestamp, cmps_par, blw_par, abv_par, debug_lvl=debug_lvl)

        # debug info
        d_time = time.time() - start_time
        Debug.dl("ReprComposition: Plotted image for parameter '{0}', model '{1}', in {2} seconds".format(
            cmps_par, sc_model_id, d_time), 1, debug_lvl)

    @staticmethod
    def plot_composition_map(sc_model_id, timestamp, composite_par, bellow_par, above_par, replace_color=None,
                             runset_id=None, debug_lvl=0):
        """
        Create a composition of two images of same size
        :param sc_model_id:
        :param timestamp:
        :param bellow_par:
        :param composite_par:
        :param above_par:
        :param replace_color:
        :param debug_lvl:
        :return: None. Changes are performed in filesystem.
        """

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
        ReprComposition.merge_images(image_bellow_file_path, image_above_file_path, output_image_file_path,
                                     replace_color=replace_color, debug_lvl=debug_lvl)

        return

    @staticmethod
    def merge_images(background_image_file_path, above_image_file_path, output_image_file_path, replace_color=None,
                     debug_lvl=0):
        """

        :param background_image_file_path:
        :param above_image_file_path:
        :param output_image_file_path:
        :param replace_color: Array of size 3 (RGB values)
        :param debug_lvl:
        :return:
        """

        # basic check - files must exist
        if not os.path.exists(background_image_file_path):
            Debug.dl("ReprComposition: File '{0}' does not exist. Skipping composition.".format(
                background_image_file_path), 1, debug_lvl)
            return
        elif not os.path.exists(above_image_file_path):
            Debug.dl("ReprComposition: File '{0}' does not exist. Skipping composition.".format(
                above_image_file_path), 1, debug_lvl)
            return

        # read first file and convert to RGB
        try:
            background_image = Image.open(background_image_file_path).convert('RGBA')
        except IOError:
            Debug.dl("ReprComposition: Unable to open file: {0}.".format(background_image_file_path),
                     1, debug_lvl)
            return

        # read second file and convert to RGB
        try:
            above_image = Image.open(above_image_file_path).convert('RGBA').resize(background_image.size)
        except IOError:
            Debug.dl("ReprComposition: Unable to open file: {0}.".format(above_image_file_path), 1,
                     debug_lvl)
            return

        # replace color
        if replace_color is not None:
            above_data = above_image.getdata()

            above_data_new = []
            for item in above_data:
                if (item[0] == replace_color[0]) and (item[1] == replace_color[1]) and (item[2] == replace_color[2]):
                    above_data_new.append((255, 255, 255, 0))
                else:
                    above_data_new.append(item)

            above_image.putdata(above_data_new)

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
            Debug.dl("ReprComposition: Saving {0} file.".format(output_image_file_path), 1, debug_lvl)
        except ValueError:
            Debug.dl("ReprComposition: Problems merging {0} and {1}.".format(background_image, above_image), 0, debug_lvl)
            Debug.dl("ReprComposition:   Wrong mode {0}.".format(composite_img.mode), 0, debug_lvl)

        return

    def __init__(self):
        return
