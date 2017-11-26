<?php
	header("Content-Type: text/plain");
	include_once("ws_metainfo_lib.php");

	$sc_menu_folder_path = MetaInfoDefs::BASE_FOLDER_PATH.MetaInfoDefs::SCMENU_FOLDER;
	$sc_menu_file_name = MetaInfoDefs::SCMENU_FILENAME;
	$sc_menu_file_path = $sc_menu_folder_path."/".$sc_menu_file_name;
	
	print(file_get_contents($sc_menu_file_path));
?>