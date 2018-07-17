from json import encoder
import shutil
import time
import json
import glob
import sys
import os
import re

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.ReprCombGenInterface import ReprCombGenInterface
from libs.FilenameDefinition import FilenameDefinition
from libs.FolderDefinition import FolderDefinition
from libs.FileDefinition import FileDefinition
from libs.GeneralUtils import GeneralUtils
from libs.Debug import Debug

debug_level_arg = 4

# ####################################################### ARGS ####################################################### #

modelcomb_id_arg = ReprCombGenInterface.get_modelcomb_id(sys.argv)
runset_id_arg = ReprCombGenInterface.get_runset_id(sys.argv)
timestamp_arg = ReprCombGenInterface.get_timestamp(sys.argv)


# ###################################################### CLASS ####################################################### #

class GlobalVar:
    days_past = 10  # replace by 10
    days_fore = 10  # replace by 10
    tinterval = 3600

    def __init__(self):
        return


class JsonLib:

    @staticmethod
    def retrive_most_recent_timestamp_in_hist_folder(folder_path, link_id, debug_lvl=0):
        """

        :param folder_path:
        :param link_id:
        :return:
        """
        Debug.dl("rpcbupd_richhydroforecast: Reading from '{0}'.".format(folder_path), 0, debug_lvl)
        listed_files = sorted(glob.glob(os.path.join(folder_path, "[0-9]*_{0}.json".format(link_id))))
        if len(listed_files) == 0:
            return None
        cur_last_basename = os.path.basename(listed_files[-1])
        return int(cur_last_basename.split("_")[0])

    @staticmethod
    def get_rounded_timestamps(timestamp_min, timestamp_max, interval):
        """

        :param timestamp_min:
        :param timestamp_max:
        :param interval:
        :return:
        """
        return range(GeneralUtils.round_timestamp_hour(timestamp_min),
                     GeneralUtils.round_timestamp_hour(timestamp_max),
                     interval)

    @staticmethod
    def get_all_models_of_frame(runset_id, modelcomb_id, represcomb_id, frame_id, debug_lvl=0):
        """

        :param runset_id:
        :param modelcomb_id:
        :param frame_id:
        :param debug_lvl:
        :return:
        """

        # read file content
        modelcomb_file_path = FileDefinition.obtain_modelcomb_file_path(modelcomb_id, runset_id, debug_lvl=debug_lvl)
        if (modelcomb_file_path is None) or (not os.path.exists(modelcomb_file_path)):
            Debug.dl("rpcbupd_richhydroforecast: File '{0}' not found.".format(modelcomb_file_path), 0, debug_lvl)
            return None
        with open(modelcomb_file_path, "r+") as rfile:
            modelcomb_json = json.load(rfile)
        try:
            represcomb_set = modelcomb_json["sc_modelcombination"]["sc_represcomb_set"]
        except KeyError:
            Debug.dl("rpcbupd_richhydroforecast: File '{0}' is incomplete.".format(modelcomb_file_path), 0, debug_lvl)
            return None

        # search frame
        frame_set = represcomb_set[represcomb_id]
        model_ids = []
        for cur_model_id in frame_set.keys():
            if frame_set[cur_model_id] == frame_id:
                model_ids.append(cur_model_id)

        return model_ids

    @staticmethod
    def find_existing_timestamps(runset_id, modelcomb_id, represcomb_id, frame_id, model_id, link_id, timestamp_min,
                                 timestamp_max, debug_lvl=0):
        """

        :param runset_id:
        :param modelcomb_id:
        :param represcomb_id:
        :param frame_id:
        :param model_id:
        :param timestamp_min:
        :param timestamp_max:
        :param debug_lvl:
        :return:
        """

        rounded_timestamps = JsonLib.get_rounded_timestamps(timestamp_min, timestamp_max, GlobalVar.tinterval)
        folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                           represcomb_id=represcomb_id,
                                                                           frame_id=frame_id,
                                                                           model_id=model_id)

        file_names = FolderDefinition2.retrive_hist_link_files_timestamps(folder_path, link_id, "json",
                                                                          debug_lvl=debug_lvl)

        if file_names is None:
            Debug.dl("rpcbupd_hydrographmultiplespast: Unable to list files at...", 1, debug_lvl)
            Debug.dl("                ...{0}.".format(folder_path), 1, debug_lvl)
            return []

        all_timestamps = []
        for cur_round_time in rounded_timestamps:
            acc_r = (59*60, None)
            cur_closest_timestamp = FolderDefinition2.retrive_closest_timestamp_in_hist_link_folder(file_names,
                                                                                                    cur_round_time,
                                                                                                    accept_range=acc_r,
                                                                                                    modify_all_timestamps=False,
                                                                                                    debug_lvl=debug_lvl)
            if cur_closest_timestamp is None:
                continue

            Debug.dl("rpcbupd_hydrographmultiplespast: Taking {0}.{1} timestamp '{2}'.".format(runset_id,
                                                                                               represcomb_id,
                                                                                               cur_closest_timestamp),
                     5, debug_lvl)

            all_timestamps.append(cur_closest_timestamp)

        if len(all_timestamps) > 1:
            Debug.dl("rpcbupd_hydrographmultiplespast: Got {0} timestamps between {1} and {2}.".format(len(all_timestamps),
                                                                                                       all_timestamps[0],
                                                                                                       all_timestamps[-1]),
                     4, debug_lvl)
        return all_timestamps

    @staticmethod
    def retrive_all_files_in_hist_folder(folder_path, link_id=None, min_timestamp=None, max_timestamp=None,
                                         debug_lvl=0):
        """

        :param folder_path:
        :param link_id:
        :param min_timestamp:
        :param max_timestamp:
        :param debug_lvl:
        :return:
        """
        if link_id is None:
            listed_files = sorted(glob.glob(os.path.join(folder_path, "[0-9]*.h5")))
        else:
            listed_files = sorted(glob.glob(os.path.join(folder_path, "[0-9]*_{0}.json".format(link_id))))
        return_list = []
        for cur_file_path in listed_files:
            cur_basename = os.path.basename(cur_file_path)
            cur_timestamp = int(re.search('^[0-9]+', cur_basename).group(0))
            if (min_timestamp is not None) and (cur_timestamp < min_timestamp):
                Debug.dl("rpcbgen_richhydroforecast: Ignoring '{0}'.".format(cur_basename), 6, debug_lvl)
                continue
            elif (max_timestamp is not None) and (cur_timestamp > max_timestamp):
                Debug.dl("rpcbgen_richhydroforecast: Ignoring '{0}'.".format(cur_basename), 6, debug_lvl)
                continue
            return_list.append(cur_file_path)
        return return_list

    @staticmethod
    def build_observed_timeseries(ref_folder_path, link_id, timestamp_min, timestamp_cur, debug_lvl=0):
        """

        :param ref_folder_path:
        :param link_id:
        :param timestamp_min:
        :param timestamp_cur:
        :return:
        """

        return_timeseries_stg = []
        return_timeseries_dsc = []

        all_file_paths = JsonLib.retrive_all_files_in_hist_folder(ref_folder_path, link_id=link_id,
                                                                  min_timestamp=timestamp_min,
                                                                  max_timestamp=timestamp_cur,
                                                                  debug_lvl=debug_lvl)
        for cur_file_path in all_file_paths:
            Debug.dl("rpcbgen_richhydroforecast: Reading file", 5, debug_lvl)
            Debug.dl("                              {0}.".format(cur_file_path), 5, debug_lvl)

            with open(cur_file_path, "r+") as r_file:
                cur_file_content = json.load(r_file)

            for cur_element in cur_file_content["stage_obs"]:
                return_timeseries_stg.append(cur_element)

            for cur_element in cur_file_content["disch_obs"]:
                return_timeseries_dsc.append(cur_element)

        Debug.dl("rpcbgen_richhydroforecast: Observed timeseries of {0}/{1} elements from {2} files.".format(len(return_timeseries_stg),
                                                                                                             len(return_timeseries_dsc),
                                                                                                             len(all_file_paths)),
                 2, debug_lvl)
        return return_timeseries_stg, return_timeseries_dsc

    @staticmethod
    def save_observed_timeseries_file(dst_folder, timestamp, link_id, obs_stg, obs_dsc, debug_lvl=0):
        """

        :param dst_folder:
        :param timestamp:
        :param link_id:
        :param obs_stg:
        :param obs_dsc:
        :param debug_lvl:
        :return:
        """

        # basic check
        if (len(obs_stg) <= 0) or (len(obs_dsc) <= 0):
            Debug.dl("rpcbgen_richhydroforecast: No observed data for link '{0}'.".format(link_id), 2, debug_lvl)
            return False

        file_name = "{0}_{1}.json".format(timestamp, link_id)
        file_path = os.path.join(dst_folder, file_name)

        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        encoder.FLOAT_REPR = lambda o: format(o, '.2f')
        with open(file_path, "w") as w_file:
            json.dump({"obs_stg": obs_stg, "obs_dsc": obs_dsc},
                      w_file)

        Debug.dl("rpcbgen_richhydroforecast: Wrote file '{0}'.".format(file_path), 2, debug_lvl)

        return True

    @staticmethod
    def save_common_file(src_folder, dst_folder, link_id, debug_lvl=0):
        """

        :param src_folder:
        :param dst_folder:
        :param link_id:
        :param debug_lvl:
        :return:
        """

        file_name = "{0}.json".format(link_id)
        src_file_path = os.path.join(src_folder, file_name)
        dst_file_path = os.path.join(dst_folder, file_name)

        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        shutil.copy(src_file_path, dst_file_path)
        Debug.dl("rpcbgen_richhydroforecast: Wrote file '{0}'.".format(dst_file_path), 2, debug_lvl)

    def __init__(self):
        return


