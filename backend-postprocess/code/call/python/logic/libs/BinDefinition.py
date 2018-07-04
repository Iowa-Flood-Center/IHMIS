from DataFileDefinition import DataFileDefinition


class BinDefinition(DataFileDefinition):
    _ext_states = '.npy'
    _ext_timeseries = '.p'
    _ext_sparse_data = '.p'

    @classmethod
    def get_file_ext(cls, sc_parameter):
        if sc_parameter in ['fq', 'istg', 'fsstg']:
            return cls._ext_timeseries
        elif sc_parameter in ['isdc']:
            return cls._ext_sparse_data
        else:
            return cls._ext_states
