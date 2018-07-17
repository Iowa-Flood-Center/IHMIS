import time
import sys

from logic.update_display_logic import update_display
from logic.libs.MetaFileManager import MetaFileManager
from logic.libs.ConsoleCall import ConsoleCall
from logic.libs.Debug import Debug

debug_lvl = 4
unix_timestamp = None
default_runset_id = "realtime"

# ####################################################### ARGS ####################################################### #

any_error = False

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Usage: python update_display.py [-m SC_MODEL_ID] [-r SC_REFERENCE_ID] [-rep SC_REPRESENTATION_ID] [-c SC_COMPARISON_ID] [-e SC_EVALUATION_ID] [-t TIMESTAMP] [-runsetid SC_RUNSET_ID]")
    print(" - SC_MODEL_ID: a sc_model_id. If None, updates all.")
    print(" - SC_REFERENCE_ID: a sc_reference_id. If None, updates all.")
    print(" - SC_REPRESENTATION_ID: a sc_presentation_id. If None, updates all.")
    print(" - SC_COMPARISON_ID: a sc_comparison_id. If None, updates all.")
    print(" - SC_EVALUATION_ID: a sc_evaluation_id. If None, updates all.")
    print(" - TIMESTAMP: integer timestamp in seconds for the higher time accepted. If null, gets the most updated available")
    print(" - SC_RUNSET_ID: a sc_runset_id. If None, assumes 'realtime'.")
    quit()

# get arguments
model_id = ConsoleCall.get_arg_str("-model_sing_id", sys.argv)
reference_id = ConsoleCall.get_arg_str("-reference_id", sys.argv)
representation_id = ConsoleCall.get_arg_str("-rep", sys.argv)
comparison_id = ConsoleCall.get_arg_str("-c", sys.argv)
evaluation_id = ConsoleCall.get_arg_str("-e", sys.argv)
try:
    unix_timestamp = ConsoleCall.get_arg_int("-t", sys.argv)
except ValueError:
    Debug.dl("clean_historical_files: Provided timestamp ({0}) is not an integer.".format(sys.argv[3]), 0, debug_lvl)
    any_error = True
runset_id = ConsoleCall.get_arg_str("-runsetid", sys.argv)
runset_id = default_runset_id if runset_id is None else runset_id

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_scmodelcomb_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_screference_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_screpresentationcomp_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_scevaluation_meta_info(debug_lvl=debug_lvl)
meta_mng.load_comparison_matrix(debug_lvl=debug_lvl)

# check model id argument
if not ((model_id is None) or (model_id == 'all') or meta_mng.scmodel_exists(model_id)):
    Debug.dl("clean_historical_files: Provided model id ({0}) not accepted.".format(model_id), 0, debug_lvl)
    any_error = True

# check reference id argument
if not ((reference_id is None) or (reference_id == 'all') or meta_mng.screference_exists(reference_id)):
    Debug.dl("clean_historical_files: Provided reference id ({0}) not accepted.".format(reference_id), 0, debug_lvl)
    any_error = True

#
if not ((representation_id is None) or (representation_id == 'all') or meta_mng.screpresentation_exists(representation_id)):
    Debug.dl("clean_historical_files: Provided representation id ({0}) not accepted.".format(representation_id), 0, debug_lvl)
    any_error = True

# check evaluation id argument
if not ((evaluation_id is None) or (evaluation_id == 'all') or meta_mng.scevaluation_exists(evaluation_id)):
    Debug.dl("clean_historical_files: Provided evaluation id ({0}) not accepted.".format(evaluation_id), 0, debug_lvl)
    any_error = True

# check model id argument
if not ((comparison_id is None) or (comparison_id == 'all') or meta_mng.comparison_exists(comparison_acronym=comparison_id)):
    Debug.dl("clean_historical_files: Provided comparison id ({0}) not accepted.".format(comparison_id), 0, debug_lvl)
    any_error = True

# check timestamp argument
if (unix_timestamp is not None) and (unix_timestamp < 0):
    Debug.dl("clean_historical_files: Provided timestamp ({0}) is negative.".format(unix_timestamp), 0, debug_lvl)
    any_error = True

# ####################################################### DEFS ####################################################### #

# start counting time for debug
start_time = time.time() if debug_lvl > 0 else None

if any_error:
    print("For more information, use 'clean_historical_files.py -h' ")
else:
    # set up model argument
    if model_id is None:
        considered_model_ids = None
    elif model_id == 'all':
        considered_model_ids = meta_mng.get_all_scmodel_ids() + meta_mng.get_all_scmodelcomb_ids()
    else:
        considered_model_ids = [model_id]

    # set up reference argument
    if reference_id is None:
        considered_reference_ids = None
    elif reference_id == 'all':
        considered_reference_ids = meta_mng.get_all_screference_ids()
    else:
        considered_reference_ids = [reference_id]

    # set up representation argument
    if representation_id is None:
        considered_representation_ids = None
    elif representation_id == 'all':
        considered_representation_ids = meta_mng.get_all_screpresentation_ids() + \
                                        meta_mng.get_all_screpresentationcomp_ids()
    else:
        considered_representation_ids = [representation_id]

    # set up comparison argument
    if comparison_id is None:
        considered_comparison_ids = None
    elif comparison_id == 'all':
        considered_comparison_ids = meta_mng.get_all_comparison_acronyms()
    else:
        considered_comparison_ids = [comparison_id]

    # set up evaluation argument
    if evaluation_id is None:
        considered_evaluation_ids = None
    elif evaluation_id == 'all':
        considered_evaluation_ids = meta_mng.get_all_scevaluation_ids()
    else:
        considered_evaluation_ids = [evaluation_id]

    # run it
    update_display(considered_model_ids, considered_reference_ids, considered_representation_ids,
                   considered_comparison_ids, considered_evaluation_ids, unix_timestamp, meta_mng, runset_id=runset_id,
                   debug_lvl=debug_lvl)

# debug info
d_time = time.time()-start_time
Debug.dl("update_display: update_display({0}, {1}, {2}) function took {3} seconds ".format(model_id, evaluation_id,
                                                                                           unix_timestamp, d_time),
         1, debug_lvl)
