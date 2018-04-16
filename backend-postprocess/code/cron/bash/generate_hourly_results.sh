#!/bin/bash

# head to the file directory
cd "$(dirname "$0")"

# ########################################## DEFS ########################################## #

# define config file reader
JQ="./third_party/jq-linux64"                                               # JSON reader tool
CFG_FILE="../../../conf/settings.json"

RUNSET_ID="realtime"
LOCAL_PY_FOLDER="../../call/python/"

# ########################################## CALL ########################################## #

echo "Started at: "$(date)

echo ""
echo "#######################################################################################"
echo "SH: Generating binary files."
python ${LOCAL_PY_FOLDER}create_binaries.py all -runsetid realtime

echo ""
echo "#######################################################################################"
echo ""
echo "Ended at: "$(date)