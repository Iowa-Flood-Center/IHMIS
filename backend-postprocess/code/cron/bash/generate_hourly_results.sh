#!/bin/bash

# head to the file directory
cd "$(dirname "$0")"

# ###################################### DEFS ###################################### #

# define config file reader
JQ="./../../../../third-party/jq-linux64"                           # JSON reader tool
CFG_FILE="../../../conf/settings.json"

SC_RUNSET_ID="realtime"
LOCAL_PY_FOLDER="../../call/python/"

# ###################################### CALL ###################################### #

echo "Started at: "$(date)

echo ""
echo "###############################################################################"

echo "SH: Importing data..."
echo "SH: Now it is "$(date)

CMD="python "${LOCAL_PY_FOLDER}"import_data_rt.py -model_sing_id all -runset_id "${SC_RUNSET_ID}
## echo "SH: Executing: "${CMD}
## eval ${CMD}
echo "SH: Would execute: "${CMD}

echo ""
echo "###############################################################################"

echo "SH: Plotting single models representations..."
echo "SH: Now it is "$(date)

CMD="python "${LOCAL_PY_FOLDER}"plot_modelsing_representations.py -model_sing_id all -runset_id "${SC_RUNSET_ID}
echo "SH: Executing: "${CMD}
eval ${CMD}
## echo "SH: Would execute: "${CMD}

echo ""
echo "###############################################################################"

echo "SH: Plotting reference representations..."
echo "SH: Now it is "$(date)

CMD="python "${LOCAL_PY_FOLDER}"plot_reference_representations.py -reference_id all -runset_id "${SC_RUNSET_ID}
echo "SH: Executing: "${CMD}
eval ${CMD}
## echo "SH: Would execute: "${CMD}

echo ""
echo "###############################################################################"

echo "SH: Plotting evaluations..."
echo "SH: Now it is "$(date)

CMD="python "${LOCAL_PY_FOLDER}"plot_evaluations_inst.py -model_sing_id all -evaluation_id all -runset_id "${SC_RUNSET_ID}
echo "SH: Executing: "${CMD}
eval ${CMD}
## echo "SH: Would execute: "${CMD}

echo ""
echo "###############################################################################"
echo ""
echo "Ended at: "$(date)