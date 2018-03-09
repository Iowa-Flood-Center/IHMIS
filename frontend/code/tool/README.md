# Frontend - Tools

These are useful pieces of code that can be eventually used for a variety of purposes.

## Cleaning the ```/tmp/``` directory

Eventually, while testing, the ```/tmp/``` may get overloaded with files owned by *Apache* user.

Just access the page ```clean_tmp.php``` and all Runset Request-related files will be deleted.

## Publishing the code

Before publishing a web code, it is considered a good practice to use minimize (it is: uglify) the *javascript* code.

For doing it, one can call the *python* script:

    $ python publish.py

This script will read the copy all the files in the ``SETTINGS:dev_code_folder_path`` and copy to the ``SETTINGS:dst_code_folder_path``, keeping the same folder structure and minimizing all non-minified *javascript* files found.
