import time
import sys

from logic.plot_reference_representations_logic import generate_references_representations
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
    print("Usage: python plot_reference_representations.py -reference_id REFERENCE_ID [TIMESTAMP]")
    print(" - REFERENCE_ID: a sc_reference_id or 'all'")
    print(" - TIMESTAMP: integer timestamp in seconds. If null, gets the most updated of the database")
    quit()

# get and check runset id
runset_id = ConsoleCall.get_arg_str("-runset_id", sys.argv)
runset_id = default_runset_id if runset_id is None else runset_id

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_screference_meta_info(debug_lvl=debug_lvl)

# check reference id argument
reference_id = ConsoleCall.get_arg_str("-reference_id", sys.argv)
if reference_id is None:
    Debug.dl("plot_reference_representations: Must provide at least one reference id, or 'all'.", 0, debug_lvl)
    any_error = True
elif reference_id == 'all':
    reference_id = None
elif not meta_mng.screference_exists(reference_id):
    Debug.dl("plot_reference_representations: Provided reference id ({0}) not accepted.".format(sys.argv[1]), 0,
             debug_lvl)
    any_error = True

# check timestamp argument
try:
    unix_timestamp = ConsoleCall.get_arg_int('-t', sys.argv)
    if (unix_timestamp is not None) and (unix_timestamp < 0):
        Debug.dl("plot_reference_representations: Provided timestamp ({0}) is negative.".format(sys.argv[2]), 0,
                 debug_lvl)
        any_error = True
except ValueError:
    Debug.dl("plot_reference_representations: Provided timestamp ({0}) is not an integer.".format(sys.argv[2]), 0,
             debug_lvl)
    any_error = True

# ####################################################### CALL ####################################################### #

# start counting time for debug
start_time = time.time() if debug_lvl > 0 else None

if any_error:
    print("For more information, use 'plot_reference_representations.py -h' ")
elif reference_id is not None:
    generate_references_representations([reference_id], runset_id, unix_timestamp, debug_lvl=debug_lvl)
else:
    generate_references_representations(meta_mng.get_all_screference_ids(), runset_id, unix_timestamp,
                                        debug_lvl=debug_lvl)

# debug info
d_time = time.time()-start_time
Debug.dl("plot_reference_representations: generate_references_representations({0}) function took {1} seconds ".format(
    reference_id, d_time), 1, debug_lvl)
