import shutil
import time
import os

from FolderDefinition import FolderDefinition
from MetaFileManager import MetaFileManager
from Debug import Debug


class ResultsDisplayUpdater:

    @staticmethod
    def update_display_images(sc_models_ids, unix_timestamp, debug_lvl=0):
        """
        For each model, comparison and evaluation, delete its content from display folder and add new contents
        :param sc_models_ids:
        :param unix_timestamp: If None, get the most recent
        :param debug_lvl:
        :return:
        """

        # TODO - check inputs

        # creating guiding objects
        meta_mng = MetaFileManager()
        meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
        meta_mng.load_all_scparameter_meta_info(debug_lvl=debug_lvl)

        for cur_sc_model_id in sc_models_ids:

            # start counting time for debug
            start_time = time.time() if debug_lvl > 0 else None
            count_plots = 0

            # determine current parameter list
            all_parameters = meta_mng.get_all_parameters_of_scmodel(cur_sc_model_id, debug_lvl=debug_lvl)

            for cur_parameter in all_parameters:

                # define type
                is_param_hist = meta_mng.is_parameter_historical(cur_parameter)
                is_param_fore = meta_mng.is_parameter_forecast(cur_parameter)

                # basic check
                if (not is_param_hist) and (not is_param_fore):
                    Debug.dl("ResultsDisplayUpdater: Parameter {0} is unknown. Skipping.".format(cur_parameter),
                             2, debug_lvl)
                    continue

                # get time step and time direction of the parameter
                time_interval = meta_mng.get_time_interval_of_scparameter(cur_parameter)

                # defining effective 0-ref timestamp
                if unix_timestamp is None:
                    hist_folder_path = FolderDefinition.get_historical_img_folder_path(cur_sc_model_id, cur_parameter)
                    the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)
                else:
                    the_timestamp = unix_timestamp

                if the_timestamp is None:
                    continue

                # TODO - update display images folder
                if is_param_hist:
                    Debug.dl("ResultsDisplayUpdater: Parameter {0} is historical of {1} secs.".format(cur_parameter,
                                                                                                          time_interval),
                             2, debug_lvl)

                    # start counting time for debug
                    start_time = time.time() if debug_lvl > 0 else None

                    count_copy = update_historical_parameter_representations(cur_sc_model_id, cur_parameter, time_interval,
                                                                             the_timestamp, clean_previous=True,
                                                                             debug_lvl=debug_lvl)

                    # debug info
                    d_time = time.time() - start_time
                    Debug.dl("ResultsDisplayUpdater: Updated {0} images in {1} seconds.".format(count_copy, d_time),
                             1, debug_lvl)

                elif is_param_fore:
                    Debug.dl("ResultsDisplayUpdater: Parameter {0} is forecast of {1} secs.".format(cur_parameter,
                                                                                                        time_interval),
                             2, debug_lvl)

                # update reference text file
                update_ref0_file(cur_sc_model_id, cur_parameter, the_timestamp, debug_lvl=debug_lvl)
                count_plots += 1

            # debug
            if count_plots > 0:

                # debug info
                d_time = time.time() - start_time
                Debug.dl("ResultsDisplayUpdater: Updated {0} images for model {1} in {2} seconds ".format(
                    count_plots, cur_sc_model_id, d_time), 1, debug_lvl)

    @staticmethod
    def update_historical_parameter_representations(sc_model_id, sc_parameter_id, time_interval, ref0_timestamp,
                                                    clean_previous=True, debug_lvl=0):
        """

        :param sc_model_id: String.
        :param sc_parameter_id: String.
        :param time_interval: Integer. Delta time between representations in seconds
        :param ref0_timestamp: Integer.
        :param clean_previous: Boolean.
        :param debug_lvl: Integer.
        :return: Integer. Number of copied files.
        """

        # TODO - rethink this constant location
        historical_maximum_back_time = 10 * 24 * 60 * 60    # 10 days in seconds

        # define update and historical folders
        upd_folder_path = FolderDefinition.get_displayed_folder_path(model_id=sc_model_id, parameter_id=sc_parameter_id)
        hst_folder_path = FolderDefinition.get_historical_img_folder_path(model_id=sc_model_id, parameter_id=sc_parameter_id)

        # clear previous file
        if clean_previous:
            for cur_filename in os.listdir(upd_folder_path):
                cur_filepath = os.path.join(upd_folder_path, cur_filename)
                if os.path.isfile(cur_filepath):
                    os.unlink(cur_filepath)

        # check and copy-renaming as possible
        cur_delta_timestamp = 0
        cur_index = 0
        count_copied = 0
        while cur_delta_timestamp < historical_maximum_back_time:
            cur_timestamp = ref0_timestamp - cur_delta_timestamp
            cur_hist_filepath = FolderDefinition.get_historical_img_file_path(sc_model_id, sc_parameter_id, cur_timestamp)
            if os.path.exists(cur_hist_filepath):
                cur_disp_filepath = FolderDefinition.get_displayed_img_file_path(sc_model_id, sc_parameter_id, cur_index)
                shutil.copy(cur_hist_filepath, cur_disp_filepath)
                Debug.dl("ResultsDisplayUpdater: Updated '{0}' => '{1}'.".format(os.path.basename(cur_hist_filepath),
                                                                                     cur_disp_filepath), 2, debug_lvl)
                count_copied += 1

            cur_index += 1
            cur_delta_timestamp += time_interval

        return count_copied

    @staticmethod
    def update_ref0_file(sc_model_id, parameter_id, runset_id, unix_timestamp, debug_lvl=0):
        """
        Delete / create new reference file
        :param sc_model_id:
        :param parameter_id:
        :param runset_id:
        :param unix_timestamp:
        :param debug_lvl:
        :return:
        """

        # creates folder if necessary
        dest_folder_path = FolderDefinition.get_timestamp_ref_txt_folder_path(sc_model_id=sc_model_id,
                                                                              sc_runset_id=runset_id)
        if not os.path.exists(dest_folder_path):
            os.makedirs(dest_folder_path)

        # gets file path and delete previous if exists
        dest_file_path = FolderDefinition.get_timestamp_ref_txt_file_path(sc_model_id, parameter_id,
                                                                          sc_runset_id=runset_id)
        if os.path.exists(dest_file_path):
            os.remove(dest_file_path)

        # create new one only with timestamp
        with open(dest_file_path, "w+") as wfile:
            wfile.write(str(unix_timestamp))

        Debug.dl("ResultsDisplayUpdater: Wrote '{0}' in '{1}'.".format(unix_timestamp, dest_file_path), 2, debug_lvl)
