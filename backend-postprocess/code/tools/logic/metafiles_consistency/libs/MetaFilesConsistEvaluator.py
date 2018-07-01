from MetaFolderDefinition import MetaFolderDefinition
import collections
import string
import json
import os


class MetaFilesConsistEvaluator:

    def __init__(self):
        return

    @staticmethod
    def convert_folder_flag(folder_flag_txt):
        """

        :param folder_flag_txt: String. Expects 'eff' for 'effective' or 'sbx' for 'sandbox'
        :return:
        """
        if folder_flag_txt == "eff":
            return MetaFolderDefinition.EFF_FLAG
        elif folder_flag_txt == "sbx":
            return MetaFolderDefinition.SBX_FLAG
        else:
            return None

    @staticmethod
    def evaluate_runset(file_path=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param folder_flag:
        :param debug_lvl:
        :return:
        """

        # define base folder
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare file
        if file_path is None:
            # if nothing is given, evaluate default menu file
            runset_file_path = MetaFolderDefinition.get_runset_file_path(folder_flag_int, runset_id=runset_id)
        else:
            runset_file_path = file_path

        return MetaFilesConsistEvaluator._evaluate_runset_file(runset_file_path, debug_lvl=debug_lvl)

    @staticmethod
    def evaluate_scmodel(file_path=None, scmodel_id=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param scmodel_id:
        :param folder_flag: String. Expects 'eff' (effective) or 'sbx' (sandbox). If None, assumes 'sbx'
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        if (file_path is not None) and (scmodel_id is not None):
            print("consist_meta_lib: excessive parameters given for 'evaluate_scmodel()'")  # TODO - use debug
            return False

        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare list of files
        if (file_path is None) and (scmodel_id is None):
            # if nothing is given, evaluate all sc_model files
            evaluated_file_paths = MetaFolderDefinition.get_all_sc_models_file_path(folder_flag_int,
                                                                                    runset_id=runset_id)
        elif (file_path is not None) and (scmodel_id is None):
            # if a file path is given, evaluate this file directly
            evaluated_file_paths = [file_path]
        elif (file_path is None) and (scmodel_id is not None):
            # if a parameter id is given, evaluate only such parameter file
            evaluated_file_paths = MetaFolderDefinition.get_sc_model_file_path(scmodel_id, folder_flag_int,
                                                                               runset_id=runset_id)
        else:
            # this case should never happen...
            print("consist_meta_lib: impossible scenario for 'evaluate_scmodel()'")  # TODO - use debug
            return False

        # evaluate all listed files
        return_boolean = True
        all_scproduct_ids = MetaFolderDefinition.get_all_sc_product_ids(folder_flag_int, runset_id=runset_id)
        all_screpresentation_ids = MetaFolderDefinition.get_all_sc_representation_ids(folder_flag_int,
                                                                                      runset_id=runset_id)
        for cur_scmodel_file_path in evaluated_file_paths:
            if not MetaFilesConsistEvaluator._evaluate_scmodel_file(cur_scmodel_file_path,
                                                                    sc_product_ids=all_scproduct_ids,
                                                                    sc_representation_ids=all_screpresentation_ids,
                                                                    debug_lvl=debug_lvl):
                return_boolean = False

        return return_boolean

    @staticmethod
    def evaluate_scmodelcombination(file_path=None, scmodelcomb_id=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param scmodelcomb_id:
        :param folder_flag: String. Expects 'eff' (effective) or 'sbx' (sandbox). If None, assumes 'sbx'
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if (file_path is not None) and (scmodelcomb_id is not None):
            print("consist_meta_lib: excessive parameters given for 'evaluate_scmodelcombination()'")  # TODO - debug
            return False

        # define folder flag
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare list of files
        if (file_path is None) and (scmodelcomb_id is None):
            # if nothing is given, evaluate all sc_model files
            evaluated_file_paths = MetaFolderDefinition.get_all_sc_modelcombinations_file_path(folder_flag_int,
                                                                                               runset_id=runset_id)
        elif (file_path is not None) and (scmodelcomb_id is None):
            # if a file path is given, evaluate this file directly
            evaluated_file_paths = [file_path]
        elif (file_path is None) and (scmodelcomb_id is not None):
            # if a parameter id is given, evaluate only such parameter file
            evaluated_file_paths = MetaFolderDefinition.get_sc_modelcombination_file_path(scmodelcomb_id,
                                                                                          folder_flag_int)
        else:
            # this case should never happen...
            print("consist_meta_lib: impossible scenario for 'evaluate_scmodelcombinations()'")  # TODO - debug
            return False

        if len(evaluated_file_paths) == 0:
            print("No files at '{0}'.".format(MetaFolderDefinition.get_sc_modelcombinations_folder_path(folder_flag_int,
                                                                                                        runset_id=runset_id)))
            return True

        # evaluate all listed files
        return_boolean = True
        all_scmodel_ids = MetaFolderDefinition.get_all_sc_model_ids(folder_flag_int, runset_id=runset_id)
        all_screprescomp_ids = MetaFolderDefinition.get_all_sc_represcomp_ids(folder_flag_int, runset_id=runset_id)
        all_screpres_ids = MetaFolderDefinition.get_all_sc_representation_ids(folder_flag_int, runset_id=runset_id)

        for cur_evaluated_file_path in evaluated_file_paths:
            if not MetaFilesConsistEvaluator._evaluate_scmodelcombination_file(cur_evaluated_file_path,
                                                                               sc_model_ids=all_scmodel_ids,
                                                                               sc_repres_ids=all_screpres_ids,
                                                                               sc_represcomp_ids=all_screprescomp_ids,
                                                                               runset_id=runset_id,
                                                                               folder_flag=folder_flag_int,
                                                                               debug_lvl=debug_lvl):
                return_boolean = False
        return return_boolean

    @staticmethod
    def evaluate_screference(folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param folder_flag:
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        return_boolean = True
        all_scproduct_ids = MetaFolderDefinition.get_all_sc_product_ids(folder_flag_int, runset_id=runset_id)
        all_screference_file_paths = MetaFolderDefinition.get_all_sc_references_file_path(folder_flag_int,
                                                                                          runset_id=runset_id)
        for cur_screference_filepath in all_screference_file_paths:
            if not MetaFilesConsistEvaluator._evaluate_screference_file(cur_screference_filepath,
                                                                        sc_products_id=all_scproduct_ids,
                                                                        debug_lvl=debug_lvl):
                return_boolean = False

        return return_boolean

    @staticmethod
    def evaluate_scproduct(folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param folder_flag:
        :param debug_lvl:
        :return:
        """

        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        return_boolean = True
        all_scproduct_file_paths = MetaFolderDefinition.get_all_sc_products_file_path(folder_flag_int,
                                                                                      runset_id=runset_id)
        for cur_scprod_filepath in all_scproduct_file_paths:
            if not MetaFilesConsistEvaluator._evaluate_scproduct_file(cur_scprod_filepath, debug_lvl=debug_lvl):
                return_boolean = False

        return return_boolean

    @staticmethod
    def evaluate_screpresentation(folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param folder_flag:
        :param debug_lvl:
        :return:
        """

        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        return_boolean = True
        all_scproduct_ids = MetaFolderDefinition.get_all_sc_product_ids(folder_flag_int, runset_id=runset_id)
        all_screpresentation_ids = MetaFolderDefinition.get_all_sc_representation_ids(folder_flag_int,
                                                                                      runset_id=runset_id)

        all_representation_file_paths = MetaFolderDefinition.get_all_sc_representations_file_path(folder_flag_int,
                                                                                                  runset_id=runset_id)
        for cur_screpresentation_filepath in all_representation_file_paths:
            if not MetaFilesConsistEvaluator._evaluate_screpresentation_file(cur_screpresentation_filepath,
                                                                             sc_products_id=all_scproduct_ids,
                                                                             sc_representations_id=all_screpresentation_ids,
                                                                             debug_lvl=debug_lvl):
                return_boolean = False

        return return_boolean

    @staticmethod
    def evaluate_scevaluation(file_path=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param folder_flag:
        :param debug_lvl:
        :return:
        """

        # define base folder
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare list of files
        if file_path is None:
            evaluated_file_paths = MetaFolderDefinition.get_all_sc_evaluations_file_path(folder_flag_int,
                                                                                         runset_id=runset_id)
        else:
            evaluated_file_paths = [file_path]

        # evaluate all listed files
        return_boolean = True
        for cur_scevaluation_file_path in evaluated_file_paths:
            if not MetaFilesConsistEvaluator._evaluate_scevaluation_file(cur_scevaluation_file_path, debug_lvl):
                return_boolean = False
        return return_boolean

    @staticmethod
    def evaluate_comparison_matrix(file_path=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param debug_lvl:
        :return:
        """

        # define base folder
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare file
        if file_path is None:
            # if nothing is given, evaluate default comparison file
            evaluated_file_path = MetaFolderDefinition.get_comparison_matrix_file_path(folder_flag_int,
                                                                                       runset_id=runset_id)
        else:
            evaluated_file_path = file_path

        all_scmodel_ids = MetaFolderDefinition.get_all_sc_model_ids(folder_flag_int, runset_id=runset_id)
        all_screpresentation_ids = MetaFolderDefinition.get_all_sc_representation_ids(folder_flag_int,
                                                                                      runset_id=runset_id)

        return MetaFilesConsistEvaluator._evaluate_comparison_matrix_file(evaluated_file_path,
                                                                          sc_models_id=all_scmodel_ids,
                                                                          sc_representations_id=all_screpresentation_ids,
                                                                          debug_lvl=debug_lvl)

    @staticmethod
    def evaluate_evaluation_matrix(file_path=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param folder_flag:
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        # define base folder
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare file
        if file_path is None:
            # if nothing is given, evaluate default evaluation file
            evaluated_file_path = MetaFolderDefinition.get_evaluation_matrix_file_path(folder_flag_int,
                                                                                       runset_id=runset_id)
        else:
            evaluated_file_path = file_path

        all_scmodel_ids = MetaFolderDefinition.get_all_sc_model_ids(folder_flag_int, runset_id=runset_id)
        all_reference_ids = MetaFolderDefinition.get_all_sc_reference_ids(folder_flag_int, runset_id=runset_id)
        all_evaluation_ids = MetaFolderDefinition.get_all_sc_evaluation_ids(folder_flag_int, runset_id=runset_id)

        return MetaFilesConsistEvaluator._evaluate_evaluation_matrix_file(evaluated_file_path,
                                                                          sc_models_id=all_scmodel_ids,
                                                                          sc_references_id=all_reference_ids,
                                                                          sc_evaluations_id=all_evaluation_ids,
                                                                          debug_lvl=debug_lvl)

    @staticmethod
    def evaluate_forecast_matrix(file_path=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param folder_flag:
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        # define base folder
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare file
        if file_path is None:
            # if nothing is given, evaluate default evaluation file
            evaluated_file_path = MetaFolderDefinition.get_forecast_matrix_file_path(folder_flag_int,
                                                                                     runset_id=runset_id)
        else:
            evaluated_file_path = file_path

        all_scmodel_ids = MetaFolderDefinition.get_all_sc_model_ids(folder_flag_int, runset_id=runset_id)
        return MetaFilesConsistEvaluator._evaluate_forecast_matrix_file(evaluated_file_path,
                                                                        sc_models_id=all_scmodel_ids,
                                                                        debug_lvl=debug_lvl)

    @staticmethod
    def evaluate_runset(file_path=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param folder_flag:
        :param runset_id:
        :param debug_lvl:
        :return:
        """

        # define base folder
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare file
        if file_path is None:
            # if nothing is given, evaluate default menu file
            runset_file_path = MetaFolderDefinition.get_runset_file_path(folder_flag_int, runset_id=runset_id)
        else:
            runset_file_path = file_path

        return MetaFilesConsistEvaluator._evaluate_runset_file(runset_file_path, debug_lvl=debug_lvl)

    @staticmethod
    def evaluate_menu(file_path=None, folder_flag=None, runset_id=None, debug_lvl=0):
        """

        :param file_path:
        :param folder_flag:
        :param debug_lvl:
        :return:
        """
        # define base folder
        folder_flag_int = MetaFilesConsistEvaluator.convert_folder_flag(folder_flag)
        folder_flag_int = MetaFolderDefinition.SBX_FLAG if folder_flag_int is None else folder_flag_int

        # prepare file
        if file_path is None:
            # if nothing is given, evaluate default menu file
            menu_file_path = MetaFolderDefinition.get_menu_file_path(folder_flag_int, runset_id=runset_id)
        else:
            menu_file_path = file_path

        all_representation_ids = MetaFolderDefinition.get_all_sc_representation_ids(folder_flag_int,
                                                                                    runset_id=runset_id)
        return MetaFilesConsistEvaluator._evaluate_menu_file(menu_file_path,
                                                             all_representation_id=all_representation_ids,
                                                             debug_lvl=debug_lvl)

    @staticmethod
    def _evaluate_parameter_file(file_path, debug_lvl=0):
        """

        :param file_path:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "sc_parameter"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            # print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            if 'id' not in root_object.keys():
                print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - use debug
                return_bol = False
            else:
                file_name = os.path.basename(file_path)
                if not file_name.startswith(root_object['id']):
                    print("consist_meta_lib: id parameter is not the filename '{0}'".format(file_path))  # TODO - use
                    return_bol = False

            if 'calendar_type' not in root_object.keys():
                print("consist_meta_lib: missing calendar_type parameter in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                if root_object['calendar_type'] not in ['daily', 'hourly', 'none']:
                    print("consist_meta_lib: calendar_type is not 'daily' or 'hourly' in '{0}'".format(file_path))  # TODO - debug
                    return_bol = False
                elif root_object['calendar_type'] == 'none':
                    return True   # if is not going to be displayed, only the id is enough

            if 'time_interval' not in root_object.keys():
                print("consist_meta_lib: missing time_interval parameter in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                try:
                    int(root_object['time_interval'])
                except ValueError:
                    print("consist_meta_lib: time_interval not integer in '{0}'".format(file_path))  # TODO - debug
                    return_bol = False

            if 'representation' not in root_object.keys():
                print("consist_meta_lib: missing representation parameter in '{0}'".format(file_path))  # TODO - ebug
                return_bol = False

        else:
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        return return_bol

    @staticmethod
    def _evaluate_scproduct_file(file_path, debug_lvl=0):
        """

        :param file_path:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "sc_product"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            if 'id' not in root_object.keys():
                print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - use debug
                return_bol = False
            else:
                file_name = os.path.basename(file_path)
                if not file_name.startswith(root_object['id']):
                    print("consist_meta_lib: id parameter is not the filename '{0}'".format(file_path))  # TODO - use
                    return_bol = False

            if 'time_series' not in root_object.keys():
                print("consist_meta_lib: missing time_series parameter in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                if root_object['time_series'] not in ['instant', 'forecast']:
                    print("consist_meta_lib: time_series is not 'instant' or 'forecast' in '{0}'".format(file_path))
                                                                                                        # TODO - debug
                    return_bol = False
                elif root_object['time_series'] == 'none':
                    return True   # if is not going to be displayed, only the id is enough

            if 'data_density' not in root_object.keys():
                print("consist_meta_lib: missing data_density parameter in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            elif root_object['data_density'] not in ['dense', 'sparse']:
                print("consist_meta_lib: data_density is not 'dense' or 'sparse' in '{0}'".format(file_path))
                                                                                                        # TODO - debug
                return_bol = False

        else:
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        return return_bol

    @staticmethod
    def _evaluate_screference_file(file_path, sc_products_id=None, debug_lvl=0):
        """

        :param cur_screference_filepath:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "sc_reference"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            if 'id' not in root_object.keys():
                print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - use debug
                return_bol = False
            else:
                file_name = os.path.basename(file_path)
                if not file_name.startswith(root_object['id']):
                    print("consist_meta_lib: id parameter is not the filename '{0}'".format(file_path))  # TODO - use
                    return_bol = False

            if 'title' not in root_object.keys():
                print("consist_meta_lib: missing title parameter in '{0}'".format(file_path))  # TODO - debug
                return_bol = False

            if 'sc_product_set' not in root_object.keys():
                print("consist_meta_lib: missing sc_product_set parameter in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                product_set = root_object['sc_product_set']
                if isinstance(product_set, list):
                    for cur_prod_id in product_set:
                        if isinstance(cur_prod_id, str) or isinstance(cur_prod_id, unicode):
                            if sc_products_id is not None:
                                if cur_prod_id not in sc_products_id:
                                    print("consist_meta_lib: invalid sc_product_id '{0}', element '{1}' in '{2}'".format(
                                            cur_prod_id, sc_products_id, file_path))
                                    return_bol = False
                        else:
                            print("consist_meta_lib: invalid sc_product_set_representation element '{0}' ({1}) in '{2}'".format(
                                cur_prod_id, type(cur_prod_id), file_path))
                            return_bol = False
                                                                                                        # TODO - debug
                else:
                    print("consist_meta_lib: sc_product_set_representation is not a list in '{0}'".format(file_path))
                                                                                                        # TODO - debug
                    return_bol = False

        else:
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        return return_bol

    @staticmethod
    def _evaluate_asynchmodel_file(file_path, debug_lvl=0):
        """

        :param file_path:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "asynch_model"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            # print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                file_data = json.load(file_data)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            if 'id' not in root_object.keys():
                print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - use debug
                return_bol = False
            else:
                file_name = os.path.basename(file_path)
                if not file_name.startswith(str(root_object['id'])):
                    print("consist_meta_lib: id parameter is not the filename '{0}'".format(file_path))  # TODO - debug
                    return_bol = False

            if 'parameter_set' not in root_object.keys():
                print("consist_meta_lib: missing parameter_set parameter in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                parameter_set = root_object['parameter_set']
                if len(parameter_set) == 0:
                    print("consist_meta_lib: parameter_set without elements in '{0}'".format(file_path))  # TODO - debug
                    return_bol = False

        else:
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        return return_bol

    @staticmethod
    def _evaluate_scmodel_file(file_path, sc_product_ids=None, sc_representation_ids=None, debug_lvl=0):
        """

        :param file_path:
        :param sc_product_ids: List of ids of sc_products for better consistency check. If None, does not check it.
        :param sc_representation_ids: List of ids of sc_representations for better consistency check. If None, does not check it.
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "sc_model"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag not in file_data.keys():
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        return_bol = True
        root_object = file_data[_root_object_tag]

        if 'id' not in root_object.keys():
            print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - use debug
            return_bol = False
        else:
            file_name = os.path.basename(file_path)
            if not file_name.startswith(str(root_object['id'])):
                print("consist_meta_lib: id parameter is not the filename '{0}'".format(file_path))  # TODO - debug
                return_bol = False

        if 'title' not in root_object.keys():
            print("consist_meta_lib: missing title parameter in '{0}'".format(file_path))  # TODO - debug
            return_bol = False

        if 'description' not in root_object.keys():
            print("consist_meta_lib: missing description parameter in '{0}'".format(file_path))  # TODO - debug
            return_bol = False

        if 'sc_product_set' not in root_object.keys():
            print("consist_meta_lib: missing sc_product_set parameter in '{0}'".format(file_path))  # TODO - debug
            return_bol = False
        else:
            product_set = root_object['sc_product_set']
            if isinstance(product_set, list):
                if sc_product_ids is not None:
                    for cur_product_id in product_set:
                        if cur_product_id not in sc_product_ids:
                            print("consist_meta_lib: undefined product_id '{0}' in '{1}'.".format(cur_product_id,
                                                                                                  file_path))
                            return_bol = False
            else:
                print("consist_meta_lib: unexpected product_set format({0}) in '{1}'".format(type(product_set),
                                                                                             file_path))  # TODO - debug
                return_bol = False

        if 'sc_representation_set' in root_object.keys():
            representation_set = root_object['sc_representation_set']
            if isinstance(representation_set, list):
                return_bol = return_bol
                if sc_representation_ids is not None:
                    for cur_representation_id in representation_set:
                        if cur_representation_id not in sc_representation_ids:
                            print("consist_meta_lib: undefined representation_id '{0}' in '{1}'.".format(cur_representation_id,
                                                                                                         file_path))
                            return_bol = False
            else:
                print("consist_meta_lib: unexpected representation_set format({0}) in '{1}'".format(type(representation_set),
                                                                                                    file_path))
                                                                                                    # TODO - debug
                return_bol = False

        return return_bol

    @staticmethod
    def _evaluate_scmodelcombination_file(file_path, sc_model_ids=None, sc_repres_ids=None, sc_represcomp_ids=None,
                                          runset_id=None, folder_flag=None, debug_lvl=0):
        """

        :param file_path:
        :param sc_model_ids:
        :param sc_repres_ids:
        :param sc_represcomp_ids:
        :param runset_id:
        :param folder_flag:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "sc_modelcombination"

        # basic checks
        if file_path is None:
            print("consist_meta_lib: Missing file path to evaluate.")
            return False
        elif not os.path.exists(file_path):
            print("consist_meta_lib: File {0} does not exist.".format(file_path))
            return False

        return_bol = True

        print("consist_meta_lib: Evaluating '{0}'.".format(file_path))

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag not in file_data.keys():
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - debug
            return False

        return_bol = True
        root_object = file_data[_root_object_tag]

        # check ID field
        if 'id' not in root_object.keys():
            print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - debug
            return_bol = False
        else:
            file_name = os.path.basename(file_path).split('.')[0]
            # if not file_name.startswith(str(root_object['id'])):
            if not file_name.strip() == str(root_object['id']).strip():
                print("consist_meta_lib: id parameter is not the filename '{0}'".format(file_path))  # TODO - debug
                print("                      '{0}' != '{1}'".format(file_name, str(root_object['id'])))  # TODO - debug
                return_bol = False

        # check title
        if 'title' not in root_object.keys():
            print("consist_meta_lib: missing title parameter in '{0}'".format(file_path))  # TODO - debug
            return_bol = False

        # check if at least one of 'sc_represcomb_set' or 'sc_repres_set' exist
        if ('sc_represcomb_set' not in root_object.keys()) and ('sc_repres_set' not in root_object.keys()):
            print("consist_meta_lib: missing one of 'sc_represcomb_set' or 'sc_repres_set' parameter in '{0}'".format(file_path))
            return_bol = False

        # manage 'sc_repres_set'
        if 'sc_repres_set' in root_object.keys():
            represents = root_object['sc_repres_set']

            # test 'modelpast'
            if 'modelpast' not in represents.keys():
                print("consist_meta_lib: missing 'modelpast' in 'sc_repres_set' for '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                if represents['modelpast'] not in sc_model_ids:
                    print("consist_meta_lib: invalid model '{0}' in 'modelpast' for '{1}'".format(represents['modelpast'], file_path))  # TODO - debug
                    return_bol = False

            # test 'modelfore'
            if 'modelfore' not in represents.keys():
                print("consist_meta_lib: missing 'modelfore' in 'sc_repres_set' for '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                if represents['modelfore'] not in sc_model_ids:
                    print("consist_meta_lib: invalid model '{0}' in 'modelfore' for '{1}'".format(represents['modelfore'], file_path))  # TODO - debug
                    return_bol = False

            # test 'sc_repr'
            if 'sc_repr' not in represents.keys():
                print("consist_meta_lib: missing 'sc_repr' in 'sc_repres_set' for '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                for cur_repr in represents['sc_repr']:
                    if cur_repr not in sc_repres_ids:
                        print("consist_meta_lib: invalid representation '{0}' in 'sc_repr' for '{1}'".format(represents['sc_repr'], file_path))  # TODO - debug
                        return_bol = False

        # manage 'sc_represcomb_set'
        if 'sc_represcomb_set' in root_object.keys():
            reprs_comb = root_object['sc_represcomb_set']
            if len(reprs_comb) == 0:
                print("consist_meta_lib: empty representation combination set for '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                for cur_represcomb_id in reprs_comb.keys():

                    requeriments_dict = {}

                    # check if combined representation exist and loads its frames
                    if cur_represcomb_id not in sc_represcomp_ids:
                        print("consist_meta_lib: representation combination {0} not in '{1}'".format(cur_represcomb_id,
                                                                                                     sc_represcomp_ids))
                        print("consist_meta_lib:    '{0}'".format(file_path))
                        return_bol = False
                        continue

                    cur_represcomb_file_path = MetaFolderDefinition.get_sc_represcomp_file_name(folder_flag,
                                                                                                cur_represcomb_id,
                                                                                                runset_id=runset_id)
                    cur_model_frames = MetaFilesConsistEvaluator._get_models_frame_of_represcomb(cur_represcomb_file_path,
                                                                                                 debug_lvl=debug_lvl)
                    if cur_model_frames is None:
                        return_bol = False
                        continue

                    cur_represcomb = reprs_comb[cur_represcomb_id]

                    # check if there is any combined representation
                    if len(cur_represcomb.keys()) == 0:
                        print("consist_meta_lib: representation combination {0} is empty in '{1}'".format(cur_represcomb_id,
                                                                                                          file_path))  # TODO - debug
                        return_bol = False
                        continue

                    # check if all models exist can receive given frame
                    cur_reprcomb_model_ids = cur_represcomb.keys()
                    for cur_model_id in cur_reprcomb_model_ids:

                        # check if model exists
                        if cur_model_id not in sc_model_ids:
                            print("consist_meta_lib: model '{0}' does not exist ('{1}').".format(cur_model_id,
                                                                                                 file_path))
                            return_bol = False

                        cur_model_frame = cur_represcomb[cur_model_id]

                        # check if model frame exists
                        if cur_model_frame not in cur_model_frames.keys():
                            print("consist_meta_lib: model frame '{0}' not found for '{1}'.".format(cur_model_frame,
                                                                                                    cur_represcomb_id))
                            return_bol = False
                            continue

                        # get model products
                        cur_model_file_path = MetaFolderDefinition.get_sc_model_file_path(cur_model_id, folder_flag,
                                                                                          runset_id=runset_id)
                        cur_model_products = MetaFilesConsistEvaluator._get_products_of_model(cur_model_file_path,
                                                                                              debug_lvl=debug_lvl)
                        if cur_model_products is None:
                            return_bol = False
                            continue

                        # check if given frame fits the model
                        for cur_frame_prod in cur_model_frames[cur_model_frame]["sc_product_set"]:
                            if cur_frame_prod not in cur_model_products:
                                print("consist_meta_lib: product frame '{0}' not found in model '{1}'.".format(
                                    cur_frame_prod, cur_model_id))
                                return_bol = False
                                continue
                            else:
                                print("consist_meta_lib: product frame '{0}' in model '{1}'.".format(cur_frame_prod,
                                                                                                     cur_model_id))

                        # register
                        if cur_model_frame not in requeriments_dict.keys():
                            requeriments_dict[cur_model_frame] = 0
                        requeriments_dict[cur_model_frame] += 1

                        print("Model {0} is ok in frame {1}.".format(cur_model_id, cur_model_frame))

                    # check if all frames were set up
                    for cur_model_frame_id in cur_model_frames.keys():
                        cur_model_frame_obj = cur_model_frames[cur_model_frame_id]

                        missing_fields = False

                        # basic check of fields
                        if "mandatory" not in cur_model_frame_obj.keys():
                            print("consist_meta_lib: frame {0} of {1} has no 'mandatory' field.".format(cur_model_frame_id,
                                                                                                        cur_represcomb_id))
                            return_bol = False
                            continue
                        if "cardinality" not in cur_model_frame_obj.keys():
                            print("consist_meta_lib: frame {0} of {1} has no 'cardinality' field.".format(cur_model_frame_id,
                                                                                                        cur_represcomb_id))
                            return_bol = False
                            continue

                        # basic check
                        if missing_fields:
                            continue

                        # check if the requierements are filled
                        if (cur_model_frame_obj["mandatory"] == "yes") and \
                                (cur_model_frame_id not in requeriments_dict.keys()):
                            print("consist_meta_lib: mandatory frame '{0}' of '{1}' not filled.".format(
                                cur_model_frame_id, cur_represcomb_id))
                            return_bol = False
                        elif cur_model_frame_obj["cardinality"] == "single":
                            if (cur_model_frame_id in requeriments_dict.keys()) and \
                                    (requeriments_dict[cur_model_frame_id] > 1):
                                print("consist_meta_lib: single frame '{0}' has {1} models set.".format(
                                    cur_model_frame_id, requeriments_dict[cur_model_frame_id]))
                                return_bol = False

        if return_bol:
            print("consist_meta_lib: File '{0}' is OK.".format(file_path))

        return return_bol

    @staticmethod
    def _get_models_frame_of_represcomb(represcomb_file_path, debug_lvl=0):
        """

        :param represcomb_file_path:
        :return:
        """

        root_tag = "sc_represcomb"
        frames_tag = "requirements"

        with open(represcomb_file_path, "r+") as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(represcomb_file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(represcomb_file_path))  # TODO - use debug
                return None

        if root_tag not in file_data.keys():
            print("consist_meta_lib: missing root tag '{0}' in '{1}'.".format(root_tag, represcomb_file_path))  # TODO - use debug
            return None

        root_obj = file_data[root_tag]

        if frames_tag not in root_obj.keys():
            print("consist_meta_lib: missing '{0}' tag in '{1}'.".format(frames_tag, represcomb_file_path))  # TODO - use debug
            return None

        return root_obj[frames_tag]

    @staticmethod
    def _get_products_of_model(sc_model_file_path, debug_lvl=0):
        """

        :param sc_model_file_path:
        :param debug_lvl:
        :return:
        """
        root_tag = "sc_model"
        prod_set_tag = "sc_product_set"

        if not os.path.exists(sc_model_file_path):
            print("consist_meta_lib: File not found: {0}".format(sc_model_file_path))  # TODO - use debug
            return None

        with open(sc_model_file_path, "r+") as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(sc_model_file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(sc_model_file_path))  # TODO - use debug
                return None

        return file_data[root_tag][prod_set_tag]

    @staticmethod
    def _evaluate_screpresentation_file(file_path, sc_products_id=None, sc_representations_id=None, debug_lvl=0):
        """

        :param cur_screpresentation_filepath:
        :param sc_products_id:
        :param sc_representations_id:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "sc_representation"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        return_bol = True
        root_object = file_data[_root_object_tag]

        if 'id' not in root_object.keys():
            print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - use debug
            return_bol = False
        else:
            file_name = os.path.basename(file_path)
            if not file_name.startswith(str(root_object['id'])):
                print("consist_meta_lib: id parameter is not the filename '{0}'".format(file_path))  # TODO - debug
                return_bol = False

        if 'calendar_type' not in root_object.keys():
            print("consist_meta_lib: missing calendar_type parameter in '{0}'".format(file_path))  # TODO - debug
            return_bol = False
        elif root_object['calendar_type'] not in ['daily', 'hourly']:
            print("consist_meta_lib: calendar_type is not 'daily' or 'hourly' in '{0}'".format(file_path))
                                                                                                        # TODO - debug
            return_bol = False

        if 'time_interval' not in root_object.keys():
            print("consist_meta_lib: missing time_interval parameter in '{0}'".format(file_path))  # TODO - debug
            return_bol = False
        elif not isinstance(root_object['time_interval'], int):
            print("consist_meta_lib: time_interval is not integer (is {0}) in '{1}'".format(type(root_object['calendar_type']),
                                                                                            file_path))  # TODO - debug
            return_bol = False

        if 'representation' not in root_object.keys():
            print("consist_meta_lib: missing representation in '{0}'".format(file_path))  # TODO - debug
            return_bol = False

        if 'repgen_script' not in root_object.keys():
            print("consist_meta_lib: missing repgen_script in '{0}'".format(file_path))  # TODO - debug
            return_bol = False

        if ('sc_product_set' not in root_object.keys()) and ('sc_representation_set' not in root_object.keys()):
            print("consist_meta_lib: missing sc_product_set OR sc_representation_set in '{0}'".format(file_path))
                                                                                                        # TODO - debug
            return_bol = False
        elif ('sc_product_set' in root_object.keys()) and ('sc_representation_set' in root_object.keys()):
            print("consist_meta_lib: both sc_product_set AND sc_representation_set present in '{0}'".format(file_path))
                                                                                                        # TODO - debug
            return_bol = False
        else:

            try:
                prod_set = root_object['sc_product_set']
                if sc_products_id is not None:
                    for cur_prod_id in prod_set:
                        if (isinstance(cur_prod_id, str)) and (cur_prod_id not in sc_products_id):
                            print("consist_meta_lib: failed '{0}'.".format(file_path))
                            print("                    missing mandatory sc_product '{0}'.".format(cur_prod_id))
                            return_bol = False
                        elif isinstance(cur_prod_id, collections.Iterable):
                            cur_prod_ids = cur_prod_id
                            accept_list = True
                            for cur_prod_id in cur_prod_ids:
                                if (isinstance(cur_prod_id, str)) and (cur_prod_id not in sc_products_id):
                                    print("consist_meta_lib: failed '{0}'.".format(file_path))
                                    print("                    missing mandatory sc_product '{0}'.".format(cur_prod_id))
                                    return_bol = False
                                    accept_list = False

                            if accept_list:
                                break
            except KeyError:
                return_bol = return_bol

            try:
                prod_set = root_object['sc_representation_set']
                if sc_representations_id is not None:
                    for cur_repr_id in prod_set:
                        if cur_repr_id not in sc_representations_id:
                            return_bol = False
            except KeyError:
                return_bol = return_bol

        return return_bol

    @staticmethod
    def _evaluate_comparison_matrix_file(file_path, sc_models_id=None, sc_representations_id=None, debug_lvl=0):
        """

        :param file_path:
        :param sc_models_id:
        :param sc_representations_id:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "comparison_matrix"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            for cur_comparison in root_object.keys():

                # evaluates the key itself
                if '_' not in cur_comparison:
                    print("consist_meta_lib: comparison id {0} seems to fail in '{1}'".format(cur_comparison,
                                                                                              file_path))
                                                                                                # TODO - use debug
                    return_bol = False
                else:
                    splited_comparison_id = cur_comparison.split("_")
                    if len(splited_comparison_id) > 2:
                        print("consist_meta_lib: comparison '{0}' has more than one '_' in '{1}'".format(cur_comparison,
                                                                                                         file_path))
                                                                                                     # TODO - use debug
                        return_bol = False
                    elif sc_models_id is not None:
                        for cur_model_id in splited_comparison_id:
                            if cur_model_id not in sc_models_id:
                                print("consist_meta_lib: undefined model id '{0}' in '{1}', '{2}'.".format(
                                    cur_model_id, cur_comparison, file_path))
                                return_bol = False
                        if return_bol:
                            print("consist_meta_lib: accepted all models of {0} in '{1}'.".format(cur_comparison,
                                                                                                  file_path))

                # evaluates the representations
                if not isinstance(root_object[cur_comparison], list):
                    print("consist_meta_lib: comparison id {0} seems to not hold a list in '{1}'".format(cur_comparison,
                                                                                                         file_path))
                                                                                                      # TODO - use debug
                    return_bol = False
                elif sc_representations_id is not None:
                    for cur_repr in root_object[cur_comparison]:
                        if cur_repr not in sc_representations_id:
                            print("consist_meta_lib: representation '{0}' not defined in '{1}', in '{2}'".format(
                                cur_repr, cur_comparison, file_path))  # TODO - use debug
                            return_bol = False
                    if return_bol:
                        print("consist_meta_lib: accepted all representations of {0} in '{1}'.".format(cur_comparison,
                                                                                                       file_path))

        else:
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        return return_bol

    @staticmethod
    def _evaluate_evaluation_matrix_file(file_path, sc_models_id=None, sc_references_id=None, sc_evaluations_id=None,
                                         debug_lvl=0):
        """

        :param file_path:
        :param sc_models_id:
        :param sc_references_id:
        :param sc_evaluations_id:
        :param debug_lvl:
        :return:
        """

        _root_object_tag = "evaluation_matrix"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            for cur_evaluation in root_object.keys():

                # evaluates the key itself
                if '_' not in cur_evaluation:
                    print("consist_meta_lib: evaluation id {0} seems to fail in '{1}'".format(cur_evaluation,
                                                                                              file_path))
                                                                                                # TODO - use debug
                    return_bol = False
                else:
                    splited_evaluation_id = cur_evaluation.split("_")
                    if len(splited_evaluation_id) > 2:
                        print("consist_meta_lib: evaluation '{0}' has more than one '_' in '{1}'".format(cur_evaluation,
                                                                                                         file_path))
                                                                                                     # TODO - use debug
                        return_bol = False
                    else:
                        # check evaluation id
                        if (sc_evaluations_id is not None) and (splited_evaluation_id[0] not in sc_evaluations_id):
                            print("consist_meta_lib: undefined evaluation id '{0}' in '{1}', '{2}'.".format(
                                    splited_evaluation_id[0], cur_evaluation, file_path))
                            return_bol = False

                        # check reference id
                        if (sc_references_id is not None) and (splited_evaluation_id[1] not in sc_references_id):
                            print("consist_meta_lib: undefined reference id '{0}' in '{1}', '{2}'.".format(
                                    splited_evaluation_id[0], cur_evaluation, file_path))
                            return_bol = False

                        # check each model
                        if sc_models_id is not None:
                            for cur_model_id in root_object[cur_evaluation]:
                                if cur_model_id not in sc_models_id:
                                    print("consist_meta_lib: undefined model id '{0}' in '{1}', '{2}'.".format(
                                        cur_model_id, cur_evaluation, file_path))
                                    return_bol = False

                # evaluates the representations
                if not isinstance(root_object[cur_evaluation], list):
                    print("consist_meta_lib: evaluation id {0} seems to not hold a list in '{1}'".format(cur_evaluation,
                                                                                                         file_path))
                                                                                                      # TODO - use debug
                    return_bol = False

        else:
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        return return_bol

    @staticmethod
    def _evaluate_forecast_matrix_file(file_path, sc_models_id=None, debug_lvl=0):
        """

        :param file_path:
        :param sc_models_id:
        :param debug_lvl:
        :return:
        """
        _root_object_tag = "forecast_matrix"

        # basic check
        if file_path is None:
            return False

        # this is not a mandatory file
        if not os.path.exists(file_path):
            return True

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate root element
        if _root_object_tag not in file_data.keys():
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return False

        # evaluate each parameter and tag
        return_bol = True
        root_object = file_data[_root_object_tag]
        for cur_base_model_id in root_object.keys():
            if cur_base_model_id not in sc_models_id:
                return_bol = False
                print("Base model id '{0}' not found as sc-model id.".format(cur_base_model_id))
                continue
            if "scenarios" not in root_object[cur_base_model_id].keys():
                return_bol = False
                print("Base model id '{0}' does not have 'scenarios' key.".format(cur_base_model_id))
                continue
            for cur_fore_model_id, cur_fore_model_obj in root_object[cur_base_model_id]["scenarios"].items():
                if cur_fore_model_id not in sc_models_id:
                    return_bol = False
                    print("Forecast model id '{0}' not found as sc-model id.".format(cur_fore_model_id))

        return return_bol

    @staticmethod
    def _evaluate_scevaluation_file(file_path, debug_lvl=0):

        _root_object_tag = "sc_evaluation"

        # basic check
        if file_path is None:
            return False

        # read file content
        with open(file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            if 'id' not in root_object.keys():
                print("consist_meta_lib: missing id parameter in '{0}'".format(file_path))  # TODO - use debug
                return_bol = False
            else:
                file_name = os.path.basename(file_path)
                if not file_name.startswith(str(root_object['id'])):
                    print("consist_meta_lib: id parameter is not the filename '{0}'".format(
                        file_path))  # TODO - debug
                    return_bol = False

            if 'sc_reference_products_id' not in root_object.keys():
                print("consist_meta_lib: missing 'sc_reference_products_id' in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                products_req = root_object['sc_reference_products_id']
                if isinstance(products_req, list):
                    return_bol = return_bol
                    # TODO - check if every product exist (see sc_model)
                else:
                    print("consist_meta_lib: unexpected sc_reference_products_id format({0}) in '{1}'".format(type(products_req),
                                                                                                   file_path))
                    return_bol = False

            if 'sc_model_products_id' not in root_object.keys():
                print("consist_meta_lib: missing 'sc_model_products_id' in '{0}'".format(file_path))  # TODO - debug
                return_bol = False
            else:
                products_req = root_object['sc_model_products_id']
                if isinstance(products_req, list):
                    return_bol = return_bol
                    # TODO - check if every product exist (see sc_model)
                else:
                    print("consist_meta_lib: unexpected sc_reference_products_id format({0}) in '{1}'".format(type(products_req),
                                                                                                   file_path))
                    return_bol = False

        else:
            print("Root object is not '{0}'.".format(_root_object_tag))  # TODO - use debug
            return_bol = False

        return return_bol

    @staticmethod
    def _evaluate_runset_file(runset_file_path, debug_lvl=0):

        _root_object_tag = "sc_runset"
        _filename = "Runset.json"

        return_bol = True

        # basic check
        if runset_file_path is None:
            return False
        elif not os.path.exists(runset_file_path):
            print("consist_meta_lib: File does not exit: '{0}'.".format(runset_file_path))
            return False

        # check filename
        file_name = os.path.basename(runset_file_path)
        if not (file_name == _filename):
            print("consist_meta_lib: Filename not '{0}' in '{1}'".format(_filename, file_path))
            return_bol = False

        # read file content
        with open(runset_file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(runset_file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(runset_file_path))  # TODO - use debug
                return False

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            root_object = file_data[_root_object_tag]

            if 'id' not in root_object.keys():
                print("consist_meta_lib: missing 'id' parameter in '{0}'".format(runset_file_path))  # TODO - debug
                return_bol = False
            else:
                # TODO - perform some way to evaluate id consistency
                return_bol = return_bol

            if 'title' not in root_object.keys():
                print("consist_meta_lib: missing 'title' parameter in '{0}'".format(runset_file_path))  # TODO - debug
                return_bol = False
            elif len(root_object['title']) > 28:
                print("consist_meta_lib: 'title' is longer than 28 characters '{0}'".format(root_object['title']))
                return_bol = False

        return return_bol

    @staticmethod
    def _evaluate_menu_file(menu_file_path, all_representation_id=None, debug_lvl=0):

        _root_object_tag = "web_menu"

        return_bol = True

        # basic check
        if menu_file_path is None:
            return False

        # check filename
        file_name = os.path.basename(menu_file_path)
        if not (file_name == "Menu.json"):
            print("consist_meta_lib: Filename not 'Menu.json' in '{0}'".format(file_path))
            return_bol = False

        # read file content
        with open(menu_file_path, 'r') as file_data:
            print("consist_meta_lib: parsing json file '{0}'".format(menu_file_path))  # TODO - use debug
            try:
                printable = set(string.printable)
                raw_file_content = file_data.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                file_data = json.loads(file_content)
            except ValueError:
                print("consist_meta_lib: not even a JSON structure in '{0}'".format(menu_file_path))  # TODO - use debug
                return False

        all_ids = []

        # evaluate each parameter and tag
        if _root_object_tag in file_data.keys():
            return_bol = True
            root_object = file_data[_root_object_tag]

            if 'single_model' not in root_object.keys():
                print("consist_meta_lib: missing 'single_model' parameter in '{0}'".format(menu_file_path))  # TODO - debug
                return_bol = False
            elif not isinstance(root_object['single_model'], list):
                print("consist_meta_lib: missing 'single_model' parameter not list in '{0}'".format(menu_file_path))  # debug
                return_bol = False
            else:
                tmp_ret = MetaFilesConsistEvaluator._evaluate_menu_representation_set(root_object['single_model'],
                                                                                      menu_file_path, 'single_model',
                                                                                      all_ids, debug_lvl=debug_lvl)
                return_bol = return_bol if tmp_ret else False

            if 'comparison_model' not in root_object.keys():
                print("consist_meta_lib: missing 'comparison_model' parameter in '{0}'".format(menu_file_path))  # TODO - debug
                return_bol = False
            elif not isinstance(root_object['comparison_model'], list):
                print("consist_meta_lib: missing 'comparison_model' parameter not list in '{0}'".format(menu_file_path))  # debug
                return_bol = False
            else:
                tmp_ret = MetaFilesConsistEvaluator._evaluate_menu_representation_set(root_object['comparison_model'],
                                                                                      menu_file_path, 'comparison_model',
                                                                                      all_ids, debug_lvl=debug_lvl)
                return_bol = return_bol if tmp_ret else False

            if 'evaluation' not in root_object.keys():
                print("consist_meta_lib: missing 'evaluation' parameter in '{0}'".format(menu_file_path))  # TODO - debug
                return_bol = False
            elif not isinstance(root_object['evaluation'], list):
                print("consist_meta_lib: missing 'evaluation' parameter not list in '{0}'".format(menu_file_path))  # debug
                return_bol = False
            else:
                for cur_eval in root_object['evaluation']:
                    if 'id' not in cur_eval.keys():
                        print("consist_meta_lib: It is missing 'id' for an '{0}' in '{1}'.".format(menu_type, file_path))
                        return_bol = False
                        continue
                    all_ids.append(cur_eval["id"])
                    if 'call_select' in cur_eval.keys():
                        if 'evaluations' not in cur_eval.keys():
                            print("consist_meta_lib: missing 'evaluations' in evaluation '{0}' of '{1}'".format(
                                cur_eval['id'],
                                menu_file_path))  # TODO - debug
                            return_bol = False
                    elif 'call_radio' in cur_eval.keys():
                        if 'evaluation' not in cur_eval.keys():
                            print("consist_meta_lib: missing 'evaluation' in evaluation '{0}' of '{1}'".format(
                                cur_eval['id'],
                                menu_file_path))  # TODO - debug
                            return_bol = False
        else:
            print("consist_meta_lib: Root object is not '{0}' in '{1}'.".format(_root_object_tag, menu_file_path))  # TODO - use debug
            return_bol = False

        repeated_ids = [str(item) for item, count in collections.Counter(all_ids).items() if count > 1]
        if len(repeated_ids) > 0:
            print("consist_meta_lib: Repeated ids found: '{0}'.".format(repeated_ids))  # TODO - use debug
            return_bol = False

        return return_bol

    @staticmethod
    def _evaluate_menu_representation_set(repr_set_object, file_path, menu_type, all_ids, debug_lvl=0):
        return_bol = True
        for cur_model in repr_set_object:
            if 'id' not in cur_model.keys():
                print("consist_meta_lib: It is missing 'id' for an '{0}' in '{1}'.".format(menu_type, file_path))
                return False

            all_ids.append(cur_model["id"])

            if 'call_select' in cur_model.keys():
                if 'representations' not in cur_model.keys():
                    print("consist_meta_lib: missing 'representations' parameter in '{0}'.'{1}'.'{2}'".format(
                          file_path, 'single_model', cur_model['id']))  # debug
                    return_bol = False
                elif not isinstance(cur_model['representations'], list):
                    print("consist_meta_lib: 'representations' parameter not list in '{0}'.'{1}'.'{2}'".format(
                          file_path, 'single_model', cur_model['id']))  # debug
                    return_bol = False
            elif 'call_radio' in cur_single_model.keys():
                if 'representation' not in cur_model.keys():
                    print("consist_meta_lib: missing 'representation' parameter in '{0}'.'{1}'.'{2}'".format(
                        file_path, 'single_model', cur_model['id']))  # debug
                    return_bol = False
                elif not isinstance(cur_model['representation'], unicode):
                    print("consist_meta_lib: 'representation' parameter not text in '{0}'.'{1}'.'{2}'".format(
                          file_path, 'single_model', cur_model['id']))  # debug
                    return_bol = False
        return return_bol
