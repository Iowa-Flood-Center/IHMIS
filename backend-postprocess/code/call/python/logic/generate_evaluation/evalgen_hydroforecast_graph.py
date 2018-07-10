import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pylab as pylab
import datetime
import pickle
import math
import time
import sys
import os

sys.path.append("{0}/..".format(os.path.dirname(os.path.realpath(__file__))))
from libs.Interpolate import Interpolate
from libs.BinAncillaryDefinition import BinAncillaryDefinition
from libs.EvalGenInterface import EvalGenInterface
from libs.FolderDefinition import FolderDefinition
from libs.FileDefinition import FileDefinition
from libs.Hydrographs import Hydrographs
from libs.Debug import Debug


debug_level_arg = 3
previous_days_arg = 10

sc_reference_id_default = "usgsgagesstage"

# ####################################################### ARGS ####################################################### #

model_id_arg = EvalGenInterface.get_model_id(sys.argv)
timestamp_arg = EvalGenInterface.get_timestamp(sys.argv)
reference_id_arg = EvalGenInterface.get_reference_id(sys.argv, default_val=sc_reference_id_default)
runset_id_arg = EvalGenInterface.get_runset_id(sys.argv)

########################################################################################################################
# ####################################################### DEFS ####################################################### #
########################################################################################################################

# ##################################################### DEFS - DB #################################################### #


def get_observed_data_fs(sc_reference_id, sc_runset_id, cur_timestamp, debug_lvl=0):
    """

    :param sc_reference_id:
    :param sc_runset_id:
    :param cur_timestamp:
    :param debug_lvl:
    :return:
    """

    sc_product_id = 'istg'

    # try to match perfectly the given time (that is given or that comes from the last model result)

    file_path = FolderDefinition.get_intermediate_bin_file_path(sc_reference_id, sc_product_id, cur_timestamp,
                                                                runset_id=sc_runset_id)

    # if file was not found, search for the closest one
    if not os.path.exists(file_path):

        folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_reference_id, sc_product_id,
                                                                        runset_id=sc_runset_id)
        closest_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(folder_path, cur_timestamp)

        Debug.dl("evalgen_hydroforecast_graph: Closest observed timestamp for {0} is {1}.".format(cur_timestamp,
                                                                                                  closest_timestamp),
                 2, debug_lvl)

        # check if found any
        if closest_timestamp is None:
            return None

        file_path = FolderDefinition.get_intermediate_bin_file_path(sc_reference_id, sc_product_id, closest_timestamp,
                                                                    runset_id=sc_runset_id)

    # read chosen file
    with open(file_path, "rb") as the_file:
        the_content = pickle.load(the_file)

    return the_content

# ##################################################### DEFS - FS #################################################### #


def get_linkid_poisid_relationship_fs(debug_lvl=0):
    """

    :param debug_lvl:
    :return:
    """

    file_path = BinAncillaryDefinition.get_bin_pois_file_path("links_pois.p")

    if not os.path.exists(file_path):
        Debug.dl("evalgen_hydroforecast_graph.py: File '{0}' not found.".format(file_path), 0, debug_lvl)
        return

    with open(file_path, "rb") as r_file:
        return_dict = pickle.load(r_file)

    return return_dict


