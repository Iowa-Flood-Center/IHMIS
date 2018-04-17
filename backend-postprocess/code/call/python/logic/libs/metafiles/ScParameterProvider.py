

# TODO - delete this class - everything must go to Meta Files
class ScParameterProvider:
    _parameters = {'ss': 'Soil total Storage',
                   'sl': 'Soil top Layer moisture',
                   'p03': 'precipitation of last 03 hours',
                   'p06': 'precipitation of last 06 hours',
                   'p12': 'precipitation of last 12 hours',
                   'p24': 'precipitation of last 24 hours',
                   'r03': 'runoff of last 03 hours',
                   'r06': 'runoff of last 06 hours',
                   'r12': 'runoff of last 12 hours',
                   'r24': 'runoff of last 24 hours',
                   'qraw': 'raw discharge',
                   'q': 'unit discharge',
                   'qindex': 'flood index',
                   'ff': 'future flood',
                   'fq': 'future discharge'}

    def __init__(self):
        return
