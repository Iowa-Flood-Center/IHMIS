import os
import re

from FolderDefinition import FolderDefinition


class FileDefinition:
    _runset_file_name = "Runset.json"
    _comparison_set_file_name = "Comparison_matrix.json"
    _evaluation_matrix_file_name = "Evaluation_matrix.json"

    @staticmethod
    def obtain_modelcomb_file_path(modelcomb_id, runset_id, folder_flag=None, debug_lvl=0):
        """

        :param modelcomb_id:
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        folder_path = FolderDefinition.get_meta_scmodelcomb_folder_path(runset_id=runset_id, folder_flag=folder_flag)
        file_path = "{0}.json".format(modelcomb_id)

        return os.path.join(folder_path, file_path)

    @staticmethod
    def obtain_runset_file_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(FolderDefinition.get_meta_scrunset_folder(runset_id=runset_id, folder_flag=folder_flag),
                            FileDefinition._runset_file_name)

    @staticmethod
    def obtain_comparison_set_file_path(runset_id=None, folder_flag=None):
        """

        :return:
        """
        return os.path.join(
            FolderDefinition.get_meta_crossmatrices_folder(runset_id=runset_id, folder_flag=folder_flag),
            FileDefinition._comparison_set_file_name)

    @staticmethod
    def obtain_evaluation_matrix_file_path(runset_id=None, folder_flag=None):
        """

        :param runset_id:
        :param folder_flag:
        :return:
        """
        return os.path.join(
            FolderDefinition.get_meta_crossmatrices_folder(runset_id=runset_id, folder_flag=folder_flag),
            FileDefinition._evaluation_matrix_file_name)

    def __init__(self):
        return