def get_set_of_hydroforecasts(model_id, runset_id, min_timestamp, max_timestamp, max_num_files, debug_lvl=0):
    """
    Read all relevant binary hydroforecast files and creates a dictionary with its contents
    :param model_id:
    :param runset_id:
    :param min_timestamp:
    :param max_timestamp:
    :param max_num_files:
    :param debug_lvl:
    :return:
    """

    sc_product_id = "fq"

    folder_path = FolderDefinition.get_intermediate_bin_folder_path(model_id=model_id, product_id=sc_product_id,
                                                                    runset_id=runset_id)

    # list all files
    all_files_name = os.listdir(folder_path)

    # get all filenames inside given interval
    all_timestamps = []
    for cur_file_name in all_files_name:
        cur_timestamp = FileDefinition.obtain_hist_file_timestamp(cur_file_name)
        if min_timestamp <= cur_timestamp <= max_timestamp:
            all_timestamps.append(cur_timestamp)

    # removing extra files
    all_timestamps.sort()
    if len(all_timestamps) <= max_num_files:
        considered_timestamps = all_timestamps
    else:
        index_step = len(all_timestamps)/(max_num_files - 1)
        count_elements = 0
        considered_timestamps = []
        while count_elements < max_num_files:
            cur_idx = int(round(index_step * count_elements))
            try:
                considered_timestamps.append(all_timestamps[cur_idx])
            except IndexError:
                Debug.dl("evalgen_hydroforecast_graph: Skip adding index {0} out of {1} hydrographs.".format(cur_idx,
                                                                                                             len(all_timestamps)),
                         3, debug_lvl)
            count_elements += 1

        # ensure the last one is included
        considered_timestamps.append(all_timestamps[-1])

    # debug it
    Debug.dl("evalgen_hydroforecast_graph: Found {0} files in folder '{1}' between {2} and {3}.".format(
        len(all_timestamps), folder_path, min_timestamp, max_timestamp), 2, debug_lvl)
    Debug.dl("evalgen_hydroforecast_graph: Reduced to {0} files only.".format(len(considered_timestamps)), 2, debug_lvl)

    # read each considered file
    return_dict = {}
    for cur_considered_timestamp in considered_timestamps:
        cur_considered_filepath = FolderDefinition.get_intermediate_bin_file_path(model_id, sc_product_id,
                                                                                  cur_considered_timestamp,
                                                                                  runset_id=runset_id)
        with open(cur_considered_filepath, "rb") as cur_file:
            # print("Reading {0} into {1}.".format(cur_considered_filepath, cur_considered_timestamp))
            try:
                return_dict[cur_considered_timestamp] = pickle.load(cur_file)
            except EOFError:
                Debug.dl("evalgen_hydroforecast_graph: EOFerror while reading {0} file.".format(cur_considered_filepath),
                         0, debug_lvl)

    return return_dict


def extract_specific_disch_stage_fs(the_rc):

    all_disch = []
    all_stage = []
    for cur_rc_elem in the_rc:
        all_disch.append(cur_rc_elem[1])
        all_stage.append(cur_rc_elem[0])

    # print("Stage: {0}".format(all_stage))
    # print("Disch: {0}".format(all_disch))

    return all_disch, all_stage

# #################################################### DEFS - ALL #################################################### #


def extract_specific_threshold_set(all_threshols, ifis_if, debug_lvl=0):
    """

    :param all_threshols:
    :param ifis_if:
    :param debug_lvl:
    :return: List of size 5 with distance to bottom, action, ..., major
    """
    for cur_threshold_tuble in all_threshols:
        if ifis_if == cur_threshold_tuble[0]:
            return cur_threshold_tuble[1:6]
        elif ifis_if < cur_threshold_tuble[0]:
            Debug.dl("evalgen_hydroforecast_graph: Thresholds not found for ifis_id: {0}.".format(ifis_if), debug_lvl, 1)
            return None


def extract_specific_observed_timeseries(all_obs_timeseries, ifis_id, debug_lvl=0):
    """

    :param all_obs_timeseries:
    :param ifis_id:
    :param debug_lvl:
    :return: Dictionary containing time -> stage
    """

    ret_dict = {}
    for cur_obs_tuple in all_obs_timeseries:
        if cur_obs_tuple[0] == ifis_id:
            ret_dict[int(cur_obs_tuple[1])] = cur_obs_tuple[2]

    return ret_dict


def get_min_max_timestamps(dict_timeseries, histogram_lenght=10):
    """
    Gets the minimum and maximum data timestamp expected
    :param dict_timeseries: Timeseries dictionary in the format ["forecast timestamp"] -> data
    :param histogram_lenght: How long each histogram goes on in time (in days)
    :return: A tuple of size three with: minimum forecast time, last forecast time, maximum forecast data time
    """

    all_fortimes = [int(float(key)) for key in dict_timeseries.keys()]
    min_fortime = min(all_fortimes)
    last_fortime = max(all_fortimes)  # 10 days of forecast
    max_fortime = last_fortime + (histogram_lenght * 24 * 3600)

    return min_fortime, last_fortime, max_fortime


