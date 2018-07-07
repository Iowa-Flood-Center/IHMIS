from __future__ import division
from osgeo import gdalnumeric
from PIL import Image
import numpy as np

from Debug import Debug


class ColorProvider:

    def __init__(self):
        return

    class ColorProvFather:

        def __init__(self):
            return

        @classmethod
        def get_color_index(cls, parameter_value):
            if parameter_value is None:
                return None
            for i, threshold in enumerate(cls._values):
                if parameter_value <= threshold:
                    return 0 if (i == 0) else (i - 1)

            return len(cls._values) - 2

        @classmethod
        def get_color_from_index(cls, color_index):
            return ((cls._r[color_index], cls._g[color_index], cls._b[color_index], cls._a[color_index]))

        @classmethod
        def get_rgba_matrix_from_numpy_matrix(cls, np_matrix):
            """
            Depends on [cls._r, cls._g, cls._b, cls._values] variables from child class.
            np_matrix: Numpy 2D matrix with raw/comparison values
            """

            if np_matrix is None:
                return None

            rgba = np.zeros((4, np_matrix.shape[0], np_matrix.shape[1],), np.uint8)
            for i in range(0, len(cls._values) - 1):  # for each threshold
                mask = np.logical_and(np_matrix > cls._values[i],
                                      np_matrix <= cls._values[i + 1])  # define a True/False mask
                palette_color = (cls._r[i], cls._g[i], cls._b[i], cls._a[i])
                for j in range(4):  # apply the color at index with True
                    rgba[j] = np.choose(mask, (rgba[j], palette_color[j]))

            return rgba

    class ColorProvSingFather(ColorProvFather):
        """
        Color definition for single model
        """

        def __init__(self):
            return

        @classmethod
        def get_pixel_color(cls, parameter_value):
            """
            Requires from all subclasses having _r, _g, _b, _a vector attributes
            """
            color_index = cls.get_color_index(parameter_value)
            return cls.get_color_from_index(color_index)

    class ColorProvCompFather(ColorProvFather):
        """
        Color definition for comparison model
        """

        def __init__(self):
            return

        @classmethod
        def get_pixel_color(cls, model1_value, model2_value, par1=None, debug=False):
            """
            Requires from all subclasses having _r, _g, _b, _a vector attributes
            Requires from all subclasses having compare() method
            """
            if par1 is None:
                parameter_value = cls.compare(model1_value, model2_value)
            else:
                parameter_value = cls.compare(model1_value, model2_value, par1)
            color_index = cls.get_color_index(parameter_value)
            if debug:
                print("- Inputs: " + str(model1_value) + " and " + str(model2_value))
                print("- Comparison value: " + str(parameter_value))
                print("- Colour index value: " + str(color_index))

            # print "Values: " + str(model1_value) + " and " + str(model2_value)
            # print "Param: " + str(parameter_value) + ", index: " + str(color_index)
            return cls.get_color_from_index(color_index)

    class ColorProvSS(ColorProvSingFather):
        """
        Soil Storage
        """
        _values = [-1, 0, 0.1, 0.2, 0.3, 0.4, 10000]
        _r = [0, 255, 161, 65, 44, 37]
        _g = [0, 255, 218, 182, 127, 52]
        _b = [0, 204, 180, 196, 184, 148]
        _a = [0, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvSL(ColorProvSingFather):
        """
        Soil Moisture
        """
        _inf = float('inf')
        # _values = [-_inf, -0.00000000000001, 0.0, 0.1, 0.2, 0.6, 0.8, _inf]
        # _r =            [0,               255, 255, 161,  65,  44,  37]
        # _g =            [0,               255, 255, 218, 182, 127,  52]
        # _b =            [0,               255, 204, 180, 196, 184, 148]
        # _a =            [0,               255, 255, 255, 255, 255, 255]

        _values = [-_inf, -0.000000001, 0.2, 0.4, 0.6, 0.8, _inf]
        _r = [0, 255, 161, 65, 44, 37]
        _g = [0, 255, 218, 182, 127, 52]
        _b = [0, 204, 180, 196, 184, 148]
        _a = [0, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvPd(ColorProvSingFather):
        """
        Precipitation
        """
        _values = np.asarray([-1, 0.01, 0.10, 0.25, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5,
                              1000]) / 39.37  # convert from inches(display) to m(DB)
        _r = [0, 191, 80, 0, 221, 170, 82, 255, 247, 230, 240, 171, 54]
        _g = [0, 255, 210, 166, 255, 255, 189, 255, 227, 153, 47, 0, 37]
        _b = [0, 233, 250, 212, 153, 0, 0, 112, 0, 0, 34, 0, 0]
        _a = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvP(ColorProvSingFather):
        """
        Precipitation
        """
        _values = np.asarray(
            [-1, 0, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 1000]) / 39.37  # convert from inches(display) to m(DB)
        _r = [0, 191, 80, 0, 221, 170, 82, 255, 247, 230, 240, 171, 54]
        _g = [0, 255, 210, 166, 255, 255, 189, 255, 227, 153, 47, 0, 37]
        _b = [0, 233, 250, 212, 153, 0, 0, 112, 0, 0, 34, 0, 0]
        _a = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvR(ColorProvP):
        """
        Runoff
        """
        _do = None  # identical to Precipitation

        def __init__(self):
            return

    class ColorProvQUnit(ColorProvSingFather):
        _values = [-1, 0, 1, 2, 3, 4, 1000]
        _r = [0, 255, 161, 65, 44, 37]
        _g = [0, 255, 218, 182, 127, 52]
        _b = [0, 204, 180, 196, 184, 148]
        _a = [0, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvQraw:
        _value_range = [0, 750]  # m3/sec
        _r_range = [0, 0]
        _g_range = [0, 0]
        _b_range = [50, 250]
        _a_range = [0, 255]

        def __init__(self):
            return

        @classmethod
        def get_color(cls, parameter_value):

            # basic check - if not in interval, quit it
            if (parameter_value < cls._value_range[0]) and (parameter_value > cls._value_range[1]):
                return [0, 0, 0, 0]

            r_value = cls._get_color_component(parameter_value, cls._r_range)
            g_value = cls._get_color_component(parameter_value, cls._g_range)
            b_value = cls._get_color_component(parameter_value, cls._b_range)
            a_value = cls._a_range[0] if parameter_value <= cls._value_range[0] else cls._a_range[1]

            return [r_value, g_value, b_value, a_value]

        @classmethod
        def get_rgba_matrix_from_numpy_matrix(cls, np_matrix):
            """
            Depends on [cls._r, cls._g, cls._b, cls._values] variables from child class.
            :param np_matrix: Numpy 2D matrix with raw/comparison values
            """

            if np_matrix is None:
                return None

            rgba = np.zeros((4, np_matrix.shape[0], np_matrix.shape[1],), np.uint8)
            biggest_val = 0
            for cur_y in range(np_matrix.shape[0]):
                for cur_x in range(np_matrix.shape[1]):
                    cur_color = cls.get_color(np_matrix[cur_y][cur_x])
                    biggest_val = np_matrix[cur_y][cur_x] if np_matrix[cur_y][cur_x] > biggest_val else biggest_val
                    # print("{0} -> {1}".format(np_matrix[cur_y][cur_x], cur_color))
                    rgba[0, cur_y, cur_x] = cur_color[0]
                    rgba[1, cur_y, cur_x] = cur_color[1]
                    rgba[2, cur_y, cur_x] = cur_color[2]
                    rgba[3, cur_y, cur_x] = cur_color[3]

            print("Biggest value: {0}".format(biggest_val))
            return rgba

        @classmethod
        def _get_color_component(cls, parameter_value, color_range):
            """
            Gets the color considering gradient of value
            :param parameter_value:
            :param color_range:
            :return:
            """
            delta_color = color_range[1] - color_range[0]
            delta_value = cls._value_range[1] - cls._value_range[0]
            norm_value = parameter_value - cls._value_range[0]

            return (((100 * norm_value) / delta_value) * delta_color) + color_range[0]

    class ColorProvFIndex(ColorProvSingFather):
        _values = [-1, 0, 1, 2, 3, 4, 1000]
        _r = [0, 161, 250, 231, 222, 162]
        _g = [0, 218, 234, 139, 43, 22]
        _b = [0, 180, 0, 0, 0, 208]
        _a = [0, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvQUnitFIndex(ColorProvSingFather):
        _values = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1000]
        _r = [0, 255, 161, 65, 44, 37, 161, 250, 231, 222, 162]
        _g = [0, 255, 218, 182, 127, 52, 218, 234, 139, 43, 22]
        _b = [0, 204, 180, 196, 184, 148, 180, 0, 0, 0, 208]
        _a = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvFF(ColorProvSingFather):
        """
        Forecast Flood
        """
        _values = [0, 0.001, 0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2, 2.25, 2.5, 3,
                   1000000000]  # disch / base_discharge
        _r = [0, 0, 191, 80, 0, 221, 170, 82, 255, 247, 230, 240, 171, 255, 54, 54]
        _g = [0, 0, 255, 210, 166, 255, 255, 189, 255, 227, 153, 47, 0, 0, 37, 37]
        _b = [0, 0, 233, 250, 212, 153, 0, 0, 112, 0, 0, 34, 0, 0, 0, 0]
        _a = [0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvFQ(ColorProvSingFather):
        _values = [0.25, 1, 3, 5, 7.5, 12, 18, 27, 40, 60, 90, 135, 200, 300, 500, 750, 1000000000]  # discharge m3/sec
        _r = [0, 0, 191, 80, 0, 221, 170, 82, 255, 247, 230, 240, 171, 255, 54, 54]
        _g = [0, 0, 255, 210, 166, 255, 255, 189, 255, 227, 153, 47, 0, 0, 37, 37]
        _b = [0, 0, 233, 250, 212, 153, 0, 0, 112, 0, 0, 34, 0, 0, 0, 0]
        _a = [0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        def __init__(self):
            return

    class ColorProvCompSS(ColorProvCompFather):
        """
        Soil Storage Comparison
        """
        _inf = float('inf')
        _values = [-_inf, -300, -200, -100, -0.001, 0.001, 100, 200, 300, _inf]  # mm
        _r = [150, 178, 239, 253, 255, 209, 103, 33, 10]
        _g = [5, 24, 138, 219, 255, 229, 169, 102, 51]
        _b = [21, 43, 98, 199, 255, 240, 207, 172, 150]
        _a = [255, 255, 255, 255, 0, 255, 255, 255, 255]

        @classmethod
        def compare(cls, model1_value, model2_value):
            """

            :param model1_value: Value of soil storage in meters
            :param model2_value: Value of soil storage in meters
            :return: Value difference em mm unit
            """
            return (model1_value - model2_value) * 1000

        @classmethod
        def get_comparison_matrix(cls, model_1_matrix, model_2_matrix):
            """

            :param model_1_matrix: Numpy 2D float matrix in meters
            :param model_2_matrix: Numpy 2D float matrix in meters.
            :return: Numpy 2D float matrix in mm
            """
            return (model_1_matrix - model_2_matrix) * 1000

        def __init__(self):
            return

    class ColorProvCompSL(ColorProvCompFather):
        """
        Soil Moisture Comparison
        """
        _inf = float('inf')
        _values = [-_inf, 0.0000000000001, 0.25, 0.33, 0.5, 0.9, 1.1, 2, 3, 4, _inf]  # in ratio
        _r = [0, 150, 178, 239, 253, 255, 209, 103, 33, 10]
        _g = [0, 5, 24, 138, 219, 255, 229, 169, 102, 51]
        _b = [0, 21, 43, 98, 199, 255, 240, 207, 172, 150]
        _a = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        @classmethod
        def compare(cls, model1_value, model2_value):
            if (model1_value == 0) and (model2_value == 0):
                return 1
            elif (model1_value != 0) and (model2_value == 0):
                return 0
            else:
                ret_value = model1_value / model2_value
                return ret_value

        @classmethod
        def get_comparison_matrix(cls, model_1_matrix, model_2_matrix):
            """

            :param model_1_matrix: Numpy 2D float matrix with soil moisture percentage
            :param model_2_matrix: Numpy 2D float matrix with soil moisture percentage
            :return: Numpy 2D float matrix
            """
            vect_compare = np.vectorize(cls.compare, otypes=[np.float])  # vectorization of single values comparison
            return vect_compare(model_1_matrix, model_2_matrix)

        def __init__(self):
            return

    class ColorProvCompP(ColorProvCompFather):
        """
        Precipitation Comparison
        """
        _inf = float('inf')
        # _values = [-1000, -2,  -1, -0.5, -0.00000001, 0.00000001, 0.5,  1,   2,  1000]  # convert inches to m
        _values = np.asarray(
            [-_inf, -2, -1, -0.5, -0.0000001, 0.0000001, 0.5, 1, 2, _inf]) / 39.37  # convert inches to m
        _r = [150, 178, 239, 253, 255, 209, 103, 33, 10]
        _g = [5, 24, 138, 219, 255, 229, 169, 102, 51]
        _b = [21, 43, 98, 199, 255, 240, 207, 172, 150]
        _a = [255, 255, 255, 255, 0, 255, 255, 255, 255]

        @classmethod
        def compare(cls, model1_value, model2_value):
            return model1_value - model2_value

        @classmethod
        def get_comparison_matrix(cls, model_1_matrix, model_2_matrix):
            """

            :param model_1_matrix: Numpy 2D float matrix
            :param model_2_matrix: Numpy 2D float matrix
            :return: Numpy 2D float matrix
            """
            return model_1_matrix - model_2_matrix

        def __init__(self):
            return

    class ColorProvCompR(ColorProvCompP):
        """
        Runoff Comparison
        """
        _do = None  # identical to Precipitation

        def __init__(self):
            return

    class ColorProvCompQ(ColorProvCompFather):
        """
        Discharge Comparison
        """
        # _values = [10,  4,   3,   2,   1,  -1,  -2,  -3,  -4, -10]
        _values = [-99.1, -10, -3.1, -2.1, -1.1, -0.001, 0.001, 1.1, 2.1, 3.1, 10]
        _r = [255, 150, 178, 239, 253, 255, 209, 103, 33, 10]
        _g = [255, 5, 24, 138, 219, 255, 229, 169, 102, 51]
        _b = [255, 21, 43, 98, 199, 255, 240, 207, 172, 150]
        _a = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        def __init__(self):
            return

        @classmethod
        def class_comparison(cls, model1_class, model2_class):
            return model1_class - model2_class if ((model1_class != 0) and (model2_class != 0)) else -99

        @classmethod
        def compare(cls, model1_value, model2_value, data_month):
            model1_class = ColorProvider.ColorProvQ.get_pixel_color_index(model1_value, data_month)
            model2_class = ColorProvider.ColorProvQ.get_pixel_color_index(model2_value, data_month)
            return cls.class_comparison(model1_class, model2_class)

        @classmethod
        def get_comparison_matrix(cls, model_1_matrix, model_2_matrix, data_month):
            vectorized_comparison = np.vectorize(ColorProvider.ColorProvQ.get_pixel_color_index)
            model1_class_matrix = vectorized_comparison(model_1_matrix, data_month)
            model2_class_matrix = vectorized_comparison(model_2_matrix, data_month)
            v_comparison = np.vectorize(cls.class_comparison, otypes=[np.int])
            return v_comparison(model1_class_matrix, model2_class_matrix)

    class ColorProvCompQIndex(ColorProvCompFather):
        """
        Unit Discharge Index Comparison
        """
        _inf = float('inf')
        _values = [-_inf, -998, -3.1, -2.1, -1.1, -0.01, 0.01, 1.0, 2.0, 3.0, _inf]
        _r = [255, 150, 178, 239, 253, 255, 209, 103, 33, 10]
        _g = [255, 5, 24, 138, 219, 255, 229, 169, 102, 51]
        _b = [255, 21, 43, 98, 199, 255, 240, 207, 172, 150]
        _a = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        @classmethod
        def compare(cls, model1_value, model2_value):
            return -999 if model1_value == 0 else ((model1_value - model2_value) / model1_value)

        @classmethod
        def get_comparison_matrix(cls, model_1_matrix, model_2_matrix):
            vectorized_comparison = np.vectorize(cls.compare, otypes=[np.float])
            return vectorized_comparison(model_1_matrix, model_2_matrix)

    class ColorProvCompFIndex(ColorProvCompFather):
        """
        Flood Index Comparison
        """
        _inf = float('inf')
        _values = [-_inf, -998, -3, -2, -1, -0.01, 0.01, 1, 2, 3, _inf]
        _r = [255, 150, 178, 239, 253, 255, 209, 103, 33, 10]
        _g = [255, 5, 24, 138, 219, 255, 229, 169, 102, 51]
        _b = [255, 21, 43, 98, 199, 255, 240, 207, 172, 150]
        _a = [0, 255, 255, 255, 255, 255, 255, 255, 255, 255]

    class ColorProvCompFF(ColorProvCompFather):
        """
        Forecast Flood
        """
        _values = [-1000, -3, -2, -1, -0.1, 0.1, 1, 2, 3, 1000]  # disch / base_discharge
        _r = [255, 255, 255, 255, 255, 200, 150, 100, 0]
        _g = [0, 100, 150, 200, 255, 200, 150, 100, 0]
        _b = [0, 100, 150, 200, 255, 255, 255, 255, 255]
        _a = [255, 255, 255, 255, 0, 255, 255, 255, 255]

        def __init__(self):
            return

        @classmethod
        def compare(cls, model1_value, model2_value):
            return model1_value - model2_value  # TODO - correct it

        @classmethod
        def get_comparison_matrix(cls, model_1_matrix, model_2_matrix):
            """

            :param model_1_matrix: Numpy 2D float matrix
            :param model_2_matrix: Numpy 2D float matrix
            :return: Numpy 2D float matrix
            """
            return model_1_matrix - model_2_matrix

    class ColorProvCompFQ(ColorProvCompFather):
        """
        Forecast Discharge
        """
        _values = [0.25, 1, 3, 5, 7.5, 12, 18, 27, 40, 60, 90, 135, 200, 300, 500, 750, 1000000000]  # discharge m3/sec
        _r = [0, 0, 191, 80, 0, 221, 170, 82, 255, 247, 230, 240, 171, 255, 54, 54]
        _g = [0, 0, 255, 210, 166, 255, 255, 189, 255, 227, 153, 47, 0, 0, 37, 37]
        _b = [0, 0, 233, 250, 212, 153, 0, 0, 112, 0, 0, 34, 0, 0, 0, 0]
        _a = [0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

        def __init__(self):
            return

        @classmethod
        def compare(cls, model1_value, model2_value):
            return model1_value - model2_value  # TODO - correct it

    @classmethod
    def get_pixel_color(cls, parameter_acronym, parameter_value, par1=None):
        """

        :param parameter_acronym:
        :param parameter_value:
        :param par1: Extra generic parameter
        :return: Tuple representing color with format (R, G, B, A) if possible, None otherwise
        """

        if parameter_acronym is None:
            return None
        elif parameter_acronym in ('ss', 'soiwac20ih'):
            return cls.ColorProvSS.get_pixel_color(parameter_value)
        elif parameter_acronym == 'sl':
            return cls.ColorProvSL.get_pixel_color(parameter_value)
        elif parameter_acronym in ('p', 'p03', 'p06', 'p12'):
            return cls.ColorProvP.get_pixel_color(parameter_value)
        elif parameter_acronym in ('r', 'r03', 'r06', 'r12'):
            return cls.ColorProvR.get_pixel_color(parameter_value)
        elif parameter_acronym == 'q':
            return cls.ColorProvQ.get_pixel_color(parameter_value, par1)
        elif parameter_acronym == 'qindex':
            return cls.ColorProvQIndex.get_pixel_color(parameter_value)
        elif parameter_acronym == 'ff':
            return cls.ColorProvFF.get_pixel_color(parameter_value)
        elif parameter_acronym == 'fq':
            return cls.ColorProvQIndex.get_pixel_color(parameter_value)
        else:
            return None

    @classmethod
    def get_pixel_value_comparison(cls, parameter_acronym, model_1_parameter_value, model_2_parameter_value,
                                   par1=None, debug=False):
        """
        Just calculate the comparison matrix values, without going for the respective colors.
        Used for debugging proposes.
        :param parameter_acronym:
        :param model_1_parameter_value:
        :param model_2_parameter_value:
        :param par1: Extra generic parameter
        :param debug:
        :return: Tuple representing color with format (R, G, B, A) if possible, None otherwise
        """

        if parameter_acronym is None:
            return None
        elif parameter_acronym == 'ss':
            return cls.ColorProvCompSS.compare(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym == 'sl':
            return cls.ColorProvCompSL.compare(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym in ('p', 'p03', 'p06', 'p12'):
            return cls.ColorProvCompP.compare(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym in ('r', 'r03', 'r06', 'r12'):
            return cls.ColorProvCompR.compare(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym == 'q':
            return cls.ColorProvCompQ.compare(model_1_parameter_value, model_2_parameter_value, par1)
        elif parameter_acronym == 'ff':
            return cls.ColorProvCompFF.compare(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym == 'fq':
            return cls.ColorProvCompFQ.compare(model_1_parameter_value, model_2_parameter_value)
        else:
            return None

    @classmethod
    def get_pixel_color_comparison(cls, parameter_acronym,
                                   model_1_parameter_value,
                                   model_2_parameter_value,
                                   par1=None, debug=False):
        """

        :param parameter_acronym:
        :param model_1_parameter_value:
        :param model_2_parameter_value:
        :param par1: Extra generic parameter
        :param debug:
        :return: Tuple representing color with format (R, G, B, A) if possible, None otherwise
        """

        if parameter_acronym is None:
            return None
        elif parameter_acronym == 'ss':
            return cls.ColorProvCompSS.get_pixel_color(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym == 'sl':
            return cls.ColorProvCompSL.get_pixel_color(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym in ('p', 'p03', 'p06', 'p12'):
            return cls.ColorProvCompP.get_pixel_color(model_1_parameter_value, model_2_parameter_value, debug=debug)
        elif parameter_acronym in ('r', 'r03', 'r06', 'r12'):
            return cls.ColorProvCompR.get_pixel_color(model_1_parameter_value, model_2_parameter_value, debug=debug)
        elif parameter_acronym == 'q':
            return cls.ColorProvCompQ.get_pixel_color(model_1_parameter_value, model_2_parameter_value, par1)
        elif parameter_acronym == 'qindex':
            return cls.ColorProvCompQIndex.get_pixel_color(model_1_parameter_value, model_2_parameter_value)
        elif parameter_acronym == 'ff':
            return cls.ColorProvCompFF.get_pixel_color(model_1_parameter_value, model_2_parameter_value, debug)
        elif parameter_acronym == 'fq':
            return cls.ColorProvCompFQ.get_pixel_color(model_1_parameter_value, model_2_parameter_value)
        else:
            return None

    @classmethod
    def get_matrix_color(cls, parameter_acronym, model_matrix, par1=None, debug_lvl=False):
        """

        :param parameter_acronym:
        :param model_matrix:
        :param par1:
        :param debug_lvl:
        :return:
        """

        # TODO - implement this for every parameter
        if parameter_acronym is None:
            Debug.db("ColorProvider: Not merging matrix. None parameter.", debug)
            rgba_mtx = None
        elif parameter_acronym in ('soiwac20ih', 'soilowwacih'):
            rgba_mtx = cls.ColorProvSS.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'soimoi20ih':
            rgba_mtx = cls.ColorProvSL.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'podwacih':
            rgba_mtx = cls.ColorProvPd.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym in ('preacchil24hh', 'preacchil12hh', 'preacchil06hh', 'preacchil03hh', 'preacchildayh'):
            rgba_mtx = cls.ColorProvP.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'preacchilharbitrary':
            rgba_mtx = cls.ColorProvP.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym in ('runacchil24hh', 'runacchil12hh', 'runacchil06hh', 'runacchil03hh'):
            rgba_mtx = cls.ColorProvR.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'runacchilharbitrary':
            rgba_mtx = cls.ColorProvR.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'disclausgsih':
            rgba_mtx = cls.ColorProvQUnit.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'qraw':
            rgba_mtx = cls.ColorProvQraw.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'fldidxusgsih':
            rgba_mtx = cls.ColorProvFIndex.get_rgba_matrix_from_numpy_matrix(model_matrix)
        elif parameter_acronym == 'dcufldicupd':
            rgba_mtx = cls.ColorProvQUnitFIndex.get_rgba_matrix_from_numpy_matrix(model_matrix)
        else:
            Debug.dl(
                "ColorProvider: Not merging matrix. Parameter acronym sing. not defined '{0}'.".format(parameter_acronym),
                0,
                debug_lvl)
            rgba_mtx = None
        return rgba_mtx

    @classmethod
    def get_matrix_value_comparison(cls, parameter_acronym,
                                    model_1_matrix, model_2_matrix, par1=None, debug=False):
        """
        Just calculate the comparison matrix values, without going for the respective colors.
        Used for debugging proposes.
        :param parameter_acronym:
        :param model_1_matrix:
        :param model_2_matrix:
        :param par1:
        :param debug:
        :return:
        """
        # TODO - implement this for every parameter
        if parameter_acronym is None:
            Debug.db("Not merging matrix. None parameter.", debug)
            comparison_matrix = None
        elif parameter_acronym == 'ss':
            comparison_matrix = cls.ColorProvCompSS.get_comparison_matrix(model_1_matrix, model_2_matrix)
        elif parameter_acronym == 'sl':
            comparison_matrix = cls.ColorProvCompSL.get_comparison_matrix(model_1_matrix, model_2_matrix)
        elif parameter_acronym == 'p':
            comparison_matrix = cls.ColorProvCompP.get_comparison_matrix(model_1_matrix, model_2_matrix)
        elif parameter_acronym == 'r':
            comparison_matrix = cls.ColorProvCompR.get_comparison_matrix(model_1_matrix, model_2_matrix)
        elif parameter_acronym == 'q':
            comparison_matrix = cls.ColorProvCompQ.get_comparison_matrix(model_1_matrix, model_2_matrix, par1)
        elif parameter_acronym == 'qindex':
            comparison_matrix = cls.ColorProvCompQIndex.get_comparison_matrix(model_1_matrix, model_2_matrix)
        elif parameter_acronym == 'ff':
            comparison_matrix = cls.ColorProvCompFF.get_comparison_matrix(model_1_matrix, model_2_matrix)
        else:
            Debug.db("Not merging matrix. Parameter letter not defined: '{0}'.".format(parameter_acronym), debug)
            comparison_matrix = None
        return comparison_matrix

    @classmethod
    def get_matrix_color_comparison(cls, parameter_acronym, comp_matrix, par1=None, debug_lvl=0):
        """

        :param parameter_acronym:
        :param model_1_matrix:
        :param model_2_matrix:
        :param par1:
        :param debug:
        :return:
        """
        # TODO - implement this for every parameter
        if parameter_acronym is None:
            Debug.db("Not merging matrix. None parameter.", debug)
            rgba_mtx = None
        elif parameter_acronym in ('soiwac20ih', 'soilowwacih'):
            rgba_mtx = cls.ColorProvCompSS.get_rgba_matrix_from_numpy_matrix(comp_matrix)
        elif parameter_acronym == 'soimoi20ih':
            rgba_mtx = cls.ColorProvCompSL.get_rgba_matrix_from_numpy_matrix(comp_matrix)
        elif parameter_acronym in ('preacchil24hh', 'preacchil12hh', 'preacchil06hh', 'preacchil03hh'):
            rgba_mtx = cls.ColorProvCompP.get_rgba_matrix_from_numpy_matrix(comp_matrix)
        elif parameter_acronym in ('runacchil24hh', 'runacchil12hh', 'runacchil06hh', 'runacchil03hh'):
            rgba_mtx = cls.ColorProvCompR.get_rgba_matrix_from_numpy_matrix(comp_matrix)
        elif parameter_acronym == 'disclausgsih':
            rgba_mtx = cls.ColorProvCompQIndex.get_rgba_matrix_from_numpy_matrix(comp_matrix)
        elif parameter_acronym == 'fldidxusgsih':
            rgba_mtx = cls.ColorProvCompFIndex.get_rgba_matrix_from_numpy_matrix(comp_matrix)
        elif parameter_acronym == 'dcufldicuih':
            rgba_mtx = cls.ColorProvCompFIndex.get_rgba_matrix_from_numpy_matrix(comp_matrix)
        elif parameter_acronym == 'ff':
            comparison_matrix = cls.ColorProvCompFF.get_comparison_matrix(model_1_matrix, model_2_matrix)
            rgba_mtx = cls.ColorProvCompFF.get_rgba_matrix_from_numpy_matrix(comparison_matrix)
        else:
            Debug.dl("Not merging matrix. Parameter acronym not defined: '{0}'.".format(parameter_acronym), 1,
                     debug_lvl)
            rgba_mtx = None
        return rgba_mtx

    @staticmethod
    def save_matrix_color(matrix_color, image_full_file_path, image_ext_name, debug_lvl=0):
        """

        :param matrix_color:
        :param image_full_file_path:
        :param image_ext_name:
        :param debug_lvl:
        """
        if matrix_color is None:
            Debug.dl("ColorProvider: Image '{0}' not generated - None matrix object.".format(image_full_file_path),
                     0, debug_lvl)
            return
        gdalnumeric.SaveArray(matrix_color.astype(gdalnumeric.numpy.uint8), image_full_file_path, image_ext_name)
        ColorProvider.convert_rgba_to_indexed(image_full_file_path, image_full_file_path)
        Debug.dl("ColorProvider: Saved image '{0}'.".format(image_full_file_path), 1, debug_lvl)

    @staticmethod
    def convert_rgba_to_indexed(source_image_path, destiny_image_path, debug_lvl=0):
        """

        :param source_image_path:
        :param destiny_image_path:
        """
        im = Image.open(source_image_path)

        # PIL complains if you don't load explicitly
        im.load()

        # Get the alpha band
        alpha = im.split()[-1]

        im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=15)

        # Set all pixel values below 128 to 255,
        # and the rest to 0
        mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)

        # Paste the color of index 255 and use alpha as a mask
        im.paste(255, mask)

        # The transparency index is 255
        im.save(destiny_image_path, transparency=255)

        Debug.dl("ColorProvider: Converted RGB image {0} to indexed ({1}).".format(source_image_path, destiny_image_path),
                 2, debug_lvl)
