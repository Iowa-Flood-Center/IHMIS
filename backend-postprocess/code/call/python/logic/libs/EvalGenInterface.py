from ConsoleCall import ConsoleCall


class EvalGenInterface:

    # ##################################################### HIST ##################################################### #
    # # Interface: sc_model_id [-t timestamp] [-ref sc_reference_id]                                                 # #
    # #   sc_model_id     : string - mandatory                                                                       # #
    # #   timestamp       : integer - optative                                                                       # #
    # #   sc_reference_id : string - mandatory                                                                       # #
    # ################################################################################################################ #

    @staticmethod
    def get_model_id(argv):
        return ConsoleCall.get_arg_str(1, argv)

    @staticmethod
    def get_timestamp(argv):
        return ConsoleCall.get_arg_int("-t", argv)

    @staticmethod
    def get_min_timestamp_hist(argv):
        return ConsoleCall.get_arg_int("-tmin", argv)

    @staticmethod
    def get_max_timestamp_hist(argv):
        return ConsoleCall.get_arg_int("-tmax", argv)

    @staticmethod
    def get_reference_id(argv, default_val=None):
        return ConsoleCall.get_arg_str("-ref", argv, default_value=default_val)

    @staticmethod
    def get_runset_id(argv):
        return ConsoleCall.get_arg_str("-runsetid", argv)

    # ##################################################### HIST ##################################################### #
    # # Interface: min_timestamp max_timestamp [-m model_id] [-ps parameter_set]                                     # #
    # #   min_timestamp : integer - mandatory                                                                        # #
    # #   max_timestamp : integer - mandatory                                                                        # #
    # #   model_id : string - optative                                                                               # #
    # #   parameter_set : string ("state" for states, "q_for" for hydroforecast. "state" is default) - optative      # #
    # ################################################################################################################ #

    '''
    @staticmethod
    def get_min_timestamp_hist(argv):
        return ConsoleCall.get_arg_int(1, argv)

    @staticmethod
    def get_max_timestamp_hist(argv):
        return ConsoleCall.get_arg_int(2, argv)

    @staticmethod
    def get_model_id_hist(argv):
        return ConsoleCall.get_arg_str("-m", argv)

    @staticmethod
    def get_parameterset_hist(argv):
        return ConsoleCall.get_arg_str("-ps", argv)
    '''

    def __init__(self):
        return
