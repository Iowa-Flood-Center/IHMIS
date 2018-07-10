import pickle
import os

from BinAncillaryDefinition import BinAncillaryDefinition


class Hydrographs:

    _rc_usgs_file_path =                     BinAncillaryDefinition.get_rating_curve_file_path("usgs")
    _rc_ifc_file_path =                      BinAncillaryDefinition.get_rating_curve_file_path("ifc")
    _links_stg_threshold_file_path =         BinAncillaryDefinition.get_bin_thresholds_file_path("links_stagethresholds.p")
    _links_threshold_file_path =             BinAncillaryDefinition.get_bin_thresholds_file_path("links_allthresholds.p")
    _links_pois_desc_area_file_path =        BinAncillaryDefinition.get_bin_pois_file_path("links_pois_descarea.p")
    _linkid_poisall_relationship_file_path = BinAncillaryDefinition.get_bin_pois_file_path("links_pois_all.p")

    @staticmethod
    def get_all_usgs_rating_curves(debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """
        file_path = Hydrographs._rc_usgs_file_path
        if not os.path.exists(file_path):
            Debug.dl("Hydrographs: File '{0}' not found.".format(file_path), 0, debug_lvl)
            return
        with open(file_path, "rb") as r_file:
            return_dict = pickle.load(r_file)
        return return_dict

    @staticmethod
    def get_all_ifc_rating_curves(debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """
        file_path = Hydrographs._rc_ifc_file_path
        if not os.path.exists(file_path):
            Debug.dl("Hydrographs: File '{0}' not found.".format(file_path), 0, debug_lvl)
            return
        with open(file_path, "rb") as r_file:
            return_dict = pickle.load(r_file)
        return return_dict

    @staticmethod
    def get_all_rating_curves(debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """
        all_rcs = {}
        all_rcs.update(Hydrographs.get_all_usgs_rating_curves())
        all_rcs.update(Hydrographs.get_all_ifc_rating_curves())
        return all_rcs

    @staticmethod
    def get_all_stage_threshold(debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        file_path = Hydrographs._links_stg_threshold_file_path

        if not os.path.exists(file_path):
            Debug.dl("Hydrographs: File '{0}' not found.".format(file_path), 0, debug_lvl)
            return None

        with open(file_path, "rb") as r_file:
            return_dict = pickle.load(r_file)

        return return_dict

    @staticmethod
    def get_all_threshold(debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        file_path = Hydrographs._links_threshold_file_path

        if not os.path.exists(file_path):
            Debug.dl("Hydrographs: File '{0}' not found.".format(file_path), 0, debug_lvl)
            return

        with open(file_path, "rb") as r_file:
            return_dict = pickle.load(r_file)

        print("Hydrographs: Just read '{0}'.".format(file_path))

        return return_dict

    @staticmethod
    def get_linkid_desc_area(debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        # TODO - send to def_system
        file_path = Hydrographs._links_pois_desc_area_file_path

        if not os.path.exists(file_path):
            Debug.dl("Hydrographs: File '{0}' not found.".format(file_path), 0, debug_lvl)
            return

        with open(file_path, "rb") as r_file:
            return_dict = pickle.load(r_file)

        return return_dict

    @staticmethod
    def get_linkid_poisall_relationship(debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        # TODO - send to def_system
        file_path = Hydrographs._linkid_poisall_relationship_file_path

        if not os.path.exists(file_path):
            Debug.dl("Hydrographs: File '{0}' not found.".format(file_path), 0, debug_lvl)
            return

        with open(file_path, "rb") as r_file:
            return_dict = pickle.load(r_file)

        return return_dict

    @staticmethod
    def extract_specific_disch_stage(link_rc):
        """
        Extract values of stage and discharge on a appropriate format for interpolation
        :param link_rc: Object extracted from rating curve objects fo a specific link id
        :return: Two arrays of the same size with discharge -> stage values.
        """

        all_disch = []
        all_stage = []
        for cur_rc_elem in link_rc:
            all_disch.append(cur_rc_elem[1])
            all_stage.append(cur_rc_elem[0])

        return all_disch, all_stage
