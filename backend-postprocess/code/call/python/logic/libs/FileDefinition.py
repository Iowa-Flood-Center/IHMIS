import os


class FileDefinition:
    _runset_file_name = "Runset.json"
    _comparison_set_file_name = "Comparison_matrix.json"
    _evaluation_matrix_file_name = "Evaluation_matrix.json"

    def __init__(self):
        return

    @staticmethod
    def obtain_hist_file_timestamp(historical_file_name):
        """
        Obtain timestamp from historical file name
        :param historical_file_name: Just the file name, starting by a unix timestamp
        :return: Integer if it was possible to retrieve timestamp, None otherwise
        """
        if historical_file_name is not None:
            # try:
            splited = re.split("[^0123456789]", historical_file_name)
            return None if splited[0] == '' else int(splited[0])
            # 'except TypeError:
            #    print("+++ None from '{0}'".format(historical_file_name))
            #    return None
        else:
            return None

    @staticmethod
    def obtain_hist_file_linkid(historical_file_name):
        """
        Obtain linkid from distributed historical file
        :param historical_file_name: Just the file name, starting by a unix timestamp
        :return: Integer if it was possible to retrieve linkid, None otherwise
        """
        if historical_file_name is not None:
            file_basename = historical_file_name.split(".")[0]
            splited_underline = file_basename.split("_")
            if len(splited_underline) > 1:
                try:
                    return int(splited_underline[1])
                except ValueError:
                    return None
            else:
                return None
        else:
            return None

    @staticmethod
    def obtain_dist_file_timestamp(distribution_file_name):
        """

        :param distribution_file_name:
        :return:
        """
        if distribution_file_name is not None:
            # remove extension
            clean_name = ".".join(distribution_file_name.split(".")[0:-1])
            last_part_from_underlines = clean_name.split("_")[-1]
            try:
                return int(last_part_from_underlines)
            except Exception as e:
                return None
        else:
            return None

    @staticmethod
    def obtain_fore_file_timestamp(forecast_file_name):
        """
        Obtain timestamp from forecast file name
        :param forecast_file_name: Just the file name, starting by a unix timestamp
        :return: Integer if it was possible to retrieve timestamp, None otherwise
        """
        if forecast_file_name is not None:
            splited = re.split("[^0123456789]", forecast_file_name)
            return None if ((splited[0] == '') or (len(splited) < 2)) else int(splited[0]) + (int(splited[1]) * 3600)
        else:
            return None

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
