import xml.etree.ElementTree
import datetime
import urllib2
import pickle
import time
import sys
import re
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.BinAncillaryDefinition import BinAncillaryDefinition
from libs.FolderDefinition import FolderDefinition
from libs.ImportInterface import ImportInterface
from libs.Debug import Debug

debug_level_arg = 3

# ####################################################### ARGS ####################################################### #

reference_id_arg = "usgsgagesdischclass"
product_id_arg = "isdc"
kml_file_source_url = "http://waterwatch.usgs.gov/index.php?m=real&w=kml&r=us&regions=ia"
force_timestamp = ImportInterface.get_timestamp(sys.argv)
runset_id_arg = ImportInterface.get_runset_id(sys.argv)

# ####################################################### DEFS ####################################################### #


def extract_usgs_id_from_name(namte_txt):
    """

    :param namte_txt:
    :return:
    """

    # 1: remove everything after brackets
    return_txt = re.sub(r'</a>.*', r'', namte_txt)

    # 2: remove everything before brackets
    return_txt = re.sub(r'.*>', r'', return_txt)

    return return_txt


def get_classifications_from_web(kml_url):
    """

    :param kml_url:
    :return: Dictionary in the format of USGS_id -> discharge USGS classification
    """

    usgsid_linkid_file_path = BinAncillaryDefinition.get_usgsid_linkid_file_path()

    http_content = urllib2.urlopen(kml_url).read()

    # read text content and remove namespace to make things easier
    http_content_clean = re.sub(' xmlns="[^"]+"', '', http_content, count=1)
    rootXml = xml.etree.ElementTree.fromstring(http_content_clean)

    # read usgs_id -> link_id dictionary file
    with open(usgsid_linkid_file_path, "rb") as r_file:
        usgsid_linkid = pickle.load(r_file)

    # parse building list of ClassDot objects
    return_dict = {}
    for cur_doc in rootXml.findall('Document'):
        for i, cur_fold in enumerate(cur_doc.findall('Folder')):
            for j, cur_place in enumerate(cur_fold.findall('Placemark')):
                cur_style_url = cur_place.find('styleUrl').text
                cur_point = cur_place.find('Point')
                if (cur_point is None) or (cur_style_url is None):
                    continue
                cur_usgs_id = int(extract_usgs_id_from_name(cur_place.find('name').text))
                cur_point_class = cur_style_url.replace("#icon_", "")
                try:
                    cur_linkid = usgsid_linkid[cur_usgs_id]
                except KeyError:
                    Debug.dl("import_stage_forecast_virtualgages_ws: usgs id not found '{0}'.".format(cur_usgs_id), 1,
                             debug_level_arg)
                    continue
                # print("> {0} -> {1}".format(cur_usgs_id, cur_point_class))
                return_dict[cur_linkid] = int(cur_point_class)
                # return_list.append(ClassDot(cur_usgs_id, cur_point_class))

    return return_dict


def write_binary_file(sc_reference_id, sc_runset_id, sc_product_id, class_dict, forced_timestamp=None, debug_lvl=0):
    """
    Write binary file
    :param sc_reference_id:
    :param sc_product_id:
    :param class_dict: Dictionary in the form of [usgs_id] -> [classification]
    :param forced_timestamp: If None, assumes exact current time.
    :return:
    """

    # define timestamp to be used
    if forced_timestamp is not None:
        eff_timestamp = forced_timestamp
    else:
        raw_datetime = datetime.datetime.fromtimestamp(int(time.time()))
        round_datetime = raw_datetime.replace(minute=0, second=0)
        eff_timestamp = int(time.mktime(round_datetime.timetuple()))

    # create folder if necessary
    folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_reference_id, sc_product_id, sc_runset_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # define file name  # TODO - replace by *.p instead
    file_path = FolderDefinition.get_intermediate_bin_file_path(sc_reference_id, sc_product_id, eff_timestamp,
                                                                runset_id=sc_runset_id)

    with open(file_path, 'wb') as the_file:
        pickle.dump(class_dict, the_file)

    Debug.dl("import_stage_forecast_virtualgages_ws: wroted file '{0}'.".format(file_path), 1, debug_level_arg)


# ####################################################### CALL ####################################################### #

# start counting time for debug
start_time = time.time() if debug_level_arg > 0 else None

# do stuffs
class_dict = get_classifications_from_web(kml_file_source_url)
write_binary_file(reference_id_arg, runset_id_arg, product_id_arg, class_dict,
                  forced_timestamp=force_timestamp, debug_lvl=debug_level_arg)

# debug info
d_time = time.time()-start_time
Debug.dl("import_stage_forecast_virtualgages_ws: main function took {0} seconds.".format(d_time), 1, debug_level_arg)

