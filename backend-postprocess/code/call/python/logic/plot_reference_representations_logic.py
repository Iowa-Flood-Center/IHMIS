import os

from libs.MetaFileManager import MetaFileManager
from libs.Debug import Debug


def generate_references_representations(sc_references_ids, sc_runset_id, unix_timestamp, debug_lvl=0):
    """

    :param sc_references_ids:
    :param sc_runset_id:
    :param unix_timestamp:
    :param debug_lvl:
    :return:
    """

    # basic check
    if (sc_references_ids is None) or (type(sc_references_ids) is not list):
        Debug.dl("plot_reference_representations_logic: First argument must be a list of sc_references_ids.", 0,
                 debug_lvl)
        return

    # basic check
    if sc_runset_id is None:
        Debug.dl("plot_singsimp_representations_lib: Invalid runset_id: '{0}'.".format(sc_runset_id), 0, debug_lvl)
        return

    # creating guiding objects
    meta_mng = MetaFileManager(runset_id=sc_runset_id)
    meta_mng.load_all_screference_meta_info(debug_lvl=debug_lvl)
    meta_mng.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)

    # preparing arguments
    the_timestamp_arg = "" if unix_timestamp is None else unix_timestamp
    cur_runset_arg = "-runsetid {0}".format(sc_runset_id)

    # for each representation of each reference, run its plotting function
    for cur_sc_reference_id in sc_references_ids:

        cur_repr_ids = meta_mng.get_all_representations_of_screference(cur_sc_reference_id)

        if cur_repr_ids is None:
            continue

        for cur_repr_id in cur_repr_ids:
            reprgen_script = meta_mng.get_genscript_of_representation_sing(cur_repr_id)
            call_command = "{0} {1} {2} {3}".format(reprgen_script, cur_sc_reference_id, the_timestamp_arg,
                                                    cur_runset_arg)
            Debug.dl("plot_reference_representations_logic: Calling '{0}' ({1}).".format(call_command, cur_repr_id),
                     2, debug_lvl)
            os.system(call_command)
