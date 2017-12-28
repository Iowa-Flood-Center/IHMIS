#!/bin/bash -l

# set up environment similar to the logged user one
. /etc/profile

# go to file dir and load config file
cd "$(dirname "$0")"
source libs/config.shlib
source libs/datelog.shlib
CONF_FILE="../../conf/system.conf"

# define log file path
LOG_FILE_PATH=$(config_get $CONF_FILE FPH_PREF_RETRIV_MERGE)
LOG_FILE_PATH=$LOG_FILE_PATH$(datelog_get)".log"

### execute the Python script in its own working directory
{
  echo "Calling script as user '"$USER"' at "$(date)"."

  # load python module
  echo "Running '"$(config_get $CONF_FILE CMD_LOAD_PYTHON)"'"
  eval $(config_get $CONF_FILE CMD_LOAD_PYTHON)

  python ../call/retrieve_runsetmerge_requests.py
  echo "Finished 'retrieve_runset_requests.sh' at "$(date)"."
 
} &> $LOG_FILE_PATH