def to_hex(num):
    """
    Convert number in range [0 ~ 15] to [0 ~ 'f']
    :param num: Integer 0 to 15
    :return: A string in range [0 ~ 'f'] if possible conversion, None otherwise
    """
    if 0 <= num <= 9:
        return str(num)
    elif num == 10:
        return 'a'
    elif num == 11:
        return 'b'
    elif num == 12:
        return 'c'
    elif num == 13:
        return 'd'
    elif num == 14:
        return 'e'
    elif num == 15:
        return 'f'
    else:
        return None


def get_color_from_index(the_idx, max_idx):
    """
    Defines a color code for given index of forecast hydrograph
    :param the_idx: Index of forecast hydrograph
    :return: A color code in the format #rrggbb
    """

    # basic check
    if max_idx == 0:
        return None

    # defines a "real index value" between 0 and 45
    real_idx = int((the_idx * 30) / max_idx) if the_idx <= max_idx else max_idx

    # defines a color from the "real index value"
    if real_idx <= 15:
        r = to_hex(real_idx)
        g = to_hex(15)
        b = to_hex(0)
    elif real_idx < 30:
        r = to_hex(15)
        g = to_hex(30 - real_idx)
        b = to_hex(0)
    else:
        r = to_hex(15)
        g = to_hex(0)
        b = to_hex(real_idx - 30)
    # print("{0}: Returning color {1}, {2}, {3}".format(real_idx, r, g, b))
    return "#{0}{0}{1}{1}{2}{2}".format(r, g, b)


