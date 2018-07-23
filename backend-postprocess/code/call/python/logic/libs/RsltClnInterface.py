from ConsoleCall import ConsoleCall


class RsltClnInterface:

    # ##################################################### HIST ##################################################### #
    # # Interface: [-m SC_MODEL_ID] [-e SC_EVALUATION_ID] [-ref SC_REFERENCE_ID] [-rep SC_REPRESENTATION_ID]         # #
    # #                                                     [-t TIMESTAMP] [-tdays T_DAYS] [-runsetid SC_RUNSET_ID]  # #
    # #   SC_MODEL_ID          : string - mandatory                                                                  # #
    # #   SC_EVALUATION_ID     : string - optative - if missing, assumes is the cleaning of a representation         # #
    # #   SC_REFERENCE_ID      : string - optative - if missing, assumes is the cleaning of a representation         # #
    # #   SC_REPRESENTATION_ID : string - optative - if missing, assumes is the cleaning of an evaluation            # #
    # #   TIMESTAMP            : integer - optative - if missing, assumes the latest available time as last time     # #
    # #   T_DAYS               : float  - optative - if missing, assumes 1.5 days for eval, 10.5 for representation  # #
    # #   SC_RUNSET_ID         : string - mandatory                                                                  # #
    # ################################################################################################################ #

    @staticmethod
    def get_model_id(argv, default_val=None):
        return ConsoleCall.get_arg_str("-m", argv, default_value=default_val)

    @staticmethod
    def get_evaluation_id(argv, default_val=None):
        return ConsoleCall.get_arg_str("-e", argv, default_value=default_val)

    @staticmethod
    def get_reference_id(argv, default_val=None):
        return ConsoleCall.get_arg_str("-ref", argv, default_value=default_val)

    @staticmethod
    def get_representation_id(argv, default_val=None):
        return ConsoleCall.get_arg_str("-rep", argv, default_value=default_val)

    @staticmethod
    def get_timestamp(argv):
        return ConsoleCall.get_arg_int("-t", argv)

    @staticmethod
    def get_back_days(argv):
        return ConsoleCall.get_arg_flt("-tdays", argv)

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

    def __init__(self):
        return
