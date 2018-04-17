from MetaFile import MetaFile


class MetaScReference(MetaFile):

    _root_object_tag = "sc_reference"

    def get_id(self):
        """

        :return:
        """
        return str(self._json_object["id"])

    def get_title(self):
        """

        :return:
        """
        return str(self._json_object["title"])

    def get_product_set(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """
        productset_json = self._json_object["sc_product_set"]
        return productset_json

    def get_representation_set(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        try:
            return self._json_object["sc_representation_set"]
        except KeyError:
            return None

    def get_binary_generator_inst_script(self):
        """

        :return:
        """
        tag = "bingen_inst_script"
        return str(self._json_object[tag]) if tag in self._json_object.keys() else None

    def get_binary_generator_hist_script(self):
        """

        :return:
        """
        tag = "bingen_hist_script"
        return str(self._json_object[tag]) if tag in self._json_object.keys() else None
