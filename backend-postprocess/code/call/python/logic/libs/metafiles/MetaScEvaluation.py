
class MetaScEvaluation(MetaFile):

    _root_object_tag = "sc_evaluation"

    def get_id(self):
        return str(self._json_object["id"])

    def get_evalgen_script(self):
        return str(self._json_object["evalgen_inst_script"])

    def get_evalgen_hist_script(self):
        tag = "evalgen_hist_script"
        return str(self._json_object[tag]) if tag in self._json_object else None

    def get_evalupd_script(self):
        return str(self._json_object["evalupd_inst_script"])

    def get_evalcln_script(self):
        tag = "evalcln_inst_script"
        return str(self._json_object[tag]) if tag in self._json_object.keys() else None
