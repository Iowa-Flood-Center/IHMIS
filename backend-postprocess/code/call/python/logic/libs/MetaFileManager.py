from Debug import Debug
import os

from FolderDefinition import FolderDefinition
from FileDefinition import FileDefinition
from metafiles.MetaScRepresentationComp import MetaScRepresentationComp
from metafiles.MetaScRepresentation import MetaScRepresentation
from metafiles.MetaEvaluationMatrix import MetaEvaluationMatrix
from metafiles.MetaComparisonSet import MetaComparisonSet
from metafiles.MetaScEvaluation import MetaScEvaluation
from metafiles.MetaScReference import MetaScReference
from metafiles.MetaScModelComb import MetaScModelComb
from metafiles.MetaScModel import MetaScModel
from metafiles.MetaRunset import MetaRunset


class MetaFileManager:

    _runsetid = None
    _folder_flag = None
    _scrunset_meta_info = None
    _scmodel_meta_infos = None
    _scmodelcomb_meta_infos = None
    _screference_meta_infos = None
    _scproduct_meta_infos = None
    _screpresentation_meta_infos = None
    _screpresentationcomp_meta_infos = None
    _scevaluation_meta_infos = None
    _comparison_matrix = None
    _evaluation_matrix = None

    # _asynchmodel_meta_infos = None
    # _scparameter_meta_infos = None

    def __init__(self, runset_id=None, folder_flag=None):
        self._runsetid = runset_id
        self._folder_flag = folder_flag

    # sc_runset methods

    def load_scrunset_meta_info(self, debug_lvl=0):
        """

        :param ignore_fails:
        :param debug_lvl:
        :return:
        """

        file_path = FileDefinition.obtain_runset_file_path(runset_id=self._runsetid, folder_flag=self._folder_flag)

        self._scrunset_meta_info = MetaRunset(file_path, debug_lvl=debug_lvl)

    def get_runset_timestamp_ini(self):
        """

        :return:
        """

        if self._scrunset_meta_info is not None:
            return self._scrunset_meta_info.get_timestamp_ini()
        else:
            return None

    def get_runset_timestamp_end(self):
        """

        :return:
        """

        if self._scrunset_meta_info is not None:
            return self._scrunset_meta_info.get_timestamp_end()
        else:
            # TODO - error message
            return None

    # sc_model methods

    def load_all_scmodel_meta_info(self, ignore_fails=False, debug_lvl=0):
        """
        Load internally all sc_models
        :param ignore_fails: If False, do not load anything if not able to load a single sc_model.
        :param debug_lvl:
        :return: None. Changes are performed inside object
        """

        folder_path = FolderDefinition.get_meta_scmodels_folder_path(runset_id=self._runsetid,
                                                                     folder_flag=self._folder_flag)

        self._scmodel_meta_infos = {}

        if not os.path.exists(folder_path):
            Debug.dl("MetaFileManage: The following folder was not found.", 1, debug_lvl)
            Debug.dl("    '{0}'".format(folder_path), 1, debug_lvl)
            return None

        all_files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

        for cur_file_path in all_files_path:
            metafile_object = MetaScModel(cur_file_path, debug_lvl)
            if (metafile_object is None) and (not ignore_fails):
                return None

            self._scmodel_meta_infos[metafile_object.get_id()] = metafile_object

    def get_all_scmodel_ids(self):
        """
        Self-decrypting name.
        Should be called after 'load_all_scmodel_meta_info()'
        :return: Array of strings if sc_models are loaded, None otherwise
        """

        return None if self._scmodel_meta_infos is None else self._scmodel_meta_infos.keys()

    def get_all_scmodel_pairs(self, evaluated_models=None, debug_lvl=0):
        """

        :param evaluated_models:
        :param debug_lvl:
        :return: List of strings if it was possible to be retrieved, None otherwise
        """

        # if nothing is given, get all models
        if evaluated_models is None:
            all_models = self.get_all_scmodel_ids()
        else:
            all_models = evaluated_models

        # basic check
        if evaluated_models is None:
            Debug.dl("MetaFileManage: List of single models id is None.", 1, debug_lvl)
            return None

        # build al possible combinations
        all_pairs = []
        for cur_model_a in all_models:
            for cur_model_b in all_models:
                if cur_model_a != cur_model_b:
                    all_pairs.append("{0}_{1}".format(cur_model_a, cur_model_b))
        return all_pairs

    def scmodel_exists(self, scmodel_id):
        """

        :param scmodel_id:
        :return: Boolean
        """

        return False if ((self._scmodel_meta_infos is None) or (scmodel_id not in self._scmodel_meta_infos)) else True

    def get_title_of_scmodel(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        scmodel_object = self._get_meta_sc_model_obj(scmodel_id, debug_lvl)

        if scmodel_object is not None:
            return scmodel_object.get_title()
        else:
            return None

    def get_all_products_of_scmodel(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return: List of sc_product ids if found model. None otherwise.pwd
        """

        scmodel_object = self._get_meta_sc_model_obj(scmodel_id, debug_lvl)

        if scmodel_object is not None:
            return scmodel_object.get_product_set(debug_lvl=debug_lvl)
        else:
            return None

    def get_scmodel_meta_file_path(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if scmodel_id is None:
            Debug.dl("MetaFileManage: Provided 'None' sc_model_id.", 1, debug_lvl)
            return None

        folder_path = FolderDefinition.get_meta_scmodels_folder_path(runset_id=self._runsetid,
                                                                     folder_flag=self._folder_flag)
        file_name = "{0}{1}".format(scmodel_id, ".json")
        file_path = os.path.join(folder_path, file_name)
        return file_path

    def get_all_representations_of_scmodel(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        scmodel_object = self._get_meta_sc_model_obj(scmodel_id, debug_lvl)

        if scmodel_object is not None:
            return scmodel_object.get_representation_set(debug_lvl=debug_lvl)
        else:
            return None

    def get_all_representations_of_screference(self, screference_id, debug_lvl=0):
        """

        :param screference_id:
        :param debug_lvl:
        :return:
        """

        screference_object = self._get_meta_sc_reference_obj(screference_id, debug_lvl)

        if screference_object is not None:
            return screference_object.get_representation_set(debug_lvl=debug_lvl)
        else:
            return None

    def get_all_representations_of_scmodelcombination(self, scmodelcomb_id, debug_lvl=0):
        """

        :param scmodelcomb_id:
        :param debug_lvl:
        :return:
        """

        scmodelcomb_object = self._get_meta_sc_modelcomb_obj(scmodelcomb_id, debug_lvl)

        if scmodelcomb_object is not None:
            return scmodelcomb_object.get_representation_set()
        else:
            return None

    def get_pastmodelid_of_scmodelcombination(self, scmodelcomb_id, debug_lvl=0):
        """

        :param scmodelcomb_id:
        :param debug_lvl:
        :return:
        """

        scmodelcomb_object = self._get_meta_sc_modelcomb_obj(scmodelcomb_id, debug_lvl)

        if scmodelcomb_object is not None:
            return scmodelcomb_object.get_representations_past_model_id()
        else:
            return None

    def get_foremodelid_of_scmodelcombination(self, scmodelcomb_id, debug_lvl=0):
        """

        :param scmodelcomb_id:
        :param debug_lvl:
        :return:
        """

        scmodelcomb_object = self._get_meta_sc_modelcomb_obj(scmodelcomb_id, debug_lvl)

        if scmodelcomb_object is not None:
            return scmodelcomb_object.get_representations_fore_model_id()
        else:
            return None

    def get_all_representationscompound_of_scmodelcombination(self, scmodelcomb_id, debug_lvl=0):
        """

        :param scmodelcomb_id:
        :param debug_lvl:
        :return:
        """

        scmodelcomb_object = self._get_meta_sc_modelcomb_obj(scmodelcomb_id, debug_lvl)

        if scmodelcomb_object is not None:
            return scmodelcomb_object.get_representationcomp_set()
        else:
            return None

    def get_all_evaluations(self):
        """

        :return:
        """

        return None if self._evaluation_matrix is None else self._evaluation_matrix.get_all_evaluations()

    def get_all_evaluations_of_scmodel(self, scmodel_id):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        if self._evaluation_matrix is not None:
            return self._evaluation_matrix.get_all_evaluations_of_scmodel(scmodel_id)
        else:
            return None

    def get_binaries_generator_script_of_scmodel(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        scmodel_object = self._get_meta_sc_model_obj(scmodel_id, debug_lvl)
        if scmodel_object is not None:
            return scmodel_object.get_binary_generator_script(debug_lvl=debug_lvl)
        else:
            return None

    def get_binaries_generator_states_history_script_of_scmodel(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        scmodel_object = self._get_meta_sc_model_obj(scmodel_id, debug_lvl)
        if scmodel_object is not None:
            return scmodel_object.get_binary_generator_states_history_script(debug_lvl=debug_lvl)
        else:
            return None

    def get_binaries_generator_script_hydroforecast_of_scmodel(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        scmodel_object = self._get_meta_sc_model_obj(scmodel_id, debug_lvl)
        if scmodel_object is not None:
            return scmodel_object.get_binary_generator_hydroforecast_script()
        else:
            return None

    # ##### model combinations #### #

    def load_all_scmodelcomb_meta_info(self, ignore_fails=False, debug_lvl=0):
        """
        Load internally all sc_modelcombs
        :param ignore_fails: If False, do not load anything if not able to load a single sc_modelcomb.
        :param debug_lvl:
        :return: None. Changes are performed inside object
        """

        self._scmodelcomb_meta_infos = {}

        folder_path = FolderDefinition.get_meta_scmodelcomb_folder_path(runset_id=self._runsetid,
                                                                        folder_flag=self._folder_flag)

        # basic check - folder must exist
        if not os.path.exists(folder_path):
            return

        # read all files and load them into memory
        all_files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
        for cur_file_path in all_files_path:
            metafile_object = MetaScModelComb(cur_file_path, debug_lvl)
            if (metafile_object is None) and (not ignore_fails):
                return

            self._scmodelcomb_meta_infos[metafile_object.get_id()] = metafile_object

    def get_all_scmodelcomb_ids(self):
        """
        Self-decrypting name.
        Should be called after 'load_all_scmodelcomb_meta_info()'
        :return: Array of strings if sc_model_combs are loaded, None otherwise
        """

        return None if self._scmodelcomb_meta_infos is None else self._scmodelcomb_meta_infos.keys()

    def scmodelcomb_exists(self, scmodelcomb_id):
        """

        :param scmodelcomb_id:
        :return: Boolean
        """

        if (self._scmodelcomb_meta_infos is None) or (scmodelcomb_id not in self._scmodelcomb_meta_infos):
            return False
        else:
            return True

    def get_all_representationcomps_of_scmodelcomb(self, scmodelcomb_id, debug_lvl=0):
        """

        :param scmodelcomb_id:
        :param debug_lvl:
        :return:
        """

        scmodelcomb_object = self._get_meta_sc_modelcomb_obj(scmodelcomb_id, debug_lvl)

        if scmodelcomb_object is not None:
            return scmodelcomb_object.get_representationcomp_set()
        else:
            return None

    # ##### reference methods #### #

    def screference_exists(self, screference_id):
        """

        :param screference_id:
        :return:
        """

        return False if ((self._screference_meta_infos is None) or
                         (screference_id not in self._screference_meta_infos)) else True

    def get_all_products_of_screference(self, screference_id, debug_lvl=0):
        """

        :param screference_id:
        :param debug_lvl:
        :return: List of sc_product ids if found model. None otherwise.pwd
        """

        screference_object = self._get_meta_sc_reference_obj(screference_id, debug_lvl)

        if screference_object is not None:
            return screference_object.get_product_set(debug_lvl=debug_lvl)
        else:
            return None

    def get_screference_meta_file_path(self, screference_id, debug_lvl=0):
        """

        :param screference_id:
        :param debug_lvl:
        :return:
        """

        folder_path = FolderDefinition.get_meta_screferences_folder_path(runset_id=self._runsetid,
                                                                         folder_flag=self._folder_flag)
        file_name = "{0}.json".format(screference_id)
        file_path = os.path.join(folder_path, file_name)
        return file_path

    def load_all_screference_meta_info(self, ignore_fails=False, debug_lvl=0):
        """

        :param ignore_fails:
        :param debug_lvl:
        :return:
        """

        folder_path = FolderDefinition.get_meta_screferences_folder_path(runset_id=self._runsetid,
                                                                         folder_flag=self._folder_flag)

        self._screference_meta_infos = {}

        if not os.path.exists(folder_path):
            Debug.dl("MetaFileManage: The following folder was not found.", 1, debug_lvl)
            Debug.dl("    '{0}'".format(folder_path), 1, debug_lvl)
            return None

        all_files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

        for cur_file_path in all_files_path:
            metafile_object = MetaScReference(cur_file_path, debug_lvl)
            if (metafile_object is None) and (not ignore_fails):
                return None

            self._screference_meta_infos[metafile_object.get_id()] = metafile_object

    def import_screference_definition(self, sc_reference_id, replace_file=False, debug_lvl=0):
        """

        :param sc_reference_id:
        :param debug_lvl:
        :return:
        """

        if self._runsetid is None:
            Debug.dl("MetaFileManage: Trying to import sc_reference {0} without setting a runset_id.".format(
                sc_reference_id), 1, debug_lvl)
            return False

        # define common filename
        screference_filename = "{0}.json".format(sc_reference_id)

        # define source
        realtime_folder_path = FolderDefinition.get_meta_screferences_folder_path()
        realtime_file_path = os.path.join(realtime_folder_path, screference_filename)

        # runset file path
        runset_folder_path = FolderDefinition.get_meta_screferences_folder_path(runset_id=self._runsetid,
                                                                                folder_flag=self._folder_flag)
        runset_file_path = os.path.join(runset_folder_path, screference_filename)

        # copy file if it is the case
        if (not replace_file) and (os.path.exists(runset_file_path)):
            Debug.dl("MetaFileManage: File already exist: {0} ".format(runset_file_path), 2, debug_lvl)
            return False
        Debug.dl("MetaFileManage: Copying {0} ".format(realtime_file_path), 2, debug_lvl)
        Debug.dl("                 to {0}.".format(runset_file_path), 2, debug_lvl)
        shutil.copy(realtime_file_path, runset_file_path)

        return True

    def get_all_screference_ids(self):
        """
        Self-decrypting name.
        Should be called after 'load_all_screference_meta_info()'
        :return: Array of strings if sc_references are loaded, None otherwise
        """

        return None if self._screference_meta_infos is None else self._screference_meta_infos.keys()

    def get_title_of_screference(self, screference_id, debug_lvl=0):
        """

        :param screference_id:
        :param debug_lvl:
        :return:
        """

        screference_object = self._get_meta_sc_reference_obj(screference_id, debug_lvl)

        if screference_object is not None:
            return screference_object.get_title()
        else:
            return None

    def get_binaries_generator_script_of_screference(self, screference_id, debug_lvl=0):
        """

        :return:
        """
        screference_object = self._get_meta_sc_reference_obj(screference_id, debug_lvl)
        if screference_object is not None:
            return screference_object.get_binary_generator_inst_script()
        else:
            return None

    def get_binaries_generator_script_hist_of_screference(self, screference_id, debug_lvl=0):
        """

        :return:
        """
        screference_object = self._get_meta_sc_reference_obj(screference_id, debug_lvl)
        return screference_object.get_binary_generator_hist_script() if screference_object is not None else None

    # ##### product methods ##### #

    def get_title_of_scproduct(self, scproduct_id):
        """

        :param scproduct_id:
        :return:
        """

        scproduct_object = self._get_meta_sc_product_obj(scproduct_id)

        if scproduct_object is not None:
            return scproduct_object.get_title()
        else:
            return None

    def load_all_scproduct_meta_info(self, ignore_fails=False, debug_lvl=0):
        """
        Load internally all sc_products
        :param ignore_fails: If False, do not load anything if not able to load a single sc_product.
        :param debug_lvl:
        :return: None. Changes are performed inside object
        """

        folder_path = FolderDefinition.get_meta_scproducts_folder_path()
        all_files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

        self._scproduct_meta_infos = {}
        for cur_file_path in all_files_path:
            metafile_object = MetaScProduct(cur_file_path, debug_lvl)
            if (metafile_object is None) and (not ignore_fails):
                return None

            self._scproduct_meta_infos[metafile_object.get_id()] = metafile_object

    def import_scproduct_definition(self, scproduct_id, replace_file=False, debug_lvl=0):
        """

        :param scproduct_id:
        :param replace_file:
        :param debug_lvl:
        :return: Boolean. True if effective on importing file, False otherwise.
        """

        if self._runsetid is None:
            Debug.dl("MetaFileManage: Trying to import sc_product {0} without setting a runset_id.".format(scproduct_id),
                     1, debug_lvl)
            return False

        # define common filename
        scproduct_filename = "{0}.json".format(scproduct_id)

        # define source
        realtime_folder_path = FolderDefinition.get_meta_scproducts_folder_path()
        realtime_file_path = os.path.join(realtime_folder_path, scproduct_filename)

        # runset file path
        runset_folder_path = FolderDefinition.get_meta_scproducts_folder_path(runset_id=self._runsetid,
                                                                              folder_flag=self._folder_flag)
        runset_file_path = os.path.join(runset_folder_path, scproduct_filename)

        # copy file if it is the case
        if (not replace_file) and (os.path.exists(runset_file_path)):
            Debug.dl("MetaFileManage: File already exist: {0} ".format(runset_file_path), 2, debug_lvl)
            return False
        Debug.dl("MetaFileManage: Copying {0} ".format(realtime_file_path), 2, debug_lvl)
        Debug.dl("                 to {0}.".format(runset_file_path), 2, debug_lvl)
        shutil.copy(realtime_file_path, runset_file_path)

        return True

    def get_scproduct_meta_file_path(self, scproduct_id, debug_lvl=0):
        """

        :param scproduct_id:
        :param debug_lvl:
        :return:
        """

        folder_path = FolderDefinition.get_meta_scproducts_folder_path(runset_id=self._runsetid,
                                                                       folder_flag=self._folder_flag)
        file_name = "{0}.json".format(scproduct_id)
        file_path = os.path.join(folder_path, file_name)
        return file_path

    # ##### representation methods ##### #

    def get_all_screpresentation_ids(self):
        """

        :return:
        """

        return None if self._screpresentation_meta_infos is None else self._screpresentation_meta_infos.keys()

    def get_time_interval_of_representation(self, screpresentation_id, debug_lvl=0):
        """

        :param screpresentation_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if screpresentation_id is None:
            return None

        screpresentation_object = self._get_meta_sc_representation_obj(screpresentation_id, debug_lvl)
        if screpresentation_object is not None:
            return int(screpresentation_object.get_time_interval())
        else:
            return None

    def get_genscript_of_representation_sing(self, screpresentation_id, debug_lvl=0):
        """

        :param screpresentation_id:
        :param debug_lvl:
        :return:
        """

        screpresentation_object = self._get_meta_sc_representation_obj(screpresentation_id, debug_lvl)
        if screpresentation_object is not None:
            return screpresentation_object.get_repgen_sing_script()
        else:
            return None

    def get_genscript_of_representation_cmpr(self, screpresentation_id, debug_lvl=0):
        """

        :param screpresentation_id:
        :param debug_lvl:
        :return:
        """

        screpresentation_object = self._get_meta_sc_representation_obj(screpresentation_id, debug_lvl)
        return None if screpresentation_object is None else screpresentation_object.get_repgen_cmpr_script()

    def load_all_screpresentation_meta_info(self, ignore_fails=False, debug_lvl=0):
        """
        Load internally all sc_representations
        :param ignore_fails: If False, do not load anything if not able to load a single sc_representation.
        :param debug_lvl:
        :return: None. Changes are performed inside object
        """

        folder_path = FolderDefinition.get_meta_screpresentations_folder_path(runset_id=self._runsetid)
        if not os.path.exists(folder_path):
            return None
        all_files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

        self._screpresentation_meta_infos = {}
        for cur_file_path in all_files_path:
            metafile_object = MetaScRepresentation(cur_file_path, debug_lvl)
            if (metafile_object is None) and (not ignore_fails):
                return None

            self._screpresentation_meta_infos[metafile_object.get_id()] = metafile_object

    def import_screpresentation_definition(self, screpresentation_id, replace_file=False, debug_lvl=0):
        """

        :param scproduct_id:
        :param replace_file:
        :param debug_lvl:
        :return: Boolean. True if effective on importing file, False otherwise.
        """

        if self._runsetid is None:
            Debug.dl("MetaFileManage: Trying to import sc_representation {0} without setting a runset_id.".format(
                screpresentation_id), 1, debug_lvl)
            return False

        # define common filename
        screpresentation_filename = "{0}.json".format(screpresentation_id)

        # define source
        realtime_folder_path = FolderDefinition.get_meta_screpresentations_folder_path()
        realtime_file_path = os.path.join(realtime_folder_path, screpresentation_filename)

        # runset file path
        runset_folder_path = FolderDefinition.get_meta_screpresentations_folder_path(runset_id=self._runsetid,
                                                                                     folder_flag=self._folder_flag)
        runset_file_path = os.path.join(runset_folder_path, screpresentation_filename)

        # copy file if it is the case
        if (not replace_file) and (os.path.exists(runset_file_path)):
            Debug.dl("MetaFileManage: File already exist: {0} ".format(runset_file_path), 2, debug_lvl)
            return False
        Debug.dl("MetaFileManage: Copying {0} ".format(realtime_file_path), 2, debug_lvl)
        Debug.dl("                 to {0}.".format(runset_file_path), 2, debug_lvl)
        shutil.copy(realtime_file_path, runset_file_path)

        return True

    def get_title_of_screpresentation(self, screpresentation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        screpresentation_object = self._get_meta_sc_representation_obj(screpresentation_id, debug_lvl=debug_lvl)
        if screpresentation_object is not None:
            return screpresentation_object.get_title()
        else:
            return None

    def screpresentation_exists(self, screpresentation_id):
        """

        :param screpresentation_id:
        :return: Boolean
        """

        if (self._screpresentation_meta_infos is None) or (screpresentation_id not in self._screpresentation_meta_infos):
            return False
        else:
            return True

    def get_representation_cleaner_script_of_screpresentation(self, screpresentation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        screpresentation_object = self._get_meta_sc_representation_obj(screpresentation_id, debug_lvl=debug_lvl)
        if screpresentation_object is not None:
            return screpresentation_object.get_reprcln_script()
        else:
            return None

    def get_screpresentation_meta_file_path(self, screpresentation_id, debug_lvl=0):
        """

        :param screpresentation_id:
        :param debug_lvl:
        :return:
        """

        folder_path = FolderDefinition.get_meta_screpresentations_folder_path(runset_id=self._runsetid,
                                                                              folder_flag=self._folder_flag)
        file_name = "{0}.json".format(screpresentation_id)
        file_path = os.path.join(folder_path, file_name)
        return file_path

    # ##### representation compound methods ##### #

    def load_all_screpresentationcomp_meta_info(self, ignore_fails=False, debug_lvl=0):
        """
        Load internally all sc_representationscomp
        :param ignore_fails: If False, do not load anything if not able to load a single sc_representationcomp.
        :param debug_lvl:
        :return: None. Changes are performed inside object
        """

        self._screpresentationcomp_meta_infos = {}

        folder_path = FolderDefinition.get_meta_screpresentationcompositions_folder_path(runset_id=self._runsetid,
                                                                                         folder_flag=self._folder_flag)

        # basic check
        if not os.path.exists(folder_path):
            return

        all_files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

        for cur_file_path in all_files_path:
            metafile_object = MetaScRepresentationComp(cur_file_path, debug_lvl)
            if (metafile_object is None) and (not ignore_fails):
                return None

            self._screpresentationcomp_meta_infos[metafile_object.get_id()] = metafile_object

    def get_all_screpresentationcomp_ids(self):
        """

        :return:
        """

        return None if self._screpresentationcomp_meta_infos is None else self._screpresentationcomp_meta_infos.keys()

    def screpresentationcomp_exists(self, screpresentationcomp_id):
        """

        :param screpresentationcomp_id:
        :return: Boolean
        """

        if (self._screpresentationcomp_meta_infos is None) or \
                (screpresentationcomp_id not in self._screpresentationcomp_meta_infos):
            return False
        else:
            return True

    def get_genscript_of_representation_cmpd(self, screpresentationcompound_id, debug_lvl=0):
        """

        :param screpresentationcompound_id:
        :param debug_lvl:
        :return:
        """

        screpresentationcmpd_object = self._get_meta_sc_representationcompound_obj(screpresentationcompound_id,
                                                                                   debug_lvl)
        return None if screpresentationcmpd_object is None else screpresentationcmpd_object.get_repgen_script()

    def get_updscript_of_representation_cmpd(self, screpresentationcompound_id, debug_lvl=0):
        """

        :param screpresentationcompound_id:
        :param debug_lvl:
        :return:
        """

        screpresentationcmpd_object = self._get_meta_sc_representationcompound_obj(screpresentationcompound_id,
                                                                                   debug_lvl)
        return None if screpresentationcmpd_object is None else screpresentationcmpd_object.get_repupd_script()

    def import_screpresentationcompound_definition(self, screpresentationcompound_id, replace_file=False, debug_lvl=0):
        """

        :param screpresentationcompound_id:
        :param replace_file:
        :param debug_lvl:
        :return:
        """

        if self._runsetid is None:
            Debug.dl("MetaFileManage: Trying to import sc_reprcompound '{0}' without setting a runset_id.".format(
                screpresentationcompound_id), 1, debug_lvl)
            return False

        # define common filename
        screpresentationcompound_filename = "{0}.json".format(screpresentationcompound_id)

        # define source
        root_folder_path = FolderDefinition.get_meta_screpresentationcompositions_folder_path()
        root_file_path = os.path.join(root_folder_path, screpresentationcompound_filename)

        # runset file path
        runset_folder_path = FolderDefinition.get_meta_screpresentationcompositions_folder_path(
            runset_id=self._runsetid, folder_flag=self._folder_flag)
        runset_file_path = os.path.join(runset_folder_path, screpresentationcompound_filename)

        # create folder if necessary
        if not os.path.exists(runset_folder_path):
            os.makedirs(runset_folder_path)

        # copy file if it is the case
        if (not replace_file) and (os.path.exists(runset_file_path)):
            Debug.dl("MetaFileManage: File already exist: {0} ".format(runset_file_path), 2, debug_lvl)
            return False
        Debug.dl("MetaFileManage: Copying {0}".format(root_file_path), 2, debug_lvl)
        Debug.dl("                 to {0}.".format(runset_file_path), 2, debug_lvl)
        shutil.copy(root_file_path, runset_file_path)

        return True

    def get_representation_cleaner_script_of_screpresentationcompound(self, screpresentationcompound_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        screpresentationcompound_object = self._get_meta_sc_representationcompound_obj(screpresentationcompound_id,
                                                                                       debug_lvl=debug_lvl)
        return None if screpresentationcompound_object is None else screpresentationcompound_object.get_repcln_script()

    # ##### evaluation methods ##### #

    def scevaluation_exists(self, scevaluation_id):
        """

        :param scevaluation_id:
        :return:
        """

        return False if ((self._scevaluation_meta_infos is None) or
                         (scevaluation_id not in self._scevaluation_meta_infos)) else True

    def load_all_scevaluation_meta_info(self, ignore_fails=False, debug_lvl=0):
        """
        Load internally all sc_evaluations
        :param ignore_fails:
        :param debug_lvl:
        :return: None. Changes are performed inside object
        """

        folder_path = FolderDefinition.get_meta_scevaluations_folder_path(runset_id=self._runsetid,
                                                                          folder_flag=self._folder_flag)
        if not os.path.exists(folder_path):
            return None
        all_files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

        self._scevaluation_meta_infos = {}
        for cur_file_path in all_files_path:
            metafile_object = MetaScEvaluation(cur_file_path, debug_lvl)
            if (metafile_object is None) and (not ignore_fails):
                return None

            self._scevaluation_meta_infos[metafile_object.get_id()] = metafile_object

        return

    def import_scevaluation_definition(self, scevaluation_id, replace_file=False, debug_lvl=0):
        """

        :param cur_evaluation_id:
        :param debug_lvl:
        :return:
        """

        if self._runsetid is None:
            Debug.dl("MetaFileManage: Trying to import sc_evaluation {0} without setting a runset_id.".format(
                cur_evaluation_id), 1, debug_lvl)
            return False

        # define common filename
        scevaluation_filename = "{0}.json".format(scevaluation_id)

        # define source
        realtime_folder_path = FolderDefinition.get_meta_scevaluations_folder_path()
        realtime_file_path = os.path.join(realtime_folder_path, scevaluation_filename)

        # runset file path
        runset_folder_path = FolderDefinition.get_meta_scevaluations_folder_path(runset_id=self._runsetid,
                                                                                 folder_flag=self._folder_flag)
        runset_file_path = os.path.join(runset_folder_path, scevaluation_filename)

        # copy file if it is the case
        if (not replace_file) and (os.path.exists(runset_file_path)):
            Debug.dl("MetaFileManage: File already exist: {0} ".format(runset_file_path), 2, debug_lvl)
            return False
        Debug.dl("MetaFileManage: Copying {0} ".format(realtime_file_path), 2, debug_lvl)
        Debug.dl("                 to {0}.".format(runset_file_path), 2, debug_lvl)
        shutil.copy(realtime_file_path, runset_file_path)

        return True

    def get_all_scevaluation_ids(self):
        """

        :return:
        """

        return None if self._scevaluation_meta_infos is None else self._scevaluation_meta_infos.keys()

    def get_scevaluation_meta_file_path(self, scevaluation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        folder_path = FolderDefinition.get_meta_scevaluations_folder_path(runset_id=self._runsetid,
                                                                          folder_flag=self._folder_flag)
        file_name = "{0}.json".format(scevaluation_id)
        file_path = os.path.join(folder_path, file_name)
        return file_path

    def get_evaluation_generator_script_of_scevaluation(self, scevaluation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        scevaluation_object = self._get_meta_sc_evaluation_obj(scevaluation_id, debug_lvl=debug_lvl)
        if scevaluation_object is not None:
            return scevaluation_object.get_evalgen_script()
        else:
            return None

    def get_evaluation_generator_hist_script_of_scevaluation(self, scevaluation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        scevaluation_object = self._get_meta_sc_evaluation_obj(scevaluation_id, debug_lvl=debug_lvl)
        if scevaluation_object is not None:
            return scevaluation_object.get_evalgen_hist_script()
        else:
            return None

    def get_evaluation_updater_script_of_scevaluation(self, scevaluation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        scevaluation_object = self._get_meta_sc_evaluation_obj(scevaluation_id, debug_lvl=debug_lvl)
        if scevaluation_object is not None:
            return scevaluation_object.get_evalupd_script()
        else:
            return None

    def get_evaluation_cleaner_script_of_scevaluation(self, scevaluation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        scevaluation_object = self._get_meta_sc_evaluation_obj(scevaluation_id, debug_lvl=debug_lvl)
        if scevaluation_object is not None:
            return scevaluation_object.get_evalcln_script()
        else:
            return None

    # ##### comparison methods ##### #

    def load_comparison_matrix(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return: A list of lists of length 2 with models to be compared
        """

        file_path = FileDefinition.obtain_comparison_set_file_path(runset_id=self._runsetid,
                                                                   folder_flag=self._folder_flag)
        Debug.dl("MetaFileManage: Loading file {0}.".format(file_path), 0, debug_lvl)
        self._comparison_matrix = MetaComparisonSet(file_path)

    def get_all_comparison_acronyms(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        if self._comparison_matrix is None:
            Debug.dl("MetaFileManage: Comparison file not previously loaded.", 0, debug_lvl)
            return None
        else:
            return self._comparison_matrix.get_all_comparison_acronyms()

    def comparison_exists(self, sc_model1=None, sc_model2=None, comparison_acronym=None, debug_lvl=0):
        """

        :param sc_model1:
        :param sc_model2:
        :param comparison_acronym:
        :param debug_lvl:
        :return:
        """

        # base check
        if self._comparison_matrix is None:
            Debug.dl("MetaFileManage: Comparison file not previously loaded.", 0, debug_lvl)
            return None

        the_comparison_acronym = "{0}_{1}".format(sc_model1, sc_model2) if comparison_acronym is None else comparison_acronym
        if the_comparison_acronym in [str(c) for c in self._comparison_matrix.get_all_comparison_acronyms()]:
            return True
        else:
            return False

    def create_comparison_matrix_empty(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        cmpr_mtx_file_path = FileDefinition.obtain_comparison_set_file_path(runset_id=self._runsetid,
                                                                            folder_flag=self._folder_flag)
        with open(cmpr_mtx_file_path, "w+") as w_file:
            w_file.write('{"comparison_matrix":{} }')

        Debug.dl("MetaFileManage: Created empty comparison matrix at '{0}'.".format(cmpr_mtx_file_path), 1, debug_lvl)

    def create_comparison_matrix_maximum(self, force_creation=True, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        cmpr_mtx_file_path = FileDefinition.obtain_comparison_set_file_path(runset_id=self._runsetid,
                                                                            folder_flag=self._folder_flag)

        # basic check
        if (not force_creation) and os.path.exists(cmpr_mtx_file_path):
            Debug.dl("MetaFileManage: Creating maximum file '{0}'.".format(cmpr_mtx_file_path), 1, debug_lvl)
            return

        cp_matrix = {}

        all_models_id = self.get_all_scmodel_ids()
        for cur_model_id_1 in all_models_id:
            for cur_model_id_2 in all_models_id:

                # avoid equals
                if cur_model_id_1 == cur_model_id_2:
                    continue

                cur_set_of_reprs = []
                cur_comparison_id = "{0}_{1}".format(cur_model_id_1, cur_model_id_2)
                reprs_01 = self.get_all_representations_of_scmodel(cur_model_id_1, debug_lvl=debug_lvl)
                reprs_02 = self.get_all_representations_of_scmodel(cur_model_id_2, debug_lvl=debug_lvl)

                for cur_repr_01 in reprs_01:
                    if cur_repr_01 in reprs_02:
                        cur_set_of_reprs.append(cur_repr_01)

                cp_matrix[cur_comparison_id] = cur_set_of_reprs

        output_matrix = {"comparison_matrix": cp_matrix}

        with open(cmpr_mtx_file_path, "w+") as w_file:
            w_file.write(json.dumps(output_matrix))

        Debug.dl("MetaFileManage: Created maximum comparison matrix at '{0}'.".format(cmpr_mtx_file_path), 1, debug_lvl)

    def get_all_representations_of_comparison(self, sc_model1=None, sc_model2=None, comparison_acronym=None,
                                              debug_lvl=0):
        """

        :param sc_model1:
        :param sc_model2:
        :param comparison_acronym:
        :param debug_lvl:
        :return:
        """

        # base check
        if self._comparison_matrix is None:
            Debug.dl("MetaFileManage: Comparison file not previously loaded.", 0, debug_lvl)
            return None

        return self._comparison_matrix.get_representation_list(composition_acronym=comparison_acronym,
                                                               sc_model1_acronym=sc_model1, sc_model2_acronym=sc_model2,
                                                               debug_lvl=debug_lvl)

    # ##### evaluation matrix methods ##### #

    def load_evaluation_matrix(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return: A list of lists of length 2 with models to be compared
        """

        file_path = FileDefinition.obtain_evaluation_matrix_file_path(runset_id=self._runsetid,
                                                                      folder_flag=self._folder_flag)
        self._evaluation_matrix = MetaEvaluationMatrix(file_path, debug_lvl=debug_lvl)

    def get_evaluated_model_ids(self, evaluation_id, debug_lvl=0):
        """

        :param evaluation_id:
        :param debug_lvl:
        :return:
        """

        return self._evaluation_matrix.get_all_evalutated_models(evaluation_id)

    def get_all_evalutated_models_and_references(self, evaluation_id):
        """

        :param evaluation_id:
        :return:
        """

        return self._evaluation_matrix.get_all_evalutated_models_and_references(evaluation_id)

    def get_all_references_associated_to_model(self, model_id):
        """

        :param model_id:
        :return:
        """
        return

    def create_evaluation_matrix_empty(self, force_creation=True, debug_lvl=0):
        """

        :param force_creation:
        :param debug_lvl:
        :return:
        """

        # define file path
        eval_mtx_file_path = FileDefinition.obtain_evaluation_matrix_file_path(runset_id=self._runsetid,
                                                                               folder_flag=self._folder_flag)

        # check if it needs to be created
        if force_creation or not os.path.exists(eval_mtx_file_path):
            with open(eval_mtx_file_path, "w+") as w_file:
                w_file.write('{"evaluation_matrix":{} }')
            Debug.dl("MetaFileManage: Creating empty file '{0}'.".format(eval_mtx_file_path), 1, debug_lvl)
        else:
            Debug.dl("MetaFileManage: File '{0}' already exists. Skipping creating.".format(eval_mtx_file_path),
                     1, debug_lvl)

    def expand_evaluation_matrix(self, sc_evaluation_pair_id, sc_model_id, force_creation=True, debug_lvl=0):
        """

        :param sc_evaluation_pair_id:
        :param sc_model_id:
        :param force_creation:
        :param debug_lvl:
        :return:
        """

        eval_root = "evaluation_matrix"

        # define file path
        eval_mtx_file_path = FileDefinition.obtain_evaluation_matrix_file_path(runset_id=self._runsetid,
                                                                               folder_flag=self._folder_flag)
        # create empty if needed
        if not os.path.exists(eval_mtx_file_path):
            self.create_evaluation_matrix_empty(force_creation=force_creation, debug_lvl=debug_lvl)

        # read eval matrix file content
        with open(eval_mtx_file_path, "r") as r_file:
            json_data = json.load(r_file)

        # add element
        if sc_evaluation_pair_id not in json_data[eval_root].keys():
            json_data[eval_root][sc_evaluation_pair_id] = []
        if sc_model_id not in json_data[eval_root][sc_evaluation_pair_id]:
            json_data[eval_root][sc_evaluation_pair_id].append(sc_model_id)

        # rewrite matrix
        with open(eval_mtx_file_path, "w") as w_file:
            json.dump(json_data, w_file, indent=4)

    # ##### ####

    def import_scmenu_definition(self, debug_lvl=0):
        """

        :param debug_lvl:
        :return:
        """

        # define source and destination paths
        realtime_folder_path = FolderDefinition.get_meta_scmenu_folder()
        runset_folder_path = FolderDefinition.get_meta_scmenu_folder(runset_id=self._runsetid,
                                                                     folder_flag=self._folder_flag)

        # copy all files
        for cur_file_name in os.listdir(realtime_folder_path):
            cur_file_path = os.path.join(realtime_folder_path, cur_file_name)
            if os.path.isfile(cur_file_path):
                cur_dest_file_path = os.path.join(runset_folder_path, cur_file_name)
                shutil.copy(cur_file_path, cur_dest_file_path)

    # ##### private methods #####

    def _get_meta_sc_model_obj(self, scmodel_id, debug_lvl=0):
        """

        :param scmodel_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if self._scmodel_meta_infos is None:
            Debug.dl("MetaFileManage: tried to get scmodel parameters without previous loading.", 1, debug_lvl)
            return None

        if scmodel_id not in self._scmodel_meta_infos.keys():
            Debug.dl("MetaFileManage: scmodel '{0}' not found.".format(scmodel_id), 1, debug_lvl)
            return None

        return self._scmodel_meta_infos[scmodel_id]

    def _get_meta_sc_modelcomb_obj(self, scmodelcomb_id, debug_lvl=0):
        """

        :param scmodelcomb_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if self._scmodelcomb_meta_infos is None:
            Debug.dl("MetaFileManage: tried to get scmodelcomb parameters without previous loading.", 1, debug_lvl)
            return None

        if scmodelcomb_id not in self._scmodelcomb_meta_infos.keys():
            Debug.dl("MetaFileManage: scmodelcomb '{0}' not found in {1}.".format(scmodelcomb_id,
                                                                                 self._scmodelcomb_meta_infos.keys()),
                     1, debug_lvl)
            return None

        return self._scmodelcomb_meta_infos[scmodelcomb_id]

    def _get_meta_sc_reference_obj(self, screference_id, debug_lvl=0):
        """

        :param screference_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if self._screference_meta_infos is None:
            Debug.dl("MetaFileManage: tried to get screference parameters without previous loading.", 1, debug_lvl)
            return None

        if screference_id not in self._screference_meta_infos.keys():
            Debug.dl("MetaFileManage: screference '{0}' not found.", 1, debug_lvl)
            return None

        return self._screference_meta_infos[screference_id]

    def _get_meta_sc_product_obj(self, scproduct_id, debug_lvl=0):
        """

        :param scproduct_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if self._scproduct_meta_infos is None:
            Debug.dl("MetaFileManage: tried to get scproduct parameters without previous loading.", 1, debug_lvl)
            return None

        if scproduct_id not in self._scproduct_meta_infos.keys():
            Debug.dl("MetaFileManage: scproduct_id '{0}' not found.", 1, debug_lvl)
            return None

        return self._scproduct_meta_infos[scproduct_id]

    def _get_meta_sc_representation_obj(self, screpresentation_id, debug_lvl=0):
        """

        :param screpresentation_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if self._screpresentation_meta_infos is None:
            Debug.dl("MetaFileManage: tried to get screpresentation information without previous loading.", 1, debug_lvl)
            return None

        if screpresentation_id not in self._screpresentation_meta_infos.keys():
            Debug.dl("MetaFileManage: screpresentation '{0}' not found.", 1, debug_lvl)
            return None

        return self._screpresentation_meta_infos[screpresentation_id]

    def _get_meta_sc_representationcompound_obj(self, screpresentationcmpd_id, debug_lvl=0):
        """

        :param screpresentationcmpd_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if self._screpresentationcomp_meta_infos is None:
            Debug.dl("MetaFileManage: tried to get sc_representation_cmpd information without previous loading.", 1,
                     debug_lvl)
            return None

        if screpresentationcmpd_id not in self._screpresentationcomp_meta_infos.keys():
            Debug.dl("MetaFileManage: sc_representation_cmpd '{0}' not found.".format(screpresentationcmpd_id), 1,
                     debug_lvl)
            return None

        return self._screpresentationcomp_meta_infos[screpresentationcmpd_id]

    def _get_meta_sc_evaluation_obj(self, scevaluation_id, debug_lvl=0):
        """

        :param scevaluation_id:
        :param debug_lvl:
        :return:
        """

        # basic check
        if self._scevaluation_meta_infos is None:
            Debug.dl("MetaFileManage: tried to get scevaluation information without previous loading.", 1, debug_lvl)
            return None

        if scevaluation_id not in self._scevaluation_meta_infos.keys():
            Debug.dl("MetaFileManage: scevaluation '{0}' not found.", 1, debug_lvl)
            return None

        return self._scevaluation_meta_infos[scevaluation_id]
