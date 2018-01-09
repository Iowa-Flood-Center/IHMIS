import sys

from libs.settingsloader_lib import SettingsLoader
settings = SettingsLoader.load_settings(track_util=True, debug_lvl=1)
from libs.generalrequestvalidator_lib import GeneralRequestValidator
from console_call import ConsoleCall
from debug import Debug

default_debug_level = 1

# ####################################################### ARGS ####################################################### #

# help argument
if ConsoleCall.calls_help(sys.argv):
    print("Verify if a given General Request is valid.")
    print("Usage: python validade.py [-file FILE_PATH] [-str JSON_STR] [-verbose] [-debug DBG_LEVEL]")
    print(" - FILE_PATH : Path for a JSON file.")
    print(" -  JSON_STR : JSON string.")
    print(" -  -verbose : If this flag is present, use verbose mode.")
    print(" - DBG_LEVEL : Integer. Debug level. 0 (only critical errors) up to 4 (show all). Default: {0}"
        .format(default_debug_level))
    print(" Output: Return 1 if was able to check that given file is valid, 0 otherwise")
    quit(0)

# get arguments
file_path = ConsoleCall.get_arg_str("-file", sys.argv)
json_str = ConsoleCall.get_arg_str("-str", sys.argv)
verbosity = ConsoleCall.get_arg_flag("-verbose", sys.argv)
debug_lvl = ConsoleCall.get_arg_int("-debug", sys.argv, default_value=default_debug_level)

# check arguments
if (file_path is None) and (json_str is None):
    Debug.dl("validate: Not given any of the mandatory arguments (-file, -str)", 1, debug_lvl)
    quit(1)
elif (file_path is not None) and (json_str is not None):
    Debug.dl("validate: Only one of the arguments [-file, -str] is expected. Both provided.", 1, debug_lvl)
    quit(1)

# ####################################################### CALL ####################################################### #

if file_path is not None:
    GeneralRequestValidator.validate_file(file_path, debug_lvl=debug_lvl)
elif json_str is not None:
    GeneralRequestValidator.validate_string(json_str, debug_lvl=debug_lvl)
else:
    print("Unexpected event.")
