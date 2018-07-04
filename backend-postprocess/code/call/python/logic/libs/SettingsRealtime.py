from Settings import Settings
import json
import os


class SettingsRealtime(Settings):

    _settings_file = "../../../../../conf/settings_realtime.json"

    @classmethod
    def get(cls, attr, sc_model_id=None):
        if cls._data is None:
            SettingsRealtime.load()

        if sc_model_id is not None:
            try:
                if sc_model_id not in cls._data["sc_models"].keys():
                    return None
            except KeyError:
                print("Key 'sc_models' not found in {0}.".format(cls._data.keys()))
                return None
            sc_model_obj = cls._data["sc_models"][sc_model_id]
            return sc_model_obj[attr] if attr in sc_model_obj.keys() else None

    def __init__(self):
        return
