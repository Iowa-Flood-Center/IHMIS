# Common

This sub-component holds libraries, tools and definitions used by more than one of the main components (*frontend*, *backend-modelrun*, *backend-postprocessing*).

## Tools overview

Each folder in this directory contains a different tool and is structured following the default folder structure of the major components. Such folders are described as follows:

### general-request

Tools and libraries for dealing with General Requests.

### util

Libraries with very generic functions used by multiple projects.

## Development patterns

Some notes for developers.

### Reading settings 

All tools should have a copy of the ```SettingsLoader.py``` file in their ```code-libs``` folder.

The reference file is in the ```general-request``` tool.

In order to read the settings, interface scripts should start with something similar to:

    from libs.SettingsLoader import SettingsLoader
    settings = SettingsLoader.load_settings(debug_lvl=1)

### Importing ```util``` packages

When calling ```SettingsLoader.load_settings(debug_lvl=1)```, set the argument ```track_util=True``` and them import required classes.

Example:

    settings = SettingsLoader.load_settings(track_util=True, debug_lvl=1)
    from console_call import ConsoleCall
    