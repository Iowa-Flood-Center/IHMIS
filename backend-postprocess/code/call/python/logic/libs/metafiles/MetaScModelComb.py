from MetaFile import MetaFile
from ..Debug import Debug


class MetaScModelComb(MetaFile):

    _root_object_tag = "sc_modelcombination"

    def get_id(self):
        return str(self._json_object["id"]) if (self._json_object is not None) and ("id" in self._json_object) else None

    def get_representation_set(self):
        if "sc_repres_set" in self._json_object.keys():
            return [str(s) for s in self._json_object["sc_repres_set"]["sc_repr"]]
        else:
            return []

    def get_representations_past_model_id(self):
        if ("sc_repres_set" in self._json_object.keys()) and ("modelpast" in self._json_object["sc_repres_set"]):
            return self._json_object["sc_repres_set"]["modelpast"]
        else:
            return None

    def get_representations_fore_model_id(self):
        if ("sc_repres_set" in self._json_object.keys()) and ("modelfore" in self._json_object["sc_repres_set"]):
            return self._json_object["sc_repres_set"]["modelfore"]
        else:
            return None

    def get_representationcomp_set(self):
        # return self.get_representation_set()
        if "sc_represcomb_set" in self._json_object.keys():
            return [str(s) for s in self._json_object["sc_represcomb_set"].keys()]
        else:
            return []
