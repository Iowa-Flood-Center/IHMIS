from ConsistMetaDefs import ConsistMetaDefs
import os


class MetaFolderDefinition:
    EFF_FLAG = 1  # effective type
    SBX_FLAG = 2  # sandbox flag
    FOLDER_FLAGS = (EFF_FLAG, SBX_FLAG)

    _root_path_runset_format = os.path.join(ConsistMetaDefs.get_runset_root_path(), "{0}/")
    _root_effective_path_runset_format = os.path.join(_root_path_runset_format, "metafiles")
    _root_sandbox_path_runset_format = os.path.join(_root_path_runset_format, "metafiles_sandbox")

    _sc_runset_foldername = "sc_runset"
    _sc_runset_filename = "Runset.json"
    _sc_models = "sc_models"
    _sc_modelcombinations = "sc_modelcombinations"
    _sc_references_foldername = "sc_references"
    _sc_products_foldername = "sc_products"
    _sc_representations_foldername = "sc_representations"
    _sc_represcomps_foldername = "sc_represcomps"
    _sc_evaluations = "sc_evaluations"
    _cross_matrix_folder = "cross_matrices"
    _comparison_matrix_filename = "Comparison_matrix.json"
    _evaluation_matrix_filename = "Evaluation_matrix.json"
    _forecast_matrix_filename = "Forecast_matrix.json"
    _menu_folder = "sc_menu"
    _menu_filename = "Menu.json"

    @staticmethod
    def get_root_path(folder_flag, runset_id=None):
        """

        :param folder_flag: Expected to be MetaFolderDefinition.EFF_FLAG or MetaFolderDefinition.SBX_FLAG
        :param runset_id:
        :return: String.
        """

        if folder_flag == MetaFolderDefinition.EFF_FLAG:
            return MetaFolderDefinition._root_effective_path_runset_format.format(runset_id)
        elif folder_flag == MetaFolderDefinition.SBX_FLAG:
            return MetaFolderDefinition._root_sandbox_path_runset_format.format(runset_id)
        else:
            return None

    # sc runsets methods

    @staticmethod
    def get_runset_file_path(folder_flag, runset_id=None):
        runset_file_path = os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                                        MetaFolderDefinition._sc_runset_foldername,
                                        MetaFolderDefinition._sc_runset_filename)
        return runset_file_path

    # sc models methods

    @staticmethod
    def get_all_sc_model_ids(folder_flag, runset_id=None):
        sc_models_folder_path = MetaFolderDefinition.get_sc_models_folder_path(folder_flag, runset_id=runset_id)
        all_sc_model_file = [os.path.splitext(f)[0] for f in os.listdir(sc_models_folder_path)]
        return all_sc_model_file

    @staticmethod
    def get_sc_models_folder_path(folder_flag, runset_id=None):
        """

        :param folder_flag:
        :param runset_id:
        :return:
        """
        return os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                            MetaFolderDefinition._sc_models)

    @staticmethod
    def get_sc_model_file_path(scmodel_id, folder_flag, runset_id=None):
        """

        :param scmodel_id:
        :param folder_flag:
        :param runset_id:
        :return:
        """
        file_name = "{0}.json".format(scmodel_id)
        folder_path = MetaFolderDefinition.get_sc_models_folder_path(folder_flag, runset_id=runset_id)
        return os.path.join(folder_path, file_name)

    @staticmethod
    def get_all_sc_models_file_path(folder_flag, runset_id=None):
        """

        :param folder_flag:
        :param runset_id:
        :return:
        """

        sc_models_folder_path = MetaFolderDefinition.get_sc_models_folder_path(folder_flag, runset_id=runset_id)
        all_sc_model_file = [os.path.join(sc_models_folder_path, f) for f in os.listdir(sc_models_folder_path)]
        return all_sc_model_file

    # model combinations

    @staticmethod
    def get_sc_modelcombinations_folder_path(folder_flag, runset_id=None):
        """

        :param folder_flag:
        :param runset_id:
        :return:
        """

        return os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                            MetaFolderDefinition._sc_modelcombinations)

    @staticmethod
    def get_all_sc_modelcombinations_file_path(folder_flag, runset_id=None):
        """

        :param folder_flag:
        :param runset_id:
        :return:
        """

        sc_modelcombinations_folder_path = MetaFolderDefinition.get_sc_modelcombinations_folder_path(folder_flag,
                                                                                                     runset_id=runset_id)

        # basic check - folder may not exist
        if not os.path.exists(sc_modelcombinations_folder_path):
            return []

        # list inner filer and build paths
        all_sc_modelcombination_file = [os.path.join(sc_modelcombinations_folder_path, f) for f in
                                        os.listdir(sc_modelcombinations_folder_path)]
        return all_sc_modelcombination_file

    # references

    @staticmethod
    def get_all_sc_reference_ids(folder_flag, runset_id=None):
        references_folder_path = MetaFolderDefinition.get_sc_references_folder_path(folder_flag, runset_id=runset_id)
        all_references_id = [os.path.splitext(f)[0] for f in os.listdir(references_folder_path)]
        return all_references_id

    @staticmethod
    def get_sc_references_folder_path(folder_flag, runset_id=None):
        return os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                            MetaFolderDefinition._sc_references_foldername)

    @staticmethod
    def get_all_sc_references_file_path(folder_flag, runset_id=None):
        references_folder_path = MetaFolderDefinition.get_sc_references_folder_path(folder_flag, runset_id=runset_id)
        all_references_file = [os.path.join(references_folder_path, f) for f in os.listdir(references_folder_path)]
        return all_references_file

    # products methods

    @staticmethod
    def get_sc_products_folder_path(folder_flag, runset_id=None):
        if folder_flag in MetaFolderDefinition.FOLDER_FLAGS:
            return os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                                MetaFolderDefinition._sc_products_foldername)
        else:
            return None

    @staticmethod
    def get_all_sc_product_ids(folder_flag, runset_id=None):
        if folder_flag in MetaFolderDefinition.FOLDER_FLAGS:
            sc_products_folder_path = MetaFolderDefinition.get_sc_products_folder_path(folder_flag, runset_id=runset_id)
            all_products_id = [os.path.splitext(f)[0] for f in os.listdir(sc_products_folder_path)]
            return all_products_id
        else:
            return None

    @staticmethod
    def get_all_sc_products_file_path(folder_flag, runset_id=None):
        if folder_flag in MetaFolderDefinition.FOLDER_FLAGS:
            sc_products_folder_path = MetaFolderDefinition.get_sc_products_folder_path(folder_flag, runset_id=runset_id)
            all_products_id = [os.path.join(sc_products_folder_path, f) for f in os.listdir(sc_products_folder_path)]
            return all_products_id
        else:
            return None

    # sc representation methods

    @staticmethod
    def get_sc_representations_folder_path(folder_flag, runset_id=None):
        return os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                            MetaFolderDefinition._sc_representations_foldername)

    @staticmethod
    def get_all_sc_representations_file_path(folder_flag, runset_id=None):
        repr_folder_path = MetaFolderDefinition.get_sc_representations_folder_path(folder_flag, runset_id=runset_id)
        all_reprs_file = [os.path.join(repr_folder_path, f) for f in os.listdir(repr_folder_path)]
        return all_reprs_file

    @staticmethod
    def get_all_sc_representation_ids(folder_flag, runset_id=None):
        sc_representations_folder_path = MetaFolderDefinition.get_sc_representations_folder_path(folder_flag,
                                                                                                 runset_id=runset_id)
        all_representations_id = [os.path.splitext(f)[0] for f in os.listdir(sc_representations_folder_path)]
        return all_representations_id

    # sc representation comparison methods

    @staticmethod
    def get_sc_represcomps_folder_path(folder_flag, runset_id=None):
        return os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                            MetaFolderDefinition._sc_represcomps_foldername)

    @staticmethod
    def get_all_sc_represcomp_ids(folder_flag, runset_id=None):
        """

        :param folder_flag:
        :param runset_id:
        :return:
        """
        sc_represcomps_folder_path = MetaFolderDefinition.get_sc_represcomps_folder_path(folder_flag,
                                                                                         runset_id=runset_id)
        all_represcomps_id = [os.path.splitext(f)[0] for f in os.listdir(sc_represcomps_folder_path)]
        return all_represcomps_id

    @staticmethod
    def get_sc_represcomp_file_name(folder_flag, represcomp_id, runset_id=None):
        """

        :param folder_flag:
        :param represcomp_id:
        :param runset_id:
        :return:
        """
        sc_represcomps_folder_path = MetaFolderDefinition.get_sc_represcomps_folder_path(folder_flag,
                                                                                         runset_id=runset_id)
        sc_represcomp_file_name = "{0}.json".format(represcomp_id)
        return os.path.join(sc_represcomps_folder_path, sc_represcomp_file_name)

    # sc evaluation methods

    @staticmethod
    def get_all_sc_evaluation_ids(folder_flag, runset_id=None):
        sc_evaluations_folder_path = MetaFolderDefinition.get_sc_evaluations_folder_path(folder_flag,
                                                                                         runset_id=runset_id)
        all_evaluations_id = [os.path.splitext(f)[0] for f in os.listdir(sc_evaluations_folder_path)]
        return all_evaluations_id

    @staticmethod
    def get_sc_evaluations_folder_path(folder_flag, runset_id=None):
        return os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                            MetaFolderDefinition._sc_evaluations)

    @staticmethod
    def get_all_sc_evaluations_file_path(folder_flag, runset_id=None):
        eval_dir_path = MetaFolderDefinition.get_sc_evaluations_folder_path(folder_flag, runset_id=runset_id)
        all_sc_eval_file = [os.path.join(eval_dir_path, f) for f in os.listdir(eval_dir_path)]
        return all_sc_eval_file

    # comparison matrix methods

    @staticmethod
    def get_comparison_matrix_file_path(folder_flag, runset_id=None):
        comparison_matrix_folder_path = os.path.join(MetaFolderDefinition.get_root_path(folder_flag,
                                                                                        runset_id=runset_id),
                                                     MetaFolderDefinition._cross_matrix_folder,
                                                     MetaFolderDefinition._comparison_matrix_filename)
        return comparison_matrix_folder_path

    # evaluation matrix methods

    @staticmethod
    def get_evaluation_matrix_file_path(folder_flag, runset_id=None):
        comparison_matrix_folder_path = os.path.join(MetaFolderDefinition.get_root_path(folder_flag,
                                                                                        runset_id=runset_id),
                                                     MetaFolderDefinition._cross_matrix_folder,
                                                     MetaFolderDefinition._evaluation_matrix_filename)
        return comparison_matrix_folder_path

    # forecast matrix methods

    @staticmethod
    def get_forecast_matrix_file_path(folder_flag, runset_id=None):
        forecast_matrix_folder_path = os.path.join(MetaFolderDefinition.get_root_path(folder_flag,
                                                                                      runset_id=runset_id),
                                                   MetaFolderDefinition._cross_matrix_folder,
                                                   MetaFolderDefinition._forecast_matrix_filename)
        return forecast_matrix_folder_path

    # menu methods

    @staticmethod
    def get_menu_file_path(folder_flag, runset_id=None):
        menu_file_path = os.path.join(MetaFolderDefinition.get_root_path(folder_flag, runset_id=runset_id),
                                      MetaFolderDefinition._menu_folder, MetaFolderDefinition._menu_filename)
        return menu_file_path

    def __init__(self):
        return
