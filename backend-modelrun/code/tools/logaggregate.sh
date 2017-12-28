#!/bin/bash

# constant
FILE_AGGR_NAME="aggregate.log"

# argument-based
FILE_SEARCH=$1
FILE_AGGR_PATH=$(dirname "${FILE_SEARCH}")"/"$FILE_AGGR_NAME

# create aggregated file
for CURRENT_FILE in $FILE_SEARCH;
do
  more $CURRENT_FILE >> $FILE_AGGR_PATH
done

# delete remaining files
rm $FILE_SEARCH

echo "Done."