def the_plot(dict_timeseries_mdl, dict_timeseries_obs, dict_timeseries_thr, model_id, link_id, timestamp,
             sc_reference_id, runset_id, pois_description=None, upstream_area=None, debug_lvl=0):
    """
    Plots
    :param dict_timeseries_mdl:
    :param dict_timeseries_obs:
    :param dict_timeseries_thr:
    :param model_id:
    :param link_id:
    :param timestamp:
    :param sc_reference_id:
    :param debug_lvl:
    :return: True if the plot was performed, False otherwise.
    """

    try:
        min_fortime, last_fortime, max_fortime = get_min_max_timestamps(dict_timeseries_mdl)
    except ValueError:
        Debug.dl("evalgen_hydroforecast_graph: Observed timeseris is empty for link id {0}.".format(link_id), 2,
                 debug_lvl)
        return False

    num_days = int(math.ceil((max_fortime - min_fortime)/(3600*24)))

    # create array of dates in x-axis
    min_fordate = datetime.datetime.fromtimestamp(min_fortime)
    last_fordate = datetime.datetime.fromtimestamp(last_fortime)
    dateList = []
    for x in range(0, num_days + 1):
        tmp = min_fordate + datetime.timedelta(days=x)
        dateList.append(tmp)

    # establish minimum/maximum y values to be used in the axis
    max_y = 0
    min_y = 100000
    for cur_forttimeseries in dict_timeseries_mdl.values():
        for cur_value in cur_forttimeseries:
            max_y = cur_value[1] if cur_value[1] > max_y else max_y
            min_y = cur_value[1] if cur_value[1] < min_y else min_y
    if dict_timeseries_obs is not None:
        for cur_obs_value in dict_timeseries_obs.values():
            cur_test = cur_obs_value * 0.0833333
            max_y = cur_test if cur_test > max_y else max_y
            min_y = cur_test if cur_test < min_y else min_y
    try:
        test = (dict_timeseries_thr[4] - dict_timeseries_thr[0])*0.0833333
        max_y = test if test > max_y else max_y
    except TypeError:
        max_y = max_y
    try:
        test = (dict_timeseries_thr[1] - dict_timeseries_thr[0])*0.0833333
        min_y = test if test < min_y else min_y
    except TypeError:
        min_y = min_y

    min_y = min_y if min_y is not None else 0
    delta_y = (max_y - min_y)*0.1
    max_y += delta_y
    min_y = max(((min_y - delta_y), 0))

    # establish image size
    params = {'figure.figsize': (15, 5)}
    pylab.rcParams.update(params)

    # define the axis
    fig, ax = plt.subplots()

    pylab.ylim(ymin=min_y, ymax=max_y)

    # set array parameters
    ax.set_xlim(dateList[0], dateList[-1])

    # make ticks daily
    days = mdates.DayLocator()
    ax.xaxis.set_major_locator(days)

    # format dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b.\n%d'))
    fig.autofmt_xdate()
    plt.xticks(rotation='horizontal')

    # center align dates with ticks
    for label in ax.xaxis.get_ticklabels():
        label.set_horizontalalignment('center')

    # plot forecaster lines first
    all_fortimes = dict_timeseries_mdl.keys()
    all_fortimes.sort()
    max_index = len(all_fortimes) - 1

    for plot_index, cur_fortime in enumerate(all_fortimes):
        cur_timeseries = dict_timeseries_mdl[cur_fortime]
        x_set = []
        y_set = []
        for i, cur_value in enumerate(cur_timeseries):
            # cur_delta_time = cur_value[0] * 60  # the forecast file is in delta-minutes. Converting to delta-seconds
            # x_set.append(datetime.datetime.fromtimestamp(cur_delta_time + cur_fortime))
            x_set.append(datetime.datetime.fromtimestamp(cur_value[0]))
            y_set.append(cur_value[1])

        cur_color = get_color_from_index(plot_index, max_index)     # defines hydrograph's time series color
        if cur_color is not None:
            plt.plot(x_set, y_set, linewidth=0.5, color=cur_color)  # plot hydrograph's time series
            plt.scatter(x_set[0], y_set[0], color=cur_color)        # plot hydrograph's starting point

    # plot observed timeseries
    if dict_timeseries_obs is not None:
        all_obs = dict_timeseries_obs.keys()
        all_obs.sort()
        obs_x_set = []
        obs_y_set = []
        if len(all_obs) > 0:
            Debug.dl("evalgen_hydroforecast_graph: Plotting {0} observed values between {1} and {2} for {3}.".format(
                len(all_obs), datetime.datetime.fromtimestamp(all_obs[0]), datetime.datetime.fromtimestamp(all_obs[-1]),
                link_id), 3, debug_lvl)
        else:
            Debug.dl("evalgen_hydroforecast_graph: No observed values between {0}.".format(link_id), 3, debug_lvl)
        for cur_obs_time in all_obs:
            obs_x_set.append(datetime.datetime.fromtimestamp(cur_obs_time))
            obs_y_set.append((dict_timeseries_obs[cur_obs_time]) * 0.0833333)    # from in to ft
        plt.plot(obs_x_set, obs_y_set, linewidth=1.0, color='k', label="Observed")

    # plot thresholds
    if dict_timeseries_thr is not None:
        try:
            plt.axhline(y=(dict_timeseries_thr[1]-dict_timeseries_thr[0])*0.0833333, linewidth=1, color='y',
                                  label="Action level", linestyle='dashdot')    # in to ft
            plt.axhline(y=(dict_timeseries_thr[2]-dict_timeseries_thr[0])*0.0833333, linewidth=1, color='#FF6900',
                                  label="Flood level", linestyle='dashdot')     # in to ft
            plt.axhline(y=(dict_timeseries_thr[3]-dict_timeseries_thr[0])*0.0833333, linewidth=1, color='r',
                                  label="Moderate level", linestyle='dashdot')  # in to ft
            plt.axhline(y=(dict_timeseries_thr[4]-dict_timeseries_thr[0])*0.0833333, linewidth=1, color='m',
                                  label="Major level", linestyle='dashdot')     # in to ft
        except TypeError:
            Debug.dl("evalgen_hydroforecast_graph: Some stage thresholds for link_id {0} is missing.".format(link_id),
                     2, debug_lvl)

    # plot vertical line
    plt.axvline(x=last_fordate, linestyle='dashed', linewidth=2, color='k', label="Last forecast run")

    # add y axis on the left side
    plt.ylabel("stage [ft]")

    # add title and legend
    up_area_str = "{:.2f}".format(upstream_area/2.59)
    plot_title = "{0} (link id: {1}, upstream area: {2} miles^2)".format(pois_description, link_id, up_area_str)
    plt.title(plot_title)
    plt.legend(loc=4)
    # handles_list = [x for x in [leg_maj, leg_mod, leg_fld, leg_act, leg_obs, leg_lst] if x is not None]
    # plt.legend(handles=handles_list)

    # debug
    Debug.dl("evalgen_hydroforecast_graph: Plot compose for link {0} finished at: {1}.".format(link_id,
                                                                                               datetime.datetime.now()),
             1, debug_lvl)

    # define folder and create it if necessary
    output_folder_path = FolderDefinition.get_historical_eval_folder_path(model_id, "hydroforecast", sc_reference_id,
                                                                          runset_id=runset_id)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # save file
    file_name = "{0}_{1}.png".format(last_fortime, link_id)
    file_path = os.path.join(output_folder_path, file_name)
    plt.savefig(file_path, bbox_inches='tight')

    # debug
    # print(file_path)
    Debug.dl("evalgen_hydroforecast_graph: File saved for link {0} finished at: {1}.".format(link_id,
                                                                                             datetime.datetime.now()),
             1, debug_lvl)
    Debug.dl("evalgen_hydroforecast_graph: File writen: {0}.".format(file_path), 1, debug_lvl)

    return True


