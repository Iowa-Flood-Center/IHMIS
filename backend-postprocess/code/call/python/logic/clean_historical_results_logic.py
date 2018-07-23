import os

from libs.MetaFileManager import MetaFileManager
from libs.Debug import Debug


def clean_historical(considered_model_ids, considered_modelcomb_ids, considered_reference_ids,
                     considered_representation_ids, considered_comparison_ids, considered_evaluation_ids, timestamp,
                     runset_id, meta_mng, debug_lvl=0):
    """

    :param considered_model_ids:
    :param considered_modelcomb_ids:
    :param considered_reference_ids:
    :param considered_representation_ids:
    :param considered_comparison_ids:
    :param considered_evaluation_ids:
    :param timestamp:
    :param runset_id:
    :param debug_lvl:
    :return:
    """

    # basic check
    if (considered_model_ids is None) and (considered_modelcomb_ids is None) and (considered_reference_ids is None) \
            and (considered_evaluation_ids is None) and (considered_comparison_ids is None) \
            and (considered_representation_ids is None):
        Debug.dl("clean_historical_results_lib: No model, model comb., reference, comparison, evaluation, representation provided.",
                 1, debug_lvl)
        return

    # basic check - timestamp
    the_timestamp = "" if timestamp is None else timestamp

    # clean models' results
    if considered_model_ids is not None:
        for cur_model_id in considered_model_ids:
            Debug.dl("clean_historical_results_lib: cleaning {0}.{1}.".format(runset_id, cur_model_id), 1, debug_lvl)

            # cleaning all representations
            all_cur_representations = meta_mng.get_all_representations_of_scmodel(cur_model_id, debug_lvl=debug_lvl)
            if (all_cur_representations is None) or (len(all_cur_representations) == 0):
                Debug.dl("clean_historical_results_lib: No representations for model {0}.".format(cur_model_id), 1,
                         debug_lvl)
            else:
                for cur_representation_id in all_cur_representations:
                    if cur_representation_id in considered_representation_ids:
                        Debug.dl("clean_historical_results_lib: cleaning {0}.{1}.{2}.".format(runset_id, cur_model_id,
                                                                                              cur_representation_id), 1,
                                 debug_lvl)
                        clean_representation_hist(cur_model_id, cur_representation_id, timestamp, meta_mng, runset_id,
                                                  debug_lvl=debug_lvl)

            # cleaning all evaluations
            all_cur_evaluations = meta_mng.get_all_evaluations_of_scmodel(cur_model_id)
            if (all_cur_evaluations is None) or (len(all_cur_evaluations) == 0):
                Debug.dl("clean_historical_results_lib: No evaluations for model {0}.".format(cur_model_id), 1,
                         debug_lvl)
            else:
                for cur_evaluation_id in all_cur_evaluations:
                    cur_sc_evaluation_id, cur_sc_reference_id = cur_evaluation_id.split('_')
                    if cur_sc_evaluation_id in considered_evaluation_ids:
                        Debug.dl("clean_historical_results_lib: cleaning {0}.{1}.{2}.".format(runset_id, cur_model_id,
                                                                                              cur_evaluation_id), 1,
                                 debug_lvl)
                        clean_evaluation_hist(cur_model_id, cur_sc_evaluation_id, cur_sc_reference_id, timestamp,
                                              meta_mng, runset_id, debug_lvl=debug_lvl)
                    else:
                        print("Evaluation '{0}' not in {1}".format(cur_evaluation_id, considered_evaluation_ids))

    # clean model combinations' results
    if considered_modelcomb_ids is not None:
        for cur_modelcomb_id in considered_modelcomb_ids:
            Debug.dl("clean_historical_results_lib: cleaning {0}.{1}.".format(runset_id, cur_modelcomb_id), 1,
                     debug_lvl)
            print("TODO - IMPLEMENTING IT")

            # cleaning all representations compound
            all_cur_represcompound = meta_mng.get_all_representationscompound_of_scmodelcombination(cur_modelcomb_id,
                                                                                                    debug_lvl=debug_lvl)
            if (all_cur_represcompound is None) or (len(all_cur_represcompound) == 0):
                Debug.dl("clean_historical_results_lib: No repr. comp. for model comb. {0}.".format(cur_modelcomb_id),
                         1, debug_lvl)
            else:
                print("clean_historical_results_lib: will clean {0}.{1}.".format(cur_modelcomb_id,
                                                                                 all_cur_represcompound))
                for cur_represcompound_id in all_cur_represcompound:
                    clean_represcompound_hist(cur_modelcomb_id, cur_represcompound_id, meta_mng, runset_id,
                                              debug_lvl=debug_lvl)

    else:
        Debug.dl("clean_historical_results_lib: no model comb. for runset '{0}'.".format(runset_id), 1, debug_lvl)


