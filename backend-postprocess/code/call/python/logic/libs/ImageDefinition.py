class ImageDefinition:
    _cols = 1741
    _rows = 1057
    _ext = '.png'
    _ext_name = 'PNG'

    @classmethod
    def define_historical_file_name(cls, timestamp, parameter_acronym, file_extension=None, debug_image=False):
        """

        :param timestamp: Timestamp in integer (seconds)
        :param parameter_acronym: Uses to be something like 'p', 'r', 'ss', 'sl'
        :param file_extension:
        :param debug_image:
        :return: String in format '123212p.png'
        """
        if file_extension is None:
            if not debug_image:
                return str(timestamp) + parameter_acronym + cls._ext
            else:
                return str(timestamp) + parameter_acronym + "_dbg" + cls._ext
        else:
            used_ext = file_extension if file_extension.startswith('.') else ".{0}".format(file_extension)
            return "{0}{1}{2}".format(timestamp, parameter_acronym, used_ext)

    @classmethod
    def define_displayed_file_name(cls, timestamp, parameter_acronym, file_extension=None, debug_image=False):
        """

        :param timestamp: Timestamp in integer (seconds)
        :param parameter_acronym: Uses to be something like 'p', 'r', 'ss', 'sl'
        :param file_extension:
        :param debug_image:
        :return: String in format '123212p.png'
        """
        if file_extension is None:
            if not debug_image:
                return str(timestamp) + parameter_acronym + cls._ext
            else:
                return str(timestamp) + parameter_acronym + "_dbg" + cls._ext
        else:
            used_ext = file_extension if file_extension.startswith('.') else ".{0}".format(file_extension)
            return "{0}{1}{2}".format(timestamp, parameter_acronym, used_ext)

    @classmethod
    def get_image_num_cols(cls):
        return cls._cols

    @classmethod
    def get_image_num_rows(cls):
        return cls._rows

    @classmethod
    def get_image_ext_name(cls):
        return cls._ext_name

    @classmethod
    def get_ext(cls):
        return cls._ext

    def __init__(self):
        return
