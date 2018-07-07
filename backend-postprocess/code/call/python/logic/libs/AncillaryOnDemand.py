import numpy as np

from BinAncillaryDefinition import BinAncillaryDefinition


class AncillaryOnDemand:
    """
    This object is used to load only one time each execution. Files are loaded once on demand and kept in memory.
    """
    _linkid_link_mask = None
    _linkid_hill_mask = None          # TODO
    _qunit_thresholds = {}
    _fidx_thresholds = None
    _linkid_qpeak_vals = None         # TODO
    _linkid_upstreamarea_vals = None  # TODO

    # input_bin_soilmask_path = BinLinkidMaskDefinition.get_slopes_file_path()
    # input_bin_qpeak_path = BinLinkidAncillaryDefinition.get_qpeak_file_path()
    # input_bin_upstreamarea_path = BinLinkidAncillaryDefinition.get_upstreamarea_file_path()

    def get_qunit_thresholds(self, month):
        """
        Self-explaining name
        :param month:
        :return: Content of binary file
        """
        if month not in self._qunit_thresholds.keys():
            cur_bin_file_path = BinAncillaryDefinition.get_unit_thresholds_file(month)
            self._qunit_thresholds[month] = np.load(cur_bin_file_path)
        return self._qunit_thresholds[month]

    def get_fidx_thresholds(self):
        """

        :return:
        """
        if self._fidx_thresholds is None:
            cur_bin_file_path = BinAncillaryDefinition.get_flood_index_thresholds_file_path()
            self._fidx_thresholds = np.load(cur_bin_file_path)
        return self._fidx_thresholds

    def get_linkid_link_mask(self):
        """
        Self-explaining name
        :return:
        """
        if self._linkid_link_mask is None:
            cur_bin_file_path = BinAncillaryDefinition.get_linksbuffer_file_path()
            AncillaryOnDemand._linkid_link_mask = np.load(cur_bin_file_path)
        return self._linkid_link_mask

    def get_linkid_hills_mask(self):
        """
        Self-explaining name
        :return:
        """
        if self._linkid_hill_mask is None:
            cur_bin_file_path = BinAncillaryDefinition.get_linksslopes_file_path()
            AncillaryOnDemand._linkid_hill_mask = np.load(cur_bin_file_path)
        return self._linkid_hill_mask

    def __init__(self):
        return
