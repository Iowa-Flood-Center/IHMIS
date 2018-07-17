import shutil
import os

from libs.FolderDefinition import FolderDefinition
from libs.MetaFileManager import MetaFileManager
from libs.GeneralUtils import GeneralUtils
from libs.Debug import Debug


def update_display(considered_model_ids, considered_reference_ids, considered_representation_ids,
                   considered_comparison_ids, considered_evaluation_ids, timestamp, meta_mng, runset_id=None,
                   debug_lvl=0):
    """
    Updates single and comparison with standard in-file function, evaluations with specific scripts.
    :param considered_model_ids: List of models ids.
    :param considered_reference_ids: List of reference ids.
    :param considered_representation_ids: List of representation ids.
    :param considered_comparison_ids: List of comparison ids.
    :param considered_evaluation_ids: List of evaluation ids.
    :param timestamp:
    :param meta_mng:
    :param runset_id: String. A sc_runset_id. If None, assumes 'realtime'.
    :param debug_lvl:
    :return:
    """

    # basic check
    if (considered_model_ids is None) and (considered_reference_ids is None) and (considered_evaluation_ids is None) \
            and (considered_comparison_ids is None):
        Debug.dl("update_display_lib: No model, reference, comparison or evaluation provided. Finishing.", 1, debug_lvl)
        return

    # basic check - timestamp
    the_timestamp = "" if timestamp is None else timestamp

    # load meta information
    # meta_mng = MetaFileManager(runset_id=runset_id)
    # meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
    # meta_mng.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)

    # update model's representations
    if considered_model_ids is not None:

        if considered_representation_ids is not None:
            for cur_model_id in considered_model_ids:
                all_cur_representations = meta_mng.get_all_representations_of_scmodel(cur_model_id, debug_lvl=debug_lvl)
                all_cur_reprcomp = meta_mng.get_all_representationscompound_of_scmodelcombination(cur_model_id,
                                                                                                  debug_lvl=debug_lvl)

                # basic check
                if (all_cur_representations is None) and (all_cur_reprcomp is None):
                    Debug.dl("update_display_lib: No representations for model {0}.".format(cur_model_id), 1, debug_lvl)
                    continue

                # update model's representations simple
                if all_cur_representations is not None:
                    for cur_representation_id in all_cur_representations:
                        if cur_representation_id in considered_representation_ids:
                            update_representation_display(cur_model_id, cur_representation_id, timestamp, meta_mng,
                                                          runset_id=runset_id, debug_lvl=debug_lvl)
                            Debug.dl("update_display_lib: Called model representations updater for {0}.{1}.{2}.".format(
                                runset_id, cur_model_id, cur_representation_id), 1, debug_lvl)

                # update model's representations compound
                if all_cur_reprcomp is not None:
                    for cur_reprcomp_id in all_cur_reprcomp:
                        if cur_reprcomp_id in considered_representation_ids:
                            the_command = meta_mng.get_updscript_of_representation_cmpd(cur_reprcomp_id,
                                                                                        debug_lvl=debug_lvl)
                            if the_command is not None:
                                call_command = "{0} -modelcomb {1} -runsetid {2}".format(the_command, cur_model_id,
                                                                                         runset_id)
                                Debug.dl("update_display_lib: call '{0}'.".format(call_command), 1, debug_lvl)
                                os.system(call_command)
                                Debug.dl("update_display_lib: Called model repres. comp. updater for {0}.{1}.{2}.".format(
                                    runset_id, cur_model_id, cur_reprcomp_id), 1, debug_lvl)
                            else:
                                Debug.dl("update_display_lib: Missing update script for representation compound '{0}.{1}'.".format(
                                    runset_id, cur_reprcomp_id), 1, debug_lvl)

                Debug.dl("update_display_lib: Updated model {0}.{1}.".format(runset_id, cur_model_id), 1, debug_lvl)
        else:
            Debug.dl("update_display_lib: Got NONE considered representations.", 1, debug_lvl)
    else:
        Debug.dl("update_display_lib: Got NONE considered models.", 1, debug_lvl)

    # update model's compound representations


    # update references's representation
    if considered_reference_ids is not None:

        # load SC_Reference content
        # meta_mng.load_all_screference_meta_info(debug_lvl=debug_lvl)

        for cur_reference_id in considered_reference_ids:
            all_cur_representations = meta_mng.get_all_representations_of_screference(cur_reference_id,
                                                                                      debug_lvl=debug_lvl)
            if all_cur_representations is None:
                Debug.dl("update_display_lib: No representations for reference {0}.".format(cur_reference_id), 1,
                         debug_lvl)
                continue

            for cur_representation_id in all_cur_representations:
                update_representation_display(cur_reference_id, cur_representation_id, timestamp, meta_mng,
                                              runset_id=runset_id, debug_lvl=debug_lvl)
            Debug.dl("update_display_lib: Updating reference {0}.".format(cur_reference_id), 1, debug_lvl)
            Debug.dl("update_display_lib: Call reference representations updater.", 0, debug_lvl)
    else:
        print("NO Refs: {0}".format(considered_reference_ids))

    # update comparison's representations
    if considered_comparison_ids is not None:
        Debug.dl("update_display_lib: {0} comparisons ids.".format(len(considered_comparison_ids)), 1, debug_lvl)
        # meta_mng.load_comparison_matrix(debug_lvl=debug_lvl)
        for cur_comparison_id in considered_comparison_ids:
            all_cur_representations = meta_mng.get_all_representations_of_comparison(comparison_acronym=cur_comparison_id,
                                                                                     debug_lvl=debug_lvl)
            if all_cur_representations is None:
                Debug.dl("update_display_lib: No representations for comparison {0}.".format(cur_comparison_id),
                         1, debug_lvl)
                continue
            for cur_representation_id in all_cur_representations:
                update_representation_display(cur_comparison_id, cur_representation_id, timestamp, meta_mng,
                                              runset_id=runset_id, debug_lvl=debug_lvl)
            Debug.dl("update_display_lib: Updating comparison {0}.".format(cur_comparison_id), 1, debug_lvl)
            Debug.dl("update_display_lib: Call comparison representations updater.", 0, debug_lvl)
    else:
        Debug.dl("update_display_lib: Ignoring comparisons.", 1, debug_lvl)

    # update evaluation's representations
    if considered_evaluation_ids is not None:

        # load SC_Evaluation content and, if necessary, all SC_Models id
        # meta_mng.load_all_scevaluation_meta_info(debug_lvl=debug_lvl)
        meta_mng.load_evaluation_matrix(debug_lvl=debug_lvl)
        if considered_model_ids is None:
            considered_model_ids = meta_mng.get_all_scmodel_ids()

        # execute the updater of each evaluation of each possible model
        for cur_evaluation_id in considered_evaluation_ids:

            '''
            cur_evaluated_models = meta_mng.get_evaluated_model_ids(cur_evalutation_id, debug_lvl=debug_lvl)
            if cur_evaluated_models is None:
                Debug.dl("update_display_lib: Evaluation '{0}' has no models.".format(cur_evalutation_id), 2, debug_lvl)
                continue

            for cur_model_id in considered_model_ids:
                if cur_model_id not in cur_evaluated_models:
                    continue

                the_command = meta_mng.get_evaluation_updater_script_of_scevaluation(cur_evalutation_id,
                                                                                     debug_lvl=debug_lvl)
                call_command = "{0} {1} {2}".format(the_command, cur_model_id, the_timestamp)
                Debug.dl("update_display_lib: Updating evaluation {0} of model {1}.".format(cur_evalutation_id,
                                                                                            cur_model_id), 1, debug_lvl)
                Debug.dl("update_display_lib: Calling command '{0}'.".format(call_command), 2, debug_lvl)
                os.system(call_command)
            '''

            evaluated_models_and_ref = meta_mng.get_all_evalutated_models_and_references(cur_evaluation_id)
            if evaluated_models_and_ref is None:
                Debug.dl("update_display_lib: Evaluation '{0}' has no models.".format(cur_evaluation_id), 2, debug_lvl)
                continue

            for cur_mdlref_id in evaluated_models_and_ref:
                cur_model_id = cur_mdlref_id[0]
                cur_ref_id = cur_mdlref_id[1]
                if cur_model_id not in considered_model_ids:
                    continue

                the_command = meta_mng.get_evaluation_updater_script_of_scevaluation(cur_evaluation_id,
                                                                                     debug_lvl=debug_lvl)

                call_command = "{0} {1} {2} -ref {3} -runsetid {4}".format(the_command, cur_model_id, the_timestamp,
                                                                           cur_ref_id, runset_id)
                Debug.dl("update_display_lib: Updating evaluation {0} of model {1}.".format(cur_evaluation_id,
                                                                                            cur_model_id), 1, debug_lvl)

                Debug.dl("update_display_lib: CALL '{0}'.".format(call_command), 2, debug_lvl)
                os.system(call_command)
    else:
        Debug.dl("update_display_lib: NONE evaluations in runset '{0}'.".format(runset_id), 2, debug_lvl)

    return


