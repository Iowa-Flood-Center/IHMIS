import time
import sys

from logic.plot_modelsing_representations_logic import generate_singsimp_representations
from logic.libs.MetaFileManager import MetaFileManager
from logic.libs.ConsoleCall import ConsoleCall
from logic.libs.Debug import Debug


debug_lvl = 20
default_runset_id = "realtime"

# ####################################################### ARGS ####################################################### #

any_error = False
unix_timestamp = None  # may be changed by argument
runset_id = None

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Usage: python plot_modelsing_representations.py MODEL_ID [-t TIMESTAMP] [-runsetid RUNSET_ID]")
    print(" - MODEL_ID: a model id, or all")
    print(" - TIMESTAMP: integer timestamp in seconds. If null, gets the most updated of the database")
    print(" - RUNSET_ID: a runset id. If None, assumes 'realtime'")
    quit()

# get and check runset id
runset_id = ConsoleCall.get_arg_str("-runset_id", sys.argv)
runset_id = default_runset_id if runset_id is None else runset_id

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)

# check model id argument
model_id = ConsoleCall.get_arg_str("-model_sing_id", sys.argv)
if model_id is None:
    Debug.dl("plot_modelsing_representations_lib: Must provide at least one model id, or 'all'.", 0, debug_lvl)
    any_error = True
elif model_id == 'all':
    model_id = None
elif not meta_mng.scmodel_exists(model_id):
    Debug.dl("plot_modelsing_representations_lib: Provided model id ({0}) not accepted.".format(model_id), 0, debug_lvl)
    any_error = True

# check timestamp argument
try:
    unix_timestamp = ConsoleCall.get_arg_int('-t', sys.argv)
    if (unix_timestamp is not None) and (unix_timestamp < 0):
        Debug.dl("plot_modelsing_representations_lib: Provided timestamp ({0}) is negative.".format(sys.argv[2]), 0, debug_lvl)
        any_error = True
except ValueError:
    Debug.dl("plot_modelsing_representations_lib: Provided timestamp ({0}) is not an integer.".format(sys.argv[2]), 0, debug_lvl)
    any_error = True

# ####################################################### CALL ####################################################### #

# start counting time for debug
start_time = time.time() if debug_lvl > 0 else None

if any_error:
    print("For more information, use 'plot_modelsing_representations.py -h' ")
elif model_id is not None:
    generate_singsimp_representations([model_id], runset_id, unix_timestamp, debug_lvl=debug_lvl)
else:
    generate_singsimp_representations(meta_mng.get_all_scmodel_ids(), runset_id, unix_timestamp, debug_lvl=debug_lvl)

# debug info
d_time = time.time()-start_time
Debug.dl("plot_modelsing_representations_lib: update_local_bins_from_hdf5({0}) function took {1} seconds ".format(model_id,
                                                                                                              d_time),
         1, debug_lvl)
