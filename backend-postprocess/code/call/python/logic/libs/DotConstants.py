from libs.SettingsVirtualGages import SettingsVirtualGages


class DotConstants:
    _ws = "http://s-iihr50.iihr.uiowa.edu/virtualgages/ws/summary.php"
    _scmodels_dict = None

    @staticmethod
    def get_webservice_address():
        return DotConstants._ws

    @staticmethod
    def get_raw_sc_model_id(sc_dot_model_id):
        """

        :param sc_dot_model_id:
        :return:
        """
        if DotConstants._scmodels_dict is None:
            DotConstants._scmodels_dict = SettingsVirtualGages.get("sc_models_equivalence")

        if sc_dot_model_id in DotConstants._scmodels_dict:
            return DotConstants._scmodels_dict[sc_dot_model_id]
        else:
            return None

    def __init__(self):
        return
