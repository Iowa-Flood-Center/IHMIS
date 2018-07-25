from Debug import Debug


class ParamDisclausgsih:
    _ancillaryOnDemand = None
    _data_month = None

    def __init__(self):
        return

    @staticmethod
    def set_ancillary_on_demand(aod):
        ParamDisclausgsih._ancillaryOnDemand = aod

    @staticmethod
    def set_data_month(data_month):
        ParamDisclausgsih._data_month = data_month

    @staticmethod
    def to_vect_classify(link_id, qraw_value):
        the_thresholds = ParamDisclausgsih._ancillaryOnDemand.get_qunit_thresholds(ParamDisclausgsih._data_month)[link_id]
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
            Debug.dl("ParamDisclausgsih: IndexError - "
                     "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                        len(qraw_value), link_id))
            return None
        except ValueError:
            print("ParamDisclausgsih: ValueError - "
                  "type of qraw_value is '{0}', size is {1}, tried index {2}".format(type(qraw_value),
                                                                                     len(qraw_value), link_id))
            return None
