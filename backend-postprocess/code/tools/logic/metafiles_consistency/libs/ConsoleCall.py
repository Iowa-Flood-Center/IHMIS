
class ConsoleCall:

    def __init__(self):
        return

    @staticmethod
    def calls_help(argv):
        return False if ((argv is None) or ('-h' not in argv)) else True

    @staticmethod
    def get_arg_str(arg, argv, default_value=None):
        """

        :param arg: Or a number (for index) or a string (for argument name - example: '-t')
        :param argv: Usually it is expected to be placed "sys.argv"
        :param default_value: Value to be returned in case of argument is not found
        :return: Value of argument in string if it is there, None otherwise
        """

        if (arg is None) or (argv is None):
            return None
        elif isinstance(arg, int):
            return argv[arg] if len(argv) > arg else default_value
        elif isinstance(arg, str):
            arg_idx = (argv.index(arg) + 1) if ((arg in argv) and (len(argv) > (argv.index(arg) + 1))) else None
            return argv[arg_idx] if ((arg_idx is not None) and (argv[arg_idx] != '')) else default_value
        else:
            return default_value

    @staticmethod
    def get_arg_int(arg, argv):
        """

        :param arg:
        :param argv:
        :return:
        """
        arg_str = ConsoleCall.get_arg_str(arg, argv)
        return int(arg_str) if ((arg_str is not None) and (arg_str != '')) else None