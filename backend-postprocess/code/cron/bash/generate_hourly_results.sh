#!/bin/bash

# head to the file directory
cd "$(dirname "$0")"

# ###################################### DEFS ###################################### #

# define config file reader
JQ="./../../../../third-party/jq-linux64"                           # JSON reader tool
CFG_FILE="../../../conf/settings.json"

SC_RUNSET_ID="realtime"
LOCAL_PY_FOLDER="../../call/python/"

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
will_call "${CMD}" true

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting single models representations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_modelsing_representations.py -model_sing_id all -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" true

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting reference representations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_reference_representations.py -reference_id all -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" true

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting evaluations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_evaluations_inst.py -model_sing_id all -evaluation_id all -runset_id "${SC_RUNSET_ID}
will_call "${CMD}" true

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Plotting compound representations..."
CMD="python "${LOCAL_PY_FOLDER}"plot_cmpd_representations.py all"
will_call "${CMD}" true

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Updating files to be displayed..."
CMD="python "${LOCAL_PY_FOLDER}"update_display.py -model_sing_id all -reference_id all -rep all -e all -c all"
will_call "${CMD}" true

echo -e ${H_LINE}  # ---------------------------------------------------

echo "SH: Cleaning historical results..."
CMD="TODO"
will_call "${CMD}" false

echo -e ${H_LINE}  # ---------------------------------------------------

echo "Ended at: "$(date)
