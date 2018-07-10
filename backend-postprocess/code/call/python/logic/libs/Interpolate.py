
class Interpolate:

    @staticmethod
    def my_interpolation_xy(x_set, y_set, the_x):

        # basic check
        if len(x_set) != len(y_set):
            return None

        for i in range(1, len(x_set)):
            if the_x == x_set[i]:
                return y_set[i]
            elif x_set[i - 1] <= the_x < x_set[i]:
                total_dist = x_set[i] - x_set[i - 1]
                weight_after = (the_x - x_set[i - 1]) / total_dist
                weight_before = (x_set[i] - the_x) / total_dist
                return (y_set[i - 1] * weight_before) + (y_set[i] * weight_after)

        # extrapolates if possible
        try:
            dist_from_last = the_x - x_set[-1]
            delta_h = x_set[-1] - x_set[-2]
            if delta_h == 0:
                delta_h = x_set[-1] - x_set[-3]
            delta_l = y_set[-1] - y_set[-2]
            dl_dh = delta_l / delta_h
            extrapolated_val = y_set[-1] + (dist_from_last * dl_dh)
            return extrapolated_val

        except Exception:
            return None
