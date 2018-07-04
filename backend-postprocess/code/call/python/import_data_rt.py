import logic.import_data_rt_logic as logic
import argparse
import sys

debug_lvl = 10

# ####################################### ARGS ###################################### #

# define arguments
parser = argparse.ArgumentParser(description='Create all binary files.')
parser.add_argument('-model_sing_id', metavar='MODEL_SING_ID', type=str, required=True,
                    help="a sc_model_sing id or 'all' for all available models")
parser.add_argument('-runset_id', metavar='RUNSET_ID', type=str, required=True,
                    help="a sc_runset id or 'all' for all available models")

# read arguments
args = parser.parse_args()

# ####################################### CALL ###################################### #

logic.import_data(args.runset_id, sc_model_id=args.model_sing_id, debug_lvl=debug_lvl)
