from libs.waitingroom_runsetmerge import WaitingRoomRunsetMergeDef
import urllib.request
import subprocess
import requests
import shutil
import json
import os

# ####################################################### DEFS ####################################################### #

# ####################################################### DEFS ####################################################### #


def process_runset_request_locally(json_data):
    """

    :param json_data:
    :return: Boolean. True if possible to merge. False otherwise.
    """

    # basic check - both FROM and TO runsets are set
    if 'from_runset_id' not in json_data.keys():
        print("Missing core key 'from_runset_id'. Stopping script.")
        return False
    elif 'to_runset_id' not in json_data.keys():
        print("Missing core key 'to_runset_id'. Stopping script.")
        return False

    # get variables
    from_runset_id = json_data['from_runset_id']
    to_runset_id = json_data['to_runset_id']

    # basic check - both FROM and TO runsets must exist locally
    runset_from_folder_path = WaitingRoomRunsetMergeDef.get_runsets_archial_folder_path(from_runset_id)
    runset_to_folder_path = WaitingRoomRunsetMergeDef.get_runsets_archial_folder_path(to_runset_id)
    if (not os.path.exists(runset_from_folder_path)) or (not os.path.isdir(runset_from_folder_path)):
        print("Folder '{0}' does not exist.".format(runset_from_folder_path))
        return False
    elif (not os.path.exists(runset_to_folder_path)) or (not os.path.isdir(runset_to_folder_path)):
        print("Folder '{0}' does not exist.".format(runset_to_folder_path))
        return False

    # sc_models
    if 'models_id' in json_data.keys():
        for cur_model_id in json_data['models_id']:
            # get source and destination folders
            cur_from_folder_path = WaitingRoomRunsetMergeDef.get_model_meta_folder_path(from_runset_id, cur_model_id)
            cur_from_folder_path = "{0}.json".format(cur_from_folder_path)
            cur_to_folder_path = WaitingRoomRunsetMergeDef.get_model_meta_folder_path(to_runset_id, cur_model_id)
            cur_to_folder_path = "{0}.json".format(cur_to_folder_path)

            # basic check - need to be renamed?
            if os.path.exists(cur_to_folder_path):
                renaming = True
                cur_dest_model_id = "{0}{1}".format(cur_model_id, from_runset_id)
                cur_to_folder_path = WaitingRoomRunsetMergeDef.get_model_meta_folder_path(to_runset_id,
                                                                                          cur_dest_model_id)
                cur_to_folder_path = "{0}.json".format(cur_to_folder_path)
                if os.path.exists(cur_to_folder_path):
                    print("Model was already copied (found '{0}').".format(cur_to_folder_path))
                    return False
            else:
                renaming = False

            print("Copy '{0}' to '{1}'.".format(cur_from_folder_path, cur_to_folder_path))
            copy_model_meta_file(cur_from_folder_path, cur_to_folder_path, renaming)

    return True

def copy_model_meta_file(from_path, to_path, renamed):
    """

    :param from_path:
    :param to_path:
    :param renamed:
    :return:
    """
    if renamed:
        new_model_id = os.path.splitext(os.path.basename(to_path))[0]
        with open(from_path, "r") as r_file:
            json_data = json.load(r_file)
        json_data["sc_model"]["id"] = new_model_id
        with open(to_path, "w") as r_file:
            json.dump(json_data, r_file, sort_keys=True, indent=4)
    else:
        shutil.copyfile(from_path, to_path)

def process_runset_request_externally(json_data):
    """

    :param json_data:
    :return:
    """

    ssh_cmd = WaitingRoomRunsetMergeDef.get_ssh_call_to_backend_postprocess(json_data)
    print("Calling externally 1: '{0}'".format(ssh_cmd))
    proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("Call output: {0}.".format(out))
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

    if process_runset_request_locally(json.loads(url_txt)):
        process_runset_request_externally(json.loads(url_txt))
    else:
        print("Failed calling internally")

    # delete file from server
    cur_del_url = WaitingRoomRunsetMergeDef.get_ws_del_url(cur_file)
    print("Calling DELETE '{0}'...".format(cur_del_url))
    requests.delete(cur_del_url)
    print("Called '{0}'.".format(cur_del_url))
