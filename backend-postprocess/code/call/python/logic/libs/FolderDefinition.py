from SettingsRealtime import SettingsRealtime
from ImageDefinition import ImageDefinition
from FileDefinition import FileDefinition
from BinDefinition import BinDefinition
from Settings import Settings
from Debug import Debug
import os


class FolderDefinition:
    # each folder has the same structure path: [base_folder_path]/[subfolder_name]/[model]/[parameter]/
    # exception: forecasts binary files (own function)

    _meta_folder_path = "anci/meta_files_repository/"

    _base_folder_name_runset = "data/runsets/"
    _runset_file_folder_name = "files"
    _runset_meta_folder_name = "metafiles"
    _runset_metasandbox_folder_name = "metafiles_sandbox"

    _txt_timestamp_ref_subfolder_name = "txts_timestamp_ref0"
    _img_historical_subfolder_path = "imgs_historical"
    _img_forecast_subfolder_name = "imgs_forecast"
    _eval_historical_subfolder_name = "eval_historical"
    _reprcomb_historical_subfolder_name = "reprcomb_historical"
    _img_displayed_subfolder_path = "repres_displayed"
    _bin_intermediate_subfolder_path = "bins_intermediate"
    _bin_input_runset_subfolder_name = "bins_input"

    _met_scmodels_subfolder_name = "sc_models"
    _met_scmodelcombs_subfolder_name = "sc_modelcombinations"
    _met_screferences_subfolder_name = "sc_references"
    _met_scproducts_subfolder_name = "sc_products"
    _met_screpresentations_subfolder_name = "sc_representations"
    _met_screpresentationcompositions_subfolder_name = "sc_represcomps"
    _met_scevaluations_subfolder_name = "sc_evaluations"
    _met_crossmatrices_subfolder_name = "cross_matrices"
    _met_scmenu_subfolder_name = "sc_menu"
    _met_scrunset_subfolder_name = "sc_runset"

    # _met_asynchmodels_subfolder_name = "asynch_models"
    # _met_scparameters_subfolder_name = "sc_parameters"

    def __init__(self):
        return

    @staticmethod
    def get_runset_folder_path(runset_id=None):
        """

        :param runset_id:
        :return:
        """
        raw_data_folder_path = Settings.get("raw_data_folder_path")
        if runset_id is None:
            return os.path.join(raw_data_folder_path, FolderDefinition._base_folder_name_runset)
        else:
            return os.path.join(raw_data_folder_path, FolderDefinition._base_folder_name_runset, runset_id)

    @staticmethod
    def get_runset_file_folder_path(runset_id):
        """

        :param runset_id:
        :return:
        """
        return os.path.join(FolderDefinition.get_runset_folder_path(runset_id),
                            FolderDefinition._runset_file_folder_name)

    @staticmethod
    def get_runset_meta_folder_path(runset_id):
        """

        :param runset_id:
        :return:
        """
        return os.path.join(FolderDefinition.get_runset_folder_path(runset_id),
                            FolderDefinition._runset_meta_folder_name)

    @staticmethod
    def get_timestamp_ref_txt_folder_path(sc_model_id=None, sc_runset_id=None):
        """

        :param sc_model_id:
        :param sc_runset_id:
        :return:
        """
        if sc_model_id is None:
            return FolderDefinition.get_subfolder_path(FolderDefinition._txt_timestamp_ref_subfolder_name,
                                                       runset_id=sc_runset_id)
        else:
            return os.path.join(FolderDefinition.get_subfolder_path(FolderDefinition._txt_timestamp_ref_subfolder_name,
                                                                    runset_id=sc_runset_id), sc_model_id)

    @staticmethod
    def get_timestamp_ref_txt_file_path(sc_model_id, sc_representation_id, sc_runset_id=None):
        """

        :param sc_model_id:
        :param sc_representation_id:
        :param sc_runset_id:
        :return:
        """
        file_name = "{0}.txt".format(sc_representation_id)
        return os.path.join(FolderDefinition.get_timestamp_ref_txt_folder_path(sc_model_id, sc_runset_id=sc_runset_id),
                            file_name)

    @classmethod
    def get_historical_img_file_path(cls, model_id, parameter_id, timestamp, runset_id=None):
        """

        :param model_id:
        :param parameter_id:
        :param timestamp:
        :param runset_id:
        :return:
        """
        folder_path = cls.get_historical_img_folder_path(model_id, parameter_id, runset_id=runset_id)
        file_name = ImageDefinition.define_historical_file_name(timestamp, parameter_id)
        return os.path.join(folder_path, file_name)

    @classmethod
    def get_historical_file_path(cls, sc_model_id, representation_id, file_extension, timestamp, runset_id=None):
        """

        :param sc_model_id:
        :param representation_id:
        :param file_extension:
        :param timestamp:
        :param runset_id:
        :return:
        """
        folder_path = cls.get_historical_img_folder_path(sc_model_id, representation_id, runset_id=runset_id)
        file_name = ImageDefinition.define_historical_file_name(timestamp, representation_id,
                                                                file_extension=file_extension)
        return os.path.join(folder_path, file_name)

    @classmethod
    def get_historical_img_folder_path(cls, model_id=None, representation_id=None, runset_id=None):
        """

        :param model_id:
        :param representation_id:
        :param runset_id:
        :return:
        """

        # define base folder path
        if runset_id is None:
            return None

        base_folder_path = cls.get_runset_file_folder_path(runset_id)

        #
        if model_id is not None:
            if representation_id is not None:
                return os.path.join(base_folder_path, cls._img_historical_subfolder_path, model_id, representation_id)
            else:
                return os.path.join(base_folder_path, cls._img_historical_subfolder_path, model_id)
        else:
            return os.path.join(base_folder_path, cls._img_historical_subfolder_path)

    @classmethod
    def get_forecast_img_folder_path(cls, model_id=None, parameter_id=None):
        return cls.get_subfolder_path(cls._img_forecast_subfolder_name, model_id,
                                      parameter_id)

    @classmethod
    def get_eval_folder_name(cls, evaluation_id, reference_id):
        """

        :param evaluation_id:
        :param reference_id:
        :return:
        """

        return "{0}_{1}".format(evaluation_id, reference_id)

    @classmethod
    def get_historical_eval_folder_path(cls, model_id, evaluation_id, reference_id, runset_id):
        """

        :param model_id:
        :param evaluation_id:
        :param reference_id:
        :param runset_id:
        :return:
        """

        sc_evaluation_id = FolderDefinition.get_eval_folder_name(evaluation_id, reference_id)

        return cls.get_subfolder_path(cls._eval_historical_subfolder_name, model_id, sc_evaluation_id,
                                      runset_id=runset_id)

    @classmethod
    def get_historical_reprcomb_folder_path(cls, runset_id, represcomb_id=None, frame_id=None, model_id=None):
        """

        :param runset_id:
        :param represcomb_id:
        :param frame_id:
        :param model_id:
        :return:
        """

        base_folder = cls.get_subfolder_path(cls._reprcomb_historical_subfolder_name, model_id=represcomb_id,
                                             parameter_id=frame_id, runset_id=runset_id)

        if (frame_id is not None) and (represcomb_id is not None) and (model_id is not None):
            return os.path.join(base_folder, model_id)
        else:
            return base_folder

    '''
    @staticmethod
    def get_forecast_bin_folder_path(model_id=None):
        # TODO - bring the logic to here
        return ModelProvider.get_forecast_bin_folder_path(model_id)
    '''

    @classmethod
    def get_displayed_img_file_path(cls, model_id, parameter_id, display_time, runset_id=None):
        """

        :param model_id:
        :param parameter_id:
        :param display_time:
        :param runset_id:
        :return:
        """
        folder_path = cls.get_displayed_folder_path(model_id, parameter_id, runset_id=runset_id)
        file_name = ImageDefinition.define_displayed_file_name(display_time, parameter_id)
        return os.path.join(folder_path, file_name)

    @classmethod
    def get_displayed_file_path(cls, sc_model_id, sc_representation_id, display_time, file_ext, runset_id=None):
        """

        :param sc_model_id: String.
        :param sc_representation_id: String.
        :param display_time: Integer.
        :param file_ext: String. Raw file extension.
        :param runset_id: String. A sc_runset_id. If None, assumes 'runtime'.
        :return:
        """
        folder_path = cls.get_displayed_folder_path(sc_model_id, sc_representation_id, runset_id=runset_id)
        file_name = ImageDefinition.define_displayed_file_name(display_time, sc_representation_id,
                                                               file_extension=file_ext)
        return os.path.join(folder_path, file_name)

    @classmethod
    def get_displayed_folder_path(cls, model_id=None, parameter_id=None, runset_id=None):
        """

        :param model_id:
        :param parameter_id:
        :param runset_id:
        :return:
        """
        return cls.get_subfolder_path(cls._img_displayed_subfolder_path, model_id, parameter_id, runset_id=runset_id)

    @classmethod
    def get_displayed_reprcomb_folder_path(cls, runset_id, modelcomb_id, represcomb_id, frame_id=None, model_id=None):
        """

        :param runset_id:
        :param represcomb_id:
        :param frame_id:
        :param model_id:
        :return:
        """

        base_folder = cls.get_subfolder_path(cls._img_displayed_subfolder_path, modelcomb_id, represcomb_id,
                                             runset_id=runset_id)
        if frame_id is not None:
            base_folder = os.path.join(base_folder, frame_id)
            if model_id is not None:
                base_folder = os.path.join(base_folder, model_id)

        return base_folder

    @classmethod
    def get_subfolder_path(cls, subfolder_name, model_id=None, parameter_id=None, runset_id=None):
        """
        CORE FUNCTION
        :param subfolder_name:
        :param model_id:
        :param parameter_id:
        :param runset_id:
        :return:
        """

        # define if base folder is realtime or a runset
        if runset_id is None:
            return None

        raw_data_folder_path = Settings.get("raw_data_folder_path")
        base_folder = os.path.join(raw_data_folder_path,
                                   FolderDefinition._base_folder_path_runset,
                                   runset_id,
                                   cls._runset_file_folder_name)

        # build path
        if (parameter_id is not None) and (model_id is not None):
            return os.path.join(base_folder, subfolder_name, model_id, parameter_id)
        elif model_id is not None:
            return os.path.join(base_folder, subfolder_name, model_id)
        else:
            return os.path.join(base_folder, subfolder_name)

    @classmethod
    def get_runset_input_bin_folder_path(cls, runset_id, sc_model_id=None):
        """

        :param runset_id:
        :param sc_model_id:
        :return:
        """

        if sc_model_id is not None:
            return os.path.join(FolderDefinition.get_runset_file_folder_path(runset_id=runset_id),
                                FolderDefinition._bin_input_runset_subfolder_name, sc_model_id)
        else:
            return os.path.join(FolderDefinition.get_runset_file_folder_path(runset_id=runset_id),
                                FolderDefinition._bin_input_runset_subfolder_name)

    @classmethod
    def get_intermediate_bin_file_path(cls, model_id, product_id, timestamp, runset_id=None):
        """

        :param model_id:
        :param product_id:
        :param timestamp:
        :param runset_id:
        :return:
        """

        folder_path = cls.get_intermediate_bin_folder_path(model_id, product_id, runset_id=runset_id)
        file_name = BinDefinition.define_file_name(timestamp, product_id)

        return os.path.join(folder_path, file_name)

    @staticmethod
    def check_intermediate_bin_file_exists(model_id, parameter_id, timestamp):
        """

        :param model_id:
        :param parameter_id:
        :param timestamp:
        :return:
        """
        file_path = FolderDefinition.get_intermediate_bin_file_path(model_id, parameter_id, timestamp)
        return os.path.exists(file_path)

    @staticmethod
    def check_hist_representation_file_exists(sc_model_id, sc_representation_id, unix_timestamp, runset_id=None):
        """

        :param sc_model_id:
        :param sc_representation_id:
        :param unix_timestamp:
        :param runset_id:
        :return:
        """
        file_path = FolderDefinition.get_historical_img_file_path(sc_model_id, sc_representation_id, unix_timestamp,
                                                                  runset_id=runset_id)
        return os.path.exists(file_path)

    @classmethod
    def get_intermediate_bin_folder_path(cls, model_id=None, product_id=None, runset_id=None):
        """

        :param model_id:
        :param product_id:
        :param runset_id:
        :return:
        """

        # define base folder path
        if runset_id is None:
            return None

        base_folder_path = cls.get_runset_file_folder_path(runset_id=runset_id)

        if model_id is not None:
            if product_id is not None:
                return os.path.join(base_folder_path, cls._bin_intermediate_subfolder_path, model_id, product_id)
            else:
                return os.path.join(base_folder_path, cls._bin_intermediate_subfolder_path, model_id)
        else:
            return os.path.join(base_folder_path, cls._bin_intermediate_subfolder_path)

    @staticmethod
    def get_model_get_model_output_hdf5_file_name_prefix(model_id):
        """

        :param model_id:
        :param timestamp:
        :return:
        """

        return SettingsRealtime.get("input_file_prefix", sc_model_id=model_id)

    @classmethod
    def get_model_output_hdf5_file_name(cls, model_id, timestamp):
        """

        :param model_id:
        :param timestamp:
        :return:
        """

        filename_prefix = FolderDefinition.get_model_get_model_output_hdf5_file_name_prefix(model_id)
        return None if filename_prefix is None else "{0}{1}.h5".format(filename_prefix, timestamp)

    @classmethod
    def get_model_output_hdf5_file_path(cls, model_id, timestamp, runset_id=None, check_alternative=False):
        """

        :param model_id:
        :param timestamp:
        :param runset_id:
        :param check_alternative:
        :return:
        """

        if runset_id is None:
            folder_path = cls.get_model_output_hdf5_folder(model_id=model_id)
            file_name = FolderDefinition.get_model_output_hdf5_file_name(model_id, timestamp)

            # basic check - not null
            if folder_path is None:
                return None
            elif file_name is None:
                return None

            file_path = os.path.join(folder_path, file_name)
        else:
            folder_path = cls.get_runset_input_bin_folder_path(runset_id=runset_id, sc_model_id=model_id)
            file_name = "{0}_{1}.h5".format(model_id, timestamp)  # TODO - create proper class
            file_path = os.path.join(folder_path, file_name)
            if check_alternative and (not os.path.exists(file_path)):
                file_name = "snapshot_{0}.h5".format(timestamp)  # TODO - create proper class
                file_path = os.path.join(folder_path, file_name)

        return file_path

    @classmethod
    def get_model_output_hdf5_folder(cls, model_id=None):
        """

        :param model_id:
        :return:
        """

        return SettingsRealtime.get("input_folder_path", sc_model_id=model_id)

    @classmethod
    def retrieve_all_single_models(cls, folder_path):
        """
        Retrieve all single models folder names existing in a folder
        :param folder_path:
        :return: List of folder names
        """
        all_single_models = []
        all_models = FolderDefinition.retrieve_all_subfolder_names(folder_path)
        for cur_model in all_models:
            if FolderDefinition.is_single_model(cur_model):
                all_single_models.append(cur_model)
        return all_single_models

    @classmethod
    def is_single_model(cls, folder_name):
        """
        Evaluates if a folder name represents a single model or a comparison of two models
        :param folder_name: Folder name. Should NOT be passed complete folder path
        :return: True if represents a single model, False otherwise
        """
        if not "_" in folder_name:
            return True
        else:
            return False

    @classmethod
    def define_model_combination_name(cls, model_a_name, model_b_name):
        """

        :param model_a_name:
        :param model_b_name:
        :return:
        """
        return model_a_name + "_" + model_b_name

    @staticmethod
    def extracts_models_acronym_from_combination(combination_acronym):
        """

        :param combination_acronym:
        :return: A 1D vector of size 2 if it was possible to obtain it, None otherwise
        """
        return combination_acronym.split('_') if (combination_acronym.count('_') == 1) else None

    @classmethod
    def create_folders_for_model_if_necessary(cls, sc_model_id, all_products_id, sc_runset_id, debug_lvl=0):
        """
        Create all folders necessary for the model, if they don't exist yet.
        :param sc_model_id:
        :param all_products_id:
        :param debug_lvl:
        :return: None. Changes are performed on file system.
        """

        # for each subfolder, evaluate if model folder exists and if each parameters folder exist
        Debug.dl("def_system: Creating folder for parameter {0}, model {1}".format(all_products_id, sc_model_id),
                 1, debug_lvl)

        '''
        # img historical folder
        FolderDefinition.create_folder_for_model_if_necessary(
            FolderDefinition.get_historical_img_folder_path(sc_model_id), all_parameters_id)

        # img display folder
        FolderDefinition.create_folder_for_model_if_necessary(
            FolderDefinition.get_displayed_folder_path(sc_model_id), all_parameters_id)
        '''

        # bin intermediate folder
        FolderDefinition.create_folder_for_model_if_necessary(
            FolderDefinition.get_intermediate_bin_folder_path(model_id=sc_model_id, runset_id=sc_runset_id),
            all_products_id)

    @staticmethod
    def create_folder_for_model_if_necessary(subfolder_path, all_parameters_id=None, debug_lvl=0):
        """
        Should only be called by 'FolderDefinition.create_folders_for_model_if_necessary()' function
        :param subfolder_path:
        :param all_parameters_id: List with the IDs of all parameters
        :return: Nothing. Changes are performed on file system
        """
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        if all_parameters_id is not None:
            for cur_parameter in all_parameters_id:
                cur_subfolder = os.path.join(subfolder_path, cur_parameter)
                if not os.path.exists(cur_subfolder):
                    Debug.dl("def_system: Creating folder '{0}'".format(cur_subfolder), 2, debug_lvl)
                    os.makedirs(cur_subfolder)

    @staticmethod
    def retrieve_all_file_names(folder_path, filename_prefix=None):
        """

        :param folder_path:
        :param filename_prefix:
        :return:
        """

        if not os.path.exists(folder_path):
            return None

        ret_list = []
        for cur_fname in os.listdir(folder_path):
            cur_file_path = os.path.join(folder_path, cur_fname)
            if os.path.isfile(cur_file_path) and ((filename_prefix is None) or (cur_fname.startswith(filename_prefix))):
                ret_list.append(cur_fname)

        # return all_files
        return ret_list

    @staticmethod
    def retrieve_all_subfolder_names(folder_path):
        """

        :param folder_path:
        :return:
        """
        all_folders = [o for o in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, o))]
        return all_folders

    @staticmethod
    def retrive_most_recent_timestamp_in_hist_folder(folder_path):
        """

        :param folder_path:
        :return: Integer or None
        """

        all_file_names = FolderDefinition.retrieve_all_file_names(folder_path)
        if (all_file_names is None) or (len(all_file_names) == 0):
            return None

        all_file_names.sort(reverse=True)
        return FileDefinition.obtain_hist_file_timestamp(all_file_names[0])

    @staticmethod
    def retrive_earliest_timestamp_in_hist_folder(folder_path):
        """

        :param folder_path:
        :return: Integer or None
        """

        all_file_names = FolderDefinition.retrieve_all_file_names(folder_path)
        if (all_file_names is None) or (len(all_file_names) == 0):
            return None

        all_file_names.sort(reverse=False)
        return FileDefinition.obtain_hist_file_timestamp(all_file_names[0])

    @staticmethod
    def retrive_closest_timestamp_in_hist_folder(folder_path, ref_timestamp, accept_range=None, debug_lvl=0):
        """
        Searches for the file with the closes timestamp value for a given timestamp as reference
        :param folder_path: Path hith historical files (files in historical format)
        :param ref_timestamp: Reference timestamp
        :param accept_range: If is a list of size two, represent the min/max time distances in sec. If int, abs min/max. If None, no range is evaluated
        :return: A integer number if found any acceptable file, None otherwise
        """

        # list all files
        all_file_names = FolderDefinition.retrieve_all_file_names(folder_path)
        if (all_file_names is None) or (len(all_file_names) == 0):
            return None

        # get the absolutely closest timestamp
        all_file_names.sort(reverse=True)
        all_timestamps = []
        for cur_filename in all_file_names:
            tm = FileDefinition.obtain_hist_file_timestamp(cur_filename)
            if tm is not None:
                all_timestamps.append(tm)

        #
        all_dists = []
        for cur_tm in all_timestamps:
            all_dists.append(abs(cur_tm - ref_timestamp))

        closer_tm_idx = all_dists.index(min(all_dists))
        closer_tm = all_timestamps[closer_tm_idx]

        # evaluate if there is a range of acceptable values
        if accept_range is not None:
            if isinstance(accept_range, list):
                min_value = ref_timestamp - accept_range[0]
                max_value = ref_timestamp - accept_range[1]
            elif isinstance(accept_range, int):
                min_value = ref_timestamp - accept_range
                max_value = ref_timestamp + accept_range
            else:
                min_value = max_value = ref_timestamp

            Debug.dl("def_system: Closest timestamp {0} must be between {1} and {2}.".format(closer_tm,
                                                                                             min_value,
                                                                                             max_value),
                     1, debug_lvl)
            closer_tm = closer_tm if ((closer_tm >= min_value) and (closer_tm <= max_value)) else None

        return closer_tm

    @staticmethod
    def retrive_timestamps_between_interval_in_hist_folder(folder_path, timestamp_min=None, timestamp_max=None,
                                                           debug_lvl=0):
        """

        :param folder_path:
        :param timestamp_min:
        :param timestamp_max:
        :param debug_lvl:
        :return:
        """

        # list all files
        all_file_names = FolderDefinition.retrieve_all_file_names(folder_path)
        if (all_file_names is None) or (len(all_file_names) == 0):
            return None

        # get the absolutely closest timestamp
        all_timestamps = [FileDefinition.obtain_hist_file_timestamp(tm) for tm in all_file_names]

        # separates the ones of our interest
        return_list = []
        for cur_timestamp in all_timestamps:
            if (timestamp_min is None) or (cur_timestamp >= timestamp_min):
                if (timestamp_max is None) or (cur_timestamp <= timestamp_max):
                    return_list.append(cur_timestamp)

        return return_list

    @staticmethod
    def retrive_files_extension_in_hist_folder(folder_path, debug_lvl=0):
        """
        Returns the extension of first file found in folder. It assumes all files have the same extension
        :param folder_path:
        :param debug_lvl:
        :return: String - extension dotless if the folder contains at least one file with extension. None otherwise.
        """

        # list all files
        all_file_names = FolderDefinition.retrieve_all_file_names(folder_path)
        if (all_file_names is None) or (len(all_file_names) == 0):
            Debug.dl("def_system: Not a single file at folder '{0}'.".format(folder_path), 2, debug_lvl)
            return None

        # basic check: file must have an extension
        one_file_name = all_file_names[0]
        if '.' not in one_file_name:
            Debug.dl("def_system: File '{0}' at '{1}': no extension.".format(one_file_name, folder_path), 2, debug_lvl)
            return None

        return one_file_name.split(".")[-1]

    @staticmethod
    def retrive_closest_timestamp_in_dist_folder(folder_path, ref_timestamp, accept_range=None, filename_prefix=None,
                                                 debug_lvl=0):
        """
        Searches for the file with the closes timestamp value for a given timestamp as reference in a distribution folder
        :param folder_path: Path with distribution files (files in distribution format)
        :param ref_timestamp: Reference timestamp
        :param accept_range: If is a list of size two, represent the min/max time distances in sec. If int, abs min/max. If None, no range is evaluated
        :param filename_prefix:
        :return: A integer number if found any acceptable file, None otherwise
        """

        # list all files
        all_file_names = FolderDefinition.retrieve_all_file_names(folder_path, filename_prefix=filename_prefix)
        if (all_file_names is None) or (len(all_file_names) == 0):
            return None

        # get the absolutely closest timestamp
        all_file_names.sort(reverse=True)
        all_timestamps = [FileDefinition.obtain_dist_file_timestamp(tm) for tm in all_file_names]

        all_dists = [abs(cur_tm - ref_timestamp) for cur_tm in all_timestamps]

        closer_tm_idx = all_dists.index(min(all_dists))
        closer_tm = all_timestamps[closer_tm_idx]

        Debug.dl("def_system: Closest timestamp found: {0} (dist: {1} from {2}) at '{3}'.".format(closer_tm,
                                                                                                  all_dists[
                                                                                                      closer_tm_idx],
                                                                                                  ref_timestamp,
                                                                                                  folder_path),
                 1, debug_lvl)

        # evaluate if there is a range of acceptable values
        if accept_range is not None:
            if isinstance(accept_range, list):
                min_value = ref_timestamp - accept_range[0]
                max_value = ref_timestamp - accept_range[1]
            elif isinstance(accept_range, int):
                min_value = ref_timestamp - accept_range
                max_value = ref_timestamp + accept_range
            else:
                min_value = max_value = ref_timestamp

            Debug.dl("def_system: Closest timestamp {0} must be between {1} and {2}.".format(closer_tm,
                                                                                             min_value,
                                                                                             max_value),
                     1, debug_lvl)
            closer_tm = closer_tm if ((closer_tm >= min_value) and (closer_tm <= max_value)) else None

        return closer_tm

    @staticmethod
    def check_both_models_exist(sc_model_id1, sc_model_id2, sc_product_id, unix_timestamp, debug_lvl=0):
        """

        :param sc_model_id1:
        :param sc_model_id2:
        :param sc_product_id:
        :param unix_timestamp:
        :param debug_lvl:
        :return: Boolean. TRUE if both files exist, FALSE otherwise.
        """
        file1_exists = FolderDefinition.check_intermediate_bin_file_exists(sc_model_id1, sc_product_id, unix_timestamp)
        file2_exists = FolderDefinition.check_intermediate_bin_file_exists(sc_model_id2, sc_product_id, unix_timestamp)
        if file1_exists and file2_exists:
            Debug.dl("plot_cmprsimp_representations_lib: files for both {0}, {1} models exist for {2} at {3}".format(
                sc_model_id1, sc_model_id2, sc_product_id, unix_timestamp
            ), 2, debug_lvl)
            return True
        else:
            Debug.dl(
                "plot_cmprsimp_representations_lib: no common files for {0}, {1} models exist for {2} at {3}".format(
                    sc_model_id1, sc_model_id2, sc_product_id, unix_timestamp
                ), 2, debug_lvl)
            return False

    @staticmethod
    def check_both_representations_exist(sc_model_id, sc_representation_id1, sc_representation_id2, unix_timestamp,
                                         runset_id=None, debug_lvl=0):
        """

        :param sc_model_id:
        :param sc_representation_id1:
        :param sc_representation_id2:
        :param unix_timestamp:
        :param runset_id:
        :param debug_lvl:
        :return: Boolean. TRUE if both files exist, FALSE otherwise.
        """
        file1_exists = FolderDefinition.check_hist_representation_file_exists(sc_model_id, sc_representation_id1,
                                                                              unix_timestamp, runset_id=runset_id)
        file2_exists = FolderDefinition.check_hist_representation_file_exists(sc_model_id, sc_representation_id2,
                                                                              unix_timestamp, runset_id=runset_id)

        if file1_exists and file2_exists:
            Debug.dl("def_system: files for both {0} and {1} representation of model {2} exist for at {3}".format(
                sc_representation_id1, sc_representation_id2, sc_model_id, unix_timestamp), 2, debug_lvl)
            return True
        else:
            Debug.dl("def_system: no common files for representation {0} and {1} for model {2} at {3}".format(
                sc_representation_id1, sc_representation_id2, sc_model_id, unix_timestamp), 2, debug_lvl)
            return False

    # meta files methods

    @staticmethod
    def get_meta_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        if (folder_flag is None) or (folder_flag == 'eff'):
            if runset_id is None:
                raw_data_folder_path = Settings.get("raw_data_folder_path")
                return os.path.join(raw_data_folder_path, FolderDefinition._meta_folder_path)
            else:
                return FolderDefinition.get_runset_meta_folder_path(runset_id)
        elif folder_flag == 'sbx':
            if runset_id is None:
                return None
            else:
                return os.path.join(FolderDefinition.get_runset_folder_path(runset_id),
                                    FolderDefinition._runset_metasandbox_folder_name)
        else:
            return None

    @staticmethod
    def get_meta_scmodels_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id: String. A Runset ID.
        :param folder_flag: String or None. Expects 'eff' for 'effective' or 'sbx' for 'sandbox'.
        :return: String. A folder path.
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_scmodels_subfolder_name)

    @staticmethod
    def get_meta_scmodelcomb_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id: String. A Runset ID.
        :param folder_flag: String or None. Expects 'eff' for 'effective' or 'sbx' for 'sandbox'.
        :return: String. A folder path.
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_scmodelcombs_subfolder_name)

    @staticmethod
    def get_meta_screferences_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_screferences_subfolder_name)

    @staticmethod
    def get_meta_scproducts_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_scproducts_subfolder_name)

    @staticmethod
    def get_meta_screpresentations_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_screpresentations_subfolder_name)

    @staticmethod
    def get_meta_screpresentationcompositions_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_screpresentationcompositions_subfolder_name)

    @staticmethod
    def get_meta_scevaluations_folder_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_scevaluations_subfolder_name)

    '''
    @staticmethod
    def get_meta_asynchmodels_folder_path():
        return os.path.join(FolderDefinition._meta_folder_path, FolderDefinition._met_asynchmodels_subfolder_name)

    @staticmethod
    def get_meta_scparameters_folder():
        return os.path.join(FolderDefinition._meta_folder_path, FolderDefinition._met_scparameters_subfolder_name)
    '''

    @staticmethod
    def get_meta_crossmatrices_folder(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_crossmatrices_subfolder_name)

    @staticmethod
    def get_meta_scmenu_folder(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_scmenu_subfolder_name)

    @staticmethod
    def get_meta_scrunset_folder(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_folder_path(runset_id=runset_id, folder_flag=folder_flag),
                            FolderDefinition._met_scrunset_subfolder_name)
