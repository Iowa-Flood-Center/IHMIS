import datetime
import time


class GeneralUtils:

    @staticmethod
    def round_timestamp_hour(the_timestamp):
        """
        Retrieve closest hour-rounded timestamp of a timestamp. Example: 18:00 for 18:07, 14:00 for 13:44.
        :param the_timestamp: Integer. The timestamp to be rounded.
        :return: Integer. The timestamp of rounded hour.
        """
        the_datetime = datetime.datetime.fromtimestamp(the_timestamp)
        the_minutes = the_datetime.minute
        ret_datetime = the_datetime.replace(minute=0, second=0)
        if the_minutes >= 30:
            ret_datetime += datetime.timedelta(hours=1)

        return int(time.mktime(ret_datetime.timetuple()))

    @staticmethod
    def floor_timestamp_day(the_timestamp):
        """
        Retrieve the closest day_floored timestamp of a timestamp.
        :param the_timestamp: Integer. The timestamp to be floored.
        :return: Integer. The timestamp of a floored day.
        """
        the_datetime = datetime.datetime.fromtimestamp(the_timestamp)
        ret_datetime = the_datetime.replace(hour=0, minute=0, second=0)
        return int(time.mktime(ret_datetime.timetuple()))

    @staticmethod
    def truncate_timestamp_hour(the_timestamp):
        """
        Retrieve hour-truncated timestamp of a timestamp. Example: 18:00 for 18:07, 13:00 for 13:44
        :param the_timestamp: Integer. The timestamp to be rounded.
        :return: Integer. The timestamp of rounded hour.
        """

        the_datetime = datetime.datetime.fromtimestamp(the_timestamp)
        ret_datetime = the_datetime.replace(minute=0, second=0)
        return int(time.mktime(ret_datetime.timetuple()))

    def __init__(self):
        return
