import inspect
import json
import sys
import os

class SettingsLoader:

    @staticmethod
    def load_settings(or_die=True, track_util=False, debug_lvl=0):
        CONF_FOLDER_NAME = "conf"
        SETTING_FILE_NAME = "settings.json"
        UTIL_PATH_KEY = "utils_libs_path"

        # current parent folder
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        folderpath = os.path.dirname(os.path.abspath(filename))
        folderpath = os.path.dirname(os.path.dirname(folderpath))

        # current conf folder
        filepath = os.path.join(folderpath, CONF_FOLDER_NAME, SETTING_FILE_NAME)

        # read file
        if not os.path.exists(filepath):
            if debug_lvl > 0:
                print("File not found: {0}".format(filepath))
            if or_die:
                quit(1)
            else:
                return None
        with open(filepath, 'r') as r_file:
            settings = json.load(r_file)

        # append lib folder to system lib
        if track_util:
            if UTIL_PATH_KEY in settings:
                sys.path.append(settings[UTIL_PATH_KEY])
            else:
                print("Missing settings key: {0}".format(UTIL_PATH_KEY))
                if or_die:
                    quit(1)
                else:
                    return None

        return settings

    def __init__(self):
        return
