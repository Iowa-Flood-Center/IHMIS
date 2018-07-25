import Debug


class ParamFldidxusgsih:
    _ancillaryOnDemand = None

    def __init__(self):
        return

    @staticmethod
    def set_ancillary_on_demand(aod):
        ParamFldidxusgsih._ancillaryOnDemand = aod

    @staticmethod
    def to_vect_classify(link_id, qraw_value):
        the_thresholds = ParamFldidxusgsih._ancillaryOnDemand.get_fidx_thresholds()[link_id]
        try:
            if qraw_value == 0:
                return 0
            elif qraw_value < the_thresholds[0]:
                return 1
            elif qraw_value < the_thresholds[1]:
                return 2
            elif qraw_value < the_thresholds[2]:
                return 3
            elif qraw_value < the_thresholds[3]:
                return 4
            else:
                return 5
        except IndexError:
            Debug.dl("ParamFldidxusgsih: "
                     "IndexError - type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                     len(qraw_value),
                                                                                                     link_id),
                     0, debug_lvl)
            return None
        except ValueError:
            Debug.dl("ParamFldidxusgsih: "
                     "ValueError: type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                                    len(qraw_value),
                                                                                                    link_id),
                     0, debug_lvl)
            return None
