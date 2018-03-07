# Frontend - Tools

These are useful pieces of code that can be eventually used for a variety of purposes.

## Cleaning the ```/tmp/``` directory

Eventually, while testing, the ```/tmp/``` may get overloaded with files owned by *Apache* user.

Access the page ```clean_tmp.php``` and all Runset Request-related files will be deleted.

## Publishing the code

Before publishing a web code, it is considered a good practice to use minimize the ```javascript``` code.

For doing it, call:

    $ python publish.py

**NOTE:** before using it, some variables need to be set on the `settings` script.
