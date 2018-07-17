from MetaFile import MetaFile
from ..Debug import Debug


class MetaComparisonSet(MetaFile):

    _root_object_tag = "comparison_matrix"


    def get_all_comparison_acronyms(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """
        return self._json_object.keys()

    def get_representation_list(self, composition_acronym=None, sc_model1_acronym=None, sc_model2_acronym=None, debug_lvl=0):
        """

        :param composition_acronym:
        :param sc_model1_acronym:
        :param sc_model2_acronym:
        :param debug_lvl:
        :return:
        """

        if composition_acronym is not None:
            composition_acron = composition_acronym
        elif (sc_model1_aconym is not None) and (sc_model2_acronym is not None):
            composition_acron = "{0}_{1}".format(sc_model1_acronym, sc_model2_acronym)
        else:
            composition_acron = None

        return [str(c) for c in self._json_object[composition_acron]] if composition_acron in self._json_object else None
