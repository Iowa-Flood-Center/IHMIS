from libs.MetaFileManager import MetaFileManager
from libs.Debug import Debug
import os


def import_data(sc_runset_id, sc_model_id='all',  unix_timestamp=None, debug_lvl=0):

    meta_file_manager = MetaFileManager(runset_id=sc_runset_id)
    meta_file_manager.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
    meta_file_manager.load_all_screference_meta_info(debug_lvl=debug_lvl)

    if unix_timestamp is None:
        cur_unix_timestamp = ""
    else:
        cur_unix_timestamp = "-t {0}".format(unix_timestamp)

    # ###################################### MODELS ################################# #

    # load list of sc_models to have their parameters generated
    if (sc_model_id is None) or (sc_model_id == 'all'):
        evaluated_sc_models_id = meta_file_manager.get_all_scmodel_ids()
    else:
        evaluated_sc_models_id = [sc_model_id]

    # run specific script for each model
    for cur_sc_model_id in evaluated_sc_models_id:

        # generate binary files for states
        cur_script_states = meta_file_manager.get_binaries_generator_script_of_scmodel(cur_sc_model_id,
                                                                                       debug_lvl=debug_lvl)
        if cur_script_states is not None:
            sys_call = "{0} -model_sing_id {1} -runset_id {2}"
            sys_call = sys_call.format(cur_script_states, cur_sc_model_id, sc_runset_id)
            # sys_call = " ".join([cur_script_states, cur_sc_model_id, cur_unix_timestamp, cur_runset_arg])
            Debug.dl("create_binaries_lib: Running '{0}' for sc model '{1}'".format(sys_call, cur_sc_model_id),
                     2, debug_lvl)
            try:
                Debug.dl("create_binaries_lib: CALL: '{0}'".format(sys_call),
                         2, debug_lvl)
                # os.system(sys_call)
            except OSError:
                Debug.dl("create_binaries_lib: Failed running '{0}'.".format(sys_call), 1, debug_lvl)
        else:
            Debug.dl("create_binaries_lib: SC model '{0}' has no script for state binary file generation.".format(
                cur_sc_model_id), 1, debug_lvl)

        # generate binary files for forecasts
        cur_script_hydroforecast = meta_file_manager.get_binaries_generator_script_hydroforecast_of_scmodel(
            cur_sc_model_id, debug_lvl=debug_lvl)
        if cur_script_hydroforecast is not None:
            sys_call = " ".join([cur_script_hydroforecast, cur_sc_model_id, cur_unix_timestamp, cur_runset_arg])
            Debug.dl("create_binaries_lib: Running '{0}' for sc model '{1}'".format(sys_call, cur_sc_model_id),
                     2, debug_lvl)
            try:
                Debug.dl("create_binaries_lib: CALL: '{0}'".format(sys_call),
                         2, debug_lvl)
                # os.system(sys_call)
            except OSError:
                Debug.dl("create_binaries_lib: Failed running '{0}'.".format(sys_call), 1, debug_lvl)
        else:
            Debug.dl(
                "create_binaries_lib: SC model '{0}' has no related script for hydroforecast binary file generation.".format(
                    cur_sc_model_id), 1, debug_lvl)

    # ################################################ REFERENCES #################################################### #

    # load list of sc_models to have their parameters generated
    if (sc_model_id is None) or (sc_model_id == 'all'):
        evaluated_sc_references_id = meta_file_manager.get_all_screference_ids()
    else:
        evaluated_sc_references_id = [sc_model_id] if sc_model_id in meta_file_manager.get_all_screference_ids() else []

    # run specific script for each reference
    for cur_sc_reference_id in evaluated_sc_references_id:
        Debug.dl("create_binaries_lib: Will run it for reference '{0}' at {1}.".format(cur_sc_reference_id,
                                                                                       cur_unix_timestamp),
                 0, debug_lvl)

        # generate binary files for states
        cur_script = meta_file_manager.get_binaries_generator_script_of_screference(cur_sc_reference_id,
                                                                                    debug_lvl=debug_lvl)

        if cur_script is not None:
            sys_call = " ".join([cur_script, cur_sc_reference_id, cur_unix_timestamp, cur_runset_arg])
            Debug.dl("create_binaries_lib: Running '{0}' for sc reference '{1}'".format(sys_call, cur_sc_reference_id),
                     2, debug_lvl)
            try:
                print("CALL: {0}".format(sys_call))
                # os.system(sys_call)
            except OSError:
                Debug.dl("create_binaries_lib: Failed running '{0}'.".format(sys_call), 1, debug_lvl)
        else:
            Debug.dl("create_binaries_lib: SC model '{0}' has no script for state binary file generation.".format(
                cur_sc_reference_id), 1, debug_lvl)
