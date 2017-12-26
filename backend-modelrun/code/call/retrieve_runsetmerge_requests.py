from libs.waitingroom_runsetmerge import WaitingRoomRunsetMergeDef
import urllib.request
import requests
import json
import os

# ####################################################### DEFS ####################################################### #

# ####################################################### DEFS ####################################################### #


def process_runset_request_locally(json_data):
    """

    :param json_data:
    :return:
    """

    # basic check - both FROM and TO runsets are set
    if 'from_runset_id' not in json_data.keys():
        print("Missing core key 'from_runset_id'. Stopping script.")
        return
    elif 'to_runset_id' not in json_data.keys():
        print("Missing core key 'to_runset_id'. Stopping script.")
        return

    # get variables
    from_runset_id = json_data['from_runset_id']
    to_runset_id = json_data['to_runset_id']

    # basic check - both FROM and TO runsets must exist locally
    runset_from_folder_path = WaitingRoomRunsetMergeDef.get_runsets_archial_folder_path(from_runset_id)
    runset_to_folder_path = WaitingRoomRunsetMergeDef.get_runsets_archial_folder_path(to_runset_id)
    if (not os.path.exists(runset_from_folder_path)) or (not os.path.isdir(runset_from_folder_path)):
        print("Folder '{0}' does not exist.".format(runset_from_folder_path))
        return
    elif (not os.path.exists(runset_to_folder_path)) or (not os.path.isdir(runset_to_folder_path)):
        print("Folder '{0}' does not exist.".format(runset_to_folder_path))
        return

    # sc_models
    if 'models_id' in json_data.keys():
        for cur_model_id in json_data['models_id']:
            cur_from_folder_path = get_model_meta_folder_path(from_runset_id, cur_model_id)
            cur_to_folder_path = get_model_meta_folder_path(to_runset_id, cur_model_id)
            print("Copy '{0}' to '{1}'.".format(cur_from_folder_path, cur_to_folder_path))


def process_runset_request_externally(json_data):
    """

    :param json_data:
    :return:
    """

    ssh_cmd = WaitingRoomRunsetMergeDef.get_ssh_call_to_backend_postprocess(json_data)
    os.system(ssh_cmd)

# ####################################################### CALL ####################################################### #

# load settings
WaitingRoomRunsetMergeDef.load_settings()

# open connection and read content
ws_url = WaitingRoomRunsetMergeDef.get_ws_list_url()
print("Reading from '{0}'.".format(ws_url))
url_con = urllib.request.urlopen(ws_url)
url_txt = str(url_con.read().decode()).strip()

# check content
json_obj = json.loads(url_txt)
if len(json_obj) == 0:
    print("No files in the waiting room.")
    quit()
else:
    print("Files in the waiting room: {0}.".format(json_obj))

# process file by file
for cur_file in json_obj:

    # read the file and process it
    cur_file_url = WaitingRoomRunsetMergeDef.get_download_file_url(cur_file)
    print("Reading from {0}".format(cur_file_url))
    url_con = urllib.request.urlopen(cur_file_url)
    url_txt = str(url_con.read().decode()).strip()
    url_con.close()
    process_runset_request_locally(json.loads(url_txt))
    process_runset_request_externally(json.loads(url_txt))

    # delete file from server
    cur_del_url = WaitingRoomRunsetMergeDef.get_ws_del_url(cur_file)
    print("Calling DELETE '{0}'...".format(cur_del_url))
    requests.delete(cur_del_url)
    print("Called '{0}'.".format(cur_del_url))
