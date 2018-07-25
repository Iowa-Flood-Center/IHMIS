#!/bin/bash

# head to the file directory
cd "$(dirname "$0")"

# ###################################### DEFS ###################################### #

# define config file reader
JQ="./../../../../third-party/jq-linux64"                           # JSON reader tool
CFG_FILE="../../../conf/settings.json"

SC_RUNSET_ID="realtime"
LOCAL_PY_FOLDER="../../call/python/"

CALL_IMPORT_DATA=true      # Step 01: Import data
CALL_PLOT_SINGREPR=true    # Step 02: Plot single model representations
CALL_PLOT_REFRREPR=true    # Step 03: Plot references representation
CALL_PLOT_CMPRREPR=true    # Step 04: Plot model comparisons
CALL_PLOT_EVALUAT=true     # Step 05: Plot evaluations
CALL_PLOT_CMPDREPR=true    # Step 06: Plot compound representations
CALL_UPDATE_DISPLAY=true   # Step 07: Upldate images to be displayed
CALL_CLEAN_IMPORT=true     # Step 08: Clean imported files
CALL_CLEAN_HIST=true       # Step 09: Clean historical files

H_LINE="\n###############################################################################"

# ###################################### FUNC ###################################### #

# Executes a command only if the second argument says so
# $1: String. Command to be executed.
# $2: Boolean. True if command $1 will be called. False otherwise.
will_call(){
  if [ $# -ne 2 ] || [ "$2" != "true" ]; then
    echo "SH: Would execute: "${1}
  else
    echo "SH: Now it is "$(date)
    echo "SH: Executing: "${1}
    eval ${1}
  fi
}

# ###################################### CALL ###################################### #

echo "Started at: "$(date)

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Importing data..."
CMD="python "${LOCAL_PY_FOLDER}"import_data_rt.py -model_sing_id all -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" ${CALL_IMPORT_DATA}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting single models representations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_modelsing_representations_inst.py -model_sing_id all -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" ${CALL_PLOT_SINGREPR}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting model comparison representations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_modelcomp_representations_inst.py -runset_id"${SC_RUNSET_ID}
will_call "${CMD}" ${CALL_PLOT_CMPRREPR}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting reference representations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_reference_representations.py -reference_id all -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" ${CALL_PLOT_REFRREPR}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting evaluations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_evaluations_inst.py -model_sing_id all -evaluation_id all -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" ${CALL_PLOT_EVALUAT}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting compound representations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_cmpd_representations.py all"
will_call "${CMD}" ${CALL_PLOT_CMPDREPR}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Updating files to be displayed..."
CMD="python "${LOCAL_PY_FOLDER}"update_display.py -model_sing_id all -reference_id all -rep all -e all -c all"
will_call "${CMD}" ${CALL_UPDATE_DISPLAY}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Cleaning imported data..."
CMD="python "${LOCAL_PY_FOLDER}"clean_imported_data.py -model_sing_id all -reference_id all"
will_call "${CMD}" ${CALL_CLEAN_IMPORT}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Cleaning historical results..."
CMD="python "${LOCAL_PY_FOLDER}"clean_historical_results.py -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" ${CALL_CLEAN_HIST}

echo -e ${H_LINE}  # ---------------------------------------------------

echo "Ended at: "$(date)
