#!/bin/bash

# This script ...
# $1: String. Folder with sparse data to be clean [mandatory]
# $2: Integer. Link id to be removed [mandatory]

# ###################################### CONS ###################################### #

PYTHON_SCRIPT="logic/delete_sparse_data/delete_sparse_data.py"

# ###################################### ARGS ###################################### #

# basic check
if [ $# -lt 1 ]; then
  echo "Missing folder path argument."
  exit
elif [ $# -lt 2 ]; then
  echo "Missing link id argument."
  exit
fi

# ###################################### CALL ###################################### #

# move to current file directory
cd "$(dirname "$0")"

CMD="python "${PYTHON_SCRIPT}" "${1}" "${2}
echo "CALL: "${CMD}
eval ${CMD}

echo ""
echo "Done."
