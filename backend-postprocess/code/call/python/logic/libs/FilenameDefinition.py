import re


class FilenameDefinition:

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

    def __init__(self):
        return
