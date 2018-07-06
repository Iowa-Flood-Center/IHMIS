import os

from FolderDefinition import FolderDefinition
from H5FileReader import H5FileReader
from Debug import Debug


class BinaryLibrary:

    # types of data
    DT_DENSE_SNAPSHOT = 1      # numpy vector
    DT_DENSE_TIMESERIES = 2    # hdf5 file
    DT_SPARCE_SNAPSHOT = 3     # pickle dictionary key -> value
    DT_SPARCE_TIMESERIES = 4   # pickle dictionary key -> [(time, value), ...]

    # product-type relationship
    # TODO - list all
    # TODO - move statics to database - cache (?)
    DT_PRODUCT = {
        "idq":   DT_DENSE_SNAPSHOT,
        "ids_s": DT_DENSE_SNAPSHOT,
        "fq":    DT_DENSE_TIMESERIES,
        "istg":  DT_SPARCE_TIMESERIES
    }

    # type-file ext relationship
    DT_FILEEXT = {
        DT_DENSE_SNAPSHOT: ".npy",
        DT_DENSE_TIMESERIES: ".h5",
        DT_SPARCE_SNAPSHOT: None,
        DT_SPARCE_TIMESERIES: None
    }

    # simple cache
    DATA_CACHE = {
        "file_path": None,
        "file_data": None
    }

    @staticmethod
    def get_timeseries_for_linkid_product(sc_runset_id, sc_model_id, sc_product_id, link_id, timestamp_ini=None,
                                          timestamp_end=None, timestamp_release=None, debug_lvl=0):
        """

        :param sc_runset_id:
        :param sc_model_id:
        :param sc_product_id:
        :param timestamp_ini:
        :param timestamp_end:
        :param timestamp_release:
        :return:
        """

        # get datatype and basic check it
        prod_datatype = BinaryLibrary._get_datatype(sc_product_id=sc_product_id)
        if prod_datatype is None:
            Debug.dl("BinaryLibrary: No datatype defined for product '{0}'.".format(sc_product_id), 1, debug_lvl)
            return None

        # call proper function
        if prod_datatype == BinaryLibrary.DT_DENSE_SNAPSHOT:
            # TODO - make call
            return None
        elif prod_datatype == BinaryLibrary.DT_DENSE_TIMESERIES:
            return BinaryLibrary._get_timeseries_for_linkid_densetimeseries(sc_runset_id, sc_model_id, sc_product_id,
                                                                            link_id, timestamp_ini=timestamp_ini,
                                                                            timestamp_end=timestamp_end,
                                                                            timestamp_release=timestamp_release,
                                                                            debug_lvl=debug_lvl)
        else:
            Debug.dl("BinaryLibrary: Unexpected datatype code '{0}'.".format(prod_datatype), 1, debug_lvl)
            return None

    @staticmethod
    def get_binary_file_path(sc_runset_id, sc_model_id, sc_product_id, timestamp, debug_lvl=0):
        """

        :param sc_runset_id:
        :param sc_model_id:
        :param sc_product_id:
        :param timestamp:
        :param debug_lvl:
        :return:
        """

        folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, sc_product_id,
                                                                        runset_id=sc_runset_id)
        file_name = BinaryLibrary._get_filename(sc_product_id, timestamp, debug_lvl=debug_lvl)
        return os.path.join(folder_path, file_name)

    @staticmethod
    def _get_datatype(sc_product_id=None, debug_lvl=0):
        """

        :param sc_product_id:
        :return:
        """

        if (sc_product_id is None) or (sc_product_id not in BinaryLibrary.DT_PRODUCT):
            # TODO - debug
            return None
        else:
            return BinaryLibrary.DT_PRODUCT[sc_product_id]

    @staticmethod
    def _get_fileextension(sc_product_id=None, debug_lvl=0):
        """

        :param sc_product_id:
        :param debug_lvl:
        :return:
        """

        the_datatype = BinaryLibrary._get_datatype(sc_product_id=sc_product_id, debug_lvl=debug_lvl)
        if (the_datatype is None) or (the_datatype not in BinaryLibrary.DT_FILEEXT):
            # TODO - debug
            return None
        else:
            return BinaryLibrary.DT_FILEEXT[the_datatype]

    @staticmethod
    def _get_filename(sc_product_id, timestamp, debug_lvl=0):
        """

        :param sc_product_id:
        :param timestamp:
        :param debug_lvl:
        :return:
        """

        if (sc_product_id is None) or (timestamp is None):
            # TODO - debug
            return None

        file_ext = BinaryLibrary._get_fileextension(sc_product_id=sc_product_id, debug_lvl=debug_lvl)
        return "{0}{1}{2}".format(timestamp, sc_product_id, file_ext)

    @staticmethod
    def _get_timeseries_for_linkid_densetimeseries(sc_runset_id, sc_model_id, sc_product_id, link_id,
                                                   timestamp_ini=None, timestamp_end=None, timestamp_release=None,
                                                   cache=True, debug_lvl=0):
        """

        :param sc_runset_id:
        :param sc_model_id:
        :param sc_product_id:
        :param timestamp_ini:
        :param timestamp_end:
        :param timestamp_release:
        :return: List of (timestamp, data) pairs
        """

        # read all timeseries from a single file
        if (timestamp_release is not None) and (timestamp_ini is None) and (timestamp_end is None):

            # define file path
            file_path = BinaryLibrary.get_binary_file_path(sc_runset_id, sc_model_id, sc_product_id, timestamp_release,
                                                           debug_lvl=debug_lvl)

            # basic check: file must exist
            if not os.path.exists(file_path):
                Debug.dl("BinaryLibrary: File '{0}' does not exist.".format(file_path), 1, debug_lvl)
                return None

            start_time = time.time()

            # 2 - load data - read file content or use cache
            if (not cache) or (BinaryLibrary.DATA_CACHE["file_path"] != file_path):
                Debug.dl("BinaryLibrary: Reading file '{0}'.".format(file_path), 2, debug_lvl)
                file_data = H5FileReader.get_data_from_asynch_hydrograph_h5(file_path, debug_lvl=debug_lvl)
                BinaryLibrary.DATA_CACHE["file_path"] = file_path
                BinaryLibrary.DATA_CACHE["file_data"] = file_data
            else:
                Debug.dl("BinaryLibrary: Cached file '{0}'.".format(file_path), 3, debug_lvl)
                file_data = BinaryLibrary.DATA_CACHE["file_data"]

            # cur_time_1 = time.time()
            # d_time = cur_time_1 - start_time
            # print("Read data in {0} seconds.".format(d_time))

            # if file is not indexed, try to index it
            link_index = H5FileReader.get_linkindex_from_asynch_hydrograph_h5(file_path, debug_lvl=debug_lvl)
            if link_index is None:
                Debug.dl("BinaryLibrary: Indexing file '{0}'.".format(file_path), 1, debug_lvl)
                H5FileReader.create_linkid_index_asynch_hydrograph_h5(file_path, force=True, debug_lvl=debug_lvl)
                link_index = H5FileReader.get_linkindex_from_asynch_hydrograph_h5(file_path, debug_lvl=debug_lvl)
                if link_index is None:
                    Debug.dl("BinaryLibrary: File '{0}' has not index possible.".format(file_path), 1, debug_lvl)
                    return

            # cur_time_0 = time.time()
            # d_time = cur_time_0 - cur_time_1
            # print("Read index in {0} seconds.".format(d_time))

            # get starting index
            cur_idx = None
            for cur_link_index in link_index:
                if cur_link_index[0] == link_id:
                    cur_idx = cur_link_index[1]
                    break

            # basic check
            if cur_idx is None:
                return None

            # cur_time_3 = time.time()
            # d_time = cur_time_3 - cur_time_0
            # print("Found starting index for link {0} ({1}) in {2} seconds.".format(link_id, cur_idx, d_time))

            # 3 - process it
            linkid_timeseries = []
            while True:
                cur_row = file_data[cur_idx]
                cur_linkid = cur_row[0]

                if cur_linkid != link_id:
                    break

                cur_timestamp = int(timestamp_release + (cur_row[1] * 60))
                cur_data = cur_row[2]

                linkid_timeseries.append((cur_timestamp, cur_data))
                cur_idx += 1
            cur_idx -= 1

            # cur_time_2 = time.time()
            # d_time = cur_time_2 - cur_time_1
            # print("Extracted {0} values (until index {1}) in {2} seconds.".format(len(linkid_timeseries), cur_idx,
            #                                                                       d_time))

            # 4 - return it
            return linkid_timeseries

        else:
            Debug.dl("BinaryLibrary: Unexpected argument set ({0}, {1}, {2}).".format(timestamp_ini, timestamp_end,
                                                                                timestamp_release), 1, debug_lvl)
            return None

    def __init__(self):
        return