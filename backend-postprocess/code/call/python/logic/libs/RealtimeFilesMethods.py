import os

from SettingsRealtime import SettingsRealtime
from Debug import Debug


class RealtimeFilesMethods:

    @staticmethod
    def get_folder_with_h5_files(model_id, runset_id):
        if runset_id != "realtime":
            return None
        else:
            return SettingsRealtime.get("input_folder_path", sc_model_id=model_id)

    @staticmethod
    def get_h5_file_name_prefix(model_id, runset_id):
        if runset_id != "realtime":
            return None
        else:
            return SettingsRealtime.get("input_file_prefix", sc_model_id=model_id)


    @staticmethod
    def get_current_timestamp_from_hdf5_files(output_folder_path, file_name_prefix, debug_lvl=0):

        # basic check
        if output_folder_path is None:
            return None
        elif not os.path.exists(output_folder_path):
            Debug.dl("RealtimeFilesMethods: Folder {0} does not exist.".format(output_folder_path), 1,
                     debug_lvl)
            return None

        # list all files in folder and basic check - must have at least one file
        all_file_names = os.listdir(output_folder_path)
        if len(all_file_names) == 0:
            Debug.dl("RealtimeFilesMethods: No file found at {0}".format(output_folder_path), 1,
                     debug_lvl)
            return None
        else:
            Debug.dl("RealtimeFilesMethods: Listed {0} files in '{1}'".format(len(all_file_names),
                                                                                                output_folder_path), 1,
                     debug_lvl)

        # retrieve most recent timestamp
        all_file_names.sort(reverse=True)
        for cur_file_name in all_file_names:
            try:
                return int(cur_file_name.replace(file_name_prefix, "").replace(".h5", ""))
            except ValueError:
                continue

    def __init__(self):
        return
