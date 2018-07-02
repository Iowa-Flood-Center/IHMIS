#!/bin/bash

# This script ...
# $1: String. Runset ID to have the metafiles uploaded [mandatory]
# $2: String. Expects 'upload' or 'hold' [optional]

# ###################################### CONS ###################################### #

LOGIC_FOLDER="logic/metafiles_consistency/"
SETTINGS_FILE="../../conf/settings.json"

# define config file reader
JQ_FOLDER="../../../common/util/third-party/"       #
JQ_EXEC="jq-linux64"                                # JSON reader tool
JQ="./../../../common/util/third-party/jq-linux64"  #

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

get_local_metafiles_sbx_folder() {
  RET=$(${JQ} -r '.raw_data_folder_path' ${SETTINGS_FILE})
  RET=${RET}"data/runsets/"${1}"/metafiles_sandbox/"
  echo ${RET}
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
echo " TODO"

# ###################################### DONE ###################################### #

echo ""
echo "Done."
