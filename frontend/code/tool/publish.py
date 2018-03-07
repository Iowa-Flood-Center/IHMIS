from libs.SettingsReader import SettingsReader
import shutil
import time
import os

# ###################################################### CONS ######################################################## #

ignored_subfolders = ['api_3_2',
                      '']

# ###################################################### CLAS ######################################################## #

class CopyChangerRec:

    _root_src = None
    _root_dst = None
    _count_c = None
    _count_m = None
    _count_f = None
    _ignored_subfolders = None

    def __init__(self, src, dst, ignored):
        self._root_src = src
        self._root_dst = dst
        self._count_c = 0
        self._count_m = 0
        self._count_f = 0
        self._ignored_subfolders = ignored

    def copy_change_recursivelly(self, sub_path=None):
        """

        :param sub_path:
        :return:
        """

        # check if in ignore
        if (self._ignored_subfolders is not None) and (sub_path in self._ignored_subfolders):
            print("Ignoring: {0}.".format(sub_path))
            return

        cur_root = self._root_src if sub_path is None else os.path.join(self._root_src, sub_path)
        print("Exploring: {0}".format(cur_root))
        all_src = os.listdir(cur_root)
        for cur_src in all_src:
            cur_src_full = os.path.join(cur_root, cur_src)
            mid_path = cur_src if sub_path is None else os.path.join(sub_path, cur_src)
            if os.path.isfile(cur_src_full):
                self.copy_file(mid_path)
            elif os.path.isdir(cur_src_full):
                self.create_folder(mid_path)
                self.copy_change_recursivelly(mid_path)

        return

    def get_summary(self):
        return self._count_c, self._count_m, self._count_f

    def create_folder(self, sub_path):
        """

        :param sub_path:
        :return:
        """
        new_path = os.path.join(self._root_dst, sub_path)
        if not os.path.exists(new_path):
            os.makedirs(new_path)

    def copy_file(self, sub_path):
        """

        :param sub_path:
        :return:
        """
        old_path = os.path.join(self._root_src, sub_path)
        new_path = os.path.join(self._root_dst, sub_path)
        if sub_path.endswith(".js") and not sub_path.endswith(".min.js"):
            self.uglify(new_path, old_path)
        else:
            self.copify(new_path, old_path)

    def uglify(self, new_path, old_path):
        """

        :param new_path:
        :param old_path:
        :return:
        """

        cmd_frame = "uglifyjs --compress --mangle -o {0} -- {1}"
        cmd_call = cmd_frame.format(new_path, old_path)
        if os.system(cmd_call) == 0:
            self._count_m += 1
        else:
            self._count_f += 1

    def copify(self, new_path, old_path):
        try:
            shutil.copy(old_path, new_path)
            self._count_c += 1
        except Error:
            self._count_f += 1


# ###################################################### CALL ######################################################## #

ini_time = time.time()

settings_reader = SettingsReader()

compresser = CopyChangerRec(settings_reader.get("dev_code_folder_path"),
                            settings_reader.get("dst_code_folder_path"),
                            ignored_subfolders)

compresser.copy_change_recursivelly()

num_c, num_m, num_f = compresser.get_summary()
print("Copied {0}, uglified {1}, failed {2}.".format(num_c, num_m, num_f))

print("Done in {0} seconds.".format(time.time() - ini_time))
