
class MetaEvaluationMatrix(MetaFile):

    _root_object_tag = "evaluation_matrix"

    def get_all_evalutated_models(self, sc_evaluation_id):
        """

        :param sc_evaluation_id:
        :return: List of Strings (sc_evaluation_id s)
        """

        # try to find the 'raw' evaluation id
        raw_try = None if sc_evaluation_id not in self._json_object.keys() else self._json_object[sc_evaluation_id]
        if raw_try is not None:
            return raw_try

        # try to find it associated with a reference
        if raw_try is None:
            all_keys = self._json_object.keys()
            for cur_key in all_keys:
                cur_key_splitted = cur_key.split('_')
                if (len(cur_key_splitted) > 1) and (cur_key_splitted[0] == sc_evaluation_id):
                    return self._json_object[cur_key]

        # ok, give up
        return None

    def get_all_evalutated_models_and_references(self, sc_evaluation_id):
        """

        :param sc_evaluation_id:
        :return: List of 2-D lists (sc_evaluation_id, sc_reference_id)
        """

        # try to find it associated with a reference
        return_list = []
        all_keys = self._json_object.keys()
        for cur_key in all_keys:
            cur_key_splitted = cur_key.split('_')
            if (len(cur_key_splitted) > 1) and (cur_key_splitted[0] == sc_evaluation_id):
                for cur_model_id in self._json_object[cur_key]:
                    return_list.append([cur_model_id, cur_key_splitted[1]])

        return return_list

    def get_all_evaluations_of_scmodel(self, sc_model_id):
        """

        :param sc_model_id:
        :return:
        """

        return_array = []
        for cur_evaluation_id in self._json_object.keys():
            cur_evaluated_models = [str(cur_s) for cur_s in self._json_object[cur_evaluation_id]]
            if sc_model_id in cur_evaluated_models:
                return_array.append(cur_evaluation_id)

        return return_array

    def get_all_evaluations(self):
        """

        :return:
        """

        return self._json_object.keys()
