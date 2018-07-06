import datetime
import urllib2
import pickle
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.FolderDefinition import FolderDefinition
from libs.ImportInterface import ImportInterface
from libs.GeneralUtils import GeneralUtils
from libs.Settings import Settings
from libs.Debug import Debug

debug_level_arg = 3

# ####################################################### ARGS ####################################################### #

reference_id_arg = "usgsgagesstage"
timestamp_arg = ImportInterface.get_timestamp(sys.argv)
runset_id_arg = ImportInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def update_local_bins_from_webservice(sc_reference_id, sc_runset_id, timestamp=None, debug_lvl=0):
    """
    Reads the data from database and generates binary files for given hydro-forecasts
    :param sc_reference_id:
    :param sc_runset_id:
    :param timestamp: If None, retrieves the most recent hydro-forecasts available
    :param debug_lvl:
    :return: None. Changes are perform at file system level
    """

    # basic check
    if sc_reference_id is None:
        Debug.dl("import_stage_inst_usgsgagesref_ws: A sc_reference id must be provided.", 1, debug_lvl)
        return
    if sc_runset_id is None:
        Debug.dl("import_stage_inst_usgsgagesref_ws: A sc_runset_id id must be provided.", 1, debug_lvl)
        return

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # retrieve raw data
    ws_url = "http://ifisfe.its.uiowa.edu/ifc/ifis.observations.php?field=ifis_id,foreign_id,foreign_id1,stage_depth,timestamp"
    Debug.dl("import_stage_inst_usgsgagesref_ws: Accessing '{0}'".format(ws_url), 1, debug_lvl)
    http_content = urllib2.urlopen(ws_url).read()

    # convert into dictionary
    data_dict_ifis = parse_http_content_into_ifis_dict(http_content, header=True, debug_lvl=debug_lvl)

    # get reference timestamp
    cur_timestamp_raw = get_current_timestamp_from_dictionary(data_dict_ifis, debug_lvl=debug_lvl) if timestamp is None else timestamp
    cur_timestamp = GeneralUtils.round_timestamp_hour(cur_timestamp_raw)
    Debug.dl("import_stage_inst_usgsgagesref_ws: Current time got is {0}, rounded to {1}".format(cur_timestamp_raw,
                                                                                            cur_timestamp),
             1, debug_lvl)

    # load ancillary dictionaries
    linkid_poisid_dict = get_linkid_poisid_relationship_fs(debug_lvl=debug_lvl)
    linkid_poistype_dict = get_linkid_poistype_relationship_fs(debug_lvl=debug_lvl)
    linkid_poisall_dict = get_linkid_poisall_relationship_fs(debug_lvl=debug_lvl)

    #
    restrict_poisid = extract_usgs_gages_poisid(linkid_poisid_dict, linkid_poistype_dict)
    restrict_poisid_from_all = extract_usgs_gages_poisid_from_all(linkid_poisall_dict)

    Debug.dl("import_stage_inst_usgsgagesref_ws: Will restrict to {0} pois.".format(len(restrict_poisid.values())), 1, debug_lvl)

    the_dictionary = {}
    count = 0
    total = len(restrict_poisid_from_all.keys())
    for cur_linkid in restrict_poisid_from_all.keys():

        cur_pois_id = restrict_poisid_from_all[cur_linkid]

        count += 1
        Debug.dl("import_stage_inst_usgsgagesref_ws: linkid={0}, poisid={1}, {2}/{3}.".format(cur_linkid, cur_pois_id,
                                                                                         count, total), 4, debug_lvl)

        obs_timeseries = {data_dict_ifis[cur_pois_id]["timestamp"]: data_dict_ifis[cur_pois_id]["stage"]}

        the_dictionary[cur_linkid] = obs_timeseries

    if len(the_dictionary.keys()) == 0:
        Debug.dl("import_stage_inst_usgsgagesref_ws: no observation was retrieved ", 1, debug_lvl)
        return

    folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_reference_id, "istg", runset_id=sc_runset_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = FolderDefinition.get_intermediate_bin_file_path(sc_reference_id, "istg", cur_timestamp,
                                                                runset_id=sc_runset_id)

    with open(file_path, 'wb') as the_file:
        pickle.dump(the_dictionary, the_file)

    Debug.dl("import_stage_inst_usgsgagesref_ws: wrote file '{0}'.".format(file_path), 1, debug_level_arg)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("import_stage_inst_usgsgagesref_ws: main function took {0} seconds ".format(d_time), 1, debug_lvl)

    return


def parse_http_content_into_ifis_dict(http_content, header=True, debug_lvl=0):
    """

    :param http_content:
    :param header:
    :param debug_lvl:
    :return:
    """

    sys_timestamp_max = int(time.time() + (24*60*60))  # max time is current time + 1 day (timezone-safety)
    lines = http_content.split("\n")
    read_header = False if header else True
    return_dict = {}

    for cur_line in lines:

        # ignore header
        if not read_header:
            read_header = True
            continue

        # split columns
        try:
            cur_cols = cur_line.split("|")
            cur_ifisid = int(cur_cols[0])
            cur_stage = float(cur_cols[3])
            cur_time_splitted = cur_cols[4][0:-3]
            cur_datetime = datetime.datetime.strptime(cur_time_splitted, "%Y-%m-%d %H:%M:%S")
            cur_timestamp = int(time.mktime(cur_datetime.timetuple()))
            if cur_timestamp > sys_timestamp_max:
                Debug.dl("import_stage_inst_usgsgagesref_ws: ignoring line '{0}' (invalid date-time).".format(cur_line),
                         2, debug_lvl)
                continue
            return_dict[cur_ifisid] = {"timestamp": cur_timestamp,
                                       "stage": cur_stage}
        except ValueError:
            continue

    return return_dict


