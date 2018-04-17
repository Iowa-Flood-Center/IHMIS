
class MetaScRepresentation(MetaFile):

    _root_object_tag = "sc_representation"

    def get_id(self):
        return str(self._json_object["id"])

    def get_title(self):
        return str(self._json_object["call_radio"]) if "call_radio" in self._json_object.keys() else None

    def get_time_interval(self):
        return str(self._json_object["time_interval"])

    def get_repgen_sing_script(self):
        return str(self._json_object["repgen_script"])

    def get_repgen_cmpr_script(self):
        tag = "repgen_script_cmpr"
        return str(self._json_object[tag]) if tag in self._json_object else None

    def get_reprcln_script(self):
        tag = "reprcln_script"
        return str(self._json_object[tag]) if tag in self._json_object else None
