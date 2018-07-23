import time
import sys

from logic.clean_historical_results_logic import clean_historical
from logic.libs.MetaFileManager import MetaFileManager
from logic.libs.ConsoleCall import ConsoleCall
from logic.libs.Debug import Debug

debug_lvl = 20
any_error = False
unix_timestamp = None

# ####################################################### ARGS ####################################################### #

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Usage: python clean_historical_results.py [-m SC_MODEL_ID] [-mcomb SC_MODELCOMB_ID] [-e SC_EVALUATION_ID] [-c SC_COMPARISON_ID] [-t TIMESTAMP] [-runsetid SC_RUNSET_ID]")
    print(" - SC_MODEL_ID: a sc_model id or 'all'.")
    print(" - SC_MODELCOMB_ID: a sc_model_combination id or 'all'.")
    print(" - SC_COMPARISON_ID: a comparison id (in the format 'model1_model2') or 'all'.")
    print(" - SC_EVALUATION_ID: a sc_evaluation id or 'all'.")
    print(" - TIMESTAMP: integer timestamp in seconds for the higher time accepted. If null, gets the most updated of the folder")
    print(" - SC_RUNSET_ID: a sc_runset_id. If None, assumes 'realtime'.")
    quit()

# get arguments
model_id = ConsoleCall.get_arg_str("-m", sys.argv)
modelcomb_id = ConsoleCall.get_arg_str("-mcomb", sys.argv)
evaluation_id = ConsoleCall.get_arg_str("-e", sys.argv)
reference_id = ConsoleCall.get_arg_str("-r", sys.argv)
representation_id = ConsoleCall.get_arg_str("-rep", sys.argv)
comparison_id = ConsoleCall.get_arg_str("-c", sys.argv)
runset_id = ConsoleCall.get_arg_str("-runset_id", sys.argv)

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_scmodelcomb_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_scevaluation_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_screpresentation_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_screpresentationcomp_meta_info(debug_lvl=debug_lvl)
meta_mng.load_comparison_matrix(debug_lvl=debug_lvl)
meta_mng.load_evaluation_matrix(debug_lvl=debug_lvl)

# get timestamp
try:
    unix_timestamp = ConsoleCall.get_arg_int("-t", sys.argv)
except ValueError:
    Debug.dl("clean_intermediate_binaries: Provided timestamp ({0}) is not an integer.".format(sys.argv[3]), 0, debug_lvl)
    any_error = True

# check model id argument
if not ((model_id is None) or (model_id == 'all') or meta_mng.scmodel_exists(model_id)):
    Debug.dl("clean_historical_results: Provided model id ({0}) not accepted.".format(model_id), 0, debug_lvl)
    any_error = True

# check model comb id argument
if not ((modelcomb_id is None) or (modelcomb_id == 'all') or meta_mng.scmodelcomb_exists(model_id)):
    Debug.dl("clean_historical_results: Provided model combination id ({0}) not accepted.".format(modelcomb_id), 0,
             debug_lvl)
    any_error = True

# check evaluation id argument
if not ((evaluation_id is None) or (evaluation_id == 'all') or meta_mng.scevaluation_exists(evaluation_id)):
    Debug.dl("clean_historical_results: Provided evaluation id ({0}) not accepted.".format(model_id), 0, debug_lvl)
    any_error = True

# check reference id argument
if not ((reference_id is None) or (reference_id == 'all') or meta_mng.screference_exists(reference_id)):
    Debug.dl("clean_historical_results: Provided reference id ({0}) not accepted.".format(reference_id), 0, debug_lvl)
    any_error = True

# check representation id argument
if not ((representation_id is None) or (representation_id == 'all') or
            meta_mng.screpresentation_exists(representation_id)):
    Debug.dl("clean_historical_results: Provided representation id ({0}) not accepted.".format(representation_id), 0,
             debug_lvl)
    any_error = True

# check comparison id argument
if not ((comparison_id is None) or (comparison_id == 'all') or meta_mng.comparison_exists(comparison_acronym=comparison_id, debug_lvl=debug_lvl)):
    Debug.dl("clean_historical_results: Provided comparison id ({0}) not accepted.".format(comparison_id), 0, debug_lvl)
    any_error = True

# check timestamp argument
if (unix_timestamp is not None) and (unix_timestamp < 0):
    Debug.dl("clean_historical_results: Provided timestamp ({0}) is negative.".format(unix_timestamp), 0, debug_lvl)
    any_error = True

# set up arguments
model_ids = meta_mng.get_all_scmodel_ids() if ((model_id is None) or (model_id == 'all')) else [model_id]
if (modelcomb_id is None) or (modelcomb_id == 'all'):
    modelcomb_ids = meta_mng.get_all_scmodelcomb_ids()
else:
    modelcomb_ids = [modelcomb_id]
refr_ids = meta_mng.get_all_screference_ids() if ((reference_id is None) or (reference_id == 'all')) else [reference_id]
repr_ids = meta_mng.get_all_screpresentation_ids() if ((representation_id is None) or (representation_id == 'all')) \
    else [representation_id]
cmpr_ids = []  # TODO
eval_ids = meta_mng.get_all_scevaluation_ids() if (evaluation_id is None) or (evaluation_id == 'all') else \
    [evaluation_id]

# ####################################################### CALL ####################################################### #

# start counting time for debug
start_time = time.time() if debug_lvl > 0 else None

if any_error:
    print("For more information, use 'clean_historical_results.py -h' ")
else:
    clean_historical(model_ids, modelcomb_ids, refr_ids, repr_ids, cmpr_ids, eval_ids, unix_timestamp, runset_id, meta_mng,
                     debug_lvl=debug_lvl)

# debug info
d_time = time.time()-start_time
Debug.dl("clean_historical_results: clean_historical({0}, {1}, {2}) function took {3} seconds ".format(model_id,
                                                                                                       reference_id,
                                                                                                       unix_timestamp,
                                                                                                       d_time), 1,
         debug_lvl)