class FolderDefinition2:

    @staticmethod
    def clean_display_folder(repr_folder_path, considered_frames, min_timestamp, link_id, debug_lvl=0):
        # basic check
        if (min_timestamp is None) or (link_id is None):
            return

        count_deleted = 0
        if not os.path.exists(repr_folder_path):
            Debug.dl("rpcbgen_richhydroforecast: Folder '{0}' not found.".format(repr_folder_path), 2, debug_lvl)
            return

        for cur_dir in os.listdir(repr_folder_path):
            cur_dir_path = os.path.join(repr_folder_path, cur_dir)
            if not os.path.isdir(cur_dir_path):
                continue
            elif cur_dir not in considered_frames:
                continue
            for cur_source in os.listdir(cur_dir_path):
                cur_source_path = os.path.join(cur_dir_path, cur_source)
                for cur_file_name in os.listdir(cur_source_path):
                    cur_file_basename_split = os.path.splitext(cur_file_name)[0].split("_")
                    cur_file_timestamp = int(cur_file_basename_split[0])
                    cur_file_linkid = int(cur_file_basename_split[1])
                    if (cur_file_timestamp < min_timestamp) and (cur_file_linkid == link_id):
                        os.remove(os.path.join(cur_source_path, cur_file_name))
                        count_deleted += 1

        Debug.dl("rpcbgen_richhydroforecast: Cleaning deleted {0} files from link {1}.".format(count_deleted, link_id),
                 2, debug_lvl)

    @staticmethod
    def retrive_hist_link_files_timestamps(folder_path, link_id, file_ext, debug_lvl=0):
        """

        :param folder_path: Path historical files (files in historical format)
        :param link_id:
        :param file_ext:
        :param debug_lvl:
        :return:
        """
        the_file_ext = file_ext if not file_ext.startswith(".") else file_ext[1, -1]
        all_file_paths = sorted(glob.glob(os.path.join(folder_path, "[0-9]*_{0}.{1}".format(link_id, the_file_ext))))

        # list all files
        all_file_names = [os.path.basename(f) for f in all_file_paths]
        if (all_file_names is None) or (len(all_file_names) == 0):
            return None

        # get the absolutely closest timestamp
        all_timestamps = []
        for cur_filename in all_file_names:
            tm = FilenameDefinition.obtain_hist_file_timestamp(cur_filename)
            if tm is not None:
                all_timestamps.append(tm)

        if len(all_timestamps) == 0:
            Debug.dl("rpcbupd_hydrographmultiplespast: Nothing from '{0}'.".format(folder_path), 6, debug_lvl)
            return None

        return all_timestamps

    @staticmethod
    def retrive_closest_timestamp_in_hist_link_folder(all_timestamps, ref_timestamp, accept_range=None,
                                                      modify_all_timestamps=True, debug_lvl=0):
        """
        Searches for the file with the closes timestamp value for a given timestamp as reference
        :param all_timestamps: List of file paths in which
        :param ref_timestamp: Reference timestamp
        :param accept_range: If is a list of size two, represent the min/max time distances in sec. If int, abs min/max. If None, no range is evaluated
        :param modify_all_timestamps:
        :param debug_lvl:
        :return: A integer number if found any acceptable file, None otherwise
        """

        # remove after or before if needed
        if modify_all_timestamps:
            if (isinstance(accept_range, list) or isinstance(accept_range, tuple)) and (accept_range[0] is None):
                for cur_idx in range(len(all_timestamps)-1, -1, -1):
                    if all_timestamps[cur_idx] < ref_timestamp:
                        del all_timestamps[cur_idx]
            if (isinstance(accept_range, list) or isinstance(accept_range, tuple)) and (accept_range[1] is None):
                for cur_idx in range(len(all_timestamps)-1, -1, -1):
                    if all_timestamps[cur_idx] > ref_timestamp:
                        del all_timestamps[cur_idx]

        if len(all_timestamps) == 0:
            Debug.dl("rpcbupd_hydrographmultiplespast: No file accepted.", 6, debug_lvl)
            return None

        #
        all_dists = []
        for cur_tm in all_timestamps:
            all_dists.append(abs(cur_tm - ref_timestamp))

        closer_tm_idx = all_dists.index(min(all_dists))
        closer_tm = all_timestamps[closer_tm_idx]

        # evaluate if there is a range of acceptable values
        if accept_range is not None:
            if isinstance(accept_range, list) or isinstance(accept_range, tuple):
                min_value = ref_timestamp - accept_range[0] if accept_range[0] is not None else ref_timestamp
                max_value = ref_timestamp + accept_range[1] if accept_range[1] is not None else ref_timestamp
            elif isinstance(accept_range, int) or isinstance(accept_range, tuple):
                min_value = ref_timestamp - accept_range
                max_value = ref_timestamp + accept_range
            else:
                min_value = max_value = ref_timestamp

            Debug.dl("rpcbupd_richhydroforecast: Closest timestamp {0} must be between {1} and {2}.".format(closer_tm,
                                                                                                            min_value,
                                                                                                            max_value),
                     5, debug_lvl)
            closer_tm = closer_tm if ((closer_tm >= min_value) and (closer_tm <= max_value)) else None

        return closer_tm

    def __init__(self):
        return


