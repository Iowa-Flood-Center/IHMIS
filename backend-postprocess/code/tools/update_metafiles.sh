#!/bin/bash

# This script ...
# $1: String. Runset ID to have the metafiles uploaded [mandatory]
# $2: String. Expects 'upload' or 'hold' [optional]

# ###################################### CONS ###################################### #

LOGIC_FOLDER="logic/metafiles_consistency/"
SETTINGS_FILE="../../conf/settings.json"

# define config file reader
JQ="./../../../common/util/third-party/jq-linux64"  # JSON reader tool

# ###################################### ARGS ###################################### #

# basic check
if [ $# -lt 1 ]; then
  echo "Missing runset_id argument."
  exit
elif [ $# -gt 2 ]; then
  echo "It is expected no more than two arguments."
  exit
fi

SC_RUNSET_ID=$1
UPLOAD_FLAG=$2

if [ "$UPLOAD_FLAG" = "upload" ]; then
  UPLOAD_FLAG=1
elif [ "$UPLOAD_FLAG" = "hold" ]; then
  UPLOAD_FLAG=0
elif [ ! ${UPLOAD_FLAG} == 0 ]; then
  echo "Second argument expected to be 'upload' or 'hold'."
  exit
fi

# ###################################### DEFS ###################################### #

call_consist_script(){
  echo "Checking if ${1} meta files are consistent..."
  python "${LOGIC_FOLDER}${2}" -runsetid ${SC_RUNSET_ID} -exit
  interpret_consist_return "$1" $?
}

interpret_consist_return() {
  if [ ${2} == 0 ]; then
     echo " ${1} meta files are ok."
  else
     echo " ${1} meta files are INCONSISTENT."
     ALL_CONSISTENT=false
  fi
  echo ""
}

get_local_metafiles_eff_folder() {
  RET=$(${JQ} -r '.raw_data_folder_path' ${SETTINGS_FILE})
  RET=${RET}"data/runsets/"${1}"/metafiles/"
  echo ${RET}
}

#
# $1 : runset_id
# RETURN :
get_local_metafiles_sbx_folder() {
  RET=$(${JQ} -r '.raw_data_folder_path' ${SETTINGS_FILE})
  RET=${RET}"data/runsets/"${1}"/metafiles_sandbox/"
  echo ${RET}
}

# ########################################## DEF. SYSTEM

METAFILESEFF_FOLDER_NAME="metafiles"

#
# $1 : runset_id
# RETURN: String with path to folder (via echo)
# How to use: myvar = $(get_server_files_folder 'my_runset_id')
function get_frontend_files_folder {
  local TAG='.frontend_runsets_complete_folder_path'
  local FRONTEND_FOLDER=$(${JQ} -r ${TAG} ${SETTINGS_FILE})
  echo ${FRONTEND_FOLDER}${1}
}

#
# $1 : runset_id
# RETURN: String with path to folder in the frontend server (via echo)
function get_frontend_metafiles_folder {
	local LOCAL_FOLDER=$(get_frontend_files_folder ${1})
	echo ${LOCAL_FOLDER}"/"${METAFILESEFF_FOLDER_NAME}"/"
}

# ###################################### CALL ###################################### #

ALL_CONSISTENT=true

# move to current file directory
cd "$(dirname "$0")"

# checking consistency

call_consist_script "SC Runset" "consist_meta_scrunset.py"
call_consist_script "SC Models" "consist_meta_scmodels.py"
call_consist_script "SC References" "consist_meta_screferences.py"
call_consist_script "SC Products" "consist_meta_scproducts.py"
call_consist_script "SC Representations" "consist_meta_screpresentations.py"
call_consist_script "SC Evaluations" "consist_meta_scevaluation.py"
call_consist_script "SC Comparison Matrix" "consist_meta_comparison_matrix.py"
call_consist_script "SC Forecast Matrix" "consist_meta_forecast_matrix.py"
call_consist_script "SC Evaluation Matrix" "consist_meta_evaluation_matrix.py"
call_consist_script "SC Menu" "consist_meta_menu.py"


# ########################################## Updating if possible

if [ "$ALL_CONSISTENT" == false ]; then
	echo "INCONSISTENCY detected. Skipping update."
	exit
fi

echo "Updating metafiles..."

# setting up folders
LOCAL_METAEFF_FOLDER=$(get_local_metafiles_eff_folder $SC_RUNSET_ID)
LOCAL_METASBX_FOLDER=$(get_local_metafiles_sbx_folder $SC_RUNSET_ID)

# clean and update local meta files
echo " Deleting contents in folder: "
echo "  ${LOCAL_METAEFF_FOLDER}"
rm -rf $LOCAL_METAEFF_FOLDER

echo " Updating local meta files folder:"
echo "  From: ${LOCAL_METASBX_FOLDER}"
echo "  To  : ${LOCAL_METAEFF_FOLDER}"
cp -r $LOCAL_METASBX_FOLDER"." $LOCAL_METAEFF_FOLDER

echo ""

# ########################################## Uploading if requested

if [ -z ${UPLOAD_FLAG} ]; then
  echo "Holding files locally. Not uploading."
  exit
fi

echo "Uploading metafiles..."

SERVER_LOCATION=$(${JQ} -r '.frontend_server_location' ${SETTINGS_FILE})
FRONTEND_METAEFF_FOLDER=$(get_frontend_metafiles_folder ${SC_RUNSET_ID})

echo " Deleting current metafiles in the frontend server..."
CMD="ssh "${SERVER_LOCATION}" rm -rf "${FRONTEND_METAEFF_FOLDER}
echo "  Executing: "${CMD}
$(${CMD})

echo " Creating folder structure for the metafiles in the frontend server..."
CMD="ssh "${SERVER_LOCATION}" mkdir -p "${FRONTEND_METAEFF_FOLDER}
echo "  Executing: "${CMD}
$(${CMD})

echo " Uploading the meta files to the frontend server..."
FRONTEND_DST_FOLDER=${SERVER_LOCATION}":"${FRONTEND_METAEFF_FOLDER}
CMD="scp -r "${LOCAL_METAEFF_FOLDER}"* "${FRONTEND_DST_FOLDER}
echo "  Executing: "${CMD}
$(${CMD})

echo " Changing permissions of the files in the frontend server..."
dest_folder=$(get_frontend_files_folder ${SC_RUNSET_ID})
ssh_command="chmod -R ugo+rwx ${dest_folder}"
CMD="ssh "${SERVER_LOCATION}" "${ssh_command}
echo "  Executing: "${CMD}
$(${CMD})

# ###################################### DONE ###################################### #

echo ""
echo "Done."
