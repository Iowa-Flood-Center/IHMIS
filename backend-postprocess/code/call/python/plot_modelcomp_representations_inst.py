import sys

from logic.plot_modelcmpr_representations_logic import generate_cmprsimp_representations
from logic.libs.MetaFileManager import MetaFileManager
from logic.libs.ConsoleCall import ConsoleCall
from logic.libs.Debug import Debug

debug_lvl = 2
default_runset_id = "realtime"

# ####################################################### ARGS ####################################################### #

any_error = False
unix_timestamp = None  # may be changed by argument
models_comparison_list = None

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Usage: python plot_modelcomp_representations_inst.py [-model_sing_1_id MODEL_ID -model_sing_2_id MODEL_ID] [-t TIMESTAMP] [-runsetid RUNSET_ID]")
    print(" - MODEL_ID: a sc_model id. If None, assumes all comparisons possible.")
    print(" - TIMESTAMP: integer timestamp in seconds. If null, gets the most updated of the database")
    print(" - RUNSET_ID: a runset id. If None, assumes 'realtime'")
    quit()

# get and check runset id
runset_id = ConsoleCall.get_arg_str("-runset_id", sys.argv)
runset_id = default_runset_id if runset_id is None else runset_id

# load meta information
meta_mng = MetaFileManager(runset_id=runset_id)
meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)

# check model id arguments: or both are set um and not None, or none should be given
model_id1 = ConsoleCall.get_arg_str('-model_sing_1_id', sys.argv)
model_id2 = ConsoleCall.get_arg_str('-model_sing_2_id', sys.argv)
if (model_id1 is not None) and (model_id2 is not None):
    meta_mng.load_all_scmodel_meta_info()
    meta_mng.load_comparison_matrix(debug_lvl=debug_lvl)
    if not meta_mng.scmodel_exists(model_id1):
        Debug.dl("plot_modelcomp_representations_inst: Provided model id ({0}) not accepted.".format(model_id1), 0, debug_lvl)
        any_error = True
    if not meta_mng.scmodel_exists(model_id2):
        Debug.dl("plot_modelcomp_representations_inst: Provided model id ({0}) not accepted.".format(model_id2), 0, debug_lvl)
        any_error = True
    if not meta_mng.comparison_exists(sc_model1=model_id1, sc_model2=model_id2):
        Debug.dl("plot_modelcomp_representations_inst: Model comparison ({0} x {1}) not defined.".format(model_id1,
                                                                                                         model_id2),
                 0, debug_lvl)
        any_error = True
    if not any_error:
        models_comparison_list = ["{0}_{1}".format(model_id1, model_id2)]
elif (model_id1 is None) and (model_id2 is None):
    meta_mng.load_comparison_matrix(debug_lvl=debug_lvl)
    models_comparison_list = meta_mng.get_all_comparison_acronyms()
else:
    Debug.dl("plot_modelcomp_representations_inst: Provided model id ({0}) not accepted.".format(model_id2), 0, debug_lvl)

# check timestamp argument
try:
    unix_timestamp = ConsoleCall.get_arg_int('-t', sys.argv)
    if (unix_timestamp is not None) and (unix_timestamp < 0):
        Debug.dl("Provided timestamp ({0}) is negative.".format(unix_timestamp), 0, debug_lvl)
        any_error = True
except ValueError:
    Debug.dl("Provided timestamp ({0}) is not an integer.".format(ConsoleCall.get_arg_str('-t', sys.argv)), 0,
             debug_lvl)
    any_error = True

# ####################################################### CALL ####################################################### #

if any_error:
    print("For more information, use 'plot_cmprsimp_representations.py -h' ")
else:
    generate_cmprsimp_representations(models_comparison_list, unix_timestamp, runset_id, debug_lvl=debug_lvl)
