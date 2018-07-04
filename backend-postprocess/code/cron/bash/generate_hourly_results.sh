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
CMD="python "${LOCAL_PY_FOLDER}"import_data_rt.py all -runsetid "${SC_RUNSET_ID}
echo "SH: Executing: "${CMD}

echo ""
echo "###############################################################################"
echo ""
echo "Ended at: "$(date)