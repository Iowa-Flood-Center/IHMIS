class DataFileDefinition:

    @classmethod
    def define_file_name(cls, timestamp, sc_parameter):
        """

        :param timestamp: Timestamp in integer (seconds)
        :param sc_parameter: Uses to be something like 'p', 'r', 'ss', 'sl'
        :return: String in format '123212p.csv'
        """
        return str(timestamp) + sc_parameter + cls.get_file_ext(sc_parameter)

    @classmethod
    def obtain_datafile_parameter(cls, csv_file_name):
        """
        NOTE: renamed from 'obtain_file_datatype'
        :param csv_file_name: Name of data file. Cannot be file path.
        :return: String with parameter of data file. Example: for 231498p.csv file, datatype is 'p'
        """
        if csv_file_name is not None:
            sub1 = re.sub("[0123456789]|\..*$", "", csv_file_name)  # removes initial numbers and final extension
            sub2 = re.sub("_+", "_", sub1)
            return sub2
        else:
            return None

    @classmethod
    def get_ext(cls):
        return cls._ext

    def __init__(self):
        return
