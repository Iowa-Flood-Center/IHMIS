import json


class WaitingRoomDef:
    _default_settings_file_name = "../../conf/settings.json"

    # constants loaded from settings file
    _download_dest_path = None
    _unzip_output_folder_path = None
    _api_url_root = None
    _api_get = None
    _api_delete = None

    @staticmethod
    def load_settings(file_path=None):
        """

        :param file_path:
        :return:
        """

        # read file
        file_desc = file_path if file_path is not None else WaitingRoomDef._default_settings_file_name
        with open(file_desc, "r") as json_file:
            settings_content = json.load(json_file)

        # set internal variables
        WaitingRoomDef._url_root = settings_content["waitingroom_files_root_url"]
        WaitingRoomDef._api_url_root = settings_content["ws_api_root_url"]
        WaitingRoomDef._unzip_output_folder_path = settings_content["runset_requests_folder_path"]
        WaitingRoomDef._download_dest_path = settings_content["runset_temp_folder_path"]
        WaitingRoomDef._api_get = settings_content["ws_api_waitingroom"] + "?from=waiting_room"
        WaitingRoomDef._api_del = settings_content["ws_api_waitingroom"] + "/{0}"

        print("Settings loaded.")

    @staticmethod
    def get_ws_list_url():
        """

        :return:
        """

        return "{0}{1}".format(WaitingRoomDef._api_url_root, WaitingRoomDef._api_get)

    @staticmethod
    def get_ws_del_url(file_name):
        """

        :param file_name:
        :return:
        """
        api_delete_call = WaitingRoomDef._api_del.format(file_name)
        return "{0}{1}".format(WaitingRoomDef._api_url_root, api_delete_call)

    @staticmethod
    def get_download_file_url(file_name):
        """

        :param file_name:
        :return:
        """
        return "{0}{1}".format(WaitingRoomDef._url_root, file_name)

    @staticmethod
    def get_download_folder_path():
        """

        :return:
        """

        return WaitingRoomDef._download_dest_path

    @staticmethod
    def get_unzip_output_folder_path():
        """

        :return:
        """
        return WaitingRoomDef._unzip_output_folder_path

    def __init__(self):
        return
