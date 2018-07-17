import os

from libs.MetaFileManager import MetaFileManager
from libs.Debug import Debug


# #################################################################################################################### #
# ####################################################### DEFS ####################################################### #
# #################################################################################################################### #

def generate_cmpd_representations(sc_modelcombs_ids, sc_runset_id, unix_timestamp, debug_lvl=0):
    """

    :param sc_modelcombs_ids:
    :param sc_runset_id:
    :param unix_timestamp:
    :param debug_lvl:
    :return:
    """

    # basic checks
    if (sc_modelcombs_ids is None) or (type(sc_modelcombs_ids) is not list):
        Debug.dl("plot_cmpd_representations_logic: First argument must be a list of sc_model_combination_ids.", 0,
                 debug_lvl)
        return
    if sc_runset_id is None:
        Debug.dl("plot_cmpd_representations_logic: Invalid runset_id: '{0}'.".format(sc_runset_id), 0, debug_lvl)
        return

    # creating guiding objects
    meta_mng = MetaFileManager(runset_id=sc_runset_id)
    meta_mng.load_all_scmodelcomb_meta_info(debug_lvl=debug_lvl)
    meta_mng.load_all_screpresentationcomp_meta_info(ignore_fails=False, debug_lvl=debug_lvl)

    # preparing arguments
    the_timestamp_arg = "" if unix_timestamp is None else "-t {0}".format(unix_timestamp)

    # for each representation of each module, run its plotting function
    for cur_sc_modelcomb_id in sc_modelcombs_ids:
        cur_reprcmpd_ids = meta_mng.get_all_representationcomps_of_scmodelcomb(cur_sc_modelcomb_id, debug_lvl=debug_lvl)
        Debug.dl("plot_cmpd_representations_logic: For '{0}':{1}.".format(cur_sc_modelcomb_id, cur_reprcmpd_ids), 1,
                 debug_lvl)

        for cur_reprcmpd_id in cur_reprcmpd_ids:

            the_script = meta_mng.get_genscript_of_representation_cmpd(cur_reprcmpd_id, debug_lvl=debug_lvl)
            call_command = "{0} -modelcomb {1} -runsetid {2} {3}".format(the_script, cur_sc_modelcomb_id, sc_runset_id,
                                                                         the_timestamp_arg)
            Debug.dl("plot_cmpd_representations_logic: Calling '{0}'.".format(call_command), 1, debug_lvl)
            os.system(call_command)
