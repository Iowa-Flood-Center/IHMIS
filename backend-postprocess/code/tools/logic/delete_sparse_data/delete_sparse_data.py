#!/usr/bin/env python
import sys
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append("{0}/../../../call/python/logic/libs".format(cur_dir))
from FilenameDefinition import FilenameDefinition

# ######################################## ARGS ###################################### #

# basic check - existence of arguments
if len(sys.argv) < 2:
    print("Missing folder path. Skipping.")
    quit(0)
elif len(sys.argv) < 3:
    print("Missing link id. Skipping.")
    quit(0)

# get arguments
folder_path = sys.argv[1]
link_id = sys.argv[2]

# basic check - arguments content
if not os.path.exists(folder_path):
    print("Folder not found: {0}. Skipping.".format(folder_path))
    quit(0)
try:
    link_id = int(link_id)
except Exception:
    print("Unable to convert link id '{0}' to integer. Skipping.".format(link_id))
    quit(0)

# ######################################## CALL ###################################### #

all_file_names = os.listdir(folder_path)
print("Checking {0} files.".format(len(all_file_names)))

count_del = 0
for cur_file_name in all_file_names:
    cur_link_id = FilenameDefinition.obtain_hist_file_linkid(cur_file_name)
    if cur_link_id == link_id:
        print("Deleting: {0}".format(cur_file_name))
        cur_file_path = os.path.join(folder_path, cur_file_name)
        os.remove(cur_file_path)
        count_del += 1

print("Deleted {0} files.".format(count_del))
