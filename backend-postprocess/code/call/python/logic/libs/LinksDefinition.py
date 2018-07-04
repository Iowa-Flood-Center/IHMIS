# TODO - this class should not be static


class LinksDefinition:
    _max_link_id = 620119
    _min_link_id = 22771

    @staticmethod
    def get_min_link_id():
        return LinksDefinition._min_link_id

    @staticmethod
    def get_max_link_id():
        return LinksDefinition._max_link_id

    def __init__(self):
        return
