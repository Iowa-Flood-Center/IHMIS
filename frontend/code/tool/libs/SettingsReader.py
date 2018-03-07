import json
import os

class SettingsReader:

    _SETTINGS_FILE = "../../../conf/common/settings.json"
    _settings = None

    def __init__(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_dir, SettingsReader._SETTINGS_FILE)
        with open(file_path, 'r') as data_file:
            data = json.load(data_file)
        self._settings = data

    def get(self, key):
        return self._settings[key] if key in self._settings else None
