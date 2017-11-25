#!/bin/bash

echo "Running at '"$(date)"' with "$SHELL

which more
more -V

echo "Moving to directory."
cd "$(dirname "$0")"

echo "Reading settings file."
settings_file_content=$(more settings.json)

# echo "Read:"
# echo $settings_file_content

echo "Cleaning settings content."
settings_file_content=$( echo $settings_file_content | sed -e 's#::::::::.*::::::::##')

echo "Processing file content."
runset_folder_path=$(echo $settings_file_content | ./jq -r '.runset_folder_path')
echo "Got folder path '"$runset_folder_path"'."

general_script="run_communicate_server54_directly.sh"

for cur_dir in ${runset_folder_path}* ; do

  echo "Evaluating directory '"$cur_dir"'."

  # ignore files
  if [ -f ${cur_dir} ]; then
    continue
  fi
  
  # ignore non-timestamp named folders
  cur_dir_name=$(basename ${cur_dir})
  if ! [[ $cur_dir_name =~ ^[0-9]+$ ]] ; then
    continue
  fi
  
  # define flag files
  cur_flag_file_path=${cur_dir}"/runsetid.txt"
  cur_done_file_path=${cur_dir}"/done.txt"
  
  # check if 'done.txt' file exists
  if ! [ -f ${cur_flag_file_path} ]; then
    if ! [ -f ${cur_done_file_path} ]; then
      echo "Still processing '"${cur_dir_name}"' at "$(date)"."
      continue
	else
      echo "Runset at '"${cur_dir_name}"' is done."
      continue
    fi
  fi
  
  # process properly
  ### cur_runsetid=$(more ${cur_flag_file_path})
  cur_runsetid=`cat ${cur_flag_file_path}`
  
  # remove flag file
  rm ${cur_flag_file_path}
  
  # execute everything
  echo "Processing runset: '"${cur_runsetid}"' ("${cur_dir_name}")."
  
  log_file_path=${cur_dir}/log.txt
  sh ${general_script} ${cur_runsetid} ${cur_dir_name} > ${log_file_path} 2>&1
  echo "Executing 'sh ${general_script} ${cur_runsetid} ${cur_dir_name} > ${log_file_path} 2>&1'."
  
  # add extra flag file
  touch ${cur_done_file_path}
  
  # remove HF5 files
  cur_h5_folder_path=${cur_dir}"/outputs/"
  rm -r ${cur_h5_folder_path}*
done

echo "Done at '"$(date)"'."
