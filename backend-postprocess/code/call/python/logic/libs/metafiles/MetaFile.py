from ..Debug import Debug
import string
import json


class MetaFile:

    _json_object = None
    _root_object_tag = None

    def __init__(self, file_path, debug_lvl=0):
        self.load_json(file_path, debug_lvl=debug_lvl)

    def load_json(self, file_path, debug_lvl=0):

        with open(file_path, 'r') as json_file:
            try:
                Debug.dl("MetaFile: Reading file '{0}'.".format(file_path), 3, debug_lvl)
                printable = set(string.printable)
                raw_file_content = json_file.read().strip()
                file_content = filter(lambda x: x in printable, raw_file_content)  # remove encoding problems
                json_all_obj = json.loads(file_content)
                self._json_object = json_all_obj[self._root_object_tag]
            except ValueError, e:
                Debug.dl("MetaFile: Error parsing '{0}'.".format(file_path), 3, debug_lvl)