def get_current_timestamp_from_dictionary(ifis_dict, debug_lvl=0):
    """
    Searches for the most recent timestamp available in the database
    :param ifis_dict:
    :param debug_lvl:
    :return:
    """

    max_timestamp = -1
    for cur_data in ifis_dict.values():
        max_timestamp = cur_data["timestamp"] if cur_data["timestamp"] > max_timestamp else max_timestamp

    return None if max_timestamp == -1 else max_timestamp


def get_observed_data_db(db_conn, table_name, poisid_constrain=None, debug_lvl=0):
    """

    :param db_conn: Connection to observed database
    :param table_name:
    :param poisid_constrain:
    :param debug_lvl:
    :return:
    """

    poisid_constrain_str = [str(cur_id) for cur_id in poisid_constrain] if poisid_constrain is not None else None
    subquery_ifisid = "" if poisid_constrain is None else "AND ifis_id IN ({0}) ".format(",".join(poisid_constrain_str))
    query_sel = "SELECT ifis_id, extract(epoch from date), stage_depth " \
                "FROM {0} " \
                "WHERE date IS NOT NULL {1} AND forecast = FALSE " \
                "ORDER BY ifis_id, date".format(table_name, subquery_ifisid)

    # print(query_sel)

    cur_cursor = db_conn.cursor()
    cur_cursor.execute(query_sel)
    all_obs = cur_cursor.fetchall()
    cur_cursor.close()

    return all_obs


def extract_specific_observed_timeseries(all_obs_timeseries, pois_id, debug_lvl=0):
    """

    :param all_obs_timeseries:
    :param pois_id:
    :param debug_lvl:
    :return: Dictionary containing time -> stage
    """

    ret_dict = {}
    for cur_obs_tuple in all_obs_timeseries:
        if cur_obs_tuple[0] == pois_id:
            ret_dict[int(cur_obs_tuple[1])] = cur_obs_tuple[2]

    return ret_dict


def get_linkid_poisid_relationship_fs(debug_lvl=0):
    """

    :param debug_lvl:
    :return:
    """

    raw_folder_path = Settings.get("raw_data_folder_path")
    file_path = os.path.join(raw_folder_path, "anci", "pois", "links_pois.p")

    if not os.path.exists(file_path):
        Debug.dl("import_stage_inst_usgsgagesref_ws: File '{0}' not found.".format(file_path), 0, debug_lvl)
        return

    with open(file_path, "rb") as r_file:
        return_dict = pickle.load(r_file)

    return return_dict


def get_linkid_poistype_relationship_fs(debug_lvl=0):
    """

    :param debug_lvl:
    :return:
    """

    raw_folder_path = Settings.get("raw_data_folder_path")
    file_path = os.path.join(raw_folder_path, "anci", "pois", "links_pois_type.p")

    if not os.path.exists(file_path):
        Debug.dl("import_stage_inst_usgsgagesref_ws: File '{0}' not found.".format(file_path), 0, debug_lvl)
        return

    with open(file_path, "rb") as r_file:
        return_dict = pickle.load(r_file)

    return return_dict


def get_linkid_poisall_relationship_fs(debug_lvl=0):
    """

    :param debug_lvl:
    :return:
    """

    raw_folder_path = Settings.get("raw_data_folder_path")
    file_path = os.path.join(raw_folder_path, "anci", "pois", "links_pois_all.p")

    if not os.path.exists(file_path):
        Debug.dl("import_stage_inst_usgsgagesref_ws: File '{0}' not found.".format(file_path), 0, debug_lvl)
        return

    with open(file_path, "rb") as r_file:
        return_dict = pickle.load(r_file)

    return return_dict


def extract_usgs_gages_poisid(link_poisid_dict, link_poistype_dict):
    """

    :param link_poisid_dict:
    :param link_poistype_dict:
    :return:
    """

    return_dict = {}
    for cur_linkid in link_poisid_dict.keys():
        if (link_poistype_dict[cur_linkid] == 2) or (link_poistype_dict[cur_linkid] == 3):
            return_dict[cur_linkid]= link_poisid_dict[cur_linkid]

    return return_dict


def extract_usgs_gages_poisid_from_all(link_poisall_dict):
    """

    :param link_poisid_dict:
    :param link_poistype_dict:
    :return:
    """

    return_dict = {}
    for cur_linkid in link_poisall_dict.keys():

        if 2 in link_poisall_dict[cur_linkid]:
            return_dict[cur_linkid] = link_poisall_dict[cur_linkid][2]["id"]
        if 3 in link_poisall_dict[cur_linkid]:
            return_dict[cur_linkid] = link_poisall_dict[cur_linkid][3]["id"]

    return return_dict

# ####################################################### CALL ####################################################### #

update_local_bins_from_webservice(reference_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
