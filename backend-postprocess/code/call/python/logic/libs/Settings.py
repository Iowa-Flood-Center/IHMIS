import json
import os


class Settings:

    _settings_file = "../../../../../conf/settings.json"
    _data = None

    @staticmethod
    def load():
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        settings_file_path = os.path.join(current_dir_path, Settings._settings_file)
        with open(settings_file_path) as r_file:
            Settings._data = json.load(r_file)
        return

    @staticmethod
    def get(attr):
        if Settings._data is None:
            Settings.load()
        return Settings._data[attr] if attr in Settings._data.keys() else None

    def __init__(self):
        return
