import time
import sys

from logic.clean_imported_data_logic import clean_historical
from logic.libs.MetaFileManager import MetaFileManager
from logic.libs.ConsoleCall import ConsoleCall
from logic.libs.Debug import Debug

debug_lvl = 20
previous_max_days = 10.5  # for how many days historical evaluation data must be hold  # TODO - include in argument

# ####################################################### ARGS ####################################################### #

any_error = False
unix_timestamp = None
default_runset_id = 'realtime'

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Usage: python clean_imported_data.py [-model_sing_id SC_MODEL_ID] [-reference_id SC_REFERENCE_ID] [-t TIMESTAMP] [-runsetid RUNSET_ID]")
    print(" - SC_MODEL_ID: a sc_model_id. If None, cleans all.")
    print(" - SC_REFERENCE_ID: a sc_reference_id. If None, cleans all.")
    print(" - TIMESTAMP: integer timestamp in seconds for the higher time accepted. If null, gets the most updated of the folder")
    print(" - RUNSET_ID: a sc_runset_id. If None, assumes 'realtime'")
    quit()

# get arguments
model_id = ConsoleCall.get_arg_str("-model_sing_id", sys.argv)
reference_id = ConsoleCall.get_arg_str("-reference_id", sys.argv)
runset_id = ConsoleCall.get_arg_str("-runsetid", sys.argv)
runset_id = default_runset_id if runset_id is None else runset_id

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
meta_mng.load_all_screference_meta_info(debug_lvl=debug_lvl)

# test arguments
try:
    unix_timestamp = ConsoleCall.get_arg_int("-t", sys.argv)
except ValueError:
    Debug.dl("clean_imported_data: Provided timestamp ({0}) is not an integer.".format(sys.argv[3]), 0, debug_lvl)
    any_error = True

# check model id argument
if not ((model_id is None) or (model_id == 'all') or meta_mng.scmodel_exists(model_id)):
    Debug.dl("clean_imported_data: Provided model id ({0}) not accepted.".format(model_id), 0, debug_lvl)
    any_error = True

# check reference id argument
if not ((reference_id is None) or (reference_id == 'all') or meta_mng.screference_exists(reference_id)):
    Debug.dl("clean_imported_data: Provided reference id ({0}) not accepted.".format(reference_id), 0, debug_lvl)
    any_error = True

# check timestamp argument
if (unix_timestamp is not None) and (unix_timestamp < 0):
    Debug.dl("clean_imported_data: Provided timestamp ({0}) is negative.".format(unix_timestamp), 0, debug_lvl)
    any_error = True

# ####################################################### DEFS ####################################################### #

# start counting time for debug
start_time = time.time() if debug_lvl > 0 else None

if any_error:
    print("For more information, use 'clean_imported_data.py -h' ")
else:
    if model_id is None:
        considered_model_ids = None
    elif model_id == 'all':
        considered_model_ids = meta_mng.get_all_scmodel_ids()
    else:
        considered_model_ids = [model_id]

    if reference_id is None:
        considered_reference_ids = None
    elif reference_id == 'all':
        considered_reference_ids = meta_mng.get_all_screference_ids()
    else:
        considered_reference_ids = [reference_id]

    print("Checking models: {0}".format(considered_model_ids))
    # quit(0)

    clean_historical(considered_model_ids, considered_reference_ids, runset_id, unix_timestamp, previous_max_days,
                     debug_lvl=debug_lvl)

# debug info
d_time = time.time()-start_time
Debug.dl("clean_imported_data: clean_historical({0}, {1}, {2}) function took {3} seconds ".format(model_id,
                                                                                                  reference_id,
                                                                                                  unix_timestamp,
                                                                                                  d_time), 1, debug_lvl)
