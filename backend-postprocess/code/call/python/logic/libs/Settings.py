import json
import os


class Settings:

    _settings_file = "../../../../../conf/settings.json"
    _data = None

    @classmethod
    def load(cls):
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        settings_file_path = os.path.join(current_dir_path, cls._settings_file)
        with open(settings_file_path) as r_file:
            cls._data = json.load(r_file)
        return

    @classmethod
    def get(cls, attr):
        if cls._data is None:
            cls.load()
        return cls._data[attr] if attr in cls._data.keys() else None

    def __init__(self):
        return