def clean_representation_hist(sc_model_id, sc_representation_id, timestamp, meta_mng, sc_runset_id, debug_lvl=0):
    """

    :param sc_model_id:
    :param sc_representation_id:
    :param timestamp:
    :param meta_mng:
    :param sc_runset_id:
    :param debug_lvl:
    :return:
    """

    # get 'representation cleaning' script
    reprcln_script_path = meta_mng.get_representation_cleaner_script_of_screpresentation(sc_representation_id,
                                                                                         debug_lvl=debug_lvl)

    # basic check
    if reprcln_script_path is None:
        Debug.dl("clean_historical_results_lib: MISSING reprcln_script OF '{0}'.".format(sc_representation_id), 1,
                 debug_lvl)
        return

    # build command to run
    sys_call = "{0} -m {1} -rep {2} -runsetid {3}".format(reprcln_script_path, sc_model_id, sc_representation_id,
                                                          sc_runset_id)
    try:
        Debug.dl("clean_historical_results_lib: Calling '{0}'.".format(sys_call), 1, debug_lvl)
        os.system(sys_call)
    except OSError:
        Debug.dl("clean_historical_results_lib: Failed running '{0}'.".format(sys_call), 1, debug_lvl)

    return


def clean_evaluation_hist(sc_model_id, sc_evaluation_id, sc_reference_id, timestamp, meta_mng, sc_runset_id, debug_lvl=0):
    """

    :param sc_model_id:
    :param sc_representation_id:
    :param timestamp:
    :param meta_mng:
    :param sc_runset_id:
    :param debug_lvl:
    :return:
    """

    # get 'evaluation cleaning' script
    evalcln_script_path = meta_mng.get_evaluation_cleaner_script_of_scevaluation(sc_evaluation_id, debug_lvl=debug_lvl)

    # basic check
    if evalcln_script_path is None:
        Debug.dl("clean_historical_results_lib: MISSING evalcln_script OF '{0}'.".format(sc_evaluation_id), 1,
                 debug_lvl)
        return

    # build command to run
    sys_call = "{0} {1} -ref {2} -runsetid {3}".format(evalcln_script_path, sc_model_id, sc_reference_id, sc_runset_id)
    try:
        Debug.dl("clean_historical_results_lib: Calling '{0}'.".format(sys_call), 1, debug_lvl)
        os.system(sys_call)
    except OSError:
        Debug.dl("clean_historical_results_lib: Failed running '{0}'.".format(sys_call), 1, debug_lvl)

    # print("Script: {0}".format(evalcln_script_path))

    return


def clean_represcompound_hist(sc_modelcomb_id, sc_represcompd_id, meta_mng, sc_runset_id, debug_lvl=0):
    """

    :param sc_modelcomb_id:
    :param meta_mng:
    :param sc_runset_id:
    :param debug_lvl:
    :return:
    """

    # get '' script
    rpcbcln_script_path = meta_mng.get_representation_cleaner_script_of_screpresentationcompound(sc_represcompd_id,
                                                                                                 debug_lvl=debug_lvl)

    # basic check
    if rpcbcln_script_path is None:
        Debug.dl("clean_historical_results_lib: MISSING rpcbcln_script OF '{0}'.".format(sc_modelcomb_id), 1, debug_lvl)
        return

    # build command to run
    sys_call = "{0} -modelcomb {1} -reprcomb {2} -runsetid {3}".format(rpcbcln_script_path, sc_modelcomb_id,
                                                                       sc_represcompd_id, sc_runset_id)
    try:
        Debug.dl("clean_historical_results_lib: Calling '{0}'.".format(sys_call), 1, debug_lvl)
        os.system(sys_call)
    except OSError:
        Debug.dl("clean_historical_results_lib: Failed running '{0}'.".format(sys_call), 1, debug_lvl)
