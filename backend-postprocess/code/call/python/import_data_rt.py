import logic.import_data_rt_logic as logic
import argparse
import sys

debug_lvl = 10

# ####################################################### ARGS #########################################################

# define arguments
parser = argparse.ArgumentParser(description='Create all binary files.')


# read arguments
args = parser.parse_args()

# ####################################################### CALL #########################################################

print("Hello python world")
print("Imported: {0}".format(logic.import_data("realtime", debug_lvl=debug_lvl)))