def plot_pdf_from_fs(sc_model_id, sc_reference_id, runset_id, timestamp=None, debug_lvl=0):
    """

    :param sc_model_id:
    :param sc_reference_id:
    :param runset_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    number_of_points = 15
    number_of_days_behind = 10

    # start counting time for debug
    start_time = time.time() if debug_lvl > 0 else None

    folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, 'fq', runset_id=runset_id)

    cur_timestamp = timestamp if timestamp is not None else \
        FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(folder_path)

    # basic check
    if cur_timestamp is None:
        Debug.dl("evalgen_hydroforecast_graph: No files in {0} folder.".format(folder_path), 1, debug_lvl)
        return

    # get all hydroforecasts and perform basic check
    min_timestamp = cur_timestamp - (number_of_days_behind * 24 * 3600)
    all_hydroforecasts = get_set_of_hydroforecasts(sc_model_id, runset_id, min_timestamp, cur_timestamp,
                                                   number_of_points, debug_lvl=debug_lvl)
    if len(all_hydroforecasts) == 0:
        Debug.dl("evalgen_hydroforecast_graph: No hydroforecast files found for {0}.".format(sc_model_id), 1, debug_lvl)
        return

    Debug.dl("evalgen_hydroforecast_graph: Got {0} hydrograph sets between {1} and {2}.".format(len(all_hydroforecasts),
                                                                                                min_timestamp,
                                                                                                cur_timestamp),
             1, debug_lvl)

    # load common reference files
    all_obs_dict = get_observed_data_fs(sc_reference_id, runset_id, cur_timestamp, debug_lvl=debug_lvl)

    if all_obs_dict is None:
        Debug.dl("evalgen_hydroforecast_graph: No available observation files found for {0}.".format(sc_reference_id),
                 1, debug_lvl)
        return

    all_stage_thresholds = Hydrographs.get_all_stage_threshold(debug_lvl=debug_lvl)
    # linkid_poisid_dict = get_linkid_poisid_relationship_fs(debug_lvl=debug_lvl)
    linkid_poisall_dict = Hydrographs.get_linkid_poisall_relationship(debug_lvl=debug_lvl)
    linkid_descarea_dict = Hydrographs.get_linkid_desc_area(debug_lvl=debug_lvl)
    all_usgs_rc = Hydrographs.get_all_usgs_rating_curves(debug_lvl=debug_lvl)

    #
    forecast_timestamps = all_hydroforecasts.keys()
    forecast_timestamps.sort()

    count_tries = 0
    count_done = 0
    for cur_linkid in linkid_poisall_dict.keys():

        # try to get observation data
        cur_obs_timeseries = all_obs_dict[cur_linkid] if cur_linkid in all_obs_dict.keys() else None
        if cur_obs_timeseries is not None:
            Debug.dl("evalgen_hydroforecast_graph: Observed timeseries for link_id {0} has {1} elements.".format(
                cur_linkid, len(cur_obs_timeseries.keys())), 3, debug_lvl)
        else:
            Debug.dl("evalgen_hydroforecast_graph: No observation data for linkid {0}".format(cur_linkid), 3, debug_lvl)

        # try to get thresholds
        cur_thresholds = all_stage_thresholds[cur_linkid] if cur_linkid in all_stage_thresholds.keys() else None

        # get rating curve information for linkid
        try:
            cur_rc = all_usgs_rc[cur_linkid]
        except KeyError:
            Debug.dl("evalgen_hydroforecast_graph: Ignoring linkid {0} (no rating curve).".format(cur_linkid), 3, debug_lvl)
            continue

        # get description/area information for linkid
        try:
            cur_descarea_dict = linkid_descarea_dict[cur_linkid]
        except KeyError:
            Debug.dl("evalgen_hydroforecast_graph: Ignoring linkid {0} (no description/area).".format(cur_linkid), 3, debug_lvl)
            continue

        # try to get area
        try:
            cur_total_area = linkid_poisall_dict[cur_linkid][linkid_poisall_dict[cur_linkid].keys()[0]]["up_area"]
        except KeyError:
            cur_total_area = -1

        all_disch, all_stage = extract_specific_disch_stage_fs(cur_rc)

        # convert modeled timeseries from discharge to stage
        all_timeseries = {}
        Debug.dl("evalgen_hydroforecast_graph: Evaluating {0} hydroforecast times.".format(len(forecast_timestamps)),
                 3, debug_lvl)
        for cur_forecast_timestamp in forecast_timestamps:

            # convert hydrograph from discharge to stage
            cur_all_hydroforecasts = all_hydroforecasts[cur_forecast_timestamp]

            if cur_linkid not in cur_all_hydroforecasts.keys():
                continue

            cur_mdl_hydrograph_disch = all_hydroforecasts[cur_forecast_timestamp][cur_linkid]

            cur_mdl_stage = [[a[0], Interpolate.my_interpolation_xy(all_disch, all_stage, a[1] * 35.315)]
                             for a in cur_mdl_hydrograph_disch]

            all_timeseries[cur_forecast_timestamp] = cur_mdl_stage
            Debug.dl("evalgen_hydroforecast_graph: Added timestamp {0} to timeseries dictionary.".format(cur_forecast_timestamp),
                 4, debug_lvl)

        # plot graph
        Debug.dl("evalgen_hydroforecast_graph: There are {0} timeseries in dictionary.".format(len(all_timeseries.keys()
                                                                                                   )), 3, debug_lvl)

        '''
        cur_plotted = the_plot(all_timeseries, cur_obs_timeseries, cur_thresholds, sc_model_id, cur_linkid,
                               cur_timestamp, pois_description=cur_descarea_dict["description"],
                               upstream_area=cur_descarea_dict["total_area"], debug_lvl=debug_lvl)
        '''
        cur_plotted = the_plot(all_timeseries, cur_obs_timeseries, cur_thresholds, sc_model_id, cur_linkid,
                               cur_timestamp, sc_reference_id, runset_id,
                               pois_description=cur_descarea_dict["description"], upstream_area=cur_total_area,
                               debug_lvl=debug_lvl)

        count_tries += 1
        count_done += 1 if cur_plotted else 0

        '''
        # for debugging purposes - stop after some ones
        if count_done == 15:
            break
        '''

    # debug info
    d_time = time.time()-start_time

    Debug.dl("evalgen_hydroforecast_graph: Plotted {0} out of {1} in {2} seconds".format(count_done, count_tries, d_time), 1, debug_lvl)


def plot_pdf(sc_model_id, sc_reference_id, runset_id_arg, timestamp, source, debug_lvl=0):
    """

    :param sc_model_id:
    :param sc_reference_id:
    :param runset_id_arg:
    :param timestamp:
    :param source:
    :param debug_lvl:
    :return:
    """

    if source == "fs":
        plot_pdf_from_fs(sc_model_id, sc_reference_id, runset_id_arg, timestamp, debug_lvl=debug_lvl)
    else:
        Debug.dl("evalgen_hydroforecast_graph: Invalid source {0}.".format(source), 0, debug_lvl)
        return

# ####################################################### CALL ####################################################### #

plot_pdf(model_id_arg, reference_id_arg, runset_id_arg, timestamp_arg, "fs", debug_lvl=debug_level_arg)
