
class MetaScProduct(MetaFile):

    _root_object_tag = "sc_product"

    def get_id(self):
        return str(self._json_object["id"])

    def get_title(self):

        if "title" in self._json_object.keys():
            return str(self._json_object["title"])
        else:
            return None
