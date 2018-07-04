#!/bin/bash

# head to the file directory and load lib files
cd "$(dirname "$0")"
source bash/libs/mini_log_rotate.shlib

# ###################################### DEFS ###################################### #

# define config file reader
JQ="./../../../common/util/third-party/jq-linux64"    # JSON reader tool
CFG_FILE="../../conf/settings.json"

# get log folder location
LOC_RAW_FOLDER=$(${JQ} -r '.raw_data_folder_path' ${CFG_FILE})
LOG_RAW_FOLDER=${LOC_RAW_FOLDER}"logs/"

LOG_BASENAME="generate_hourly_results"
SH_FILE="bash/generate_hourly_results.sh"

# ###################################### CALL ###################################### #

### SET UP LOGS ####################
mini_log_rotate ${LOG_RAW_FOLDER} ${LOG_BASENAME} ${SH_FILE}
