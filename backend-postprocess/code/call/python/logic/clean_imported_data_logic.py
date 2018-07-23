import os

from libs.FilenameDefinition import FilenameDefinition
from libs.FolderDefinition import FolderDefinition
from libs.MetaFileManager import MetaFileManager
from libs.FileDefinition import FileDefinition
from libs.Debug import Debug


def clean_historical(considered_model_ids, considered_reference_ids, runset_id, timestamp, previous_max_days, debug_lvl=0):
    """

    :param considered_model_ids:
    :param considered_reference_ids:
    :param runset_id:
    :param timestamp:
    :param previous_max_days:
    :param debug_lvl:
    :return:
    """

    if (considered_model_ids is None) and (considered_reference_ids is None):
        Debug.dl("clean_imported_data_logic: No sc_model or sc_reference id provided. Not cleaning.", 0, debug_lvl)
        return

    # load meta information
    meta_mng = MetaFileManager(runset_id=runset_id)
    meta_mng.load_all_scmodel_meta_info(debug_lvl=debug_lvl)
    meta_mng.load_all_screference_meta_info(debug_lvl=debug_lvl)

    if considered_model_ids is not None:
        total_int_del_files = 0
        for cur_model_id in considered_model_ids:
            total_int_del_files += clean_binary_files_of_scmodel(cur_model_id, runset_id, meta_mng, timestamp,
                                                                 previous_max_days, debug_lvl=debug_lvl)
        Debug.dl("clean_imported_data_logic: Deleted {0} intermediate binary files from models.".format(
            total_int_del_files), 1, debug_lvl)

    if considered_reference_ids is not None:
        total_int_del_files = 0
        for cur_reference_id in considered_reference_ids:
            total_int_del_files += clean_binary_files_of_screference(cur_reference_id, runset_id, meta_mng,
                                                                     timestamp, previous_max_days, debug_lvl=debug_lvl)
        Debug.dl("clean_imported_data_logic: Deleted {0} intermediate binary files from references.".format(
            total_int_del_files), 1, debug_lvl)

    return


def clean_binary_files_of_scmodel(sc_model_id, sc_runset_id, meta_mng, timestamp, previous_max_days, debug_lvl=0):
    """

    :param sc_model_id:
    :param meta_mng:
    :param timestamp:
    :param previous_max_days:
    :param debug_lvl:
    :return:
    """

    all_product_ids = meta_mng.get_all_products_of_scmodel(sc_model_id, debug_lvl=debug_lvl)
    print("  Model '{0}' has: {1}".format(sc_model_id, all_product_ids))
    return clean_binary_files(all_product_ids, sc_model_id, sc_runset_id, timestamp, previous_max_days,
                              debug_lvl=debug_lvl)


def clean_binary_files_of_screference(sc_model_id, sc_runset_id, meta_mng, timestamp, previous_max_days, debug_lvl=0):
    """

    :param sc_model_id:
    :param meta_mng:
    :param timestamp:
    :param previous_max_days:
    :param debug_lvl:
    :return:
    """

    all_product_ids = meta_mng.get_all_products_of_screference(sc_model_id, debug_lvl=debug_lvl)
    return clean_binary_files(all_product_ids, sc_model_id, sc_runset_id, timestamp, previous_max_days,
                              debug_lvl=debug_lvl)


def clean_binary_files(sc_products_ids, sc_model_id, sc_runset_id, timestamp, previous_max_days, debug_lvl=0):
    """

    :param sc_products_ids:
    :param sc_model_id:
    param sc_runset_id:
    :param timestamp:
    :param previous_max_days:
    :param debug_lvl:
    :return: Integer. Total binary files deleted
    """

    count_deleted_total = 0

    for cur_mdl_prod in sc_products_ids:

        count_deleted_prod = 0

        # define the reference timestamp
        hist_folder_path = FolderDefinition.get_intermediate_bin_folder_path(sc_model_id, cur_mdl_prod, sc_runset_id)
        if timestamp is None:
            max_timestamp = FolderDefinition.retrive_most_recent_timestamp_in_hist_folder(hist_folder_path)
        else:
            max_timestamp = timestamp
        if max_timestamp is None:
            Debug.dl("clean_imported_data_logic: No files in folder '{0}'.".format(hist_folder_path), 3, debug_lvl)
            continue

        # defines minimum timestamp
        min_timestamp = max_timestamp - (previous_max_days * 24 * 60 * 60)

        # delete everything between the boundaries
        all_file_names = [f for f in os.listdir(hist_folder_path) if os.path.isfile(os.path.join(hist_folder_path, f))]
        for cur_file_name in all_file_names:
            cur_timestamp = FilenameDefinition.obtain_hist_file_timestamp(cur_file_name)
            if not (min_timestamp <= cur_timestamp <= max_timestamp):
                cur_file_path = os.path.join(hist_folder_path, cur_file_name)
                Debug.dl("clean_imported_data_logic: Deleting '{0}'.".format(cur_file_path), 3, debug_lvl)
                os.remove(cur_file_path)
                count_deleted_prod += 1

        Debug.dl("clean_imported_data_logic: Deleted '{0}' files of {1}.{2}.".format(count_deleted_prod, sc_model_id,
                                                                                     cur_mdl_prod), 2, debug_lvl)
        Debug.dl("                               folder '{0}'.".format(hist_folder_path), 2, debug_lvl)
        count_deleted_total += count_deleted_prod

    Debug.dl("clean_imported_data_logic: Deleted '{0}' int. binary files of {1} model.".format(count_deleted_total,
                                                                                               sc_model_id),
             1, debug_lvl)

    return count_deleted_total
