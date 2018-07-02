# Third Party

Codes and tools developed my third party developers.

## jq-linux64

Tool for translating json-structured files into bash-language variables.

Usage:

Suppose the JSON file located at ```SETTINGS_FILE``` contains a dictionary with the attribute ```folder_path```. In order to read this attribute into the bash variable FDP, one can execute the following command: 

    FDP=$(./jq-linux64 -r '.folder_path' ${SETTINGS_FILE})

For more information about this tool, access the creators [site](https://stedolan.github.io/jq/).