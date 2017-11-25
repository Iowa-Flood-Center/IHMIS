from libs.waitingroom_downloader import WaitingRoomDef
import urllib.request
import requests
import json
import os


# ####################################################### DEFS ####################################################### #

def get_runset_job(folder_path):
    """

    :param folder_path:
    :return: File path, runset id
    """

    all_file_names = os.listdir(folder_path)
    all_file_names.sort()
    ignore_this = False
    for cur_idx, cur_file_name in enumerate(all_file_names):
        print("...Considering '{0}'.".format(cur_file_name))
        if ignore_this:
            print("......Ignoring '{0}'.".format(cur_file_name))
            ignore_this = False
            continue

        if cur_file_name.endswith(".gbl"):
            print("......Found '{0}'.".format(cur_file_name))
            ignore_this = True
            continue

        if cur_file_name.endswith(".job"):
            print("......Returning '{0}'.".format(cur_file_name))
            return os.path.join(folder_path, cur_file_name), cur_file_name.replace(".job", "")
    return None, None


# ####################################################### CALL ####################################################### #

# load settings
WaitingRoomDef.load_settings()

# open connection and read content
ws_url = WaitingRoomDef.get_ws_list_url()
print("Reading from '{0}'.".format(ws_url))
url_con = urllib.request.urlopen(ws_url)
url_txt = str(url_con.read().decode()).strip()

# download the first
json_obj = json.loads(url_txt)
if len(json_obj) == 0:
    print("No files in the waiting room.")
    quit()
else:
    print("Files in the waiting room: {0}.".format(json_obj))

for cur_file in json_obj:

    # download the file and change its permissions
    cur_file_url = WaitingRoomDef.get_download_file_url(cur_file)
    cur_file_path = os.path.join(WaitingRoomDef.get_download_folder_path(), cur_file)
    urllib.request.urlretrieve(cur_file_url, cur_file_path)
    os.system("chmod ugo+wr {0}".format(cur_file_path))

    # unzip content
    print("Unzipping '{0}'".format(cur_file_path))
    print("  into '{0}'".format(WaitingRoomDef.get_unzip_output_folder_path()))
    os.system("tar -xzvf {0} -C {1}".format(cur_file_path, WaitingRoomDef.get_unzip_output_folder_path()))
    print("Unzipped.")

    # define timestamp, unzip folder and define runset id
    cur_timestamp = cur_file.replace(".tar.gz", "")
    unzipped_folder_path = os.path.join(WaitingRoomDef.get_unzip_output_folder_path(), cur_timestamp)
    runset_job_path, runset_id = get_runset_job(unzipped_folder_path)

    # basic check
    if None in (runset_job_path, runset_id):
        print("Missing Runset id ({0}) or job file ({1})".format(runset_id, runset_job_path))
        exit(1)

    # submitting job for execution
    os_call = "qsub -v runsetid={0},curtimestamp={1} {2}".format(runset_id, cur_timestamp, runset_job_path)
    print("Calling os.system for '{0}').".format(os_call))
    os.system(os_call)
    print("Called os.system .")

    # delete file from server
    cur_del_url = WaitingRoomDef.get_ws_del_url(cur_file)
    print("Calling DELETE '{0}'...".format(cur_del_url))
    requests.delete(cur_del_url)
    print("Called '{0}'.".format(cur_del_url))

    # delete file from local
    print("Deleting '{0}'...".format(cur_file_path))
    os.remove(cur_file_path)
    print("Deleted.")
