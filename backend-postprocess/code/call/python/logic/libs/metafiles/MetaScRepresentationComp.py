
class MetaScRepresentationComp(MetaFile):

    _root_object_tag = "sc_represcomb"

    def get_id(self):
        return str(self._json_object["id"])

    def get_repgen_script(self):
        return str(self._json_object["rpcbgen_inst_script"])

    def get_repupd_script(self):
        return str(self._json_object["rpcbupd_inst_script"])

    def get_repcln_script(self):
        return str(self._json_object["rpcbcln_script"]) if "rpcbcln_script" in self._json_object else None
