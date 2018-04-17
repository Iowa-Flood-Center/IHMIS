# Backend - Post-Process - Code - Call - Python

This folder contains the interface files for most of the features in the *Backend-PostProcess* component of IHMIS.

## Basic file structure

Each file has the only objective of parsing system calls arguments and call the appropriate function in the corresponding *_logic* file located at the *logic* folder.

**Example:** when executed, the file  *import_data_rt.py* only parses the system arguments provided and call appropriated function imported from *logic/import_data_rt.py*

## Naming convention

Each file is designed to perform a single, independent activity. Some files are designed only for the *realtime* runsets, other for *historical* runsets. Thus, they are named using the basic convention:

    [verb]_[substantive]_[runset-type].py

In which *[verb]* is the action performed, *[substantive]* is the target object and *[runset-type]* should get the values *rt* for the *real-time runset* or *ht* for *historical runsets*

**Example:** import_data_rt.py

## Help argument

All files in this folder have *-h* option for help on system calls.

**Example:** in order to get more information about how to use *import_data.py*, execute the command:

    python import_data.py -h