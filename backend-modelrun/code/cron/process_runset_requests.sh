#!/bin/bash

# go to file dir and load config file
cd "$(dirname "$0")"
source libs/config.shlib
source libs/datelog.shlib
CONF_FILE="../../conf/system.conf"

# define process script, folders and flags
PROCESS_SCRIPT="process_runset_requests_remotely.sh"
NEW_FLAG_FILE="runsetid.txt"
DONE_FLAG_FILE="done.txt"
FPH_INNE_PROCES=$(config_get $CONF_FILE FPH_INNE_PROCES)
RREQUEST_FOLDER=$(config_get $CONF_FILE RREQUEST_FOLDER)
RARCHIVE_FOLDER=$(config_get $CONF_FILE RARCHIVE_FOLDER)
DELETE_OUTFILES=$(config_get $CONF_FILE DELETE_OUTFILES)

# define log file path
LOG_FILE_PATH=$(config_get $CONF_FILE FPH_PREF_PROCES)
LOG_FILE_PATH=$LOG_FILE_PATH$(datelog_get)".log"

# set some flags - useful for debugging - 0:no, 1:yes
move_to_archive=1

### execute commands

{
  echo "Running at '"$(date)"' using "$SHELL
  echo "Requests folder path: '"$RREQUEST_FOLDER"'."
  
  for cur_dir in ${RREQUEST_FOLDER}* ; do

    # ignore files and non-timestamp named folders
    if [ -f ${cur_dir} ]; then
      continue
    fi
    cur_dir_name=$(basename ${cur_dir})
    if ! [[ $cur_dir_name =~ ^[0-9]+$ ]] ; then
      continue
    fi
	
	echo "Evaluating directory '"$cur_dir"'."
  
    # define flag files
    cur_flag_file_path=${cur_dir}"/"${NEW_FLAG_FILE}
    cur_done_file_path=${cur_dir}"/"${DONE_FLAG_FILE}
  
    # check if 'done.txt' file exists
    if ! [ -f ${cur_flag_file_path} ]; then
      if ! [ -f ${cur_done_file_path} ]; then
        echo "Runset at '"${cur_dir_name}"' is being processed."
        continue
	  else
        echo "Runset at '"${cur_dir_name}"' is done."
        continue
      fi
    else
      echo "Runset at '"${cur_dir_name}"' will be processed."
    fi
  
    # get runset id
    cur_runsetid=`cat ${cur_flag_file_path}`
    echo "Processing runset: '"${cur_runsetid}"' ("${cur_dir_name}")."

    # remove 'runsetid' flag file
    rm ${cur_flag_file_path}

    # call remote post-processing script
    log_file_path=${FPH_INNE_PROCES}${cur_runsetid}".log"
	postprocess_cmd="bash ${PROCESS_SCRIPT} ${cur_runsetid} ${cur_dir_name} > ${log_file_path} 2>&1"
    echo "Executing '"${postprocess_cmd}"'."
    eval ${postprocess_cmd}
  
    # add extra flag file
    touch ${cur_done_file_path}
  
    # remove HF5 files if specified to
    if [ "$DELETE_OUTFILES" = true ] ; then
      echo "Deleting output files."
      cur_h5_folder_path=${cur_dir}"/outputs/"
      rm -r ${cur_h5_folder_path}*
    fi
	
    # move to archive
    if [ $move_to_archive -eq 1 ] ; then
      arch_dir=${RARCHIVE_FOLDER}${cur_runsetid}"/"
	  mv ${cur_dir} ${arch_dir}
      echo "Moved to archive."
    else
      echo "Skipped moving to archive."
    fi
    
  done

  echo "Done at '"$(date)"'."
} &> $LOG_FILE_PATH
