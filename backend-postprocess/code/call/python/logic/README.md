# Logic

Each Python script in this folder holds a function that is expected to be called by an importing script. They where **not** supposed to be called directly by python system calls.

They are expected to be imported by the files in the parent folder only by the script with similar name, but without the ```_logic``` sufix.

*Example:* The file ```.../logic/update_display_logic.py``` is imported by ```.../update_display.py```.