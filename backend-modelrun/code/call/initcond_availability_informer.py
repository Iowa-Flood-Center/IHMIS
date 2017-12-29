import urllib.request
import json
import os

# ####################################################### CONS ####################################################### #

settings_file_name = "../../conf/settings.json"
snapshot_file_pref = "state"
snapshot_file_ext = ".h5"

# ####################################################### DEFS ####################################################### #


def load_json_settings(file_name):
    """

    :param file_name:
    :return:
    """
    file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(file_dir, file_name)
    with open(file_path, 'r') as data_file:
        data = json.load(data_file)
    return data


def list_available_files_per_version(all_settings):
    """

    :param all_settings:
    :return: Dictionary with format "asynch_version" -> [filaname1, filename2, ...]
    """

    return_dict = {}

    print("Considering Asynch versions: {0}".format(all_settings['all_asynch_versions']))
    for cur_asynch_ver in all_settings['all_asynch_versions']:
        cur_initcond_dir_path = os.path.join(all_settings['initcond_directory'], cur_asynch_ver)
        cur_hlm_ids = list_all_hlm_ids(cur_initcond_dir_path)
        if cur_hlm_ids is None:
            continue

        print("Considering HLM ids: {0}".format(cur_hlm_ids))

        # get dir path
        if (not os.path.exists(cur_initcond_dir_path)) or (not os.path.isdir(cur_initcond_dir_path)):
            print("Folder not found: '{0}'.".format(cur_initcond_dir_path))
            continue

        # list files
        cur_all_files = os.listdir(cur_initcond_dir_path)
        if len(cur_all_files) == 0:
            print("Folder is empty: '{0}'.".format(cur_initcond_dir_path))
            continue

        # add to dictionary
        if cur_asynch_ver not in return_dict.keys():
            return_dict[cur_asynch_ver] = []

        return_dict[cur_asynch_ver].extend(cur_all_files)

    return return_dict


def list_all_hlm_ids(initcond_repo_folder_path):
    """

    :param initcond_repo_folder_path:
    :return:
    """

    # basic check
    if not os.path.exists(initcond_repo_folder_path):
        print("Missing folder {0}.".format(initcond_repo_folder_path))
        return None

    # explore folder
    return_array = []
    print ("Exploring {0}".format(initcond_repo_folder_path))
    for cur_file_name in os.listdir(initcond_repo_folder_path):
        if cur_file_name.startswith(snapshot_file_pref) and cur_file_name.endswith(snapshot_file_ext):
            return_array.append(int(cur_file_name.split("_")[0].replace(snapshot_file_pref, "")))
    return_array = list(set(return_array))  # remove duplicates
    return return_array


def build_http_args(available_files):
    """

    :param available_files:
    :return: String
    """

    # basich check
    if available_files is None:
        print("NONE available files.")
        return None

    all_strings = []

    for cur_key in available_files.keys():
        # print("Joining '{0}'.".format(available_files[cur_key]))
        cur_strings = ",".join(available_files[cur_key])
        cur_key_arg = cur_key.replace(".", "d")
        all_strings.append("{0}={1}".format(cur_key_arg, cur_strings))

    # basic check
    if len(all_strings) == 0:
        print("String size 0.")
        return None

    return "&".join(all_strings)


def make_http_request(available_files, all_settings):
    """

    :param available_files:
    :return:
    """

    # build http args and check it
    http_args = build_http_args(available_files)
    if http_args is None:
        print("NONE http_args.")
        return

    # perform http call
    sys_call = 'wget {0} --post-data "{1}" -O /dev/null'.format(all_settings['web_service_url'], http_args)
    os.system(sys_call)


# ####################################################### CALL ####################################################### #

the_settings = load_json_settings(settings_file_name)
all_available_files = list_available_files_per_version(the_settings)
make_http_request(all_available_files, the_settings)
print("Done.")
