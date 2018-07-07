import pickle
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.FolderDefinition import FolderDefinition
from libs.ImportInterface import ImportInterface
from libs.DotConstants import DotConstants
from libs.DotWS import DotWS
from libs.Debug import Debug

debug_level_arg = 10

# ################################################# ARGS ################################################# #

model_id_arg = ImportInterface.get_model_id(sys.argv)
timestamp_arg = ImportInterface.get_timestamp(sys.argv)  # useless argument
runset_id_arg = ImportInterface.get_runset_id(sys.argv)

# basic check
if model_id_arg is None:
    Debug.dl("import_stage_forecast_virtualgages_ws: Missing argument for model_id.", 0, debug_level_arg)
    quit()
if runset_id_arg is None:
    Debug.dl("import_stage_forecast_virtualgages_ws: Missing argument for runset_id.", 0, debug_level_arg)
    quit()


# ################################################# DEFS ################################################# #

def update_local_bins_from_webservice(model_id, runset_id, timestamp_arg, debug_lvl=0):
    """

    :param model_id:
    :param runset_id:
    :param timestamp_arg:
    :param debug_lvl:
    :return:
    """

    # 1 - read content of web service
    # 2 - write output file

    # 1
    all_ws_lines = DotWS.get_forecast(model_id, only_forecast=False)
    if all_ws_lines is None:
        return
    ignore_header = True
    in_past = True
    last_elev_obs = {}
    forecast_disct = {}
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
            if cur_obs_elev == -1:
                continue

            cur_obs_timestamp = int(cur_ws_line_split[7])
            if cur_link_id not in last_elev_obs:
                # create new register
                last_elev_obs[cur_link_id] = {
                    "timestamp": cur_obs_timestamp,
                    "obs_elev": cur_obs_elev,
                    "delta_glue": None}
            elif last_elev_obs[cur_link_id]["timestamp"] < cur_obs_timestamp:
                # update old register
                last_elev_obs[cur_link_id]["timestamp"] = cur_obs_timestamp
                last_elev_obs[cur_link_id]["obs_elev"] = cur_obs_elev

            if (timestamp_arg is None) and ((oldest_observation is None) or (oldest_observation < cur_obs_timestamp)):
                oldest_observation = cur_obs_timestamp

            continue

        elif in_past and cur_ws_line_split[6].strip() != "'past'":
            in_past = False

        # getting raw
        cur_mdl_elev = float(cur_ws_line_split[3].strip())
        cur_mdl_timestamp = int(cur_ws_line_split[1].strip())

        # considering delta glue were needed
        if cur_link_id in last_elev_obs:
            if last_elev_obs[cur_link_id]["delta_glue"] is None:
                last_elev_obs[cur_link_id]["delta_glue"] = last_elev_obs[cur_link_id]["obs_elev"] - cur_mdl_elev
            cur_delta_glue = last_elev_obs[cur_link_id]["delta_glue"]
        else:
            cur_delta_glue = 0

        cur_the_elev = cur_mdl_elev + cur_delta_glue

        # adding to dictionary
        if cur_link_id not in forecast_disct:
            forecast_disct[cur_link_id] = []
        forecast_disct[cur_link_id].append([cur_mdl_timestamp, cur_the_elev])

    # 2
    the_timestamp = oldest_observation if timestamp_arg is None else timestamp_arg
    save_binary_file(model_id, runset_id, the_timestamp, forecast_disct, debug_lvl=debug_lvl)

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

    product_id = "fsstg"

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


# ################################################# CALL ################################################# #

update_local_bins_from_webservice(model_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
