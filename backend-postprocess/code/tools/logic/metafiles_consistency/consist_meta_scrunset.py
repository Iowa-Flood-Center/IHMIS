#!/usr/bin/env python
from libs.MetaFilesConsistEvaluator import MetaFilesConsistEvaluator
from libs.ConsoleCall import ConsoleCall
import sys

output_format = 1

# ####################################################### ARGS ####################################################### #

if (len(sys.argv) == 1) or ('-print' in sys.argv):
    output_format = 1
elif '-exit' in sys.argv:
    output_format = 2
else:
    print("Invalid argument: {0}".format(sys.argv))
    quit()

runset_id = ConsoleCall.get_arg_str("-runsetid", sys.argv)

# ####################################################### CALL ####################################################### #

is_ok = MetaFilesConsistEvaluator.evaluate_runset(runset_id=runset_id)

if output_format == 1:
    printed = "Runset is OK" if is_ok else "Runset is bad"
    print(printed)
elif output_format == 2:
    exit_code = 0 if is_ok else 1
    sys.exit(exit_code)
