import os

from libs.MetaFileManager import MetaFileManager
from libs.Debug import Debug


# ####################################################### DEFS ####################################################### #

def generate_evaluations(sc_model_ids, sc_evaluation_ids, sc_runset_id, timestamp, debug_lvl=0):

    # basic check
    # TODO - do it

    the_timestamp = "" if timestamp is None else timestamp

    # load meta information
    meta_mng = MetaFileManager(runset_id=sc_runset_id)
    meta_mng.load_all_scevaluation_meta_info(debug_lvl=debug_lvl)
    meta_mng.load_evaluation_matrix(debug_lvl=debug_lvl)

    for cur_evaluation_id in sc_evaluation_ids:

        '''
        evaluated_models = meta_mng.get_evaluated_model_ids(cur_evaluation_id)
        if evaluated_models is None:
            Debug.dl("plot_evaluations_logic: Evaluation {0} is not related on Evaluation matrix.".format(cur_evaluation_id),
                     1, debug_lvl)
            continue

        for cur_model_id in sc_model_ids:

            # check if such combination is possible
            if cur_model_id in evaluated_models:
                the_script = meta_mng.get_evaluation_generator_script_of_scevaluation(cur_evaluation_id, debug_lvl)
                the_call = "{0} {1} {2}".format(the_script, cur_model_id, the_timestamp)
                Debug.dl("plot_evaluations_logic: Will execute '{0}'.".format(the_call), 1, debug_lvl)
                os.system(the_call)

            else:
                Debug.dl("plot_evaluations_logic: Skip {0} with {1}.".format(cur_model_id, cur_evaluation_id), 1,
                         debug_lvl)
        '''

        evaluated_models_and_ref = meta_mng.get_all_evalutated_models_and_references(cur_evaluation_id)
        # print(evaluated_models_and_ref)
        if (evaluated_models_and_ref is None) or (len(evaluated_models_and_ref) == 0):
            Debug.dl("plot_evaluations_logic: Evaluation {0} is not related on Evaluation matrix.".format(cur_evaluation_id),
                     1, debug_lvl)
            continue

        for cur_model_id in sc_model_ids:
            for cur_evalref_id in evaluated_models_and_ref:
                if cur_model_id == cur_evalref_id[0]:
                    the_script = meta_mng.get_evaluation_generator_script_of_scevaluation(cur_evaluation_id, debug_lvl)
                    the_call = "{0} {1} {2} -ref {3} -runsetid {4}".format(the_script, cur_model_id, the_timestamp,
                                                                           cur_evalref_id[1], sc_runset_id)
                    Debug.dl("plot_evaluations_logic: Will execute '{0}'.".format(the_call), 1, debug_lvl)
                    os.system(the_call)

    return


def generate_evaluations_hist(sc_model_ids, sc_evaluation_ids, sc_runset_id, metafile_mng, timestamp_min=None,
                              timestamp_max=None, debug_lvl=0):
    """

    :param sc_model_ids:
    :param sc_evaluation_ids:
    :param sc_runset_id:
    :param timestamp_min:
    :param timestamp_max:
    :param metafile_mng:
    :param debug_lvl:
    :return:
    """

    # load needed meta information
    metafile_mng.load_evaluation_matrix(debug_lvl=debug_lvl)
    if (timestamp_min is None) or (timestamp_max is None):
        metafile_mng.load_scrunset_meta_info(debug_lvl=debug_lvl)

    timestamp_ini = metafile_mng.get_runset_timestamp_ini() if timestamp_min is None else timestamp_min
    timestamp_end = metafile_mng.get_runset_timestamp_end() if timestamp_min is None else timestamp_max

    # basic check
    if (timestamp_ini is None) or (timestamp_end is None):
        Debug.dl("plot_evaluations_logic: Missing initial or final timestamp ({0}/{1}).".format(timestamp_min,
                                                                                              timestamp_max), 1,
                 debug_lvl)
        return

    for cur_evaluation_id in sc_evaluation_ids:

        evaluated_models_and_ref = metafile_mng.get_all_evalutated_models_and_references(cur_evaluation_id)

        if (evaluated_models_and_ref is None) or (len(evaluated_models_and_ref) == 0):
            Debug.dl("plot_evaluations_logic: Evaluation {0} is not related on Evaluation matrix.".format(cur_evaluation_id),
                     1, debug_lvl)
            continue

        for cur_model_id in sc_model_ids:
            for cur_evalref_id in evaluated_models_and_ref:
                if cur_model_id == cur_evalref_id[0]:

                    the_script = metafile_mng.get_evaluation_generator_hist_script_of_scevaluation(cur_evaluation_id,
                                                                                                   debug_lvl)

                    # basic check
                    if the_script is None:
                        Debug.dl("plot_evaluations_logic: Missing evaluation script for {0}.".format(cur_evaluation_id),
                                 1, debug_lvl)
                        continue

                    # execute command
                    the_call = "{0} {1} -ref {2} -runsetid {3} -tmin {4} -tmax {5}".format(the_script, cur_model_id,
                                                                                           cur_evalref_id[1],
                                                                                           sc_runset_id, timestamp_ini,
                                                                                           timestamp_end)
                    Debug.dl("plot_evaluations_logic: Will execute '{0}'.".format(the_call), 1, debug_lvl)
                    os.system(the_call)

    return
