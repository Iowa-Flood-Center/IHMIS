import numpy as np
import h5py
import os

from Debug import Debug


class H5FileReader:

    @staticmethod
    def get_data_from_asynch_hydrograph_h5(hdf5_file_path, debug_lvl=0):
        """

        :param hdf5_file_path:
        :param debug_lvl:
        :return:
        """

        # basic check - file must exist
        if (hdf5_file_path is None) or (not os.path.exists(hdf5_file_path)):
            Debug.dl("H5FileReader: File '{0}' does not exist.".format(hdf5_file_path), 1, debug_lvl)
            return None, None

        # import data into matrix
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            hdf_data = np.array(hdf_file.get('outputs'))

        return hdf_data

    @staticmethod
    def get_linkindex_from_asynch_hydrograph_h5(hdf5_file_path, debug_lvl=0):
        """

        :param hdf5_file_path:
        :param debug_lvl:
        :return:
        """

        # basic check - file must exist
        if (hdf5_file_path is None) or (not os.path.exists(hdf5_file_path)):
            Debug.dl("H5FileReader: File '{0}' does not exist.".format(hdf5_file_path), 1, debug_lvl)
            return None, None

        # import data into matrix
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            return np.array(hdf_file.get('linkid_index')) if 'linkid_index' in hdf_file.keys() else None

    @staticmethod
    def create_linkid_index_asynch_hydrograph_h5(hdf5_file_path, force=False, debug_lvl=0):
        """

        :param hdf5_file_path:
        :return:
        """

        # basic check - file must exist
        if (hdf5_file_path is None) or (not os.path.exists(hdf5_file_path)):
            Debug.dl("H5FileReader: File '{0}' does not exist.".format(hdf5_file_path), 1, debug_lvl)
            return None, None

        # import data into matrix
        with h5py.File(hdf5_file_path, 'r+') as hdf_file:

            # basic check
            if 'linkid_index' in hdf_file.keys():
                if not force:
                    Debug.dl("H5FileReader: Dataset 'linkid_index' already exists in '{0}' file.".format(hdf5_file_path), 1,
                             debug_lvl)
                    return
                else:
                    del hdf_file['linkid_index']

            hdf_data = np.array(hdf_file.get('outputs'))

            # build index
            # count_debug = 5
            last_link_id = None
            link_index = []
            cur_i = 0
            for cur_row in hdf_data:

                cur_link_id = cur_row[0]
                if (last_link_id is None) or (cur_link_id != last_link_id):
                    link_index.append((cur_link_id, cur_i))

                last_link_id = cur_link_id
                cur_i += 1

                # if len(link_index) >= count_debug:
                #    break

            # write it to file
            link_index_numpy = np.asarray(link_index, dtype=np.uint32)
            hdf_file.create_dataset('linkid_index', data=link_index_numpy)

        Debug.dl("H5FileReader: Created index for '{0}' file.".format(hdf5_file_path), 1, debug_lvl)

    def __init__(self):
        return
