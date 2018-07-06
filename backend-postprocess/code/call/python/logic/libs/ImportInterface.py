from ConsoleCall import ConsoleCall


class ImportInterface:

    @staticmethod
    def get_model_id(argv):
        return ConsoleCall.get_arg_str("-model_sing_id", argv)

    @staticmethod
    def get_timestamp(argv):
        return ConsoleCall.get_arg_int("-t", argv)

    @staticmethod
    def get_flextime(argv):
        return ConsoleCall.get_arg_int("-flex", argv)

    # ##################################################### HIST ##################################################### #
    # # Interface: min_timestamp max_timestamp [-m model_id] [-ps parameter_set]                                     # #
    # #   min_timestamp : integer - mandatory                                                                        # #
    # #   max_timestamp : integer - mandatory                                                                        # #
    # #   model_id : string - optative                                                                               # #
    # #   parameter_set : string ("state" for states, "q_for" for hydroforecast. "state" is default) - optative      # #
    # ################################################################################################################ #

    @staticmethod
    def get_min_timestamp_hist(argv):
        return ConsoleCall.get_arg_int("-tmin", argv)

    @staticmethod
    def get_max_timestamp_hist(argv):
        return ConsoleCall.get_arg_int("-tmax", argv)

    @staticmethod
    def get_runset_id(argv):
        return ConsoleCall.get_arg_str("-runset_id", argv)

    @staticmethod
    def get_reference_id(argv):
        return ConsoleCall.get_arg_str("-ref", argv)

    @staticmethod
    def get_model_id_hist(argv):
        return ConsoleCall.get_arg_str("-m", argv)

    @staticmethod
    def get_parameterset_hist(argv):
        return ConsoleCall.get_arg_str("-ps", argv)

    def __init__(self):
        return