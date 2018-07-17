from ConsoleCall import ConsoleCall


class ReprCombGenInterface:

    @staticmethod
    def get_modelcomb_id(argv):
        return ConsoleCall.get_arg_str("-modelcomb", argv)

    @staticmethod
    def get_reprcomb_id(argv):
        return ConsoleCall.get_arg_str("-reprcomb", argv)

    @staticmethod
    def get_runset_id(argv):
        return ConsoleCall.get_arg_str("-runsetid", argv)

    @staticmethod
    def get_timestamp(argv):
        return ConsoleCall.get_arg_int("-t", argv)

    @staticmethod
    def get_min_timestamp_hist(argv):
        return ConsoleCall.get_arg_int("-tmin", argv)

    @staticmethod
    def get_max_timestamp_hist(argv):
        return ConsoleCall.get_arg_int("-tmax", argv)

    def __init__(self):
        return