def update_representation_display(sc_model_id, sc_representation_id, timestamp, metafile_mng, runset_id=None,
                                  debug_lvl=0):
    """

    :param sc_model_id:
    :param sc_representation_id:
    :param metafile_mng: MetaFileManager object
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    # constants
    default_time_interval = 3600
    # TODO - move to metafile-sourced
    if (runset_id is None) or (runset_id == "realtime"):
        images_back_time = 10.2 * 24 * 60 * 60  # updates up to 10 days of images
    else:
        images_back_time = 20.2 * 24 * 60 * 60  # updates up to 20 days of images

    # define source folder and reference timestamp
    hist_folder_path = FolderDefinition.get_historical_img_folder_path(model_id=sc_model_id,
                                                                       representation_id=sc_representation_id,
                                                                       runset_id=runset_id)
    if timestamp is None:
        the_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)
    else:
        the_timestamp = timestamp

    # basic check timestamp
    if the_timestamp is None:
        Debug.dl("update_display_lib: No images for {0}.{1}.{2}.".format(runset_id, sc_model_id, sc_representation_id),
                 1, debug_lvl)
        return

    # define time interval between images
    time_interval = metafile_mng.get_time_interval_of_representation(sc_representation_id, debug_lvl=debug_lvl)
    the_timestep = default_time_interval if time_interval is None else time_interval

    Debug.dl("update_display_lib: For {0}, interval time is {1}.".format(sc_model_id, time_interval), 1,
             debug_lvl)

    # define current index and extreme timestamp
    cur_index = 0
    cur_timestamp = GeneralUtils.round_timestamp_hour(the_timestamp)  # TODO - read from MetaFiles
    ext_timestamp = the_timestamp - images_back_time   # extreme timestamp

    # create folder if necessary
    d_folder_path = FolderDefinition.get_displayed_folder_path(sc_model_id, sc_representation_id, runset_id=runset_id)
    if not os.path.exists(d_folder_path):
        os.makedirs(d_folder_path)
    else:
        # delete previous files
        all_prev_file_paths = [os.path.join(d_folder_path, f) for f in os.listdir(d_folder_path)]

        count = 0
        for cur_prev_file_path in all_prev_file_paths:
            if os.path.isfile(cur_prev_file_path):
                count += 1
                os.unlink(cur_prev_file_path)
        Debug.dl("update_display_lib: Deleted {0} previous files of {1}.{2}".format(count, sc_model_id,
                                                                                    sc_representation_id), 3, debug_lvl)

    # discovers files' extensions
    file_ext = FolderDefinition.retrive_files_extension_in_hist_folder(hist_folder_path, debug_lvl=debug_lvl)

    # go copying
    while cur_timestamp > ext_timestamp:
        cur_effective_timestamp = FolderDefinition.retrive_closest_timestamp_in_hist_folder(hist_folder_path,
                                                                                            cur_timestamp,
                                                                                            accept_range=(29 * 60))
        cur_h_filepath = FolderDefinition.get_historical_file_path(sc_model_id, sc_representation_id, file_ext,
                                                                   cur_effective_timestamp, runset_id=runset_id)
        if os.path.exists(cur_h_filepath):
            cur_d_filepath = FolderDefinition.get_displayed_file_path(sc_model_id, sc_representation_id,
                                                                      cur_index, file_ext, runset_id=runset_id)
            shutil.copy(cur_h_filepath, cur_d_filepath)
            Debug.dl("update_display_lib: Copying {0} ...".format(cur_h_filepath), 5, debug_lvl)
            Debug.dl("update_display_lib:  '-> to {0}.".format(cur_d_filepath), 5, debug_lvl)
        else:
            Debug.dl("update_display_lib: Not found {0} for index {1}.".format(cur_h_filepath, cur_index), 5, debug_lvl)

        cur_timestamp -= the_timestep
        cur_index += 1

    # update reference file
    Debug.dl("update_display_lib: Calling 'update_ref0_file'.", 5, debug_lvl)
    update_ref0_file(sc_model_id, sc_representation_id, GeneralUtils.round_timestamp_hour(the_timestamp),
                     runset_id=runset_id, debug_lvl=debug_lvl)


def update_ref0_file(sc_model_id, sc_representation_id, timestamp, runset_id=None, debug_lvl=0):
    """
    Delete / create new reference file
    :param sc_model_id:
    :param sc_representation_id:
    :param timestamp:
    :param debug_lvl:
    :return:
    """

    # creates folder if necessary
    dest_folder_path = FolderDefinition.get_timestamp_ref_txt_folder_path(sc_model_id=sc_model_id,
                                                                          sc_runset_id=runset_id)
    if not os.path.exists(dest_folder_path):
        os.makedirs(dest_folder_path)

    # gets file path and delete previous if exists
    dest_file_path = FolderDefinition.get_timestamp_ref_txt_file_path(sc_model_id, sc_representation_id,
                                                                      sc_runset_id=runset_id)
    if os.path.exists(dest_file_path):
        os.remove(dest_file_path)

    # create new one only with timestamp
    with open(dest_file_path, "w+") as wfile:
        wfile.write(str(timestamp))

    Debug.dl("update_display_lib: Created file '{0}' holding '{1}'.".format(dest_file_path, timestamp), 2, debug_lvl)
