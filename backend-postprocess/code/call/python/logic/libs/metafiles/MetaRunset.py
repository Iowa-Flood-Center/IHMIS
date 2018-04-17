
class MetaRunset(MetaFile):

    _root_object_tag = "sc_runset"

    def get_id(self):
        """

        :return:
        """

        return str(self._json_object["id"])

    def get_title(self):
        """

        :return:
        """

        return str(self._json_object["title"])

    def get_timestamp_ini(self):
        """

        :return:
        """
        tag = 'timestamp_ini'
        if tag not in self._json_object.keys():
            return None
        else:
            return int(self._json_object[tag])

    def get_timestamp_end(self):
        """

        :return:
        """
        tag = 'timestamp_end'
        return None if tag not in self._json_object.keys() else int(self._json_object[tag])
