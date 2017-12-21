#!/bin/bash -l

# go to file dir and load config file
cd "$(dirname "$0")"
source libs/config.shlib
source libs/datelog.shlib
CONF_FILE="../../conf/system.conf"

# define log file path
LOG_FILE_PATH=$(config_get $CONF_FILE FPH_PREF_ICINFO)
LOG_FILE_PATH=$LOG_FILE_PATH$(datelog_get)".log"

# load python module
eval $(config_get $CONF_FILE CMD_LOAD_PYTHON)

### execute the Python script in its own working directory
{

  echo "Calling script as user '"$USER"'."
  python ../call/initcond_availability_informer.py
  echo "Finished 'initcond_availability_informer.sh'."

} &> $LOG_FILE_PATH
