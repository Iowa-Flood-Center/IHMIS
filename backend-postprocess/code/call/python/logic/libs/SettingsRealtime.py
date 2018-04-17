from Settings import Settings
import json
import os


class SettingsRealtime(Settings):

    _settings_file = "../../../../../conf/settings_realtime.json"

    @staticmethod
    def get(attr, sc_model_id=None):
        if SettingsRealtime._data is None:
            SettingsRealtime.load()

        if sc_model_id is not None:
            if sc_model_id not in SettingsRealtime._data["sc_models"].keys():
                return None
            sc_model_obj = SettingsRealtime._data["sc_models"][sc_model_id]
            return sc_model_obj[attr] if attr in sc_model_obj.keys() else None

    def __init__(self):
        return
