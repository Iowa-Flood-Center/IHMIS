import urllib2

from DotConstants import DotConstants


class DotWS:

    @staticmethod
    def get_forecast(sc_dot_model_id, only_forecast=False):
        """

        :param sc_dot_model_id:
        :param only_forecast:
        :return:
        """

        model_id = DotConstants.get_raw_sc_model_id(sc_dot_model_id)
        if model_id is None:
            print("DotWS: sc_model_id '{0}' not supported.".format(sc_dot_model_id))
            return None

        arg_only_f = "&only_forecast=yes" if only_forecast else ""
        arguments = "forecast_id={0}{1}&show_me=the_truth&show_linkid=yes".format(model_id, arg_only_f)
        the_url = "?".join([DotConstants.get_webservice_address(), arguments])

        print("DotWS: Reading from '{0}'.".format(the_url))

        http_content = urllib2.urlopen(the_url).read()
        http_content_lines = http_content.split("\n")
        return http_content_lines

    def __init__(self):
        return
