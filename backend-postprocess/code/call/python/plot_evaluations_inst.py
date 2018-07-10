import time
import sys

from logic.plot_evaluations_logic import generate_evaluations
from logic.libs.MetaFileManager import MetaFileManager
from logic.libs.ConsoleCall import ConsoleCall
from logic.libs.Debug import Debug

debug_lvl = 20

# ####################################################### ARGS ####################################################### #

any_error = False
unix_timestamp = None
runset_id = None
default_runset_id = 'realtime'

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Usage: python plot_evaluations_inst.py SC_MODEL_ID SC_EVALUATION_ID [-t TIMESTAMP] [-runset_id RUNSET_ID]")
    print(" - SC_MODEL_ID: a sc_model_id or 'all'")
    print(" - SC_EVALUATION_ID: a sc_evaluation_id or 'all'")
    print(" - TIMESTAMP: integer timestamp in seconds. If null, gets the most updated of the database")
    print(" - RUNSET_ID: a sc_runset_id. If None, assumes 'realtime'")
    quit()

# get and check runset id
runset_id = ConsoleCall.get_arg_str("-runset_id", sys.argv)
runset_id = default_runset_id if runset_id is None else runset_id

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_scevaluation_meta_info(debug_lvl=debug_lvl)

# check model id argument
model_id = ConsoleCall.get_arg_str("-model_sing_id", sys.argv)
if model_id is None:
    Debug.dl("plot_evaluations_inst: Must provide at least one model id, or 'all'.", 0, debug_lvl)
    any_error = True
elif model_id == 'all':
    model_id = None
elif not meta_mng.scmodel_exists(model_id):
    Debug.dl("plot_evaluations_inst: Provided model id ({0}) not accepted.".format(model_id), 0, debug_lvl)
    any_error = True

# check evaluation id argument
evaluation_id = ConsoleCall.get_arg_str("-evaluation_id", sys.argv)
if evaluation_id is None:
    Debug.dl("plot_evaluations_inst: Must provide at least one evaluation id, or 'all'.", 0, debug_lvl)
    any_error = True
elif evaluation_id == 'all':
    evaluation_id = None
elif not meta_mng.scevaluation_exists(evaluation_id):
    Debug.dl("plot_evaluations_inst: Provided model id ({0}) not accepted.".format(evaluation_id), 0, debug_lvl)
    any_error = True

# check timestamp argument
try:
    unix_timestamp = ConsoleCall.get_arg_int("-t", sys.argv)
    if (unix_timestamp is not None) and (unix_timestamp < 0):
        Debug.dl("plot_evaluations_inst: Provided timestamp ({0}) is negative.".format(unix_timestamp), 0, debug_lvl)
        any_error = True
except ValueError:
    Debug.dl("plot_evaluations_inst: Provided timestamp ({0}) is not an integer.".format(sys.argv[3]), 0, debug_lvl)
    any_error = True

# ####################################################### CALL ####################################################### #

# start counting time for debug
start_time = time.time() if debug_lvl > 0 else None

if any_error:
    print("For more information, use 'plot_evaluations.py -h' ")
else:
    considered_model_ids = [model_id] if model_id is not None else meta_mng.get_all_scmodel_ids()
    considered_evaluation_ids = [evaluation_id] if evaluation_id is not None else meta_mng.get_all_scevaluation_ids()
    generate_evaluations(considered_model_ids, considered_evaluation_ids, runset_id, unix_timestamp,
                         debug_lvl=debug_lvl)

# debug info
d_time = time.time()-start_time
Debug.dl("plot_evaluations_inst: generate_evaluations({0}) function took {1} seconds ".format(model_id, d_time), 1, debug_lvl)
