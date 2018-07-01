import json
import os


class ConsistMetaDefs:
    _settings_file_path = "../../../../../conf/settings.json"
    _root_path = None

    @staticmethod
    def get_runset_root_path():
        ConsistMetaDefs._read_settings()
        return os.path.join(ConsistMetaDefs._root_path, "data/runsets/")

    @staticmethod
    def _read_settings():
        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        settings_file_dir = os.path.join(this_file_dir,
                                         ConsistMetaDefs._settings_file_path)
        if ConsistMetaDefs._root_path is not None:
            return
        with open(settings_file_dir) as r_file:
            j_content = json.load(r_file)
        ConsistMetaDefs._root_path = j_content["raw_data_folder_path"]

    def __init__(self):
        return
