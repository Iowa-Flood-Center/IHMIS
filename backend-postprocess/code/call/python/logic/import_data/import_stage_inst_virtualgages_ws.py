import pickle
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.SettingsVirtualGages import SettingsVirtualGages
from libs.FolderDefinition import FolderDefinition
from libs.ImportInterface import ImportInterface
from libs.DotConstants import DotConstants
from libs.DotWS import DotWS
from libs.Debug import Debug

debug_level_arg = 10

# ####################################################### ARGS ####################################################### #

model_id_arg = ImportInterface.get_model_id(sys.argv)
timestamp_arg = ImportInterface.get_timestamp(sys.argv)  # useless argument
runset_id_arg = ImportInterface.get_runset_id(sys.argv)

# basic check
if model_id_arg is None:
    Debug.dl("import_stage_inst_virtualgages_ws: Missing argument for model_id.", 0, debug_level_arg)
    quit()
if runset_id_arg is None:
    Debug.dl("import_stage_forecast_virtualgages_ws: Missing argument for runset_id.", 0, debug_level_arg)
    quit()


# ####################################################### DEFS ####################################################### #

def update_local_bins_from_webservice(model_id, runset_id, timestamp_arg, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param timestamp_arg:
    :param debug_lvl:
    :return:
    """

    # 0 - check inputs
    # 1 - read content of web service
    # 2 - write output file

    # 0
    supported_mdl = SettingsVirtualGages.get("sc_models_instant")
    supported_ref = SettingsVirtualGages.get("sc_references")
    if (model_id not in supported_mdl) and (model_id not in supported_ref):
        Debug.dl("import_stage_forecast_virtualgages_ws: Model id {0} not among supported models ({1}) or refs ({2}).".format(model_id,
                                                                                                         supported_mdl,
                                                                                                         supported_ref),
                 0, debug_level_arg)
        return

    # 1
    all_ws_lines = DotWS.get_forecast(model_id, only_forecast=False)
    if all_ws_lines is None:
        return
    ignore_header = True
    in_past = True
    last_elev_obs = {}
    oldest_observation = None
    for cur_ws_line in all_ws_lines:

        # ignore header
        if ignore_header:
            ignore_header = False
            continue

        # split and basic check for size
        cur_ws_line_split = cur_ws_line.split(",")
        if len(cur_ws_line_split) < 11:
            continue

        cur_link_id = int(cur_ws_line_split[10])  # TODO - make a more intelligent index tracker

        # basic check - no link_id, no game
        if cur_link_id == -1:
            continue

        if in_past and cur_ws_line_split[6].strip() == "'past'":
            # only considers observed
            cur_obs_elev = float(cur_ws_line_split[9].strip())
            cur_mdl_elev = float(cur_ws_line_split[3].strip())
            # cur_elev = cur_obs_elev if cur_obs_elev != -1 else cur_mdl_elev
            if model_id in supported_mdl:
                cur_elev = cur_mdl_elev
            elif model_id in supported_ref:
                if cur_obs_elev == -1:
                    continue
                cur_elev = cur_obs_elev
            else:
                Debug.dl("import_stage_forecast_virtualgages_ws: We have a Sherlock Homes here ({0}).".format(model_id), 0, debug_level_arg)
                cur_elev = 0
            oldest_observation = int(cur_ws_line_split[7])
            last_elev_obs[cur_link_id] = cur_elev
            continue

        elif in_past and cur_ws_line_split[6].strip() != "'past'":
            break

    # 2
    the_timestamp = oldest_observation if timestamp_arg is None else timestamp_arg
    save_binary_file(model_id, runset_id, the_timestamp, last_elev_obs, debug_lvl=debug_lvl)

    Debug.dl("import_stage_forecast_virtualgages_ws: Done for {0}.{1}.".format(runset_id, model_id), 1, debug_lvl)


def save_binary_file(model_id, runset_id, timestamp, hydroforecast_dictionary, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param timestamp:
    :param hydroforecast_dictionary:
    :param debug_lvl:
    :return:
    """

    product_id = "istg"

    # basic check
    if hydroforecast_dictionary is None:
        return

    bin_file_path = FolderDefinition.get_intermediate_bin_file_path(model_id, product_id, timestamp,
                                                                    runset_id=runset_id)

    # create folder if necessary
    bin_folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id, product_id, runset_id=runset_id)
    if not os.path.exists(bin_folder_path):
        os.makedirs(bin_folder_path)

    Debug.dl("import_stage_forecast_virtualgages_ws: Saving '{0}' file.".format(bin_file_path), 2, debug_lvl)
    with open(bin_file_path, "wb") as w_file:
        pickle.dump(hydroforecast_dictionary, w_file)

    Debug.dl("import_stage_forecast_virtualgages_ws: Binary file saved: '{0}'.".format(bin_file_path), 1, debug_lvl)

    return

# ####################################################### CALL ####################################################### #

update_local_bins_from_webservice(model_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
