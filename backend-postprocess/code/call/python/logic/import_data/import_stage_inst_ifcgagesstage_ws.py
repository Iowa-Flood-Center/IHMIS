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
from libs.Debug import Debug


debug_level_arg = 3

# ####################################################### ARGS ####################################################### #

reference_id_arg = "ifcgagesstage"
timestamp_arg = ImportInterface.get_timestamp(sys.argv)
runset_id_arg = ImportInterface.get_runset_id(sys.argv)

# ####################################################### CONS ####################################################### #

WS_LATEST_URL = "http://ifis.iowafloodcenter.org/ifis/ws/elev_sites.php?format=tab"
WS_LINKID_URL = "http://ifisfe.its.uiowa.edu/ifc/ifis.objects.php?field=foreign_id1,link_id&type=4"

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
        Debug.dl("import_stage_inst_ifcgagesstage_ws:A sc_reference id must be provided.", 1, debug_lvl)
        return
    if sc_runset_id is None:
        Debug.dl("import_stage_inst_ifcgagesstage_ws:A sc_runset_id id must be provided.", 1, debug_lvl)
        return

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    # retrieve raw data
    Debug.dl("import_stage_inst_ifcgagesstage_ws:Accessing '{0}'".format(WS_LATEST_URL), 1, debug_lvl)
    http_content = urllib2.urlopen(WS_LATEST_URL).read()

    # convert into dictionary
    data_dict_ifis = parse_http_content_into_ifis_dict(http_content, debug_lvl=debug_lvl)
    Debug.dl("import_stage_inst_ifcgagesstage_ws:Obtained data for {0} IFC sites.".format(
        len(data_dict_ifis.keys())), 1, debug_lvl)

    # get reference timestamp
    if timestamp is None:
        cur_timestamp_raw = get_current_timestamp_from_dictionary(data_dict_ifis)
    else:
        cur_timestamp_raw = timestamp
    cur_timestamp = GeneralUtils.round_timestamp_hour(cur_timestamp_raw)
    Debug.dl("import_stage_inst_ifcgagesstage_ws:Current time got is {0}, rounded to {1}".format(cur_timestamp_raw,
                                                                                           cur_timestamp),
             1, debug_lvl)

    # get place - linkid relationship
    restrict_srcid_from_all = extract_ifc_gages_srcid_ws(debug_lvl=debug_lvl)

    the_dictionary = {}
    count = 0
    for cur_linkid, cur_src_id in restrict_srcid_from_all.items():

        count += 1

        try:
            obs_timeseries = {
                data_dict_ifis[cur_src_id]["timestamp"]: data_dict_ifis[cur_src_id]["stage"]
            }
        except KeyError:
            continue

        the_dictionary[cur_linkid] = obs_timeseries

    if len(the_dictionary.keys()) == 0:
        Debug.dl("import_stage_inst_ifcgagesstage_ws:no observation was retrieved ", 1, debug_lvl)
        return

    folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_reference_id, "istg",
                                                                    runset_id=sc_runset_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = FolderDefinition.get_intermediate_bin_file_path(sc_reference_id, "istg", cur_timestamp,
                                                                runset_id=sc_runset_id)

    with open(file_path, 'wb') as the_file:
        pickle.dump(the_dictionary, the_file)

    Debug.dl("import_stage_inst_ifcgagesstage_ws:wrote file '{0}'.".format(file_path), 1, debug_level_arg)

    # debug info
    d_time = time.time()-start_time
    Debug.dl("import_stage_inst_ifcgagesstage_ws:main function took {0} seconds ".format(d_time), 1, debug_lvl)

    return


def parse_http_content_into_ifis_dict(http_content, header_tag='#', debug_lvl=0):
    """

    :param http_content:
    :param header_tag:
    :param debug_lvl:
    :return:
    """

    sys_timestamp_max = int(time.time() + (24*60*60))  # max time is current time + 1 day (timezone-safety)
    lines = http_content.split("\n")
    return_dict = {}

    for cur_line in lines:

        # ignore headers
        if (len(cur_line) <= 0) or ((header_tag is not None) and (cur_line.startswith(header_tag))):
            continue

        # split columns
        try:
            cur_cols = cur_line.split("\t")
            cur_ifisid = int(cur_cols[1])
            cur_stage = float(cur_cols[4])
            cur_time_splitted = cur_cols[2].strip()[0:-3]
            cur_datetime = datetime.datetime.strptime(cur_time_splitted, "%Y-%m-%d %H:%M:%S")
            cur_timestamp = int(time.mktime(cur_datetime.timetuple()))
            if cur_timestamp > sys_timestamp_max:
                Debug.dl("import_stage_inst_ifcgagesstage_ws:ignoring line '{0}' (invalid date-time).".format(cur_line),
                         2, debug_lvl)
                continue
            return_dict[cur_ifisid] = {"timestamp": cur_timestamp,
                                       "stage": cur_stage}
        except ValueError:
            continue

    return return_dict


def get_current_timestamp_from_dictionary(ifis_dict):
    """
    Searches for the most recent timestamp available in the database
    :param ifis_dict:
    :return:
    """

    max_timestamp = -1
    for cur_data in ifis_dict.values():
        max_timestamp = cur_data["timestamp"] if cur_data["timestamp"] > max_timestamp else max_timestamp

    return None if max_timestamp == -1 else max_timestamp


def extract_ifc_gages_srcid_ws(header_tag='#', debug_lvl=0):
    """

    :param header_tag:
    :param debug_lvl:
    :return:
    """

    # retrieve raw data
    Debug.dl("import_stage_inst_ifcgagesstage_ws:Accessing '{0}'".format(WS_LINKID_URL), 1, debug_lvl)
    http_content_lines = urllib2.urlopen(WS_LINKID_URL).read().split("\n")

    return_dict = {}
    for cur_line in http_content_lines:
        cur_line_strip = cur_line.strip()
        if len(cur_line_strip) == 0:
            continue
        if (header_tag is not None) and (cur_line_strip.startswith(header_tag)):
            continue
        cur_line_split = cur_line_strip.split('|')
        try:
            cur_linkid = int(cur_line_split[1])
            cur_srcid = int(cur_line_split[0])
            return_dict[cur_linkid] = cur_srcid
        except ValueError:
            continue

    return return_dict

# ####################################################### CALL ####################################################### #

update_local_bins_from_webservice(reference_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)

# print("bingen_ref_usgsgagesstage: EXECUTING THE SCRIPT.")
