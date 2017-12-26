from libs.waitingroom_downloader import WaitingRoomDef
import json
import os


class WaitingRoomRunsetMergeDef(WaitingRoomDef):

    _server_add = None
    _server_usr = None
    _server_cmd = None

    @staticmethod
    def load_settings(file_path=None):
        WaitingRoomDef.load_settings(file_path)

        # read file
        file_desc = file_path if file_path is not None else WaitingRoomRunsetMergeDef._default_settings_file_name
        with open(file_desc, "r") as json_file:
            settings_content = json.load(json_file)

        # set attributes
        WaitingRoomRunsetMergeDef._url_root = settings_content["waitingroom_runsetmerge_files_root_url"]
        WaitingRoomRunsetMergeDef._api_get = settings_content["ws_api_waitingroom_runsetmerge"] + "?from=waiting_room"
        WaitingRoomRunsetMergeDef._api_del = settings_content["ws_api_waitingroom_runsetmerge"] + "/{0}"
        WaitingRoomRunsetMergeDef._runset_archival_folder_path = settings_content["runset_archival_folder_path"]

        WaitingRoomRunsetMergeDef._server_add = settings_content["proc_server_addr"]
        WaitingRoomRunsetMergeDef._server_usr = settings_content["proc_server_user"]
        WaitingRoomRunsetMergeDef._server_cmd = settings_content["runsetmerge_remote_system_call"]

    @staticmethod
    def get_ws_list_url():
        """

        :return:
        """

        return "{0}{1}".format(WaitingRoomDef._api_url_root, WaitingRoomRunsetMergeDef._api_get)

    @staticmethod
    def get_ws_del_url(file_name):
        """

        :param file_name:
        :return:
        """
        api_delete_call = WaitingRoomRunsetMergeDef._api_del.format(file_name)
        return "{0}{1}".format(WaitingRoomDef._api_url_root, api_delete_call)

    @staticmethod
    def get_download_file_url(file_name):
        """

        :param cur_file:
        :return:
        """
        return "{0}{1}".format(WaitingRoomRunsetMergeDef._url_root, file_name)

    @staticmethod
    def get_ssh_call_to_backend_postprocess(json_object):
        """

        :param json_object:
        :return:
        """
        ssh_call = "ssh {0}@{1} {2} {3}"
        ssh_call = ssh_call.format(WaitingRoomRunsetMergeDef._server_usr,
                                   WaitingRoomRunsetMergeDef._server_add,
                                   WaitingRoomRunsetMergeDef._server_cmd,
                                   WaitingRoomRunsetMergeDef.escape_json(json_object))
        return ssh_call

    @staticmethod
    def escape_json(json_object):
        """

        :param json_object:
        :return: String
        """

        json_txt = json.dumps(json_object)
        json_txt = json_txt.replace('"', '\\"')
        return "\\'{0}\\'".format(json_txt)

    # ################################## TODO - move to another place ################################################ #

    @staticmethod
    def get_runsets_archial_folder_path(runset_id):
        """

        :param runset_id:
        :return:
        """
        return os.path.join(WaitingRoomRunsetMergeDef._runset_archival_folder_path, runset_id)

    @staticmethod
    def get_model_meta_folder_path(runset_id, model_id):
        """

        :param runset_id:
        :param model_id:
        :return:
        """
        return os.path.join(WaitingRoomRunsetMergeDef.get_runsets_archial_folder_path(runset_id),
                            'metafiles_sandbox', 'sc_models', model_id)
