
class ScModelProvider:
    _models = None

    def __init__(self):
        return

    @staticmethod
    def _load_models_if_necessary(debug_lvl=0):
        """
        Read meta files if necessary and updates local variable
        :param debug_lvl:
        :return: None. Changes are performed internally to the object
        """

        if ModelProvider._models is None:
            metafile_mng = MetaFileManager()
            MetaFileManager.load_all_scmodel_meta_info(ignore_fails=True, debug_lvl=debug_lvl)
            ModelProvider._models = metafile_mng.get_all_scmodel_ids()