# ####################################################### DEFS ####################################################### #

def link_in_ref_folder(link_id, ref_folder_path):
    """

    :param link_id:
    :param ref_folder_path:
    :return:
    """
    all_file_names = os.listdir(ref_folder_path)
    for cur_file_name in all_file_names:
        cur_link_id = FilenameDefinition.obtain_hist_file_linkid(cur_file_name)
        if cur_link_id == link_id:
            return True
    return False

def update_display_files(modelcomb_id, runset_id, timestamp, debug_lvl=0):
    """

    :param modelcomb_id:
    :param runset_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    sc_reprcomp = "richhydroforecast"
    ref0_frame = "stageref"
    stg_frame = "modelforestg"
    link_frame = "common"

    # 0 - set up variables
    fore_model_ids = JsonLib.get_all_models_of_frame(runset_id, modelcomb_id, sc_reprcomp, stg_frame,
                                                     debug_lvl=debug_lvl)
    ref_model_ids = JsonLib.get_all_models_of_frame(runset_id, modelcomb_id, sc_reprcomp, ref0_frame,
                                                    debug_lvl=debug_lvl)
    if (ref_model_ids is None) or (fore_model_ids is None):
        return

    ref_folder_paths = [FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                             represcomb_id=sc_reprcomp,
                                                                             frame_id=ref0_frame,
                                                                             model_id=ref_id)
                        for ref_id in ref_model_ids]

    common_folder_path = FolderDefinition.get_historical_reprcomb_folder_path(runset_id, represcomb_id=sc_reprcomp,
                                                                              frame_id=link_frame)
    if not os.path.exists(common_folder_path):
        Debug.dl("rpcbupd_hydrographmultiplespast: Folder '{0}' not found.".format(common_folder_path), 1, debug_lvl)
        return
    all_link_ids = [int(fn.replace(".json", "")) for fn in os.listdir(common_folder_path)]

    # 1 - delete previous content in display folder
    '''
    Debug.dl("rpcbupd_hydrographmultiplespast: Cleaning '{0}'.".format(cur_modelpaststg_dest_folder_path), 2, debug_lvl)
    if os.path.exists(cur_modelpaststg_dest_folder_path):
        shutil.rmtree(cur_modelpaststg_dest_folder_path)
    '''

    for cur_link_id in all_link_ids:

        Debug.dl("rpcbupd_hydrographmultiplespast: Preparing link '{0}'.".format(cur_link_id), 2, debug_lvl)
        cur_start_time = time.time()

        # 1 - define the reference for this link
        ref_model_id = None
        for i in range(len(ref_folder_paths)):
            if link_in_ref_folder(cur_link_id, ref_folder_paths[i]):
                ref_model_id = ref_model_ids[i]
                ref_folder_path = ref_folder_paths[i]
                break

        if ref_model_id is None:
            continue

        # 2 - define timestamps
        if timestamp is not None:
            timestamp_cur = timestamp
        else:
            timestamp_cur = JsonLib.retrive_most_recent_timestamp_in_hist_folder(ref_folder_path, cur_link_id, debug_lvl)

        if timestamp_cur is None:
            Debug.dl("rpcbupd_hydrographmultiplespast: No hist files for link '{0}'.".format(cur_link_id), 1, debug_lvl)
            continue

        timestamp_min = timestamp_cur - (GlobalVar.days_past * 24 * 60 * 60)
        timestamp_max = timestamp_cur + (GlobalVar.days_fore * 24 * 60 * 60)

        # 3 - build observed timeseries
        cur_time_mark = time.time()
        cur_observ_timeseries_stg, cur_observ_timeseries_dsc = JsonLib.build_observed_timeseries(ref_folder_path,
                                                                                                 cur_link_id,
                                                                                                 timestamp_min,
                                                                                                 timestamp_cur,
                                                                                                 debug_lvl=debug_lvl)

        FolderDefinition2.clean_display_folder(FolderDefinition.get_displayed_reprcomb_folder_path(runset_id,
                                                                                                   modelcomb_id,
                                                                                                   represcomb_id=sc_reprcomp),
                                               (ref0_frame, stg_frame), timestamp_min, cur_link_id, debug_lvl=debug_lvl)

        cur_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(runset_id, modelcomb_id,
                                                                                   represcomb_id=sc_reprcomp,
                                                                                   frame_id=ref0_frame,
                                                                                   model_id=ref_model_id)

        cur_d_time = time.time() - cur_time_mark
        Debug.dl("rpcbupd_hydrographmultiplespast: Total time for getting obs timeseries: {0}.".format(cur_d_time), 3,
                 debug_lvl)
        cur_time_mark = time.time()
        cur_save = JsonLib.save_observed_timeseries_file(cur_dest_folder_path, timestamp_cur, cur_link_id,
                                                         cur_observ_timeseries_stg, cur_observ_timeseries_dsc,
                                                         debug_lvl=debug_lvl)
        cur_d_time = time.time() - cur_time_mark
        Debug.dl("rpcbupd_hydrographmultiplespast: Total time for writing obs timeseries: {0}.".format(cur_d_time), 3,
                 debug_lvl)

        if not cur_save:
            continue

        cur_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(runset_id, modelcomb_id,
                                                                                   represcomb_id=sc_reprcomp,
                                                                                   frame_id="common")
        JsonLib.save_common_file(common_folder_path, cur_dest_folder_path, cur_link_id, debug_lvl=debug_lvl)

        # 4 - capture all forecasts between the interval and copy the files
        count_copy = 0
        for cur_fore_model_id in fore_model_ids:
            Debug.dl("rpcbupd_hydrographmultiplespast: Getting forecasts of {0} for link '{1}'.".format(
                cur_fore_model_id, cur_link_id), 5, debug_lvl)

            cur_time_mark = time.time()

            # finding forecast files to be copyed
            cur_model_folder = FolderDefinition.get_historical_reprcomb_folder_path(runset_id,
                                                                                    represcomb_id=sc_reprcomp,
                                                                                    frame_id=stg_frame,
                                                                                    model_id=cur_fore_model_id)

            Debug.dl("rpcbupd_hydrographmultiplespast: Exploring folder {0}.".format(cur_model_folder), 5, debug_lvl)
            all_considered_timestamps = JsonLib.find_existing_timestamps(runset_id, modelcomb_id, sc_reprcomp,
                                                                         stg_frame, cur_fore_model_id, cur_link_id,
                                                                         timestamp_min, timestamp_max,
                                                                         debug_lvl=debug_lvl)

            cur_d_time = time.time() - cur_time_mark
            Debug.dl("rpcbupd_hydrographmultiplespast: Total time to find existing timestamps of link {0}: {1}.".format(
                cur_d_time, cur_link_id), 3, debug_lvl)

            if (all_considered_timestamps is None) or (len(all_considered_timestamps) == 0):
                Debug.dl("rpcbupd_hydrographmultiplespast: No {0}{1} forecast for link {2}.".format(runset_id,
                                                                                                    cur_fore_model_id,
                                                                                                    cur_link_id), 5,
                         debug_lvl)
                continue

            # copying files
            cur_dest_folder_path = FolderDefinition.get_displayed_reprcomb_folder_path(runset_id, modelcomb_id,
                                                                                       represcomb_id=sc_reprcomp,
                                                                                       frame_id=stg_frame,
                                                                                       model_id=cur_fore_model_id)
            if not os.path.exists(cur_dest_folder_path):
                os.makedirs(cur_dest_folder_path)
            for cur_considered_timestamp in all_considered_timestamps:
                cur_file_name = "{0}_{1}.json".format(cur_considered_timestamp, cur_link_id)
                dst_file_path = os.path.join(cur_dest_folder_path, cur_file_name)
                if os.path.exists(dst_file_path):
                    continue
                org_file_path = os.path.join(cur_model_folder, cur_file_name)
                shutil.copy(org_file_path, dst_file_path)
                count_copy += 1
                Debug.dl("rpcbupd_hydrographmultiplespast: Created {0}.".format(dst_file_path), 5, debug_lvl)
            Debug.dl("rpcbupd_hydrographmultiplespast: Copied {0} out of {1} forecast files for link {2}, model {3}.{4} between {5} and {6}.".format(
                count_copy, len(all_considered_timestamps), cur_link_id, runset_id, cur_fore_model_id,
                all_considered_timestamps[0], all_considered_timestamps[-1]), 4, debug_lvl)

            # debug time
            cur_d_time = time.time() - cur_time_mark
            Debug.dl("rpcbupd_hydrographmultiplespast: Total time for getting {0}.{1} forecasts link {2}: {3}.".format(
                runset_id, cur_fore_model_id, cur_link_id, cur_d_time), 3, debug_lvl)

        # debug time
        cur_d_time = time.time() - cur_start_time
        Debug.dl("rpcbupd_hydrographmultiplespast: Total time for link {0}: {1}.".format(cur_link_id, cur_d_time), 3,
                 debug_lvl)

    Debug.dl("rpcbupd_hydrographmultiplespast: Finished.", 2, debug_lvl)

# ####################################################### CALL ####################################################### #

update_display_files(modelcomb_id_arg, runset_id_arg, timestamp_arg, debug_lvl=debug_level_arg)
