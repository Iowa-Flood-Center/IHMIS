import time
import sys

from logic.plot_cmpd_representations_logic import generate_cmpd_representations
from logic.libs.MetaFileManager import MetaFileManager
from logic.libs.ConsoleCall import ConsoleCall
from logic.libs.Debug import Debug

debug_lvl = 20
default_runset_id = "realtime"

# ####################################################### ARGS ####################################################### #

any_error = False

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Script for generating compound representation (of combined models)")
    print("Usage: python plot_cmpd_representations.py MODELCOMB_ID [-t TIMESTAMP] [-runsetid RUNSET_ID]")
    print(" - MODELCOMB_ID: a model combination id")
    print(" - TIMESTAMP: integer timestamp in seconds. If null, gets the most updated of the database")
    print(" - RUNSET_ID: a runset id. If None, assumes 'realtime'")
    quit()

# get and check runset id
runset_id = ConsoleCall.get_arg_str("-runsetid", sys.argv)
runset_id = default_runset_id if runset_id is None else runset_id

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodelcomb_meta_info(debug_lvl=debug_lvl)

# check modelcomb id argument
modelcomb_id = ConsoleCall.get_arg_str(1, sys.argv)
if modelcomb_id is None:
    Debug.dl("plot_cmpd_representations: Must provide at least one model combination id, or 'all'.", 0, debug_lvl)
    any_error = True
elif modelcomb_id == 'all':
    modelcomb_id = None
elif not meta_mng.scmodelcomb_exists(modelcomb_id):
    Debug.dl("plot_cmpd_representations: Provided model combination id ({0}) not accepted.".format(sys.argv[1]), 0,
             debug_lvl)
    any_error = True

# check timestamp argument
try:
    unix_timestamp = ConsoleCall.get_arg_int("-t", sys.argv)
    if (unix_timestamp is not None) and (unix_timestamp < 0):
        Debug.dl("plot_cmpd_representations: Provided timestamp ({0}) is negative.".format(unix_timestamp), 0,
                 debug_lvl)
        any_error = True
except ValueError:
    Debug.dl("plot_cmpd_representations: Provided timestamp is not an integer.", 0, debug_lvl)
    any_error = True

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodelcomb_meta_info(ignore_fails=False, debug_lvl=debug_lvl)

# ####################################################### CALL ####################################################### #

# start counting time for debug
start_time = time.time() if debug_lvl > 0 else None

if any_error:
    print("For more information, use 'plot_cmpd_representations.py -h' ")
elif modelcomb_id is not None:
    print("Considering {0}.{1}.".format(runset_id, [modelcomb_id]))
    generate_cmpd_representations([modelcomb_id], runset_id, unix_timestamp, debug_lvl=debug_lvl)
else:
    print("Will get_all_scmodelcomb_ids()")
    print("Considering {0}.{1}.".format(runset_id, meta_mng.get_all_scmodelcomb_ids()))
    generate_cmpd_representations(meta_mng.get_all_scmodelcomb_ids(), runset_id, unix_timestamp, debug_lvl=debug_lvl)

# debug info
d_time = time.time()-start_time
Debug.dl("plot_cmpd_representations: update_local_bins_from_hdf5({0}) function took {1} seconds ".format(modelcomb_id,
                                                                                                         d_time),
         1, debug_lvl)
