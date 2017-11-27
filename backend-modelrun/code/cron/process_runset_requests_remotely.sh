#!/bin/bash

# go to file dir and load config file
cd "$(dirname "$0")"
source libs/config.shlib
source libs/datelog.shlib
CONF_FILE="../../conf/system.conf"

# get arguments
runsetid=$1
curtimestamp=$2

# define local logs and requests folder
RREQUEST_FOLDER=$(config_get $CONF_FILE RREQUEST_FOLDER)
src_root_dir=${RREQUEST_FOLDER}${curtimestamp}"/"
src_meta_dir=${src_root_dir}"metafiles_sandbox/"
src_bins_dir=${src_root_dir}"outputs/"

# define remote processing server settings
remote_user=$(config_get $CONF_FILE PROCSERV_USERNM)
remote_addr=$(config_get $CONF_FILE PROCSERV_ADDRES)
remote_addr=${remote_user}"@"${remote_addr}
dst_root_dir=$(config_get $CONF_FILE PROCSERV_RSTFDR)"${runsetid}/"
dst_meta_dir="${dst_root_dir}metafiles_sandbox/"
dst_bins_dir="${dst_root_dir}files/bins_input/"
log_folder_path=$(config_get $CONF_FILE PROCSERV_LOGFDR)"generate_runset_representations_"
ext_foldergen_script=$(config_get $CONF_FILE PROCSERV_FGNFPH)
ext_represgen_script=$(config_get $CONF_FILE PROCSERV_RGNFPH)

# set some flags - useful for debugging - 0:no, 1:yes
setup_dir_tree=0
upload_metafiles=0
upload_hdf5files=0
execute_bash=1

# load python module
eval $(config_get $CONF_FILE CMD_LOAD_PYTHON)

### execute - outputs to std-out

{
  echo "Processing '"${src_root_dir}"'."

  # create folders
  if ! [ $setup_dir_tree -eq 0 ] ; then
    cur_command="ssh "${remote_addr}" python "${ext_foldergen_script}" -runsetid "${runsetid}
    echo "  Executing: '"${cur_command}"'."
    eval ${cur_command}
  fi

  # send hdf5 files
  if ! [ $upload_hdf5files -eq 0 ] ; then
    cur_command="scp -rp "${src_bins_dir}"* "${remote_addr}":"${dst_bins_dir}
    echo "  Executing: '"${cur_command}"'."
    eval ${cur_command}
  fi

  # send meta files
  if ! [ $upload_metafiles -eq 0 ] ; then
    cur_command="scp -r "${src_meta_dir}"* "${remote_addr}":"${dst_meta_dir}
    echo "  Executing: '"${cur_command}"'."
    eval ${cur_command}
  fi

  # send hdf5 files
  if ! [ $upload_hdf5files -eq 0 ] ; then
    cur_command="scp -rp "${src_bins_dir}"* "${remote_addr}":"${dst_bins_dir}
    echo "  Executing: '"${cur_command}"'."
    eval ${cur_command}
  fi

  # perform post-processing effective steps
  if ! [ $execute_bash -eq 0 ] ; then
    ssh_command="bash ${ext_represgen_script} ${runsetid}"
    log_path=${log_folder_path}${runsetid}".log"
    ssh_call="${ssh_command} >> ${log_path} 2>&1"
    cur_command="ssh "${remote_addr}" '"${ssh_call}"'"
    echo "  Executing: "${cur_command}"."
    eval ${cur_command}
  fi
  
  echo "Executed remote caller script."
}
