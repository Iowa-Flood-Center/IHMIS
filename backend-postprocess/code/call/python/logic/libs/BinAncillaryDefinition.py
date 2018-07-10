import os

from Settings import Settings


class BinAncillaryDefinition:
    _bin_ancillary_files_folder_path = os.path.join(Settings.get("raw_data_folder_path"), "anci")
    _bin_ratingcurves_folder_path = os.path.join(_bin_ancillary_files_folder_path, "rating_curves")
    _bin_thresholds_folder_path = os.path.join(_bin_ancillary_files_folder_path, "thresholds")
    _bin_params_folder_path = os.path.join(_bin_ancillary_files_folder_path, "params")
    _bin_masks_folder_path = os.path.join(_bin_ancillary_files_folder_path, "masks")
    _bin_links_folder_path = os.path.join(_bin_ancillary_files_folder_path, "links")
    _bin_pois_folder_path = os.path.join(_bin_ancillary_files_folder_path, "pois")

    _bin_qunit_subfolder_path = os.path.join(_bin_thresholds_folder_path, "qunit")

    _bin_linkid_floodindexthresholds_filename = "links_floodthresholds.npy"
    _bin_linkid_linksbuffer_filename = "linksbuffer_l4_mask_webmerc.npy"
    _bin_linkid_linksslopes_filename = "hillslopes_mask_webmerc.npy"
    _bin_linkid_missi_missu_filename = "linkids_missi_missu.npy"
    _bin_linkid_latlng_filename = "links_latlng.p"
    _bin_usgsid_linkid_filename = "usgsid_linkid.p"

    @staticmethod
    def get_bin_ancillary_files_folder_path():
        return BinAncillaryDefinition._bin_ancillary_files_folder_path

    @staticmethod
    def get_bin_thresholds_file_path(file_name):
        return os.path.join(BinAncillaryDefinition._bin_thresholds_folder_path, file_name)

    @staticmethod
    def get_bin_pois_file_path(file_name):
        return os.path.join(BinAncillaryDefinition._bin_pois_folder_path, file_name)

    @staticmethod
    def get_linksbuffer_file_path():
        return os.path.join(BinAncillaryDefinition._bin_masks_folder_path,
                            BinAncillaryDefinition._bin_linkid_linksbuffer_filename)

    @staticmethod
    def get_linksslopes_file_path():
        return os.path.join(BinAncillaryDefinition._bin_masks_folder_path,
                            BinAncillaryDefinition._bin_linkid_linksslopes_filename)

    @staticmethod
    def get_linkids_missi_missu_file_path():
        return os.path.join(BinAncillaryDefinition._bin_links_folder_path,
                            BinAncillaryDefinition._bin_linkid_missi_missu_filename)

    @staticmethod
    def get_linkids_latlng_file_path():
        return os.path.join(BinAncillaryDefinition._bin_links_folder_path,
                            BinAncillaryDefinition._bin_linkid_latlng_filename)

    @staticmethod
    def get_usgsid_linkid_file_path():
        return os.path.join(BinAncillaryDefinition._bin_links_folder_path,
                            BinAncillaryDefinition._bin_usgsid_linkid_filename)

    @staticmethod
    def get_flood_index_thresholds_file_path():
        return os.path.join(BinAncillaryDefinition._bin_thresholds_folder_path,
                            BinAncillaryDefinition._bin_linkid_floodindexthresholds_filename)

    @staticmethod
    def get_unit_thresholds_file(month):
        thresholds_bin_file_name = "{0}.npy".format(month)
        thresholds_bin_file_path = os.path.join(BinAncillaryDefinition._bin_qunit_subfolder_path,
                                                thresholds_bin_file_name)
        return thresholds_bin_file_path

    @staticmethod
    def get_rating_curve_file_path(provider):
        """

        :param provider: Expected 'usgs', 'ifc' or 'dot'
        :return: String with file path for pickle file
        """

        file_name = "rc_{0}.p".format(provider)
        return os.path.join(BinAncillaryDefinition._bin_ratingcurves_folder_path, file_name)

    def __init__(self):
        return
