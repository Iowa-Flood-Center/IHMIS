from debug import Debug
import inspect
import json
import os

class GeneralRequestValidator:

    _valid_options = None

    def __init__(self):
        return

    @staticmethod
    def load_valid_options(force=False):
        """
        Changes the value of the internal static _valid_options variable
        :param force:
        :return:
        """

        CONTAINING_FOLDER_NAME = "static"
        OPTIONS_FILE_NAME = "valid_options.json"

        if (GeneralRequestValidator._valid_options is not None) and (not force):
            return

        # define file path
        current_folder_path = inspect.getframeinfo(inspect.currentframe()).filename
        folderpath = os.path.dirname(os.path.abspath(current_folder_path))
        folderpath = os.path.dirname(os.path.dirname(folderpath))
        filepath = os.path.join(folderpath, CONTAINING_FOLDER_NAME, OPTIONS_FILE_NAME)

        # read it
        with open(filepath, "r") as r_file:
            GeneralRequestValidator._valid_options = json.load(r_file)
        return

    @staticmethod
    def validate_file(file_path, debug_lvl=0):
        """

        :param file_path:
        :param debug_lvl:
        :return:
        """

        # basic check
        if (not os.path.exists(file_path)) or (file_path is None):
            Debug.dl("generalrequestvalidator_lib: File not found: {0}".format(file_path), 1, debug_lvl)
            return False

        # read file and validate content
        with open(file_path, "r") as r_file:
            try:
                json_data = json.load(r_file)
            except json.decoder.JSONDecodeError:
                Debug.dl("generalrequestvalidator_lib: Invalid JSON content given.", 1, debug_lvl)
                return False
        return GeneralRequestValidator.validate(json_data, debug_lvl=debug_lvl)

    @staticmethod
    def validate_string(json_string, debug_lvl=0):
        """

        :param json_string:
        :param debug_lvl:
        :return:
        """

        # basic check
        if json_string is None:
            return None

        # parse and validate content
        try:
            json_data = json.loads(json_string)
        except json.decoder.JSONDecodeError:
            Debug.dl("generalrequestvalidator_lib: Invalid JSON content given.", 1, debug_lvl)
            return False
        return GeneralRequestValidator.validate(json_data, debug_lvl=debug_lvl)

    @staticmethod
    def validate(json_data, debug_lvl=0):
        """

        :param json_data:
        :param debug_lvl:
        :return:
        """

        GeneralRequestValidator.load_valid_options()

        mandatory_args = GeneralRequestValidator._get_mandatory_arguments(json_data, debug_lvl=debug_lvl)
        if mandatory_args is None:
            Debug.dl("generalrequestvalidator_lib: Failed due to missing a mandatory key.", 2, debug_lvl)
            return False

        return GeneralRequestValidator._validate_mandatory_arguments(json_data, mandatory_args, debug_lvl=debug_lvl)

    @staticmethod
    def _list_mandatory_arguments(dict, debug_lvl=0):
        """

        :param dict:
        :param debug_lvl:
        :return:
        """

        ret_list = {}
        for cur_key in dict.keys():
            if cur_key.startswith("+"):
                ret_list[cur_key[1:]] = dict[cur_key]
        return ret_list

    @staticmethod
    def _get_mandatory_arguments(json_data, debug_lvl=0):
        """

        :param json_data:
        :param valid_options:
        :param debug_lvl:
        :return: List of Strings if possible to build it. None otherwise.
        """

        args = {}

        # get mandatory arguments in the first level
        cur_dict = GeneralRequestValidator._valid_options
        args.update(GeneralRequestValidator._list_mandatory_arguments(cur_dict, debug_lvl=debug_lvl))

        # get target dictionary
        if "target" not in json_data.keys():
            Debug.dl("generalrequestvalidator_lib: Missing 'target' key.", 3, debug_lvl)
            return None
        if "~{0}".format(json_data["target"]) not in cur_dict["targets"].keys():
            Debug.dl("generalrequestvalidator_lib: Invalid 'target' value ({0}).".format(json_data["target"]), 3,
                     debug_lvl)
            return None

        # get mandatory arguments in the second level
        cur_dict = cur_dict["targets"]["~{0}".format(json_data["target"])]
        args.update(GeneralRequestValidator._list_mandatory_arguments(cur_dict, debug_lvl=debug_lvl))

        # get action dictionary
        if "action" not in json_data.keys():
            Debug.dl("generalrequestvalidator_lib: Missing 'action' key.", 3, debug_lvl)
            return None
        if "-{0}".format(json_data["action"]) not in cur_dict["actions"].keys():
            Debug.dl("generalrequestvalidator_lib: Invalid 'action' value ({0}).".format(json_data["action"]), 3,
                     debug_lvl)
            return None

        # get mandatory arguments in the third level
        cur_dict = cur_dict["actions"]["-{0}".format(json_data["action"])]
        args.update(GeneralRequestValidator._list_mandatory_arguments(cur_dict, debug_lvl=debug_lvl))

        return args

    @staticmethod
    def _validate_mandatory_arguments(json_data, mandatory_arguments, debug_lvl=0):
        """

        :param json_data:
        :param mandatory_arguments:
        :param debug_lvl:
        :return:
        """

        # get action dictionary
        if "arguments" not in json_data.keys():
            Debug.dl("generalrequestvalidator_lib: Missing 'arguments' key.", 3, debug_lvl)
            return None

        given_args = json_data["arguments"]
        for cur_mandatory_arg in mandatory_arguments.keys():
            if cur_mandatory_arg not in given_args:
                Debug.dl("generalrequestvalidator_lib: Missing argument '{0}'.".format(cur_mandatory_arg), 3, debug_lvl)
                return None
            argument_value = given_args[cur_mandatory_arg]
            argument_type = mandatory_arguments[cur_mandatory_arg]
            if not GeneralRequestValidator._validate_given_argument_value(argument_value, argument_type):
                Debug.dl("generalrequestvalidator_lib: Mismatch argument type for '{0}'.".format(cur_mandatory_arg), 3,
                         debug_lvl)
                Debug.dl("generalrequestvalidator_lib:     Expected '{0}', '{1}' given.".format(argument_type, type(argument_value)), 3,
                         debug_lvl)
                return None

        # if got to this point, accept it
        Debug.dl("generalrequestvalidator_lib: Content approved.", 4, debug_lvl)
        return True

    @staticmethod
    def _validate_given_argument_value(argument_value, argument_type):
        """

        :param argument_value:
        :param argument_type:
        :param debug_lvl:
        :return:
        """
        if (argument_type == "STRING") and (type(argument_value) is str):
            return True
        elif (argument_type == "[STRING]") and (type(argument_value) is list):
            return True
        else:
            return False
