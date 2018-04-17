from MetaFile import MetaFile
from ..Debug import Debug


class MetaScModel(MetaFile):

    _root_object_tag = "sc_model"

    def get_id(self):
        return str(self._json_object["id"])

    def get_title(self):
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

    def get_binary_generator_script(self, asynchmodel_dict=None, debug_lvl=0):
        """

        :param asynchmodel_dict: Dictionary structure with all information associated with asynch_models
        :param debug_lvl: Integer
        :return:
        """

        bingen_tag = 'bingen_script'

        # first try: bingen script directly related to sc_model
        bg_script = None if bingen_tag not in self._json_object.keys() else str(self._json_object[bingen_tag])

        # debugging
        if not bg_script:
            Debug.dl("def_metafiles: '{0}' not found in {1}".format(bingen_tag, self._json_object.keys()), 2, debug_lvl)
        else:
            Debug.dl("def_metafiles: '{0}' found in {1}".format(bingen_tag, self._json_object.keys()), 2, debug_lvl)

        '''
        # second try: bingen related to asynch_model
        if bg_script is None:
            parameterset_json = self._json_object["parameter_set"]
            if ('type' in parameterset_json.keys()) and (parameterset_json['type'] == 'asynch_model'):
                if asynchmodel_dict is not None:
                    asynch_model_id = str(parameterset_json['id'])
                    if asynch_model_id in asynchmodel_dict.keys():
                        asynchmodel = asynchmodel_dict[asynch_model_id]
                        bg_script = str(asynchmodel.get_binary_generator_script())
                    else:
                        Debug.dl("def_metafiles: Asynch method {0} not found.".format(asynch_model_id), 1, debug_lvl)
                else:
                    Debug.dl("def_metafiles: Missing Asynch dictionary.", 1, debug_lvl)
        '''

        return bg_script

    def get_binary_generator_states_history_script(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        bingen_tag = 'bingen_state_hist_script'

        # first try: bingen script directly related to sc_model
        bg_script = None if bingen_tag not in self._json_object.keys() else str(self._json_object[bingen_tag])

        # debugging
        if not bg_script:
            Debug.dl("def_metafiles: '{0}' not found in {1}".format(bingen_tag, self._json_object.keys()), 2, debug_lvl)
        else:
            Debug.dl("def_metafiles: '{0}' found in {1}".format(bingen_tag, self._json_object.keys()), 2, debug_lvl)

        return bg_script

    def get_binary_generator_hydroforecast_script(self):
        """

        :param debug_lvl:
        :return:
        """

        tag = 'bingen_hydroforecast_script'

        return None if tag not in self._json_object.keys() else str(self._json_object[tag])
